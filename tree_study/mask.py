"""Ancestor bitmask/window layout for the packed tree verifier; one 32-bit word per query."""

import triton
import triton.language as tl


@triton.jit
def layout(parent, mask, window, N: tl.constexpr, P: tl.constexpr):
    i = tl.arange(0, P)
    node = i
    bits = tl.full((P,), 0, tl.uint32)
    for d in range(max(N, 4)):
        valid = (i < N) & (node >= 0)
        bits |= tl.where(valid, tl.full((P,), 1, tl.uint32) << (node & 31), 0)
        if d < 4:
            tl.store(window + i * 4 + 3 - d, node, i < N)
        prev = tl.load(parent + node, valid, other=-1).to(tl.int32)
        node = tl.where(node >= 0, prev, node - 1)
    tl.store(mask + i, bits, i < N)
