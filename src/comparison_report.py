"""Read and report the paired EAGLE-4 and Suffix benchmarks."""
from __future__ import annotations

import hashlib
from collections import defaultdict
from itertools import product
from math import ceil, isfinite
from pathlib import Path
from statistics import geometric_mean, median

from plot_style import BASELINE, METHOD_STYLES, MUTED, SUFFIX, save_plot
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


def panel(ax, profiles, methods, workload, metric, ranges=False):
    ax.axhline(1, color=BASELINE, linestyle="--", linewidth=1.05)
    ax.grid(axis="y")
    peak = 1.0
    for index, (method, label, (color, marker, style)) in enumerate(methods):
        cells = paired_runs(profiles, method, workload, metric)
        values = list(cells.values())
        centers = [median(cell) for cell in values]
        x = [position + (index - (len(methods) - 1) / 2) * 0.075 for position in range(len(cells))]
        ax.plot(x, centers, color=color, marker=marker, linestyle=style, markeredgecolor="white",
                markeredgewidth=0.7, label=label, zorder=3)
        upper = [max(cell) for cell in values] if ranges else centers
        peak = max(peak, max(upper))
        if ranges:
            ax.vlines(x, [min(cell) for cell in values], upper, color=color, alpha=0.56, linewidth=1.65)
    ax.set_xticks(range(len(cells)), tuple(cells))
    ax.set_xlim(-0.25, len(cells) - 0.75)
    return peak


def decorate(fig, axes, title, caption):
    handles, labels = axes.get_legend_handles_labels()
    fig.suptitle(title, x=0.084, y=0.965, ha="left", fontsize=14, fontweight="semibold")
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, 0.048), ncol=len(labels))
    fig.text(0.084, 0.019, caption, fontsize=10, color=MUTED)


