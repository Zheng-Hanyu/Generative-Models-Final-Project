#!/usr/bin/env python3
"""Generate publication-style figures from retained benchmark summaries."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from plot_style import BASELINE, DFLASH, DSPARK, MTP, PLUM, save_plot, setup_plots


plt = setup_plots()
ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "results" / "processed"
FIGURES = ROOT / "report" / "course_study" / "figures"
STYLES = {
    "normal": (BASELINE, "o", "--"),
    "mtp-k3": (MTP, "o", "-"),
    "mtp-k5": (DSPARK, "s", "-"),
    "mtp-k6": (DFLASH, "^", "-"),
    "mtp-k7": (PLUM, "D", "-"),
    "mtp-dynamic-oracle": ("#94365D", "P", "--"),
    "mtp-dynamic-smooth": ("#17637C", "X", "--"),
    "dspark-k1": (MTP, "s", "-"),
    "dspark-k3": (DFLASH, "^", "-"),
    "dspark-k7": (DSPARK, "o", "-"),
    "dspark-adaptive": (PLUM, "D", "--"),
}
CONCURRENCY_STYLES = dict(zip((1, 4, 16, 32), ((MTP, "o"), (DSPARK, "s"), (DFLASH, "^"), (PLUM, "D"))))
PHASE_TITLES = {
    "formal-r1": "Random requests",
    "semantic-r1": "Spec-Bench",
    "policy-mtp-fixed-r1": "MTP fixed lengths on random requests",
    "policy-mtp-r1": "MTP schedules on random requests",
    "policy-dspark-r1": "DSpark on random requests",
    "policy-dspark-high-r1": "DSpark on random requests at high concurrency",
    "semantic-r1-dspark-adaptive": "DSpark on Spec-Bench",
    "semantic-r1-dspark-high": "DSpark on Spec-Bench at high concurrency",
}
LABELS = {
    "normal": "Normal",
    "mtp-k3": "MTP K=3",
    "mtp-k5": "MTP K=5",
    "mtp-k6": "MTP K=6",
    "mtp-k7": "MTP K=7",
    "mtp-dynamic-oracle": "MTP dynamic oracle",
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


def series_style(method):
    color, marker, line = STYLES[method]
    return {"color": color, "marker": marker, "linestyle": line, "label": LABELS[method]}


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


def finish_figure(fig, axes, title, note=None):
    from matplotlib.ticker import StrMethodFormatter

    for ax in axes:
        ax.grid(axis="y")
        if max(abs(value) for value in ax.get_ylim()) >= 1000:
            ax.yaxis.set_major_formatter(StrMethodFormatter("{x:,.0f}"))
    handles, labels = axes[0].get_legend_handles_labels()
    columns = min(4, len(labels))
    rows = (len(labels) + columns - 1) // columns
    if note:
        fig.text(0.055, 0.025, note, color=BASELINE, fontsize=9.5)
    legend_y = 0.085 if note else 0.015
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.5, legend_y), ncol=columns)
    fig.suptitle(title, x=0.055, ha="left", fontsize=16, fontweight="semibold")
    fig.tight_layout(rect=(0, legend_y + 0.065 * rows, 1, 0.89))


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
            capsize=3,
            **series_style(method),
        )
    ax.set_xticks(x, [str(c) for c in concurrencies])
    ax.set_xlabel("Client concurrency")
    ax.set_ylabel("Output throughput (tokens/s)")
    finish_figure(fig, [ax], PHASE_TITLES[phase], "Output throughput is the mean ± sample SD across three runs.")
    save_plot(fig, plt, FIGURES, f"{phase}-throughput")


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
            capsize=3,
            **series_style(method),
        )
    ax.axhline(1.0, color=BASELINE, linewidth=1, linestyle="--")
    ax.set_xticks(x, [str(c) for c in concurrencies])
    ax.set_xlabel("Client concurrency")
    baseline_text = LABELS.get(baseline_label, baseline_label)
    ax.set_ylabel(f"Throughput / {baseline_text}")
    finish_figure(fig, [ax], PHASE_TITLES[phase], "Ratios pair matching seeds. Error bars show sample SD.")
    save_plot(fig, plt, FIGURES, f"{phase}-{filename_suffix}")


def plot_acceptance(summary: dict, phase: str, methods: list[str]) -> None:
    concurrencies = concurrency_values(summary)
    x = np.arange(len(concurrencies))
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.1))
    for method in methods:
        axes[0].plot(x, metric_values(summary, method, "acceptance_length", concurrencies=concurrencies), **series_style(method))
        axes[1].plot(x, metric_values(summary, method, "acceptance_rate_percent", concurrencies=concurrencies), **series_style(method))
    for ax in axes:
        ax.set_xticks(x, [str(c) for c in concurrencies])
        ax.set_xlabel("Client concurrency")
    axes[0].set_ylabel("Tokens advanced per step")
    axes[0].set_title("Acceptance length")
    axes[1].set_ylabel("Accepted draft tokens (%)")
    axes[1].set_title("Draft-token acceptance rate")
    finish_figure(fig, axes, PHASE_TITLES[phase])
    save_plot(fig, plt, FIGURES, f"{phase}-acceptance")


def plot_p95(summary: dict, phase: str, methods: list[str]) -> None:
    concurrencies = concurrency_values(summary)
    x = np.arange(len(concurrencies))
    fig, axes = plt.subplots(1, 2, figsize=(10.5, 4.1))
    for method in methods:
        axes[0].plot(x, metric_values(summary, method, "pooled_request_tpot_ms", pooled=True, concurrencies=concurrencies), **series_style(method))
        axes[1].plot(x, metric_values(summary, method, "pooled_request_e2el_ms", pooled=True, concurrencies=concurrencies), **series_style(method))
    for ax in axes:
        ax.set_xticks(x, [str(c) for c in concurrencies])
        ax.set_xlabel("Client concurrency")
    axes[0].set_ylabel("P95 latency (ms)")
    axes[0].set_title("Time per output token")
    axes[1].set_ylabel("P95 latency (ms)")
    axes[1].set_title("End-to-end latency")
    finish_figure(fig, axes, PHASE_TITLES[phase], "P95 uses pooled requests from all three runs.")
    save_plot(fig, plt, FIGURES, f"{phase}-p95-latency")


def plot_k_scan(method: str) -> None:
    path = PROCESSED / f"kscan-r1-{method}-cost-analysis.json"
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    if not data["records"]:
        return
    fig, axes = plt.subplots(1, 3, figsize=(14.0, 4.1))
    for concurrency, (color, marker) in CONCURRENCY_STYLES.items():
        records = sorted(
            (r for r in data["records"] if r["concurrency"] == concurrency),
            key=lambda r: r["k"],
        )
        ks = [r["k"] for r in records]
        style = {"color": color, "marker": marker, "label": f"Concurrency {concurrency}"}
        axes[0].plot(ks, [r["output_tps"] for r in records], **style)
        axes[1].plot(ks, [r["acceptance_length"] for r in records], **style)
        axes[2].plot(ks, [r["estimated_cycle_ms"] for r in records], **style)
    axes[0].set_ylabel("Output throughput (tokens/s)")
    axes[1].set_ylabel("Acceptance length")
    axes[2].set_ylabel("TPOT × acceptance length (ms)")
    for ax, title in zip(axes, ["Throughput", "Acceptance length", "Estimated cycle time"]):
        ax.set_xlabel("Draft tokens (K)")
        ax.set_title(title)
        ax.set_xticks(sorted({r["k"] for r in data["records"]}))
    method_name = "MTP" if method == "mtp" else "DSpark"
    finish_figure(fig, axes, f"{method_name} draft-length sweep")
    save_plot(fig, plt, FIGURES, f"kscan-r1-{method}-tps-acceptance-cycle")

    max_k = max(r["k"] for r in data["records"])
    fig, ax = plt.subplots(figsize=(7.0, 4.2))
    for concurrency, (color, marker) in CONCURRENCY_STYLES.items():
        record = next((r for r in data["records"] if r["concurrency"] == concurrency and r["k"] == max_k), None)
        if record is None:
            continue
        rates = record["per_position_unconditional_acceptance"]
        ax.plot(np.arange(1, len(rates) + 1), 100 * np.asarray(rates), marker=marker, color=color, label=f"Concurrency {concurrency}")
    ax.set_xlabel("Draft position")
    ax.set_ylabel("Unconditional acceptance probability (%)")
    ax.set_xticks(range(1, max_k + 1))
    finish_figure(fig, [ax], f"{method_name} acceptance by draft position (K={max_k})")
    save_plot(fig, plt, FIGURES, f"kscan-r1-{method}-per-position-acceptance")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--include-policies", action="store_true")
    args = parser.parse_args()
    FIGURES.mkdir(parents=True, exist_ok=True)
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
