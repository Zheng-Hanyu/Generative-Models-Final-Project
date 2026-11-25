"""Validate paired measurements and render the unified framework's figures."""

from __future__ import annotations

from math import isclose
from pathlib import Path
from statistics import geometric_mean, median

from plot_style import BASELINE, DFLASH, DSPARK, INK, MTP, MUTED, save_plot, setup_plots
from unified_framework import CONFIG, cell_name, read_json, stress_cells, write_json


LABELS = {"mtp": "Native MTP", "dspark": "DSpark", "dflash": "DFlash 2", "suffix": "Suffix"}
COLORS = {"mtp": MTP, "dspark": DSPARK, "dflash": DFLASH, "suffix": DFLASH}
MARKERS = {"mtp": "o", "dspark": "s", "dflash": "^", "suffix": "^"}
EXTERNAL = {"speed": ("NVIDIA SPEED-Bench", "speed-bench-throughput"),
            "burst": ("BurstGPT v2.0", "burstgpt-throughput")}
METRICS = ("output_throughput", "p95_ttft_ms", "p95_tpot_ms", "spec_decode_acceptance_rate")
SCHEMA = 2


def retained_role(info):
    return "selected" if info["recommended"]["id"] == info["selection"]["selected"]["id"] else "reference"


def paired_ratios(cell, metric, role):
    return [row[role][metric] / row["normal"][metric] for row in cell["runs"]]


def graph_capture(path):
    log = path.read_text(encoding="utf-8", errors="replace")
    if "Capturing CUDA graphs (FULL)" in log:
        return "full"
    if "setting cudagraph_mode=NONE" in log:
        return "disabled"
    return "unconfirmed"


def load_run(directory, name, count, concurrency, speeds):
    row = read_json(directory / f"{name}.json")
    if (row["completed"] != count or row["failed"] != 0 or row["max_concurrency"] != concurrency
            or len(row["input_lens"]) != count or len(row["output_lens"]) != count
            or row["output_throughput"] != speeds[name]):
        raise ValueError(f"{directory}/{name}: incomplete or inconsistent benchmark")
    return row


def load_runs(lane, profile, phase, concurrency, seeds, count, manifest, stress):
    directory = lane / "holdout" / profile
    completed = read_json(directory / "completed.json")["speeds"]
    rows = []
    for seed in seeds:
        name = cell_name(phase, concurrency, seed)
        row = load_run(directory, name, count, concurrency, completed)
        if phase == "holdout" and name not in manifest:
            raise ValueError(f"{lane}: missing workload signature for {name}")
        if phase == "stress" and (row["input_lens"] != [stress["input_tokens"]] * count
                                  or row["output_lens"] != [stress["output_tokens"]] * count):
            raise ValueError(f"{profile}/{name}: stress token lengths differ from the protocol")
        rows.append(row)
    return rows


def summarize_cells(runs, seeds):
    rows = []
    for seed, *measurements in zip(seeds, *runs.values(), strict=True):
        normal = measurements[0]
        if any(row["input_lens"] != normal["input_lens"] for row in measurements[1:]):
            raise ValueError("Paired benchmarks used different input lengths")
        rows.append({
            "seed": seed,
            **{role: {key: row.get(key) for key in METRICS} | {
                "completed": row["completed"], "failed": row["failed"], "duration_seconds": row["duration"],
                "total_output_tokens": row["total_output_tokens"],
                **({"dispatch_span_seconds": row["dispatch_span_seconds"]} if "dispatch_span_seconds" in row else {}),
            } for role, row in zip(runs, measurements, strict=True)},
        })

    summary = {
        "runs": rows,
        "median_tps": {role: median(row[role]["output_throughput"] for row in rows) for role in runs},
        "median_p95_ttft_ms": {role: median(row[role]["p95_ttft_ms"] for row in rows) for role in runs},
        "median_p95_tpot_ms": {role: median(row[role]["p95_tpot_ms"] for row in rows) for role in runs},
        "successful": {role: sum(row[role]["completed"] for row in rows) for role in runs},
        "failed": {role: sum(row[role]["failed"] for row in rows) for role in runs},
    }
    summary["to_normal"] = paired_ratios(summary, "output_throughput", "selected")
    if "reference" in runs:
        summary["to_reference"] = [row["selected"]["output_throughput"] / row["reference"]["output_throughput"] for row in rows]
    return summary


