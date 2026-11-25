#!/usr/bin/env python3
"""Export result summaries as Markdown tables for the Chinese technical report."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "results" / "processed"
TABLES = ROOT / "report" / "tables"


def number(value: float | None, digits: int = 2) -> str:
    return "—" if value is None else f"{value:.{digits}f}"


def mean_sd(stat: dict | None, digits: int = 2) -> str:
    if not stat:
        return "—"
    mean = number(stat.get("mean"), digits)
    sd = stat.get("sample_stdev")
    return mean if sd is None else f"{mean} ± {number(sd, digits)}"


def export_summary(phase: str) -> None:
    path = PROCESSED / f"{phase}-summary.json"
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    paired = {
        (item["method"], item["concurrency"]): item
        for item in data.get("paired_speedups", data.get("paired_speedups_vs_normal", []))
    }
    lines = [
        "| 方法 | 并发 | 完成轮数 | 输出吞吐 (tokens/s)，均值 ± 样本标准差 | 配对加速比 | 接受长度 | 草稿接受率 (%) | P95 TPOT (ms) | P95 E2EL (ms) |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for group in sorted(data["groups"], key=lambda item: (item["concurrency"], item["method"])):
        speedup = paired.get((group["method"], group["concurrency"]))
        lines.append(
            "| {method} | {c} | {n} | {tps} | {speedup} | {length} | {rate} | {tpot} | {e2el} |".format(
                method=group["method"],
                c=group["concurrency"],
                n=group["output_throughput_tokens_s"]["n"],
                tps=mean_sd(group["output_throughput_tokens_s"]),
                speedup=mean_sd(speedup["paired_speedup"], 3) if speedup else "—",
                length=mean_sd(group.get("acceptance_length"), 3),
                rate=mean_sd(group.get("acceptance_rate_percent")),
                tpot=number(group["pooled_request_tpot_ms"]["p95"]),
                e2el=number(group["pooled_request_e2el_ms"]["p95"]),
            )
        )
    if data.get("best_fixed_by_concurrency"):
        lines += [
            "",
            "### 各并发下平均吞吐最高的固定配置",
            "",
            "| 并发 | 固定方法 | K | 输出吞吐 (tokens/s)，均值 ± 样本标准差 |",
            "|---:|---|---:|---:|",
        ]
        for item in data["best_fixed_by_concurrency"]:
            lines.append(
                f"| {item['concurrency']} | {item['method']} | {item['k']} | "
                f"{mean_sd(item['output_throughput_tokens_s'])} |"
            )
        lines += [
            "",
            "### 与最佳固定配置的配对比较",
            "",
            "每个倍数配对相同种子。固定基线和倍率都来自同一批三轮运行，因此这些结果只描述本次实验。",
            "",
            "| 方法 | 并发 | 最佳固定基线 | 配对加速比 | 平均吞吐之比 |",
            "|---|---:|---|---:|---:|",
        ]
        for item in data.get("paired_speedups_vs_best_fixed", []):
            lines.append(
                f"| {item['method']} | {item['concurrency']} | {item['baseline_method']} | "
                f"{mean_sd(item['paired_speedup'], 3)} | {number(item['ratio_of_mean_output_tps'], 3)} |"
            )
    (TABLES / f"{phase}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def export_k_scan(method: str) -> None:
    path = PROCESSED / f"kscan-r1-{method}-cost-analysis.json"
    if not path.exists():
        return
    data = json.loads(path.read_text(encoding="utf-8"))
    lines = [
        "| 并发 | K | 输出吞吐 (tokens/s) | 平均 TPOT (ms) | 接受长度 | 草稿接受率 (%) | 估算周期耗时 TPOT × A (ms) |",
        "|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for record in sorted(data["records"], key=lambda item: (item["concurrency"], item["k"])):
        lines.append(
            f"| {record['concurrency']} | {record['k']} | {record['output_tps']:.2f} | "
            f"{record['mean_tpot_ms']:.3f} | {record['acceptance_length']:.3f} | "
            f"{record['acceptance_rate_percent']:.2f} | {record['estimated_cycle_ms']:.3f} |"
        )
    lines += [
        "",
        "### 各并发下单轮扫描的最佳固定 K",
        "",
        "| 并发 | 已扫描 K | 最佳固定 K | 最高吞吐 (tokens/s) | 相对参考 K 的加速比 |",
        "|---:|---|---:|---:|---:|",
    ]
    for entry in data["configuration_oracle_by_concurrency"]:
        lines.append(
            f"| {entry['concurrency']} | {entry['available_ks']} | {entry['best_fixed_k']} | "
            f"{entry['best_output_tps']:.2f} | {number(entry.get('configuration_oracle_speedup_over_reference'), 3)} |"
        )
    (TABLES / f"kscan-r1-{method}.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phases", nargs="+", default=["formal-r1", "semantic-r1"])
    args = parser.parse_args()
    TABLES.mkdir(parents=True, exist_ok=True)
    for phase in args.phases:
        export_summary(phase)
    export_k_scan("mtp")
    export_k_scan("dspark")
    print(f"Markdown tables written to {TABLES}")


if __name__ == "__main__":
    main()
