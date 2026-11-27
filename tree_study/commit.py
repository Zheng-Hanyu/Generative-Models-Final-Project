"""Greedy path selection and batched cache compaction for a batch-one verifier."""

import torch
import triton
import triton.language as tl


@triton.jit
def _select(
    token,
    parent,
    pred,
    path,
    emitted,
    count,
    rejected,
    N: tl.constexpr,
    P: tl.constexpr,
):
    i = tl.arange(0, P)
    tokens = tl.load(token + i, i < N, other=-1)
    parents = tl.load(parent + i, i < N, other=-2)
    node = 0
    length = 0
    while node >= 0:
        next_id = tl.load(pred + node)
        tl.store(path + length, node)
        tl.store(emitted + length, next_id)
        length += 1
        node = tl.max(tl.where((parents == node) & (tokens == next_id), i, -1), 0)
    tl.store(count, length)
    tl.store(rejected, N - length)


@triton.jit
def _state_copy(
    ptrs, path, count, S: tl.constexpr, SIZE: tl.constexpr, BLOCK: tl.constexpr
):
    layer = tl.program_id(0)
    i = tl.program_id(1) * BLOCK + tl.arange(0, BLOCK)
    state = tl.load(ptrs + layer * 5).to(tl.pointer_type(tl.float32))
    slots = tl.load(ptrs + layer * 5 + 1).to(tl.pointer_type(tl.int32))
    last = tl.load(count) - 1
    leaf = tl.load(path + last)
    if last != leaf:
        src = tl.load(slots + leaf).to(tl.int64)
        dst = tl.load(slots + last).to(tl.int64)
        val = tl.load(state + src * S + i, i < SIZE, other=0)
        tl.store(state + dst * S + i, val, i < SIZE)


@triton.jit
def _conv_commit(
    ptrs,
    path,
    count,
    window,
    D: tl.constexpr,
    SH: tl.constexpr,
    SD: tl.constexpr,
    ST: tl.constexpr,
    SX: tl.constexpr,
    BLOCK: tl.constexpr,
):
    layer = tl.program_id(0)
    col = tl.program_id(1) * BLOCK + tl.arange(0, BLOCK)
    slots = tl.load(ptrs + layer * 5 + 1).to(tl.pointer_type(tl.int32))
    conv = tl.load(ptrs + layer * 5 + 2).to(tl.pointer_type(tl.bfloat16))
    raw = tl.load(ptrs + layer * 5 + 3).to(tl.pointer_type(tl.bfloat16))
    previous = tl.load(ptrs + layer * 5 + 4).to(tl.pointer_type(tl.int32))
    last = tl.load(count) - 1
    leaf = tl.load(path + last)
    base = conv + tl.load(slots).to(tl.int64) * SH
    offset = tl.load(previous) - 1
    j = tl.arange(0, 4)
    source = tl.load(window + leaf * 4 + j)
    hist = tl.load(
        base + (offset + 3 + source[:, None]) * ST + col[None, :] * SD,
        (source[:, None] < 0) & (col[None, :] < D),
        other=0,
    )
    val = tl.load(
        raw + source[:, None] * SX + col[None, :],
        (source[:, None] >= 0) & (col[None, :] < D),
        other=0,
    )
    result = tl.where(source[:, None] < 0, hist, val)
    tl.debug_barrier()
    tl.store(
        base + (last + j[:, None] - 1) * ST + col[None, :] * SD,
        result,
        (j[:, None] > 0) & (col[None, :] < D),
    )


@triton.jit
def _kv_commit(
    ptrs,
    path,
    count,
    PAGE: tl.constexpr,
    SB: tl.constexpr,
    SP: tl.constexpr,
    SH: tl.constexpr,
    WIDTH: tl.constexpr,
    HEADS: tl.constexpr,
    BLOCK: tl.constexpr,
):
    layer = tl.program_id(0)
    i = tl.program_id(1) * BLOCK + tl.arange(0, BLOCK)
    cache = tl.load(ptrs + layer * 2).to(tl.pointer_type(tl.bfloat16))
    slots = tl.load(ptrs + layer * 2 + 1).to(tl.pointer_type(tl.int64))
    offset = (i // WIDTH) * SH + i % WIDTH
    for dest in range(1, tl.load(count)):
        source = tl.load(path + dest)
        if source != dest:
            src = tl.load(slots + source)
            dst = tl.load(slots + dest)
            val = tl.load(
                cache + src // PAGE * SB + src % PAGE * SP + offset,
                i < HEADS * WIDTH,
                other=0,
            )
            tl.store(
                cache + dst // PAGE * SB + dst % PAGE * SP + offset,
                val,
                i < HEADS * WIDTH,
            )
            tl.debug_barrier()


def select_and_commit(tree, n, pred, window, records):
    dev = pred.device
    path = torch.zeros(n, device=dev, dtype=torch.int64)
    out = torch.full((1, n), -1, device=dev, dtype=torch.int64)
    count = torch.empty(1, device=dev, dtype=torch.int32)
    rejected = torch.empty_like(count)
    _select[(1,)](
        tree.tokens,
        tree.parents,
        pred,
        path,
        out,
        count,
        rejected,
        n,
        triton.next_power_of_2(n),
    )
    recurrent = [r[1:] for r in records if r[0] == "gdn"]
    attention = [r[1:] for r in records if r[0] == "kv"]
    state, slots, conv, raw, previous = recurrent[0]
    assert slots.dtype == previous.dtype == torch.int32 and state.dtype == torch.float32
    assert raw.dtype == conv.dtype == torch.bfloat16
    rp = torch.tensor(
        [[t.data_ptr() for t in r] for r in recurrent], device=dev, dtype=torch.int64
    )
    state_size = state[0].numel()
    _state_copy[(len(recurrent), triton.cdiv(state_size, 1024))](
        rp, path, count, state.stride(0), state_size, 1024
    )
    d = raw.shape[-1]
    _conv_commit[(len(recurrent), triton.cdiv(d, 128))](
        rp, path, count, window, d, *conv.stride(), raw.stride(0), 128
    )
    pages, loc = attention[0]
    assert (
        loc.dtype == torch.int64
        and pages.dtype == torch.bfloat16
        and pages.stride(-1) == 1
    )
    kp = torch.tensor(
        [[p.data_ptr(), s.data_ptr()] for p, s in attention],
        device=dev,
        dtype=torch.int64,
    )
    _, page, heads, width = pages.shape
    _kv_commit[(len(attention), triton.cdiv(width * heads, 128))](
        kp, path, count, page, *pages.stride()[:3], width, heads, 128
    )
    return path, out, count, rejected