def summarize_tuning(lane, selection, protocol):
    seed = protocol["tuning_seed"]
    count = protocol["tuning_prompts"]
    for key in ("round1", "round2"):
        for candidate in selection[key]:
            if "score" not in candidate:
                continue
            profile = candidate["profile"]["id"]
            location = lane / "tuning" / profile
            speeds = read_json(location / "completed.json")["speeds"]
            tuning = {}
            for concurrency in protocol["concurrencies"]:
                name = cell_name("tuning", concurrency, seed)
                row = read_json(location / f"{name}.json")
                if row["completed"] != count or row["failed"] or row["output_throughput"] != speeds[name]:
                    raise ValueError(f"{location}/{name}: incomplete tuning benchmark")
                tuning[str(concurrency)] = speeds[name]
            candidate["tps"] = tuning
            candidate["cuda_graph"] = graph_capture(location / "server.log")
            if not isclose(candidate["score"], geometric_mean(tuning.values()), rel_tol=1e-12):
                raise ValueError(f"{location}: tuning score differs from the saved measurements")


def collect(root, profiles=None):
    profiles = read_json(CONFIG)["methods"] if profiles is None else profiles
    methods = {}
    workload_identity = None
    environment_identity = None
    stress_enabled = None
    for method in (method for method in profiles if method != "normal"):
        lane = root / method
        experiment = read_json(lane / "experiment.json")
        protocol = experiment["protocol"]
        manifest = read_json(lane / "workloads.json")
        signature = (protocol, experiment["dataset_sha256"], manifest)
        hardware = (Path(experiment["target"]).name, experiment["vllm_version"],
                    experiment["gpu"]["name"], experiment["gpu"]["driver_version"])
        if experiment["method"] != method or (workload_identity is not None and workload_identity != signature):
            raise ValueError(f"{lane}: experiment inputs differ from the other methods")
        if environment_identity is not None and environment_identity != hardware:
            raise ValueError(f"{lane}: model, vLLM or GPU environment differs")
        workload_identity, environment_identity = signature, hardware
        selection_path = lane / "selection.json"
        if selection_path.exists():
            selection = read_json(selection_path)
        else:
            profile = experiment["method_config"]["reference"]
            selection = {"method": method, "reference": profile, "selected": profile, "round1": [], "round2": []}
        confirmation = read_json(lane / "confirmation.json")
        if stress_enabled is not None and stress_enabled != confirmation["stress"]:
            raise ValueError("Run random stress for every lane or skip it for every lane")
        stress_enabled = confirmation["stress"]
        if (selection["method"] != method or selection["selected"]["id"] != confirmation["selected"]
                or selection["reference"]["id"] != confirmation["reference"]):
            raise ValueError(f"{lane}: confirmation did not use the selected and reference profiles")
        summarize_tuning(lane, selection, protocol)
        info = {
            "selection": selection,
            "gpu_index": experiment["gpu"]["index"],
            "graph_capture": {role: graph_capture(lane / "holdout" / confirmation[role] / "server.log")
                              for role in ("normal", "reference", "selected")},
            "holdout": {}, "stress": {},
        }
        cells = [("holdout", concurrency, protocol["holdout_seeds"], protocol["holdout_prompts"])
                 for concurrency in protocol["concurrencies"]]
        if confirmation["stress"]:
            cells.extend(("stress", concurrency, [seed], protocol["stress"]["prompts"])
                         for concurrency, seed in stress_cells(protocol))
        for phase, concurrency, seeds, count in cells:
            runs = {role: load_runs(lane, confirmation[role], phase, concurrency, seeds, count, manifest, protocol["stress"])
                    for role in ("normal", "reference", "selected")}
            info[phase][str(concurrency)] = summarize_cells(runs, seeds)

        info["score_vs_normal"] = geometric_mean(median(row["to_normal"]) for row in info["holdout"].values())
        info["score_vs_reference"] = geometric_mean(median(row["to_reference"]) for row in info["holdout"].values())
        info["recommended"] = selection["selected" if info["score_vs_reference"] > 1 else "reference"]
        role = retained_role(info)
        info["retained_score_vs_normal"] = geometric_mean(
            median(paired_ratios(row, "output_throughput", role)) for row in info["holdout"].values()
        )
        for key in ("reference", "selected"):
            selection[key] = {"id": selection[key]["id"]}
        for key in ("round1", "round2"):
            for candidate in selection[key]:
                candidate["profile"] = {"id": candidate["profile"]["id"]}
        methods[method] = info

    protocol, data_sha256, workloads = workload_identity
    model, vllm, gpu, driver = environment_identity
    run_counts = {"tuning": 0, "holdout": 0, "stress": 0}
    for info in methods.values():
        selection = info["selection"]
        profiles = 2 + int(selection["reference"]["id"] != selection["selected"]["id"])
        run_counts["tuning"] += sum(len(row.get("tps", {})) for key in ("round1", "round2") for row in selection[key])
        for phase in ("holdout", "stress"):
            run_counts[phase] += profiles * sum(len(row["runs"]) for row in info[phase].values())
    return {
        "schema": SCHEMA, "model": model, "vllm": vllm, "gpu": gpu, "driver": driver,
        "protocol": protocol, "data_sha256": data_sha256, "workloads": workloads,
        "methods": methods, "benchmark_counts": run_counts,
    }


