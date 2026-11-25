#!/usr/bin/env python3
"""Record GPU state throughout a benchmark phase without using extra devices."""

import argparse
import csv
import datetime as dt
from pathlib import Path
import subprocess
import time

FIELDS = [
    "timestamp_utc",
    "gpu_index",
    "gpu_uuid",
    "temperature_c",
    "power_w",
    "sm_clock_mhz",
    "memory_clock_mhz",
    "gpu_utilization_percent",
    "memory_used_mib",
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--interval", type=float, default=5.0)
    parser.add_argument("--devices", default="0,1,2,3")
    args = parser.parse_args()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("x", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        while True:
            started = time.monotonic()
            result = subprocess.run(
                [
                    "/usr/bin/nvidia-smi",
                    f"--id={args.devices}",
                    "--query-gpu=index,uuid,temperature.gpu,power.draw,clocks.sm,clocks.mem,utilization.gpu,memory.used",
                    "--format=csv,noheader,nounits",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            timestamp = dt.datetime.now(dt.timezone.utc).isoformat()
            for line in result.stdout.splitlines():
                values = [value.strip() for value in line.split(",")]
                if len(values) != 8:
                    continue
                writer.writerow(dict(zip(FIELDS, [timestamp, *values])))
            handle.flush()
            elapsed = time.monotonic() - started
            time.sleep(max(0.0, args.interval - elapsed))


if __name__ == "__main__":
    main()
