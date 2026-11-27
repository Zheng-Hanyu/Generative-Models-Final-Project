"""Build and run the local vLLM server and benchmark client."""
from __future__ import annotations

import fcntl
import json
import math
import os
import signal
import socket
import subprocess
import time
from collections.abc import Sequence
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from urllib.request import ProxyHandler, Request, build_opener

CAPTURE_SIZES = (1, 2, 3, 4, 6, 8, 12, 16, 20, 24, 28, 32)
HTTP = build_opener(ProxyHandler({}))


def warmup(url):
    for prompt in ('Explain how a bicycle brake works.', 'Describe what a pendulum measures.',
                   'Give two uses of a barometer.', 'How does a rechargeable battery deliver energy?'):
        body = {'model': 'qwen-fp8', 'messages': [{'role': 'user', 'content': prompt}],
                'max_tokens': 32, 'temperature': 0}
        request = Request(url + '/v1/chat/completions', data=json.dumps(body).encode(),
                          headers={'Content-Type': 'application/json'})
        with HTTP.open(request, timeout=45) as response:
            if not json.load(response)['choices']:
                raise RuntimeError('Warmup produced no choices')


def build_launch_command(args, config, capture_sizes=CAPTURE_SIZES, eagle=False):
    graph = {"decode_cudagraph_capture_request_sizes": capture_sizes}
    command = [
        args.vllm, 'serve', args.model, '--served-model-name', 'qwen-fp8',
        '--host', '127.0.0.1', '--port', str(args.port), '--language-model-only',
        '--no-enable-prefix-caching', '--generation-config', 'vllm', '--max-model-len', '4096',
        '--max-num-seqs', '32', '--max-num-batched-tokens', '4096',
        '--gpu-memory-utilization', '0.55', '--attention-backend', 'CUSTOM' if eagle else 'TRITON_ATTN',
    ]
    if eagle:
        command.extend(("--linear-backend", "flashinfer_cutedsl"))
    else:
        command.extend(("--compilation-config", json.dumps(graph)))
    if config is not None:
        command.extend(('--speculative-config', json.dumps(config, separators=(',', ':'))))
    return command


def environment(args, eagle=False):
    env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(args.gpu), HF_HUB_OFFLINE='1')
    env['NO_PROXY'] = env['no_proxy'] = '127.0.0.1,localhost'
    if args.bench_deps:
        env['PYTHONPATH'] = os.pathsep.join(filter(None, (args.bench_deps, env.get('PYTHONPATH'))))
    if eagle:
        env["VLLM_USE_V2_MODEL_RUNNER"] = "1"
    return env


def wait_for_server(process, url, timeout=360):
    deadline = time.monotonic() + timeout
    while time.monotonic() < deadline and process.poll() is None:
        try:
            with HTTP.open(url + '/v1/models', timeout=1) as response:
                if any(model['id'] == 'qwen-fp8' for model in json.load(response)['data']):
                    return
        except OSError:
            pass
        time.sleep(2)
    raise RuntimeError(f'vLLM failed to become ready (status {process.poll()})')


def terminate(signum, _frame):
    raise SystemExit(128 + signum)


@contextmanager
def reserve_gpu(args):
    lock_path = Path.home() / f".speculative-decoding-lab-gpu-{args.gpu}.lock"
    with lock_path.open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        fields = ("name", "uuid", "driver_version", "memory.used", "utilization.gpu")
        gpu = subprocess.check_output(
            ["nvidia-smi", "-i", str(args.gpu), "--query-gpu=" + ",".join(fields),
             "--format=csv,noheader,nounits"], text=True
        ).strip().split(", ")
        if int(gpu[-2]) > 512 or int(gpu[-1]) > 0:
            raise RuntimeError(f"GPU {args.gpu} is in use")
        with socket.socket() as connection:
            connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            connection.bind(("127.0.0.1", args.port))
        yield dict(zip(fields[:3], gpu[:3]))


@contextmanager
def running_server(command, env, url, log_path, timeout=900):
    with log_path.open("w", encoding="utf-8") as log:
        process = subprocess.Popen(command, env=env, stdout=log, stderr=subprocess.STDOUT, start_new_session=True)
        try:
            wait_for_server(process, url, timeout=timeout)
            yield
        finally:
            try:
                os.killpg(process.pid, signal.SIGTERM)
            except ProcessLookupError:
                pass
            try:
                process.wait(timeout=25)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()


@dataclass(frozen=True)
class BenchmarkCell:
    name: str
    seed: int
    concurrency: int
    count: int
    dataset: Sequence[str]
    input_tokens: int | list[int] | None = None
    output_tokens: int | list[int] | None = None


def spec_bench_flags(path, output_tokens):
    return ("--dataset-name", "spec_bench", "--dataset-path", str(path),
            "--spec-bench-output-len", str(output_tokens), "--no-oversample")


def prompt_flags(path, output_tokens):
    return ("--dataset-name", "speed_bench", "--dataset-path", str(path.parent),
            "--speed-bench-output-len", str(output_tokens), "--no-oversample", "--ignore-eos")


def benchmark_command(client, model, url, cell, path):
    return [
        client, "bench", "serve", "--backend", "openai", "--endpoint", "/v1/completions",
        "--base-url", url, "--model", "qwen-fp8", "--tokenizer", model, *cell.dataset,
        "--seed", str(cell.seed), "--temperature", "0", "--num-warmups", "0",
        "--ready-check-timeout-sec", "0", "--request-rate", "inf",
        "--max-concurrency", str(cell.concurrency), "--num-prompts", str(cell.count),
        "--metric-percentiles", "50,95,99", "--save-detailed", "--save-result",
        "--result-dir", str(path.parent), "--result-filename", path.name,
    ]


def measure_cell(client, model, url, cell, path, env):
    warmup(url)
    command = benchmark_command(client, model, url, cell, path)
    with path.with_suffix(".log").open("w", encoding="utf-8") as log:
        subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=300)
    result = json.loads(path.read_text(encoding="utf-8"))
    speed = result["output_throughput"]
    if (result["completed"], result["failed"]) != (cell.count, 0) or not math.isfinite(speed) or speed <= 0:
        raise RuntimeError(f"{path}: incomplete requests or invalid throughput")
    for key, tokens in (("input_lens", cell.input_tokens), ("output_lens", cell.output_tokens)):
        expected = [tokens] * cell.count if isinstance(tokens, int) else tokens
        if expected is not None and result[key] != expected:
            raise RuntimeError(f"{path}: {key} differ from the workload")
    print(f"  {path.parent.name} {cell.name}: {speed:.2f} tok/s", flush=True)
    return speed


def vllm_version(executable, env):
    output = subprocess.check_output([executable, "--version"], env=env, text=True,
                                     stderr=subprocess.DEVNULL, timeout=60)
    return output.strip().splitlines()[-1]
