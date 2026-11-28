"""Batch-one packed vLLM verifier for the pinned Qwen hybrid target.

The scheduler allocates ordinary speculative slots. Attention sees the prefix
and node ancestors. Each GDN node has its own native speculative state slot.
After verification the accepted KV rows, convolution window, state and hidden
rows are put in the positions expected by the stock vLLM continuation.
"""

from dataclasses import replace

import torch
import triton
import triton.language as tl


@triton.jit
def _gather_kv(
    cache,
    table,
    indices,
    out,
    PAGE: tl.constexpr,
    HEADS: tl.constexpr,
    WIDTH: tl.constexpr,
    SB: tl.constexpr,
    SP: tl.constexpr,
    SH: tl.constexpr,
    BLOCK: tl.constexpr,
):
    row = tl.program_id(0)
    offset = tl.program_id(1) * BLOCK + tl.arange(0, BLOCK)
    token = tl.load(indices + row)
    page = tl.load(table + token // PAGE).to(tl.int64)
    src = page * SB + (token % PAGE) * SP + (offset // WIDTH) * SH + offset % WIDTH
    value = tl.load(cache + src, offset < HEADS * WIDTH, other=0)
    tl.store(out + row * HEADS * WIDTH + offset, value, offset < HEADS * WIDTH)


@triton.jit
def _conv(
    x,
    w,
    hist,
    slots,
    previous,
    window,
    out,
    D: tl.constexpr,
    W: tl.constexpr,
    SX: tl.constexpr,
    SW: tl.constexpr,
    SH: tl.constexpr,
    SD: tl.constexpr,
    ST: tl.constexpr,
    BLOCK: tl.constexpr,
):
    node = tl.program_id(0)
    col = tl.program_id(1) * BLOCK + tl.arange(0, BLOCK)
    slot = tl.load(slots).to(tl.int64)
    offset = tl.load(previous) - 1
    acc = tl.full((BLOCK,), 0, tl.float32)
    for j in tl.static_range(W):
        row = tl.load(window + node * W + j)
        val = tl.load(x + row * SX + col, mask=(row >= 0) & (col < D), other=0)
        old = tl.load(
            hist + slot * SH + col * SD + (offset + W - 1 + row) * ST,
            mask=(row < 0) & (col < D),
            other=0,
        )
        weight = tl.load(w + col * SW + j, mask=col < D, other=0)
        acc += tl.where(row >= 0, val, old) * weight
    tl.store(out + node * D + col, acc / (1 + tl.exp(-acc)), mask=col < D)


@triton.jit
def _recur(
    x,
    a,
    b,
    A,
    dt,
    parents,
    slots,
    previous,
    state,
    out,
    N: tl.constexpr,
    H: tl.constexpr,
    HV: tl.constexpr,
    K: tl.constexpr,
    V: tl.constexpr,
    D: tl.constexpr,
    SA: tl.constexpr,
    SB: tl.constexpr,
    SS: tl.constexpr,
    BV: tl.constexpr,
):
    # Parent-indexed extension of vLLM's fused_sigmoid_gating_delta_rule_update
    # (Apache-2.0). One CTA owns its state tile throughout the topological walk.
    head = tl.program_id(0)
    vk = tl.arange(0, K)
    vv = tl.program_id(1) * BV + tl.arange(0, BV)
    tile = head * V * K + vv[:, None] * K + vk[None, :]
    qh = head // (HV // H)
    decay = -tl.exp(tl.load(A + head).to(tl.float32))
    bias = tl.load(dt + head).to(tl.float32)
    old_slot = tl.load(slots + tl.load(previous) - 1)
    for node in range(N):
        parent = tl.load(parents + node)
        src = tl.load(slots + tl.maximum(parent, 0))
        src = tl.where(node == 0, old_slot, src).to(tl.int64)
        mat = tl.load(state + src * SS + tile).to(tl.float32)
        q = tl.load(x + node * D + qh * K + vk).to(tl.float32)
        key = tl.load(x + node * D + H * K + qh * K + vk).to(tl.float32)
        val = tl.load(x + node * D + 2 * H * K + head * V + vv).to(tl.float32)
        q *= tl.rsqrt(tl.sum(q * q, 0) + 1.0e-6)
        q *= K**-0.5
        key *= tl.rsqrt(tl.sum(key * key, 0) + 1.0e-6)
        z = tl.load(a + node * SA + head).to(tl.float32) + bias
        mat *= tl.exp(decay * tl.where(z <= 20.0, tl.log(1.0 + tl.exp(z)), z))
        beta = tl.sigmoid(tl.load(b + node * SB + head).to(tl.float32))
        # Match the SM100 vLLM 0.34 GDN reduction: the last four value rows
        # in a 32-row tile contract the first product of each pair into an FMA.
        # Even one ULP in this prediction can persist in the recurrent state.
        lo, hi = tl.split(tl.permute(tl.reshape(mat, (BV, K // 4, 2, 2)), (0, 1, 3, 2)))
        kl, kh = tl.split(tl.permute(tl.reshape(key, (K // 4, 2, 2)), (0, 2, 1)))
        pairs = tl.fma(lo, kl[None, :, :], hi * kh[None, :, :])
        tail_prediction = tl.sum(tl.sum(pairs, 2), 1)
        prediction = tl.where(vv % 32 >= 28, tail_prediction, tl.sum(mat * key[None, :], 1))
        update = (val - prediction) * beta
        mat += update[:, None] * key[None, :]
        tl.store(out + (node * HV + head) * V + vv, tl.sum(mat * q[None, :], 1))
        dest = tl.load(slots + node).to(tl.int64)
        tl.store(state + dest * SS + tile, mat)
        tl.debug_barrier()


class PackedVerifier:
    def __init__(self):
        self.fused_kv = False
        self.mlp_graph = False
        self.mlp_graphs = {}
        self.active = False
        self.tree = None
        self.path = None
        self.layers = []

    def begin(self, batch, tree):
        # The scheduler may shorten the final lookahead. A best-first/BFS
        # prefix remains prefix-closed.
        n = batch.num_tokens
        if n != batch.num_draft_tokens + 1 or n > tree.tokens.shape[1]:
            raise ValueError("Expected a single speculative decode batch")
        self.tree = tree
        self.n = n
        from .mask import layout

        self.parent = tree.parents[0, :n].contiguous()
        self.depth = tree.depths[0, :n]
        self.bits = torch.empty(n, device=self.depth.device, dtype=torch.int32)
        self.window = torch.empty((n, 4), device=self.depth.device, dtype=torch.int64)
        layout[(1,)](self.parent, self.bits, self.window, n, triton.next_power_of_2(n))
        self.layers = []
        self.active = True
        self.attention_index = None

    def gdn(self, layer, mixed_qkv, b, a, core_attn_out):
        from vllm.forward_context import get_forward_context
        from vllm.model_executor.layers.mamba.mamba_utils import is_conv_state_dim_first

        meta = get_forward_context().attn_metadata[layer.prefix]
        slots = meta.spec_state_indices_tensor[0]
        previous = meta.num_accepted_tokens
        conv, state = layer.kv_cache
        if not is_conv_state_dim_first():
            conv = conv.transpose(-1, -2)
        w = layer.conv1d.weight.squeeze(1)
        assert w.shape[1] == 4 and layer.conv1d.bias is None and state.stride(-1) == 1
        n, d = self.n, mixed_qkv.shape[-1]
        x = torch.empty((n, d), device=a.device, dtype=mixed_qkv.dtype)
        _conv[(n, triton.cdiv(d, 256))](
            mixed_qkv,
            w,
            conv,
            slots,
            previous,
            self.window,
            x,
            d,
            4,
            mixed_qkv.stride(0),
            w.stride(0),
            *conv.stride(),
            256,
        )
        hv = layer.num_v_heads
        h = layer.num_k_heads
        k, v = layer.head_k_dim, layer.head_v_dim
        assert (
            state.stride(-2) == k and state.stride(-3) == v * k and layer.tp_size == 1
        )
        _recur[(hv, v // 16)](
            x,
            a,
            b,
            layer.A_log,
            layer.dt_bias,
            self.parent,
            slots,
            previous,
            state,
            core_attn_out,
            n,
            h,
            hv,
            k,
            v,
            d,
            a.stride(0),
            b.stride(0),
            state.stride(0),
            16,
        )
        self.layers.append(("gdn", state, slots, conv, mixed_qkv, previous))

    def accept(self, runner, hidden, batch):
        from vllm.v1.worker.gpu.sample.output import SamplerOutput

        pred = runner.model_state.compute_sample_logits(
            hidden[batch.logits_indices]
        ).argmax(-1)
        from .commit import select_and_commit

        self.path, out, count, rejected = select_and_commit(
            self.tree, self.n, pred, self.window, self.layers
        )
        self.layers.clear()
        self.active = False
        return SamplerOutput(out, None, None, count, rejected), count, rejected

    def install(self):
        from vllm.model_executor.models.qwen3_5 import Qwen3NextMLP

        original_mlp = Qwen3NextMLP.forward

        def mlp(layer, x):
            if not self.active or not self.mlp_graph or x.shape[0] != 32:
                return original_mlp(layer, x)
            if layer not in self.mlp_graphs:
                static = x.clone()
                graph = torch.cuda.CUDAGraph()
                with torch.cuda.graph(graph):
                    output = original_mlp(layer, static)
                self.mlp_graphs[layer] = (graph, static, output)
            graph, static, output = self.mlp_graphs[layer]
            static.copy_(x)
            graph.replay()
            return output

        Qwen3NextMLP.forward = mlp
        from vllm.model_executor.layers.linear import UnquantizedLinearMethod
        from vllm.model_executor.layers.quantization.fp8 import Fp8LinearMethod
        from vllm.model_executor.layers.vocab_parallel_embedding import (
            UnquantizedEmbeddingMethod,
        )

        def align_rows(original):
            def apply(method, layer, x, *args, **kwargs):
                if (
                    self.active
                    and isinstance(x, torch.Tensor)
                    and x.ndim == 2
                    and x.shape[0] in (9, 17, 24)
                ):
                    rows = x.shape[0]
                    padded = torch.nn.functional.pad(
                        x, (0, 0, 0, triton.next_power_of_2(rows) - rows)
                    )
                    return original(method, layer, padded, *args, **kwargs)[:rows]
                return original(method, layer, x, *args, **kwargs)

            return apply

        for cls in (
            UnquantizedLinearMethod,
            UnquantizedEmbeddingMethod,
            Fp8LinearMethod,
        ):
            cls.apply = align_rows(cls.apply)
        from vllm.model_executor.layers.mamba.gdn.qwen_gdn_linear_attn import (
            QwenGatedDeltaNetAttention as GDN,
        )
        from vllm.v1.attention.backends.flash_attn import FlashAttentionImpl
        from vllm.v1.worker.gpu.model_states.default import DefaultModelState

        original_inputs = DefaultModelState.prepare_inputs
        original_attn = FlashAttentionImpl.forward
        original_gdn = GDN._forward_core
        original_fused = GDN._can_use_fused_gdn_mtp_decode

        def inputs(model, batch, states):
            data = original_inputs(model, batch, states)
            if self.active:
                pos = data.get("positions", batch.positions)
                # This experiment uses text-only prompts. Preserve multimodal
                # RoPE axis offsets already supplied by the engine.
                data["positions"] = pos[..., :1] + self.depth
            return data

        def attn(
            impl, layer, query, key, value, kv_cache, attn_metadata, output, *args, **kw
        ):
            if self.active:
                # Present a compact chronological KV sequence for every query
                # to the engine's stock FA4 kernel in one launch.
                pages = kv_cache.transpose(1, 2)
                if self.attention_index is None:
                    n = self.n
                    device = query.device
                    prefix = int(attn_metadata.seq_lens[0]) - n
                    page = pages.shape[1]
                    num_pages = triton.cdiv(prefix + n, page)
                    col = torch.arange(num_pages * page, device=device)
                    # Ancestors precede descendants in both builder layouts.
                    idx = torch.arange(n, device=device)
                    member = ((self.bits[:, None] >> idx) & 1).bool()
                    paths = torch.where(member, idx, n).sort(-1).values
                    chosen = paths[:, (col - prefix).clamp(0, n - 1)].clamp_max(n - 1)
                    self.attention_index = torch.where(
                        col < prefix, col, prefix + chosen
                    )
                    self.virtual_meta = replace(
                        attn_metadata,
                        max_query_len=1,
                        max_seq_len=prefix + n,
                        seq_lens=(prefix + self.depth + 1).int(),
                        query_start_loc=torch.arange(
                            n + 1, device=device, dtype=torch.int32
                        ),
                        block_table=torch.arange(
                            n * num_pages, device=device, dtype=torch.int32
                        ).view(n, num_pages),
                        scheduler_metadata=None,
                    )
                idx = self.attention_index
                size = pages.shape[1]
                if self.fused_kv:
                    heads, width = pages.shape[2:]
                    assert (
                        pages.stride(-1) == attn_metadata.block_table.stride(-1) == 1
                        and idx.is_contiguous()
                    )
                    scratch = pages.new_empty((idx.numel(), heads, width))
                    _gather_kv[(idx.numel(), triton.cdiv(heads * width, 256))](
                        pages,
                        attn_metadata.block_table,
                        idx,
                        scratch,
                        size,
                        heads,
                        width,
                        *pages.stride()[:3],
                        256,
                    )
                else:
                    scratch = pages[
                        attn_metadata.block_table[0, idx // size].long(), idx % size
                    ]
                scratch = scratch.reshape(-1, size, *pages.shape[2:]).transpose(1, 2)
                self.layers.append(("kv", pages, attn_metadata.slot_mapping))
                return original_attn(
                    impl,
                    layer,
                    query,
                    key,
                    value,
                    scratch,
                    self.virtual_meta,
                    output,
                    *args,
                    **kw,
                )
            return original_attn(
                impl,
                layer,
                query,
                key,
                value,
                kv_cache,
                attn_metadata,
                output,
                *args,
                **kw,
            )

        def core(layer, mixed_qkv, b, a, core_attn_out):
            if self.active:
                return self.gdn(layer, mixed_qkv, b, a, core_attn_out)
            return original_gdn(layer, mixed_qkv, b, a, core_attn_out)

        DefaultModelState.prepare_inputs = inputs
        FlashAttentionImpl.forward = attn
        GDN._forward_core = core
        GDN._can_use_fused_gdn_mtp_decode = lambda layer, meta: (
            not self.active and original_fused(layer, meta)
        )
