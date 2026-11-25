"""Prepare independent NVIDIA SPEED-Bench and BurstGPT v2.0 serving workloads."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import random
from collections import Counter, defaultdict, deque
from itertools import islice, product
from pathlib import Path


SPEED_URL = "https://huggingface.co/datasets/nvidia/SPEED-Bench/resolve/fa4e669bee2a4393c56aa8ed05a7c667897f9590/qualitative/test-00000-of-00001.parquet"
BURST_URL = "https://github.com/HPMLL/BurstGPT/releases/download/v2.0/BurstGPT_without_fails_3.csv"
SEEDS = (423, 557, 691)
SPEED_COUNTS = {1: 16, 16: 32}
BURST_COUNT = 64
TRACE_SECONDS = 8
TRACE_OFFSETS = (40_000, 100_000, 250_000)


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


def make_manifest(args):
    args.output.mkdir(parents=True)
    cells = []
    for cell, rows in (*speed_cells(args.speed_parquet, args.spec_bench), *burst_cells(args.burst_csv)):
        path = args.output / cell["input"]
        path.parent.mkdir(exist_ok=True)
        data = "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows).encode()
        path.write_bytes(data)
        cells.append({**cell, "sha256": hashlib.sha256(data).hexdigest()})
    sources = {}
    for name, path, url in (("speed", args.speed_parquet, SPEED_URL), ("burst", args.burst_csv, BURST_URL)):
        with path.open("rb") as source:
            digest = hashlib.file_digest(source, "sha256").hexdigest()
        sources[name] = {"url": url, "sha256": digest}
    manifest = {"schema": 1, "sources": sources, "cells": cells}
    (args.output / "manifest.json").write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--speed-parquet", type=Path, required=True)
    parser.add_argument("--burst-csv", type=Path, required=True)
    parser.add_argument("--spec-bench", type=Path, default=Path(__file__).resolve().parents[1] / "data/spec_bench/question.jsonl")
    parser.add_argument("--output", type=Path, required=True)
    make_manifest(parser.parse_args())
