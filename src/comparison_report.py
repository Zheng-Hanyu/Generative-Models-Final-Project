"""Read and report the paired EAGLE-4 and DFlash 2 benchmarks."""
from __future__ import annotations

import hashlib
from collections import defaultdict
from itertools import product
from math import ceil, isfinite
from pathlib import Path
from statistics import geometric_mean, median

from plot_style import BASELINE, METHOD_STYLES, MUTED, save_plot, speed_bars
from serving import DEFAULT_MAX_BATCHED_TOKENS
from workloads import cell_name, read_json, write_json

WORKLOADS = (("spec-bench", "Spec-Bench 留出集"), ("repetition", "重复代码与 JSON"))
WORKLOAD_TITLES = (("spec-bench", "Spec-Bench holdout"), ("repetition", "Repetitive code / JSON"))
PAIRED_STYLES = (
    ("eagle4", "EAGLE-4"),
    ("dflash", "DFlash 2"),
)
METRICS = ("output_throughput", "p95_ttft_ms", "p95_tpot_ms")


def profile_for(data, method):
    profile = data["winners"].get(method)
    return profile if profile in data["profiles"] else None


def retain_methods(data, methods):
    profiles = data["profiles"]
    retained = {}
    for method, metadata in methods.items():
        profile = data["winners"].get(method, metadata["reference"]["id"])
        if profile in profiles:
            retained[method] = profile
    if not retained:
        raise ValueError("Summary contains no configured methods")
    needed = set(retained.values()) | {profiles[key]["baseline"] for key in retained.values()}
    result = {**data, "winners": retained, "profiles": {key: profile for key, profile in profiles.items() if key in needed}}
    experiment = data.get("experiment", {})
    if "lanes" in experiment:
        result["experiment"] = {**experiment, "lanes": {method: lane for method, lane in experiment["lanes"].items()
                                                         if method in retained}}
    if data["winners"].keys() - retained.keys():
        result.pop("failed_candidate_counts", None)
        if "selection" in data:
            result["selection"] = {method: data["selection"][method] for method in retained}
        if "dflash" not in retained:
            result.pop("diagnosis", None)
    return result


def collect_paired(root, config, study):
    spec = config["studies"][study]
    protocol = spec.get("protocol", config["protocol"])
    workloads = ("spec-bench", "repetition") if study == "paired" else ("spec-bench",)
    expected = set(product(workloads, protocol["concurrencies"], protocol["holdout_seeds"]))
    reused_prompts = protocol.get("reuse_prompts_by_seed", False)
    lanes = [root] if (root / "experiment.json").is_file() else [
        root / method for method in spec["methods"] if (root / method / "experiment.json").is_file()
    ]
    if not lanes:
        raise ValueError(f"{root}: no completed {study} replay directories")
    data = {"winners": {}, "profiles": {}}
    signature = None
    for lane in lanes:
        identity = read_json(lane / "experiment.json")
        method = identity["method"]
        if (identity["study"] != study or method not in spec["methods"]
                or method in data["winners"]):
            raise ValueError(f"{lane}: expected a full {study} benchmark")
        cells = {(item["workload"], item["concurrency"], item["seed"]): item for item in identity["cells"]}
        if (set(cells) != expected or len(cells) != len(identity["cells"])
                or any(cell["count"] != protocol["holdout_prompts"] or cell["name"] != cell_name(
                    workload if study == "paired" else "holdout", concurrency, seed)
                    for (workload, concurrency, seed), cell in cells.items())):
            raise ValueError(f"{lane}: replay cells differ from the configured protocol")
        current = (Path(identity["target"]).name, identity["gpu"]["name"], identity["gpu"]["driver_version"],
                   identity["client_version"], identity["dataset_sha256"],
                   {key: cell["sha256"] for key, cell in cells.items()})
        if signature is not None and current != signature:
            raise ValueError(f"{lane}: inputs, client or hardware differ from the other methods")
        signature = current
        if reused_prompts:
            for seed in protocol["holdout_seeds"]:
                hashes = {cell["sha256"] for (_, _, run_seed), cell in cells.items() if run_seed == seed}
                if len(hashes) != 1:
                    raise ValueError(f"{lane}: concurrency levels must share the same prompts per seed")
            if len({cell["sha256"] for cell in cells.values()}) != len(protocol["holdout_seeds"]):
                raise ValueError(f"{lane}: trial prompt sets must differ")
            experiment = data.setdefault("experiment", {
                "study": study, "target": current[0], "gpu": current[1], "driver": current[2],
                "client_version": current[3], "dataset_sha256": current[4], "protocol": protocol, "lanes": {},
            })
            experiment["lanes"][method] = {
                "gpu_index": identity["gpu"]["index"], "server_version": identity["server_version"],
                "order": list(identity["serving_commands"]),
            }
        profile = identity["profile"]
        label = profile["id"]
        baseline = f"normal-{method}"
        data["winners"][method] = label
        roles = ("normal", method)
        lengths = {}
        for role, key, control in zip(roles, (baseline, label), (None, baseline), strict=True):
            directory = lane / role
            record = read_json(directory / "completed.json")
            expected_profile = config["methods"]["normal"]["reference"] if control is None else profile
            if record["profile"] != expected_profile:
                raise ValueError(f"{directory}: profile does not match the experiment")
            rows = defaultdict(list)
            for (workload, concurrency, seed), cell in sorted(cells.items()):
                name = cell["name"]
                result_path = directory / f"{name}.json"
                result = read_json(result_path)
                if (result["completed"], result["failed"], result["max_concurrency"]) != (cell["count"], 0, concurrency):
                    raise ValueError(f"{result_path}: incomplete benchmark or wrong concurrency")
                if result["output_throughput"] != record["speeds"][name] or any(
                    not isfinite(result[metric]) or result[metric] <= 0 for metric in METRICS
                ):
                    raise ValueError(f"{result_path}: invalid benchmark metrics")
                row = {
                    "seed": seed, "completed": result["completed"], "failed": result["failed"],
                    "test_input_sha256": cell["sha256"], "raw_result_sha256": hashlib.sha256(result_path.read_bytes()).hexdigest(),
                    **{metric: result[metric] for metric in METRICS},
                    "spec_decode_acceptance_rate": result.get("spec_decode_acceptance_rate"),
                }
                if reused_prompts:
                    input_lens = result["input_lens"]
                    if len(input_lens) != cell["count"] or lengths.setdefault(seed, input_lens) != input_lens:
                        raise ValueError(f"{result_path}: input sequence differs by role or concurrency")
                    row.update({metric: result[metric] for metric in ("total_output_tokens", "duration")})
                rows[workload, concurrency].append(row)
            data["profiles"][key] = {"spec": record["profile"]["spec"], "baseline": control, "rows": [
                {"workload": workload, "concurrency": concurrency, "runs": matches}
                for (workload, concurrency), matches in rows.items()
            ]}
            if study == "high-load":
                data["profiles"][key]["max_num_batched_tokens"] = expected_profile.get(
                    "max_num_batched_tokens", DEFAULT_MAX_BATCHED_TOKENS
                )
    return data