def collect_external(root, summary):
    results = {}
    common_manifest = None
    for method, details in summary["methods"].items():
        lane = root / method
        identity = read_json(lane / "experiment.json")
        confirmation = read_json(lane / "confirmation.json")
        manifest = identity["external_workloads"]
        if common_manifest is not None and common_manifest != manifest:
            raise ValueError("External benchmark workloads differ across methods")
        common_manifest = manifest
        if (identity["method"] != method or identity["method_config"]["reference"] != details["recommended"]
                or confirmation["selected"] != details["recommended"]["id"] or confirmation["normal"] != "normal"
                or Path(identity["target"]).name != summary["model"] or identity["vllm_version"] != summary["vllm"]
                or identity["gpu"]["name"] != summary["gpu"] or identity["gpu"]["driver_version"] != summary["driver"]):
            raise ValueError(f"{lane}: external benchmark environment or profile does not match the report")
        cells = {}
        for cell in manifest["cells"]:
            workload, concurrency = cell["workload"], cell["concurrency"]
            cells.setdefault((workload, concurrency), []).append(cell)
        if set(cells) != {("speed", 1), ("speed", 16), ("burst", 16)}:
            raise ValueError("Incomplete external benchmark matrix")
        results[method] = {"speed": {}, "burst": {}}
        for (workload, concurrency), group in cells.items():
            seeds = [cell["seed"] for cell in group]
            if len(set(seeds)) != 3 or len(seeds) != 3:
                raise ValueError("External workload requires three independent trials")
            runs = {role: [] for role in ("normal", "selected")}
            for role, rows in runs.items():
                directory = lane / "external" / confirmation[role]
                speeds = read_json(directory / "completed.json")["speeds"]
                for cell in group:
                    name = cell_name(workload, concurrency, cell["seed"])
                    row = load_run(directory, name, cell["count"], concurrency, speeds)
                    if workload == "burst":
                        row["dispatch_span_seconds"] = max(row["start_times"]) - min(row["start_times"])
                    rows.append(row)
            if any(a["output_lens"] != b["output_lens"] for a, b in zip(*runs.values(), strict=True)):
                raise ValueError(f"{workload}: paired output budgets differ")
            results[method][workload][str(concurrency)] = summarize_cells(runs, seeds)
    return {"manifest": common_manifest, "methods": results, "benchmark_count": len(common_manifest["cells"]) * 2 * len(results)}


