#!/usr/bin/env python3
"""Run deterministic semantic smoke requests and preserve complete responses."""

import argparse
import datetime as dt
import json
from pathlib import Path
import time
import urllib.error
import urllib.request

PROMPTS = [
    {
        "id": "explanation_en",
        "prompt": "Explain speculative decoding to a computer science student in three concise paragraphs.",
    },
    {
        "id": "reasoning_math",
        "prompt": "A training job processes 2400 samples in 75 seconds. At the same rate, how many samples does it process in 5 minutes? Show the calculation and final answer.",
    },
    {
        "id": "code_python",
        "prompt": "Write a Python function moving_average(values, window) that returns the arithmetic mean of each contiguous window. Include input validation and two usage examples.",
    },
    {
        "id": "explanation_zh",
        "prompt": "请用中文解释为什么大语言模型自回归解码通常受显存带宽限制，并说明投机解码为什么可能降低延迟。",
    },
]


def utc_now():
    return dt.datetime.now(dt.timezone.utc).isoformat()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--base-url", required=True)
    parser.add_argument("--model", default="qwen-target")
    parser.add_argument("--max-tokens", type=int, default=96)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    result = {
        "schema_version": 1,
        "started_at": utc_now(),
        "base_url": args.base_url,
        "model": args.model,
        "sampling": {
            "temperature": 0.0,
            "top_p": 1.0,
            "top_k": -1,
            "seed": 0,
            "max_tokens": args.max_tokens,
            "return_token_ids": True,
        },
        "requests": [],
    }
    endpoint = args.base_url.rstrip("/") + "/v1/completions"
    for item in PROMPTS:
        payload = {
            "model": args.model,
            "prompt": item["prompt"],
            **result["sampling"],
        }
        record = {"id": item["id"], "prompt": item["prompt"], "request": payload}
        request = urllib.request.Request(
            endpoint,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        started = time.perf_counter()
        record["started_at"] = utc_now()
        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                record["http_status"] = response.status
                record["response"] = json.loads(response.read().decode("utf-8"))
            record["success"] = True
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            record["success"] = False
            record["error"] = repr(exc)
        record["latency_seconds"] = time.perf_counter() - started
        result["requests"].append(record)
        print(
            f"{item['id']}: success={record['success']} "
            f"latency={record['latency_seconds']:.3f}s",
            flush=True,
        )

    result["finished_at"] = utc_now()
    result["all_succeeded"] = all(item["success"] for item in result["requests"])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(f"Saved {args.output}")
    return 0 if result["all_succeeded"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
