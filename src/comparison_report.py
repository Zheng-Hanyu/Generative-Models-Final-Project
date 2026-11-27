"""Read and report the paired EAGLE-4 and Suffix benchmarks."""
from __future__ import annotations

import hashlib
from collections import defaultdict
from itertools import product
from math import ceil, isfinite
from pathlib import Path
from statistics import geometric_mean, median

from plot_style import BAR_HATCHES, BASELINE, METHOD_STYLES, MUTED, SUFFIX, save_plot, speed_bars
from workloads import cell_name, read_json, write_json

WORKLOADS = (("spec-bench", "Spec-Bench 留出集"), ("repetition", "重复代码与 JSON"))
WORKLOAD_TITLES = (("spec-bench", "Spec-Bench holdout"), ("repetition", "Repetitive code / JSON"))
PAIRED_STYLES = (
    ("eagle4", "EAGLE-4"),
    ("suffix", "Adaptive Suffix"),
    ("dflash", "DFlash 2"),
)
METRICS = ("output_throughput", "p95_ttft_ms", "p95_tpot_ms")
PUBLISHED_DFLASH = "dflash2-mxfp8"


def profile_for(data, method):
    profile = data["winners"].get(method, PUBLISHED_DFLASH if method == "dflash" else None)
    return profile if profile in data["profiles"] else None