def phase_rows(summary, phase):
    if phase in EXTERNAL:
        return {method: (info[phase], "selected") for method, info in summary["external"]["methods"].items()}
    return {method: (info[phase], retained_role(info)) for method, info in summary["methods"].items()}


def speed_plot(summary, output, plt, phase):
    groups = phase_rows(summary, phase)
    cells = list(next(iter(groups.values()))[0])
    if not cells:
        return
    fig, axes = plt.subplots(1, len(cells), figsize=(max(4.2, 3.45 * len(cells)), 3.45),
                             sharex=True, sharey=True, squeeze=False)
    positions = range(len(groups))
    stress = summary["protocol"]["stress"]
    titles = {
        "holdout": ("Spec-Bench held-out throughput", "spec-bench-throughput"),
        "stress": (f"Synthetic stress test ({stress['input_tokens']:,} input, {stress['output_tokens']:,} output tokens)", "random-stress"),
        "speed": ("SPEED-Bench throughput", EXTERNAL["speed"][1]),
        "burst": ("BurstGPT v2.0 trace replay", EXTERNAL["burst"][1]),
    }
    title, filename = titles[phase]
    fig.suptitle(title, x=0.05, ha="left", fontsize=16, fontweight="semibold")
    ratios = {method: {c: paired_ratios(rows[c], "output_throughput", role) for c in cells}
              for method, (rows, role) in groups.items()}
    limits = [value for method in groups for concurrency in cells for value in ratios[method][concurrency]]
    low, high = min(min(limits), 1), max(max(limits), 1)
    span = max(high - low, 0.65)
    axes[0][0].set_xlim(max(0, low - 0.15 * span), high + 0.27 * span)
    for index, (ax, concurrency) in enumerate(zip(axes[0], cells, strict=True)):
        ax.set_title(f"Concurrency {concurrency}", loc="left")
        ax.axvline(1, color=BASELINE, lw=1.1, ls="--")
        ax.grid(axis="x")
        for position, method in enumerate(groups):
            values = ratios[method][concurrency]
            center = median(values)
            ax.hlines(position, min(values), max(values), color=COLORS[method], lw=3, alpha=0.55)
            ax.scatter(center, position, s=54, color=COLORS[method], marker=MARKERS[method], zorder=3)
            ax.annotate(f"{center:.2f}×", (max(values), position), xytext=(7, 0),
                        textcoords="offset points", va="center", fontsize=9)
        ax.set_yticks(list(positions), [LABELS[method] for method in groups])
        ax.set_ylim(len(groups) - 0.55, -0.55)
        ax.set_xlabel("Throughput / same-GPU Normal")
        if index:
            ax.tick_params(axis="y", length=0, labelleft=False)
    if phase == "stress":
        caption = "One run per point. The dashed line marks Normal."
    else:
        caption = "Markers show paired medians. Bars span the three observed runs."
    fig.text(0.05, 0.018, caption, fontsize=9.5, color=MUTED)
    fig.tight_layout(rect=(0, 0.08, 1, 0.94))
    save_plot(fig, plt, output, filename)


def latency_plot(summary, output, plt):
    cells = list(next(iter(summary["methods"].values()))["holdout"])
    fig, axes = plt.subplots(1, 2, figsize=(10.2, 4.25), sharey=True)
    fig.suptitle("Spec-Bench tail latency", x=0.06, ha="left", fontsize=16, fontweight="semibold")
    for ax, metric, title in zip(axes, ("p95_ttft_ms", "p95_tpot_ms"),
                                 ("Time to first token", "Time per output token"), strict=True):
        ax.axhline(1, color=BASELINE, lw=1.1, ls="--")
        ax.grid(axis="y")
        for method, info in summary["methods"].items():
            ratios = [median(paired_ratios(info["holdout"][c], metric, retained_role(info))) for c in cells]
            ax.plot(range(len(cells)), ratios, color=COLORS[method], marker=MARKERS[method], label=LABELS[method])
        ax.set_title(title, loc="left")
        ax.set_xticks(range(len(cells)), cells)
        ax.set_xlabel("Concurrency")
    axes[0].set_ylabel("P95 latency / same-GPU Normal")
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="lower center", bbox_to_anchor=(0.53, 0.015), ncol=3, frameon=False)
    fig.tight_layout(rect=(0, 0.10, 1, 0.94))
    save_plot(fig, plt, output, "spec-bench-latency")


