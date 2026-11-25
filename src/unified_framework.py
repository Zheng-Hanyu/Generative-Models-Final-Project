#!/usr/bin/env python3
"""Serve, tune, measure and report vLLM speculative decoding profiles."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import math
import os
import random
import re
import shlex
import signal
import socket
import subprocess
from collections import defaultdict
from contextlib import contextmanager
from itertools import product
from pathlib import Path

from run_supplemental_benchmark import build_launch_command, environment, terminate, wait_for_server, warmup


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/unified_framework.json"
DATASET = ROOT / "data/spec_bench/question.jsonl"
CAPTURE_SIZES = [1, 2, 3, 4, 6, 8, 12, 16, 20, 24, 28, 32]
DRAFT_MODELS = {
    "dspark": "/home/genai/dspark-bench/redhat-dspark",
    "dflash": "/home/genai/selected-drafts/Qwen3.8-27B-DFlash2",
}


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


def draft_path(args, profile):
    spec = profile["spec"]
    if spec and spec["method"] in DRAFT_MODELS:
        return str(args.draft_model or spec.get("model") or DRAFT_MODELS[spec["method"]])
    return None


def config_command(args, profile):
    spec = profile["spec"]
    model = draft_path(args, profile)
    if model is not None:
        spec = {**spec, "model": model}
    return build_launch_command(args, spec, CAPTURE_SIZES)


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
        ("tuning", [protocol["tuning_seed"]], tuning, protocol["tuning_prompts"]),
        ("holdout", protocol["holdout_seeds"], holdout, protocol["holdout_prompts"]),
    ]
    directory.mkdir(exist_ok=True)
    manifest = {}
    for phase, seeds, rows, count in groups:
        cells = list(product(seeds, protocol["concurrencies"]))
        for index, (seed, concurrency) in enumerate(cells):
            name = cell_name(phase, concurrency, seed)
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


@contextmanager
def reserve_gpu(args):
    lock_path = Path.home() / f".speculative-decoding-lab-gpu-{args.gpu}.lock"
    with lock_path.open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fields = ("name", "uuid", "driver_version", "memory.used", "utilization.gpu")
        gpu = subprocess.check_output(
            ["nvidia-smi", "-i", str(args.gpu), "--query-gpu=" + ",".join(fields),
             "--format=csv,noheader,nounits"], text=True
        ).strip().split(", ")
        if int(gpu[-2]) > 512 or int(gpu[-1]) > 0:
            raise RuntimeError(f"GPU {args.gpu} is in use")
        with socket.socket() as connection:
            connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            connection.bind(("127.0.0.1", args.port))
        yield dict(zip(fields[:3], gpu[:3]))


@contextmanager
def running_server(command, env, url, log_path):
    with log_path.open("w", encoding="utf-8") as log:
        process = subprocess.Popen(command, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            wait_for_server(process, url, timeout=900)
            yield
        finally:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=25)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()


class Experiment:
    def __init__(self, args, config, gpu):
        self.args = args
        self.protocol = config["protocol"]
        self.method = config["methods"][args.method]
        self.normal = config["methods"]["normal"]["reference"]
        self.out = args.output.resolve()
        self.out.mkdir(parents=True, exist_ok=True)
        self.url = f"http://127.0.0.1:{args.port}"
        self.env = environment(args)
        self.external = load_serving_workloads(args.workloads) if getattr(args, "workloads", None) else None
        versions = subprocess.check_output([args.vllm, "--version"], env=self.env, text=True,
                                           stderr=subprocess.DEVNULL, timeout=60).splitlines()
        identity = {
            "method": args.method, "method_config": self.method, "protocol": self.protocol,
            "vllm_version": versions[-1].strip(), "gpu": {"index": args.gpu, **gpu}, "target": args.model,
            "draft": draft_path(args, self.method["reference"]),
            "dataset_sha256": hashlib.sha256(args.dataset.read_bytes()).hexdigest(),
        }
        if self.external:
            identity["external_workloads"] = self.external
        identity_path = self.out / "experiment.json"
        if identity_path.exists() and read_json(identity_path) != identity:
            raise ValueError("Existing output directory belongs to a different experiment")
        write_json(identity_path, identity)
        workloads = write_workloads(self.out / "workloads", args.dataset, self.protocol)
        write_json(self.out / "workloads.json", workloads)

    def benchmark_cell(self, directory, phase, concurrency, seed, cell=None):
        stress = self.protocol["stress"]
        name = cell_name(phase, concurrency, seed)
        path = directory / f"{name}.json"
        if cell is not None:
            count = cell["count"]
            request_path = self.args.workloads.resolve() / cell["input"]
            if phase == "speed":
                dataset = ["--dataset-name", "speed_bench", "--dataset-path", str(request_path.parent),
                           "--speed-bench-output-len", str(cell["fixed_output_tokens"]), "--no-oversample", "--ignore-eos"]
            else:
                dataset = ["--dataset-name", "timed_trace", "--dataset-path", str(request_path)]
        elif phase == "stress":
            count = stress["prompts"]
            dataset = [
                "--dataset-name", "random", "--random-input-len", str(stress["input_tokens"]),
                "--random-output-len", str(stress["output_tokens"]), "--random-range-ratio", "0", "--ignore-eos",
            ]
        else:
            count = self.protocol[f"{phase}_prompts"]
            dataset = [
                "--dataset-name", "spec_bench", "--dataset-path", str(self.out / "workloads" / f"{name}.jsonl"),
                "--spec-bench-output-len", str(self.protocol["output_tokens"]), "--no-oversample",
            ]
        warmup(self.url)
        command = [
            self.args.vllm, "bench", "serve", "--backend", "openai", "--endpoint", "/v1/completions",
            "--base-url", self.url, "--model", "qwen-fp8", "--tokenizer", self.args.model, *dataset,
            "--seed", str(seed), "--temperature", "0", "--num-warmups", "0", "--ready-check-timeout-sec", "0",
            "--request-rate", "inf", "--max-concurrency", str(concurrency), "--num-prompts", str(count),
            "--metric-percentiles", "50,95,99", "--save-detailed", "--save-result", "--result-dir", str(directory),
            "--result-filename", path.name,
        ]
        with path.with_suffix(".log").open("w", encoding="utf-8") as log:
            subprocess.run(command, env={**self.env, "PYTHONHASHSEED": "0"} if cell else self.env,
                           stdout=log, stderr=subprocess.STDOUT, check=True, timeout=300)
        result = read_json(path)
        speed = result["output_throughput"]
        if (result["completed"] != count or result["failed"] != 0
                or not math.isfinite(speed) or speed <= 0):
            raise RuntimeError(f"{name}: invalid result in {path}")
        if phase == "stress" and (result["input_lens"] != [stress["input_tokens"]] * count
                                  or result["output_lens"] != [stress["output_tokens"]] * count):
            raise RuntimeError(f"{name}: random stress token lengths differ from the protocol")
        if phase == "speed" and result["output_lens"] != [cell["fixed_output_tokens"]] * count:
            raise RuntimeError(f"{name}: SPEED-Bench output lengths differ from the protocol")
        if phase == "burst":
            trace = [json.loads(line) for line in request_path.read_text(encoding="utf-8").splitlines()]
            expected = ([row["input_length"] for row in trace], [row["output_length"] for row in trace])
            if (result["input_lens"], result["output_lens"]) != expected:
                raise RuntimeError(f"{name}: BurstGPT token lengths differ from the trace")
        print(f"  {directory.name} {name}: {speed:.2f} tok/s", flush=True)
        return speed

    def measure(self, profile, phase, stress=False):
        if not re.fullmatch(r"[a-zA-Z0-9_-]+", profile["id"]):
            raise ValueError(f"Invalid profile ID: {profile['id']}")
        destination = self.out / phase / profile["id"]
        command = config_command(self.args, profile)
        stamp = destination / "completed.json"
        if stamp.exists():
            record = read_json(stamp)
            if record["profile"] != profile or record["stress"] != stress:
                raise ValueError(f"{destination}: existing result uses different settings")
            return record
        destination.parent.mkdir(parents=True, exist_ok=True)
        attempts = destination.parent / ".attempts"
        attempts.mkdir(exist_ok=True)
        counter = 1
        while (attempts / f"{profile['id']}-{counter}").exists():
            counter += 1
        trial = attempts / f"{profile['id']}-{counter}"
        trial.mkdir()
        write_json(trial / "command.json", command)
        print(f"Starting {phase} {profile['id']}", flush=True)
        seeds = [self.protocol["tuning_seed"]] if phase == "tuning" else self.protocol["holdout_seeds"]
        speeds = {}
        with running_server(command, self.env, self.url, trial / "server.log"):
            if phase == "external":
                for cell in self.external["cells"]:
                    kind, concurrency, seed = cell["workload"], cell["concurrency"], cell["seed"]
                    speeds[cell_name(kind, concurrency, seed)] = self.benchmark_cell(trial, kind, concurrency, seed, cell)
            else:
                for seed, concurrency in product(seeds, self.protocol["concurrencies"]):
                    speeds[cell_name(phase, concurrency, seed)] = self.benchmark_cell(trial, phase, concurrency, seed)
            if stress:
                for concurrency, seed in stress_cells(self.protocol):
                    speeds[cell_name("stress", concurrency, seed)] = self.benchmark_cell(trial, "stress", concurrency, seed)
        record = {"profile": profile, "stress": stress, "speeds": speeds}
        write_json(trial / "completed.json", record)
        trial.rename(destination)
        return record

    def screen(self, profiles):
        rows = []
        for profile in profiles:
            try:
                speeds = self.measure(profile, "tuning")["speeds"].values()
            except (OSError, RuntimeError, subprocess.SubprocessError) as error:
                print(f"  {profile['id']}: {error}", flush=True)
                rows.append({"profile": profile, "error": str(error)})
            else:
                score = math.exp(sum(math.log(speed) for speed in speeds) / len(speeds))
                rows.append({"profile": profile, "score": score})
        return rows

    def tune(self):
        if self.args.method == "normal":
            raise ValueError("Normal has no speculative parameters to tune")
        phase1 = self.screen([self.method["reference"], *self.method["round1"]])
        valid1 = [row for row in phase1 if "score" in row]
        if len(valid1) < 2:
            raise RuntimeError("At least two valid profiles are needed in tuning round one")
        best = max(valid1, key=lambda row: row["score"])["profile"]
        updates = []
        for row in self.method["round2"]:
            merged = best["spec"] | row["override"]
            updates.append({"id": row["id"], "spec": {key: value for key, value in merged.items() if value is not None}})
        phase2 = self.screen(updates)
        valid2 = [row for row in phase2 if "score" in row]
        if not valid2:
            raise RuntimeError("No valid profiles in tuning round two")
        selected = max(valid1 + valid2, key=lambda row: row["score"])["profile"]
        write_json(self.out / "selection.json", {
            "method": self.args.method, "round1": phase1, "round2": phase2, "reference": self.method["reference"],
            "selected": selected,
        })
        print(f"Selected {selected['id']}", flush=True)

    def confirm(self):
        reference = self.method["reference"]
        if self.external:
            profiles = [self.normal] if reference == self.normal else [self.normal, reference]
            if self.args.gpu % 2 == 0:
                profiles.reverse()
            for profile in profiles:
                self.measure(profile, "external")
            write_json(self.out / "confirmation.json", {"normal": self.normal["id"], "selected": reference["id"]})
            return
        selection = self.out / "selection.json"
        selected = selected_profile(self.args.method, selection, reference) if selection.exists() else reference
        profiles = {profile["id"]: profile for profile in (self.normal, reference, selected)}
        ordered = list(profiles.values())
        # Alternate launch order by GPU. Every comparison stays on one GPU.
        if self.args.gpu % 2 == 0:
            ordered.reverse()
        for profile in ordered:
            self.measure(profile, "holdout", stress=not self.args.skip_stress)
        write_json(self.out / "confirmation.json", {
            "normal": self.normal["id"], "reference": reference["id"], "selected": selected["id"],
            "stress": not self.args.skip_stress,
        })


def selected_profile(method, path, reference):
    if path is None:
        return reference
    selected = read_json(path)
    if "methods" in selected:
        method_results = selected["methods"][method]
        selected = method_results["selection"]
        profile = method_results["recommended"]
    else:
        profile = selected["selected"]
    if selected["method"] != method:
        raise ValueError(f"{path}: selection belongs to {selected['method']}")
    if profile["spec"]["method"] != method:
        raise ValueError(f"{path}: selected profile does not match method {method}")
    return profile


def run_quantization_study(args, config, gpu):
    reference = config["methods"]["dflash"]["reference"]
    spec = {key: value for key, value in reference["spec"].items() if key != "quantization"}
    reference = {"id": f"dflash2-k{spec['num_speculative_tokens']}", "spec": spec}
    methods = {**config["methods"]}
    methods["dflash"] = {**methods["dflash"], "reference": reference}
    study_config = {**config, "methods": methods}
    candidates = [
        {"id": "dflash2-" + name.replace("_", "-"), "spec": {**spec, "quantization": name}}
        for name in args.quantizations
    ]
    if len({profile["id"] for profile in candidates}) != len(candidates):
        raise ValueError("Draft quantization names must produce distinct profile IDs")

    raw = args.output / "raw/dflash"
    screen_args = argparse.Namespace(**{**vars(args), "output": raw, "workloads": None, "skip_stress": False})
    experiment = Experiment(screen_args, study_config, gpu)
    first = experiment.screen([reference, *candidates[:2]])
    second = experiment.screen(candidates[2:])
    eligible = [row for row in first[1:] + second if "score" in row]
    if "score" not in first[0] or not eligible:
        raise RuntimeError("The BF16 reference and at least one quantized profile must finish screening")
    best = max(eligible, key=lambda row: row["score"])["profile"]
    write_json(raw / "selection.json", {
        "method": "dflash", "round1": first, "round2": second, "reference": reference, "selected": best,
    })
    print(f"Selected quantized draft for confirmation: {best['id']}", flush=True)
    experiment.confirm()

    external_dir = args.output / "external/dflash"
    external_args = argparse.Namespace(**{**vars(args), "output": external_dir})
    experiment = Experiment(external_args, study_config, gpu)
    for profile in (best, experiment.normal, reference):
        experiment.measure(profile, "external")
    write_json(external_dir / "confirmation.json", {
        "normal": experiment.normal["id"], "reference": reference["id"], "selected": best["id"],
    })


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=CONFIG)
    actions = parser.add_subparsers(dest="action", required=True)
    actions.add_parser("profiles")
    for action in ("serve", "tune", "benchmark", "quantization-study"):
        sub = actions.add_parser(action)
        if action == "quantization-study":
            sub.set_defaults(method="dflash")
            sub.add_argument("--quantizations", nargs="+", required=True)
            sub.add_argument("--workloads", type=Path, required=True)
        else:
            sub.add_argument("--method", required=True)
        sub.add_argument("--gpu", type=int, default=0)
        sub.add_argument("--port", type=int, default=24820)
        sub.add_argument("--model", default="/home/model/Qwen3.8-27B-FP8")
        sub.add_argument("--draft-model", type=Path)
        sub.add_argument("--vllm", default="/home/genai/.pixi/envs/default/bin/vllm")
        sub.add_argument("--bench-deps", default="")
        if action == "serve":
            sub.add_argument("--selection", type=Path)
            sub.add_argument("--print-command", action="store_true")
        else:
            sub.add_argument("--output", type=Path, required=True)
            sub.add_argument("--dataset", type=Path, default=DATASET)
        if action == "benchmark":
            sub.add_argument("--skip-stress", action="store_true")
            sub.add_argument("--workloads", type=Path, help="replay a prepared SPEED-Bench and BurstGPT manifest")
    report = actions.add_parser("report")
    report.add_argument("--results", type=Path, required=True)
    report.add_argument("--external-results", type=Path)
    report.add_argument("--draft-study", type=Path, help="include a completed DFlash 2 quantization study")
    report.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.action == "report":
        from unified_report import generate_report

        methods = read_json(args.config)["methods"] if args.results.is_dir() else None
        generate_report(args.results, args.output, args.external_results, methods, args.draft_study)
        print(f"Report written to {args.output}")
        return

    config = read_json(args.config)
    if args.action == "profiles":
        for method, row in config["methods"].items():
            print(f"{method:8} {row['label']:12} {row['reference']['id']}")
        return
    if args.method not in config["methods"]:
        parser.error(f"Unknown method {args.method}; choose from {', '.join(config['methods'])}")
    if args.action == "serve":
        if args.method == "normal" and args.selection:
            parser.error("Normal does not use a speculative selection")
        reference = config["methods"][args.method]["reference"]
        profile = selected_profile(args.method, args.selection, reference)
        command = config_command(args, profile)
        if args.print_command:
            print(shlex.join(command))
        else:
            os.execvpe(command[0], command, environment(args))
        return

    if args.action == "tune" and not all(config["methods"][args.method].get(round_name)
                                         for round_name in ("round1", "round2")):
        parser.error("Supply a tuning plan with round1 and round2 via --config")
    signal.signal(signal.SIGTERM, terminate)
    args.output.mkdir(parents=True, exist_ok=True)
    with (args.output / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        with reserve_gpu(args) as gpu:
            if args.action == "quantization-study":
                run_quantization_study(args, config, gpu)
                return
            experiment = Experiment(args, config, gpu)
            if args.action == "tune":
                experiment.tune()
            else:
                experiment.confirm()


if __name__ == "__main__":
    main()
