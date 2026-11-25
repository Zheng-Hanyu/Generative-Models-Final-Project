#!/usr/bin/env python3
"""Validate retained raw results and export checksums for reproducibility."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "results" / "raw"
PROCESSED = ROOT / "results" / "processed"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--required-summaries", nargs="+", default=["formal-r1", "semantic-r1"])
    args = parser.parse_args()

    raw_files = sorted(RAW.glob("*.json"))
    checks = []
    errors = []
    checksum_rows = []
    total_requests = 0
    for path in raw_files:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            if "completed" not in data:
                checks.append(
                    {
                        "file": str(path.relative_to(ROOT)),
                        "type": "auxiliary_smoke_record",
                        "checks": {"json_parseable": True},
                    }
                )
                checksum_rows.append(
                    {
                        "file": str(path.relative_to(ROOT)),
                        "bytes": path.stat().st_size,
                        "sha256": sha256(path),
                    }
                )
                continue
            completed = data["completed"]
            output_lens = data["output_lens"]
            file_checks = {
                "no_failed_requests": data["failed"] == 0,
                "output_length_rows_match_completed": len(output_lens) == completed,
                "fixed_output_length": len(set(output_lens)) <= 1,
                "total_output_tokens_matches_rows": data["total_output_tokens"] == sum(output_lens),
                "positive_duration": data["duration"] > 0,
                "positive_output_throughput": data["output_throughput"] > 0,
            }
            rates = data.get("spec_decode_per_position_acceptance_rates")
            acceptance_length = data.get("spec_decode_acceptance_length")
            if rates is not None and acceptance_length is not None:
                file_checks["acceptance_length_identity"] = abs((1.0 + sum(rates)) - acceptance_length) < 1e-5
            if not all(file_checks.values()):
                errors.append({"file": str(path.relative_to(ROOT)), "failed_checks": [k for k, v in file_checks.items() if not v]})
            total_requests += completed
            checks.append(
                {
                    "file": str(path.relative_to(ROOT)),
                    "phase": data.get("phase"),
                    "method": data.get("method_name", data.get("mode")),
                    "concurrency": data.get("concurrency"),
                    "seed": data.get("seed"),
                    "completed": completed,
                    "failed": data["failed"],
                    "output_tokens_per_request": output_lens[0] if output_lens else None,
                    "checks": file_checks,
                }
            )
        except Exception as exc:
            errors.append({"file": str(path.relative_to(ROOT)), "error": repr(exc)})
            continue
        checksum_rows.append(
            {
                "file": str(path.relative_to(ROOT)),
                "bytes": path.stat().st_size,
                "sha256": sha256(path),
            }
        )

    manifest_checks = []
    for path in sorted(PROCESSED.glob("*manifest.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        runs = data.get("runs", [])
        for run in runs:
            if run.get("status") == "completed":
                result_path = Path(run["result_path"])
                if result_path.is_absolute() and result_path.parent.parts[-2:] == ("results", "raw"):
                    result_path = RAW / result_path.name
                elif not result_path.is_absolute():
                    result_path = ROOT / result_path
                if not result_path.is_file():
                    errors.append({"manifest": path.name, "missing_result": str(result_path)})
        manifest_checks.append(
            {
                "file": path.name,
                "status": data.get("status"),
                "run_count": len(runs),
                "completed_runs": sum(r.get("status") == "completed" for r in runs),
                "failed_runs": sum(r.get("status") == "failed" for r in runs),
            }
        )

    summary_checks = []
    for phase in args.required_summaries:
        path = PROCESSED / f"{phase}-summary.json"
        if not path.exists():
            errors.append({"missing_summary": path.name})
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        summary_checks.append(
            {
                "file": path.name,
                "status": data.get("status"),
                "expected_run_count": data.get("expected_run_count"),
                "loaded_run_count": data.get("loaded_run_count"),
                "missing_files": data.get("missing_files"),
            }
        )
        if data.get("status") != "complete":
            errors.append({"incomplete_summary": path.name, "missing_files": data.get("missing_files")})

    with (PROCESSED / "raw-sha256.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["file", "bytes", "sha256"])
        writer.writeheader()
        writer.writerows(checksum_rows)

    report = {
        "schema_version": 1,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "raw_json_files": len(raw_files),
        "total_completed_requests": total_requests,
        "raw_file_checks": checks,
        "manifest_checks": manifest_checks,
        "required_summary_checks": summary_checks,
        "errors": errors,
        "status": "complete" if not errors else "failed",
        "checksum_file": "results/processed/raw-sha256.csv",
    }
    (PROCESSED / "artifact-validation.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps({key: value for key, value in report.items() if key not in {"raw_file_checks", "manifest_checks", "errors"}}, indent=2))
    print(json.dumps({"error_count": len(errors), "first_errors": errors[:5]}, indent=2))
    raise SystemExit(0 if not errors else 1)


if __name__ == "__main__":
    main()
