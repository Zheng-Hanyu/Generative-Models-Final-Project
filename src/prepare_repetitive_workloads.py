"""Generate paired, synthetic repetition-heavy benchmark inputs."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import random


def code_edit(identifier):
    function = f"build_index_{identifier:04d}"
    body = [f"def {function}(records):", "    index = {}"]
    for slot in range(8):
        body.extend([
            f'    record = records.get("slot_{slot:02d}")',
            '    if record is not None and record["active"]:',
            f'        index["slot_{slot:02d}"] = {{"value": record["value"], "status": "pending"}}',
        ])
    body.append("    return index")
    return (
        "Update this Python function. In every index entry, rename the output field "
        'from "status" to "state" and change its value from "pending" to "queued". '
        "Keep the explicit repeated blocks, the order, and all other code as supplied. "
        "Return the full updated Python function as plain text.\n\n"
        + "\n".join(body)
    )


def json_output(identifier):
    rows = [
        f"slot_{slot:02d}, item_{identifier:04d}_{slot:02d}, {10 + slot}, pending"
        for slot in range(10)
    ]
    return (
        'Convert the following CSV records to one JSON object with an "items" array. '
        'Each array entry has exactly these keys in this order: "slot", "item", '
        '"quantity", "state", "source". Set "source" to "warehouse"; make "quantity" '
        "a number and preserve the other CSV values and row order. Return the JSON "
        "object as plain text.\n\nslot,item,quantity,state\n" + "\n".join(rows)
    )


def build_rows(first_identifier, count, seed):
    rows = []
    for offset in range(count // 2):
        identifier = first_identifier + offset
        rows.extend([
            {"category": "code_edit", "messages": [{"role": "user", "content": code_edit(identifier)}]},
            {"category": "json_output", "messages": [{"role": "user", "content": json_output(identifier)}]},
        ])
    random.Random(seed).shuffle(rows)
    return rows


def prepare(protocol, output):
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    manifest = []
    used = set()
    first_identifier = 0
    for phase, seeds in (("tuning", [protocol["tuning_seed"]]), ("holdout", protocol["holdout_seeds"])):
        count = protocol[f"{phase}_prompts"]
        if count % 2:
            raise ValueError(f"{phase} needs an even request count")
        for seed in seeds:
            for concurrency in protocol["concurrencies"]:
                name = f"{phase}-repetition-c{concurrency}-s{seed}"
                rows = build_rows(first_identifier, count, 100 * seed + concurrency)
                first_identifier += count // 2
                prompts = {row["messages"][0]["content"] for row in rows}
                if len(prompts) != count or used.intersection(prompts):
                    raise ValueError(f"Repeated input across cells: {name}")
                used.update(prompts)
                cell_path = output / name
                cell_path.mkdir(exist_ok=True)
                file = cell_path / "qualitative.jsonl"
                data = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows).encode()
                file.write_bytes(data)
                manifest.append({
                    "phase": phase,
                    "workload": "repetition",
                    "seed": seed,
                    "concurrency": concurrency,
                    "count": count,
                    "input": str(file.relative_to(output)),
                    "output_tokens": protocol["output_tokens"],
                    "categories": dict(Counter(row["category"] for row in rows)),
                    "sha256": hashlib.sha256(data).hexdigest(),
                })
    (output / "manifest.json").write_text(
        json.dumps({"schema": 1, "cells": manifest}, indent=2) + "\n", encoding="utf-8"
    )
    return manifest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    protocol = json.loads(args.config.read_text(encoding="utf-8"))["protocol"]
    prepare(protocol, args.output)


if __name__ == "__main__":
    main()