def workflow_plot(output, plt):
    from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

    fig, ax = plt.subplots(figsize=(10.2, 2.9))
    ax.set(xlim=(0, 10), ylim=(0, 3))
    ax.axis("off")
    cards = [
        (0.12, 1.17, "Profiles", "Method settings"),
        (2.58, 2.12, "Tune", "Spec-Bench tuning split"),
        (2.58, 0.22, "Serve", "Run vLLM separately"),
        (5.04, 1.17, "Benchmark", "Three public workloads"),
        (7.50, 1.17, "Report", "Tables and figures"),
    ]
    for x, y, name, line in cards:
        ax.add_patch(FancyBboxPatch((x, y), 2.30, 0.78, boxstyle="round,pad=0.025,rounding_size=0.09",
                                   facecolor="#F1F5F9", edgecolor="#CFDCE8"))
        ax.text(x + 0.17, y + 0.50, name, color=INK, fontsize=14, fontweight="semibold", va="center")
        ax.text(x + 0.17, y + 0.24, line, color=MUTED, fontsize=9.5, va="center")
    for start, end in (
        ((2.42, 1.70), (2.59, 2.30)),
        ((2.42, 1.44), (2.59, 0.77)),
        ((2.42, 1.56), (5.05, 1.56)),
        ((4.88, 2.31), (5.05, 1.70)),
        ((7.34, 1.56), (7.51, 1.56)),
    ):
        ax.add_patch(FancyArrowPatch(start, end, arrowstyle="-|>", mutation_scale=11, color=BASELINE))
    fig.subplots_adjust(left=0.005, right=0.995, bottom=0.01, top=0.99)
    save_plot(fig, plt, output, "workflow")


