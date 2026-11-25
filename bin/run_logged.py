#!/usr/bin/env python3
"""Run a command while preserving its arguments, output, timing, and exit code."""

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys
import threading

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "logs" / "commands.jsonl"


def timestamp():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def append_event(event):
    with INDEX.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(event, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    parser.add_argument("--cwd", default=str(ROOT))
    parser.add_argument("command", nargs=argparse.REMAINDER)
    args = parser.parse_args()
    command = args.command
    if command and command[0] == "--":
        command = command[1:]
    if not command:
        parser.error("a command is required after --")

    safe_label = re.sub(r"[^A-Za-z0-9_.-]+", "_", args.label)
    output_path = ROOT / "logs" / "commands" / f"{safe_label}.log"
    counter = 1
    while output_path.exists():
        output_path = ROOT / "logs" / "commands" / f"{safe_label}.{counter}.log"
        counter += 1

    event = {
        "event": "started",
        "label": args.label,
        "started_at": timestamp(),
        "cwd": os.path.abspath(args.cwd),
        "argv": command,
        "command": shlex.join(command),
        "output_log": str(output_path),
    }
    print(f"+ {event['command']}", flush=True)

    with output_path.open("w", encoding="utf-8") as log:
        log.write(f"COMMAND: {event['command']}\n")
        log.write(f"CWD: {event['cwd']}\n")
        log.write(f"STARTED_AT: {event['started_at']}\n\n")
        log.flush()
        process = subprocess.Popen(
            command,
            cwd=args.cwd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )
        event["pid"] = process.pid
        append_event(event)
        pid_path = ROOT / "logs" / f"{safe_label}.pid"
        pid_path.write_text(str(process.pid) + "\n")

        def forward_output():
            assert process.stdout is not None
            for line in process.stdout:
                sys.stdout.write(line)
                sys.stdout.flush()
                log.write(line)
                log.flush()

        reader = threading.Thread(target=forward_output)
        reader.start()
        try:
            return_code = process.wait()
        except KeyboardInterrupt:
            process.send_signal(2)
            return_code = process.wait()
        finally:
            reader.join()

    append_event({
        "event": "finished",
        "label": args.label,
        "finished_at": timestamp(),
        "pid": process.pid,
        "output_log": str(output_path),
        "exit_code": return_code,
    })
    pid_path.unlink(missing_ok=True)
    return return_code


if __name__ == "__main__":
    sys.exit(main())
