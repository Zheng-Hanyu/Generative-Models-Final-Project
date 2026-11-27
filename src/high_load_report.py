"""Report confirmed serving configurations and the DFlash 2 latency controls."""

from statistics import median

from concurrency_report import LABELS, plot_concurrency, render_concurrency
from workloads import write_json


def selection_lines(selection):
    lines = ["## 调参和独立复测", "",
             "筛选用调参池的两组输入，每组 64 条。独立复测用此前并发重测未使用的 144 条留出输入，分成三轮。"
             "每档先取相对现行配置的配对中位数，再对三档吞吐倍率作等权几何平均。距最快吞吐 3% 以内时，"
             "选并发 32 的 P95 首 token 延迟更低者。最佳挑战者在留出集上与现行配置及 Normal 复测。"
             "每组计时前用四条短请求预热。", "",
             "| 方法 | 完成筛选 / 计划配置 | 发布配置 | 综合吞吐 vs 现行 | C32 P95 TTFT（现行 → 发布，ms） |",
             "|---|---:|---|---:|---:|"]
    for method, row in selection.items():
        lines.append(f"| {LABELS[method]} | {row['screened']}/{row['screened'] + row['failed']} | "
                     f"`{row['winner']}` | {row['winner_throughput_vs_incumbent']:.3f}× | "
                     f"{row['incumbent_c32_ttft_ms']:.2f} → {row['winner_c32_ttft_ms']:.2f} |")
    rejected = [row for row in selection.values() if row["winner"] == row["incumbent"]]
    if rejected:
        lines.extend(["", "留出集保留现行配置的比较如下。", "",
                      "| 方法 | 挑战者综合吞吐 vs 现行 | 挑战者 C32 P95 TTFT (ms) |",
                      "|---|---:|---:|"])
        for method, row in selection.items():
            if row["winner"] == row["incumbent"]:
                lines.append(f"| {LABELS[method]} | {row['challenger_throughput_vs_incumbent']:.3f}× | "
                             f"{row['challenger_c32_ttft_ms']:.2f} |")
    return lines


def diagnosis_lines(diagnosis):
    original = diagnosis["original_c32"]
    lines = ["## DFlash 2 并发 32 首 token 延迟", "",
             f"原并发重测中，DFlash 2 的 P95 TTFT 从 C24 的 {original['dflash_c24_p95_ms']:.2f} ms "
             f"升到 C32 的 {original['dflash_p95_ms']:.2f} ms。C32 的 Normal P95 为 {original['normal_p95_ms']:.2f} ms。"
             f"同档的 P50 从 Normal 的 {original['normal_p50_ms']:.2f} ms 降到 DFlash 2 的 {original['dflash_p50_ms']:.2f} ms。"
             "客户端的并发信号量等待发生在 TTFT 开始计时之前。"
             f"首轮 C32 在 {original['first_c32_jit_warning_utc']} UTC 记录了运行中 CuTeDSL JIT，后两轮的 P95 仍高于配对 Normal。"
             f"三轮首次发出的 32 条请求各有 {min(original['first_wave_prompt_tokens']):,} 至 "
             f"{max(original['first_wave_prompt_tokens']):,} 个输入 token，超过了每个调度步的 4,096 token 预算。", "",
             "专项复测在同一张 B200 上使用原来的三个种子和输入，保持 K=7、MXFP8 及服务构建固定，"
             "分别改变 Normal 和 DFlash 2 的单步 token 预算。服务端阶段耗时是每轮请求均值的三轮中位数，"
             "服务端 prefill 从首次调度计到首次产出 token，包含阶段内的等待。客户端 P95 是每轮百分位数的三轮中位数。", "",
             "| 模式 | 调度 token 预算 | 并发 | 输出 (tok/s) | P50 TTFT (ms) | P95 TTFT (ms) | 服务端排队 (ms) | 服务端 prefill (ms) | 三轮 prefill >300 ms 请求数 |",
             "|---|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for entry in diagnosis["controls"]:
        for concurrency in (24, 32):
            rows = [row for row in entry["runs"] if row["concurrency"] == concurrency]
            values = [median(row[key] for row in rows) for key in (
                "output_throughput", "median_ttft_ms", "p95_ttft_ms", "server_queue_ms", "server_prefill_ms"
            )]
            lines.append(f"| {entry['mode']} | {entry['budget']} | {concurrency} | "
                         + " | ".join(f"{value:.2f}" for value in values)
                         + f" | {sum(row['prefill_over_300ms'] for row in rows)}/192 |")
    lines.extend(["", "在另一个 B200 上，同一 DFlash 2 进程内将每个种子的 C32 压测立即跑第二遍。", "",
                  "| 调度 token 预算 | 种子 | 首次 P95 TTFT (ms) | 立即复测 P95 TTFT (ms) |",
                  "|---:|---:|---:|---:|"])
    for entry in diagnosis["repeat_probe"]:
        for pair in entry["pairs"]:
            lines.append(f"| {entry['budget']} | {pair['seed']} | {pair['first_ttft_ms']:.2f} | {pair['repeat_ttft_ms']:.2f} |")
    if diagnosis.get("interpretation"):
        lines.extend(["", *diagnosis["interpretation"]])
    lines.extend(["", "[vLLM 分块 prefill](https://docs.vllm.ai/en/v0.34.0/configuration/optimization/#chunked-prefill)"
                  " · [调度器源码](https://github.com/vllm-project/vllm/blob/v0.34.0/vllm/v1/core/sched/scheduler.py)"
                  " · [延迟指标定义](https://github.com/vllm-project/vllm/blob/v0.34.0/vllm/v1/metrics/stats.py)"])
    return lines


def report_high_load(data, output, plt):
    figures = output / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    sections = [render_concurrency(data, title="高并发调参留出复测", figure_name="high-load").rstrip()]
    if data.get("selection"):
        sections.append("\n".join(selection_lines(data["selection"])))
    if data.get("diagnosis"):
        sections.append("\n".join(diagnosis_lines(data["diagnosis"])))
    (output / "high-load.md").write_text("\n\n".join(sections) + "\n", encoding="utf-8")
    write_json(output / "high-load-summary.json", data)
    plot_concurrency(data, figures, plt, "high-load", log_scale=False)
