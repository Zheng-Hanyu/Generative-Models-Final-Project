#!/usr/bin/env python3
"""Launch run_logged.py in a detached session for long-lived servers."""

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
RUN_LOGGED = ROOT / "bin" / "run_logged.py"


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
    pid_path = ROOT / "logs" / f"{safe_label}.pid"
    if pid_path.exists():
        raise SystemExit(f"Refusing to duplicate label with live PID file: {pid_path}")

    console_path = ROOT / "logs" / "server" / f"{safe_label}.console.log"
    launcher_path = ROOT / "logs" / "server" / f"{safe_label}.launcher.json"
    argv = [
        sys.executable,
        str(RUN_LOGGED),
        "--label",
        args.label,
        "--cwd",
        args.cwd,
        "--",
        *command,
    ]
    with console_path.open("w", encoding="utf-8") as console:
        process = subprocess.Popen(
            argv,
            cwd=args.cwd,
            stdin=subprocess.DEVNULL,
            stdout=console,
            stderr=subprocess.STDOUT,
            start_new_session=True,
            env=os.environ.copy(),
        )
    record = {
        "label": args.label,
        "launcher_pid": process.pid,
        "launched_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "run_logged_argv": argv,
        "server_command": shlex.join(command),
        "console_log": str(console_path),
        "server_pid_file": str(pid_path),
    }
    launcher_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(record, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
