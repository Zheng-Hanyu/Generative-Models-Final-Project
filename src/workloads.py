"""Prepare and verify the Spec-Bench, synthetic, and public serving inputs."""
from __future__ import annotations

import csv
import hashlib
import json
import random
from collections import Counter, defaultdict, deque
from itertools import islice, product
from pathlib import Path
from tempfile import TemporaryDirectory

from serving import BenchmarkCell, prompt_flags, spec_bench_flags

ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / "data/spec_bench/question.jsonl"

SPEED_URL = "https://huggingface.co/datasets/nvidia/SPEED-Bench/resolve/fa4e669bee2a4393c56aa8ed05a7c667897f9590/qualitative/test-00000-of-00001.parquet"
BURST_URL = "https://github.com/HPMLL/BurstGPT/releases/download/v2.0/BurstGPT_without_fails_3.csv"
SEEDS = (423, 557, 691)
SPEED_COUNTS = {1: 16, 16: 32}
BURST_COUNT = 64
TRACE_SECONDS = 8
TRACE_OFFSETS = (40_000, 100_000, 250_000)


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, allow_nan=False) + "\n", encoding="utf-8")
    temporary.replace(path)


def cell_name(phase, concurrency, seed):
    return f"{phase}-c{concurrency}-s{seed}"


def stress_cells(protocol):
    stress = protocol["stress"]
    return [(concurrency, stress["seed"] + index) for index, concurrency in enumerate(stress["concurrencies"])]


def write_workloads(directory, source, protocol):
    categories = defaultdict(list)
    seen = set()
    for line in source.read_text(encoding="utf-8").splitlines():
        row = json.loads(line)
        prompt = row["turns"][0].strip()
        if prompt in seen:
            raise ValueError("Spec-Bench contains duplicate first turns")
        seen.add(prompt)
        categories[row["category"]].append(row)

    rng = random.Random(protocol["split_seed"])
    tuning, holdout = [], []
    for rows in categories.values():
        rng.shuffle(rows)
        cutoff = round(protocol["tuning_fraction"] * len(rows))
        tuning.extend(rows[:cutoff])
        holdout.extend(rows[cutoff:])

    groups = [
        ("holdout", protocol["holdout_seeds"], holdout, protocol["holdout_prompts"]),
    ]
    if "tuning_seed" in protocol:
        groups.insert(0, ("tuning", [protocol["tuning_seed"]], tuning, protocol["tuning_prompts"]))
    directory.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for phase, seeds, rows, count in groups:
        cells = list(product(seeds, protocol["concurrencies"]))
        for index, (seed, concurrency) in enumerate(cells):
            name = cell_name(phase, concurrency, seed)
            if phase == "holdout" and protocol.get("reuse_prompts_by_seed"):
                offset = protocol.get("holdout_offset", 0)
                subset = rows[seeds.index(seed)::len(seeds)][offset:offset + count]
            else:
                subset = rows[index::len(cells)]
            if len(subset) < count:
                raise ValueError(f"{name}: only {len(subset)} distinct questions for {count} requests")
            contents = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in subset)
            path = directory / f"{name}.jsonl"
            if path.exists():
                if path.read_text(encoding="utf-8") != contents:
                    raise ValueError(f"{path}: workload changed between runs")
            else:
                temporary = path.with_suffix(".tmp")
                temporary.write_text(contents, encoding="utf-8")
                temporary.replace(path)
            manifest[name] = {"candidates": len(subset), "sha256": hashlib.sha256(contents.encode()).hexdigest()}
    return manifest


def load_serving_workloads(directory):
    root = directory.resolve()
    manifest = read_json(root / "manifest.json")
    if manifest["schema"] != 1:
        raise ValueError("Unsupported serving workload manifest")
    seen = set()
    for cell in manifest["cells"]:
        name = cell_name(cell["workload"], cell["concurrency"], cell["seed"])
        if cell["workload"] not in ("speed", "burst") or name in seen:
            raise ValueError(f"Unexpected serving workload cell {name}")
        path = (root / cell["input"]).resolve()
        if not path.is_relative_to(root) or hashlib.sha256(path.read_bytes()).hexdigest() != cell["sha256"]:
            raise ValueError(f"Serving workload checksum differs for {name}")
        seen.add(name)
    return manifest


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


def prepare_repetition(protocol, output):
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
                if file.exists():
                    if file.read_bytes() != data:
                        raise ValueError(f"{file}: workload changed between runs")
                else:
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


def speed_cells(source, spec_bench):
    import pyarrow.parquet as pq

    def prompt_key(text):
        return " ".join(text.split())

    used = {prompt_key(json.loads(line)["turns"][0]) for line in spec_bench.read_text(encoding="utf-8").splitlines()}
    categories = defaultdict(list)
    for row in pq.read_table(source, columns=["category", "turns"]).to_pylist():
        prompt = row["turns"][0].strip()
        key = prompt_key(prompt)
        if key in used or not key or len(prompt.encode()) > 3500 or "FULL BENCHMARK DATA" in prompt:
            continue
        used.add(key)
        category = row["category"]
        categories[category].append({"category": category, "messages": [{"role": "user", "content": prompt}]})
    rng = random.Random(20261125)
    rows = []
    for category in sorted(categories):
        group = categories[category]
        rng.shuffle(group)
        rows.extend(group)
    rng.shuffle(rows)
    prompts = iter(rows)
    for seed, concurrency in product(SEEDS, SPEED_COUNTS):
        count = SPEED_COUNTS[concurrency]
        group = list(islice(prompts, count))
        if len(group) < count:
            raise ValueError("Insufficient distinct SPEED-Bench prompts for the requested design")
        yield {
            "workload": "speed", "seed": seed, "concurrency": concurrency, "count": count,
            "input": f"speed-c{concurrency}-s{seed}/qualitative.jsonl", "fixed_output_tokens": 128,
            "categories": dict(Counter(row["category"] for row in group)),
        }, group