def plot_paired(data, output, plt):
    profiles = data["profiles"]
    methods = [
        (profile, label, METHOD_STYLES[method])
        for method, label in PAIRED_STYLES
        if (profile := profile_for(data, method)) is not None
    ]

    fig, axes = plt.subplots(1, 2, figsize=(7.75, 3.7), sharey=True)
    peaks = []
    for index, (ax, (workload, label)) in enumerate(zip(axes, WORKLOAD_TITLES, strict=True)):
        peaks.append(panel(ax, profiles, methods, workload, "output_throughput", ranges=True))
        ax.set_title(f"({chr(97 + index)})  {label}", loc="left")
        ax.tick_params(axis="x", pad=4)
    axes[0].set_ylim(0, ceil(1.05 * max(peaks)))
    axes[0].set_ylabel("Output throughput / matched Normal")
    fig.supxlabel("Concurrent requests", y=0.145, fontsize=10.5, color=MUTED)
    decorate(
        fig, axes[0], "Speculative decoding speedup by workload",
        "Dots: paired medians. Bars: min–max across 3 seeds. Dashed line: matched Normal.",
    )
    fig.subplots_adjust(left=0.105, right=0.97, bottom=0.265, top=0.815, wspace=0.16)
    save_plot(fig, plt, output, "eagle4-suffix-throughput")

    fig, axes = plt.subplots(2, 2, figsize=(7.75, 5.1), sharex=True, sharey=True)
    metrics = (("p95_ttft_ms", "P95 TTFT"), ("p95_tpot_ms", "P95 TPOT"))
    peaks = []
    for row_index, (row, (workload, label)) in enumerate(zip(axes, WORKLOAD_TITLES, strict=True)):
        for column, (ax, (metric, title)) in enumerate(zip(row, metrics, strict=True)):
            peaks.append(panel(ax, profiles, methods, workload, metric))
            letter = chr(97 + 2 * row_index + column)
            ax.set_title(f"({letter})  {label} · {title}", loc="left", fontsize=11.2)
    axes[0, 0].set_ylim(0, ceil(4.3 * max(peaks)) / 4)
    fig.supylabel("P95 latency / matched Normal", x=0.028, fontsize=10.5, color=MUTED)
    fig.supxlabel("Concurrent requests", y=0.113, fontsize=10.5, color=MUTED)
    decorate(
        fig, axes[0][0], "Speculative decoding tail latency",
        "Median of 3 paired P95 ratios. Values below 1 indicate lower latency.",
    )
    fig.subplots_adjust(left=0.105, right=0.97, bottom=0.205, top=0.835, wspace=0.15, hspace=0.31)
    save_plot(fig, plt, output, "eagle4-suffix-latency")


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
    lines.extend(["", "![配对吞吐倍率](figures/eagle4-suffix-throughput.png)", "",
                  "![配对尾延迟倍率](figures/eagle4-suffix-latency.png)"])
    for workload, title in WORKLOADS:
        lines.extend(["", f"## {title}", "",
                      "| 方法 | 并发 | Normal (tok/s) | 方法 (tok/s) | 配对吞吐倍率 | P95 TTFT 倍率 | P95 TPOT 倍率 | 草稿接受率 |",
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
                acceptance = [run["spec_decode_acceptance_rate"] for run in row["runs"]
                              if run["spec_decode_acceptance_rate"] is not None]
                rates = f"{median(acceptance):.1f}%" if acceptance else "—"
                lines.append(f"| {label} | {c} | {control:.2f} | {tps:.2f} | {speed:.3f}× "
                             f"| {ttft:.3f}× | {tpot:.3f}× | {rates} |")
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
             "| 并发 | Normal (tok/s) | Suffix (tok/s) | 吞吐倍率 | P95 TPOT（ms，Normal / Suffix） | 全文一致 |",
             "|---:|---:|---:|---:|---:|---:|"]
    for concurrency, row in rows:
        center = median(row["paired_speedups"])
        lines.append(f"| {concurrency} | {row['normal_output_tps_median']:.2f} | {row['selected_output_tps_median']:.2f} "
                     f"| {center:.3f}× | {row['normal_p95_tpot_ms_median']:.2f} / {row['selected_p95_tpot_ms_median']:.2f} "
                     f"| {row['exact_text_matches']}/{row['requests_per_configuration']} |")
    lines.extend(["", "![标准 Suffix 的配对吞吐倍率](figures/standard-suffix-throughput.png)", ""])
    (output / "standard-suffix-results.md").write_text("\n".join(lines), encoding="utf-8")

    fig, ax = plt.subplots(figsize=(5.55, 2.85))
    fig.suptitle("Standard Suffix on Spec-Bench", x=0.137, y=0.95, ha="left", fontsize=14, fontweight="semibold")
    ax.axvline(1, color=BASELINE, linestyle="--", linewidth=1.05)
    ax.grid(axis="x")
    for index, (_, row) in enumerate(rows):
        values = row["paired_speedups"]
        ax.hlines(index, min(values), max(values), color=SUFFIX, linewidth=2.4, alpha=0.5)
        ax.scatter(median(values), index, color=SUFFIX, marker="P", zorder=3)
        ax.annotate(f"{median(values):.3f}×", (max(values), index), xytext=(8, 0),
                    textcoords="offset points", va="center")
    values = [value for _, row in rows for value in row["paired_speedups"]]
    span = max(0.4, max(1, max(values)) - min(1, min(values)))
    ax.set_yticks(range(len(rows)), [f"C = {label}" for label, _ in rows])
    ax.set(xlim=(max(0, min(1, min(values)) - 0.15 * span), max(1, max(values)) + 0.37 * span),
           ylim=(len(rows) - 0.55, -0.55), xlabel="Output throughput / matched Normal")
    fig.text(0.137, 0.035, "Dots: paired medians. Bars: min–max across 3 seeds.", fontsize=10, color=MUTED)
    fig.subplots_adjust(left=0.14, right=0.95, top=0.73, bottom=0.27)
    save_plot(fig, plt, output / "figures", "standard-suffix-throughput")


def report_comparison(data, study, output, plt):
    output.mkdir(parents=True, exist_ok=True)
    (output / "figures").mkdir(exist_ok=True)
    if study == "paired":
        (output / "paired-results.md").write_text(render_paired(data), encoding="utf-8")
        plot_paired(data, output / "figures", plt)
    else:
        report_standard(data, output, plt)
    write_json(output / f"{study}-summary.json", data)