def paired_runs(profiles, method, workload, metric):
    profile = profiles[method]
    control = profiles[profile["baseline"]]
    baselines = {
        (row["concurrency"], run["seed"]): run[metric]
        for row in control["rows"] if row["workload"] == workload
        for run in row["runs"]
    }
    cells = {
        row["concurrency"]: [
            run[metric] / baselines[row["concurrency"], run["seed"]] for run in row["runs"]
        ]
        for row in profile["rows"] if row["workload"] == workload
    }
    return dict(sorted(cells.items()))


def plot_paired(data, output, plt):
    from matplotlib.legend_handler import HandlerTuple
    from matplotlib.lines import Line2D

    profiles = data["profiles"]
    methods = [(method, profile, label) for method, label in PAIRED_STYLES
               if (profile := profile_for(data, method)) is not None]
    fig, axes = plt.subplots(3, 2, figsize=(7.7, 6.55), sharex="col", sharey="row")
    peak = 1.0
    ratios_peak = 1.0
    for column, (workload, label) in enumerate(WORKLOAD_TITLES):
        speed, latency, acceptance = axes[:, column]
        groups = {method: paired_runs(profiles, profile, workload, "output_throughput")
                  for method, profile, _ in methods}
        peak = max(peak, speed_bars(speed, groups))
        speed.set_title(label, loc="center", pad=10)
        latency.axhline(1, color=BASELINE, linestyle="--", linewidth=1.0)
        latency.grid(axis="y")
        acceptance.grid(axis="y")
        for method, profile, _ in methods:
            color, marker, style = METHOD_STYLES[method]
            values = paired_runs(profiles, profile, workload, "p95_tpot_ms")
            medians = [median(runs) for runs in values.values()]
            ratios_peak = max(ratios_peak, max(medians))
            latency.plot(range(len(values)), medians, color=color, marker=marker, linestyle=style)
            rows = {row["concurrency"]: row["runs"] for row in profiles[profile]["rows"] if row["workload"] == workload}
            rates = []
            for concurrency in values:
                rates_in_run = [run["spec_decode_acceptance_rate"] for run in rows[concurrency]
                                if run["spec_decode_acceptance_rate"] is not None]
                rates.append(median(rates_in_run) if rates_in_run else float("nan"))
            acceptance.plot(range(len(values)), rates, color=color, marker=marker, linestyle=style)
            acceptance.set_xticks(range(len(values)), list(values))
    axes[0, 0].set_ylim(0, ceil(2.15 * peak) / 2)
    axes[1, 0].set_ylim(0, max(1.25, ceil(4.1 * ratios_peak) / 4))
    axes[2, 0].set_ylim(0, 100)
    axes[2, 0].set_yticks([0, 25, 50, 75, 100])
    for row, name in zip(axes, ("Output throughput / Normal", "P95 TPOT / Normal", "Draft acceptance (%)"), strict=True):
        row[0].set_ylabel(name)
    for index, ax in enumerate(axes.flat):
        ax.text(0.025, 0.95, f"({chr(97 + index)})", transform=ax.transAxes, va="top",
                fontsize=8.8, fontweight="bold", color=MUTED)
    fig.supxlabel("Concurrent requests", y=0.025)
    patches, _ = axes[0, 0].get_legend_handles_labels()
    handles = []
    for patch, (method, _, _) in zip(patches, methods, strict=True):
        color, marker, style = METHOD_STYLES[method]
        handles.append((patch, Line2D([], [], color=color, marker=marker, linestyle=style)))
    fig.legend(handles, [label for _, _, label in methods], loc="upper center",
               bbox_to_anchor=(0.5, 0.992), ncol=len(methods), handlelength=3.25,
               handler_map={tuple: HandlerTuple(ndivide=None, pad=0.3)})
    fig.subplots_adjust(left=0.105, right=0.98, bottom=0.095, top=0.886, wspace=0.16, hspace=0.19)
    save_plot(fig, plt, output, "eagle4-dflash")


