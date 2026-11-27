#!/usr/bin/env python3
"""Replay the selected EAGLE-4, Suffix, or DFlash 2 profile against its matched Normal."""
from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
from pathlib import Path
import signal
import subprocess

from prepare_repetitive_workloads import prepare
from run_supplemental_benchmark import build_launch_command, environment, terminate, warmup
from unified_framework import CAPTURE_SIZES, CONFIG, DATASET, read_json, reserve_gpu, running_server, write_json, write_workloads


ROOT = Path(__file__).resolve().parents[1]
RELEASE = ROOT / "config/eagle4_suffix_b200.json"
TARGET = "/home/model/Qwen3.8-27B-FP8"


def cells_for(output, protocol):
    spec_root = output / "spec-bench"
    spec_rows = write_workloads(spec_root, DATASET, protocol)
    for name, cell in spec_rows.items():
        phase, concurrency, seed = name.split("-")
        if phase == "holdout":
            yield {
                "name": f"spec-bench-{concurrency}-{seed}", "seed": int(seed[1:]),
                "concurrency": int(concurrency[1:]), "count": protocol["holdout_prompts"],
                "sha256": cell["sha256"],
                "dataset": [
                    "--dataset-name", "spec_bench", "--dataset-path", str(spec_root / (name + ".jsonl")),
                    "--spec-bench-output-len", str(protocol["output_tokens"]), "--no-oversample",
                ],
            }
    repetition = output / "repetitive"
    for cell in prepare(protocol, repetition):
        if cell["phase"] == "holdout":
            parallel, seed = cell["concurrency"], cell["seed"]
            yield {
                **cell,
                "name": f"repetition-c{parallel}-s{seed}",
                "dataset": [
                    "--dataset-name", "speed_bench", "--dataset-path", str((repetition / cell["input"]).parent),
                    "--speed-bench-output-len", str(cell["output_tokens"]), "--no-oversample", "--ignore-eos",
                ],
            }


def launch(args, spec):
    command = build_launch_command(args, spec, CAPTURE_SIZES)
    if args.method == "eagle4":
        command[command.index("--attention-backend") + 1] = "CUSTOM"
        compilation = command.index("--compilation-config")
        del command[compilation:compilation + 2]
        command.extend(("--linear-backend", "flashinfer_cutedsl"))
    return command


def benchmark(client, args, cell, path, env, url):
    warmup(url)
    command = [
        client, "bench", "serve", "--backend", "openai", "--endpoint", "/v1/completions",
        "--base-url", url, "--model", "qwen-fp8", "--tokenizer", args.model, *cell["dataset"],
        "--seed", str(cell["seed"]), "--temperature", "0", "--num-warmups", "0",
        "--ready-check-timeout-sec", "0", "--request-rate", "inf",
        "--max-concurrency", str(cell["concurrency"]), "--num-prompts", str(cell["count"]),
        "--metric-percentiles", "50,95,99", "--save-detailed", "--save-result",
        "--result-dir", str(path.parent), "--result-filename", path.name,
    ]
    with path.with_suffix(".log").open("w", encoding="utf-8") as log:
        subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=300)
    result = read_json(path)
    if (result["completed"], result["failed"]) != (cell["count"], 0):
        raise RuntimeError(f"{path}: some requests failed")
    if "output_tokens" in cell and result["output_lens"] != [cell["output_tokens"]] * cell["count"]:
        raise RuntimeError(f"{path}: unexpected output lengths")
    print(path.parent.name, path.stem, f"{result['output_throughput']:.2f} tok/s", flush=True)


def speculative_config(args, release, project):
    if args.method == "dflash":
        if not args.draft_model:
            raise ValueError("DFlash 2 requires --draft-model")
        return {
            **project["methods"]["dflash"]["reference"]["spec"],
            "model": str(args.draft_model.resolve()),
        }
    spec = release["methods"][args.method]["spec"]
    if args.method == "eagle4":
        if not args.draft_model or not args.calibration:
            raise ValueError("EAGLE-4 requires --draft-model and --calibration")
        return {**spec, "model": str(args.draft_model.resolve()), "method_config": {
            **spec["method_config"], "data_path": str(args.calibration.resolve()),
        }}
    return spec


def verify_version(executable, expected, env):
    output = subprocess.check_output([executable, "--version"], env=env, text=True, timeout=60)
    actual = output.split()[-1]
    if actual != expected:
        raise ValueError(f"{executable}: expected vLLM {expected}, found {actual}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--method", choices=("suffix", "eagle4", "dflash"), required=True)
    parser.add_argument("--vllm", default="vllm", help="server's vLLM executable")
    parser.add_argument("--client-vllm", default="vllm", help="vLLM 0.34.0 benchmark client")
    parser.add_argument("--gpu", type=int, default=0)
    parser.add_argument("--port", type=int, default=24828)
    parser.add_argument("--model", default=TARGET)
    parser.add_argument("--bench-deps", default="")
    parser.add_argument("--draft-model", type=Path)
    parser.add_argument("--calibration", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    release, project = read_json(RELEASE), read_json(CONFIG)
    spec = speculative_config(args, release, project)
    env = environment(args)
    if args.method == "eagle4":
        env["VLLM_USE_V2_MODEL_RUNNER"] = "1"
    server_version = release["methods"][args.method]["vllm"] if args.method == "eagle4" else "0.34.0"
    verify_version(args.vllm, server_version, env)
    if args.client_vllm != args.vllm or server_version != "0.34.0":
        verify_version(args.client_vllm, "0.34.0", env)
    url = f"http://127.0.0.1:{args.port}"
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    signal.signal(signal.SIGTERM, terminate)
    with (output / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        for name in ("normal", args.method):
            if (output / name).exists():
                raise ValueError("Provide a fresh output directory for the paired benchmark")
        cells = list(cells_for(output, project["protocol"]))
        with reserve_gpu(args) as gpu:
            write_json(output / "experiment.json", {
                "gpu": gpu, "gpu_index": args.gpu, "target": args.model,
                "spec_bench_sha256": hashlib.sha256(DATASET.read_bytes()).hexdigest(),
                "cells": cells,
            })
            for role, profile in (("normal", None), (args.method, spec)):
                directory = output / role
                directory.mkdir()
                command = launch(args, profile)
                write_json(directory / "command.json", command)
                with running_server(command, env, url, directory / "server.log"):
                    for cell in cells:
                        benchmark(args.client_vllm, args, cell, directory / (cell["name"] + ".json"), env, url)


if __name__ == "__main__":
    main()