def collect_paired(root, config, study):
    spec = config["studies"][study]
    protocol = spec.get("protocol", config["protocol"])
    workloads = ("spec-bench", "repetition") if study == "paired" else ("spec-bench",)
    expected = set(product(workloads, protocol["concurrencies"], protocol["holdout_seeds"]))
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
        if (identity["study"] != study or identity["smoke"] or method not in spec["methods"]
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
        profile = identity["profile"]
        label = profile["id"]
        baseline = f"normal-{method}"
        data["winners"][method] = label
        roles = ("normal", method) if study == "paired" else ("baseline", "selected")
        runs = {}
        for role, key, control in zip(roles, (baseline, label), (None, baseline), strict=True):
            directory = lane / role
            record = read_json(directory / "completed.json")
            if record["profile"]["spec"] != (None if control is None else profile["spec"]):
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
                run_key = (workload, concurrency, seed)
                row = {
                    "seed": seed, "completed": result["completed"], "failed": result["failed"],
                    "test_input_sha256": cell["sha256"], "raw_result_sha256": hashlib.sha256(result_path.read_bytes()).hexdigest(),
                    **{metric: result[metric] for metric in METRICS},
                    "spec_decode_acceptance_rate": result.get("spec_decode_acceptance_rate"),
                }
                if study == "standard-suffix":
                    texts = result["generated_texts"]
                    if len(texts) != cell["count"]:
                        raise ValueError(f"{result_path}: incomplete output text")
                    if control is None:
                        runs[run_key] = texts
                    else:
                        row["exact_text_matches"] = sum(a == b for a, b in zip(runs[run_key], texts, strict=True))
                rows[workload, concurrency].append(row)
            data["profiles"][key] = {"spec": record["profile"]["spec"], "baseline": control, "rows": [
                {"workload": workload, "concurrency": concurrency, "runs": matches}
                for (workload, concurrency), matches in rows.items()
            ]}
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
    save_plot(fig, plt, output, "eagle4-suffix")


def render_paired(data):
    profiles = data["profiles"]
    methods = [(profile_for(data, method), label) for method, label in PAIRED_STYLES]
    methods = [(profile, label) for profile, label in methods if profile is not None]
    lines = ["# EAGLE-4、自适应 Suffix 与 DFlash 2", "",
             "同一档并发先计算各轮相对同构建 Normal 的倍率，再取中位数。综合倍率取各档中位倍率的几何平均。", "",
             "| 方法 | Spec-Bench | 重复代码与 JSON |", "|---|---:|---:|"]
    for profile, label in methods:
        values = [geometric_mean(median(cell) for cell in paired_runs(
            profiles, profile, workload, "output_throughput").values()) for workload, _ in WORKLOADS]
        lines.append(f"| {label} | {values[0]:.3f}× | {values[1]:.3f}× |")
    lines.extend(["", "![配对吞吐、P95 每 token 延迟和草稿接受率](figures/eagle4-suffix.png)", "",
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


def standard_rows(data):
    if "rows" in data:
        return data["rows"]
    profiles = data["profiles"]
    key = data["winners"]["suffix-standard"]
    item = profiles[key]
    baseline = {row["concurrency"]: row["runs"] for row in profiles[item["baseline"]]["rows"]}
    ratios = paired_runs(profiles, key, "spec-bench", "output_throughput")
    return {
        str(row["concurrency"]): {
            "normal_output_tps_median": median(run["output_throughput"] for run in baseline[row["concurrency"]]),
            "selected_output_tps_median": median(run["output_throughput"] for run in row["runs"]),
            "normal_p95_ttft_ms_median": median(run["p95_ttft_ms"] for run in baseline[row["concurrency"]]),
            "selected_p95_ttft_ms_median": median(run["p95_ttft_ms"] for run in row["runs"]),
            "normal_p95_tpot_ms_median": median(run["p95_tpot_ms"] for run in baseline[row["concurrency"]]),
            "selected_p95_tpot_ms_median": median(run["p95_tpot_ms"] for run in row["runs"]),
            "paired_speedups": ratios[row["concurrency"]],
            "exact_text_matches": sum(run["exact_text_matches"] for run in row["runs"]),
            "requests_per_configuration": sum(run["completed"] for run in row["runs"]),
        } for row in item["rows"]
    }


def report_standard(data, output, plt):
    rows = sorted(standard_rows(data).items(), key=lambda row: int(row[0]))
    score = geometric_mean(median(row["paired_speedups"]) for _, row in rows)
    lines = ["# 标准 Suffix", "",
             f"Spec-Bench 留出集的综合吞吐是同卡 Normal 的 **{score:.3f}×**。"
             "每档并发取三轮配对倍率的中位数，再作几何平均。", "",
             "| 并发 | Normal (tok/s) | Suffix (tok/s) | 吞吐倍率 | P95 TTFT（ms） | P95 TPOT（ms） | 全文一致 |",
             "|---:|---:|---:|---:|---:|---:|---:|"]
    for concurrency, row in rows:
        center = median(row["paired_speedups"])
        lines.append(f"| {concurrency} | {row['normal_output_tps_median']:.2f} | {row['selected_output_tps_median']:.2f} "
                     f"| {center:.3f}× | {row['normal_p95_ttft_ms_median']:.2f} → {row['selected_p95_ttft_ms_median']:.2f} "
                     f"| {row['normal_p95_tpot_ms_median']:.2f} → {row['selected_p95_tpot_ms_median']:.2f} "
                     f"| {row['exact_text_matches']}/{row['requests_per_configuration']} |")
    lines.extend(["", "![标准 Suffix 的吞吐与 P95 每 token 延迟](figures/standard-suffix.png)", "",
                  "吞吐须线覆盖各轮最小值和最大值，延迟柱分别取两组 P95 的中位数。", ""])
    (output / "standard-suffix-results.md").write_text("\n".join(lines), encoding="utf-8")

    fig, (speed, delay) = plt.subplots(1, 2, figsize=(7.7, 3.15))
    groups = {"suffix": {concurrency: row["paired_speedups"] for concurrency, row in rows}}
    peak = speed_bars(speed, groups)
    speed.set_title("(a)  Output throughput", loc="left")
    speed.set(ylabel="Throughput / Normal", ylim=(0, ceil(2.35 * peak) / 2))
    for index, (_, row) in enumerate(rows):
        runs = row["paired_speedups"]
        speed.annotate(f"{median(runs):.3f}×", (index, max(runs)), xytext=(0, 5),
                       textcoords="offset points", ha="center", va="bottom", fontsize=8.7)
    delay.set_title("(b)  Time per output token", loc="left")
    delay.grid(axis="y")
    for role, label, color, hatch, offset in (("normal", "Normal", BASELINE, "", -0.16),
                                              ("selected", "Standard Suffix", SUFFIX, BAR_HATCHES["suffix"], 0.16)):
        bars = delay.bar([index + offset for index in range(len(rows))],
                         [row[f"{role}_p95_tpot_ms_median"] for _, row in rows], width=0.29,
                         color=color, edgecolor="white", linewidth=0.5, hatch=hatch, label=label)
        delay.bar_label(bars, fmt="%.2f", padding=3, fontsize=8.7)
    delay.set_ylabel("P95 TPOT (ms)")
    delay.set_xticks(range(len(rows)), [concurrency for concurrency, _ in rows])
    ymax = max(row[key] for _, row in rows for key in ("normal_p95_tpot_ms_median", "selected_p95_tpot_ms_median"))
    delay.set_ylim(0, ymax * 1.23)
    handles, labels = delay.get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.992), ncol=2)
    fig.supxlabel("Concurrent requests", y=0.025)
    fig.subplots_adjust(left=0.104, right=0.98, bottom=0.16, top=0.79, wspace=0.28)
    save_plot(fig, plt, output / "figures", "standard-suffix")


def report_comparison(data, study, output, plt):
    output.mkdir(parents=True, exist_ok=True)
    (output / "figures").mkdir(exist_ok=True)
    if study == "paired":
        (output / "paired-results.md").write_text(render_paired(data), encoding="utf-8")
        plot_paired(data, output / "figures", plt)
    else:
        report_standard(data, output, plt)
    write_json(output / f"{study}-summary.json", data)
