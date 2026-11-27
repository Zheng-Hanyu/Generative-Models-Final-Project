"""Validate paired measurements and render the unified framework's figures."""

from __future__ import annotations

import re
from math import ceil, isclose
from pathlib import Path
from statistics import geometric_mean, median

from comparison_report import collect_paired, report_comparison
from plot_style import BASELINE, DFLASH, METHOD_STYLES, save_plot, setup_plots, speed_bars
from workloads import ROOT, cell_name, read_json, stress_cells, write_json


LABELS = {"normal": "Normal", "mtp": "Native MTP", "dspark": "DSpark", "dflash": "DFlash 2", "suffix": "Suffix"}
EXTERNAL = {"speed": "NVIDIA SPEED-Bench", "burst": "BurstGPT v2.0"}
METRICS = ("output_throughput", "p95_ttft_ms", "p95_tpot_ms", "spec_decode_acceptance_rate")
SCHEMA = 2
PUBLISHED = {
    "framework": ROOT / "results/processed/unified-framework/summary.json",
    "paired": ROOT / "results/processed/unified-framework/eagle4-suffix-b200.json",
    "standard-suffix": ROOT / "results/processed/supplemental_speculative_summary.json",
}


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


def collect(root, profiles):
    direct = (root / "experiment.json").is_file()
    if direct:
        profiles = [read_json(root / "experiment.json")["method"]]
    else:
        profiles = [method for method in profiles if (root / method / "experiment.json").is_file()]
    profiles = [method for method in profiles if method != "normal"]
    if not profiles:
        raise ValueError(f"{root}: no method replay with a Normal control")
    methods = {}
    workload_identity = None
    environment_identity = None
    stress_enabled = None
    for method in profiles:
        lane = root if direct else root / method
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
    return {
        "schema": SCHEMA, "model": model, "vllm": vllm, "gpu": gpu, "driver": driver,
        "protocol": protocol, "data_sha256": data_sha256, "workloads": workloads,
        "methods": methods, "benchmark_counts": count_method_runs(methods),
    }


def count_method_runs(methods):
    counts = {"tuning": 0, "holdout": 0, "stress": 0}
    for info in methods.values():
        selection = info["selection"]
        profiles = 2 + int(selection["reference"]["id"] != selection["selected"]["id"])
        counts["tuning"] += sum(len(row.get("tps", {})) for key in ("round1", "round2") for row in selection[key])
        for phase in ("holdout", "stress"):
            counts[phase] += profiles * sum(len(row["runs"]) for row in info[phase].values())
    return counts


def external_cells(lane, manifest, confirmation, roles):
    cells = {}
    for cell in manifest["cells"]:
        workload, concurrency = cell["workload"], cell["concurrency"]
        cells.setdefault((workload, concurrency), []).append(cell)
    if set(cells) != {("speed", 1), ("speed", 16), ("burst", 16)}:
        raise ValueError("Incomplete external benchmark matrix")
    results = {"speed": {}, "burst": {}}
    for (workload, concurrency), group in cells.items():
        seeds = [cell["seed"] for cell in group]
        if len(set(seeds)) != 3 or len(seeds) != 3:
            raise ValueError("External workload requires three independent trials")
        runs = {}
        for role in roles:
            directory = lane / "external" / confirmation[role]
            speeds = read_json(directory / "completed.json")["speeds"]
            rows = []
            for cell in group:
                name = cell_name(workload, concurrency, cell["seed"])
                row = load_run(directory, name, cell["count"], concurrency, speeds)
                if workload == "burst":
                    row["dispatch_span_seconds"] = max(row["start_times"]) - min(row["start_times"])
                rows.append(row)
            if runs and any(a["output_lens"] != b["output_lens"] for a, b in zip(runs["normal"], rows, strict=True)):
                raise ValueError(f"{workload}: paired output budgets differ")
            runs[role] = rows
        results[workload][str(concurrency)] = summarize_cells(runs, seeds)
    return results


