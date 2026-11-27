"""Summarize a same-input Spec-Bench concurrency sweep."""

from statistics import median

from comparison_report import paired_runs
from plot_style import BASELINE, METHOD_STYLES, save_plot
from workloads import write_json


LABELS = {
    "mtp": "Native MTP", "dspark": "DSpark", "dflash": "DFlash 2",
    "eagle4": "EAGLE-4",
}


def method_cells(data, method):
    profiles = data["profiles"]
    name = data["winners"][method]
    profile = profiles[name]
    selected = {row["concurrency"]: row["runs"] for row in profile["rows"]}
    control = {row["concurrency"]: row["runs"] for row in profiles[profile["baseline"]]["rows"]}
    return name, selected, control


def plot_concurrency(data, figures, plt, filename="concurrency", *, log_scale=True):
    profiles = data["profiles"]
    fig, axes = plt.subplots(2, 2, figsize=(8.2, 5.35), sharex=True)
    titles = ("(a)  Output throughput", "(b)  Throughput gain", "(c)  Time to first token", "(d)  Time per output token")
    ylabels = ("Output throughput (tok/s)", "Throughput / Normal", "P95 TTFT / Normal", "P95 TPOT / Normal")
    metrics = ("output_throughput", "p95_ttft_ms", "p95_tpot_ms")
    concurrencies = data["experiment"]["protocol"]["concurrencies"]
    for method in data["winners"]:
        name, selected, _ = method_cells(data, method)
        values = [[median(run["output_throughput"] for run in selected[c]) for c in concurrencies]]
        for metric in metrics:
            ratios = paired_runs(profiles, name, "spec-bench", metric)
            values.append([median(ratios[c]) for c in concurrencies])
        color, marker, style = METHOD_STYLES[method]
        for ax, series in zip(axes.flat, values, strict=True):
            ax.plot(concurrencies, series, color=color, marker=marker, linestyle=style, label=LABELS[method])
    for index, (ax, title, ylabel) in enumerate(zip(axes.flat, titles, ylabels, strict=True)):
        ax.set_title(title, loc="left")
        if log_scale:
            ax.set_xscale("log", base=2)
        ax.set_ylabel(ylabel)
        ax.grid(axis="y")
        if index:
            ax.axhline(1, color=BASELINE, linestyle="--", linewidth=1.0, zorder=1)
        else:
            ax.set_ylim(bottom=0)
    for ax in axes[-1]:
        ax.set_xticks(concurrencies, [str(c) for c in concurrencies])
    handles, labels = axes[0, 0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.995), ncol=len(labels))
    fig.supxlabel("Concurrent requests (log base 2)" if log_scale else "Concurrent requests", y=0.023)
    fig.subplots_adjust(left=0.112, right=0.98, bottom=0.11, top=0.87, wspace=0.28, hspace=0.34)
    save_plot(fig, plt, figures, filename)


def render_concurrency(data, *, title="Spec-Bench 并发重测", figure_name="concurrency"):
    profiles = data["profiles"]
    experiment = data["experiment"]
    protocol = experiment["protocol"]
    trials = len(protocol["holdout_seeds"])
    concurrencies = protocol["concurrencies"]
    counts = 2 * len(data["winners"]) * len(concurrencies) * trials
    levels = "、".join(map(str, concurrencies))
    seeds = "、".join(map(str, protocol["holdout_seeds"]))
    speedups = {
        method: {c: median(samples) for c, samples in paired_runs(
            profiles, name, "spec-bench", "output_throughput").items()}
        for method, name in data["winners"].items()
    }
    low, high = min(concurrencies), max(concurrencies)
    narrowing = sum(values[high] < values[low] for values in speedups.values())
    run_note = (f"合计 {counts} 组压测、{counts * protocol['holdout_prompts']:,} 条计时请求。"
                "每个方法独立配对同卡、同 vLLM 构建的 Normal。本轮用同一台服务器上的不同 B200 并行压测各方法，客户端版本一致。"
                if figure_name == "concurrency" else
                f"图表所列配置及其 Normal 共 {counts} 组压测、{counts * protocol['holdout_prompts']:,} 条计时请求。"
                "每个方法独立配对同卡、同 vLLM 构建的 Normal。")
    lines = [
        f"# {title}", "",
        f"{experiment['target']} · {experiment['gpu']} · 驱动 {experiment['driver']}", "",
        f"并发 {levels}，种子 {seeds}。每档、每个种子使用 {protocol['holdout_prompts']} 条请求，"
        f"每条最多生成 {protocol['output_tokens']} tokens。每个种子在所有并发档和方法中使用同一组输入，"
        "三个种子的输入互不重叠。种子内打乱档位运行顺序，两组使用同一顺序。", "",
        run_note, "",
        "## 吞吐倍率", "",
        "每个倍率先对同种子、同并发的运行配对，再取各轮中位数。绝对吞吐用于查看各方法随并发的变化，相对 Normal 的倍率用于比较方法。延迟倍率低于 1 表示延迟下降。", "",
        f"从并发 {low} 到 {high}，相对 Normal 的吞吐倍率下降的方法有 {narrowing}/{len(speedups)} 种。", "",
        "| 方法 | " + " | ".join(f"C={c}" for c in concurrencies) + " |",
        "|---|" + "---:|" * len(concurrencies),
    ]
    for method, ratios in speedups.items():
        lines.append(f"| {LABELS[method]} | " + " | ".join(f"{ratios[c]:.3f}×" for c in concurrencies) + " |")
    lines.extend(["", f"![各并发档的绝对吞吐、配对吞吐及尾延迟](figures/{figure_name}.png)", "",
                  "## 逐方法结果", "",
                  "以下绝对吞吐和延迟分别取各组的逐轮中位数。括号内是最小及最大配对吞吐倍率。"])
    for method, lane in experiment["lanes"].items():
        name, selected, control = method_cells(data, method)
        ratios = paired_runs(profiles, name, "spec-bench", "output_throughput")
        lines.extend(["", f"### {LABELS[method]}", "",
                      f"配置 `{name}`，GPU {lane['gpu_index']}，两组服务均使用 vLLM `{lane['server_version']}`。", "",
                      "| 并发 | Normal (tok/s) | 方法 (tok/s) | 配对倍率（范围） | P95 TTFT (ms) | P95 TPOT (ms) | 草稿接受率 |",
                      "|---:|---:|---:|---:|---:|---:|---:|"])
        for c in concurrencies:
            normal, spec = control[c], selected[c]
            values = [f"{median(run['output_throughput'] for run in group):.2f}" for group in (normal, spec)]
            speed = f"{median(ratios[c]):.3f}× ({min(ratios[c]):.3f}–{max(ratios[c]):.3f})"
            delays = [" → ".join(f"{median(run[metric] for run in group):.2f}" for group in (normal, spec))
                      for metric in ("p95_ttft_ms", "p95_tpot_ms")]
            rates = [run["spec_decode_acceptance_rate"] for run in spec if run["spec_decode_acceptance_rate"] is not None]
            acceptance = f"{median(rates):.1f}%" if rates else "—"
            lines.append(f"| {c} | {values[0]} | {values[1]} | {speed} | {delays[0]} | {delays[1]} | {acceptance} |")
    return "\n".join(lines) + "\n"


def report_concurrency(data, output, plt):
    figures = output / "figures"
    figures.mkdir(parents=True, exist_ok=True)
    (output / "concurrency.md").write_text(render_concurrency(data), encoding="utf-8")
    write_json(output / "concurrency-summary.json", data)
    plot_concurrency(data, figures, plt)