def performance_table(summary, phase):
    lines = [
        "| 方法 | 并发 | Normal TPS | 方法 TPS | 配对倍率 | P95 TTFT（ms）Normal → 方法 | P95 TPOT（ms）Normal → 方法 | 成功（Normal → 方法） | 草稿接受率 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for method, (cells, role) in phase_rows(summary, phase).items():
        for concurrency, row in cells.items():
            tps, ttft, tpot = (row[key] for key in ("median_tps", "median_p95_ttft_ms", "median_p95_tpot_ms"))
            ratios = paired_ratios(row, "output_throughput", role)
            acceptance = [run[role]["spec_decode_acceptance_rate"] for run in row["runs"]
                          if run[role]["spec_decode_acceptance_rate"] is not None]
            ratio = f"{median(ratios):.3f}×"
            success = " → ".join(f"{row['successful'][key]}/{row['successful'][key] + row['failed'][key]}"
                                 for key in ("normal", role))
            acceptance_cell = f"{median(acceptance):.1f}%" if acceptance else "—"
            lines.append(f"| {LABELS[method]} | {concurrency} | {tps['normal']:.2f} | {tps[role]:.2f} | {ratio} | "
                         f"{ttft['normal']:.2f} → {ttft[role]:.2f} | {tpot['normal']:.2f} → {tpot[role]:.2f} | "
                         f"{success} | {acceptance_cell} |")
    return lines


def render_tables(summary):
    lines = [
        "# 统一框架实测结果", "",
        f"{summary['model']} · {summary['gpu']} · vLLM {summary['vllm']} · 主模型使用 Triton Attention", "",
        "| 方法 | 原配置 | 调参入选 | 入选相对原配置 | 最终配置 | 最终相对 Normal |",
        "|---|---|---|---:|---|---:|",
    ]
    for method, info in summary["methods"].items():
        reference, selected = (info["selection"][key]["id"] for key in ("reference", "selected"))
        lines.append(f"| {LABELS[method]} | `{reference}` | `{selected}` | {info['score_vs_reference']:.3f}× | "
                     f"`{info['recommended']['id']}` | {info['retained_score_vs_normal']:.3f}× |")
    lines.extend(["", "综合倍数取 Spec-Bench 三档并发的配对中位倍率，再作几何平均。各负载的结果使用每种方法的发布配置。", "",
                  "TPS、P95 TTFT、P95 TPOT 和草稿接受率均为各轮中位数。每个吞吐倍率配对同卡、同种子和同并发的运行，再取各轮中位数。", "",
                  "## Spec-Bench 留出集", "", *performance_table(summary, "holdout"), "",
                  "![Spec-Bench 吞吐](spec-bench-throughput.png)", "",
                  "![Spec-Bench 延迟](spec-bench-latency.png)", ""])
    if "external" in summary:
        for phase, (label, filename) in EXTERNAL.items():
            lines.extend([f"## {label}", "", *performance_table(summary, phase), "", f"![{label} 吞吐]({filename}.png)", ""])
        lines.extend(["SPEED-Bench 使用去重后的写作、代码和多语言提示。BurstGPT 回放三段轨迹，保留请求长度和相对到达间隔。回放速率会限制总吞吐，因此也要看首 token 延迟和每 token 延迟。", ""])
    cells = summary["protocol"]["concurrencies"]
    columns = "".join(f" C={concurrency} TPS |" for concurrency in cells)
    counts = summary["benchmark_counts"]
    extra = summary.get("external", {}).get("benchmark_count", 0)
    lines.extend(["## 两轮调参", "",
                  f"调参跑了 {counts['tuning']} 个执行单元。留出复测、外部负载和随机压测各有 {counts['holdout']}、{extra} 和 {counts['stress']} 个执行单元。", "",
                  f"| 方法 | 轮次 | 配置 |{columns} 调参得分 | CUDA Graph | 入选 |",
                  "|---|---:|---|" + "---:|" * len(cells) + "---:|---|---|"])
    for method, info in summary["methods"].items():
        selected = info["selection"]["selected"]["id"]
        for phase, phase_rows in enumerate((info["selection"]["round1"], info["selection"]["round2"]), start=1):
            for row in phase_rows:
                profile = row["profile"]["id"]
                score = f"{row['score']:.2f}" if "score" in row else "运行失败"
                speeds = "".join(f" {row['tps'][str(c)]:.2f} |" if "tps" in row else " — |" for c in cells)
                graph = {"full": "完整", "disabled": "关闭", "unconfirmed": "未确认"}.get(row.get("cuda_graph"), "—")
                lines.append(f"| {LABELS[method]} | {phase} | `{profile}` |{speeds} {score} | {graph} | "
                             f"{'✓' if profile == selected else ''} |")
    if any(info["stress"] for info in summary["methods"].values()):
        lines.extend(["", "## 合成压力对照", "", *performance_table(summary, "stress"), "",
                      "![随机压力测试](random-stress.png)"])
    lines.append("")
    return "\n".join(lines)


def generate_report(results, output, external=None, profiles=None):
    summary = read_json(results) if results.is_file() else collect(results, profiles)
    if summary["schema"] != SCHEMA:
        raise ValueError("Unsupported summary format")
    if external is not None:
        summary["external"] = collect_external(external, summary)
    output.mkdir(parents=True, exist_ok=True)
    write_json(output / "summary.json", summary)
    (output / "results.md").write_text(render_tables(summary), encoding="utf-8")
    plt = setup_plots()
    workflow_plot(output, plt)
    speed_plot(summary, output, plt, "holdout")
    latency_plot(summary, output, plt)
    speed_plot(summary, output, plt, "stress")
    if "external" in summary:
        for phase in EXTERNAL:
            speed_plot(summary, output, plt, phase)
