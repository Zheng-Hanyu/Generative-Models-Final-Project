#!/usr/bin/env python3
"""Safely stop a command launched by run_logged.py after checking its argv."""

import argparse
import json
import os
from pathlib import Path
import re
import signal
import time

ROOT = Path(__file__).resolve().parents[1]


def process_argv(pid):
    try:
        raw = Path(f"/proc/{pid}/cmdline").read_bytes()
    except FileNotFoundError:
        return None
    return [part.decode("utf-8", errors="replace") for part in raw.split(b"\0") if part]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", required=True)
    parser.add_argument("--expect", action="append", default=[])
    parser.add_argument("--timeout", type=float, default=120.0)
    parser.add_argument("--signal", choices=["TERM", "INT"], default="TERM")
    args = parser.parse_args()
    safe_label = re.sub(r"[^A-Za-z0-9_.-]+", "_", args.label)
    pid_path = ROOT / "logs" / f"{safe_label}.pid"
    if not pid_path.exists():
        print(json.dumps({"label": args.label, "status": "not_running"}))
        return 0
    pid = int(pid_path.read_text().strip())
    argv = process_argv(pid)
    if argv is None:
        pid_path.unlink(missing_ok=True)
        print(json.dumps({"label": args.label, "pid": pid, "status": "already_exited"}))
        return 0
    missing = [item for item in args.expect if not any(item in part for part in argv)]
    if missing:
        raise SystemExit(
            f"Refusing to signal PID {pid}: expected argv fragments not found: {missing}; argv={argv}"
        )

    sig = signal.SIGTERM if args.signal == "TERM" else signal.SIGINT
    os.kill(pid, sig)
    deadline = time.monotonic() + args.timeout
    while time.monotonic() < deadline:
        if not process_argv(pid):
            break
        time.sleep(0.2)
    else:
        raise SystemExit(f"PID {pid} did not exit within {args.timeout}s after {sig.name}")
    print(
        json.dumps(
            {
                "label": args.label,
                "pid": pid,
                "signal": sig.name,
                "status": "exited",
                "checked_at": time.time(),
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