def render_paired(data):
    profiles = data["profiles"]
    methods = [(profile_for(data, method), label) for method, label in PAIRED_STYLES]
    methods = [(profile, label) for profile, label in methods if profile is not None]
    lines = ["# EAGLE-4 与 DFlash 2", "",
             "同一档并发先计算各轮相对同构建 Normal 的倍率，再取中位数。综合倍率取各档中位倍率的几何平均。", "",
             "| 方法 | Spec-Bench | 重复代码与 JSON |", "|---|---:|---:|"]
    for profile, label in methods:
        values = [geometric_mean(median(cell) for cell in paired_runs(
            profiles, profile, workload, "output_throughput").values()) for workload, _ in WORKLOADS]
        lines.append(f"| {label} | {values[0]:.3f}× | {values[1]:.3f}× |")
    lines.extend(["", "![配对吞吐、P95 每 token 延迟和草稿接受率](figures/eagle4-dflash.png)", "",
                  "吞吐须线覆盖各轮最小值和最大值。虚线对应同构建 Normal。"])
    for workload, title in WORKLOADS:
        lines.extend(["", f"## {title}", "",
                      "| 方法 | 并发 | Normal (tok/s) | 方法 (tok/s) | 配对吞吐倍率 | P95 TTFT 倍率（中位数及范围） | P95 TPOT 倍率 | 草稿接受率 |",
                      "|---|---:|---:|---:|---:|---:|---:|---:|"])
        for profile, label in methods:
            item = profiles[profile]
            controls = {row["concurrency"]: row["runs"] for row in profiles[item["baseline"]]["rows"]
                        if row["workload"] == workload}
            ratios = [paired_runs(profiles, profile, workload, metric) for metric in METRICS]
            for row in sorted(item["rows"], key=lambda row: row["concurrency"]):
                if row["workload"] != workload:
                    continue
                c = row["concurrency"]
                control = median(run["output_throughput"] for run in controls[c])
                tps = median(run["output_throughput"] for run in row["runs"])
                speed, ttft, tpot = (median(values[c]) for values in ratios)
                ttft_samples = ratios[1][c]
                acceptance = [run["spec_decode_acceptance_rate"] for run in row["runs"]
                              if run["spec_decode_acceptance_rate"] is not None]
                rates = f"{median(acceptance):.1f}%" if acceptance else "—"
                lines.append(f"| {label} | {c} | {control:.2f} | {tps:.2f} | {speed:.3f}× "
                             f"| {ttft:.3f}× ({min(ttft_samples):.3f}–{max(ttft_samples):.3f}) | {tpot:.3f}× | {rates} |")
    return "\n".join(lines) + "\n"


def report_comparison(data, output, plt):
    output.mkdir(parents=True, exist_ok=True)
    (output / "figures").mkdir(exist_ok=True)
    (output / "paired-results.md").write_text(render_paired(data), encoding="utf-8")
    plot_paired(data, output / "figures", plt)
    write_json(output / "paired-summary.json", data)