def collect_external(root, summary):
    results = {}
    common_manifest = None
    for method, details in summary["methods"].items():
        lane = root if (root / "experiment.json").is_file() else root / method
        identity = read_json(lane / "experiment.json")
        confirmation = read_json(lane / "confirmation.json")
        manifest = identity["external_workloads"]
        if common_manifest is not None and common_manifest != manifest:
            raise ValueError("External benchmark workloads differ across methods")
        common_manifest = manifest
        if (identity["method"] != method or identity["method_config"]["reference"]["id"] != details["recommended"]["id"]
                or ("spec" in details["recommended"] and identity["method_config"]["reference"] != details["recommended"])
                or confirmation["selected"] != details["recommended"]["id"] or confirmation["normal"] != "normal"
                or Path(identity["target"]).name != summary["model"] or identity["vllm_version"] != summary["vllm"]
                or identity["gpu"]["name"] != summary["gpu"] or identity["gpu"]["driver_version"] != summary["driver"]):
            raise ValueError(f"{lane}: external benchmark environment or profile does not match the report")
        results[method] = external_cells(lane, manifest, confirmation, ("normal", "selected"))
    return {"manifest": common_manifest, "methods": results, "benchmark_count": len(common_manifest["cells"]) * 2 * len(results)}


def apply_draft_study(summary, root):
    if "external" not in summary:
        raise ValueError("A draft study must be included with the three-workload report")
    study = collect(root / "raw", ["dflash"])
    for key in ("model", "vllm", "gpu", "driver", "protocol", "data_sha256", "workloads"):
        if study[key] != summary[key]:
            raise ValueError(f"Draft study differs from the report in {key}")

    raw = root / "raw/dflash"
    external = root / "external/dflash"
    core = study["methods"]["dflash"]
    selection = read_json(raw / "selection.json")
    reference, selected = selection["reference"], selection["selected"]
    if {key: value for key, value in selected["spec"].items() if key != "quantization"} != reference["spec"]:
        raise ValueError("Draft study comparison may only change draft precision")
    roles = ("normal", "reference", "selected")
    expected = {"normal": "normal", "reference": reference["id"], "selected": selected["id"]}
    identity = read_json(external / "experiment.json")
    raw_identity = read_json(raw / "experiment.json")
    manifest = identity.pop("external_workloads")
    if (identity != raw_identity or manifest != summary["external"]["manifest"]
            or read_json(external / "confirmation.json") != expected):
        raise ValueError("Draft study external inputs or comparison profiles differ from the Spec-Bench run")

    comparison = external_cells(external, manifest, expected, roles)
    workload_scores = {
        name: geometric_mean(median(cell["to_reference"]) for cell in cells.values())
        for name, cells in {"holdout": core["holdout"], **comparison}.items()
    }
    throughput_score = geometric_mean(workload_scores.values())
    adopted = throughput_score > 1 and min(workload_scores.values()) >= 0.97
    kept = "selected" if adopted else "reference"
    core["recommended"] = selected if adopted else reference
    core["retained_score_vs_normal"] = geometric_mean(
        median(paired_ratios(cell, "output_throughput", kept)) for cell in core["holdout"].values()
    )

    memory = {}
    attention_versions = set()
    for role in roles:
        log = (raw / "holdout" / expected[role] / "server.log").read_text(encoding="utf-8", errors="replace")
        memory[role] = model_memory_gib(log)
        if role != "normal":
            versions = set(re.findall(r"Using FlashAttention version (\d+)", log))
            if len(versions) != 1:
                raise ValueError(f"Could not identify the DFlash 2 FlashAttention version for {role}")
            attention_versions.update(versions)
    if len(attention_versions) != 1:
        raise ValueError("Draft quantization must keep the same FlashAttention version")

    summary["methods"]["dflash"] = core
    summary["benchmark_counts"] = count_method_runs(summary["methods"])
    summary["external"]["methods"]["dflash"] = {**comparison, "retained_role": kept}
    summary["external"]["benchmark_count"] = sum(
        len(cell["runs"]) * len(cell["successful"])
        for phases in summary["external"]["methods"].values()
        for phase in EXTERNAL for cell in phases[phase].values()
    )
    summary["dflash_quantization"] = {
        "quantized_format": selected["spec"]["quantization"], "release_role": kept,
        "throughput_score_vs_bf16": throughput_score, "workload_scores_vs_bf16": workload_scores,
        "flash_attention_version": int(attention_versions.pop()), "model_memory_gib": memory,
        "screening_memory_gib": {
            row["profile"]["id"]: model_memory_gib(
                (raw / "tuning" / row["profile"]["id"] / "server.log").read_text(encoding="utf-8", errors="replace")
            )
            for phase in ("round1", "round2") for row in selection[phase] if "score" in row
        },
    }


