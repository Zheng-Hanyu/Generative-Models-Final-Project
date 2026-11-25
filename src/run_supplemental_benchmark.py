#!/usr/bin/env python3
"""Serve or benchmark the selected supplemental decoding configuration."""

import argparse
import fcntl
import json
import os
import random
import signal
import socket
import subprocess
import time
from collections import defaultdict
from pathlib import Path
from urllib.request import ProxyHandler, Request, build_opener


ROOT = Path(__file__).resolve().parents[1]
DATASET = ROOT / 'data/spec_bench/question.jsonl'
CONFIG = ROOT / 'config/supplemental_speculative_config.json'
SEEDS = (43, 44, 45)
CONCURRENCIES = (1, 16)
HTTP = build_opener(ProxyHandler({}))


def split_holdout(directory):
    strata = defaultdict(list)
    for line in DATASET.read_text(encoding='utf-8').splitlines():
        row = json.loads(line)
        strata[row['category']].append(row)
    rng = random.Random(20261125)
    holdout = []
    for rows in strata.values():
        rng.shuffle(rows)
        holdout.extend(rows[round(0.30 * len(rows)):])

    directory.mkdir()
    cell_count = len(SEEDS) * len(CONCURRENCIES)
    for index in range(cell_count):
        seed = SEEDS[index // len(CONCURRENCIES)]
        concurrency = CONCURRENCIES[index % len(CONCURRENCIES)]
        rows = holdout[index::cell_count]
        path = directory / f'holdout-c{concurrency}-s{seed}.jsonl'
        path.write_text(''.join(json.dumps(row, ensure_ascii=False) + '\n' for row in rows),
                        encoding='utf-8')


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


def launch_command(args, speculative=True):
    config = json.loads(CONFIG.read_text(encoding='utf-8')) if speculative else None
    return build_launch_command(args, config, [1, 2, 4, 8, 16, 24, 32])


def build_launch_command(args, config, capture_sizes):
    graph = {'decode_cudagraph_capture_request_sizes': capture_sizes}
    command = [
        args.vllm, 'serve', args.model, '--served-model-name', 'qwen-fp8',
        '--host', '127.0.0.1', '--port', str(args.port), '--language-model-only',
        '--no-enable-prefix-caching', '--generation-config', 'vllm', '--max-model-len', '4096',
        '--max-num-seqs', '32', '--max-num-batched-tokens', '4096',
        '--gpu-memory-utilization', '0.55', '--compilation-config', json.dumps(graph),
        '--attention-backend', 'TRITON_ATTN',
    ]
    if config is not None:
        command.extend(('--speculative-config', json.dumps(config, separators=(',', ':'))))
    return command


def environment(args):
    env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(args.gpu), HF_HUB_OFFLINE='1')
    env['NO_PROXY'] = env['no_proxy'] = '127.0.0.1,localhost'
    if args.bench_deps:
        env['PYTHONPATH'] = os.pathsep.join(filter(None, (args.bench_deps, env.get('PYTHONPATH'))))
    return env


def wait_for_server(process, url):
    deadline = time.monotonic() + 360
    while time.monotonic() < deadline and process.poll() is None:
        try:
            with HTTP.open(url + '/v1/models', timeout=1) as response:
                if any(model['id'] == 'qwen-fp8' for model in json.load(response)['data']):
                    return
        except OSError:
            pass
        time.sleep(2)
    raise RuntimeError(f'vLLM failed to become ready (status {process.poll()})')


def benchmark(args, url, env, directory, seed, concurrency, count):
    name = f'holdout-c{concurrency}-s{seed}'
    path = directory / f'{name}.json'
    warmup(url)
    command = [
        args.vllm, 'bench', 'serve', '--backend', 'openai', '--endpoint', '/v1/completions',
        '--base-url', url, '--model', 'qwen-fp8', '--tokenizer', args.model,
        '--dataset-name', 'spec_bench', '--dataset-path', str(args.output.resolve() / 'workloads' / f'{name}.jsonl'),
        '--spec-bench-output-len', '128', '--seed', str(seed), '--temperature', '0',
        '--num-warmups', '0', '--ready-check-timeout-sec', '0', '--no-oversample',
        '--request-rate', 'inf', '--max-concurrency', str(concurrency),
        '--num-prompts', str(count), '--metric-percentiles', '50,95,99',
        '--save-detailed', '--save-result', '--result-dir', str(directory), '--result-filename', path.name,
    ]
    with (directory / f'{name}.log').open('w') as log:
        subprocess.run(command, env=env, stdout=log, stderr=subprocess.STDOUT, check=True, timeout=300)
    result = json.loads(path.read_text())
    speed = result['output_throughput']
    if result['completed'] != count or result['failed'] or speed <= 0:
        raise RuntimeError(f'{name}: incomplete requests or zero output throughput; see {path}')
    print(f'{directory.name} seed {seed} C={concurrency}: {count}/{count}, {speed:.2f} tok/s', flush=True)


def replay(args, env, label, speculative):
    directory = args.output.resolve() / label
    directory.mkdir()
    url = f'http://127.0.0.1:{args.port}'
    with (directory / 'server.log').open('w') as log:
        process = subprocess.Popen(launch_command(args, speculative), env=env, stdout=log,
                                   stderr=subprocess.STDOUT, start_new_session=True)
        try:
            wait_for_server(process, url)
            seeds = SEEDS[:1] if args.action == 'smoke' else SEEDS
            concurrencies = CONCURRENCIES[:1] if args.action == 'smoke' else CONCURRENCIES
            count = 4 if args.action == 'smoke' else 48
            for seed in seeds:
                for concurrency in concurrencies:
                    benchmark(args, url, env, directory, seed, concurrency, count)
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


def terminate(signum, _frame):
    raise SystemExit(128 + signum)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=('serve', 'benchmark', 'smoke'))
    parser.add_argument('--gpu', type=int, required=True)
    parser.add_argument('--port', type=int, required=True)
    parser.add_argument('--output', type=Path)
    parser.add_argument('--vllm', default='/home/genai/.pixi/envs/default/bin/vllm')
    parser.add_argument('--model', default='/home/model/Qwen3.8-27B-FP8')
    parser.add_argument('--bench-deps', default='')
    args = parser.parse_args()
    env = environment(args)
    if args.action == 'serve':
        command = launch_command(args)
        os.execvpe(command[0], command, env)
    if args.output is None:
        parser.error('--output is required for benchmark or smoke')
    signal.signal(signal.SIGTERM, terminate)
    with (Path.home() / f'.speculative-decoding-lab-gpu-{args.gpu}.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        used, utilization = subprocess.check_output(
            ['nvidia-smi', '-i', str(args.gpu), '--query-gpu=memory.used,utilization.gpu',
             '--format=csv,noheader,nounits'], text=True
        ).strip().split(',')
        if int(used) > 512 or int(utilization) > 0:
            raise RuntimeError(f'GPU {args.gpu} is already in use')
        with socket.socket() as connection:
            connection.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            connection.bind(('127.0.0.1', args.port))
        args.output.mkdir(parents=True)
        split_holdout(args.output / 'workloads')
        runs = [('selected', True)]
        if args.action == 'benchmark':
            runs.append(('baseline', False))
        if args.gpu % 2:
            runs.reverse()
        for label, speculative in runs:
            replay(args, env, label, speculative)


if __name__ == '__main__':
    main()
