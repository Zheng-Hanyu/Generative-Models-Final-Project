#!/usr/bin/env python3
"""Plot the B200 EAGLE-4 and adaptive Suffix comparison from paired runs."""
from __future__ import annotations

import argparse
import json
from math import ceil
from pathlib import Path
from statistics import median

from plot_style import BASELINE, DFLASH, DSPARK, MTP, MUTED, save_plot, setup_plots

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results/processed/unified-framework/eagle4-suffix-b200.json"
WORKLOADS = (("spec-bench", "Spec-Bench holdout"), ("repetition", "Repetitive code / JSON"))
CONCURRENCIES = (1, 4, 16)


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
    return [cells[count] for count in CONCURRENCIES]


def panel(ax, profiles, methods, workload, metric, ranges=False):
    ax.axhline(1, color=BASELINE, linestyle="--", linewidth=1.05)
    ax.grid(axis="y")
    peak = 1.0
    for index, (method, label, color, marker) in enumerate(methods):
        values = paired_runs(profiles, method, workload, metric)
        centers = [median(cell) for cell in values]
        x = [position + (index - 1) * 0.075 for position in range(len(CONCURRENCIES))]
        ax.plot(x, centers, color=color, marker=marker, label=label)
        upper = [max(cell) for cell in values] if ranges else centers
        peak = max(peak, max(upper))
        if ranges:
            ax.vlines(x, [min(cell) for cell in values], upper, color=color, alpha=0.45, linewidth=1.5)
    ax.set_xticks(range(len(CONCURRENCIES)), CONCURRENCIES)
    ax.set_xlim(-0.25, len(CONCURRENCIES) - 0.75)
    return peak


def decorate(fig, axes, title, caption):
    handles, labels = axes.get_legend_handles_labels()
    fig.suptitle(title, x=0.076, y=0.955, ha="left", fontsize=17, fontweight="semibold")
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, 0.052), ncol=len(labels))
    fig.text(0.076, 0.025, caption, fontsize=9.5, color=MUTED)


def plot(data, output):
    plt = setup_plots()
    profiles = data["profiles"]
    methods = (
        (data["winners"]["eagle4"], "EAGLE-4", MTP, "o"),
        (data["winners"]["suffix"], "Adaptive Suffix", DSPARK, "s"),
        ("dflash2-mxfp8", "DFlash 2", DFLASH, "D"),
    )
    output.mkdir(parents=True, exist_ok=True)

    fig, axes = plt.subplots(1, 2, figsize=(10, 4.45), sharey=True)
    peaks = []
    for ax, (workload, label) in zip(axes, WORKLOADS, strict=True):
        peaks.append(panel(ax, profiles, methods, workload, "output_throughput", ranges=True))
        ax.set_title(label, loc="left")
        ax.set_xlabel("Concurrent requests")
    axes[0].set_ylim(0, ceil(1.05 * max(peaks)))
    axes[0].set_ylabel("Output throughput / matched Normal")
    decorate(
        fig, axes[0], "Speculative decoding speedup by workload",
        "Points show paired medians. Thin bars span three runs. Dashed line marks each method’s matched Normal.",
    )
    fig.subplots_adjust(left=0.082, right=0.97, bottom=0.25, top=0.82, wspace=0.12)
    save_plot(fig, plt, output, "eagle4-suffix-throughput")

    fig, axes = plt.subplots(2, 2, figsize=(10, 6.45), sharex=True, sharey=True)
    metrics = (("p95_ttft_ms", "First token"), ("p95_tpot_ms", "Time per output token"))
    peaks = []
    for row, (workload, label) in zip(axes, WORKLOADS, strict=True):
        for ax, (metric, title) in zip(row, metrics, strict=True):
            peaks.append(panel(ax, profiles, methods, workload, metric))
            ax.set_title(f"{label} · {title}", loc="left", fontsize=10.75)
    axes[0, 0].set_ylim(0, ceil(4.3 * max(peaks)) / 4)
    fig.supylabel("P95 latency / matched Normal", x=0.025, fontsize=10.5, color=MUTED)
    for ax in axes[-1]:
        ax.set_xlabel("Concurrent requests")
    decorate(
        fig, axes[0][0], "Speculative decoding tail latency",
        "Each point is the median of three paired P95 ratios. Values below 1 indicate lower latency.",
    )
    fig.subplots_adjust(left=0.086, right=0.97, bottom=0.20, top=0.83, wspace=0.15, hspace=0.29)
    save_plot(fig, plt, output, "eagle4-suffix-latency")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--results", type=Path, default=RESULTS)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    plot(json.loads(args.results.read_text(encoding="utf-8")), args.output)


if __name__ == "__main__":
    main()
