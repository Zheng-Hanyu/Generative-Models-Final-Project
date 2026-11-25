#!/usr/bin/env python3
"""Aggregate repeated vLLM benchmark runs without discarding request-level data."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "results" / "raw"
PROCESSED = ROOT / "results" / "processed"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def sample_stats(values: list[float]) -> dict[str, float | int | None]:
    return {
        "n": len(values),
        "mean": statistics.fmean(values) if values else None,
        "sample_stdev": statistics.stdev(values) if len(values) > 1 else None,
        "min": min(values) if values else None,
        "max": max(values) if values else None,
    }


def percentiles(values: list[float]) -> dict[str, float | int | None]:
    if not values:
        return {"n": 0, "mean": None, "p50": None, "p95": None, "p99": None}
    array = np.asarray(values, dtype=np.float64)
    return {
        "n": len(values),
        "mean": float(np.mean(array)),
        "p50": float(np.percentile(array, 50)),
        "p95": float(np.percentile(array, 95)),
        "p99": float(np.percentile(array, 99)),
    }


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def load_run(path: Path) -> tuple[dict[str, Any], dict[str, list[float]]]:
    data = json.loads(path.read_text(encoding="utf-8"))
    output_lens = data["output_lens"]
    ttfts_ms = [1000.0 * value for value in data["ttfts"]]
    e2el_ms = [1000.0 * value for value in data["latencies"]]
    tpot_ms = [
        1000.0 * (latency - ttft) / (output_len - 1)
        for latency, ttft, output_len in zip(data["latencies"], data["ttfts"], output_lens)
        if output_len > 1
    ]
    itl_ms = [1000.0 * value for request_itls in data["itls"] for value in request_itls]
    run = {
        "phase": data["phase"],
        "method": data.get("method_name") or path.name.removeprefix(f"{data['phase']}-").split("-i", 1)[0],
        "mode": data.get("mode"),
        "k": int(data["k"]),
        "gpu": int(data["gpu"]),
        "concurrency": int(data["concurrency"]),
        "seed": int(data["seed"]),
        "input_len": round(data["total_input_tokens"] / data["completed"]),
        "mean_input_tokens": statistics.fmean(data["input_lens"]),
        "total_input_tokens": data["total_input_tokens"],
        "output_len": round(data["total_output_tokens"] / data["completed"]),
        "completed": data["completed"],
        "failed": data["failed"],
        "duration_s": data["duration"],
        "request_throughput_req_s": data["request_throughput"],
        "output_throughput_tokens_s": data["output_throughput"],
        "total_token_throughput_tokens_s": data["total_token_throughput"],
        "mean_ttft_ms": data["mean_ttft_ms"],
        "mean_tpot_ms": data["mean_tpot_ms"],
        "mean_itl_ms": data["mean_itl_ms"],
        "mean_e2el_ms": data["mean_e2el_ms"],
        "acceptance_rate_percent": data.get("spec_decode_acceptance_rate"),
        "acceptance_length": data.get("spec_decode_acceptance_length"),
        "num_drafts": data.get("spec_decode_num_drafts"),
        "draft_tokens": data.get("spec_decode_draft_tokens"),
        "accepted_tokens": data.get("spec_decode_accepted_tokens"),
        "per_position_acceptance_rates_percent": (
            [100.0 * value for value in data["spec_decode_per_position_acceptance_rates"]]
            if data.get("spec_decode_per_position_acceptance_rates") is not None
            else None
        ),
        "raw_file": str(path.relative_to(ROOT)),
    }
    return run, {
        "input_tokens": [float(value) for value in data["input_lens"]],
        "ttft_ms": ttfts_ms,
        "tpot_ms": tpot_ms,
        "itl_ms": itl_ms,
        "e2el_ms": e2el_ms,
    }


def compare_runs_to_baseline(
    runs: list[dict[str, Any]],
    groups: list[dict[str, Any]],
    methods: list[str],
    concurrencies: list[int],
    seeds: list[int],
    baseline_method: str,
) -> list[dict[str, Any]]:
    """Compute same-seed throughput ratios against one explicit baseline."""
    comparisons: list[dict[str, Any]] = []
    has_baseline = any(run["method"] == baseline_method for run in runs)
    for method in methods:
        if method == baseline_method or not has_baseline:
            continue
        for concurrency in concurrencies:
            pairs = []
            for seed in seeds:
                baseline = next(
                    (r for r in runs if r["method"] == baseline_method and r["concurrency"] == concurrency and r["seed"] == seed),
                    None,
                )
                candidate = next(
                    (r for r in runs if r["method"] == method and r["concurrency"] == concurrency and r["seed"] == seed),
                    None,
                )
                if baseline is None or candidate is None:
                    continue
                pairs.append(
                    {
                        "seed": seed,
                        "baseline_method": baseline_method,
                        "baseline_output_tps": baseline["output_throughput_tokens_s"],
                        "candidate_output_tps": candidate["output_throughput_tokens_s"],
                        "speedup": candidate["output_throughput_tokens_s"] / baseline["output_throughput_tokens_s"],
                    }
                )
            if not pairs:
                continue
            baseline_group = next(g for g in groups if g["method"] == baseline_method and g["concurrency"] == concurrency)
            candidate_group = next(g for g in groups if g["method"] == method and g["concurrency"] == concurrency)
            comparisons.append(
                {
                    "method": method,
                    "baseline_method": baseline_method,
                    "concurrency": concurrency,
                    "pairs": pairs,
                    "paired_speedup": sample_stats([pair["speedup"] for pair in pairs]),
                    "ratio_of_mean_output_tps": (
                        candidate_group["output_throughput_tokens_s"]["mean"]
                        / baseline_group["output_throughput_tokens_s"]["mean"]
                    ),
                }
            )
    return comparisons


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", default="formal-r1")
    parser.add_argument(
        "--output-stem",
        help="Optional output filename stem; defaults to --phase. Input files still use --phase.",
    )
    parser.add_argument("--methods", nargs="+", default=["normal", "mtp-k3", "dspark-k7"])
    parser.add_argument("--concurrencies", nargs="+", type=int, default=[1, 4, 16, 32])
    parser.add_argument("--seeds", nargs="+", type=int, default=[42, 43, 44])
    parser.add_argument("--input-len", type=int, default=1024)
    parser.add_argument("--output-len", type=int, default=512)
    parser.add_argument("--num-prompts", type=int, default=128)
    parser.add_argument("--dataset-name", choices=["random", "spec_bench"], default="random")
    parser.add_argument("--baseline-method", default="normal")
    parser.add_argument(
        "--additional-baseline-methods",
        nargs="+",
        default=[],
        help="Optional extra baselines; same-seed comparisons are exported for every other selected method.",
    )
    parser.add_argument(
        "--best-fixed-methods",
        nargs="+",
        help="Optional fixed methods used to select the best mean-throughput configuration per concurrency.",
    )
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()

    runs: list[dict[str, Any]] = []
    request_values: dict[tuple[str, int], dict[str, list[float]]] = {}
    missing: list[str] = []
    for method in args.methods:
        for concurrency in args.concurrencies:
            key = (method, concurrency)
            request_values[key] = {"input_tokens": [], "ttft_ms": [], "tpot_ms": [], "itl_ms": [], "e2el_ms": []}
            for seed in args.seeds:
                workload_tag = (
                    f"i{args.input_len}-o{args.output_len}"
                    if args.dataset_name == "random"
                    else f"specbench-o{args.output_len}"
                )
                filename = f"{args.phase}-{method}-{workload_tag}-c{concurrency}-s{seed}.json"
                path = RAW / filename
                if not path.exists():
                    missing.append(str(path.relative_to(ROOT)))
                    continue
                run, values = load_run(path)
                if run["completed"] != args.num_prompts or run["failed"] != 0:
                    raise ValueError(f"Unsuccessful benchmark in {path}")
                if args.dataset_name == "random" and run["input_len"] != args.input_len:
                    raise ValueError(f"Unexpected input length in {path}")
                if run["output_len"] != args.output_len:
                    raise ValueError(f"Unexpected output length in {path}")
                runs.append(run)
                for metric, metric_values in values.items():
                    request_values[key][metric].extend(metric_values)

    expected_run_count = len(args.methods) * len(args.concurrencies) * len(args.seeds)
    if missing and not args.allow_partial:
        raise FileNotFoundError(f"Missing {len(missing)} runs; first missing: {missing[:5]}")
    if not runs:
        raise ValueError("No benchmark runs found")

    groups: list[dict[str, Any]] = []
    group_csv: list[dict[str, Any]] = []
    for method in args.methods:
        for concurrency in args.concurrencies:
            selected = [r for r in runs if r["method"] == method and r["concurrency"] == concurrency]
            if not selected:
                continue
            if len(selected) != len(args.seeds) and not args.allow_partial:
                raise ValueError(f"Incomplete group: {method}, C={concurrency}")
            entry: dict[str, Any] = {
                "phase": args.phase,
                "method": method,
                "mode": selected[0]["mode"],
                "k": selected[0]["k"],
                "gpu": selected[0]["gpu"],
                "concurrency": concurrency,
                "input_len": args.input_len if args.dataset_name == "random" else None,
                "dataset_name": args.dataset_name,
                "output_len": args.output_len,
                "complete": len(selected) == len(args.seeds),
                "seeds": sorted(r["seed"] for r in selected),
                "total_completed_requests": sum(r["completed"] for r in selected),
                "total_failed_requests": sum(r["failed"] for r in selected),
            }
            metrics = {
                "output_throughput_tokens_s": "output_throughput_tokens_s",
                "request_throughput_req_s": "request_throughput_req_s",
                "duration_s": "duration_s",
                "mean_ttft_ms": "mean_ttft_ms",
                "mean_tpot_ms": "mean_tpot_ms",
                "mean_itl_ms": "mean_itl_ms",
                "mean_e2el_ms": "mean_e2el_ms",
                "acceptance_rate_percent": "acceptance_rate_percent",
                "acceptance_length": "acceptance_length",
            }
            for output_key, run_key in metrics.items():
                values = [float(r[run_key]) for r in selected if r[run_key] is not None]
                entry[output_key] = sample_stats(values) if values else None
            for metric, values in request_values[(method, concurrency)].items():
                entry[f"pooled_request_{metric}"] = percentiles(values)
            per_position = [r["per_position_acceptance_rates_percent"] for r in selected if r["per_position_acceptance_rates_percent"]]
            entry["per_position_acceptance_rates_percent"] = (
                [statistics.fmean(position) for position in zip(*per_position)] if per_position else None
            )
            entry["draft_tokens_total"] = sum(r["draft_tokens"] or 0 for r in selected) or None
            entry["accepted_tokens_total"] = sum(r["accepted_tokens"] or 0 for r in selected) or None
            if entry["draft_tokens_total"]:
                entry["token_weighted_acceptance_rate_percent"] = (
                    100.0 * entry["accepted_tokens_total"] / entry["draft_tokens_total"]
                )
            else:
                entry["token_weighted_acceptance_rate_percent"] = None
            entry["raw_files"] = [r["raw_file"] for r in selected]
            groups.append(entry)
            group_csv.append(
                {
                    "method": method,
                    "k": entry["k"],
                    "gpu": entry["gpu"],
                    "concurrency": concurrency,
                    "runs": len(selected),
                    "requests": entry["total_completed_requests"],
                    "input_tokens_p50": entry["pooled_request_input_tokens"]["p50"],
                    "input_tokens_p95": entry["pooled_request_input_tokens"]["p95"],
                    "output_tps_mean": entry["output_throughput_tokens_s"]["mean"],
                    "output_tps_sample_stdev": entry["output_throughput_tokens_s"]["sample_stdev"],
                    "request_tps_mean": entry["request_throughput_req_s"]["mean"],
                    "run_mean_tpot_ms_mean": entry["mean_tpot_ms"]["mean"],
                    "run_mean_tpot_ms_sample_stdev": entry["mean_tpot_ms"]["sample_stdev"],
                    "pooled_tpot_p95_ms": entry["pooled_request_tpot_ms"]["p95"],
                    "run_mean_e2el_ms_mean": entry["mean_e2el_ms"]["mean"],
                    "pooled_e2el_p95_ms": entry["pooled_request_e2el_ms"]["p95"],
                    "pooled_ttft_p95_ms": entry["pooled_request_ttft_ms"]["p95"],
                    "acceptance_rate_percent_mean": (
                        entry["acceptance_rate_percent"]["mean"] if entry["acceptance_rate_percent"] else None
                    ),
                    "acceptance_length_mean": (
                        entry["acceptance_length"]["mean"] if entry["acceptance_length"] else None
                    ),
                    "complete": entry["complete"],
                }
            )

    baseline_method = args.baseline_method
    paired_speedups = compare_runs_to_baseline(
        runs, groups, args.methods, args.concurrencies, args.seeds, baseline_method
    )
    paired_speedups_vs_additional_baselines = {
        additional_baseline: compare_runs_to_baseline(
            runs, groups, args.methods, args.concurrencies, args.seeds, additional_baseline
        )
        for additional_baseline in args.additional_baseline_methods
    }

    best_fixed_by_concurrency: list[dict[str, Any]] = []
    paired_speedups_vs_best_fixed: list[dict[str, Any]] = []
    if args.best_fixed_methods:
        for concurrency in args.concurrencies:
            fixed_groups = [
                g
                for g in groups
                if g["method"] in args.best_fixed_methods and g["concurrency"] == concurrency
            ]
            if not fixed_groups:
                continue
            best_fixed = max(
                fixed_groups,
                key=lambda g: g["output_throughput_tokens_s"]["mean"],
            )
            best_fixed_by_concurrency.append(
                {
                    "concurrency": concurrency,
                    "method": best_fixed["method"],
                    "k": best_fixed["k"],
                    "output_throughput_tokens_s": best_fixed["output_throughput_tokens_s"],
                    "candidate_fixed_methods": [g["method"] for g in fixed_groups],
                    "selection": "Highest three-run mean output throughput among the supplied fixed methods at this concurrency.",
                }
            )
            for method in args.methods:
                if method == "normal":
                    continue
                candidate_group = next(
                    (g for g in groups if g["method"] == method and g["concurrency"] == concurrency),
                    None,
                )
                if candidate_group is None:
                    continue
                pairs = []
                for seed in args.seeds:
                    baseline = next(
                        (
                            r
                            for r in runs
                            if r["method"] == best_fixed["method"]
                            and r["concurrency"] == concurrency
                            and r["seed"] == seed
                        ),
                        None,
                    )
                    candidate = next(
                        (
                            r
                            for r in runs
                            if r["method"] == method
                            and r["concurrency"] == concurrency
                            and r["seed"] == seed
                        ),
                        None,
                    )
                    if baseline is None or candidate is None:
                        continue
                    pairs.append(
                        {
                            "seed": seed,
                            "baseline_method": best_fixed["method"],
                            "baseline_output_tps": baseline["output_throughput_tokens_s"],
                            "candidate_output_tps": candidate["output_throughput_tokens_s"],
                            "speedup": (
                                candidate["output_throughput_tokens_s"]
                                / baseline["output_throughput_tokens_s"]
                            ),
                        }
                    )
                if not pairs:
                    continue
                paired_speedups_vs_best_fixed.append(
                    {
                        "method": method,
                        "baseline_method": best_fixed["method"],
                        "concurrency": concurrency,
                        "pairs": pairs,
                        "paired_speedup": sample_stats([pair["speedup"] for pair in pairs]),
                        "ratio_of_mean_output_tps": (
                            candidate_group["output_throughput_tokens_s"]["mean"]
                            / best_fixed["output_throughput_tokens_s"]["mean"]
                        ),
                    }
                )

    for row in runs:
        row["per_position_acceptance_rates_percent"] = json.dumps(
            row["per_position_acceptance_rates_percent"], ensure_ascii=False
        )

    summary = {
        "schema_version": 1,
        "phase": args.phase,
        "generated_at": utc_now(),
        "status": "partial" if missing else "complete",
        "expected_run_count": expected_run_count,
        "loaded_run_count": len(runs),
        "missing_files": missing,
        "methodology": {
            "run_statistics": "Arithmetic mean and sample standard deviation (ddof=1) across independent benchmark runs.",
            "request_percentiles": f"Computed after pooling request-level values from all runs ({len(args.seeds) * args.num_prompts} requests per complete configuration), using NumPy linear interpolation.",
            "tpot_definition": "1000 * (end-to-end latency - TTFT) / (output tokens - 1), in milliseconds per request.",
            "itl_definition": "Intervals between recorded streaming output events/chunks; a speculative-decoding chunk may contain multiple tokens, so ITL is not a complete per-token arrival distribution.",
            "paired_speedup": f"For each seed, candidate output throughput / {baseline_method} output throughput; report mean and sample stdev of the run-level ratios. Ratio of mean throughputs is also provided.",
            "additional_paired_speedups": "Optional explicit baselines use the same per-seed ratio and sample-statistic definitions; no pooling across seeds is used for paired ratios.",
            "confidence_intervals": "Not computed; three-run sample stdev is not a confidence interval.",
            "cross_gpu_caveat": "Formal round 1 runs methods concurrently on separate B200 GPUs. Final interpretation requires same-GPU checks and rotation.",
            "best_fixed_selection": "When requested, the best fixed method is selected using the same three runs used for descriptive paired comparisons; this is a post-selection comparison, not an independent generalization estimate.",
        },
        "groups": groups,
        "paired_speedups": paired_speedups,
        "paired_speedups_vs_normal": paired_speedups if baseline_method == "normal" else [],
        "paired_speedups_vs_additional_baselines": paired_speedups_vs_additional_baselines,
        "best_fixed_by_concurrency": best_fixed_by_concurrency,
        "paired_speedups_vs_best_fixed": paired_speedups_vs_best_fixed,
    }
    PROCESSED.mkdir(parents=True, exist_ok=True)
    output_stem = args.output_stem or args.phase
    summary_path = PROCESSED / f"{output_stem}-summary.json"
    summary_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_csv(PROCESSED / f"{output_stem}-runs.csv", runs)
    write_csv(PROCESSED / f"{output_stem}-groups.csv", group_csv)
    print(json.dumps({"summary": str(summary_path), "status": summary["status"], "runs": len(runs)}, indent=2))


if __name__ == "__main__":
    main()
