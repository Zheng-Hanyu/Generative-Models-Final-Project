"""Parent-conditioned lattices and GPU tree construction, with the anchor at node zero."""

from dataclasses import dataclass

import torch
import triton
import triton.language as tl


@dataclass
class Tree:
    tokens: torch.Tensor
    parents: torch.Tensor
    depths: torch.Tensor

    def host(self):
        return (
            torch.stack((self.tokens, self.parents, self.depths), dim=-1).cpu().tolist()
        )


def markov_lattice(model, base, anchor, shortlist=2048, beam=32):
    """SpecPilot wide Markov lattice. Retain full-vocabulary tail mass before beam selection."""
    if model.draft_id_to_target_id is not None or getattr(
        model, "has_recurrent_markov_head", False
    ):
        raise ValueError(
            "This adapter requires the pinned full-vocabulary vanilla Markov head."
        )
    head = model.model.markov_head
    base = base.float()
    values, ids = base.topk(shortlist, dim=-1)
    total = base.logsumexp(-1)
    tail = total + torch.log1p(
        -(values.logsumexp(-1) - total).exp().clamp(max=1 - 1e-7)
    )
    keys = head.markov_w2.weight[ids]
    parent = anchor.long().reshape(1, 1)
    path = torch.zeros_like(parent, dtype=torch.float32)
    candidates, edges = [], []
    for slot in range(base.size(1)):
        bias = torch.bmm(head.markov_w1(parent), keys[:, slot].transpose(1, 2)).float()
        logits = values[:, slot, None] + bias * model.logits_processor.scale
        logp = (
            logits
            - torch.logaddexp(logits.logsumexp(-1), tail[:, slot, None])[..., None]
        )
        path, chosen = (path[..., None] + logp).amax(1).topk(beam)
        parent = ids[:, slot].gather(1, chosen)
        candidates.append(parent)
        edges.append(
            logp.gather(2, chosen[:, None].expand(-1, logp.size(1), -1)).expand(
                -1, beam, -1
            )
        )
    return torch.stack(candidates, 1), torch.stack(edges, 1)


@triton.jit
def _grow(
    ids,
    ordered,
    logp,
    anchor,
    tokens,
    parents,
    depths,
    S: tl.constexpr,
    K: tl.constexpr,
    C: tl.constexpr,
    N: tl.constexpr,
    P: tl.constexpr,
    FIXED: tl.constexpr,
):
    # One CTA per request. Frontier entries encode parent node and conditional child rank.
    b = tl.program_id(0)
    offsets = tl.arange(0, P)
    tl.store(tokens + b * N, tl.load(anchor + b))
    tl.store(parents + b * N, -1)
    tl.store(depths + b * N, 0)
    row = b * S * K * C
    frontier = tl.load(logp + row + offsets, mask=offsets < C, other=-float("inf"))
    ranks = tl.load(ordered + row + offsets, mask=offsets < C, other=0)
    levels = tl.full((P,), 1, tl.int32)
    for i in range(1, N):
        if FIXED:
            choice = i - 1
        else:
            choice = tl.argmax(frontier, 0, tie_break_left=True)
        rank = tl.sum(tl.where(offsets == choice, ranks, 0), 0)
        depth = tl.sum(tl.where(offsets == choice, levels, 0), 0)
        score = tl.max(tl.where(offsets == choice, frontier, -float("inf")), 0)
        token = tl.load(ids + (b * S + depth - 1) * K + rank)
        tl.store(tokens + b * N + i, token)
        tl.store(parents + b * N + i, choice // C)
        tl.store(depths + b * N + i, depth)
        new = (offsets // C == i) & (depth < S)
        src = ((b * S + depth) * K + rank) * C + offsets % C
        child = tl.load(logp + src, mask=new, other=-float("inf"))
        child_rank = tl.load(ordered + src, mask=new, other=0)
        frontier = tl.where(
            new, score + child, tl.where(offsets == choice, -float("inf"), frontier)
        )
        ranks = tl.where(new, child_rank, ranks)
        levels = tl.where(new, depth + 1, levels)


def build(ids, edges, anchor, mode, budget, branching, max_depth):
    """Edges are already normalized on the original lattice, before branching is capped."""
    if (
        mode not in ("fixed", "best")
        or budget < 1
        or max_depth < 1
        or not 1 <= branching <= ids.size(-1)
    ):
        raise ValueError("Invalid tree configuration")
    steps = min(max_depth, ids.shape[1])
    count = min(budget, sum(branching**d for d in range(steps + 1)))
    ids = ids[:, :steps].contiguous()
    # Stable ordering makes equal-score children deterministic on both backends.
    ranks = torch.argsort(edges[:, :steps], dim=-1, descending=True, stable=True)[
        ..., :branching
    ].contiguous()
    scores = edges[:, :steps].gather(-1, ranks).contiguous()
    shape = (ids.size(0), count)
    tree = Tree(
        *(torch.empty(shape, device=ids.device, dtype=torch.long) for _ in range(3))
    )
    _grow[(ids.size(0),)](
        ids,
        ranks.int(),
        scores,
        anchor.contiguous(),
        tree.tokens,
        tree.parents,
        tree.depths,
        steps,
        ids.size(-1),
        branching,
        count,
        triton.next_power_of_2(count * branching),
        mode == "fixed",
    )
    return tree
