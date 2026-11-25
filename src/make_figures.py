#!/usr/bin/env python3
"""Generate publication-style figures from retained benchmark summaries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "results" / "processed"
FIGURES = ROOT / "report" / "figures"
COLORS = {
    "normal": "#4C78A8",
    "mtp-k3": "#F58518",
    "mtp-k5": "#54A24B",
    "mtp-k6": "#72B7B2",
    "mtp-k7": "#B279A2",
    "mtp-dynamic-oracle": "#E45756",
    "mtp-dynamic-smooth": "#9D755D",
    "dspark-k1": "#4C78A8",
    "dspark-k3": "#54A24B",
    "dspark-k7": "#E45756",
    "dspark-adaptive": "#9D755D",
}
LABELS = {
    "normal": "Normal",
    "mtp-k3": "MTP K=3",
    "mtp-k5": "MTP K=5",
    "mtp-k6": "MTP K=6",
    "mtp-k7": "MTP K=7",
    "mtp-dynamic-oracle": "MTP dynamic Oracle",
    "mtp-dynamic-smooth": "MTP dynamic smooth",
    "dspark-k1": "DSpark K=1",
    "dspark-k3": "DSpark K=3",
    "dspark-k7": "DSpark K=7",
    "dspark-adaptive": "DSpark adaptive",
}


def load_summary(phase: str) -> dict | None:
    path = PROCESSED / f"{phase}-summary.json"
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def group(summary: dict, method: str, concurrency: int) -> dict | None:
    return next(
        (
            item
            for item in summary["groups"]
            if item["method"] == method and item["concurrency"] == concurrency
        ),
        None,
    )


def concurrency_values(summary: dict) -> list[int]:
    return sorted({item["concurrency"] for item in summary["groups"]})


def save(fig: plt.Figure, name: str) -> None:
    fig.savefig(FIGURES / f"{name}.png", dpi=190, bbox_inches="tight")
    fig.savefig(FIGURES / f"{name}.svg", bbox_inches="tight")
    plt.close(fig)


def setup() -> None:
    FIGURES.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update(
        {
            "font.size": 10,
            "axes.titlesize": 11,
            "axes.labelsize": 10,
            "legend.fontsize": 9,
            "figure.dpi": 120,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "axes.grid": True,
            "grid.alpha": 0.25,
        }
    )


def metric_values(
    summary: dict,
    method: str,
    metric: str,
    pooled: bool = False,
    concurrencies: list[int] | None = None,
):
    values = []
    for concurrency in concurrencies or concurrency_values(summary):
        item = group(summary, method, concurrency)
        source = item.get(metric) if item else None
        if pooled:
            values.append(source.get("p95") if source else np.nan)
        else:
            values.append(source.get("mean") if source else np.nan)
    return np.asarray(values, dtype=float)


def finish_single_panel_figure(fig, ax, methods: list[str]) -> None:
    """Place large policy legends outside the plotting area."""
    if len(methods) < 5:
        ax.legend(frameon=False)
    else:
        handles, labels = ax.get_legend_handles_labels()
        fig.legend(handles, labels, frameon=False, loc="center left", bbox_to_anchor=(1.0, 0.5))
    fig.tight_layout()


def plot_throughput(summary: dict, phase: str, methods: list[str]) -> None:
    concurrencies = concurrency_values(summary)
    x = np.arange(len(concurrencies))
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    for method in methods:
        means, errors = [], []
        for concurrency in concurrencies:
            item = group(summary, method, concurrency)
            stat = item["output_throughput_tokens_s"] if item else {}
            means.append(stat.get("mean", np.nan))
            errors.append(stat.get("sample_stdev") or 0.0)
        ax.errorbar(
            x,
            means,
            yerr=errors,
            marker="o",
            linewidth=2,
            capsize=4,
            color=COLORS.get(method),
            label=LABELS.get(method, method),
        )
    ax.set_xticks(x, [str(c) for c in concurrencies])
    ax.set_xlabel("Client concurrency")
    ax.set_ylabel("Output throughput (tokens/s)")
    ax.set_title("Output throughput vs. concurrency (mean ± sample SD, 3 runs)")
    finish_single_panel_figure(fig, ax, methods)
    save(fig, f"{phase}-throughput")


def plot_speedup(
    summary: dict,
    phase: str,
    methods: list[str],
    *,
    source_key: str = "paired_speedups_vs_normal",
    baseline_label: str = "Normal",
    filename_suffix: str = "paired-speedup",
) -> None:
    concurrencies = concurrency_values(summary)
    x = np.arange(len(concurrencies))
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    for method in methods:
        means, errors = [], []
        for concurrency in concurrencies:
            item = next(
                (
                    entry
                    for entry in summary[source_key]
                    if entry["method"] == method and entry["concurrency"] == concurrency
                ),
                None,
            )
            stat = item["paired_speedup"] if item else {}
            means.append(stat.get("mean", np.nan))
            errors.append(stat.get("sample_stdev") or 0.0)
        ax.errorbar(
            x,
            means,
            yerr=errors,
            marker="o",
            linewidth=2,
            capsize=4,
            color=COLORS.get(method),
            label=LABELS.get(method, method),
        )
    ax.axhline(1.0, color="black", linewidth=1, linestyle="--")
    ax.set_xticks(x, [str(c) for c in concurrencies])
    ax.set_xlabel("Client concurrency")
    baseline_text = LABELS.get(baseline_label, baseline_label)
    ax.set_ylabel(f"Paired speedup over {baseline_text}")
    ax.set_title(f"Same-seed paired speedup over {baseline_text} (mean ± sample SD)")
    finish_single_panel_figure(fig, ax, methods)
    save(fig, f"{phase}-{filename_suffix}")


def finish_two_panel_figure(fig, axes, methods: list[str]) -> None:
    """Keep legends for larger policy comparisons clear of the data panels."""
    if len(methods) < 4:
        axes[0].legend(frameon=False)
        fig.tight_layout()
        return
    handles, labels = axes[0].get_legend_handles_labels()
    columns = min(4, len(methods))
    rows = (len(methods) + columns - 1) // columns
    fig.legend(handles, labels, frameon=False, loc="lower center", bbox_to_anchor=(0.5, 0.005), ncol=columns)
    fig.tight_layout(rect=(0, 0.10 + 0.06 * rows, 1, 1))


def plot_acceptance(summary: dict, phase: str, methods: list[str]) -> None:
    concurrencies = concurrency_values(summary)
    x = np.arange(len(concurrencies))
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.1))
    for method in methods:
        color = COLORS.get(method)
        label = LABELS.get(method, method)
        axes[0].plot(x, metric_values(summary, method, "acceptance_length", concurrencies=concurrencies), marker="o", linewidth=2, color=color, label=label)
        axes[1].plot(x, metric_values(summary, method, "acceptance_rate_percent", concurrencies=concurrencies), marker="o", linewidth=2, color=color, label=label)
    for ax in axes:
        ax.set_xticks(x, [str(c) for c in concurrencies])
        ax.set_xlabel("Client concurrency")
    axes[0].set_ylabel("Accepted tokens per engine step")
    axes[0].set_title("Acceptance length")
    axes[1].set_ylabel("Accepted / proposed draft tokens (%)")
    axes[1].set_title("Draft-token acceptance rate")
    finish_two_panel_figure(fig, axes, methods)
    save(fig, f"{phase}-acceptance")


def plot_p95(summary: dict, phase: str, methods: list[str]) -> None:
    concurrencies = concurrency_values(summary)
    x = np.arange(len(concurrencies))
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.1))
    for method in methods:
        color = COLORS.get(method)
        label = LABELS.get(method, method)
        axes[0].plot(x, metric_values(summary, method, "pooled_request_tpot_ms", pooled=True, concurrencies=concurrencies), marker="o", linewidth=2, color=color, label=label)
        axes[1].plot(x, metric_values(summary, method, "pooled_request_e2el_ms", pooled=True, concurrencies=concurrencies), marker="o", linewidth=2, color=color, label=label)
    for ax in axes:
        ax.set_xticks(x, [str(c) for c in concurrencies])
        ax.set_xlabel("Client concurrency")
    axes[0].set_ylabel("P95 request-level TPOT (ms)")
    axes[0].set_title("Pooled request-level TPOT")
    axes[1].set_ylabel("P95 end-to-end latency (ms)")
    axes[1].set_title("Pooled request-level E2EL")
    finish_two_panel_figure(fig, axes, methods)
    save(fig, f"{phase}-p95-latency")


def plot_k_scan(method: str) -> None:
    path = PROCESSED / f"kscan-r1-{method}-cost-analysis.json"
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data["records"]:
        return
    fig, axes = plt.subplots(1, 3, figsize=(14.0, 4.1))
    for concurrency, color in zip([1, 4, 16, 32], ["#4C78A8", "#F58518", "#54A24B", "#E45756"]):
        records = sorted(
            (r for r in data["records"] if r["concurrency"] == concurrency),
            key=lambda r: r["k"],
        )
        ks = [r["k"] for r in records]
        axes[0].plot(ks, [r["output_tps"] for r in records], marker="o", color=color, label=f"C={concurrency}")
        axes[1].plot(ks, [r["acceptance_length"] for r in records], marker="o", color=color, label=f"C={concurrency}")
        axes[2].plot(ks, [r["estimated_cycle_ms"] for r in records], marker="o", color=color, label=f"C={concurrency}")
    axes[0].set_ylabel("Output throughput (tokens/s)")
    axes[1].set_ylabel("Acceptance length")
    axes[2].set_ylabel("TPOT × acceptance length (ms)")
    for ax, title in zip(axes, ["Throughput", "Accepted tokens per step", "Effective cycle cost"]):
        ax.set_xlabel("Number of draft tokens K")
        ax.set_title(title)
        ax.set_xticks(sorted({r["k"] for r in data["records"]}))
    axes[0].legend(frameon=False)
    fig.tight_layout()
    save(fig, f"kscan-r1-{method}-tps-acceptance-cycle")

    max_k = max(r["k"] for r in data["records"])
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    for concurrency, color in zip([1, 4, 16, 32], ["#4C78A8", "#F58518", "#54A24B", "#E45756"]):
        record = next((r for r in data["records"] if r["concurrency"] == concurrency and r["k"] == max_k), None)
        if record is None:
            continue
        rates = record["per_position_unconditional_acceptance"]
        ax.plot(np.arange(1, len(rates) + 1), 100 * np.asarray(rates), marker="o", color=color, label=f"C={concurrency}")
    ax.set_xlabel("Draft position")
    ax.set_ylabel("Unconditional acceptance probability (%)")
    ax.set_title(f"Per-position acceptance from K={max_k} runs")
    ax.legend(frameon=False)
    save(fig, f"kscan-r1-{method}-per-position-acceptance")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-policies", action="store_true")
    args = parser.parse_args()
    setup()
    formal = load_summary("formal-r1")
    if formal:
        methods = ["normal", "mtp-k3", "dspark-k7"]
        plot_throughput(formal, "formal-r1", methods)
        plot_speedup(formal, "formal-r1", methods[1:])
        plot_acceptance(formal, "formal-r1", methods[1:])
        plot_p95(formal, "formal-r1", methods)
    semantic = load_summary("semantic-r1")
    if semantic:
        methods = ["normal", "mtp-k3", "dspark-k7"]
        plot_throughput(semantic, "semantic-r1", methods)
        plot_speedup(semantic, "semantic-r1", methods[1:])
        plot_acceptance(semantic, "semantic-r1", methods[1:])
        plot_p95(semantic, "semantic-r1", methods)
    plot_k_scan("mtp")
    plot_k_scan("dspark")
    if args.include_policies:
        policy_specs = [
            (
                "policy-mtp-fixed-r1",
                ["normal", "mtp-k3", "mtp-k5", "mtp-k6", "mtp-k7"],
                "normal",
            ),
            (
                "policy-mtp-r1",
                [
                    "normal",
                    "mtp-k3",
                    "mtp-k5",
                    "mtp-k6",
                    "mtp-k7",
                    "mtp-dynamic-oracle",
                    "mtp-dynamic-smooth",
                ],
                "normal",
            ),
            ("policy-dspark-r1", ["dspark-k7", "dspark-adaptive"], "dspark-k7"),
            (
                "policy-dspark-high-r1",
                ["dspark-k1", "dspark-k3", "dspark-k7", "dspark-adaptive"],
                "dspark-k7",
            ),
            (
                "semantic-r1-dspark-adaptive",
                ["dspark-k7", "dspark-adaptive"],
                "dspark-k7",
            ),
            (
                "semantic-r1-dspark-high",
                ["dspark-k1", "dspark-k3", "dspark-k7", "dspark-adaptive"],
                "dspark-k7",
            ),
        ]
        for phase, methods, baseline in policy_specs:
            summary = load_summary(phase)
            if not summary or summary.get("status") != "complete":
                continue
            present = [m for m in methods if any(g["method"] == m for g in summary["groups"])]
            plot_throughput(summary, phase, present)
            candidates = [m for m in present if m != baseline]
            if baseline == "normal":
                plot_speedup(summary, phase, candidates)
            else:
                plot_speedup(
                    summary,
                    phase,
                    candidates,
                    source_key="paired_speedups",
                    baseline_label=baseline,
                    filename_suffix=f"paired-speedup-vs-{baseline}",
                )
            if summary.get("paired_speedups_vs_best_fixed"):
                plot_speedup(
                    summary,
                    phase,
                    [m for m in present if m != "normal"],
                    source_key="paired_speedups_vs_best_fixed",
                    baseline_label="best fixed K",
                    filename_suffix="paired-speedup-vs-best-fixed",
                )
            plot_acceptance(summary, phase, [m for m in present if m != "normal"])
            plot_p95(summary, phase, present)
    print(f"Figures written to {FIGURES}")


if __name__ == "__main__":
    main()
