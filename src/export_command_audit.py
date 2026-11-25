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


def log_reference(value: str | None) -> str:
    if not value:
        return "- 输出日志未记录"
    log = Path(value)
    relative = Path(*log.parts[-3:])
    if relative.parent == Path("logs/commands"):
        return f"- [输出日志 {log.name}](../{relative.as_posix()})"
    return f"- 输出日志位于 `{value}`"


def read_events() -> list[dict]:
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
    return records


def write_structured(records: list[dict], archive: Path) -> None:
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
    archive.write_text(
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


def main() -> None:
    archive = PROCESSED / "command-audit.json"
    if INDEX.is_file():
        records = read_events()
        write_structured(records, archive)
    else:
        records = json.loads(archive.read_text(encoding="utf-8"))["records"]

    lines = [
        "# 实验命令记录",
        "",
        "日志保留每条命令的标准输出和标准错误。[请求级结果](../results/raw/) · [结构化命令记录](../results/processed/command-audit.json)",
        "",
    ]
    for index, record in enumerate(records, 1):
        lines += [
            f"## {index}. {record['label']}",
            "",
            f"- 状态为 `{record['status']}`，退出码为 {record['exit_code'] if record['exit_code'] is not None else '未记录'}",
            f"- 开始于 {record['started_at']}" if record["started_at"] else "- 开始时间未记录",
            f"- 结束于 {record['finished_at']}" if record["finished_at"] else "- 结束时间未记录",
            f"- 工作目录为 `{record['cwd']}`" if record["cwd"] else "- 工作目录未记录",
            log_reference(record["output_log"]),
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