def burst_cells(source):
    with source.open(encoding="utf-8", newline="") as stream:
        def eligible():
            for row in csv.DictReader(stream):
                input_length = int(row["Request tokens"])
                output_length = int(row["Response tokens"])
                if 8 <= input_length <= 3072 and 16 <= output_length <= 512:
                    yield float(row["Timestamp"]), input_length, output_length

        trace = eligible()
        consumed = 0
        for index, (seed, offset) in enumerate(zip(SEEDS, TRACE_OFFSETS, strict=True)):
            deque(islice(trace, offset - consumed), maxlen=0)
            samples = list(islice(trace, BURST_COUNT))
            consumed = offset + BURST_COUNT
            if len(samples) != BURST_COUNT:
                raise ValueError("BurstGPT trace ended before the final window")
            earliest = samples[0][0]
            duration = samples[-1][0] - earliest
            if duration <= 0 or any(b[0] < a[0] for a, b in zip(samples[:-1], samples[1:], strict=True)):
                raise ValueError("BurstGPT window has invalid timestamps")
            rows = []
            for position, (timestamp, input_length, output_length) in enumerate(samples):
                base_hash = (index * BURST_COUNT + position) * 256
                rows.append({
                    "timestamp": (timestamp - earliest) * TRACE_SECONDS / duration,
                    "input_length": input_length,
                    "output_length": output_length,
                    "hash_ids": list(range(base_hash, base_hash + (input_length + 15) // 16)),
                })
            yield {
                "workload": "burst", "seed": seed, "concurrency": 16, "count": BURST_COUNT,
                "input": f"burst-c16-s{seed}.jsonl",
                "eligible_row_offset": offset, "source_span_seconds": duration, "replay_span_seconds": TRACE_SECONDS,
            }, rows


def prepare_external(output, spec_bench, speed_parquet, burst_csv):
    output = output.resolve()
    if output.exists():
        raise ValueError(f"{output}: use a new directory for external workloads")
    output.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix=".serving-inputs-", dir=output.parent) as temporary:
        staging = Path(temporary) / "inputs"
        staging.mkdir()
        cells = []
        for cell, rows in (*speed_cells(speed_parquet, spec_bench), *burst_cells(burst_csv)):
            path = staging / cell["input"]
            path.parent.mkdir(exist_ok=True)
            data = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows).encode()
            path.write_bytes(data)
            cells.append({**cell, "sha256": hashlib.sha256(data).hexdigest()})
        sources = {}
        for name, path, url in (("speed", speed_parquet, SPEED_URL), ("burst", burst_csv, BURST_URL)):
            with path.open("rb") as source:
                digest = hashlib.file_digest(source, "sha256").hexdigest()
            sources[name] = {"url": url, "sha256": digest}
        write_json(staging / "manifest.json", {"schema": 1, "sources": sources, "cells": cells})
        staging.rename(output)


def prepare_inputs(output, dataset, config, study):
    protocol = config["protocol"] if study == "framework" else config["studies"][study].get("protocol", config["protocol"])
    spec_directory = output / "spec-bench" if study == "paired" else output / "workloads"
    spec = write_workloads(spec_directory, dataset, protocol)
    write_json(output / "workloads.json", spec)
    if study == "framework":
        return ()
    cells = []
    for seed in protocol["holdout_seeds"]:
        concurrencies = protocol["concurrencies"].copy()
        if protocol.get("reuse_prompts_by_seed"):
            random.Random(seed).shuffle(concurrencies)
        for concurrency in concurrencies:
            name = cell_name("holdout", concurrency, seed)
            run_name = cell_name("spec-bench", concurrency, seed) if study == "paired" else name
            cell = BenchmarkCell(run_name, seed, concurrency, protocol["holdout_prompts"],
                                 spec_bench_flags(spec_directory / f"{name}.jsonl", protocol["output_tokens"]))
            cells.append(("spec-bench", spec[name]["sha256"], cell))
    if study == "paired":
        repetition = output / "repetitive"
        for row in prepare_repetition(protocol, repetition):
            if row["phase"] == "holdout":
                seed, concurrency = row["seed"], row["concurrency"]
                cell = BenchmarkCell(cell_name("repetition", concurrency, seed), seed, concurrency, row["count"],
                                     prompt_flags(repetition / row["input"], row["output_tokens"]),
                                     output_tokens=row["output_tokens"])
                cells.append(("repetition", row["sha256"], cell))
    return cells


def serving_cell(directory, row):
    workload, concurrency, seed = row["workload"], row["concurrency"], row["seed"]
    name = cell_name(workload, concurrency, seed)
    path = directory / row["input"]
    if workload == "speed":
        count = row["fixed_output_tokens"]
        return BenchmarkCell(name, seed, concurrency, row["count"], prompt_flags(path, count),
                             output_tokens=count)
    trace = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
    return BenchmarkCell(name, seed, concurrency, row["count"],
                         ("--dataset-name", "timed_trace", "--dataset-path", str(path)),
                         [sample["input_length"] for sample in trace],
                         [sample["output_length"] for sample in trace])
