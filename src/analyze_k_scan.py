#!/usr/bin/env python3
"""Analyze fixed-K scans and estimate configuration-level dynamic-K headroom."""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "results" / "raw"
PROCESSED = ROOT / "results" / "processed"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", default="kscan-r1")
    parser.add_argument("--method", choices=["mtp", "dspark"], required=True)
    parser.add_argument("--ks", nargs="+", type=int, required=True)
    parser.add_argument("--concurrencies", nargs="+", type=int, default=[1, 4, 16, 32])
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--num-prompts", type=int, default=32)
    parser.add_argument("--input-len", type=int, default=1024)
    parser.add_argument("--output-len", type=int, default=512)
    parser.add_argument("--reference-k", type=int, default=3)
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()

    records = []
    missing = []
    for k in args.ks:
        for concurrency in args.concurrencies:
            name = (
                f"{args.phase}-{args.method}-k{k}-i{args.input_len}-o{args.output_len}"
                f"-c{concurrency}-s{args.seed}.json"
            )
            path = RAW / name
            if not path.exists():
                missing.append(name)
                continue
            data = json.loads(path.read_text(encoding="utf-8"))
            if data["completed"] != args.num_prompts or data["failed"]:
                raise ValueError(f"Incomplete or failed run: {name}")
            acceptance_length = data["spec_decode_acceptance_length"]
            tpot_ms = data["mean_tpot_ms"]
            per_position = data.get("spec_decode_per_position_acceptance_rates") or []
            records.append(
                {
                    "method": args.method,
                    "k": k,
                    "concurrency": concurrency,
                    "output_tps": data["output_throughput"],
                    "request_tps": data["request_throughput"],
                    "mean_tpot_ms": tpot_ms,
                    "mean_itl_ms": data["mean_itl_ms"],
                    "mean_e2el_ms": data["mean_e2el_ms"],
                    "acceptance_length": acceptance_length,
                    "acceptance_rate_percent": data["spec_decode_acceptance_rate"],
                    "estimated_cycle_ms": tpot_ms * acceptance_length,
                    "num_drafts": data["spec_decode_num_drafts"],
                    "draft_tokens": data["spec_decode_draft_tokens"],
                    "accepted_tokens": data["spec_decode_accepted_tokens"],
                    "per_position_unconditional_acceptance": per_position,
                    "raw_file": str(path.relative_to(ROOT)),
                }
            )
    if missing and not args.allow_partial:
        raise FileNotFoundError(f"Missing {len(missing)} runs: {missing[:4]}")
    if not records:
        raise ValueError("No completed K-scan records")

    by_concurrency = []
    for concurrency in args.concurrencies:
        group = [r for r in records if r["concurrency"] == concurrency]
        if not group:
            continue
        best = max(group, key=lambda r: r["output_tps"])
        reference = next((r for r in group if r["k"] == args.reference_k), None)
        entry = {
            "concurrency": concurrency,
            "available_ks": sorted(r["k"] for r in group),
            "best_fixed_k": best["k"],
            "best_output_tps": best["output_tps"],
            "reference_k": args.reference_k if reference else None,
            "reference_output_tps": reference["output_tps"] if reference else None,
            "configuration_oracle_speedup_over_reference": (
                best["output_tps"] / reference["output_tps"] if reference else None
            ),
        }
        if len(group) >= 3:
            x = np.asarray([r["k"] for r in group], dtype=float)
            y = np.asarray([r["estimated_cycle_ms"] for r in group], dtype=float)
            slope, intercept = np.polyfit(x, y, 1)
            predicted = intercept + slope * x
            ss_res = float(np.sum((y - predicted) ** 2))
            ss_tot = float(np.sum((y - np.mean(y)) ** 2))
            entry["linear_cycle_cost_fit"] = {
                "intercept_ms": float(intercept),
                "marginal_ms_per_k": float(slope),
                "r_squared": 1.0 - ss_res / ss_tot if ss_tot > 0 else None,
                "interpretation": "Descriptive fit of TPOT*acceptance_length, not a standalone draft/verify profiler measurement.",
            }
        by_concurrency.append(entry)

    max_k = max(r["k"] for r in records)
    prefix_predictions = []
    for concurrency in args.concurrencies:
        max_record = next(
            (r for r in records if r["concurrency"] == concurrency and r["k"] == max_k), None
        )
        if max_record is None or len(max_record["per_position_unconditional_acceptance"]) != max_k:
            continue
        rates = max_record["per_position_unconditional_acceptance"]
        for k in args.ks:
            if k > max_k:
                continue
            actual = next((r for r in records if r["concurrency"] == concurrency and r["k"] == k), None)
            if actual is None:
                continue
            predicted = 1.0 + float(np.sum(rates[:k]))
            prefix_predictions.append(
                {
                    "concurrency": concurrency,
                    "k": k,
                    "max_k_trace": max_k,
                    "predicted_acceptance_length_from_max_k_marginals": predicted,
                    "measured_acceptance_length": actual["acceptance_length"],
                    "absolute_error": abs(predicted - actual["acceptance_length"]),
                    "relative_error_percent": 100.0 * abs(predicted - actual["acceptance_length"]) / actual["acceptance_length"],
                }
            )

    range_bounds = {1: (1, 1), 4: (2, 4), 16: (5, 16), 32: (17, 256)}
    schedule = []
    for entry in by_concurrency:
        start, end = range_bounds[entry["concurrency"]]
        schedule.append([start, end, entry["best_fixed_k"]])
    speculative_config = {
        "method": args.method,
        "num_speculative_tokens": max_k,
        "num_speculative_tokens_per_batch_size": schedule,
    }
    if args.method == "dspark":
        speculative_config["model"] = "/home/genai/models/Qwen3.8-27B-DSpark-vLLM"

    result = {
        "schema_version": 1,
        "phase": args.phase,
        "method": args.method,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "status": "partial" if missing else "complete",
        "missing_files": missing,
        "definitions": {
            "estimated_cycle_ms": "mean TPOT * acceptance length. It is an end-to-end effective cycle-cost estimate, not a kernel-level timing.",
            "per_position_acceptance": "vLLM per-position unconditional acceptance fractions; acceptance length is approximately 1 + their sum.",
            "configuration_oracle": "Best measured fixed K at each concurrency. This is not a per-step oracle and does not claim an upper bound for every possible online policy.",
        },
        "configuration_oracle_by_concurrency": by_concurrency,
        "suggested_batch_size_schedule": speculative_config,
        "max_k_prefix_acceptance_predictions": prefix_predictions,
        "records": records,
    }
    output = PROCESSED / f"{args.phase}-{args.method}-cost-analysis.json"
    output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    csv_rows = []
    for record in records:
        row = {key: value for key, value in record.items() if key != "per_position_unconditional_acceptance"}
        row["per_position_unconditional_acceptance"] = json.dumps(record["per_position_unconditional_acceptance"])
        csv_rows.append(row)
    with (PROCESSED / f"{args.phase}-{args.method}-cost-records.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(csv_rows[0]))
        writer.writeheader()
        writer.writerows(csv_rows)
    print(json.dumps({"output": str(output), "status": result["status"], "oracle": by_concurrency}, indent=2))


if __name__ == "__main__":
    main()
