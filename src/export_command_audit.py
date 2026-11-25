#!/usr/bin/env python3
"""Export the append-only command audit into convenient CSV, JSON and Markdown."""

from __future__ import annotations

import csv
import json
from collections import defaultdict
from datetime import datetime
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "logs" / "commands.jsonl"
PROCESSED = ROOT / "results" / "processed"
REPORT = ROOT / "report"


def parse_time(value: str | None) -> datetime | None:
    return datetime.fromisoformat(value) if value else None


def main() -> None:
    active: dict[str, list[dict]] = defaultdict(list)
    records: list[dict] = []
    for line in INDEX.read_text(encoding="utf-8").splitlines():
        event = json.loads(line)
        label = event["label"]
        if event["event"] == "started":
            active[label].append(event)
            continue
        if event["event"] not in {"finished", "reconciled_stopped"}:
            continue
        start = active[label].pop(0) if active[label] else {"label": label}
        started_at = start.get("started_at")
        finished_at = event.get("finished_at")
        start_time, end_time = parse_time(started_at), parse_time(finished_at)
        status = (
            "stopped"
            if event["event"] == "reconciled_stopped"
            else "completed" if event.get("exit_code") == 0 else "failed"
        )
        records.append(
            {
                "label": label,
                "status": status,
                "exit_code": event.get("exit_code"),
                "started_at": started_at,
                "finished_at": finished_at,
                "duration_seconds": (end_time - start_time).total_seconds() if start_time and end_time else None,
                "cwd": start.get("cwd"),
                "command": start.get("command"),
                "argv": start.get("argv"),
                "output_log": event.get("output_log") or start.get("output_log"),
            }
        )
    for label, starts in active.items():
        for start in starts:
            records.append(
                {
                    "label": label,
                    "status": "running",
                    "exit_code": None,
                    "started_at": start.get("started_at"),
                    "finished_at": None,
                    "duration_seconds": None,
                    "cwd": start.get("cwd"),
                    "command": start.get("command"),
                    "argv": start.get("argv"),
                    "output_log": start.get("output_log"),
                }
            )
    records.sort(key=lambda item: item.get("started_at") or "")

    csv_fields = [
        "label",
        "status",
        "exit_code",
        "started_at",
        "finished_at",
        "duration_seconds",
        "cwd",
        "command",
        "output_log",
    ]
    with (PROCESSED / "command-audit.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=csv_fields, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(records)
    (PROCESSED / "command-audit.json").write_text(
        json.dumps(
            {
                "schema_version": 1,
                "source": str(INDEX),
                "record_count": len(records),
                "records": records,
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    lines = [
        "# 完整命令审计",
        "",
        "本文件由 `logs/commands.jsonl` 自动导出。每次命令的完整标准输出与标准错误保留在所链接的日志中；基准请求的原始指标保存在 `results/raw/`。",
        "",
    ]
    for index, record in enumerate(records, 1):
        lines += [
            f"## {index}. {record['label']}",
            "",
            f"- 状态：{record['status']}；退出码：{record['exit_code']}",
            f"- 开始：{record['started_at']}",
            f"- 结束：{record['finished_at']}",
            f"- 工作目录：`{record['cwd']}`",
            f"- 输出日志：[{Path(record['output_log']).name}]({record['output_log']})" if record["output_log"] else "- 输出日志：无",
            "",
            "```bash",
            record["command"] or "",
            "```",
            "",
        ]
    (REPORT / "command_audit.md").write_text("\n".join(lines), encoding="utf-8")
    counts = {status: sum(r["status"] == status for r in records) for status in ["completed", "failed", "stopped", "running"]}
    print(json.dumps({"records": len(records), "status_counts": counts}, ensure_ascii=False))


if __name__ == "__main__":
    main()
