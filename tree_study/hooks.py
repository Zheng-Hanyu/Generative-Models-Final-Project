"""Process-local instrumentation for the pinned vLLM V2 worker, TP=1, eager, synchronous scheduling."""

import copy
import os

import torch
from .trees import Tree, build, markov_lattice


def event():
    e = torch.cuda.Event(enable_timing=True)
    e.record()
    return e


class Study:
    def __init__(self, slots=7, capacity=None):
        self.slots = slots
        self.capacity = capacity or slots
        self.shared_chain = False
        self.graphs = {}
        self.detailed = os.getenv("TREE_TELEMETRY") == "1"
        from .packed import PackedVerifier

        self.verifier = PackedVerifier()
        self.start("off", 8, 1, 7)

    def start(self, mode, budget, branching, depth):
        self.mode, self.budget, self.branching, self.depth = (
            mode,
            budget,
            branching,
            depth,
        )
        self.traces = []
        self.tree = None
        self.verifier.active = False
        self.verifier.path = None
        self.req = None
        self.width = None
        self.events = {k: [] for k in ("draft", "build", "verify")}
        if self.detailed:
            self.events.update(prefill=[], target_forward=[], sample_commit=[])
        self.rounds = []
        self.current = None
        self.verify_start = None
        self.chain_tokens = None
        self.edges = None

    def metrics(self):
        torch.cuda.synchronize()
        return {
            "rounds": self.rounds,
            "stage_ms": {
                k: sum(a.elapsed_time(b) for a, b in v) for k, v in self.events.items()
            },
        }

    def install(self):
        from vllm.v1.worker.gpu.model_runner import GPUModelRunner
        from vllm.v1.worker.gpu.spec_decode.dflash.speculator import DFlashSpeculator
        from vllm.v1.worker.gpu.spec_decode.dflash2.speculator import DFlash2Speculator
        from vllm.v1.worker.gpu.spec_decode.dspark.speculator import DSparkSpeculator
        from vllm.v1.worker.gpu.spec_decode.utils import DraftTokensHandler

        original_sample = GPUModelRunner.sample
        original_execute = GPUModelRunner.execute_model
        original_propose = DFlashSpeculator.propose
        original_set = DraftTokensHandler.set_draft_tokens
        original_prepare = GPUModelRunner.prepare_attn
        original_init = DFlashSpeculator.__init__
        original_ds = DSparkSpeculator._sample_sequential
        original_df = DFlash2Speculator._generate_draft

        def init(spec, vllm_config, device):
            config = copy.copy(vllm_config)
            config.speculative_config = copy.copy(config.speculative_config)
            config.speculative_config.num_speculative_tokens = self.slots
            original_init(spec, config, device)

        def prepare(runner, input_batch):
            result = original_prepare(runner, input_batch)
            if self.tree is not None and input_batch.num_draft_tokens:
                self.verifier.begin(input_batch, self.tree)
            return result

        def execute(runner, *args, **kwargs):
            if self.mode not in ("off", "capture") and self.current is not None:
                self.verify_start = event()
            elif self.detailed and self.mode not in ("off", "capture"):
                self.prefill_start = event()
            return original_execute(runner, *args, **kwargs)

        def sample(runner, hidden, batch, grammar):
            detailed = self.detailed and self.mode not in ("off", "capture")
            if detailed:
                forward_end = event()
            if self.verifier.active:
                result = self.verifier.accept(runner, hidden, batch)
            else:
                result = original_sample(runner, hidden, batch, grammar)
            if detailed:
                if self.current is None:
                    self.events["prefill"].append((self.prefill_start, event()))
                else:
                    self.events["target_forward"].append(
                        (self.verify_start, forward_end)
                    )
                    self.events["sample_commit"].append((forward_end, event()))
            if self.mode == "capture":
                sampled, count, _ = result
                if int(count[0]) != 1 or batch.num_draft_tokens:
                    raise RuntimeError(
                        f"Replay requires one AR step, got {int(count[0])} with {batch.num_draft_tokens} drafts"
                    )
                sampled.sampled_token_ids[0, 0] = self.truth[len(self.traces)]
                return result
            if self.mode in ("off", "capture") or self.current is None:
                return result
            self.events["verify"].append((self.verify_start, event()))
            sampled, count, _ = result
            committed = int(count[0])
            self.current["steps"] += 1
            self.current["verified_inputs"] += int(batch.num_tokens)
            self.current["committed"] += committed
            self.rounds.append(self.current)
            self.current = self.tree = None
            return result

        def record_lattice(spec, ids, edges, anchor):
            self.edges = (ids, edges, anchor)
            if self.mode == "capture":
                return
            start = event()
            key = (self.mode, self.budget, self.branching, self.depth)
            if os.getenv("TREE_CUDA_GRAPH", "1") == "1":
                if key not in self.graphs:
                    buffers = tuple(t.clone() for t in (ids, edges, anchor))
                    build(*buffers, *key)
                    graph = torch.cuda.CUDAGraph()
                    with torch.cuda.graph(graph):
                        output = build(*buffers, *key)
                    self.graphs[key] = (buffers, graph, output)
                buffers, graph, nodes = self.graphs[key]
                for dst, src in zip(buffers, (ids, edges, anchor)):
                    dst.copy_(src)
                graph.replay()
            else:
                nodes = build(ids, edges, anchor, *key)
            self.tree = nodes
            self.events["build"].append((start, event()))
            self.current = {
                "nodes": nodes.tokens.size(1),
                "steps": 0,
                "verified_inputs": 0,
                "committed": 0,
            }

        def ds(spec, num_reqs, head_hidden):
            if self.mode in ("off", "chain"):
                return original_ds(spec, num_reqs, head_hidden)
            assert num_reqs == 1
            h = head_hidden[spec.sample_indices[: spec.num_speculative_steps]]
            base = spec.model.compute_draft_logits(h).unsqueeze(0)
            anchor = spec.input_buffers.input_ids[spec._anchor_idx[:1]]
            ids, edges = markov_lattice(spec.model, base, anchor)
            record_lattice(spec, ids, edges, anchor)
            if self.mode == "capture":
                return original_ds(spec, num_reqs, head_hidden)

        def df(
            spec,
            num_reqs,
            num_tokens_padded,
            attn_metadata,
            slot_mappings,
            num_tokens_across_dp,
            cudagraph_runtime_mode,
        ):
            if self.mode in ("off", "chain"):
                return original_df(
                    spec,
                    num_reqs,
                    num_tokens_padded,
                    attn_metadata,
                    slot_mappings,
                    num_tokens_across_dp,
                    cudagraph_runtime_mode,
                )
            assert num_reqs == 1
            last = spec._run_model(
                num_tokens_padded,
                attn_metadata,
                slot_mappings,
                num_tokens_across_dp,
                cudagraph_runtime_mode,
            )
            n = spec.num_speculative_steps
            h = last[spec.sample_indices[:n]].reshape(1, n, -1)
            ids, unary = spec.model.compute_candidates(h.flatten(0, 1))
            ids = ids.reshape(1, n, spec.top_k)
            scores = spec._score_candidates(ids, unary.reshape_as(ids), h)
            anchor = spec.input_buffers.input_ids[:1]
            record_lattice(spec, ids, scores.float().log_softmax(-1), anchor)
            if self.mode == "capture":
                spec.candidate_sampler.sample(
                    ids,
                    scores,
                    1,
                    spec.sample_pos,
                    spec.sample_idx_mapping,
                    spec.temperature,
                    spec.seeds,
                    spec.draft_tokens,
                    spec.draft_logits,
                    spec.use_fp64_gumbel,
                )

        def propose(spec, input_batch, *args, **kwargs):
            batch = input_batch

            def pad(tensor):
                return torch.nn.functional.pad(
                    tensor, (0, self.capacity - tensor.size(1)), value=0
                )

            if self.mode == "off" or kwargs.get("dummy_run"):
                native = original_propose(spec, batch, *args, **kwargs)
                self.width = native.size(1)
                return pad(native)
            assert batch.num_reqs == 1
            if self.req != batch.req_ids[0]:
                self.req = batch.req_ids[0]
                self.current = self.tree = None
            start = event()
            path = self.verifier.path
            if path is not None:
                # Stock proposer consumes accepted target features at the front.
                # Gather into temporaries so source rows survive overlaps.
                aux = args[3]
                for features in aux or [args[2]]:
                    features[: path.numel()].copy_(features.index_select(0, path))
                self.verifier.path = None
            num_builds = len(self.events["build"])
            draft = original_propose(spec, batch, *args, **kwargs)
            end = event()
            if kwargs.get("num_speculative_tokens") == 0:
                self.width = 0
                self.events["draft"].append((start, end))
                return pad(draft)
            if self.mode == "capture":
                ids, edge, anchor = self.edges
                self.traces.append(
                    (
                        ids[0].cpu(),
                        edge[0].cpu(),
                        anchor[0].cpu(),
                        draft[0].cpu().clone(),
                    )
                )
                self.width = 0
            elif self.mode == "chain":
                self.width = draft.size(1)
                self.current = {
                    "nodes": self.width + 1,
                    "steps": 0,
                    "verified_inputs": 0,
                    "committed": 0,
                }
                if self.shared_chain:
                    depths = torch.arange(self.width + 1, device=draft.device).reshape(
                        1, -1
                    )
                    self.tree = Tree(
                        torch.cat(
                            (spec.input_buffers.input_ids[:1].reshape(1, 1), draft), 1
                        ),
                        depths - 1,
                        depths,
                    )
            else:
                draft = self.tree.tokens[:, 1:]
                self.width = draft.size(1)
            # Split at the build interval to avoid double-counting GPU timeline.
            if len(self.events["build"]) > num_builds:
                a, b = self.events["build"][-1]
                self.events["draft"].extend([(start, a), (b, end)])
            else:
                self.events["draft"].append((start, end))
            return pad(draft)

        def publish(handler, batch, drafts):
            if self.width is not None:
                drafts = drafts[:, : self.width]
            return original_set(handler, batch, drafts)

        GPUModelRunner.execute_model = execute
        GPUModelRunner.prepare_attn = prepare
        DFlashSpeculator.__init__ = init
        GPUModelRunner.sample = sample
        DSparkSpeculator._sample_sequential = ds
        DFlash2Speculator._generate_draft = df
        DFlashSpeculator.propose = propose
        DraftTokensHandler.set_draft_tokens = publish
        self.verifier.install()
