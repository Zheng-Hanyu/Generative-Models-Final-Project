#!/usr/bin/env python3
"""Sequentially serve fixed-K configurations and benchmark each on one GPU."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable
VLLM = "/home/genai/.pixi/envs/default/bin/vllm"
TARGET = "/home/model/Qwen3.8-27B-FP8"
DSPARK = "/home/genai/models/Qwen3.8-27B-DSpark-vLLM"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def write_json(path: Path, value: dict) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def run(command: list[str]) -> None:
    print(f"K_SCAN_COMMAND: {command}", flush=True)
    subprocess.run(command, cwd=ROOT, check=True)


def server_command(method: str, k: int, gpu: int, port: int) -> list[str]:
    speculative: dict[str, object] = {"method": method, "num_speculative_tokens": k}
    if method == "dspark":
        speculative["model"] = DSPARK
    return [
        "/usr/bin/env",
        f"CUDA_VISIBLE_DEVICES={gpu}",
        "VLLM_USE_RUST_FRONTEND=1",
        VLLM,
        "serve",
        TARGET,
        "--served-model-name",
        "qwen-target",
        "--host",
        "127.0.0.1",
        "--port",
        str(port),
        "--tensor-parallel-size",
        "1",
        "--enable-auto-tool-choice",
        "--tool-call-parser",
        "qwen3_coder",
        "--reasoning-parser",
        "qwen3",
        "--mm-encoder-tp-mode",
        "data",
        "--max-model-len",
        "8192",
        "--max-num-seqs",
        "256",
        "--gpu-memory-utilization",
        "0.90",
        "--generation-config",
        "vllm",
        "--disable-log-requests",
        "--disable-prefix-caching",
        "--seed",
        "0",
        "--speculative-config",
        json.dumps(speculative, separators=(",", ":")),
    ]


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", choices=["mtp", "dspark"], required=True)
    parser.add_argument("--ks", nargs="+", type=int, required=True)
    parser.add_argument("--gpu", type=int, required=True)
    parser.add_argument("--port", type=int, required=True)
    parser.add_argument("--phase", default="kscan-r1")
    parser.add_argument("--label-prefix", required=True)
    parser.add_argument("--num-prompts", type=int, default=32)
    parser.add_argument("--seeds", nargs="+", type=int, default=[42])
    parser.add_argument("--concurrencies", nargs="+", type=int, default=[32, 16, 4, 1])
    args = parser.parse_args()

    manifest_path = ROOT / "results" / "processed" / f"{args.phase}-{args.method}-kscan-{args.label_prefix}-manifest.json"
    manifest: dict[str, object] = {
        "schema_version": 1,
        "phase": args.phase,
        "method_family": args.method,
        "gpu": args.gpu,
        "port": args.port,
        "ks": args.ks,
        "num_prompts": args.num_prompts,
        "seeds": args.seeds,
        "concurrencies": args.concurrencies,
        "started_at": utc_now(),
        "status": "running",
        "configurations": [],
    }
    records: list[dict[str, object]] = []
    manifest["configurations"] = records
    write_json(manifest_path, manifest)

    try:
        for k in args.ks:
            method_name = f"{args.method}-k{k}"
            server_label = f"{args.label_prefix}-server-{method_name}-gpu{args.gpu}"
            record: dict[str, object] = {
                "method": method_name,
                "k": k,
                "server_label": server_label,
                "started_at": utc_now(),
                "status": "starting_server",
            }
            records.append(record)
            write_json(manifest_path, manifest)
            try:
                run(
                    [
                        PYTHON,
                        str(ROOT / "bin" / "launch_detached.py"),
                        "--label",
                        server_label,
                        "--cwd",
                        str(ROOT),
                        "--",
                        *server_command(args.method, k, args.gpu, args.port),
                    ]
                )
                record["status"] = "benchmarking"
                write_json(manifest_path, manifest)
                run(
                    [
                        PYTHON,
                        str(ROOT / "src" / "run_benchmark_matrix.py"),
                        "--method",
                        method_name,
                        "--port",
                        str(args.port),
                        "--gpu",
                        str(args.gpu),
                        "--phase",
                        args.phase,
                        "--vllm",
                        VLLM,
                        "--num-prompts",
                        str(args.num_prompts),
                        "--seeds",
                        *(str(seed) for seed in args.seeds),
                        "--concurrencies",
                        *(str(c) for c in args.concurrencies),
                    ]
                )
                record["status"] = "completed"
            finally:
                stop = subprocess.run(
                    [
                        PYTHON,
                        str(ROOT / "bin" / "stop_logged.py"),
                        "--label",
                        server_label,
                        "--expect",
                        VLLM,
                        "--expect",
                        str(args.port),
                        "--timeout",
                        "120",
                    ],
                    cwd=ROOT,
                )
                record["stop_exit_code"] = stop.returncode
                record["finished_at"] = utc_now()
                if record["status"] != "completed":
                    record["status"] = "failed"
                write_json(manifest_path, manifest)
                if stop.returncode != 0:
                    raise RuntimeError(f"Failed to stop {server_label}")

        manifest["status"] = "completed"
        manifest["finished_at"] = utc_now()
        write_json(manifest_path, manifest)
        print(f"K_SCAN_COMPLETE: {manifest_path}", flush=True)
    except Exception as exc:
        manifest["status"] = "failed"
        manifest["finished_at"] = utc_now()
        manifest["error"] = repr(exc)
        write_json(manifest_path, manifest)
        raise


if __name__ == "__main__":
    main()
