#!/usr/bin/env python3
"""Serve, tune, measure and report vLLM speculative decoding profiles."""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import math
import os
import re
import shlex
import signal
import subprocess
from tempfile import mkdtemp
from contextlib import contextmanager
from dataclasses import asdict, replace
from itertools import product
from pathlib import Path

from serving import (
    CAPTURE_SIZES, BenchmarkCell, benchmark_command, build_launch_command, environment,
    measure_cell, reserve_gpu, running_server, spec_bench_flags, terminate, vllm_version,
)
from workloads import (
    DATASET, cell_name, load_serving_workloads, prepare_external, prepare_inputs,
    read_json, serving_cell, stress_cells, write_json,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/unified_framework.json"
DRAFT_MODELS = {
    "dspark": "/home/genai/dspark-bench/redhat-dspark",
    "dflash": "/home/genai/selected-drafts/Qwen3.8-27B-DFlash2",
}


def draft_path(args, profile):
    spec = profile["spec"]
    if spec and spec["method"] in DRAFT_MODELS:
        return str(args.draft_model or spec.get("model") or DRAFT_MODELS[spec["method"]])
    return None


def config_command(args, profile, capture_sizes=CAPTURE_SIZES):
    spec = profile["spec"]
    model = draft_path(args, profile)
    if model is not None:
        spec = {**spec, "model": model}
    eagle = args.method == "eagle4"
    if eagle and spec:
        if args.draft_model is None:
            raise ValueError("EAGLE-4 requires --draft-model")
        calibration = args.calibration or ROOT / spec["method_config"]["data_path"]
        spec = {**spec, "model": str(args.draft_model.resolve()), "method_config": {
            **spec["method_config"], "data_path": str(calibration.resolve()),
        }}
    return build_launch_command(args, spec, capture_sizes, eagle=eagle)


def confirmation_profiles(args, config, selected=None):
    reference = config["methods"][args.method]["reference"]
    normal = config["methods"]["normal"]["reference"]
    if args.workloads:
        profiles = (normal, reference)
    else:
        if selected is None:
            selection = args.output / "selection.json"
            selected = selected_profile(args.method, selection if selection.exists() else None, reference)
        profiles = (normal, reference, selected)
    ordered = list({profile["id"]: profile for profile in profiles}.values())
    return ordered[::-1] if args.gpu % 2 == 0 else ordered


def new_attempt(destination):
    attempts = destination.parent / ".attempts"
    attempts.mkdir(parents=True, exist_ok=True)
    return Path(mkdtemp(prefix=f"{destination.name}-", dir=attempts))


def framework_cells(args, protocol, phase, stress=False, external=None):
    if phase == "external":
        return [serving_cell(args.workloads.resolve(), row) for row in external["cells"]]
    seeds = [protocol["tuning_seed"]] if phase == "tuning" else protocol["holdout_seeds"]
    cells = []
    for seed, concurrency in product(seeds, protocol["concurrencies"]):
        name = cell_name(phase, concurrency, seed)
        source = args.output.resolve() / "workloads" / f"{name}.jsonl"
        cells.append(BenchmarkCell(name, seed, concurrency, protocol[f"{phase}_prompts"],
                                   spec_bench_flags(source, protocol["output_tokens"])))
    if stress:
        setup = protocol["stress"]
        for concurrency, seed in stress_cells(protocol):
            dataset = ("--dataset-name", "random", "--random-input-len", str(setup["input_tokens"]),
                       "--random-output-len", str(setup["output_tokens"]), "--random-range-ratio", "0", "--ignore-eos")
            cells.append(BenchmarkCell(cell_name("stress", concurrency, seed), seed, concurrency, setup["prompts"],
                                       dataset, setup["input_tokens"], setup["output_tokens"]))
    return cells


class Experiment:
    def __init__(self, args, config, gpu):
        self.args = args
        self.config = config
        self.protocol = config["protocol"]
        self.method = config["methods"][args.method]
        self.normal = config["methods"]["normal"]["reference"]
        self.out = args.output.resolve()
        self.out.mkdir(parents=True, exist_ok=True)
        self.url = f"http://127.0.0.1:{args.port}"
        self.env = environment(args)
        self.external = load_serving_workloads(args.workloads) if getattr(args, "workloads", None) else None
        identity = {
            "method": args.method, "method_config": self.method, "protocol": self.protocol,
            "vllm_version": vllm_version(args.vllm, self.env), "gpu": {"index": args.gpu, **gpu}, "target": args.model,
            "draft": draft_path(args, self.method["reference"]),
            "dataset_sha256": hashlib.sha256(args.dataset.read_bytes()).hexdigest(),
        }
        if self.external:
            identity["external_workloads"] = self.external
        identity_path = self.out / "experiment.json"
        if identity_path.exists() and read_json(identity_path) != identity:
            raise ValueError("Existing output directory belongs to a different experiment")
        write_json(identity_path, identity)
        prepare_inputs(self.out, args.dataset, config, "framework")

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
        trial = new_attempt(destination)
        write_json(trial / "command.json", command)
        print(f"Starting {phase} {profile['id']}", flush=True)
        cells = framework_cells(self.args, self.protocol, phase, stress, self.external)
        env = {**self.env, "PYTHONHASHSEED": "0"} if phase == "external" else self.env
        with running_server(command, self.env, self.url, trial / "server.log"):
            speeds = {cell.name: measure_cell(self.args.vllm, self.args.model, self.url, cell,
                                               trial / f"{cell.name}.json", env) for cell in cells}
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
            for profile in confirmation_profiles(self.args, self.config):
                self.measure(profile, "external")
            write_json(self.out / "confirmation.json", {"normal": self.normal["id"], "selected": reference["id"]})
            return
        selection = self.out / "selection.json"
        selected = selected_profile(self.args.method, selection, reference) if selection.exists() else reference
        for profile in confirmation_profiles(self.args, self.config, selected):
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
    if profile["spec"]["method"] != reference["spec"]["method"]:
        raise ValueError(f"{path}: selected profile does not match method {method}")
    return profile


def quantization_profiles(args, config):
    published = config["methods"]["dflash"]["reference"]
    spec = {key: value for key, value in published["spec"].items() if key != "quantization"}
    reference = {"id": f"dflash2-k{spec['num_speculative_tokens']}", "spec": spec}
    candidates = [
        {"id": "dflash2-" + name.replace("_", "-"), "spec": {**spec, "quantization": name}}
        for name in args.quantizations
    ]
    if len({profile["id"] for profile in candidates}) != len(candidates):
        raise ValueError("Draft quantization names must produce distinct profile IDs")
    return reference, candidates


def run_quantization_study(args, config, gpu):
    reference, candidates = quantization_profiles(args, config)
    methods = {**config["methods"]}
    methods["dflash"] = {**methods["dflash"], "reference": reference}
    study_config = {**config, "methods": methods}
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


def quantization_plan(args, config):
    reference, candidates = quantization_profiles(args, config)
    protocol = config["protocol"]
    raw = argparse.Namespace(**{**vars(args), "output": args.output / "raw/dflash"})
    external = load_serving_workloads(args.workloads)
    prepare_inputs(raw.output.resolve(), args.dataset, config, "framework")
    normal = config["methods"]["normal"]["reference"]
    launches = {profile["id"]: (profile, config_command(args, profile)) for profile in [normal, reference, *candidates]}
    print_plan(args, "framework", args.vllm, f"http://127.0.0.1:{args.port}", launches,
               framework_cells(raw, protocol, "tuning"), args.output.resolve(), extra={
                   "holdout_and_stress": [asdict(cell) for cell in framework_cells(raw, protocol, "holdout", True)],
                   "external": [asdict(cell) for cell in framework_cells(args, protocol, "external", external=external)],
                   "confirmation": "Best tuning candidate, BF16 reference and Normal",
               })


@contextmanager
def lock_output(output):
    output.mkdir(parents=True, exist_ok=True)
    with (output / ".lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield


def study_name(config, method, requested):
    studies = config["studies"]
    if requested is None:
        return next(name for name, study in studies.items() if method in study["methods"])
    if requested not in studies or method not in studies[requested]["methods"]:
        raise ValueError(f"{method} is not available in the {requested} study")
    return requested


def paired_profiles(args, config, study):
    reference = config["methods"][args.method]["reference"]
    normal = config["methods"]["normal"]["reference"]
    if args.smoke:
        return [("selected", reference)]
    if study == "standard-suffix":
        profiles = [("selected", reference), ("baseline", normal)]
        return profiles[::-1] if args.gpu % 2 else profiles
    return [("normal", normal), (args.method, reference)]


def run_paired(args, config, study, dry_run=False):
    setup = config["studies"][study]
    if study == "paired" and args.method == "dflash" and args.draft_model is None:
        raise ValueError("DFlash 2 requires --draft-model for the paired study")
    capture = setup.get("capture_sizes", CAPTURE_SIZES)
    eagle = args.method == "eagle4"
    expected_client = setup["client_version"]
    expected_server = config["methods"][args.method].get("vllm", expected_client)
    client = args.client_vllm or args.vllm
    if eagle and client == args.vllm:
        raise ValueError("EAGLE-4 requires a separate vLLM 0.34.0 --client-vllm")
    env = environment(args, eagle=eagle)
    output = args.output.resolve()
    url = f"http://127.0.0.1:{args.port}"
    launches = {
        role: (profile, config_command(args, profile, capture))
        for role, profile in paired_profiles(args, config, study)
    }
    cells = prepare_inputs(output, args.dataset, config, study)
    if args.smoke:
        workload, digest, first = cells[0]
        cells = [(workload, digest, replace(first, count=4))]
    if dry_run:
        print_plan(args, study, client, url, launches, [cell for _, _, cell in cells], output,
                   extra={"server_version": expected_server, "client_version": expected_client,
                          "server_environment": {"VLLM_USE_V2_MODEL_RUNNER": "1"} if eagle else {}})
        return

    server_version = vllm_version(args.vllm, env)
    if server_version.split()[-1] != expected_server:
        raise ValueError(f"{args.vllm}: expected vLLM {expected_server}, found {server_version}")
    if client != args.vllm:
        client_version = vllm_version(client, env)
        if client_version.split()[-1] != expected_client:
            raise ValueError(f"{client}: expected vLLM {expected_client}, found {client_version}")
    with reserve_gpu(args) as gpu:
        experiment = {
            "study": study, "method": args.method, "gpu": {**gpu, "index": args.gpu},
            "target": args.model, "server_version": expected_server, "client_version": expected_client,
            "profile": config["methods"][args.method]["reference"], "serving_commands": {
                role: command for role, (_, command) in launches.items()
            },
            "dataset_sha256": hashlib.sha256(args.dataset.read_bytes()).hexdigest(), "smoke": args.smoke,
            "cells": [{"workload": workload, "sha256": digest, **asdict(cell), "dataset": list(cell.dataset)} for workload, digest, cell in cells],
        }
        identity = output / "experiment.json"
        if identity.exists() and read_json(identity) != experiment:
            raise ValueError(f"{output}: existing results belong to a different experiment")
        write_json(identity, experiment)
        for role, (profile, command) in launches.items():
            directory = output / role
            if (directory / "completed.json").exists():
                continue
            trial = new_attempt(directory)
            write_json(trial / "command.json", command)
            with running_server(command, env, url, trial / "server.log", timeout=360 if study == "standard-suffix" else 900):
                speeds = {cell.name: measure_cell(client, args.model, url, cell, trial / f"{cell.name}.json", env)
                          for _, _, cell in cells}
            write_json(trial / "completed.json", {"profile": profile, "speeds": speeds})
            trial.rename(directory)


def print_plan(args, study, client, url, launches, cells, output, extra=None):
    plan = {
        "study": study, "method": args.method, "gpu": args.gpu,
        "profiles": {role: command for role, (_, command) in launches.items()},
        "cells": [asdict(cell) for cell in cells],
        "example_benchmark": benchmark_command(client, args.model, url, cells[0], output / f"{cells[0].name}.json"),
        **(extra or {}),
    }
    print(json.dumps(plan, ensure_ascii=False, indent=2))


def framework_plan(args, config):
    prepare_inputs(args.output.resolve(), args.dataset, config, "framework")
    phase = "external" if args.workloads else "holdout"
    external = load_serving_workloads(args.workloads) if args.workloads else None
    cells = framework_cells(args, config["protocol"], phase, not args.skip_stress and not args.workloads, external)
    launches = {profile["id"]: (profile, config_command(args, profile)) for profile in confirmation_profiles(args, config)}
    print_plan(args, "framework", args.vllm, f"http://127.0.0.1:{args.port}", launches, cells, args.output.resolve())


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=CONFIG)
    actions = parser.add_subparsers(dest="action", required=True)
    actions.add_parser("profiles", help="list published profiles and study names")
    prepare = actions.add_parser("prepare", help="prepare benchmark input files")
    prepare.add_argument("--study", choices=("framework", "paired", "standard-suffix", "external"), default="framework")
    prepare.add_argument("--dataset", type=Path, default=DATASET)
    prepare.add_argument("--speed-parquet", type=Path)
    prepare.add_argument("--burst-csv", type=Path)
    prepare.add_argument("--output", type=Path, required=True)
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
        sub.add_argument("--vllm", default="vllm")
        sub.add_argument("--bench-deps", default="")
        if action in ("serve", "benchmark"):
            sub.add_argument("--study", choices=("framework", "paired", "standard-suffix"))
            sub.add_argument("--calibration", type=Path, help="EAGLE-4 cost-table directory (defaults to the published tables)")
        if action == "serve":
            sub.add_argument("--selection", type=Path)
            sub.add_argument("--print-command", action="store_true")
        else:
            sub.add_argument("--output", type=Path, required=True)
            sub.add_argument("--dataset", type=Path, default=DATASET)
        if action in ("benchmark", "quantization-study"):
            sub.add_argument("--print-plan", action="store_true", help="prepare inputs and print the run plan without a GPU")
        if action == "benchmark":
            sub.add_argument("--skip-stress", action="store_true")
            sub.add_argument("--workloads", type=Path, help="replay a prepared SPEED-Bench and BurstGPT manifest")
            sub.add_argument("--client-vllm", help="separate vLLM 0.34.0 benchmark client for the paired study")
            sub.add_argument("--smoke", action="store_true", help="for standard Suffix, run four requests with Suffix only")
    report = actions.add_parser("report", help="render tables and figures")
    report.add_argument("--study", choices=("framework", "paired", "standard-suffix"))
    report.add_argument("--results", type=Path, help="a summary JSON or a replay directory; defaults to all published studies")
    report.add_argument("--external-results", type=Path)
    report.add_argument("--draft-study", type=Path, help="include a completed DFlash 2 quantization study")
    report.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = read_json(args.config)
    if "studies" not in config:
        config["studies"] = {"framework": {"methods": list(config["methods"])}}
    try:
        dispatch(args, config)
    except ValueError as error:
        parser.error(str(error))


def dispatch(args, config):
    if args.action == "report":
        from unified_report import report_studies

        report_studies(args, config)
        print(f"Report written to {args.output}")
        return
    if args.action == "profiles":
        for method, row in config["methods"].items():
            studies = ", ".join(name for name, group in config["studies"].items() if method in group["methods"])
            print(f"{method:16} {row['label']:17} {row['reference']['id']:21} {studies}")
        return
    if args.action == "prepare":
        if args.study == "external":
            if args.speed_parquet is None or args.burst_csv is None:
                raise ValueError("External preparation requires --speed-parquet and --burst-csv")
            prepare_external(args.output, args.dataset, args.speed_parquet, args.burst_csv)
        else:
            if args.speed_parquet or args.burst_csv:
                raise ValueError("Use --study external with --speed-parquet or --burst-csv")
            if args.study not in config["studies"]:
                raise ValueError(f"Configuration has no {args.study} study")
            with lock_output(args.output):
                prepare_inputs(args.output.resolve(), args.dataset, config, args.study)
        print(f"Inputs written to {args.output}")
        return
    if args.method not in config["methods"]:
        raise ValueError(f"Unknown method {args.method}. Choose from {', '.join(config['methods'])}")
    study = study_name(config, args.method, getattr(args, "study", None))
    if args.action == "serve":
        if args.method == "normal" and args.selection:
            raise ValueError("Normal does not use a speculative selection")
        reference = config["methods"][args.method]["reference"]
        profile = selected_profile(args.method, args.selection, reference)
        command = config_command(args, profile, config["studies"][study].get("capture_sizes", CAPTURE_SIZES))
        if args.print_command:
            print(shlex.join(command))
        else:
            os.execvpe(command[0], command, environment(args, eagle=args.method == "eagle4"))
        return

    if args.action == "tune" and (study != "framework" or not all(
        config["methods"][args.method].get(round_name) for round_name in ("round1", "round2")
    )):
        raise ValueError("Supply a framework tuning plan with round1 and round2 via --config")
    if args.action == "benchmark":
        if args.smoke and study != "standard-suffix":
            raise ValueError("--smoke is for the standard-suffix study")
        if study == "framework" and args.client_vllm:
            raise ValueError("--client-vllm is for paired studies")
        if study != "framework" and (args.workloads or args.skip_stress):
            raise ValueError("--workloads and --skip-stress are for the framework study")

    signal.signal(signal.SIGTERM, terminate)
    with lock_output(args.output):
        if getattr(args, "print_plan", False):
            if args.action == "quantization-study":
                quantization_plan(args, config)
            elif study == "framework":
                framework_plan(args, config)
            else:
                run_paired(args, config, study, dry_run=True)
            return
        if study != "framework":
            run_paired(args, config, study)
            return
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
