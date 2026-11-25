#!/usr/bin/env python3
"""Compare token IDs from deterministic smoke outputs across decoding modes."""

import argparse
import json
from pathlib import Path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", action="append", required=True, metavar="NAME=PATH")
    parser.add_argument("--reference", required=True)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    runs = {}
    input_paths = {}
    for spec in args.input:
        name, separator, path = spec.partition("=")
        if not separator:
            parser.error(f"Invalid --input {spec!r}; expected NAME=PATH")
        input_paths[name] = path
        runs[name] = json.loads(Path(path).read_text())
    if args.reference not in runs:
        parser.error(f"Reference {args.reference!r} is not an input")

    reference_requests = {
        item["id"]: item for item in runs[args.reference]["requests"]
    }
    comparisons = []
    for request_id, reference in reference_requests.items():
        ref_ids = reference["response"]["choices"][0]["token_ids"]
        row = {
            "request_id": request_id,
            "reference": args.reference,
            "reference_token_count": len(ref_ids),
            "methods": {},
        }
        for name, run in runs.items():
            by_id = {item["id"]: item for item in run["requests"]}
            candidate = by_id[request_id]
            candidate_ids = candidate["response"]["choices"][0]["token_ids"]
            common = min(len(ref_ids), len(candidate_ids))
            first_mismatch = next(
                (index for index in range(common) if ref_ids[index] != candidate_ids[index]),
                None,
            )
            exact = ref_ids == candidate_ids
            row["methods"][name] = {
                "success": candidate["success"],
                "token_count": len(candidate_ids),
                "finish_reason": candidate["response"]["choices"][0]["finish_reason"],
                "exact_token_id_match": exact,
                "first_mismatch_index": first_mismatch,
                "reference_token_at_mismatch": (
                    ref_ids[first_mismatch] if first_mismatch is not None else None
                ),
                "candidate_token_at_mismatch": (
                    candidate_ids[first_mismatch] if first_mismatch is not None else None
                ),
                "latency_seconds": candidate["latency_seconds"],
            }
        comparisons.append(row)

    result = {
        "reference": args.reference,
        "inputs": input_paths,
        "all_requests_exact": all(
            method["exact_token_id_match"]
            for row in comparisons
            for method in row["methods"].values()
        ),
        "comparisons": comparisons,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["all_requests_exact"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