def model_memory_gib(log):
    values = re.findall(r"Model loading took ([\d.]+) GiB memory", log)
    if len(values) != 1:
        raise ValueError("Expected one model-loading memory measurement in the vLLM server log")
    return float(values[0])


def render_draft_study(summary):
    study = summary["dflash_quantization"]
    core = summary["methods"]["dflash"]
    external = summary["external"]["methods"]["dflash"]
    phases = {"Spec-Bench": core["holdout"], "SPEED-Bench": external["speed"], "BurstGPT v2.0": external["burst"]}
    memory = study["model_memory_gib"]
    scores = study["workload_scores_vs_bf16"]
    lines = [
        "", "## DFlash 2 草稿量化复测", "",
        f"入选量化为 `{study['quantized_format']}`，发布配置为 `{core['recommended']['id']}`。"
        f"相对 BF16 的三套负载综合倍率为 {study['throughput_score_vs_bf16']:.3f}×。"
        f"Spec-Bench、SPEED-Bench 和 BurstGPT 的倍率分别为 {scores['holdout']:.3f}×、"
        f"{scores['speed']:.3f}× 和 {scores['burst']:.3f}×。"
        "每套负载先对各档并发的配对中位倍率取几何平均，三套负载等权。"
        "综合倍率大于 1 且各套负载降幅均在 3% 以内时采用量化。",
        "",
        f"vLLM 报告的模型加载显存为 Normal {memory['normal']:.2f} GiB、DFlash 2 BF16 {memory['reference']:.2f} GiB、"
        f"量化草稿 {memory['selected']:.2f} GiB。该值不含 KV cache 和 CUDA Graph。两种草稿使用 FlashAttention {study['flash_attention_version']}。",
        "",
        "| 负载 | 并发 | TPS（BF16 → 量化） | 配对倍率（中位数及范围） | P95 TTFT (ms) | P95 TPOT (ms) | 草稿接受率 | 成功请求 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for label, cells in phases.items():
        for concurrency, cell in cells.items():
            metrics = []
            for key in ("median_tps", "median_p95_ttft_ms", "median_p95_tpot_ms"):
                metrics.append(" → ".join(f"{cell[key][r]:.2f}" for r in ("reference", "selected")))
            accept = " → ".join(f"{median(row[r]['spec_decode_acceptance_rate'] for row in cell['runs']):.1f}%"
                                for r in ("reference", "selected"))
            success = " → ".join(f"{cell['successful'][r]}/{cell['successful'][r] + cell['failed'][r]}"
                                 for r in ("reference", "selected"))
            ratios = cell["to_reference"]
            speed = f"{median(ratios):.3f}× ({min(ratios):.3f}–{max(ratios):.3f})"
            lines.append(f"| {label} | {concurrency} | {metrics[0]} | {speed} | "
                         f"{metrics[1]} | {metrics[2]} | {accept} | {success} |")
    return lines


def phase_rows(summary, phase):
    if phase in EXTERNAL:
        return {method: (info[phase], info.get("retained_role", "selected"))
                for method, info in summary["external"]["methods"].items()}
    return {method: (info[phase], retained_role(info)) for method, info in summary["methods"].items()}


def serving_throughput_plot(summary, output, plt):
    panels = [("holdout", "Spec-Bench holdout")]
    if "external" in summary:
        panels.extend((("speed", "SPEED-Bench"), ("burst", "BurstGPT v2.0")))
    if any(info["stress"] for info in summary["methods"].values()):
        panels.append(("stress", "Synthetic stress"))
    columns = min(2, len(panels))
    rows = ceil(len(panels) / columns)
    fig, axes = plt.subplots(rows, columns, figsize=(7.7 if columns == 2 else 5.65, 1.99 * rows + 0.95),
                             sharey=True, squeeze=False)
    peak = 1.0
    handles = {}
    for index, ((phase, title), ax) in enumerate(zip(panels, axes.flat)):
        groups = {
            method: {c: paired_ratios(cell, "output_throughput", role) for c, cell in cells.items()}
            for method, (cells, role) in phase_rows(summary, phase).items() if cells
        }
        peak = max(peak, speed_bars(ax, groups))
        ax.set_title(f"({chr(97 + index)})  {title}", loc="left")
        artists, methods = ax.get_legend_handles_labels()
        handles.update(zip(methods, artists, strict=True))
    for ax in list(axes.flat)[len(panels):]:
        ax.set_visible(False)
    axes[0, 0].set_ylim(0, max(1.5, ceil(2.25 * peak) / 2))
    fig.supylabel("Output throughput / matched Normal", x=0.028)
    fig.supxlabel("Concurrent requests", y=0.032)
    fig.legend(list(handles.values()), [LABELS[method] for method in handles], loc="upper center",
               bbox_to_anchor=(0.5, 0.992), ncol=len(handles))
    fig.subplots_adjust(left=0.106 if columns == 2 else 0.14, right=0.98,
                        bottom=0.13 if rows == 2 else 0.17, top=0.855 if rows == 2 else 0.80,
                        wspace=0.18, hspace=0.40)
    save_plot(fig, plt, output, "serving-throughput")


def latency_plot(summary, output, plt):
    cells = list(next(iter(summary["methods"].values()))["holdout"])
    x = range(len(cells))
    fig, axes = plt.subplots(1, 2, figsize=(7.7, 3.25), sharey=True)
    for ax, metric, title in zip(axes, ("p95_ttft_ms", "p95_tpot_ms"),
                                 ("(a)  Time to first token", "(b)  Time per output token"), strict=True):
        ax.axhline(1, color=BASELINE, linestyle="--", linewidth=1.0)
        ax.grid(axis="y")
        for method, info in summary["methods"].items():
            ratios = [median(paired_ratios(info["holdout"][c], metric, retained_role(info))) for c in cells]
            color, marker, style = METHOD_STYLES[method]
            ax.plot(x, ratios, color=color, marker=marker, linestyle=style, markeredgecolor="white",
                    markeredgewidth=0.6, label=LABELS[method])
        ax.set_title(title, loc="left")
        ax.set_xticks(x, cells)
    axes[0].set_ylabel("P95 latency / matched Normal")
    fig.supxlabel("Concurrent requests", y=0.025)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper center", bbox_to_anchor=(0.5, 0.992), ncol=len(labels))
    fig.subplots_adjust(left=0.104, right=0.975, bottom=0.16, top=0.81, wspace=0.17)
    save_plot(fig, plt, output, "spec-bench-latency")


def method_summary(summary):
    c = str(max(summary["protocol"]["concurrencies"]))
    lines = ["## 各方法的吞吐和尾延迟", "",
             f"Spec-Bench 并发 {c} 时，各方法独立配对同卡、同 vLLM 构建的 Normal。表中的延迟是两组各自的逐轮中位数。", "",
             "| 方法 | Spec-Bench 综合倍率 | 并发 " + c + " 吞吐倍率 | P95 TTFT (ms) | P95 TPOT (ms) |",
             "|---|---:|---:|---:|---:|"]
    for method, info in summary["methods"].items():
        role = retained_role(info)
        cell = info["holdout"][c]
        speed = median(paired_ratios(cell, "output_throughput", role))
        latencies = [" → ".join(f"{cell[key][k]:.2f}" for k in ("normal", role))
                     for key in ("median_p95_ttft_ms", "median_p95_tpot_ms")]
        lines.append(f"| {LABELS[method]} | {info['retained_score_vs_normal']:.3f}× | {speed:.3f}× "
                     f"| {latencies[0]} | {latencies[1]} |")
    if "external" in summary:
        lines.extend(["", "BurstGPT 按固定到达轨迹回放。此处同时列出吞吐、首 token 和后续生成的延迟。", "",
                      "| 方法 | BurstGPT 并发 16 吞吐倍率 | P95 TTFT (ms) | P95 TPOT (ms) |",
                      "|---|---:|---:|---:|"])
        for method, info in summary["external"]["methods"].items():
            role = info.get("retained_role", "selected")
            cell = info["burst"]["16"]
            speed = median(paired_ratios(cell, "output_throughput", role))
            latencies = [" → ".join(f"{cell[key][k]:.2f}" for k in ("normal", role))
                         for key in ("median_p95_ttft_ms", "median_p95_tpot_ms")]
            lines.append(f"| {LABELS[method]} | {speed:.3f}× | {latencies[0]} | {latencies[1]} |")
    return lines


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
    lines.extend(["", "Spec-Bench 综合倍率取各档并发的配对中位倍率，再作几何平均。各负载下均使用表中的最终配置。", "",
                  *method_summary(summary), "",
                  "吞吐柱表示配对中位数，须线覆盖各轮最小值和最大值。虚线对应 Normal，随机压力每档只测一轮。", "",
                  "![各负载的输出吞吐与三轮范围](figures/serving-throughput.png)", "",
                  "## Spec-Bench 留出集", "", *performance_table(summary, "holdout"), "",
                  "![Spec-Bench 配对 P95 首 token 延迟和每 token 延迟](figures/spec-bench-latency.png)", "",
                  "延迟图先对各轮 P95 计算方法相对 Normal 的倍率，再取中位数。低于 1 表示延迟下降。", ""])
    if "external" in summary:
        for phase, label in EXTERNAL.items():
            lines.extend([f"## {label}", "", *performance_table(summary, phase), ""])
        lines.extend(["SPEED-Bench 使用去重后的写作、代码和多语言提示。BurstGPT 回放三段轨迹，保留请求长度和相对到达间隔。回放速率会限制总吞吐，因此也要看首 token 延迟和每 token 延迟。", ""])
    cells = summary["protocol"]["concurrencies"]
    columns = "".join(f" C={concurrency} TPS |" for concurrency in cells)
    counts = summary["benchmark_counts"]
    extra = summary.get("external", {}).get("benchmark_count", 0)
    memory = summary.get("dflash_quantization", {}).get("screening_memory_gib", {})
    memory_column = " 模型显存 (GiB) |" if memory else ""
    memory_separator = "---:|" if memory else ""
    lines.extend(["## 调参记录", "",
                  f"调参跑了 {counts['tuning']} 个执行单元。留出复测、外部负载和随机压测各有 {counts['holdout']}、{extra} 和 {counts['stress']} 个执行单元。", "",
                  f"| 方法 | 轮次 | 配置 |{columns} 调参得分 | CUDA Graph |{memory_column} 入选 |",
                  "|---|---:|---|" + "---:|" * len(cells) + "---:|---|" + memory_separator + "---|"])
    for method, info in summary["methods"].items():
        selected = info["selection"]["selected"]["id"]
        for phase, phase_rows in enumerate((info["selection"]["round1"], info["selection"]["round2"]), start=1):
            for row in phase_rows:
                profile = row["profile"]["id"]
                score = f"{row['score']:.2f}" if "score" in row else "运行失败"
                speeds = "".join(f" {row['tps'][str(c)]:.2f} |" if "tps" in row else " — |" for c in cells)
                graph = {"full": "完整", "disabled": "关闭", "unconfirmed": "未确认"}.get(row.get("cuda_graph"), "—")
                loaded = f"{memory[profile]:.2f}" if profile in memory else "—"
                lines.append(f"| {LABELS[method]} | {phase} | `{profile}` |{speeds} {score} | {graph} | "
                             f"{loaded + ' | ' if memory else ''}{'✓' if profile == selected else ''} |")
    if any(info["stress"] for info in summary["methods"].values()):
        lines.extend(["", "## 合成压力对照", "", "每档仅测一轮，适合观察该次回放的量级。", "",
                      *performance_table(summary, "stress")])
    if "dflash_quantization" in summary:
        lines.extend(render_draft_study(summary))
        lines.extend(["", "![DFlash 2 草稿量化的模型显存与配对吞吐](figures/dflash-quantization.png)"])
    lines.append("")
    return "\n".join(lines)


def generate_report(results, output, plt, external=None, profiles=None, draft_study=None):
    summary = read_json(results) if results.is_file() else collect(results, profiles)
    if summary["schema"] != SCHEMA:
        raise ValueError("Unsupported summary format")
    if external is not None:
        summary["external"] = collect_external(external, summary)
    if draft_study is not None:
        apply_draft_study(summary, draft_study)
    output.mkdir(parents=True, exist_ok=True)
    write_json(output / "summary.json", summary)
    (output / "results.md").write_text(render_tables(summary), encoding="utf-8")
    figures = output / "figures"
    figures.mkdir(exist_ok=True)
    serving_throughput_plot(summary, figures, plt)
    latency_plot(summary, figures, plt)
    if "dflash_quantization" in summary:
        quantization_plot(summary["dflash_quantization"], figures, plt)


def quantization_plot(data, output, plt):
    fig, (memory, speed) = plt.subplots(1, 2, figsize=(7.75, 3.45), gridspec_kw={"width_ratios": (0.9, 1.1)})
    quantization = data["quantized_format"].upper()
    memory.set_title("(a)  Model loading memory", loc="left")
    values = [data["model_memory_gib"][role] for role in ("reference", "selected")]
    memory.barh([0, 1], values, height=0.37, color=(BASELINE, DFLASH), alpha=0.87)
    for index, value in enumerate(values):
        memory.annotate(f"{value:.2f}", (value, index), xytext=(5, 0), textcoords="offset points", va="center")
    memory.set_yticks([0, 1], ("BF16", quantization))
    memory.set(xlim=(0, max(values) * 1.24), ylim=(1.65, -0.65), xlabel="GPU memory (GiB)")
    memory.grid(axis="x")

    speed.set_title(f"(b)  {quantization} throughput vs BF16", loc="left")
    scores = data["workload_scores_vs_bf16"]
    positions = range(3)
    speed.axvline(1, color=BASELINE, linestyle="--", linewidth=1.05)
    values = [scores[key] for key in ("holdout", "speed", "burst")]
    span = max(0.025, *(abs(value - 1) for value in values))
    for index, value in enumerate(values):
        speed.hlines(index, min(1, value), max(1, value), linewidth=2.4, color=DFLASH, alpha=0.5)
        speed.scatter(value, index, color=DFLASH, s=44, marker="D", edgecolor="white", linewidth=0.7, zorder=3)
        speed.annotate(f"{value:.3f}×", (value, index), xytext=(6, 0), textcoords="offset points", va="center")
    speed.set_yticks(list(positions), ("Spec-Bench", "SPEED-Bench", "BurstGPT"))
    speed.set(xlim=(1 - 1.25 * span, 1 + 1.85 * span), ylim=(2.55, -0.55), xlabel="Geometric mean of paired medians")
    speed.grid(axis="x")
    fig.tight_layout(w_pad=2.0)
    save_plot(fig, plt, output, "dflash-quantization")


def report_studies(args, config):
    study = args.study
    if args.results and study is None:
        if args.results.is_file():
            data = read_json(args.results)
            if "profiles" in data:
                study = "standard-suffix" if "suffix-standard" in data["winners"] else "paired"
            else:
                study = "standard-suffix" if "cell_sha256" in data else "framework"
        elif (args.results / "experiment.json").is_file():
            study = read_json(args.results / "experiment.json").get("study", "framework")
        else:
            study = "framework"
    studies = [study] if study else list(PUBLISHED)
    if "framework" not in studies and (args.external_results or args.draft_study):
        raise ValueError("--external-results and --draft-study apply to the framework report")
    plt = setup_plots()
    for name in studies:
        results = args.results or PUBLISHED[name]
        if name == "framework":
            framework = config["studies"]["framework"]
            generate_report(results, args.output, plt, args.external_results, framework["methods"], args.draft_study)
        else:
            data = read_json(results) if results.is_file() else collect_paired(results, config, name)
            report_comparison(data, name, args.output, plt)
