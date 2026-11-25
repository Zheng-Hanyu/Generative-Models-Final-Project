#!/usr/bin/env python3
"""Run one method's reproducible benchmark matrix through the audit wrapper."""

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
RUN_LOGGED = ROOT / "bin" / "run_logged.py"


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n")
    temporary.replace(path)


def wait_until_ready(base_url, timeout=900):
    deadline = time.monotonic() + timeout
    last_error = None
    while time.monotonic() < deadline:
        try:
            with urllib.request.urlopen(base_url + "/health", timeout=3) as response:
                if response.status == 200:
                    print(f"Server ready: {base_url}", flush=True)
                    return
        except Exception as exc:  # Startup errors are preserved in the server log.
            last_error = repr(exc)
        time.sleep(2)
    raise RuntimeError(f"Server did not become ready at {base_url}: {last_error}")


def run_audited(label, command):
    argv = [
        sys.executable,
        str(RUN_LOGGED),
        "--label",
        label,
        "--cwd",
        str(ROOT),
        "--",
        *command,
    ]
    print(f"MATRIX_COMMAND: {label}: {command}", flush=True)
    return subprocess.run(argv, cwd=ROOT).returncode


def validate_result(path, expected_requests, expected_output_len):
    data = json.loads(path.read_text())
    output_lens = data.get("output_lens", [])
    errors = [error for error in data.get("errors", []) if error]
    checks = {
        "completed_matches": data.get("completed") == expected_requests,
        "no_failed_requests": data.get("failed") == 0,
        "no_error_strings": not errors,
        "request_level_output_lengths_present": len(output_lens) == expected_requests,
        "all_output_lengths_exact": all(
            length == expected_output_len for length in output_lens
        ),
        "total_output_tokens_exact": data.get("total_output_tokens")
        == expected_requests * expected_output_len,
        "positive_duration": data.get("duration", 0) > 0,
        "positive_output_throughput": data.get("output_throughput", 0) > 0,
    }
    summary = {
        "valid": all(checks.values()),
        "checks": checks,
        "completed": data.get("completed"),
        "failed": data.get("failed"),
        "total_output_tokens": data.get("total_output_tokens"),
        "duration": data.get("duration"),
        "output_throughput": data.get("output_throughput"),
        "mean_tpot_ms": data.get("mean_tpot_ms"),
        "spec_decode_acceptance_rate": data.get("spec_decode_acceptance_rate"),
        "spec_decode_acceptance_length": data.get("spec_decode_acceptance_length"),
    }
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--method", required=True)
    parser.add_argument("--port", required=True, type=int)
    parser.add_argument("--gpu", required=True, type=int)
    parser.add_argument("--phase", default="formal-r1")
    parser.add_argument("--vllm", required=True)
    parser.add_argument("--tokenizer", default="/home/model/Qwen3.8-27B-FP8")
    parser.add_argument("--concurrencies", nargs="+", type=int, default=[32, 16, 4, 1])
    parser.add_argument("--seeds", nargs="+", type=int, default=[42, 43, 44])
    parser.add_argument("--num-prompts", type=int, default=128)
    parser.add_argument("--input-len", type=int, default=1024)
    parser.add_argument("--output-len", type=int, default=512)
    parser.add_argument("--dataset-name", choices=["random", "spec_bench"], default="random")
    parser.add_argument("--dataset-path")
    parser.add_argument("--spec-bench-category")
    args = parser.parse_args()

    base_url = f"http://127.0.0.1:{args.port}"
    if args.method == "normal":
        method, k = "normal", 0
    else:
        match = re.fullmatch(r"(mtp|dspark)(?:-k(\d+)|-(?:dynamic|adaptive)(?:-[a-z]+)?)", args.method)
        if not match:
            parser.error(
                "--method must be normal, mtp-kN, dspark-kN, "
                "mtp-dynamic[-variant], or dspark-adaptive[-variant]"
            )
        method = match.group(1)
        k = int(match.group(2)) if match.group(2) is not None else -1
    manifest_path = ROOT / "results" / "processed" / f"{args.phase}-{args.method}-matrix-manifest.json"
    manifest = {
        "schema_version": 1,
        "phase": args.phase,
        "method": args.method,
        "gpu": args.gpu,
        "base_url": base_url,
        "num_prompts_per_run": args.num_prompts,
        "input_len": args.input_len if args.dataset_name == "random" else None,
        "output_len": args.output_len,
        "dataset_name": args.dataset_name,
        "dataset_path": args.dataset_path,
        "spec_bench_category": args.spec_bench_category,
        "concurrencies": args.concurrencies,
        "seeds": args.seeds,
        "prefix_caching": False,
        "started_at": utc_now(),
        "status": "waiting_for_server",
        "runs": [],
    }
    write_json(manifest_path, manifest)
    wait_until_ready(base_url)
    manifest["status"] = "running"
    manifest["server_ready_at"] = utc_now()
    write_json(manifest_path, manifest)

    if args.dataset_name == "random":
        dataset_arguments = [
            "--dataset-name",
            "random",
            "--random-input-len",
            str(args.input_len),
            "--random-output-len",
            str(args.output_len),
            "--random-range-ratio",
            "0",
        ]
        workload_tag = f"i{args.input_len}-o{args.output_len}"
    else:
        if not args.dataset_path:
            parser.error("--dataset-path is required for Spec-Bench")
        dataset_arguments = [
            "--dataset-name",
            "spec_bench",
            "--dataset-path",
            args.dataset_path,
            "--spec-bench-output-len",
            str(args.output_len),
        ]
        if args.spec_bench_category:
            dataset_arguments += ["--spec-bench-category", args.spec_bench_category]
        workload_tag = f"specbench-o{args.output_len}"

    common = [
        "/usr/bin/env",
        f"CUDA_VISIBLE_DEVICES={args.gpu}",
        args.vllm,
        "bench",
        "serve",
        "--backend",
        "openai",
        "--base-url",
        base_url,
        "--endpoint",
        "/v1/completions",
        "--model",
        "qwen-target",
        "--tokenizer",
        args.tokenizer,
        *dataset_arguments,
        "--request-rate",
        "inf",
        "--ignore-eos",
        "--temperature",
        "0",
        "--top-p",
        "1",
        "--top-k",
        "-1",
        "--percentile-metrics",
        "ttft,tpot,itl,e2el",
        "--metric-percentiles",
        "50,90,95,99",
        "--disable-tqdm",
    ]

    try:
        for concurrency in args.concurrencies:
            warmup_label = f"warmup-{args.phase}-{args.method}-c{concurrency}"
            warmup_command = [
                *common,
                "--num-prompts",
                str(max(4, concurrency)),
                "--num-warmups",
                "0",
                "--max-concurrency",
                str(concurrency),
                "--seed",
                str(1000 + concurrency),
                "--request-id-prefix",
                warmup_label + "-",
            ]
            return_code = run_audited(warmup_label, warmup_command)
            if return_code != 0:
                raise RuntimeError(f"Warmup failed: {warmup_label}, exit={return_code}")

            for seed in args.seeds:
                label = f"{args.phase}-{args.method}-{workload_tag}-c{concurrency}-s{seed}"
                filename = label + ".json"
                result_path = ROOT / "results" / "raw" / filename
                command = [
                    *common,
                    "--num-prompts",
                    str(args.num_prompts),
                    "--num-warmups",
                    "0",
                    "--max-concurrency",
                    str(concurrency),
                    "--seed",
                    str(seed),
                    "--request-id-prefix",
                    label + "-",
                    "--save-result",
                    "--save-detailed",
                    "--result-dir",
                    str(ROOT / "results" / "raw"),
                    "--result-filename",
                    filename,
                    "--metadata",
                    f"method_name={args.method}",
                    f"dataset_name={args.dataset_name}",
                    f"mode={method}",
                    f"k={k}",
                    f"gpu={args.gpu}",
                    f"phase={args.phase}",
                    f"concurrency={concurrency}",
                    f"seed={seed}",
                    "prefix_cache=false",
                ]
                run_record = {
                    "label": label,
                    "concurrency": concurrency,
                    "seed": seed,
                    "command": command,
                    "result_path": str(result_path),
                    "started_at": utc_now(),
                    "status": "running",
                }
                manifest["runs"].append(run_record)
                write_json(manifest_path, manifest)
                return_code = run_audited(label, command)
                run_record["finished_at"] = utc_now()
                run_record["exit_code"] = return_code
                if return_code != 0 or not result_path.exists():
                    run_record["status"] = "failed"
                    write_json(manifest_path, manifest)
                    raise RuntimeError(
                        f"Benchmark failed: {label}, exit={return_code}, result={result_path}"
                    )
                validation = validate_result(
                    result_path, args.num_prompts, args.output_len
                )
                run_record["validation"] = validation
                run_record["status"] = "completed" if validation["valid"] else "invalid"
                write_json(manifest_path, manifest)
                print(f"RUN_VALIDATION: {label}: {validation}", flush=True)
                if not validation["valid"]:
                    raise RuntimeError(f"Result validation failed: {label}: {validation}")

        manifest["status"] = "completed"
        manifest["finished_at"] = utc_now()
        write_json(manifest_path, manifest)
        print(f"MATRIX_COMPLETE: {manifest_path}", flush=True)
        return 0
    except Exception as exc:
        manifest["status"] = "failed"
        manifest["finished_at"] = utc_now()
        manifest["error"] = repr(exc)
        write_json(manifest_path, manifest)
        print(f"MATRIX_FAILED: {exc!r}", flush=True)
        raise


if __name__ == "__main__":
    raise SystemExit(main())
