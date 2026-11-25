# 完整命令审计

本文件由 `logs/commands.jsonl` 自动导出。每次命令的完整标准输出与标准错误保留在所链接的日志中；基准请求的原始指标保存在 `results/raw/`。

## 1. 001-environment

- 状态：completed；退出码：0
- 开始：2026-11-24T14:05:00.364794+00:00
- 结束：2026-11-24T14:05:00.754431+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[001-environment.log](/home/genai/spec_decoding_study/logs/commands/001-environment.log)

```bash
bash -lc 'uname -a; python --version; command -v python; python -c "import importlib.metadata as m; print(\"vLLM:\",m.version(\"vllm\")); print(\"Torch:\",m.version(\"torch\")); print(\"Transformers:\",m.version(\"transformers\"))"; nvidia-smi --query-gpu=index,name,memory.total,memory.used,driver_version --format=csv,noheader; free -h; df -h /home/genai; git -C /home/genai/vllm rev-parse HEAD; git -C /home/genai/vllm status --short --branch; command -v uv || true; ls -l /home/genai/.local/bin/uv /usr/local/bin/uv /usr/bin/uv 2>/dev/null || true; python -m uv --version 2>/dev/null || true'
```

## 2. 002-model-inventory

- 状态：completed；退出码：0
- 开始：2026-11-24T14:05:01.003625+00:00
- 结束：2026-11-24T14:05:05.157332+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[002-model-inventory.log](/home/genai/spec_decoding_study/logs/commands/002-model-inventory.log)

```bash
python /home/genai/spec_decoding_study/bin/inspect_models.py
```

## 3. 003-model-recipe

- 状态：failed；退出码：127
- 开始：2026-11-24T14:05:05.558311+00:00
- 结束：2026-11-24T14:05:06.276992+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[003-model-recipe.log](/home/genai/spec_decoding_study/logs/commands/003-model-recipe.log)

```bash
bash -lc 'curl -fsSL https://recipes.vllm.ai/Qwen/Qwen3.8-27B-FP8.json -o /home/genai/spec_decoding_study/config/qwen3.8-27b-fp8-recipe.json && /home/genai/vllm/.agents/skills/model-recipes/scripts/read_recipe.sh /home/genai/spec_decoding_study/config/qwen3.8-27b-fp8-recipe.json'
```

## 4. 004-install-uv

- 状态：completed；退出码：0
- 开始：2026-11-24T14:05:47.857099+00:00
- 结束：2026-11-24T14:05:57.734651+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[004-install-uv.log](/home/genai/spec_decoding_study/logs/commands/004-install-uv.log)

```bash
zsh -c 'curl -LsSf https://astral.sh/uv/install.sh | sh'
```

## 5. 005-pixi-environment

- 状态：completed；退出码：0
- 开始：2026-11-24T14:05:58.021405+00:00
- 结束：2026-11-24T14:06:13.071525+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[005-pixi-environment.log](/home/genai/spec_decoding_study/logs/commands/005-pixi-environment.log)

```bash
zsh -c '/home/genai/.pixi/envs/default/bin/python --version; /home/genai/.pixi/envs/default/bin/python -c "import importlib.metadata as m; print(\"vLLM:\",m.version(\"vllm\")); print(\"Torch:\",m.version(\"torch\")); print(\"Transformers:\",m.version(\"transformers\"))"; /home/genai/.pixi/envs/default/bin/vllm --version; nvidia-smi --query-gpu=index,name,memory.total,memory.used,driver_version --format=csv,noheader'
```

## 6. 006-create-vllm-venv

- 状态：completed；退出码：0
- 开始：2026-11-24T14:06:40.920566+00:00
- 结束：2026-11-24T14:07:00.767384+00:00
- 工作目录：`/home/genai/vllm`
- 输出日志：[006-create-vllm-venv.log](/home/genai/spec_decoding_study/logs/commands/006-create-vllm-venv.log)

```bash
/home/genai/.local/bin/uv venv --python 3.14
```

## 7. 007-vllm-dev-install

- 状态：stopped；退出码：None
- 开始：2026-11-24T14:07:32.026291+00:00
- 结束：None
- 工作目录：`/home/genai/vllm`
- 输出日志：[007-vllm-dev-install.log](/home/genai/spec_decoding_study/logs/commands/007-vllm-dev-install.log)

```bash
zsh -c '/home/genai/.local/bin/uv pip install -r requirements/lint.txt && .venv/bin/pre-commit install && VLLM_USE_PRECOMPILED=1 /home/genai/.local/bin/uv pip install -e . --torch-backend=auto'
```

## 8. 008-b200-recipe

- 状态：completed；退出码：0
- 开始：2026-11-24T14:07:32.241291+00:00
- 结束：2026-11-24T14:07:33.017614+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[008-b200-recipe.log](/home/genai/spec_decoding_study/logs/commands/008-b200-recipe.log)

```bash
zsh -c 'curl -fsSL https://recipes.vllm.ai/Qwen/Qwen3.8-27B-FP8/hw/b200.json -o /home/genai/spec_decoding_study/config/qwen3.8-27b-fp8-b200.json && /home/genai/.pixi/envs/default/bin/python -c "import json; d=json.load(open(\"/home/genai/spec_decoding_study/config/qwen3.8-27b-fp8-b200.json\")); print(json.dumps(d,indent=2))"'
```

## 9. 009-installed-serve-help

- 状态：completed；退出码：0
- 开始：2026-11-24T14:08:19.901547+00:00
- 结束：2026-11-24T14:08:27.157007+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[009-installed-serve-help.log](/home/genai/spec_decoding_study/logs/commands/009-installed-serve-help.log)

```bash
zsh -c '/home/genai/.pixi/envs/default/bin/vllm serve --help > /home/genai/spec_decoding_study/config/installed-vllm-serve-help.txt'
```

## 10. 010-installed-bench-help

- 状态：completed；退出码：0
- 开始：2026-11-24T14:08:27.443313+00:00
- 结束：2026-11-24T14:08:35.072139+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[010-installed-bench-help.log](/home/genai/spec_decoding_study/logs/commands/010-installed-bench-help.log)

```bash
zsh -c '/home/genai/.pixi/envs/default/bin/vllm bench serve --help > /home/genai/spec_decoding_study/config/installed-vllm-bench-serve-help.txt'
```

## 11. 008-vllm-serve-help-all

- 状态：completed；退出码：0
- 开始：2026-11-24T14:12:45.823984+00:00
- 结束：2026-11-24T14:12:52.645853+00:00
- 工作目录：`/home/genai/vllm`
- 输出日志：[008-vllm-serve-help-all.log](/home/genai/spec_decoding_study/logs/commands/008-vllm-serve-help-all.log)

```bash
/bin/sh -c 'CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm serve --help=all > /home/genai/spec_decoding_study/config/installed-vllm-serve-help-all.txt'
```

## 12. 009-vllm-bench-help-all

- 状态：completed；退出码：0
- 开始：2026-11-24T14:12:52.855099+00:00
- 结束：2026-11-24T14:13:00.017842+00:00
- 工作目录：`/home/genai/vllm`
- 输出日志：[009-vllm-bench-help-all.log](/home/genai/spec_decoding_study/logs/commands/009-vllm-bench-help-all.log)

```bash
/bin/sh -c 'CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --help=all > /home/genai/spec_decoding_study/config/installed-vllm-bench-serve-help-all.txt'
```

## 13. 010-gpu-preflight

- 状态：completed；退出码：0
- 开始：2026-11-24T14:13:00.241025+00:00
- 结束：2026-11-24T14:13:00.371825+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[010-gpu-preflight.log](/home/genai/spec_decoding_study/logs/commands/010-gpu-preflight.log)

```bash
/usr/bin/nvidia-smi --query-gpu=index,name,uuid,memory.total,memory.used,utilization.gpu --format=csv,noheader
```

## 14. 011-server-normal-smoke

- 状态：failed；退出码：1
- 开始：2026-11-24T14:15:10.755861+00:00
- 结束：2026-11-24T14:15:19.559283+00:00
- 工作目录：`/home/genai/vllm`
- 输出日志：[011-server-normal-smoke.log](/home/genai/spec_decoding_study/logs/commands/011-server-normal-smoke.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8000 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --seed 0
```

## 15. 012-server-normal-smoke-installed

- 状态：completed；退出码：0
- 开始：2026-11-24T14:15:47.832086+00:00
- 结束：2026-11-24T14:26:39.386329+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[012-server-normal-smoke-installed.log](/home/genai/spec_decoding_study/logs/commands/012-server-normal-smoke-installed.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8000 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --seed 0
```

## 16. 013-server-mtp-k3-smoke-installed

- 状态：completed；退出码：0
- 开始：2026-11-24T14:18:29.049338+00:00
- 结束：2026-11-24T14:26:39.659152+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[013-server-mtp-k3-smoke-installed.log](/home/genai/spec_decoding_study/logs/commands/013-server-mtp-k3-smoke-installed.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8001 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --seed 0 --speculative-config '{"method":"mtp","num_speculative_tokens":3}'
```

## 17. 014-server-dspark-k7-smoke-installed

- 状态：completed；退出码：0
- 开始：2026-11-24T14:18:29.257289+00:00
- 结束：2026-11-24T14:26:40.260586+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[014-server-dspark-k7-smoke-installed.log](/home/genai/spec_decoding_study/logs/commands/014-server-dspark-k7-smoke-installed.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8002 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --seed 0 --speculative-config '{"method":"dspark","model":"/home/genai/models/Qwen3.8-27B-DSpark-vLLM","num_speculative_tokens":7}'
```

## 18. 015-download-speed-bench-preparer

- 状态：completed；退出码：0
- 开始：2026-11-24T14:19:23.833716+00:00
- 结束：2026-11-24T14:19:28.618300+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[015-download-speed-bench-preparer.log](/home/genai/spec_decoding_study/logs/commands/015-download-speed-bench-preparer.log)

```bash
/usr/bin/curl -fsSL https://raw.githubusercontent.com/NVIDIA-NeMo/Skills/refs/heads/main/nemo_skills/dataset/speed-bench/prepare.py -o /home/genai/spec_decoding_study/config/prepare_speed_bench.py
```

## 19. 016-smoke-normal-installed

- 状态：completed；退出码：0
- 开始：2026-11-24T14:20:40.452750+00:00
- 结束：2026-11-24T14:20:44.040222+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[016-smoke-normal-installed.log](/home/genai/spec_decoding_study/logs/commands/016-smoke-normal-installed.log)

```bash
/home/genai/.pixi/envs/default/bin/python src/smoke_generate.py --base-url http://127.0.0.1:8000 --output results/raw/smoke-normal-installed.json
```

## 20. 017-bench-normal-random-c1-exploratory

- 状态：completed；退出码：0
- 开始：2026-11-24T14:21:08.183676+00:00
- 结束：2026-11-24T14:21:27.448577+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[017-bench-normal-random-c1-exploratory.log](/home/genai/spec_decoding_study/logs/commands/017-bench-normal-random-c1-exploratory.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8000 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 128 --random-range-ratio 0 --num-prompts 8 --num-warmups 2 --max-concurrency 1 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --seed 0 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename exploratory-normal-random-i1024-o128-c1.json --metadata mode=normal k=0 gpu=0 phase=exploratory --disable-tqdm
```

## 21. 018-smoke-mtp-k3-installed

- 状态：completed；退出码：0
- 开始：2026-11-24T14:23:53.451927+00:00
- 结束：2026-11-24T14:23:55.087380+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[018-smoke-mtp-k3-installed.log](/home/genai/spec_decoding_study/logs/commands/018-smoke-mtp-k3-installed.log)

```bash
/home/genai/.pixi/envs/default/bin/python src/smoke_generate.py --base-url http://127.0.0.1:8001 --output results/raw/smoke-mtp-k3-installed.json
```

## 22. 019-smoke-dspark-k7-installed

- 状态：completed；退出码：0
- 开始：2026-11-24T14:23:55.344724+00:00
- 结束：2026-11-24T14:23:57.012166+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[019-smoke-dspark-k7-installed.log](/home/genai/spec_decoding_study/logs/commands/019-smoke-dspark-k7-installed.log)

```bash
/home/genai/.pixi/envs/default/bin/python src/smoke_generate.py --base-url http://127.0.0.1:8002 --output results/raw/smoke-dspark-k7-installed.json
```

## 23. 020-bench-mtp-k3-random-c1-exploratory

- 状态：completed；退出码：0
- 开始：2026-11-24T14:24:32.965663+00:00
- 结束：2026-11-24T14:24:45.343103+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[020-bench-mtp-k3-random-c1-exploratory.log](/home/genai/spec_decoding_study/logs/commands/020-bench-mtp-k3-random-c1-exploratory.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8001 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 128 --random-range-ratio 0 --num-prompts 8 --num-warmups 2 --max-concurrency 1 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --seed 0 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename exploratory-mtp-k3-random-i1024-o128-c1.json --metadata mode=mtp k=3 gpu=1 phase=exploratory --disable-tqdm
```

## 24. 021-bench-dspark-k7-random-c1-exploratory

- 状态：completed；退出码：0
- 开始：2026-11-24T14:24:45.583125+00:00
- 结束：2026-11-24T14:24:58.796554+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[021-bench-dspark-k7-random-c1-exploratory.log](/home/genai/spec_decoding_study/logs/commands/021-bench-dspark-k7-random-c1-exploratory.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8002 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 128 --random-range-ratio 0 --num-prompts 8 --num-warmups 2 --max-concurrency 1 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --seed 0 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename exploratory-dspark-k7-random-i1024-o128-c1.json --metadata mode=dspark k=7 gpu=2 phase=exploratory --disable-tqdm
```

## 25. 022-compare-smoke-greedy

- 状态：failed；退出码：2
- 开始：2026-11-24T14:26:13.578762+00:00
- 结束：2026-11-24T14:26:13.604927+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[022-compare-smoke-greedy.log](/home/genai/spec_decoding_study/logs/commands/022-compare-smoke-greedy.log)

```bash
/home/genai/.pixi/envs/default/bin/python src/compare_smoke.py --reference normal --input normal=results/raw/smoke-normal-installed.json --input mtp_k3=results/raw/smoke-mtp-k3-installed.json --input dspark_k7=results/raw/smoke-dspark-k7-installed.json --output results/processed/smoke-greedy-consistency.json
```

## 26. 023-stop-normal-smoke

- 状态：failed；退出码：1
- 开始：2026-11-24T14:26:36.903295+00:00
- 结束：2026-11-24T14:26:36.932861+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[023-stop-normal-smoke.log](/home/genai/spec_decoding_study/logs/commands/023-stop-normal-smoke.log)

```bash
/home/genai/.pixi/envs/default/bin/python bin/stop_logged.py --label 012-server-normal-smoke-installed --expect vllm --expect 8000
```

## 27. 024-stop-mtp-smoke

- 状态：failed；退出码：1
- 开始：2026-11-24T14:26:37.134847+00:00
- 结束：2026-11-24T14:26:37.159642+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[024-stop-mtp-smoke.log](/home/genai/spec_decoding_study/logs/commands/024-stop-mtp-smoke.log)

```bash
/home/genai/.pixi/envs/default/bin/python bin/stop_logged.py --label 013-server-mtp-k3-smoke-installed --expect vllm --expect 8001
```

## 28. 025-stop-dspark-smoke

- 状态：failed；退出码：1
- 开始：2026-11-24T14:26:37.326154+00:00
- 结束：2026-11-24T14:26:37.351767+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[025-stop-dspark-smoke.log](/home/genai/spec_decoding_study/logs/commands/025-stop-dspark-smoke.log)

```bash
/home/genai/.pixi/envs/default/bin/python bin/stop_logged.py --label 014-server-dspark-k7-smoke-installed --expect vllm --expect 8002
```

## 29. 026-stop-script-idempotence-check

- 状态：completed；退出码：0
- 开始：2026-11-24T14:27:12.697363+00:00
- 结束：2026-11-24T14:27:12.722090+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[026-stop-script-idempotence-check.log](/home/genai/spec_decoding_study/logs/commands/026-stop-script-idempotence-check.log)

```bash
/home/genai/.pixi/envs/default/bin/python bin/stop_logged.py --label 012-server-normal-smoke-installed --expect vllm --expect 8000
```

## 30. 027-server-formal-normal-gpu0

- 状态：completed；退出码：0
- 开始：2026-11-24T14:27:42.531191+00:00
- 结束：2026-11-24T15:14:29.498820+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[027-server-formal-normal-gpu0.log](/home/genai/spec_decoding_study/logs/commands/027-server-formal-normal-gpu0.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8100 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0
```

## 31. 028-server-formal-mtp-k3-gpu1

- 状态：completed；退出码：0
- 开始：2026-11-24T14:27:42.799972+00:00
- 结束：2026-11-24T15:04:15.724218+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[028-server-formal-mtp-k3-gpu1.log](/home/genai/spec_decoding_study/logs/commands/028-server-formal-mtp-k3-gpu1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8101 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"mtp","num_speculative_tokens":3}'
```

## 32. 029-server-formal-dspark-k7-gpu2

- 状态：completed；退出码：0
- 开始：2026-11-24T14:27:43.018847+00:00
- 结束：2026-11-24T15:12:18.530324+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[029-server-formal-dspark-k7-gpu2.log](/home/genai/spec_decoding_study/logs/commands/029-server-formal-dspark-k7-gpu2.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8102 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"dspark","model":"/home/genai/models/Qwen3.8-27B-DSpark-vLLM","num_speculative_tokens":7}'
```

## 33. 030-experiment-scripts-syntax-check

- 状态：completed；退出码：0
- 开始：2026-11-24T14:30:33.289042+00:00
- 结束：2026-11-24T14:30:33.317932+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[030-experiment-scripts-syntax-check.log](/home/genai/spec_decoding_study/logs/commands/030-experiment-scripts-syntax-check.log)

```bash
/home/genai/.pixi/envs/default/bin/python -m py_compile bin/run_logged.py bin/launch_detached.py bin/stop_logged.py src/smoke_generate.py src/compare_smoke.py src/run_benchmark_matrix.py
```

## 34. 031-gpu-monitor-formal-r1

- 状态：stopped；退出码：None
- 开始：2026-11-24T14:31:17.202281+00:00
- 结束：None
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[031-gpu-monitor-formal-r1.log](/home/genai/spec_decoding_study/logs/commands/031-gpu-monitor-formal-r1.log)

```bash
/home/genai/.pixi/envs/default/bin/python src/monitor_gpus.py --output results/raw/gpu-timeseries-formal-r1.csv --interval 5 --devices 0,1,2,3
```

## 35. 032-matrix-formal-normal-gpu0

- 状态：completed；退出码：0
- 开始：2026-11-24T14:31:31.216334+00:00
- 结束：2026-11-24T15:13:34.458677+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[032-matrix-formal-normal-gpu0.log](/home/genai/spec_decoding_study/logs/commands/032-matrix-formal-normal-gpu0.log)

```bash
/home/genai/.pixi/envs/default/bin/python src/run_benchmark_matrix.py --method normal --port 8100 --gpu 0 --phase formal-r1 --vllm /home/genai/.pixi/envs/default/bin/vllm
```

## 36. warmup-formal-r1-normal-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T14:31:31.285651+00:00
- 结束：2026-11-24T14:31:46.460582+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-formal-r1-normal-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-formal-r1-normal-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-formal-r1-normal-c32-
```

## 37. 033-matrix-formal-mtp-k3-gpu1

- 状态：completed；退出码：0
- 开始：2026-11-24T14:31:31.469785+00:00
- 结束：2026-11-24T14:49:16.454011+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[033-matrix-formal-mtp-k3-gpu1.log](/home/genai/spec_decoding_study/logs/commands/033-matrix-formal-mtp-k3-gpu1.log)

```bash
/home/genai/.pixi/envs/default/bin/python src/run_benchmark_matrix.py --method mtp-k3 --port 8101 --gpu 1 --phase formal-r1 --vllm /home/genai/.pixi/envs/default/bin/vllm
```

## 38. warmup-formal-r1-mtp-k3-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T14:31:31.538003+00:00
- 结束：2026-11-24T14:31:43.906453+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-formal-r1-mtp-k3-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-formal-r1-mtp-k3-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-formal-r1-mtp-k3-c32-
```

## 39. 034-matrix-formal-dspark-k7-gpu2

- 状态：completed；退出码：0
- 开始：2026-11-24T14:31:31.674170+00:00
- 结束：2026-11-24T14:56:12.777153+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[034-matrix-formal-dspark-k7-gpu2.log](/home/genai/spec_decoding_study/logs/commands/034-matrix-formal-dspark-k7-gpu2.log)

```bash
/home/genai/.pixi/envs/default/bin/python src/run_benchmark_matrix.py --method dspark-k7 --port 8102 --gpu 2 --phase formal-r1 --vllm /home/genai/.pixi/envs/default/bin/vllm
```

## 40. warmup-formal-r1-dspark-k7-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T14:31:31.751033+00:00
- 结束：2026-11-24T14:32:19.144732+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-formal-r1-dspark-k7-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-formal-r1-dspark-k7-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-formal-r1-dspark-k7-c32-
```

## 41. formal-r1-mtp-k3-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:31:43.939930+00:00
- 结束：2026-11-24T14:32:09.813867+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-mtp-k3-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-mtp-k3-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix formal-r1-mtp-k3-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-mtp-k3-i1024-o512-c32-s42.json --metadata mode=mtp k=3 gpu=1 phase=formal-r1 concurrency=32 seed=42 prefix_cache=false
```

## 42. formal-r1-normal-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:31:46.493634+00:00
- 结束：2026-11-24T14:32:22.808765+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-normal-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-normal-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix formal-r1-normal-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-normal-i1024-o512-c32-s42.json --metadata mode=normal k=0 gpu=0 phase=formal-r1 concurrency=32 seed=42 prefix_cache=false
```

## 43. formal-r1-mtp-k3-i1024-o512-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T14:32:09.848705+00:00
- 结束：2026-11-24T14:32:34.481234+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-mtp-k3-i1024-o512-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-mtp-k3-i1024-o512-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix formal-r1-mtp-k3-i1024-o512-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-mtp-k3-i1024-o512-c32-s43.json --metadata mode=mtp k=3 gpu=1 phase=formal-r1 concurrency=32 seed=43 prefix_cache=false
```

## 44. formal-r1-dspark-k7-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:32:19.174058+00:00
- 结束：2026-11-24T14:32:55.291421+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-dspark-k7-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-dspark-k7-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix formal-r1-dspark-k7-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-dspark-k7-i1024-o512-c32-s42.json --metadata mode=dspark k=7 gpu=2 phase=formal-r1 concurrency=32 seed=42 prefix_cache=false
```

## 45. formal-r1-normal-i1024-o512-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T14:32:22.853849+00:00
- 结束：2026-11-24T14:32:59.293869+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-normal-i1024-o512-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-normal-i1024-o512-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix formal-r1-normal-i1024-o512-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-normal-i1024-o512-c32-s43.json --metadata mode=normal k=0 gpu=0 phase=formal-r1 concurrency=32 seed=43 prefix_cache=false
```

## 46. formal-r1-mtp-k3-i1024-o512-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T14:32:34.515371+00:00
- 结束：2026-11-24T14:32:58.971545+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-mtp-k3-i1024-o512-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-mtp-k3-i1024-o512-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix formal-r1-mtp-k3-i1024-o512-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-mtp-k3-i1024-o512-c32-s44.json --metadata mode=mtp k=3 gpu=1 phase=formal-r1 concurrency=32 seed=44 prefix_cache=false
```

## 47. formal-r1-dspark-k7-i1024-o512-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T14:32:55.327073+00:00
- 结束：2026-11-24T14:33:32.376852+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-dspark-k7-i1024-o512-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-dspark-k7-i1024-o512-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix formal-r1-dspark-k7-i1024-o512-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-dspark-k7-i1024-o512-c32-s43.json --metadata mode=dspark k=7 gpu=2 phase=formal-r1 concurrency=32 seed=43 prefix_cache=false
```

## 48. warmup-formal-r1-mtp-k3-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T14:32:59.005961+00:00
- 结束：2026-11-24T14:33:10.673877+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-formal-r1-mtp-k3-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-formal-r1-mtp-k3-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-formal-r1-mtp-k3-c16-
```

## 49. formal-r1-normal-i1024-o512-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T14:32:59.339128+00:00
- 结束：2026-11-24T14:33:35.603667+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-normal-i1024-o512-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-normal-i1024-o512-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix formal-r1-normal-i1024-o512-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-normal-i1024-o512-c32-s44.json --metadata mode=normal k=0 gpu=0 phase=formal-r1 concurrency=32 seed=44 prefix_cache=false
```

## 50. formal-r1-mtp-k3-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:33:10.703492+00:00
- 结束：2026-11-24T14:33:46.444980+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-mtp-k3-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-mtp-k3-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix formal-r1-mtp-k3-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-mtp-k3-i1024-o512-c16-s42.json --metadata mode=mtp k=3 gpu=1 phase=formal-r1 concurrency=16 seed=42 prefix_cache=false
```

## 51. formal-r1-dspark-k7-i1024-o512-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T14:33:32.412941+00:00
- 结束：2026-11-24T14:34:07.370946+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-dspark-k7-i1024-o512-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-dspark-k7-i1024-o512-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix formal-r1-dspark-k7-i1024-o512-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-dspark-k7-i1024-o512-c32-s44.json --metadata mode=dspark k=7 gpu=2 phase=formal-r1 concurrency=32 seed=44 prefix_cache=false
```

## 52. warmup-formal-r1-normal-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T14:33:35.646762+00:00
- 结束：2026-11-24T14:33:49.182259+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-formal-r1-normal-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-formal-r1-normal-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-formal-r1-normal-c16-
```

## 53. formal-r1-mtp-k3-i1024-o512-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T14:33:46.478586+00:00
- 结束：2026-11-24T14:34:22.221935+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-mtp-k3-i1024-o512-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-mtp-k3-i1024-o512-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix formal-r1-mtp-k3-i1024-o512-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-mtp-k3-i1024-o512-c16-s43.json --metadata mode=mtp k=3 gpu=1 phase=formal-r1 concurrency=16 seed=43 prefix_cache=false
```

## 54. formal-r1-normal-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:33:49.211330+00:00
- 结束：2026-11-24T14:34:43.010114+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-normal-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-normal-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix formal-r1-normal-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-normal-i1024-o512-c16-s42.json --metadata mode=normal k=0 gpu=0 phase=formal-r1 concurrency=16 seed=42 prefix_cache=false
```

## 55. warmup-formal-r1-dspark-k7-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T14:34:07.406082+00:00
- 结束：2026-11-24T14:34:23.287121+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-formal-r1-dspark-k7-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-formal-r1-dspark-k7-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-formal-r1-dspark-k7-c16-
```

## 56. formal-r1-mtp-k3-i1024-o512-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T14:34:22.256708+00:00
- 结束：2026-11-24T14:34:57.352045+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-mtp-k3-i1024-o512-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-mtp-k3-i1024-o512-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix formal-r1-mtp-k3-i1024-o512-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-mtp-k3-i1024-o512-c16-s44.json --metadata mode=mtp k=3 gpu=1 phase=formal-r1 concurrency=16 seed=44 prefix_cache=false
```

## 57. formal-r1-dspark-k7-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:34:23.316569+00:00
- 结束：2026-11-24T14:35:06.232048+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-dspark-k7-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-dspark-k7-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix formal-r1-dspark-k7-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-dspark-k7-i1024-o512-c16-s42.json --metadata mode=dspark k=7 gpu=2 phase=formal-r1 concurrency=16 seed=42 prefix_cache=false
```

## 58. formal-r1-normal-i1024-o512-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T14:34:43.052726+00:00
- 结束：2026-11-24T14:35:36.635026+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-normal-i1024-o512-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-normal-i1024-o512-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix formal-r1-normal-i1024-o512-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-normal-i1024-o512-c16-s43.json --metadata mode=normal k=0 gpu=0 phase=formal-r1 concurrency=16 seed=43 prefix_cache=false
```

## 59. warmup-formal-r1-mtp-k3-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T14:34:57.386438+00:00
- 结束：2026-11-24T14:35:07.707823+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-formal-r1-mtp-k3-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-formal-r1-mtp-k3-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-formal-r1-mtp-k3-c4-
```

## 60. formal-r1-dspark-k7-i1024-o512-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T14:35:06.267764+00:00
- 结束：2026-11-24T14:35:53.043037+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-dspark-k7-i1024-o512-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-dspark-k7-i1024-o512-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix formal-r1-dspark-k7-i1024-o512-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-dspark-k7-i1024-o512-c16-s43.json --metadata mode=dspark k=7 gpu=2 phase=formal-r1 concurrency=16 seed=43 prefix_cache=false
```

## 61. formal-r1-mtp-k3-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:35:07.737496+00:00
- 结束：2026-11-24T14:36:16.069767+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-mtp-k3-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-mtp-k3-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix formal-r1-mtp-k3-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-mtp-k3-i1024-o512-c4-s42.json --metadata mode=mtp k=3 gpu=1 phase=formal-r1 concurrency=4 seed=42 prefix_cache=false
```

## 62. formal-r1-normal-i1024-o512-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T14:35:36.678628+00:00
- 结束：2026-11-24T14:36:30.461197+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-normal-i1024-o512-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-normal-i1024-o512-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix formal-r1-normal-i1024-o512-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-normal-i1024-o512-c16-s44.json --metadata mode=normal k=0 gpu=0 phase=formal-r1 concurrency=16 seed=44 prefix_cache=false
```

## 63. formal-r1-dspark-k7-i1024-o512-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T14:35:53.079834+00:00
- 结束：2026-11-24T14:36:35.586688+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-dspark-k7-i1024-o512-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-dspark-k7-i1024-o512-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix formal-r1-dspark-k7-i1024-o512-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-dspark-k7-i1024-o512-c16-s44.json --metadata mode=dspark k=7 gpu=2 phase=formal-r1 concurrency=16 seed=44 prefix_cache=false
```

## 64. formal-r1-mtp-k3-i1024-o512-c4-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T14:36:16.105115+00:00
- 结束：2026-11-24T14:37:24.778219+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-mtp-k3-i1024-o512-c4-s43.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-mtp-k3-i1024-o512-c4-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 43 --request-id-prefix formal-r1-mtp-k3-i1024-o512-c4-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-mtp-k3-i1024-o512-c4-s43.json --metadata mode=mtp k=3 gpu=1 phase=formal-r1 concurrency=4 seed=43 prefix_cache=false
```

## 65. warmup-formal-r1-normal-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T14:36:30.504084+00:00
- 结束：2026-11-24T14:36:42.644894+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-formal-r1-normal-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-formal-r1-normal-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-formal-r1-normal-c4-
```

## 66. warmup-formal-r1-dspark-k7-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T14:36:35.626245+00:00
- 结束：2026-11-24T14:36:45.706424+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-formal-r1-dspark-k7-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-formal-r1-dspark-k7-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-formal-r1-dspark-k7-c4-
```

## 67. formal-r1-normal-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:36:42.674301+00:00
- 结束：2026-11-24T14:39:22.237783+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-normal-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-normal-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix formal-r1-normal-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-normal-i1024-o512-c4-s42.json --metadata mode=normal k=0 gpu=0 phase=formal-r1 concurrency=4 seed=42 prefix_cache=false
```

## 68. formal-r1-dspark-k7-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:36:45.736634+00:00
- 结束：2026-11-24T14:38:19.474669+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-dspark-k7-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-dspark-k7-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix formal-r1-dspark-k7-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-dspark-k7-i1024-o512-c4-s42.json --metadata mode=dspark k=7 gpu=2 phase=formal-r1 concurrency=4 seed=42 prefix_cache=false
```

## 69. formal-r1-mtp-k3-i1024-o512-c4-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T14:37:24.812903+00:00
- 结束：2026-11-24T14:38:32.980177+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-mtp-k3-i1024-o512-c4-s44.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-mtp-k3-i1024-o512-c4-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 44 --request-id-prefix formal-r1-mtp-k3-i1024-o512-c4-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-mtp-k3-i1024-o512-c4-s44.json --metadata mode=mtp k=3 gpu=1 phase=formal-r1 concurrency=4 seed=44 prefix_cache=false
```

## 70. formal-r1-dspark-k7-i1024-o512-c4-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T14:38:19.510696+00:00
- 结束：2026-11-24T14:40:01.513652+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-dspark-k7-i1024-o512-c4-s43.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-dspark-k7-i1024-o512-c4-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 43 --request-id-prefix formal-r1-dspark-k7-i1024-o512-c4-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-dspark-k7-i1024-o512-c4-s43.json --metadata mode=dspark k=7 gpu=2 phase=formal-r1 concurrency=4 seed=43 prefix_cache=false
```

## 71. warmup-formal-r1-mtp-k3-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T14:38:33.014334+00:00
- 结束：2026-11-24T14:38:47.705222+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-formal-r1-mtp-k3-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-formal-r1-mtp-k3-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-formal-r1-mtp-k3-c1-
```

## 72. 035-speed-bench-deps

- 状态：completed；退出码：0
- 开始：2026-11-24T14:38:43.416511+00:00
- 结束：2026-11-24T14:39:10.865080+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[035-speed-bench-deps.log](/home/genai/spec_decoding_study/logs/commands/035-speed-bench-deps.log)

```bash
/home/genai/.local/bin/uv pip install --python /home/genai/.pixi/envs/default/bin/python pandas tiktoken datasets
```

## 73. formal-r1-mtp-k3-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:38:47.737498+00:00
- 结束：2026-11-24T14:42:17.562411+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-mtp-k3-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-mtp-k3-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix formal-r1-mtp-k3-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-mtp-k3-i1024-o512-c1-s42.json --metadata mode=mtp k=3 gpu=1 phase=formal-r1 concurrency=1 seed=42 prefix_cache=false
```

## 74. formal-r1-normal-i1024-o512-c4-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T14:39:22.280855+00:00
- 结束：2026-11-24T14:42:02.356371+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-normal-i1024-o512-c4-s43.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-normal-i1024-o512-c4-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 43 --request-id-prefix formal-r1-normal-i1024-o512-c4-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-normal-i1024-o512-c4-s43.json --metadata mode=normal k=0 gpu=0 phase=formal-r1 concurrency=4 seed=43 prefix_cache=false
```

## 75. 036-prepare-speed-bench-qualitative

- 状态：failed；退出码：-15
- 开始：2026-11-24T14:39:25.047805+00:00
- 结束：2026-11-24T14:47:49.096184+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[036-prepare-speed-bench-qualitative.log](/home/genai/spec_decoding_study/logs/commands/036-prepare-speed-bench-qualitative.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/config/prepare_speed_bench.py --config qualitative --output_dir /home/genai/spec_decoding_study/data/speed_bench
```

## 76. formal-r1-dspark-k7-i1024-o512-c4-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T14:40:01.554864+00:00
- 结束：2026-11-24T14:41:32.399728+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-dspark-k7-i1024-o512-c4-s44.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-dspark-k7-i1024-o512-c4-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 44 --request-id-prefix formal-r1-dspark-k7-i1024-o512-c4-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-dspark-k7-i1024-o512-c4-s44.json --metadata mode=dspark k=7 gpu=2 phase=formal-r1 concurrency=4 seed=44 prefix_cache=false
```

## 77. warmup-formal-r1-dspark-k7-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T14:41:32.435024+00:00
- 结束：2026-11-24T14:41:46.388864+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-formal-r1-dspark-k7-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-formal-r1-dspark-k7-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-formal-r1-dspark-k7-c1-
```

## 78. formal-r1-dspark-k7-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:41:46.419132+00:00
- 结束：2026-11-24T14:46:34.165414+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-dspark-k7-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-dspark-k7-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix formal-r1-dspark-k7-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-dspark-k7-i1024-o512-c1-s42.json --metadata mode=dspark k=7 gpu=2 phase=formal-r1 concurrency=1 seed=42 prefix_cache=false
```

## 79. formal-r1-normal-i1024-o512-c4-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T14:42:02.399096+00:00
- 结束：2026-11-24T14:44:42.744106+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-normal-i1024-o512-c4-s44.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-normal-i1024-o512-c4-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 44 --request-id-prefix formal-r1-normal-i1024-o512-c4-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-normal-i1024-o512-c4-s44.json --metadata mode=normal k=0 gpu=0 phase=formal-r1 concurrency=4 seed=44 prefix_cache=false
```

## 80. formal-r1-mtp-k3-i1024-o512-c1-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T14:42:17.597795+00:00
- 结束：2026-11-24T14:45:46.937327+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-mtp-k3-i1024-o512-c1-s43.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-mtp-k3-i1024-o512-c1-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 43 --request-id-prefix formal-r1-mtp-k3-i1024-o512-c1-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-mtp-k3-i1024-o512-c1-s43.json --metadata mode=mtp k=3 gpu=1 phase=formal-r1 concurrency=1 seed=43 prefix_cache=false
```

## 81. 037-kscan-mtp-gpu3

- 状态：failed；退出码：1
- 开始：2026-11-24T14:43:58.148054+00:00
- 结束：2026-11-24T14:48:27.318277+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[037-kscan-mtp-gpu3.log](/home/genai/spec_decoding_study/logs/commands/037-kscan-mtp-gpu3.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/run_k_scan.py --method mtp --ks 1 2 3 4 5 --gpu 3 --port 8103 --phase kscan-r1 --label-prefix 037 --num-prompts 32 --seeds 42 --concurrencies 32 16 4 1
```

## 82. 037-server-mtp-k1-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T14:43:58.218345+00:00
- 结束：2026-11-24T14:53:37.552358+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[037-server-mtp-k1-gpu3.log](/home/genai/spec_decoding_study/logs/commands/037-server-mtp-k1-gpu3.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8103 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"mtp","num_speculative_tokens":1}'
```

## 83. warmup-formal-r1-normal-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T14:44:42.788003+00:00
- 结束：2026-11-24T14:45:08.442516+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-formal-r1-normal-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-formal-r1-normal-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-formal-r1-normal-c1-
```

## 84. warmup-kscan-r1-mtp-k1-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T14:44:58.280976+00:00
- 结束：2026-11-24T14:45:12.745716+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k1-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k1-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-kscan-r1-mtp-k1-c32-
```

## 85. formal-r1-normal-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:45:08.472686+00:00
- 结束：2026-11-24T14:54:36.923760+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-normal-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-normal-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix formal-r1-normal-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-normal-i1024-o512-c1-s42.json --metadata mode=normal k=0 gpu=0 phase=formal-r1 concurrency=1 seed=42 prefix_cache=false
```

## 86. kscan-r1-mtp-k1-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:45:12.774878+00:00
- 结束：2026-11-24T14:45:27.365473+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k1-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k1-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix kscan-r1-mtp-k1-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k1-i1024-o512-c32-s42.json --metadata mode=mtp k=1 gpu=3 phase=kscan-r1 concurrency=32 seed=42 prefix_cache=false
```

## 87. warmup-kscan-r1-mtp-k1-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T14:45:27.397139+00:00
- 结束：2026-11-24T14:45:39.453229+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k1-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k1-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-kscan-r1-mtp-k1-c16-
```

## 88. kscan-r1-mtp-k1-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:45:39.485688+00:00
- 结束：2026-11-24T14:45:55.537735+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k1-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k1-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix kscan-r1-mtp-k1-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k1-i1024-o512-c16-s42.json --metadata mode=mtp k=1 gpu=3 phase=kscan-r1 concurrency=16 seed=42 prefix_cache=false
```

## 89. formal-r1-mtp-k3-i1024-o512-c1-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T14:45:46.972147+00:00
- 结束：2026-11-24T14:49:16.434057+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-mtp-k3-i1024-o512-c1-s44.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-mtp-k3-i1024-o512-c1-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 44 --request-id-prefix formal-r1-mtp-k3-i1024-o512-c1-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-mtp-k3-i1024-o512-c1-s44.json --metadata mode=mtp k=3 gpu=1 phase=formal-r1 concurrency=1 seed=44 prefix_cache=false
```

## 90. warmup-kscan-r1-mtp-k1-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T14:45:55.569224+00:00
- 结束：2026-11-24T14:46:06.450491+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k1-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k1-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-kscan-r1-mtp-k1-c4-
```

## 91. kscan-r1-mtp-k1-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:46:06.480001+00:00
- 结束：2026-11-24T14:46:37.455030+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k1-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k1-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix kscan-r1-mtp-k1-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k1-i1024-o512-c4-s42.json --metadata mode=mtp k=1 gpu=3 phase=kscan-r1 concurrency=4 seed=42 prefix_cache=false
```

## 92. 038-plot-deps

- 状态：completed；退出码：0
- 开始：2026-11-24T14:46:17.451210+00:00
- 结束：2026-11-24T14:47:04.203003+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[038-plot-deps.log](/home/genai/spec_decoding_study/logs/commands/038-plot-deps.log)

```bash
/home/genai/.local/bin/uv pip install --python /home/genai/.pixi/envs/default/bin/python matplotlib
```

## 93. formal-r1-dspark-k7-i1024-o512-c1-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T14:46:34.201359+00:00
- 结束：2026-11-24T14:51:46.253218+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-dspark-k7-i1024-o512-c1-s43.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-dspark-k7-i1024-o512-c1-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 43 --request-id-prefix formal-r1-dspark-k7-i1024-o512-c1-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-dspark-k7-i1024-o512-c1-s43.json --metadata mode=dspark k=7 gpu=2 phase=formal-r1 concurrency=1 seed=43 prefix_cache=false
```

## 94. warmup-kscan-r1-mtp-k1-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T14:46:37.487124+00:00
- 结束：2026-11-24T14:46:56.859017+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k1-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k1-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-kscan-r1-mtp-k1-c1-
```

## 95. kscan-r1-mtp-k1-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:46:56.888424+00:00
- 结束：2026-11-24T14:48:27.272714+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k1-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k1-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix kscan-r1-mtp-k1-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k1-i1024-o512-c1-s42.json --metadata mode=mtp k=1 gpu=3 phase=kscan-r1 concurrency=1 seed=42 prefix_cache=false
```

## 96. 039-download-spec-bench

- 状态：completed；退出码：0
- 开始：2026-11-24T14:47:49.485320+00:00
- 结束：2026-11-24T14:47:51.836579+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[039-download-spec-bench.log](/home/genai/spec_decoding_study/logs/commands/039-download-spec-bench.log)

```bash
zsh -c 'mkdir -p "/home/genai/spec_decoding_study/data/spec_bench" && curl -fL "https://raw.githubusercontent.com/hemingkx/Spec-Bench/refs/heads/main/data/spec_bench/question.jsonl" -o "/home/genai/spec_decoding_study/data/spec_bench/question.jsonl"'
```

## 97. 040-semantic-mtp-k3-gpu1

- 状态：completed；退出码：0
- 开始：2026-11-24T14:50:24.459837+00:00
- 结束：2026-11-24T15:01:58.458800+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[040-semantic-mtp-k3-gpu1.log](/home/genai/spec_decoding_study/logs/commands/040-semantic-mtp-k3-gpu1.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/run_benchmark_matrix.py --method mtp-k3 --port 8101 --gpu 1 --phase semantic-r1 --vllm /home/genai/.pixi/envs/default/bin/vllm --num-prompts 128 --output-len 256 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --seeds 42 43 44 --concurrencies 32 16 4 1
```

## 98. warmup-semantic-r1-mtp-k3-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T14:50:24.528704+00:00
- 结束：2026-11-24T14:50:34.614581+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-mtp-k3-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-mtp-k3-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-semantic-r1-mtp-k3-c32-
```

## 99. semantic-r1-mtp-k3-specbench-o256-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:50:34.643843+00:00
- 结束：2026-11-24T14:50:51.440428+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-mtp-k3-specbench-o256-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-mtp-k3-specbench-o256-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix semantic-r1-mtp-k3-specbench-o256-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-mtp-k3-specbench-o256-c32-s42.json --metadata method_name=mtp-k3 dataset_name=spec_bench mode=mtp k=3 gpu=1 phase=semantic-r1 concurrency=32 seed=42 prefix_cache=false
```

## 100. semantic-r1-mtp-k3-specbench-o256-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T14:50:51.472850+00:00
- 结束：2026-11-24T14:51:08.563746+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-mtp-k3-specbench-o256-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-mtp-k3-specbench-o256-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix semantic-r1-mtp-k3-specbench-o256-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-mtp-k3-specbench-o256-c32-s43.json --metadata method_name=mtp-k3 dataset_name=spec_bench mode=mtp k=3 gpu=1 phase=semantic-r1 concurrency=32 seed=43 prefix_cache=false
```

## 101. semantic-r1-mtp-k3-specbench-o256-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T14:51:08.596704+00:00
- 结束：2026-11-24T14:51:25.053306+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-mtp-k3-specbench-o256-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-mtp-k3-specbench-o256-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix semantic-r1-mtp-k3-specbench-o256-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-mtp-k3-specbench-o256-c32-s44.json --metadata method_name=mtp-k3 dataset_name=spec_bench mode=mtp k=3 gpu=1 phase=semantic-r1 concurrency=32 seed=44 prefix_cache=false
```

## 102. warmup-semantic-r1-mtp-k3-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T14:51:25.088943+00:00
- 结束：2026-11-24T14:51:34.952226+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-mtp-k3-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-mtp-k3-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-semantic-r1-mtp-k3-c16-
```

## 103. semantic-r1-mtp-k3-specbench-o256-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:51:34.981751+00:00
- 结束：2026-11-24T14:51:58.191173+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-mtp-k3-specbench-o256-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-mtp-k3-specbench-o256-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix semantic-r1-mtp-k3-specbench-o256-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-mtp-k3-specbench-o256-c16-s42.json --metadata method_name=mtp-k3 dataset_name=spec_bench mode=mtp k=3 gpu=1 phase=semantic-r1 concurrency=16 seed=42 prefix_cache=false
```

## 104. formal-r1-dspark-k7-i1024-o512-c1-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T14:51:46.290357+00:00
- 结束：2026-11-24T14:56:12.756261+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-dspark-k7-i1024-o512-c1-s44.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-dspark-k7-i1024-o512-c1-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 44 --request-id-prefix formal-r1-dspark-k7-i1024-o512-c1-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-dspark-k7-i1024-o512-c1-s44.json --metadata mode=dspark k=7 gpu=2 phase=formal-r1 concurrency=1 seed=44 prefix_cache=false
```

## 105. semantic-r1-mtp-k3-specbench-o256-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T14:51:58.223910+00:00
- 结束：2026-11-24T14:52:21.822582+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-mtp-k3-specbench-o256-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-mtp-k3-specbench-o256-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix semantic-r1-mtp-k3-specbench-o256-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-mtp-k3-specbench-o256-c16-s43.json --metadata method_name=mtp-k3 dataset_name=spec_bench mode=mtp k=3 gpu=1 phase=semantic-r1 concurrency=16 seed=43 prefix_cache=false
```

## 106. semantic-r1-mtp-k3-specbench-o256-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T14:52:21.854981+00:00
- 结束：2026-11-24T14:52:45.260088+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-mtp-k3-specbench-o256-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-mtp-k3-specbench-o256-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix semantic-r1-mtp-k3-specbench-o256-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-mtp-k3-specbench-o256-c16-s44.json --metadata method_name=mtp-k3 dataset_name=spec_bench mode=mtp k=3 gpu=1 phase=semantic-r1 concurrency=16 seed=44 prefix_cache=false
```

## 107. warmup-semantic-r1-mtp-k3-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T14:52:45.294425+00:00
- 结束：2026-11-24T14:52:54.436472+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-mtp-k3-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-mtp-k3-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-semantic-r1-mtp-k3-c4-
```

## 108. semantic-r1-mtp-k3-specbench-o256-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:52:54.466817+00:00
- 结束：2026-11-24T14:53:38.877839+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-mtp-k3-specbench-o256-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-mtp-k3-specbench-o256-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix semantic-r1-mtp-k3-specbench-o256-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-mtp-k3-specbench-o256-c4-s42.json --metadata method_name=mtp-k3 dataset_name=spec_bench mode=mtp k=3 gpu=1 phase=semantic-r1 concurrency=4 seed=42 prefix_cache=false
```

## 109. semantic-r1-mtp-k3-specbench-o256-c4-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T14:53:38.910535+00:00
- 结束：2026-11-24T14:54:23.621347+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-mtp-k3-specbench-o256-c4-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-mtp-k3-specbench-o256-c4-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 43 --request-id-prefix semantic-r1-mtp-k3-specbench-o256-c4-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-mtp-k3-specbench-o256-c4-s43.json --metadata method_name=mtp-k3 dataset_name=spec_bench mode=mtp k=3 gpu=1 phase=semantic-r1 concurrency=4 seed=43 prefix_cache=false
```

## 110. 042-kscan-mtp-k2-k5-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T14:53:45.804924+00:00
- 结束：2026-11-24T15:08:51.192854+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[042-kscan-mtp-k2-k5-gpu3.log](/home/genai/spec_decoding_study/logs/commands/042-kscan-mtp-k2-k5-gpu3.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/run_k_scan.py --method mtp --ks 2 3 4 5 --gpu 3 --port 8103 --phase kscan-r1 --label-prefix 042 --num-prompts 32 --seeds 42 --concurrencies 32 16 4 1
```

## 111. 042-server-mtp-k2-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T14:53:45.875054+00:00
- 结束：2026-11-24T14:57:45.394417+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[042-server-mtp-k2-gpu3.log](/home/genai/spec_decoding_study/logs/commands/042-server-mtp-k2-gpu3.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8103 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"mtp","num_speculative_tokens":2}'
```

## 112. semantic-r1-mtp-k3-specbench-o256-c4-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T14:54:23.654926+00:00
- 结束：2026-11-24T14:55:08.585524+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-mtp-k3-specbench-o256-c4-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-mtp-k3-specbench-o256-c4-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 44 --request-id-prefix semantic-r1-mtp-k3-specbench-o256-c4-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-mtp-k3-specbench-o256-c4-s44.json --metadata method_name=mtp-k3 dataset_name=spec_bench mode=mtp k=3 gpu=1 phase=semantic-r1 concurrency=4 seed=44 prefix_cache=false
```

## 113. formal-r1-normal-i1024-o512-c1-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T14:54:36.969265+00:00
- 结束：2026-11-24T15:04:05.981152+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-normal-i1024-o512-c1-s43.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-normal-i1024-o512-c1-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 43 --request-id-prefix formal-r1-normal-i1024-o512-c1-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-normal-i1024-o512-c1-s43.json --metadata mode=normal k=0 gpu=0 phase=formal-r1 concurrency=1 seed=43 prefix_cache=false
```

## 114. warmup-kscan-r1-mtp-k2-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T14:54:47.937444+00:00
- 结束：2026-11-24T14:55:00.853552+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k2-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k2-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-kscan-r1-mtp-k2-c32-
```

## 115. kscan-r1-mtp-k2-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:55:00.883031+00:00
- 结束：2026-11-24T14:55:13.701822+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k2-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k2-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix kscan-r1-mtp-k2-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k2-i1024-o512-c32-s42.json --metadata method_name=mtp-k2 dataset_name=random mode=mtp k=2 gpu=3 phase=kscan-r1 concurrency=32 seed=42 prefix_cache=false
```

## 116. warmup-semantic-r1-mtp-k3-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T14:55:08.618545+00:00
- 结束：2026-11-24T14:55:20.414937+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-mtp-k3-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-mtp-k3-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-semantic-r1-mtp-k3-c1-
```

## 117. warmup-kscan-r1-mtp-k2-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T14:55:13.732653+00:00
- 结束：2026-11-24T14:55:26.357250+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k2-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k2-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-kscan-r1-mtp-k2-c16-
```

## 118. semantic-r1-mtp-k3-specbench-o256-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:55:20.445476+00:00
- 结束：2026-11-24T14:57:33.056698+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-mtp-k3-specbench-o256-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-mtp-k3-specbench-o256-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix semantic-r1-mtp-k3-specbench-o256-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-mtp-k3-specbench-o256-c1-s42.json --metadata method_name=mtp-k3 dataset_name=spec_bench mode=mtp k=3 gpu=1 phase=semantic-r1 concurrency=1 seed=42 prefix_cache=false
```

## 119. kscan-r1-mtp-k2-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:55:26.386894+00:00
- 结束：2026-11-24T14:55:41.477617+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k2-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k2-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix kscan-r1-mtp-k2-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k2-i1024-o512-c16-s42.json --metadata method_name=mtp-k2 dataset_name=random mode=mtp k=2 gpu=3 phase=kscan-r1 concurrency=16 seed=42 prefix_cache=false
```

## 120. warmup-kscan-r1-mtp-k2-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T14:55:41.508636+00:00
- 结束：2026-11-24T14:55:52.103416+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k2-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k2-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-kscan-r1-mtp-k2-c4-
```

## 121. kscan-r1-mtp-k2-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:55:52.133144+00:00
- 结束：2026-11-24T14:56:18.438459+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k2-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k2-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix kscan-r1-mtp-k2-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k2-i1024-o512-c4-s42.json --metadata method_name=mtp-k2 dataset_name=random mode=mtp k=2 gpu=3 phase=kscan-r1 concurrency=4 seed=42 prefix_cache=false
```

## 122. warmup-kscan-r1-mtp-k2-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T14:56:18.470427+00:00
- 结束：2026-11-24T14:56:33.968237+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k2-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k2-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-kscan-r1-mtp-k2-c1-
```

## 123. kscan-r1-mtp-k2-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:56:33.997933+00:00
- 结束：2026-11-24T14:57:43.443602+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k2-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k2-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix kscan-r1-mtp-k2-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k2-i1024-o512-c1-s42.json --metadata method_name=mtp-k2 dataset_name=random mode=mtp k=2 gpu=3 phase=kscan-r1 concurrency=1 seed=42 prefix_cache=false
```

## 124. semantic-r1-mtp-k3-specbench-o256-c1-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T14:57:33.089523+00:00
- 结束：2026-11-24T14:59:45.694610+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-mtp-k3-specbench-o256-c1-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-mtp-k3-specbench-o256-c1-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 43 --request-id-prefix semantic-r1-mtp-k3-specbench-o256-c1-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-mtp-k3-specbench-o256-c1-s43.json --metadata method_name=mtp-k3 dataset_name=spec_bench mode=mtp k=3 gpu=1 phase=semantic-r1 concurrency=1 seed=43 prefix_cache=false
```

## 125. 042-server-mtp-k3-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T14:57:45.334160+00:00
- 结束：2026-11-24T15:01:30.737700+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[042-server-mtp-k3-gpu3.log](/home/genai/spec_decoding_study/logs/commands/042-server-mtp-k3-gpu3.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8103 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"mtp","num_speculative_tokens":3}'
```

## 126. warmup-kscan-r1-mtp-k3-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T14:58:45.397966+00:00
- 结束：2026-11-24T14:58:57.968187+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k3-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k3-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-kscan-r1-mtp-k3-c32-
```

## 127. kscan-r1-mtp-k3-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:58:57.997837+00:00
- 结束：2026-11-24T14:59:11.063107+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k3-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k3-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix kscan-r1-mtp-k3-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k3-i1024-o512-c32-s42.json --metadata method_name=mtp-k3 dataset_name=random mode=mtp k=3 gpu=3 phase=kscan-r1 concurrency=32 seed=42 prefix_cache=false
```

## 128. warmup-kscan-r1-mtp-k3-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T14:59:11.094060+00:00
- 结束：2026-11-24T14:59:24.167441+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k3-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k3-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-kscan-r1-mtp-k3-c16-
```

## 129. kscan-r1-mtp-k3-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:59:24.196309+00:00
- 结束：2026-11-24T14:59:39.689350+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k3-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k3-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix kscan-r1-mtp-k3-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k3-i1024-o512-c16-s42.json --metadata method_name=mtp-k3 dataset_name=random mode=mtp k=3 gpu=3 phase=kscan-r1 concurrency=16 seed=42 prefix_cache=false
```

## 130. warmup-kscan-r1-mtp-k3-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T14:59:39.720543+00:00
- 结束：2026-11-24T14:59:49.740813+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k3-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k3-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-kscan-r1-mtp-k3-c4-
```

## 131. semantic-r1-mtp-k3-specbench-o256-c1-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T14:59:45.728187+00:00
- 结束：2026-11-24T15:01:58.432269+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-mtp-k3-specbench-o256-c1-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-mtp-k3-specbench-o256-c1-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 44 --request-id-prefix semantic-r1-mtp-k3-specbench-o256-c1-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-mtp-k3-specbench-o256-c1-s44.json --metadata method_name=mtp-k3 dataset_name=spec_bench mode=mtp k=3 gpu=1 phase=semantic-r1 concurrency=1 seed=44 prefix_cache=false
```

## 132. kscan-r1-mtp-k3-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T14:59:49.769955+00:00
- 结束：2026-11-24T15:00:14.047544+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k3-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k3-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix kscan-r1-mtp-k3-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k3-i1024-o512-c4-s42.json --metadata method_name=mtp-k3 dataset_name=random mode=mtp k=3 gpu=3 phase=kscan-r1 concurrency=4 seed=42 prefix_cache=false
```

## 133. warmup-kscan-r1-mtp-k3-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:00:14.077955+00:00
- 结束：2026-11-24T15:00:28.780048+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k3-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k3-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-kscan-r1-mtp-k3-c1-
```

## 134. kscan-r1-mtp-k3-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:00:28.808928+00:00
- 结束：2026-11-24T15:01:28.849364+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k3-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k3-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix kscan-r1-mtp-k3-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k3-i1024-o512-c1-s42.json --metadata method_name=mtp-k3 dataset_name=random mode=mtp k=3 gpu=3 phase=kscan-r1 concurrency=1 seed=42 prefix_cache=false
```

## 135. 043-semantic-dspark-k7-gpu2

- 状态：completed；退出码：0
- 开始：2026-11-24T15:00:28.908353+00:00
- 结束：2026-11-24T15:10:42.327452+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[043-semantic-dspark-k7-gpu2.log](/home/genai/spec_decoding_study/logs/commands/043-semantic-dspark-k7-gpu2.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/run_benchmark_matrix.py --method dspark-k7 --port 8102 --gpu 2 --phase semantic-r1 --vllm /home/genai/.pixi/envs/default/bin/vllm --num-prompts 128 --output-len 256 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --seeds 42 43 44 --concurrencies 32 16 4 1
```

## 136. warmup-semantic-r1-dspark-k7-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:00:28.978043+00:00
- 结束：2026-11-24T15:00:39.823294+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-dspark-k7-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-dspark-k7-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-semantic-r1-dspark-k7-c32-
```

## 137. 044-summarize-formal-partial

- 状态：completed；退出码：0
- 开始：2026-11-24T15:00:29.034985+00:00
- 结束：2026-11-24T15:00:29.519635+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[044-summarize-formal-partial.log](/home/genai/spec_decoding_study/logs/commands/044-summarize-formal-partial.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/summarize_benchmarks.py --phase formal-r1 --methods normal mtp-k3 dspark-k7 --concurrencies 1 4 16 32 --seeds 42 43 44 --allow-partial
```

## 138. 045-analyze-mtp-kscan-partial

- 状态：completed；退出码：0
- 开始：2026-11-24T15:00:29.718666+00:00
- 结束：2026-11-24T15:00:29.824022+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[045-analyze-mtp-kscan-partial.log](/home/genai/spec_decoding_study/logs/commands/045-analyze-mtp-kscan-partial.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/analyze_k_scan.py --method mtp --ks 1 2 3 4 5 --allow-partial
```

## 139. semantic-r1-dspark-k7-specbench-o256-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:00:39.855237+00:00
- 结束：2026-11-24T15:00:57.456064+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k7-specbench-o256-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k7-specbench-o256-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix semantic-r1-dspark-k7-specbench-o256-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k7-specbench-o256-c32-s42.json --metadata method_name=dspark-k7 dataset_name=spec_bench mode=dspark k=7 gpu=2 phase=semantic-r1 concurrency=32 seed=42 prefix_cache=false
```

## 140. semantic-r1-dspark-k7-specbench-o256-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:00:57.488230+00:00
- 结束：2026-11-24T15:01:15.247553+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k7-specbench-o256-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k7-specbench-o256-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix semantic-r1-dspark-k7-specbench-o256-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k7-specbench-o256-c32-s43.json --metadata method_name=dspark-k7 dataset_name=spec_bench mode=dspark k=7 gpu=2 phase=semantic-r1 concurrency=32 seed=43 prefix_cache=false
```

## 141. semantic-r1-dspark-k7-specbench-o256-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:01:15.279271+00:00
- 结束：2026-11-24T15:01:33.208651+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k7-specbench-o256-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k7-specbench-o256-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix semantic-r1-dspark-k7-specbench-o256-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k7-specbench-o256-c32-s44.json --metadata method_name=dspark-k7 dataset_name=spec_bench mode=dspark k=7 gpu=2 phase=semantic-r1 concurrency=32 seed=44 prefix_cache=false
```

## 142. 042-server-mtp-k4-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T15:01:30.738914+00:00
- 结束：2026-11-24T15:05:11.370855+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[042-server-mtp-k4-gpu3.log](/home/genai/spec_decoding_study/logs/commands/042-server-mtp-k4-gpu3.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8103 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"mtp","num_speculative_tokens":4}'
```

## 143. warmup-semantic-r1-dspark-k7-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:01:33.240640+00:00
- 结束：2026-11-24T15:01:43.653020+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-dspark-k7-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-dspark-k7-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-semantic-r1-dspark-k7-c16-
```

## 144. semantic-r1-dspark-k7-specbench-o256-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:01:43.682950+00:00
- 结束：2026-11-24T15:02:04.619164+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k7-specbench-o256-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k7-specbench-o256-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix semantic-r1-dspark-k7-specbench-o256-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k7-specbench-o256-c16-s42.json --metadata method_name=dspark-k7 dataset_name=spec_bench mode=dspark k=7 gpu=2 phase=semantic-r1 concurrency=16 seed=42 prefix_cache=false
```

## 145. 046-summarize-semantic-partial

- 状态：completed；退出码：0
- 开始：2026-11-24T15:01:53.996387+00:00
- 结束：2026-11-24T15:01:54.149688+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[046-summarize-semantic-partial.log](/home/genai/spec_decoding_study/logs/commands/046-summarize-semantic-partial.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/summarize_benchmarks.py --phase semantic-r1 --methods mtp-k3 dspark-k7 --concurrencies 1 4 16 32 --seeds 42 43 44 --dataset-name spec_bench --num-prompts 128 --output-len 256 --allow-partial
```

## 146. semantic-r1-dspark-k7-specbench-o256-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:02:04.653008+00:00
- 结束：2026-11-24T15:02:25.146676+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k7-specbench-o256-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k7-specbench-o256-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix semantic-r1-dspark-k7-specbench-o256-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k7-specbench-o256-c16-s43.json --metadata method_name=dspark-k7 dataset_name=spec_bench mode=dspark k=7 gpu=2 phase=semantic-r1 concurrency=16 seed=43 prefix_cache=false
```

## 147. semantic-r1-dspark-k7-specbench-o256-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:02:25.179367+00:00
- 结束：2026-11-24T15:02:45.922633+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k7-specbench-o256-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k7-specbench-o256-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix semantic-r1-dspark-k7-specbench-o256-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k7-specbench-o256-c16-s44.json --metadata method_name=dspark-k7 dataset_name=spec_bench mode=dspark k=7 gpu=2 phase=semantic-r1 concurrency=16 seed=44 prefix_cache=false
```

## 148. warmup-kscan-r1-mtp-k4-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:02:32.802401+00:00
- 结束：2026-11-24T15:02:45.411750+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k4-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k4-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-kscan-r1-mtp-k4-c32-
```

## 149. kscan-r1-mtp-k4-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:02:45.441145+00:00
- 结束：2026-11-24T15:02:58.395587+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k4-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k4-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix kscan-r1-mtp-k4-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k4-i1024-o512-c32-s42.json --metadata method_name=mtp-k4 dataset_name=random mode=mtp k=4 gpu=3 phase=kscan-r1 concurrency=32 seed=42 prefix_cache=false
```

## 150. warmup-semantic-r1-dspark-k7-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T15:02:45.954670+00:00
- 结束：2026-11-24T15:02:55.366930+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-dspark-k7-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-dspark-k7-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-semantic-r1-dspark-k7-c4-
```

## 151. semantic-r1-dspark-k7-specbench-o256-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:02:55.400381+00:00
- 结束：2026-11-24T15:03:36.417349+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k7-specbench-o256-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k7-specbench-o256-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix semantic-r1-dspark-k7-specbench-o256-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k7-specbench-o256-c4-s42.json --metadata method_name=dspark-k7 dataset_name=spec_bench mode=dspark k=7 gpu=2 phase=semantic-r1 concurrency=4 seed=42 prefix_cache=false
```

## 152. warmup-kscan-r1-mtp-k4-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:02:58.426759+00:00
- 结束：2026-11-24T15:03:11.409686+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k4-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k4-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-kscan-r1-mtp-k4-c16-
```

## 153. kscan-r1-mtp-k4-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:03:11.438510+00:00
- 结束：2026-11-24T15:03:25.601755+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k4-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k4-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix kscan-r1-mtp-k4-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k4-i1024-o512-c16-s42.json --metadata method_name=mtp-k4 dataset_name=random mode=mtp k=4 gpu=3 phase=kscan-r1 concurrency=16 seed=42 prefix_cache=false
```

## 154. warmup-kscan-r1-mtp-k4-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T15:03:25.631999+00:00
- 结束：2026-11-24T15:03:36.040142+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k4-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k4-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-kscan-r1-mtp-k4-c4-
```

## 155. kscan-r1-mtp-k4-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:03:36.069188+00:00
- 结束：2026-11-24T15:03:58.752586+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k4-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k4-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix kscan-r1-mtp-k4-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k4-i1024-o512-c4-s42.json --metadata method_name=mtp-k4 dataset_name=random mode=mtp k=4 gpu=3 phase=kscan-r1 concurrency=4 seed=42 prefix_cache=false
```

## 156. semantic-r1-dspark-k7-specbench-o256-c4-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:03:36.455422+00:00
- 结束：2026-11-24T15:04:17.151129+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k7-specbench-o256-c4-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k7-specbench-o256-c4-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 43 --request-id-prefix semantic-r1-dspark-k7-specbench-o256-c4-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k7-specbench-o256-c4-s43.json --metadata method_name=dspark-k7 dataset_name=spec_bench mode=dspark k=7 gpu=2 phase=semantic-r1 concurrency=4 seed=43 prefix_cache=false
```

## 157. warmup-kscan-r1-mtp-k4-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:03:58.782773+00:00
- 结束：2026-11-24T15:04:13.513708+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k4-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k4-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-kscan-r1-mtp-k4-c1-
```

## 158. formal-r1-normal-i1024-o512-c1-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:04:06.029416+00:00
- 结束：2026-11-24T15:13:34.431622+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[formal-r1-normal-i1024-o512-c1-s44.log](/home/genai/spec_decoding_study/logs/commands/formal-r1-normal-i1024-o512-c1-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 44 --request-id-prefix formal-r1-normal-i1024-o512-c1-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename formal-r1-normal-i1024-o512-c1-s44.json --metadata mode=normal k=0 gpu=0 phase=formal-r1 concurrency=1 seed=44 prefix_cache=false
```

## 159. kscan-r1-mtp-k4-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:04:13.542996+00:00
- 结束：2026-11-24T15:05:09.329179+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k4-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k4-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix kscan-r1-mtp-k4-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k4-i1024-o512-c1-s42.json --metadata method_name=mtp-k4 dataset_name=random mode=mtp k=4 gpu=3 phase=kscan-r1 concurrency=1 seed=42 prefix_cache=false
```

## 160. semantic-r1-dspark-k7-specbench-o256-c4-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:04:17.184189+00:00
- 结束：2026-11-24T15:04:57.938347+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k7-specbench-o256-c4-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k7-specbench-o256-c4-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 44 --request-id-prefix semantic-r1-dspark-k7-specbench-o256-c4-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k7-specbench-o256-c4-s44.json --metadata method_name=dspark-k7 dataset_name=spec_bench mode=dspark k=7 gpu=2 phase=semantic-r1 concurrency=4 seed=44 prefix_cache=false
```

## 161. 047-server-semantic-normal-gpu1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:04:25.879628+00:00
- 结束：2026-11-24T15:35:28.111616+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[047-server-semantic-normal-gpu1.log](/home/genai/spec_decoding_study/logs/commands/047-server-semantic-normal-gpu1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8101 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0
```

## 162. 048-semantic-normal-gpu1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:04:25.906588+00:00
- 结束：2026-11-24T15:27:15.529675+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[048-semantic-normal-gpu1.log](/home/genai/spec_decoding_study/logs/commands/048-semantic-normal-gpu1.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/run_benchmark_matrix.py --method normal --port 8101 --gpu 1 --phase semantic-r1 --vllm /home/genai/.pixi/envs/default/bin/vllm --num-prompts 128 --output-len 256 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --seeds 42 43 44 --concurrencies 32 16 4 1
```

## 163. warmup-semantic-r1-dspark-k7-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:04:57.971265+00:00
- 结束：2026-11-24T15:05:09.336044+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-dspark-k7-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-dspark-k7-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-semantic-r1-dspark-k7-c1-
```

## 164. semantic-r1-dspark-k7-specbench-o256-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:05:09.365707+00:00
- 结束：2026-11-24T15:07:00.100798+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k7-specbench-o256-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k7-specbench-o256-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix semantic-r1-dspark-k7-specbench-o256-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k7-specbench-o256-c1-s42.json --metadata method_name=dspark-k7 dataset_name=spec_bench mode=dspark k=7 gpu=2 phase=semantic-r1 concurrency=1 seed=42 prefix_cache=false
```

## 165. 042-server-mtp-k5-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T15:05:11.424571+00:00
- 结束：2026-11-24T15:08:51.287950+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[042-server-mtp-k5-gpu3.log](/home/genai/spec_decoding_study/logs/commands/042-server-mtp-k5-gpu3.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8103 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"mtp","num_speculative_tokens":5}'
```

## 166. warmup-semantic-r1-normal-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:05:29.991673+00:00
- 结束：2026-11-24T15:05:42.073318+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-normal-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-normal-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-semantic-r1-normal-c32-
```

## 167. semantic-r1-normal-specbench-o256-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:05:42.102623+00:00
- 结束：2026-11-24T15:06:03.391157+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-normal-specbench-o256-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-normal-specbench-o256-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix semantic-r1-normal-specbench-o256-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-normal-specbench-o256-c32-s42.json --metadata method_name=normal dataset_name=spec_bench mode=normal k=0 gpu=1 phase=semantic-r1 concurrency=32 seed=42 prefix_cache=false
```

## 168. 049-analyze-mtp-kscan-k1-k4

- 状态：completed；退出码：0
- 开始：2026-11-24T15:05:59.508618+00:00
- 结束：2026-11-24T15:05:59.612347+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[049-analyze-mtp-kscan-k1-k4.log](/home/genai/spec_decoding_study/logs/commands/049-analyze-mtp-kscan-k1-k4.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/analyze_k_scan.py --method mtp --ks 1 2 3 4 --allow-partial
```

## 169. semantic-r1-normal-specbench-o256-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:06:03.428468+00:00
- 结束：2026-11-24T15:06:24.625191+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-normal-specbench-o256-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-normal-specbench-o256-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix semantic-r1-normal-specbench-o256-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-normal-specbench-o256-c32-s43.json --metadata method_name=normal dataset_name=spec_bench mode=normal k=0 gpu=1 phase=semantic-r1 concurrency=32 seed=43 prefix_cache=false
```

## 170. warmup-kscan-r1-mtp-k5-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:06:17.492959+00:00
- 结束：2026-11-24T15:06:31.674426+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k5-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k5-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-kscan-r1-mtp-k5-c32-
```

## 171. semantic-r1-normal-specbench-o256-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:06:24.666619+00:00
- 结束：2026-11-24T15:06:45.993591+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-normal-specbench-o256-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-normal-specbench-o256-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix semantic-r1-normal-specbench-o256-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-normal-specbench-o256-c32-s44.json --metadata method_name=normal dataset_name=spec_bench mode=normal k=0 gpu=1 phase=semantic-r1 concurrency=32 seed=44 prefix_cache=false
```

## 172. kscan-r1-mtp-k5-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:06:31.703829+00:00
- 结束：2026-11-24T15:06:44.305301+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k5-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k5-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix kscan-r1-mtp-k5-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k5-i1024-o512-c32-s42.json --metadata method_name=mtp-k5 dataset_name=random mode=mtp k=5 gpu=3 phase=kscan-r1 concurrency=32 seed=42 prefix_cache=false
```

## 173. warmup-kscan-r1-mtp-k5-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:06:44.335801+00:00
- 结束：2026-11-24T15:06:55.687197+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k5-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k5-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-kscan-r1-mtp-k5-c16-
```

## 174. warmup-semantic-r1-normal-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:06:46.030072+00:00
- 结束：2026-11-24T15:06:56.923143+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-normal-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-normal-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-semantic-r1-normal-c16-
```

## 175. kscan-r1-mtp-k5-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:06:55.716209+00:00
- 结束：2026-11-24T15:07:09.837084+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k5-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k5-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix kscan-r1-mtp-k5-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k5-i1024-o512-c16-s42.json --metadata method_name=mtp-k5 dataset_name=random mode=mtp k=5 gpu=3 phase=kscan-r1 concurrency=16 seed=42 prefix_cache=false
```

## 176. semantic-r1-normal-specbench-o256-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:06:56.952337+00:00
- 结束：2026-11-24T15:07:26.569191+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-normal-specbench-o256-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-normal-specbench-o256-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix semantic-r1-normal-specbench-o256-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-normal-specbench-o256-c16-s42.json --metadata method_name=normal dataset_name=spec_bench mode=normal k=0 gpu=1 phase=semantic-r1 concurrency=16 seed=42 prefix_cache=false
```

## 177. semantic-r1-dspark-k7-specbench-o256-c1-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:07:00.134161+00:00
- 结束：2026-11-24T15:08:50.624264+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k7-specbench-o256-c1-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k7-specbench-o256-c1-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 43 --request-id-prefix semantic-r1-dspark-k7-specbench-o256-c1-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k7-specbench-o256-c1-s43.json --metadata method_name=dspark-k7 dataset_name=spec_bench mode=dspark k=7 gpu=2 phase=semantic-r1 concurrency=1 seed=43 prefix_cache=false
```

## 178. warmup-kscan-r1-mtp-k5-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T15:07:09.867384+00:00
- 结束：2026-11-24T15:07:20.026759+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k5-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k5-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-kscan-r1-mtp-k5-c4-
```

## 179. kscan-r1-mtp-k5-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:07:20.055770+00:00
- 结束：2026-11-24T15:07:42.447205+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k5-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k5-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix kscan-r1-mtp-k5-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k5-i1024-o512-c4-s42.json --metadata method_name=mtp-k5 dataset_name=random mode=mtp k=5 gpu=3 phase=kscan-r1 concurrency=4 seed=42 prefix_cache=false
```

## 180. semantic-r1-normal-specbench-o256-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:07:26.615625+00:00
- 结束：2026-11-24T15:07:56.724903+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-normal-specbench-o256-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-normal-specbench-o256-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix semantic-r1-normal-specbench-o256-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-normal-specbench-o256-c16-s43.json --metadata method_name=normal dataset_name=spec_bench mode=normal k=0 gpu=1 phase=semantic-r1 concurrency=16 seed=43 prefix_cache=false
```

## 181. warmup-kscan-r1-mtp-k5-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:07:42.477691+00:00
- 结束：2026-11-24T15:07:56.866423+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k5-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k5-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-kscan-r1-mtp-k5-c1-
```

## 182. semantic-r1-normal-specbench-o256-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:07:56.762059+00:00
- 结束：2026-11-24T15:08:26.487102+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-normal-specbench-o256-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-normal-specbench-o256-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix semantic-r1-normal-specbench-o256-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-normal-specbench-o256-c16-s44.json --metadata method_name=normal dataset_name=spec_bench mode=normal k=0 gpu=1 phase=semantic-r1 concurrency=16 seed=44 prefix_cache=false
```

## 183. kscan-r1-mtp-k5-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:07:56.895448+00:00
- 结束：2026-11-24T15:08:49.345442+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k5-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k5-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix kscan-r1-mtp-k5-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k5-i1024-o512-c1-s42.json --metadata method_name=mtp-k5 dataset_name=random mode=mtp k=5 gpu=3 phase=kscan-r1 concurrency=1 seed=42 prefix_cache=false
```

## 184. 050-render-partial-figures

- 状态：completed；退出码：0
- 开始：2026-11-24T15:08:11.616897+00:00
- 结束：2026-11-24T15:08:14.348244+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[050-render-partial-figures.log](/home/genai/spec_decoding_study/logs/commands/050-render-partial-figures.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/make_figures.py
```

## 185. warmup-semantic-r1-normal-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T15:08:26.524188+00:00
- 结束：2026-11-24T15:08:36.729694+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-normal-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-normal-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-semantic-r1-normal-c4-
```

## 186. semantic-r1-normal-specbench-o256-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:08:36.759751+00:00
- 结束：2026-11-24T15:09:59.356927+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-normal-specbench-o256-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-normal-specbench-o256-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix semantic-r1-normal-specbench-o256-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-normal-specbench-o256-c4-s42.json --metadata method_name=normal dataset_name=spec_bench mode=normal k=0 gpu=1 phase=semantic-r1 concurrency=4 seed=42 prefix_cache=false
```

## 187. semantic-r1-dspark-k7-specbench-o256-c1-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:08:50.657138+00:00
- 结束：2026-11-24T15:10:42.308237+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k7-specbench-o256-c1-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k7-specbench-o256-c1-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 44 --request-id-prefix semantic-r1-dspark-k7-specbench-o256-c1-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k7-specbench-o256-c1-s44.json --metadata method_name=dspark-k7 dataset_name=spec_bench mode=dspark k=7 gpu=2 phase=semantic-r1 concurrency=1 seed=44 prefix_cache=false
```

## 188. 051-analyze-mtp-kscan-complete

- 状态：completed；退出码：0
- 开始：2026-11-24T15:09:42.360883+00:00
- 结束：2026-11-24T15:09:42.468439+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[051-analyze-mtp-kscan-complete.log](/home/genai/spec_decoding_study/logs/commands/051-analyze-mtp-kscan-complete.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/analyze_k_scan.py --method mtp --ks 1 2 3 4 5
```

## 189. 052-summarize-mtp-kscan-complete

- 状态：completed；退出码：0
- 开始：2026-11-24T15:09:42.664979+00:00
- 结束：2026-11-24T15:09:42.808320+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[052-summarize-mtp-kscan-complete.log](/home/genai/spec_decoding_study/logs/commands/052-summarize-mtp-kscan-complete.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/summarize_benchmarks.py --phase kscan-r1 --methods mtp-k1 mtp-k2 mtp-k3 mtp-k4 mtp-k5 --concurrencies 1 4 16 32 --seeds 42 --num-prompts 32
```

## 190. semantic-r1-normal-specbench-o256-c4-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:09:59.393976+00:00
- 结束：2026-11-24T15:11:21.513121+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-normal-specbench-o256-c4-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-normal-specbench-o256-c4-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 43 --request-id-prefix semantic-r1-normal-specbench-o256-c4-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-normal-specbench-o256-c4-s43.json --metadata method_name=normal dataset_name=spec_bench mode=normal k=0 gpu=1 phase=semantic-r1 concurrency=4 seed=43 prefix_cache=false
```

## 191. 053-kscan-mtp-k6-k7-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T15:10:05.041695+00:00
- 结束：2026-11-24T15:17:26.568841+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[053-kscan-mtp-k6-k7-gpu3.log](/home/genai/spec_decoding_study/logs/commands/053-kscan-mtp-k6-k7-gpu3.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/run_k_scan.py --method mtp --ks 6 7 --gpu 3 --port 8103 --phase kscan-r1 --label-prefix 053 --num-prompts 32 --seeds 42 --concurrencies 32 16 4 1
```

## 192. 053-server-mtp-k6-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T15:10:05.112721+00:00
- 结束：2026-11-24T15:13:45.802840+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[053-server-mtp-k6-gpu3.log](/home/genai/spec_decoding_study/logs/commands/053-server-mtp-k6-gpu3.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8103 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"mtp","num_speculative_tokens":6}'
```

## 193. warmup-kscan-r1-mtp-k6-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:11:11.178590+00:00
- 结束：2026-11-24T15:11:24.896081+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k6-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k6-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-kscan-r1-mtp-k6-c32-
```

## 194. semantic-r1-normal-specbench-o256-c4-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:11:21.555044+00:00
- 结束：2026-11-24T15:12:43.997680+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-normal-specbench-o256-c4-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-normal-specbench-o256-c4-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 44 --request-id-prefix semantic-r1-normal-specbench-o256-c4-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-normal-specbench-o256-c4-s44.json --metadata method_name=normal dataset_name=spec_bench mode=normal k=0 gpu=1 phase=semantic-r1 concurrency=4 seed=44 prefix_cache=false
```

## 195. kscan-r1-mtp-k6-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:11:24.926451+00:00
- 结束：2026-11-24T15:11:38.613463+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k6-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k6-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix kscan-r1-mtp-k6-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k6-i1024-o512-c32-s42.json --metadata method_name=mtp-k6 dataset_name=random mode=mtp k=6 gpu=3 phase=kscan-r1 concurrency=32 seed=42 prefix_cache=false
```

## 196. warmup-kscan-r1-mtp-k6-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:11:38.643882+00:00
- 结束：2026-11-24T15:11:50.943582+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k6-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k6-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-kscan-r1-mtp-k6-c16-
```

## 197. kscan-r1-mtp-k6-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:11:50.973525+00:00
- 结束：2026-11-24T15:12:06.088061+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k6-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k6-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix kscan-r1-mtp-k6-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k6-i1024-o512-c16-s42.json --metadata method_name=mtp-k6 dataset_name=random mode=mtp k=6 gpu=3 phase=kscan-r1 concurrency=16 seed=42 prefix_cache=false
```

## 198. warmup-kscan-r1-mtp-k6-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T15:12:06.123234+00:00
- 结束：2026-11-24T15:12:16.353130+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k6-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k6-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-kscan-r1-mtp-k6-c4-
```

## 199. kscan-r1-mtp-k6-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:12:16.382775+00:00
- 结束：2026-11-24T15:12:38.093904+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k6-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k6-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix kscan-r1-mtp-k6-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k6-i1024-o512-c4-s42.json --metadata method_name=mtp-k6 dataset_name=random mode=mtp k=6 gpu=3 phase=kscan-r1 concurrency=4 seed=42 prefix_cache=false
```

## 200. 054-policy-dspark-fixed-vs-adaptive-gpu2

- 状态：completed；退出码：0
- 开始：2026-11-24T15:12:18.479970+00:00
- 结束：2026-11-24T15:32:25.229075+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[054-policy-dspark-fixed-vs-adaptive-gpu2.log](/home/genai/spec_decoding_study/logs/commands/054-policy-dspark-fixed-vs-adaptive-gpu2.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/run_server_suite.py --config /home/genai/spec_decoding_study/config/dspark_policy_comparison.json --gpu 2 --port 8102 --phase policy-dspark-r1 --label-prefix 054 --num-prompts 32 --seeds 42 43 44 --concurrencies 32 16 4 1
```

## 201. 054-server-dspark-k7-gpu2

- 状态：completed；退出码：0
- 开始：2026-11-24T15:12:18.551056+00:00
- 结束：2026-11-24T15:21:54.948473+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[054-server-dspark-k7-gpu2.log](/home/genai/spec_decoding_study/logs/commands/054-server-dspark-k7-gpu2.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8102 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"dspark","model":"/home/genai/models/Qwen3.8-27B-DSpark-vLLM","num_speculative_tokens":7}'
```

## 202. 055-summarize-semantic-near-complete

- 状态：completed；退出码：0
- 开始：2026-11-24T15:12:31.035880+00:00
- 结束：2026-11-24T15:12:31.296067+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[055-summarize-semantic-near-complete.log](/home/genai/spec_decoding_study/logs/commands/055-summarize-semantic-near-complete.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/summarize_benchmarks.py --phase semantic-r1 --methods normal mtp-k3 dspark-k7 --concurrencies 1 4 16 32 --seeds 42 43 44 --dataset-name spec_bench --num-prompts 128 --output-len 256 --allow-partial
```

## 203. warmup-kscan-r1-mtp-k6-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:12:38.124552+00:00
- 结束：2026-11-24T15:12:52.405193+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k6-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k6-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-kscan-r1-mtp-k6-c1-
```

## 204. warmup-semantic-r1-normal-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:12:44.033924+00:00
- 结束：2026-11-24T15:13:00.587127+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-normal-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-normal-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-semantic-r1-normal-c1-
```

## 205. kscan-r1-mtp-k6-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:12:52.434766+00:00
- 结束：2026-11-24T15:13:43.639945+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k6-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k6-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix kscan-r1-mtp-k6-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k6-i1024-o512-c1-s42.json --metadata method_name=mtp-k6 dataset_name=random mode=mtp k=6 gpu=3 phase=kscan-r1 concurrency=1 seed=42 prefix_cache=false
```

## 206. semantic-r1-normal-specbench-o256-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:13:00.617284+00:00
- 结束：2026-11-24T15:17:44.973615+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-normal-specbench-o256-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-normal-specbench-o256-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix semantic-r1-normal-specbench-o256-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-normal-specbench-o256-c1-s42.json --metadata method_name=normal dataset_name=spec_bench mode=normal k=0 gpu=1 phase=semantic-r1 concurrency=1 seed=42 prefix_cache=false
```

## 207. warmup-policy-dspark-r1-dspark-k7-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:13:20.614990+00:00
- 结束：2026-11-24T15:13:38.286926+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-dspark-r1-dspark-k7-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-dspark-r1-dspark-k7-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-policy-dspark-r1-dspark-k7-c32-
```

## 208. policy-dspark-r1-dspark-k7-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:13:38.316338+00:00
- 结束：2026-11-24T15:13:58.136737+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k7-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k7-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix policy-dspark-r1-dspark-k7-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k7-i1024-o512-c32-s42.json --metadata method_name=dspark-k7 dataset_name=random mode=dspark k=7 gpu=2 phase=policy-dspark-r1 concurrency=32 seed=42 prefix_cache=false
```

## 209. 053-server-mtp-k7-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T15:13:45.731403+00:00
- 结束：2026-11-24T15:17:26.657838+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[053-server-mtp-k7-gpu3.log](/home/genai/spec_decoding_study/logs/commands/053-server-mtp-k7-gpu3.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8103 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"mtp","num_speculative_tokens":7}'
```

## 210. policy-dspark-r1-dspark-k7-i1024-o512-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:13:58.169232+00:00
- 结束：2026-11-24T15:14:17.940459+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k7-i1024-o512-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k7-i1024-o512-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix policy-dspark-r1-dspark-k7-i1024-o512-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k7-i1024-o512-c32-s43.json --metadata method_name=dspark-k7 dataset_name=random mode=dspark k=7 gpu=2 phase=policy-dspark-r1 concurrency=32 seed=43 prefix_cache=false
```

## 211. policy-dspark-r1-dspark-k7-i1024-o512-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:14:17.972155+00:00
- 结束：2026-11-24T15:14:35.715078+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k7-i1024-o512-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k7-i1024-o512-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix policy-dspark-r1-dspark-k7-i1024-o512-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k7-i1024-o512-c32-s44.json --metadata method_name=dspark-k7 dataset_name=random mode=dspark k=7 gpu=2 phase=policy-dspark-r1 concurrency=32 seed=44 prefix_cache=false
```

## 212. 056-stop-formal-normal-gpu0

- 状态：completed；退出码：0
- 开始：2026-11-24T15:14:27.415006+00:00
- 结束：2026-11-24T15:14:29.443025+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[056-stop-formal-normal-gpu0.log](/home/genai/spec_decoding_study/logs/commands/056-stop-formal-normal-gpu0.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/bin/stop_logged.py --label 027-server-formal-normal-gpu0 --expect /home/genai/.pixi/envs/default/bin/vllm --expect 8100 --timeout 120
```

## 213. 057-kscan-dspark-k1-k3-k5-k7-gpu0

- 状态：completed；退出码：0
- 开始：2026-11-24T15:14:29.503649+00:00
- 结束：2026-11-24T15:34:32.363539+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[057-kscan-dspark-k1-k3-k5-k7-gpu0.log](/home/genai/spec_decoding_study/logs/commands/057-kscan-dspark-k1-k3-k5-k7-gpu0.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/run_k_scan.py --method dspark --ks 1 3 5 7 --gpu 0 --port 8100 --phase kscan-r1 --label-prefix 057 --num-prompts 32 --seeds 42 --concurrencies 32 16 4 1
```

## 214. 057-server-dspark-k1-gpu0

- 状态：completed；退出码：0
- 开始：2026-11-24T15:14:29.581440+00:00
- 结束：2026-11-24T15:20:05.631114+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[057-server-dspark-k1-gpu0.log](/home/genai/spec_decoding_study/logs/commands/057-server-dspark-k1-gpu0.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8100 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"dspark","num_speculative_tokens":1,"model":"/home/genai/models/Qwen3.8-27B-DSpark-vLLM"}'
```

## 215. 058-summarize-formal-complete

- 状态：completed；退出码：0
- 开始：2026-11-24T15:14:29.679005+00:00
- 结束：2026-11-24T15:14:30.217821+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[058-summarize-formal-complete.log](/home/genai/spec_decoding_study/logs/commands/058-summarize-formal-complete.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/summarize_benchmarks.py --phase formal-r1 --methods normal mtp-k3 dspark-k7 --concurrencies 1 4 16 32 --seeds 42 43 44
```

## 216. warmup-policy-dspark-r1-dspark-k7-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:14:35.749763+00:00
- 结束：2026-11-24T15:14:53.385655+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-dspark-r1-dspark-k7-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-dspark-r1-dspark-k7-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-policy-dspark-r1-dspark-k7-c16-
```

## 217. warmup-kscan-r1-mtp-k7-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:14:47.797795+00:00
- 结束：2026-11-24T15:15:01.263790+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k7-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k7-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-kscan-r1-mtp-k7-c32-
```

## 218. policy-dspark-r1-dspark-k7-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:14:53.415712+00:00
- 结束：2026-11-24T15:15:14.727803+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k7-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k7-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix policy-dspark-r1-dspark-k7-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k7-i1024-o512-c16-s42.json --metadata method_name=dspark-k7 dataset_name=random mode=dspark k=7 gpu=2 phase=policy-dspark-r1 concurrency=16 seed=42 prefix_cache=false
```

## 219. kscan-r1-mtp-k7-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:15:01.293425+00:00
- 结束：2026-11-24T15:15:14.735222+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k7-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k7-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix kscan-r1-mtp-k7-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k7-i1024-o512-c32-s42.json --metadata method_name=mtp-k7 dataset_name=random mode=mtp k=7 gpu=3 phase=kscan-r1 concurrency=32 seed=42 prefix_cache=false
```

## 220. policy-dspark-r1-dspark-k7-i1024-o512-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:15:14.759930+00:00
- 结束：2026-11-24T15:15:36.564012+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k7-i1024-o512-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k7-i1024-o512-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix policy-dspark-r1-dspark-k7-i1024-o512-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k7-i1024-o512-c16-s43.json --metadata method_name=dspark-k7 dataset_name=random mode=dspark k=7 gpu=2 phase=policy-dspark-r1 concurrency=16 seed=43 prefix_cache=false
```

## 221. warmup-kscan-r1-mtp-k7-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:15:14.765257+00:00
- 结束：2026-11-24T15:15:27.354008+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k7-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k7-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-kscan-r1-mtp-k7-c16-
```

## 222. kscan-r1-mtp-k7-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:15:27.387697+00:00
- 结束：2026-11-24T15:15:42.321423+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k7-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k7-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix kscan-r1-mtp-k7-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k7-i1024-o512-c16-s42.json --metadata method_name=mtp-k7 dataset_name=random mode=mtp k=7 gpu=3 phase=kscan-r1 concurrency=16 seed=42 prefix_cache=false
```

## 223. policy-dspark-r1-dspark-k7-i1024-o512-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:15:36.600961+00:00
- 结束：2026-11-24T15:15:56.241065+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k7-i1024-o512-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k7-i1024-o512-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix policy-dspark-r1-dspark-k7-i1024-o512-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k7-i1024-o512-c16-s44.json --metadata method_name=dspark-k7 dataset_name=random mode=dspark k=7 gpu=2 phase=policy-dspark-r1 concurrency=16 seed=44 prefix_cache=false
```

## 224. warmup-kscan-r1-dspark-k1-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:15:39.655445+00:00
- 结束：2026-11-24T15:15:57.680462+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-dspark-k1-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-dspark-k1-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-kscan-r1-dspark-k1-c32-
```

## 225. warmup-kscan-r1-mtp-k7-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T15:15:42.356156+00:00
- 结束：2026-11-24T15:15:53.168664+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k7-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k7-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-kscan-r1-mtp-k7-c4-
```

## 226. kscan-r1-mtp-k7-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:15:53.203154+00:00
- 结束：2026-11-24T15:16:16.506117+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k7-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k7-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix kscan-r1-mtp-k7-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k7-i1024-o512-c4-s42.json --metadata method_name=mtp-k7 dataset_name=random mode=mtp k=7 gpu=3 phase=kscan-r1 concurrency=4 seed=42 prefix_cache=false
```

## 227. warmup-policy-dspark-r1-dspark-k7-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T15:15:56.277473+00:00
- 结束：2026-11-24T15:16:07.958669+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-dspark-r1-dspark-k7-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-dspark-r1-dspark-k7-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-policy-dspark-r1-dspark-k7-c4-
```

## 228. kscan-r1-dspark-k1-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:15:57.715770+00:00
- 结束：2026-11-24T15:16:15.976726+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-dspark-k1-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-dspark-k1-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix kscan-r1-dspark-k1-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-dspark-k1-i1024-o512-c32-s42.json --metadata method_name=dspark-k1 dataset_name=random mode=dspark k=1 gpu=0 phase=kscan-r1 concurrency=32 seed=42 prefix_cache=false
```

## 229. policy-dspark-r1-dspark-k7-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:16:07.992836+00:00
- 结束：2026-11-24T15:16:42.170261+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k7-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k7-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix policy-dspark-r1-dspark-k7-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k7-i1024-o512-c4-s42.json --metadata method_name=dspark-k7 dataset_name=random mode=dspark k=7 gpu=2 phase=policy-dspark-r1 concurrency=4 seed=42 prefix_cache=false
```

## 230. warmup-kscan-r1-dspark-k1-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:16:16.013369+00:00
- 结束：2026-11-24T15:16:32.585051+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-dspark-k1-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-dspark-k1-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-kscan-r1-dspark-k1-c16-
```

## 231. warmup-kscan-r1-mtp-k7-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:16:16.540859+00:00
- 结束：2026-11-24T15:16:32.636246+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-mtp-k7-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-mtp-k7-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-kscan-r1-mtp-k7-c1-
```

## 232. kscan-r1-dspark-k1-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:16:32.619016+00:00
- 结束：2026-11-24T15:16:52.498546+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-dspark-k1-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-dspark-k1-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix kscan-r1-dspark-k1-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-dspark-k1-i1024-o512-c16-s42.json --metadata method_name=dspark-k1 dataset_name=random mode=dspark k=1 gpu=0 phase=kscan-r1 concurrency=16 seed=42 prefix_cache=false
```

## 233. kscan-r1-mtp-k7-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:16:32.669754+00:00
- 结束：2026-11-24T15:17:24.313144+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-mtp-k7-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-mtp-k7-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix kscan-r1-mtp-k7-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-mtp-k7-i1024-o512-c1-s42.json --metadata method_name=mtp-k7 dataset_name=random mode=mtp k=7 gpu=3 phase=kscan-r1 concurrency=1 seed=42 prefix_cache=false
```

## 234. policy-dspark-r1-dspark-k7-i1024-o512-c4-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:16:42.206253+00:00
- 结束：2026-11-24T15:17:16.406740+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k7-i1024-o512-c4-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k7-i1024-o512-c4-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 43 --request-id-prefix policy-dspark-r1-dspark-k7-i1024-o512-c4-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k7-i1024-o512-c4-s43.json --metadata method_name=dspark-k7 dataset_name=random mode=dspark k=7 gpu=2 phase=policy-dspark-r1 concurrency=4 seed=43 prefix_cache=false
```

## 235. warmup-kscan-r1-dspark-k1-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T15:16:52.536155+00:00
- 结束：2026-11-24T15:17:04.867681+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-dspark-k1-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-dspark-k1-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-kscan-r1-dspark-k1-c4-
```

## 236. kscan-r1-dspark-k1-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:17:04.898092+00:00
- 结束：2026-11-24T15:17:44.965729+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-dspark-k1-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-dspark-k1-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix kscan-r1-dspark-k1-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-dspark-k1-i1024-o512-c4-s42.json --metadata method_name=dspark-k1 dataset_name=random mode=dspark k=1 gpu=0 phase=kscan-r1 concurrency=4 seed=42 prefix_cache=false
```

## 237. policy-dspark-r1-dspark-k7-i1024-o512-c4-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:17:16.442944+00:00
- 结束：2026-11-24T15:17:44.495296+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k7-i1024-o512-c4-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k7-i1024-o512-c4-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 44 --request-id-prefix policy-dspark-r1-dspark-k7-i1024-o512-c4-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k7-i1024-o512-c4-s44.json --metadata method_name=dspark-k7 dataset_name=random mode=dspark k=7 gpu=2 phase=policy-dspark-r1 concurrency=4 seed=44 prefix_cache=false
```

## 238. warmup-policy-dspark-r1-dspark-k7-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:17:44.526546+00:00
- 结束：2026-11-24T15:17:59.304034+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-dspark-r1-dspark-k7-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-dspark-r1-dspark-k7-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-policy-dspark-r1-dspark-k7-c1-
```

## 239. warmup-kscan-r1-dspark-k1-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:17:45.003749+00:00
- 结束：2026-11-24T15:18:05.923232+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-dspark-k1-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-dspark-k1-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-kscan-r1-dspark-k1-c1-
```

## 240. semantic-r1-normal-specbench-o256-c1-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:17:45.016327+00:00
- 结束：2026-11-24T15:22:30.768676+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-normal-specbench-o256-c1-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-normal-specbench-o256-c1-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 43 --request-id-prefix semantic-r1-normal-specbench-o256-c1-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-normal-specbench-o256-c1-s43.json --metadata method_name=normal dataset_name=spec_bench mode=normal k=0 gpu=1 phase=semantic-r1 concurrency=1 seed=43 prefix_cache=false
```

## 241. 059-analyze-mtp-kscan-k1-k7

- 状态：completed；退出码：0
- 开始：2026-11-24T15:17:52.523076+00:00
- 结束：2026-11-24T15:17:52.648644+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[059-analyze-mtp-kscan-k1-k7.log](/home/genai/spec_decoding_study/logs/commands/059-analyze-mtp-kscan-k1-k7.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/analyze_k_scan.py --method mtp --ks 1 2 3 4 5 6 7
```

## 242. 060-summarize-mtp-kscan-k1-k7

- 状态：completed；退出码：0
- 开始：2026-11-24T15:17:52.863105+00:00
- 结束：2026-11-24T15:17:53.034682+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[060-summarize-mtp-kscan-k1-k7.log](/home/genai/spec_decoding_study/logs/commands/060-summarize-mtp-kscan-k1-k7.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/summarize_benchmarks.py --phase kscan-r1 --methods mtp-k1 mtp-k2 mtp-k3 mtp-k4 mtp-k5 mtp-k6 mtp-k7 --concurrencies 1 4 16 32 --seeds 42 --num-prompts 32
```

## 243. policy-dspark-r1-dspark-k7-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:17:59.334164+00:00
- 结束：2026-11-24T15:19:25.518592+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k7-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k7-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix policy-dspark-r1-dspark-k7-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k7-i1024-o512-c1-s42.json --metadata method_name=dspark-k7 dataset_name=random mode=dspark k=7 gpu=2 phase=policy-dspark-r1 concurrency=1 seed=42 prefix_cache=false
```

## 244. kscan-r1-dspark-k1-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:18:05.956676+00:00
- 结束：2026-11-24T15:20:03.206913+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-dspark-k1-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-dspark-k1-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix kscan-r1-dspark-k1-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-dspark-k1-i1024-o512-c1-s42.json --metadata method_name=dspark-k1 dataset_name=random mode=dspark k=1 gpu=0 phase=kscan-r1 concurrency=1 seed=42 prefix_cache=false
```

## 245. 061-resolve-dynamic-schedules

- 状态：completed；退出码：0
- 开始：2026-11-24T15:19:00.840219+00:00
- 结束：2026-11-24T15:19:02.055985+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[061-resolve-dynamic-schedules.log](/home/genai/spec_decoding_study/logs/commands/061-resolve-dynamic-schedules.log)

```bash
/home/genai/.pixi/envs/default/bin/python -c 'import json; from pathlib import Path; from vllm.v1.spec_decode.dynamic.utils import build_dynamic_sd_schedule_lookup; cs=json.loads(Path("config/mtp_policy_comparison.json").read_text())["configurations"]; out={}; [(out.update({c["name"]: {str(b): build_dynamic_sd_schedule_lookup(c["speculative_config"]["num_speculative_tokens_per_batch_size"],256,c["speculative_config"]["num_speculative_tokens"])[b] for b in [1,2,4,5,16,17,32,256]}})) for c in cs if c["speculative_config"] and "num_speculative_tokens_per_batch_size" in c["speculative_config"]]; Path("results/processed/mtp-dynamic-schedule-lookup.json").write_text(json.dumps(out,indent=2)+"\n"); print(json.dumps(out,indent=2))'
```

## 246. policy-dspark-r1-dspark-k7-i1024-o512-c1-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:19:25.554611+00:00
- 结束：2026-11-24T15:20:52.895948+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k7-i1024-o512-c1-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k7-i1024-o512-c1-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 43 --request-id-prefix policy-dspark-r1-dspark-k7-i1024-o512-c1-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k7-i1024-o512-c1-s43.json --metadata method_name=dspark-k7 dataset_name=random mode=dspark k=7 gpu=2 phase=policy-dspark-r1 concurrency=1 seed=43 prefix_cache=false
```

## 247. 062-screen-mtp-dynamic-policies-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T15:19:35.701405+00:00
- 结束：2026-11-24T15:26:37.819521+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[062-screen-mtp-dynamic-policies-gpu3.log](/home/genai/spec_decoding_study/logs/commands/062-screen-mtp-dynamic-policies-gpu3.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/run_server_suite.py --config /home/genai/spec_decoding_study/config/mtp_policy_comparison.json --methods mtp-dynamic-oracle mtp-dynamic-smooth --gpu 3 --port 8103 --phase policy-mtp-screen --label-prefix 062 --num-prompts 32 --seeds 42 --concurrencies 32 16 4 1
```

## 248. 062-server-mtp-dynamic-oracle-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T15:19:35.780728+00:00
- 结束：2026-11-24T15:23:08.265532+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[062-server-mtp-dynamic-oracle-gpu3.log](/home/genai/spec_decoding_study/logs/commands/062-server-mtp-dynamic-oracle-gpu3.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8103 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"mtp","num_speculative_tokens":7,"num_speculative_tokens_per_batch_size":[[1,1,7],[2,4,6],[5,16,7],[17,256,5]]}'
```

## 249. 057-server-dspark-k3-gpu0

- 状态：completed；退出码：0
- 开始：2026-11-24T15:20:05.714108+00:00
- 结束：2026-11-24T15:24:52.075045+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[057-server-dspark-k3-gpu0.log](/home/genai/spec_decoding_study/logs/commands/057-server-dspark-k3-gpu0.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8100 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"dspark","num_speculative_tokens":3,"model":"/home/genai/models/Qwen3.8-27B-DSpark-vLLM"}'
```

## 250. warmup-policy-mtp-screen-mtp-dynamic-oracle-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:20:37.843746+00:00
- 结束：2026-11-24T15:20:50.519860+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-screen-mtp-dynamic-oracle-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-screen-mtp-dynamic-oracle-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-policy-mtp-screen-mtp-dynamic-oracle-c32-
```

## 251. policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:20:50.549364+00:00
- 结束：2026-11-24T15:21:03.136100+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c32-s42.json --metadata method_name=mtp-dynamic-oracle dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-screen concurrency=32 seed=42 prefix_cache=false
```

## 252. policy-dspark-r1-dspark-k7-i1024-o512-c1-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:20:52.928228+00:00
- 结束：2026-11-24T15:21:52.877183+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k7-i1024-o512-c1-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k7-i1024-o512-c1-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 44 --request-id-prefix policy-dspark-r1-dspark-k7-i1024-o512-c1-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k7-i1024-o512-c1-s44.json --metadata method_name=dspark-k7 dataset_name=random mode=dspark k=7 gpu=2 phase=policy-dspark-r1 concurrency=1 seed=44 prefix_cache=false
```

## 253. warmup-policy-mtp-screen-mtp-dynamic-oracle-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:21:03.166774+00:00
- 结束：2026-11-24T15:21:14.797376+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-screen-mtp-dynamic-oracle-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-screen-mtp-dynamic-oracle-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-policy-mtp-screen-mtp-dynamic-oracle-c16-
```

## 254. warmup-kscan-r1-dspark-k3-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:21:09.783844+00:00
- 结束：2026-11-24T15:21:26.212732+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-dspark-k3-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-dspark-k3-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-kscan-r1-dspark-k3-c32-
```

## 255. policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:21:14.826771+00:00
- 结束：2026-11-24T15:21:28.528219+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c16-s42.json --metadata method_name=mtp-dynamic-oracle dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-screen concurrency=16 seed=42 prefix_cache=false
```

## 256. kscan-r1-dspark-k3-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:21:26.241899+00:00
- 结束：2026-11-24T15:21:43.210096+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-dspark-k3-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-dspark-k3-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix kscan-r1-dspark-k3-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-dspark-k3-i1024-o512-c32-s42.json --metadata method_name=dspark-k3 dataset_name=random mode=dspark k=3 gpu=0 phase=kscan-r1 concurrency=32 seed=42 prefix_cache=false
```

## 257. warmup-policy-mtp-screen-mtp-dynamic-oracle-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T15:21:28.558379+00:00
- 结束：2026-11-24T15:21:39.075886+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-screen-mtp-dynamic-oracle-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-screen-mtp-dynamic-oracle-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-policy-mtp-screen-mtp-dynamic-oracle-c4-
```

## 258. policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:21:39.105503+00:00
- 结束：2026-11-24T15:22:00.419240+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c4-s42.json --metadata method_name=mtp-dynamic-oracle dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-screen concurrency=4 seed=42 prefix_cache=false
```

## 259. warmup-kscan-r1-dspark-k3-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:21:43.241469+00:00
- 结束：2026-11-24T15:21:58.953589+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-dspark-k3-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-dspark-k3-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-kscan-r1-dspark-k3-c16-
```

## 260. 054-server-dspark-adaptive-gpu2

- 状态：completed；退出码：0
- 开始：2026-11-24T15:21:54.770356+00:00
- 结束：2026-11-24T15:32:25.642853+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[054-server-dspark-adaptive-gpu2.log](/home/genai/spec_decoding_study/logs/commands/054-server-dspark-adaptive-gpu2.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8102 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"dspark","model":"/home/genai/models/Qwen3.8-27B-DSpark-vLLM","num_speculative_tokens":7,"enable_adaptive_verification":true}'
```

## 261. kscan-r1-dspark-k3-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:21:58.983681+00:00
- 结束：2026-11-24T15:22:19.683203+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-dspark-k3-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-dspark-k3-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix kscan-r1-dspark-k3-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-dspark-k3-i1024-o512-c16-s42.json --metadata method_name=dspark-k3 dataset_name=random mode=dspark k=3 gpu=0 phase=kscan-r1 concurrency=16 seed=42 prefix_cache=false
```

## 262. warmup-policy-mtp-screen-mtp-dynamic-oracle-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:22:00.449742+00:00
- 结束：2026-11-24T15:22:15.652583+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-screen-mtp-dynamic-oracle-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-screen-mtp-dynamic-oracle-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-policy-mtp-screen-mtp-dynamic-oracle-c1-
```

## 263. policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:22:15.689214+00:00
- 结束：2026-11-24T15:23:06.356123+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-screen-mtp-dynamic-oracle-i1024-o512-c1-s42.json --metadata method_name=mtp-dynamic-oracle dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-screen concurrency=1 seed=42 prefix_cache=false
```

## 264. warmup-kscan-r1-dspark-k3-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T15:22:19.714721+00:00
- 结束：2026-11-24T15:22:30.052697+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-dspark-k3-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-dspark-k3-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-kscan-r1-dspark-k3-c4-
```

## 265. kscan-r1-dspark-k3-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:22:30.082066+00:00
- 结束：2026-11-24T15:23:03.211175+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-dspark-k3-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-dspark-k3-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix kscan-r1-dspark-k3-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-dspark-k3-i1024-o512-c4-s42.json --metadata method_name=dspark-k3 dataset_name=random mode=dspark k=3 gpu=0 phase=kscan-r1 concurrency=4 seed=42 prefix_cache=false
```

## 266. semantic-r1-normal-specbench-o256-c1-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:22:30.805207+00:00
- 结束：2026-11-24T15:27:15.507929+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-normal-specbench-o256-c1-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-normal-specbench-o256-c1-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=1 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8101 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 44 --request-id-prefix semantic-r1-normal-specbench-o256-c1-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-normal-specbench-o256-c1-s44.json --metadata method_name=normal dataset_name=spec_bench mode=normal k=0 gpu=1 phase=semantic-r1 concurrency=1 seed=44 prefix_cache=false
```

## 267. warmup-kscan-r1-dspark-k3-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:23:03.243081+00:00
- 结束：2026-11-24T15:23:18.976913+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-dspark-k3-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-dspark-k3-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-kscan-r1-dspark-k3-c1-
```

## 268. 062-server-mtp-dynamic-smooth-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T15:23:08.246200+00:00
- 结束：2026-11-24T15:26:37.981309+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[062-server-mtp-dynamic-smooth-gpu3.log](/home/genai/spec_decoding_study/logs/commands/062-server-mtp-dynamic-smooth-gpu3.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8103 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"mtp","num_speculative_tokens":6,"num_speculative_tokens_per_batch_size":[[1,4,6],[5,256,5]]}'
```

## 269. kscan-r1-dspark-k3-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:23:19.006645+00:00
- 结束：2026-11-24T15:24:50.093130+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-dspark-k3-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-dspark-k3-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix kscan-r1-dspark-k3-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-dspark-k3-i1024-o512-c1-s42.json --metadata method_name=dspark-k3 dataset_name=random mode=dspark k=3 gpu=0 phase=kscan-r1 concurrency=1 seed=42 prefix_cache=false
```

## 270. warmup-policy-dspark-r1-dspark-adaptive-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:23:42.849133+00:00
- 结束：2026-11-24T15:23:59.842315+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-dspark-r1-dspark-adaptive-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-dspark-r1-dspark-adaptive-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-policy-dspark-r1-dspark-adaptive-c32-
```

## 271. policy-dspark-r1-dspark-adaptive-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:23:59.871927+00:00
- 结束：2026-11-24T15:24:17.388942+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-adaptive-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-adaptive-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix policy-dspark-r1-dspark-adaptive-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-adaptive-i1024-o512-c32-s42.json --metadata method_name=dspark-adaptive dataset_name=random mode=dspark k=-1 gpu=2 phase=policy-dspark-r1 concurrency=32 seed=42 prefix_cache=false
```

## 272. warmup-policy-mtp-screen-mtp-dynamic-smooth-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:24:08.310335+00:00
- 结束：2026-11-24T15:24:20.705508+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-screen-mtp-dynamic-smooth-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-screen-mtp-dynamic-smooth-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-policy-mtp-screen-mtp-dynamic-smooth-c32-
```

## 273. policy-dspark-r1-dspark-adaptive-i1024-o512-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:24:17.420742+00:00
- 结束：2026-11-24T15:24:34.976657+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-adaptive-i1024-o512-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-adaptive-i1024-o512-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix policy-dspark-r1-dspark-adaptive-i1024-o512-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-adaptive-i1024-o512-c32-s43.json --metadata method_name=dspark-adaptive dataset_name=random mode=dspark k=-1 gpu=2 phase=policy-dspark-r1 concurrency=32 seed=43 prefix_cache=false
```

## 274. policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:24:20.735217+00:00
- 结束：2026-11-24T15:24:33.584858+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c32-s42.json --metadata method_name=mtp-dynamic-smooth dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-screen concurrency=32 seed=42 prefix_cache=false
```

## 275. warmup-policy-mtp-screen-mtp-dynamic-smooth-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:24:33.615539+00:00
- 结束：2026-11-24T15:24:45.240306+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-screen-mtp-dynamic-smooth-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-screen-mtp-dynamic-smooth-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-policy-mtp-screen-mtp-dynamic-smooth-c16-
```

## 276. policy-dspark-r1-dspark-adaptive-i1024-o512-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:24:35.009850+00:00
- 结束：2026-11-24T15:24:52.183101+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-adaptive-i1024-o512-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-adaptive-i1024-o512-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix policy-dspark-r1-dspark-adaptive-i1024-o512-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-adaptive-i1024-o512-c32-s44.json --metadata method_name=dspark-adaptive dataset_name=random mode=dspark k=-1 gpu=2 phase=policy-dspark-r1 concurrency=32 seed=44 prefix_cache=false
```

## 277. policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:24:45.274404+00:00
- 结束：2026-11-24T15:24:58.661256+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c16-s42.json --metadata method_name=mtp-dynamic-smooth dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-screen concurrency=16 seed=42 prefix_cache=false
```

## 278. 057-server-dspark-k5-gpu0

- 状态：completed；退出码：0
- 开始：2026-11-24T15:24:52.188849+00:00
- 结束：2026-11-24T15:29:37.517696+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[057-server-dspark-k5-gpu0.log](/home/genai/spec_decoding_study/logs/commands/057-server-dspark-k5-gpu0.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8100 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"dspark","num_speculative_tokens":5,"model":"/home/genai/models/Qwen3.8-27B-DSpark-vLLM"}'
```

## 279. warmup-policy-dspark-r1-dspark-adaptive-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:24:52.214951+00:00
- 结束：2026-11-24T15:25:08.018581+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-dspark-r1-dspark-adaptive-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-dspark-r1-dspark-adaptive-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-policy-dspark-r1-dspark-adaptive-c16-
```

## 280. warmup-policy-mtp-screen-mtp-dynamic-smooth-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T15:24:58.691887+00:00
- 结束：2026-11-24T15:25:08.579771+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-screen-mtp-dynamic-smooth-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-screen-mtp-dynamic-smooth-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-policy-mtp-screen-mtp-dynamic-smooth-c4-
```

## 281. policy-dspark-r1-dspark-adaptive-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:25:08.048714+00:00
- 结束：2026-11-24T15:25:27.899347+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-adaptive-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-adaptive-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix policy-dspark-r1-dspark-adaptive-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-adaptive-i1024-o512-c16-s42.json --metadata method_name=dspark-adaptive dataset_name=random mode=dspark k=-1 gpu=2 phase=policy-dspark-r1 concurrency=16 seed=42 prefix_cache=false
```

## 282. policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:25:08.609752+00:00
- 结束：2026-11-24T15:25:30.333790+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c4-s42.json --metadata method_name=mtp-dynamic-smooth dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-screen concurrency=4 seed=42 prefix_cache=false
```

## 283. policy-dspark-r1-dspark-adaptive-i1024-o512-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:25:27.930921+00:00
- 结束：2026-11-24T15:25:48.298114+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-adaptive-i1024-o512-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-adaptive-i1024-o512-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix policy-dspark-r1-dspark-adaptive-i1024-o512-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-adaptive-i1024-o512-c16-s43.json --metadata method_name=dspark-adaptive dataset_name=random mode=dspark k=-1 gpu=2 phase=policy-dspark-r1 concurrency=16 seed=43 prefix_cache=false
```

## 284. warmup-policy-mtp-screen-mtp-dynamic-smooth-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:25:30.364221+00:00
- 结束：2026-11-24T15:25:44.918702+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-screen-mtp-dynamic-smooth-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-screen-mtp-dynamic-smooth-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-policy-mtp-screen-mtp-dynamic-smooth-c1-
```

## 285. policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:25:44.948347+00:00
- 结束：2026-11-24T15:26:35.971804+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-screen-mtp-dynamic-smooth-i1024-o512-c1-s42.json --metadata method_name=mtp-dynamic-smooth dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-screen concurrency=1 seed=42 prefix_cache=false
```

## 286. policy-dspark-r1-dspark-adaptive-i1024-o512-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:25:48.333421+00:00
- 结束：2026-11-24T15:26:07.720377+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-adaptive-i1024-o512-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-adaptive-i1024-o512-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix policy-dspark-r1-dspark-adaptive-i1024-o512-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-adaptive-i1024-o512-c16-s44.json --metadata method_name=dspark-adaptive dataset_name=random mode=dspark k=-1 gpu=2 phase=policy-dspark-r1 concurrency=16 seed=44 prefix_cache=false
```

## 287. warmup-kscan-r1-dspark-k5-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:25:58.255597+00:00
- 结束：2026-11-24T15:26:15.493209+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-dspark-k5-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-dspark-k5-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-kscan-r1-dspark-k5-c32-
```

## 288. warmup-policy-dspark-r1-dspark-adaptive-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T15:26:07.751738+00:00
- 结束：2026-11-24T15:26:18.186335+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-dspark-r1-dspark-adaptive-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-dspark-r1-dspark-adaptive-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-policy-dspark-r1-dspark-adaptive-c4-
```

## 289. kscan-r1-dspark-k5-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:26:15.522747+00:00
- 结束：2026-11-24T15:26:32.923513+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-dspark-k5-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-dspark-k5-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix kscan-r1-dspark-k5-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-dspark-k5-i1024-o512-c32-s42.json --metadata method_name=dspark-k5 dataset_name=random mode=dspark k=5 gpu=0 phase=kscan-r1 concurrency=32 seed=42 prefix_cache=false
```

## 290. policy-dspark-r1-dspark-adaptive-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:26:18.216486+00:00
- 结束：2026-11-24T15:26:52.471400+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-adaptive-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-adaptive-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix policy-dspark-r1-dspark-adaptive-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-adaptive-i1024-o512-c4-s42.json --metadata method_name=dspark-adaptive dataset_name=random mode=dspark k=-1 gpu=2 phase=policy-dspark-r1 concurrency=4 seed=42 prefix_cache=false
```

## 291. warmup-kscan-r1-dspark-k5-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:26:32.954934+00:00
- 结束：2026-11-24T15:26:48.614099+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-dspark-k5-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-dspark-k5-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-kscan-r1-dspark-k5-c16-
```

## 292. kscan-r1-dspark-k5-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:26:48.643605+00:00
- 结束：2026-11-24T15:27:08.451447+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-dspark-k5-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-dspark-k5-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix kscan-r1-dspark-k5-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-dspark-k5-i1024-o512-c16-s42.json --metadata method_name=dspark-k5 dataset_name=random mode=dspark k=5 gpu=0 phase=kscan-r1 concurrency=16 seed=42 prefix_cache=false
```

## 293. policy-dspark-r1-dspark-adaptive-i1024-o512-c4-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:26:52.503407+00:00
- 结束：2026-11-24T15:27:28.091663+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-adaptive-i1024-o512-c4-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-adaptive-i1024-o512-c4-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 43 --request-id-prefix policy-dspark-r1-dspark-adaptive-i1024-o512-c4-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-adaptive-i1024-o512-c4-s43.json --metadata method_name=dspark-adaptive dataset_name=random mode=dspark k=-1 gpu=2 phase=policy-dspark-r1 concurrency=4 seed=43 prefix_cache=false
```

## 294. warmup-kscan-r1-dspark-k5-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T15:27:08.483252+00:00
- 结束：2026-11-24T15:27:18.883877+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-dspark-k5-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-dspark-k5-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-kscan-r1-dspark-k5-c4-
```

## 295. kscan-r1-dspark-k5-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:27:18.913197+00:00
- 结束：2026-11-24T15:27:53.243172+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-dspark-k5-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-dspark-k5-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix kscan-r1-dspark-k5-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-dspark-k5-i1024-o512-c4-s42.json --metadata method_name=dspark-k5 dataset_name=random mode=dspark k=5 gpu=0 phase=kscan-r1 concurrency=4 seed=42 prefix_cache=false
```

## 296. policy-dspark-r1-dspark-adaptive-i1024-o512-c4-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:27:28.123711+00:00
- 结束：2026-11-24T15:27:57.170471+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-adaptive-i1024-o512-c4-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-adaptive-i1024-o512-c4-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 44 --request-id-prefix policy-dspark-r1-dspark-adaptive-i1024-o512-c4-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-adaptive-i1024-o512-c4-s44.json --metadata method_name=dspark-adaptive dataset_name=random mode=dspark k=-1 gpu=2 phase=policy-dspark-r1 concurrency=4 seed=44 prefix_cache=false
```

## 297. warmup-kscan-r1-dspark-k5-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:27:53.275065+00:00
- 结束：2026-11-24T15:28:07.776464+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-dspark-k5-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-dspark-k5-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-kscan-r1-dspark-k5-c1-
```

## 298. warmup-policy-dspark-r1-dspark-adaptive-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:27:57.201022+00:00
- 结束：2026-11-24T15:28:11.565471+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-dspark-r1-dspark-adaptive-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-dspark-r1-dspark-adaptive-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-policy-dspark-r1-dspark-adaptive-c1-
```

## 299. kscan-r1-dspark-k5-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:28:07.807699+00:00
- 结束：2026-11-24T15:29:35.065675+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-dspark-k5-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-dspark-k5-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix kscan-r1-dspark-k5-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-dspark-k5-i1024-o512-c1-s42.json --metadata method_name=dspark-k5 dataset_name=random mode=dspark k=5 gpu=0 phase=kscan-r1 concurrency=1 seed=42 prefix_cache=false
```

## 300. policy-dspark-r1-dspark-adaptive-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:28:11.595365+00:00
- 结束：2026-11-24T15:29:45.859378+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-adaptive-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-adaptive-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix policy-dspark-r1-dspark-adaptive-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-adaptive-i1024-o512-c1-s42.json --metadata method_name=dspark-adaptive dataset_name=random mode=dspark k=-1 gpu=2 phase=policy-dspark-r1 concurrency=1 seed=42 prefix_cache=false
```

## 301. 057-server-dspark-k7-gpu0

- 状态：completed；退出码：0
- 开始：2026-11-24T15:29:37.557902+00:00
- 结束：2026-11-24T15:34:32.412001+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[057-server-dspark-k7-gpu0.log](/home/genai/spec_decoding_study/logs/commands/057-server-dspark-k7-gpu0.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8100 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"dspark","num_speculative_tokens":7,"model":"/home/genai/models/Qwen3.8-27B-DSpark-vLLM"}'
```

## 302. policy-dspark-r1-dspark-adaptive-i1024-o512-c1-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:29:45.890449+00:00
- 结束：2026-11-24T15:31:14.561876+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-adaptive-i1024-o512-c1-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-adaptive-i1024-o512-c1-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 43 --request-id-prefix policy-dspark-r1-dspark-adaptive-i1024-o512-c1-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-adaptive-i1024-o512-c1-s43.json --metadata method_name=dspark-adaptive dataset_name=random mode=dspark k=-1 gpu=2 phase=policy-dspark-r1 concurrency=1 seed=43 prefix_cache=false
```

## 303. warmup-kscan-r1-dspark-k7-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:30:49.624975+00:00
- 结束：2026-11-24T15:31:07.879716+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-dspark-k7-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-dspark-k7-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-kscan-r1-dspark-k7-c32-
```

## 304. kscan-r1-dspark-k7-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:31:07.908941+00:00
- 结束：2026-11-24T15:31:27.118708+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-dspark-k7-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-dspark-k7-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix kscan-r1-dspark-k7-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-dspark-k7-i1024-o512-c32-s42.json --metadata method_name=dspark-k7 dataset_name=random mode=dspark k=7 gpu=0 phase=kscan-r1 concurrency=32 seed=42 prefix_cache=false
```

## 305. policy-dspark-r1-dspark-adaptive-i1024-o512-c1-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:31:14.593749+00:00
- 结束：2026-11-24T15:32:22.377612+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-adaptive-i1024-o512-c1-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-adaptive-i1024-o512-c1-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 44 --request-id-prefix policy-dspark-r1-dspark-adaptive-i1024-o512-c1-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-adaptive-i1024-o512-c1-s44.json --metadata method_name=dspark-adaptive dataset_name=random mode=dspark k=-1 gpu=2 phase=policy-dspark-r1 concurrency=1 seed=44 prefix_cache=false
```

## 306. warmup-kscan-r1-dspark-k7-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:31:27.150464+00:00
- 结束：2026-11-24T15:31:44.112875+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-dspark-k7-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-dspark-k7-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-kscan-r1-dspark-k7-c16-
```

## 307. kscan-r1-dspark-k7-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:31:44.142788+00:00
- 结束：2026-11-24T15:32:04.496009+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-dspark-k7-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-dspark-k7-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix kscan-r1-dspark-k7-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-dspark-k7-i1024-o512-c16-s42.json --metadata method_name=dspark-k7 dataset_name=random mode=dspark k=7 gpu=0 phase=kscan-r1 concurrency=16 seed=42 prefix_cache=false
```

## 308. warmup-kscan-r1-dspark-k7-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T15:32:04.528076+00:00
- 结束：2026-11-24T15:32:15.798272+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-dspark-k7-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-dspark-k7-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-kscan-r1-dspark-k7-c4-
```

## 309. kscan-r1-dspark-k7-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:32:15.827837+00:00
- 结束：2026-11-24T15:32:49.789032+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-dspark-k7-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-dspark-k7-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix kscan-r1-dspark-k7-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-dspark-k7-i1024-o512-c4-s42.json --metadata method_name=dspark-k7 dataset_name=random mode=dspark k=7 gpu=0 phase=kscan-r1 concurrency=4 seed=42 prefix_cache=false
```

## 310. warmup-kscan-r1-dspark-k7-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:32:49.820843+00:00
- 结束：2026-11-24T15:33:04.455163+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-kscan-r1-dspark-k7-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-kscan-r1-dspark-k7-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-kscan-r1-dspark-k7-c1-
```

## 311. kscan-r1-dspark-k7-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:33:04.485445+00:00
- 结束：2026-11-24T15:34:30.312297+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[kscan-r1-dspark-k7-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/kscan-r1-dspark-k7-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=0 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8100 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix kscan-r1-dspark-k7-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename kscan-r1-dspark-k7-i1024-o512-c1-s42.json --metadata method_name=dspark-k7 dataset_name=random mode=dspark k=7 gpu=0 phase=kscan-r1 concurrency=1 seed=42 prefix_cache=false
```

## 312. 063-policy-mtp-final-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T15:35:25.795990+00:00
- 结束：2026-11-24T16:30:49.524591+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[063-policy-mtp-final-gpu3.log](/home/genai/spec_decoding_study/logs/commands/063-policy-mtp-final-gpu3.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/run_server_suite.py --config /home/genai/spec_decoding_study/config/mtp_policy_comparison.json --gpu 3 --port 8103 --phase policy-mtp-r1 --label-prefix 063 --num-prompts 32 --seeds 42 43 44 --concurrencies 32 16 4 1
```

## 313. 063-server-normal-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T15:35:25.867424+00:00
- 结束：2026-11-24T15:49:01.564989+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[063-server-normal-gpu3.log](/home/genai/spec_decoding_study/logs/commands/063-server-normal-gpu3.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8103 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0
```

## 314. 064-semantic-dspark-adaptive-gpu2

- 状态：completed；退出码：0
- 开始：2026-11-24T15:35:59.987269+00:00
- 结束：2026-11-24T15:48:30.721888+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[064-semantic-dspark-adaptive-gpu2.log](/home/genai/spec_decoding_study/logs/commands/064-semantic-dspark-adaptive-gpu2.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/run_server_suite.py --config /home/genai/spec_decoding_study/config/dspark_policy_comparison.json --methods dspark-adaptive --gpu 2 --port 8102 --phase semantic-r1 --label-prefix 064 --num-prompts 128 --seeds 42 43 44 --concurrencies 32 16 4 1 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --output-len 256
```

## 315. 064-server-dspark-adaptive-gpu2

- 状态：completed；退出码：0
- 开始：2026-11-24T15:36:00.058800+00:00
- 结束：2026-11-24T15:48:30.852453+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[064-server-dspark-adaptive-gpu2.log](/home/genai/spec_decoding_study/logs/commands/064-server-dspark-adaptive-gpu2.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8102 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"dspark","model":"/home/genai/models/Qwen3.8-27B-DSpark-vLLM","num_speculative_tokens":7,"enable_adaptive_verification":true}'
```

## 316. warmup-policy-mtp-r1-normal-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:36:23.930600+00:00
- 结束：2026-11-24T15:36:38.972858+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-normal-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-normal-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-policy-mtp-r1-normal-c32-
```

## 317. policy-mtp-r1-normal-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:36:39.002066+00:00
- 结束：2026-11-24T15:36:54.092449+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-normal-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-normal-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix policy-mtp-r1-normal-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-normal-i1024-o512-c32-s42.json --metadata method_name=normal dataset_name=random mode=normal k=0 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=42 prefix_cache=false
```

## 318. policy-mtp-r1-normal-i1024-o512-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:36:54.125679+00:00
- 结束：2026-11-24T15:37:09.030641+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-normal-i1024-o512-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-normal-i1024-o512-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix policy-mtp-r1-normal-i1024-o512-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-normal-i1024-o512-c32-s43.json --metadata method_name=normal dataset_name=random mode=normal k=0 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=43 prefix_cache=false
```

## 319. policy-mtp-r1-normal-i1024-o512-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:37:09.063629+00:00
- 结束：2026-11-24T15:37:23.919868+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-normal-i1024-o512-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-normal-i1024-o512-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix policy-mtp-r1-normal-i1024-o512-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-normal-i1024-o512-c32-s44.json --metadata method_name=normal dataset_name=random mode=normal k=0 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=44 prefix_cache=false
```

## 320. warmup-policy-mtp-r1-normal-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:37:23.953473+00:00
- 结束：2026-11-24T15:37:37.511960+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-normal-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-normal-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-policy-mtp-r1-normal-c16-
```

## 321. policy-mtp-r1-normal-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:37:37.542875+00:00
- 结束：2026-11-24T15:37:56.880971+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-normal-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-normal-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix policy-mtp-r1-normal-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-normal-i1024-o512-c16-s42.json --metadata method_name=normal dataset_name=random mode=normal k=0 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=42 prefix_cache=false
```

## 322. warmup-semantic-r1-dspark-adaptive-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:37:40.134506+00:00
- 结束：2026-11-24T15:37:50.391147+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-dspark-adaptive-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-dspark-adaptive-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-semantic-r1-dspark-adaptive-c32-
```

## 323. semantic-r1-dspark-adaptive-specbench-o256-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:37:50.420638+00:00
- 结束：2026-11-24T15:38:07.447101+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-adaptive-specbench-o256-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-adaptive-specbench-o256-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix semantic-r1-dspark-adaptive-specbench-o256-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-adaptive-specbench-o256-c32-s42.json --metadata method_name=dspark-adaptive dataset_name=spec_bench mode=dspark k=-1 gpu=2 phase=semantic-r1 concurrency=32 seed=42 prefix_cache=false
```

## 324. policy-mtp-r1-normal-i1024-o512-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:37:56.915109+00:00
- 结束：2026-11-24T15:38:16.144784+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-normal-i1024-o512-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-normal-i1024-o512-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix policy-mtp-r1-normal-i1024-o512-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-normal-i1024-o512-c16-s43.json --metadata method_name=normal dataset_name=random mode=normal k=0 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=43 prefix_cache=false
```

## 325. semantic-r1-dspark-adaptive-specbench-o256-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:38:07.479464+00:00
- 结束：2026-11-24T15:38:24.410525+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-adaptive-specbench-o256-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-adaptive-specbench-o256-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix semantic-r1-dspark-adaptive-specbench-o256-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-adaptive-specbench-o256-c32-s43.json --metadata method_name=dspark-adaptive dataset_name=spec_bench mode=dspark k=-1 gpu=2 phase=semantic-r1 concurrency=32 seed=43 prefix_cache=false
```

## 326. policy-mtp-r1-normal-i1024-o512-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:38:16.181078+00:00
- 结束：2026-11-24T15:38:35.347992+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-normal-i1024-o512-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-normal-i1024-o512-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix policy-mtp-r1-normal-i1024-o512-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-normal-i1024-o512-c16-s44.json --metadata method_name=normal dataset_name=random mode=normal k=0 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=44 prefix_cache=false
```

## 327. semantic-r1-dspark-adaptive-specbench-o256-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:38:24.442923+00:00
- 结束：2026-11-24T15:38:41.942390+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-adaptive-specbench-o256-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-adaptive-specbench-o256-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix semantic-r1-dspark-adaptive-specbench-o256-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-adaptive-specbench-o256-c32-s44.json --metadata method_name=dspark-adaptive dataset_name=spec_bench mode=dspark k=-1 gpu=2 phase=semantic-r1 concurrency=32 seed=44 prefix_cache=false
```

## 328. warmup-policy-mtp-r1-normal-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T15:38:35.380574+00:00
- 结束：2026-11-24T15:38:47.853386+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-normal-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-normal-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-policy-mtp-r1-normal-c4-
```

## 329. warmup-semantic-r1-dspark-adaptive-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:38:41.976700+00:00
- 结束：2026-11-24T15:38:51.691907+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-dspark-adaptive-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-dspark-adaptive-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-semantic-r1-dspark-adaptive-c16-
```

## 330. policy-mtp-r1-normal-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:38:47.883259+00:00
- 结束：2026-11-24T15:39:33.652838+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-normal-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-normal-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix policy-mtp-r1-normal-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-normal-i1024-o512-c4-s42.json --metadata method_name=normal dataset_name=random mode=normal k=0 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=42 prefix_cache=false
```

## 331. semantic-r1-dspark-adaptive-specbench-o256-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:38:51.720980+00:00
- 结束：2026-11-24T15:39:13.033762+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-adaptive-specbench-o256-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-adaptive-specbench-o256-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix semantic-r1-dspark-adaptive-specbench-o256-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-adaptive-specbench-o256-c16-s42.json --metadata method_name=dspark-adaptive dataset_name=spec_bench mode=dspark k=-1 gpu=2 phase=semantic-r1 concurrency=16 seed=42 prefix_cache=false
```

## 332. semantic-r1-dspark-adaptive-specbench-o256-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:39:13.066609+00:00
- 结束：2026-11-24T15:39:34.046468+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-adaptive-specbench-o256-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-adaptive-specbench-o256-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix semantic-r1-dspark-adaptive-specbench-o256-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-adaptive-specbench-o256-c16-s43.json --metadata method_name=dspark-adaptive dataset_name=spec_bench mode=dspark k=-1 gpu=2 phase=semantic-r1 concurrency=16 seed=43 prefix_cache=false
```

## 333. policy-mtp-r1-normal-i1024-o512-c4-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:39:33.686832+00:00
- 结束：2026-11-24T15:40:20.241142+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-normal-i1024-o512-c4-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-normal-i1024-o512-c4-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 43 --request-id-prefix policy-mtp-r1-normal-i1024-o512-c4-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-normal-i1024-o512-c4-s43.json --metadata method_name=normal dataset_name=random mode=normal k=0 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=43 prefix_cache=false
```

## 334. semantic-r1-dspark-adaptive-specbench-o256-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:39:34.083762+00:00
- 结束：2026-11-24T15:39:55.291473+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-adaptive-specbench-o256-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-adaptive-specbench-o256-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix semantic-r1-dspark-adaptive-specbench-o256-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-adaptive-specbench-o256-c16-s44.json --metadata method_name=dspark-adaptive dataset_name=spec_bench mode=dspark k=-1 gpu=2 phase=semantic-r1 concurrency=16 seed=44 prefix_cache=false
```

## 335. warmup-semantic-r1-dspark-adaptive-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T15:39:55.324264+00:00
- 结束：2026-11-24T15:40:04.723070+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-dspark-adaptive-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-dspark-adaptive-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-semantic-r1-dspark-adaptive-c4-
```

## 336. semantic-r1-dspark-adaptive-specbench-o256-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:40:04.752787+00:00
- 结束：2026-11-24T15:40:46.864112+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-adaptive-specbench-o256-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-adaptive-specbench-o256-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix semantic-r1-dspark-adaptive-specbench-o256-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-adaptive-specbench-o256-c4-s42.json --metadata method_name=dspark-adaptive dataset_name=spec_bench mode=dspark k=-1 gpu=2 phase=semantic-r1 concurrency=4 seed=42 prefix_cache=false
```

## 337. policy-mtp-r1-normal-i1024-o512-c4-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:40:20.274730+00:00
- 结束：2026-11-24T15:41:06.412447+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-normal-i1024-o512-c4-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-normal-i1024-o512-c4-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 44 --request-id-prefix policy-mtp-r1-normal-i1024-o512-c4-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-normal-i1024-o512-c4-s44.json --metadata method_name=normal dataset_name=random mode=normal k=0 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=44 prefix_cache=false
```

## 338. semantic-r1-dspark-adaptive-specbench-o256-c4-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:40:46.896603+00:00
- 结束：2026-11-24T15:41:29.901528+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-adaptive-specbench-o256-c4-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-adaptive-specbench-o256-c4-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 43 --request-id-prefix semantic-r1-dspark-adaptive-specbench-o256-c4-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-adaptive-specbench-o256-c4-s43.json --metadata method_name=dspark-adaptive dataset_name=spec_bench mode=dspark k=-1 gpu=2 phase=semantic-r1 concurrency=4 seed=43 prefix_cache=false
```

## 339. warmup-policy-mtp-r1-normal-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:41:06.450786+00:00
- 结束：2026-11-24T15:41:31.866912+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-normal-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-normal-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-policy-mtp-r1-normal-c1-
```

## 340. semantic-r1-dspark-adaptive-specbench-o256-c4-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:41:29.934364+00:00
- 结束：2026-11-24T15:42:12.666056+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-adaptive-specbench-o256-c4-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-adaptive-specbench-o256-c4-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 4 --seed 44 --request-id-prefix semantic-r1-dspark-adaptive-specbench-o256-c4-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-adaptive-specbench-o256-c4-s44.json --metadata method_name=dspark-adaptive dataset_name=spec_bench mode=dspark k=-1 gpu=2 phase=semantic-r1 concurrency=4 seed=44 prefix_cache=false
```

## 341. policy-mtp-r1-normal-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:41:31.897215+00:00
- 结束：2026-11-24T15:44:00.834773+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-normal-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-normal-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix policy-mtp-r1-normal-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-normal-i1024-o512-c1-s42.json --metadata method_name=normal dataset_name=random mode=normal k=0 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=42 prefix_cache=false
```

## 342. warmup-semantic-r1-dspark-adaptive-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:42:12.758382+00:00
- 结束：2026-11-24T15:42:24.294078+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-dspark-adaptive-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-dspark-adaptive-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-semantic-r1-dspark-adaptive-c1-
```

## 343. semantic-r1-dspark-adaptive-specbench-o256-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:42:24.327862+00:00
- 结束：2026-11-24T15:44:25.421543+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-adaptive-specbench-o256-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-adaptive-specbench-o256-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix semantic-r1-dspark-adaptive-specbench-o256-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-adaptive-specbench-o256-c1-s42.json --metadata method_name=dspark-adaptive dataset_name=spec_bench mode=dspark k=-1 gpu=2 phase=semantic-r1 concurrency=1 seed=42 prefix_cache=false
```

## 344. policy-mtp-r1-normal-i1024-o512-c1-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:44:00.877459+00:00
- 结束：2026-11-24T15:46:29.979618+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-normal-i1024-o512-c1-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-normal-i1024-o512-c1-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 43 --request-id-prefix policy-mtp-r1-normal-i1024-o512-c1-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-normal-i1024-o512-c1-s43.json --metadata method_name=normal dataset_name=random mode=normal k=0 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=43 prefix_cache=false
```

## 345. semantic-r1-dspark-adaptive-specbench-o256-c1-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:44:25.458283+00:00
- 结束：2026-11-24T15:46:27.257223+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-adaptive-specbench-o256-c1-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-adaptive-specbench-o256-c1-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 43 --request-id-prefix semantic-r1-dspark-adaptive-specbench-o256-c1-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-adaptive-specbench-o256-c1-s43.json --metadata method_name=dspark-adaptive dataset_name=spec_bench mode=dspark k=-1 gpu=2 phase=semantic-r1 concurrency=1 seed=43 prefix_cache=false
```

## 346. semantic-r1-dspark-adaptive-specbench-o256-c1-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:46:27.295666+00:00
- 结束：2026-11-24T15:48:28.671545+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-adaptive-specbench-o256-c1-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-adaptive-specbench-o256-c1-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 1 --seed 44 --request-id-prefix semantic-r1-dspark-adaptive-specbench-o256-c1-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-adaptive-specbench-o256-c1-s44.json --metadata method_name=dspark-adaptive dataset_name=spec_bench mode=dspark k=-1 gpu=2 phase=semantic-r1 concurrency=1 seed=44 prefix_cache=false
```

## 347. policy-mtp-r1-normal-i1024-o512-c1-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:46:30.017500+00:00
- 结束：2026-11-24T15:48:59.570681+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-normal-i1024-o512-c1-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-normal-i1024-o512-c1-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 44 --request-id-prefix policy-mtp-r1-normal-i1024-o512-c1-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-normal-i1024-o512-c1-s44.json --metadata method_name=normal dataset_name=random mode=normal k=0 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=44 prefix_cache=false
```

## 348. 063-server-mtp-k3-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T15:49:01.465445+00:00
- 结束：2026-11-24T15:56:27.888974+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[063-server-mtp-k3-gpu3.log](/home/genai/spec_decoding_study/logs/commands/063-server-mtp-k3-gpu3.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8103 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"mtp","num_speculative_tokens":3}'
```

## 349. warmup-policy-mtp-r1-mtp-k3-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:50:01.528306+00:00
- 结束：2026-11-24T15:50:14.171397+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-k3-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-k3-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-policy-mtp-r1-mtp-k3-c32-
```

## 350. policy-mtp-r1-mtp-k3-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:50:14.201073+00:00
- 结束：2026-11-24T15:50:27.121662+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k3-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k3-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix policy-mtp-r1-mtp-k3-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k3-i1024-o512-c32-s42.json --metadata method_name=mtp-k3 dataset_name=random mode=mtp k=3 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=42 prefix_cache=false
```

## 351. policy-mtp-r1-mtp-k3-i1024-o512-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:50:27.152360+00:00
- 结束：2026-11-24T15:50:39.393790+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k3-i1024-o512-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k3-i1024-o512-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix policy-mtp-r1-mtp-k3-i1024-o512-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k3-i1024-o512-c32-s43.json --metadata method_name=mtp-k3 dataset_name=random mode=mtp k=3 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=43 prefix_cache=false
```

## 352. policy-mtp-r1-mtp-k3-i1024-o512-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:50:39.424675+00:00
- 结束：2026-11-24T15:50:51.893859+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k3-i1024-o512-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k3-i1024-o512-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix policy-mtp-r1-mtp-k3-i1024-o512-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k3-i1024-o512-c32-s44.json --metadata method_name=mtp-k3 dataset_name=random mode=mtp k=3 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=44 prefix_cache=false
```

## 353. warmup-policy-mtp-r1-mtp-k3-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:50:51.924512+00:00
- 结束：2026-11-24T15:51:04.246293+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-k3-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-k3-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-policy-mtp-r1-mtp-k3-c16-
```

## 354. policy-mtp-r1-mtp-k3-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:51:04.278013+00:00
- 结束：2026-11-24T15:51:19.844485+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k3-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k3-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix policy-mtp-r1-mtp-k3-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k3-i1024-o512-c16-s42.json --metadata method_name=mtp-k3 dataset_name=random mode=mtp k=3 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=42 prefix_cache=false
```

## 355. policy-mtp-r1-mtp-k3-i1024-o512-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:51:19.875094+00:00
- 结束：2026-11-24T15:51:35.273533+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k3-i1024-o512-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k3-i1024-o512-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix policy-mtp-r1-mtp-k3-i1024-o512-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k3-i1024-o512-c16-s43.json --metadata method_name=mtp-k3 dataset_name=random mode=mtp k=3 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=43 prefix_cache=false
```

## 356. policy-mtp-r1-mtp-k3-i1024-o512-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:51:35.305033+00:00
- 结束：2026-11-24T15:51:50.313633+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k3-i1024-o512-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k3-i1024-o512-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix policy-mtp-r1-mtp-k3-i1024-o512-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k3-i1024-o512-c16-s44.json --metadata method_name=mtp-k3 dataset_name=random mode=mtp k=3 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=44 prefix_cache=false
```

## 357. 065-policy-dspark-fixed-high-gpu2

- 状态：completed；退出码：0
- 开始：2026-11-24T15:51:48.595919+00:00
- 结束：2026-11-24T15:58:47.355515+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[065-policy-dspark-fixed-high-gpu2.log](/home/genai/spec_decoding_study/logs/commands/065-policy-dspark-fixed-high-gpu2.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/run_k_scan.py --method dspark --ks 1 3 --gpu 2 --port 8102 --phase policy-dspark-r1 --label-prefix 065 --num-prompts 32 --seeds 42 43 44 --concurrencies 32 16
```

## 358. 065-server-dspark-k1-gpu2

- 状态：completed；退出码：0
- 开始：2026-11-24T15:51:48.666719+00:00
- 结束：2026-11-24T15:55:18.112825+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[065-server-dspark-k1-gpu2.log](/home/genai/spec_decoding_study/logs/commands/065-server-dspark-k1-gpu2.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8102 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"dspark","num_speculative_tokens":1,"model":"/home/genai/models/Qwen3.8-27B-DSpark-vLLM"}'
```

## 359. warmup-policy-mtp-r1-mtp-k3-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T15:51:50.344285+00:00
- 结束：2026-11-24T15:52:00.710244+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-k3-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-k3-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-policy-mtp-r1-mtp-k3-c4-
```

## 360. policy-mtp-r1-mtp-k3-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:52:00.739937+00:00
- 结束：2026-11-24T15:52:25.026486+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k3-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k3-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix policy-mtp-r1-mtp-k3-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k3-i1024-o512-c4-s42.json --metadata method_name=mtp-k3 dataset_name=random mode=mtp k=3 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=42 prefix_cache=false
```

## 361. policy-mtp-r1-mtp-k3-i1024-o512-c4-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:52:25.057894+00:00
- 结束：2026-11-24T15:52:49.111125+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k3-i1024-o512-c4-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k3-i1024-o512-c4-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 43 --request-id-prefix policy-mtp-r1-mtp-k3-i1024-o512-c4-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k3-i1024-o512-c4-s43.json --metadata method_name=mtp-k3 dataset_name=random mode=mtp k=3 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=43 prefix_cache=false
```

## 362. policy-mtp-r1-mtp-k3-i1024-o512-c4-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:52:49.142183+00:00
- 结束：2026-11-24T15:53:12.540029+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k3-i1024-o512-c4-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k3-i1024-o512-c4-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 44 --request-id-prefix policy-mtp-r1-mtp-k3-i1024-o512-c4-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k3-i1024-o512-c4-s44.json --metadata method_name=mtp-k3 dataset_name=random mode=mtp k=3 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=44 prefix_cache=false
```

## 363. warmup-policy-dspark-r1-dspark-k1-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:52:52.731779+00:00
- 结束：2026-11-24T15:53:10.033329+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-dspark-r1-dspark-k1-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-dspark-r1-dspark-k1-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-policy-dspark-r1-dspark-k1-c32-
```

## 364. policy-dspark-r1-dspark-k1-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:53:10.062368+00:00
- 结束：2026-11-24T15:53:27.774040+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k1-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k1-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix policy-dspark-r1-dspark-k1-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k1-i1024-o512-c32-s42.json --metadata method_name=dspark-k1 dataset_name=random mode=dspark k=1 gpu=2 phase=policy-dspark-r1 concurrency=32 seed=42 prefix_cache=false
```

## 365. warmup-policy-mtp-r1-mtp-k3-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T15:53:12.571259+00:00
- 结束：2026-11-24T15:53:27.279930+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-k3-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-k3-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-policy-mtp-r1-mtp-k3-c1-
```

## 366. policy-mtp-r1-mtp-k3-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:53:27.309393+00:00
- 结束：2026-11-24T15:54:26.822438+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k3-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k3-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix policy-mtp-r1-mtp-k3-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k3-i1024-o512-c1-s42.json --metadata method_name=mtp-k3 dataset_name=random mode=mtp k=3 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=42 prefix_cache=false
```

## 367. policy-dspark-r1-dspark-k1-i1024-o512-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:53:27.807085+00:00
- 结束：2026-11-24T15:53:45.072688+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k1-i1024-o512-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k1-i1024-o512-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix policy-dspark-r1-dspark-k1-i1024-o512-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k1-i1024-o512-c32-s43.json --metadata method_name=dspark-k1 dataset_name=random mode=dspark k=1 gpu=2 phase=policy-dspark-r1 concurrency=32 seed=43 prefix_cache=false
```

## 368. policy-dspark-r1-dspark-k1-i1024-o512-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:53:45.104944+00:00
- 结束：2026-11-24T15:54:02.331841+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k1-i1024-o512-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k1-i1024-o512-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix policy-dspark-r1-dspark-k1-i1024-o512-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k1-i1024-o512-c32-s44.json --metadata method_name=dspark-k1 dataset_name=random mode=dspark k=1 gpu=2 phase=policy-dspark-r1 concurrency=32 seed=44 prefix_cache=false
```

## 369. warmup-policy-dspark-r1-dspark-k1-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:54:02.363653+00:00
- 结束：2026-11-24T15:54:17.016710+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-dspark-r1-dspark-k1-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-dspark-r1-dspark-k1-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-policy-dspark-r1-dspark-k1-c16-
```

## 370. policy-dspark-r1-dspark-k1-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:54:17.046307+00:00
- 结束：2026-11-24T15:54:35.951719+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k1-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k1-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix policy-dspark-r1-dspark-k1-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k1-i1024-o512-c16-s42.json --metadata method_name=dspark-k1 dataset_name=random mode=dspark k=1 gpu=2 phase=policy-dspark-r1 concurrency=16 seed=42 prefix_cache=false
```

## 371. policy-mtp-r1-mtp-k3-i1024-o512-c1-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:54:26.857328+00:00
- 结束：2026-11-24T15:55:25.491658+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k3-i1024-o512-c1-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k3-i1024-o512-c1-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 43 --request-id-prefix policy-mtp-r1-mtp-k3-i1024-o512-c1-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k3-i1024-o512-c1-s43.json --metadata method_name=mtp-k3 dataset_name=random mode=mtp k=3 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=43 prefix_cache=false
```

## 372. policy-dspark-r1-dspark-k1-i1024-o512-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:54:35.983578+00:00
- 结束：2026-11-24T15:54:57.294666+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k1-i1024-o512-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k1-i1024-o512-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix policy-dspark-r1-dspark-k1-i1024-o512-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k1-i1024-o512-c16-s43.json --metadata method_name=dspark-k1 dataset_name=random mode=dspark k=1 gpu=2 phase=policy-dspark-r1 concurrency=16 seed=43 prefix_cache=false
```

## 373. policy-dspark-r1-dspark-k1-i1024-o512-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:54:57.327906+00:00
- 结束：2026-11-24T15:55:16.325916+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k1-i1024-o512-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k1-i1024-o512-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix policy-dspark-r1-dspark-k1-i1024-o512-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k1-i1024-o512-c16-s44.json --metadata method_name=dspark-k1 dataset_name=random mode=dspark k=1 gpu=2 phase=policy-dspark-r1 concurrency=16 seed=44 prefix_cache=false
```

## 374. 065-server-dspark-k3-gpu2

- 状态：completed；退出码：0
- 开始：2026-11-24T15:55:18.016758+00:00
- 结束：2026-11-24T15:58:47.876519+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[065-server-dspark-k3-gpu2.log](/home/genai/spec_decoding_study/logs/commands/065-server-dspark-k3-gpu2.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8102 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"dspark","num_speculative_tokens":3,"model":"/home/genai/models/Qwen3.8-27B-DSpark-vLLM"}'
```

## 375. policy-mtp-r1-mtp-k3-i1024-o512-c1-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:55:25.525349+00:00
- 结束：2026-11-24T15:56:25.806197+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k3-i1024-o512-c1-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k3-i1024-o512-c1-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 44 --request-id-prefix policy-mtp-r1-mtp-k3-i1024-o512-c1-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k3-i1024-o512-c1-s44.json --metadata method_name=mtp-k3 dataset_name=random mode=mtp k=3 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=44 prefix_cache=false
```

## 376. warmup-policy-dspark-r1-dspark-k3-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:56:22.080759+00:00
- 结束：2026-11-24T15:56:38.501107+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-dspark-r1-dspark-k3-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-dspark-r1-dspark-k3-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-policy-dspark-r1-dspark-k3-c32-
```

## 377. 063-server-mtp-k5-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T15:56:27.897183+00:00
- 结束：2026-11-24T16:03:18.251371+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[063-server-mtp-k5-gpu3.log](/home/genai/spec_decoding_study/logs/commands/063-server-mtp-k5-gpu3.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8103 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"mtp","num_speculative_tokens":5}'
```

## 378. policy-dspark-r1-dspark-k3-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:56:38.530373+00:00
- 结束：2026-11-24T15:56:55.258914+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k3-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k3-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix policy-dspark-r1-dspark-k3-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k3-i1024-o512-c32-s42.json --metadata method_name=dspark-k3 dataset_name=random mode=dspark k=3 gpu=2 phase=policy-dspark-r1 concurrency=32 seed=42 prefix_cache=false
```

## 379. policy-dspark-r1-dspark-k3-i1024-o512-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:56:55.290756+00:00
- 结束：2026-11-24T15:57:11.860544+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k3-i1024-o512-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k3-i1024-o512-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix policy-dspark-r1-dspark-k3-i1024-o512-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k3-i1024-o512-c32-s43.json --metadata method_name=dspark-k3 dataset_name=random mode=dspark k=3 gpu=2 phase=policy-dspark-r1 concurrency=32 seed=43 prefix_cache=false
```

## 380. policy-dspark-r1-dspark-k3-i1024-o512-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:57:11.892391+00:00
- 结束：2026-11-24T15:57:28.060873+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k3-i1024-o512-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k3-i1024-o512-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix policy-dspark-r1-dspark-k3-i1024-o512-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k3-i1024-o512-c32-s44.json --metadata method_name=dspark-k3 dataset_name=random mode=dspark k=3 gpu=2 phase=policy-dspark-r1 concurrency=32 seed=44 prefix_cache=false
```

## 381. warmup-policy-mtp-r1-mtp-k5-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T15:57:27.962930+00:00
- 结束：2026-11-24T15:57:41.353768+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-k5-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-k5-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-policy-mtp-r1-mtp-k5-c32-
```

## 382. warmup-policy-dspark-r1-dspark-k3-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:57:28.091795+00:00
- 结束：2026-11-24T15:57:43.589429+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-dspark-r1-dspark-k3-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-dspark-r1-dspark-k3-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-policy-dspark-r1-dspark-k3-c16-
```

## 383. policy-mtp-r1-mtp-k5-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:57:41.383113+00:00
- 结束：2026-11-24T15:57:53.808246+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k5-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k5-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix policy-mtp-r1-mtp-k5-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k5-i1024-o512-c32-s42.json --metadata method_name=mtp-k5 dataset_name=random mode=mtp k=5 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=42 prefix_cache=false
```

## 384. policy-dspark-r1-dspark-k3-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:57:43.618602+00:00
- 结束：2026-11-24T15:58:03.981345+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k3-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k3-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix policy-dspark-r1-dspark-k3-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k3-i1024-o512-c16-s42.json --metadata method_name=dspark-k3 dataset_name=random mode=dspark k=3 gpu=2 phase=policy-dspark-r1 concurrency=16 seed=42 prefix_cache=false
```

## 385. policy-mtp-r1-mtp-k5-i1024-o512-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:57:53.842384+00:00
- 结束：2026-11-24T15:58:06.343500+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k5-i1024-o512-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k5-i1024-o512-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix policy-mtp-r1-mtp-k5-i1024-o512-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k5-i1024-o512-c32-s43.json --metadata method_name=mtp-k5 dataset_name=random mode=mtp k=5 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=43 prefix_cache=false
```

## 386. policy-dspark-r1-dspark-k3-i1024-o512-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:58:04.014075+00:00
- 结束：2026-11-24T15:58:25.247931+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k3-i1024-o512-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k3-i1024-o512-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix policy-dspark-r1-dspark-k3-i1024-o512-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k3-i1024-o512-c16-s43.json --metadata method_name=dspark-k3 dataset_name=random mode=dspark k=3 gpu=2 phase=policy-dspark-r1 concurrency=16 seed=43 prefix_cache=false
```

## 387. policy-mtp-r1-mtp-k5-i1024-o512-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:58:06.374404+00:00
- 结束：2026-11-24T15:58:19.151632+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k5-i1024-o512-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k5-i1024-o512-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix policy-mtp-r1-mtp-k5-i1024-o512-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k5-i1024-o512-c32-s44.json --metadata method_name=mtp-k5 dataset_name=random mode=mtp k=5 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=44 prefix_cache=false
```

## 388. warmup-policy-mtp-r1-mtp-k5-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T15:58:19.182064+00:00
- 结束：2026-11-24T15:58:30.699221+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-k5-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-k5-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-policy-mtp-r1-mtp-k5-c16-
```

## 389. policy-dspark-r1-dspark-k3-i1024-o512-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:58:25.281125+00:00
- 结束：2026-11-24T15:58:45.305794+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-dspark-r1-dspark-k3-i1024-o512-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-dspark-r1-dspark-k3-i1024-o512-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix policy-dspark-r1-dspark-k3-i1024-o512-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-dspark-r1-dspark-k3-i1024-o512-c16-s44.json --metadata method_name=dspark-k3 dataset_name=random mode=dspark k=3 gpu=2 phase=policy-dspark-r1 concurrency=16 seed=44 prefix_cache=false
```

## 390. policy-mtp-r1-mtp-k5-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:58:30.728214+00:00
- 结束：2026-11-24T15:58:44.292810+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k5-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k5-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix policy-mtp-r1-mtp-k5-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k5-i1024-o512-c16-s42.json --metadata method_name=mtp-k5 dataset_name=random mode=mtp k=5 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=42 prefix_cache=false
```

## 391. policy-mtp-r1-mtp-k5-i1024-o512-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:58:44.323723+00:00
- 结束：2026-11-24T15:58:58.244185+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k5-i1024-o512-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k5-i1024-o512-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix policy-mtp-r1-mtp-k5-i1024-o512-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k5-i1024-o512-c16-s43.json --metadata method_name=mtp-k5 dataset_name=random mode=mtp k=5 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=43 prefix_cache=false
```

## 392. policy-mtp-r1-mtp-k5-i1024-o512-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T15:58:58.274993+00:00
- 结束：2026-11-24T15:59:11.523462+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k5-i1024-o512-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k5-i1024-o512-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix policy-mtp-r1-mtp-k5-i1024-o512-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k5-i1024-o512-c16-s44.json --metadata method_name=mtp-k5 dataset_name=random mode=mtp k=5 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=44 prefix_cache=false
```

## 393. warmup-policy-mtp-r1-mtp-k5-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T15:59:11.553928+00:00
- 结束：2026-11-24T15:59:21.505654+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-k5-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-k5-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-policy-mtp-r1-mtp-k5-c4-
```

## 394. 066-semantic-dspark-fixed-high-gpu2

- 状态：completed；退出码：0
- 开始：2026-11-24T15:59:14.871566+00:00
- 结束：2026-11-24T16:06:34.733970+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[066-semantic-dspark-fixed-high-gpu2.log](/home/genai/spec_decoding_study/logs/commands/066-semantic-dspark-fixed-high-gpu2.log)

```bash
/home/genai/.pixi/envs/default/bin/python /home/genai/spec_decoding_study/src/run_server_suite.py --config /home/genai/spec_decoding_study/config/dspark_high_concurrency_confirmation.json --gpu 2 --port 8102 --phase semantic-r1 --label-prefix 066 --num-prompts 128 --seeds 42 43 44 --concurrencies 32 16 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --output-len 256
```

## 395. 066-server-dspark-k1-gpu2

- 状态：completed；退出码：0
- 开始：2026-11-24T15:59:14.943320+00:00
- 结束：2026-11-24T16:03:05.598275+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[066-server-dspark-k1-gpu2.log](/home/genai/spec_decoding_study/logs/commands/066-server-dspark-k1-gpu2.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8102 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"dspark","model":"/home/genai/models/Qwen3.8-27B-DSpark-vLLM","num_speculative_tokens":1}'
```

## 396. policy-mtp-r1-mtp-k5-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T15:59:21.535110+00:00
- 结束：2026-11-24T15:59:44.134758+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k5-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k5-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix policy-mtp-r1-mtp-k5-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k5-i1024-o512-c4-s42.json --metadata method_name=mtp-k5 dataset_name=random mode=mtp k=5 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=42 prefix_cache=false
```

## 397. policy-mtp-r1-mtp-k5-i1024-o512-c4-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T15:59:44.165996+00:00
- 结束：2026-11-24T16:00:06.052988+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k5-i1024-o512-c4-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k5-i1024-o512-c4-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 43 --request-id-prefix policy-mtp-r1-mtp-k5-i1024-o512-c4-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k5-i1024-o512-c4-s43.json --metadata method_name=mtp-k5 dataset_name=random mode=mtp k=5 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=43 prefix_cache=false
```

## 398. policy-mtp-r1-mtp-k5-i1024-o512-c4-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:00:06.083931+00:00
- 结束：2026-11-24T16:00:27.979245+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k5-i1024-o512-c4-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k5-i1024-o512-c4-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 44 --request-id-prefix policy-mtp-r1-mtp-k5-i1024-o512-c4-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k5-i1024-o512-c4-s44.json --metadata method_name=mtp-k5 dataset_name=random mode=mtp k=5 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=44 prefix_cache=false
```

## 399. warmup-semantic-r1-dspark-k1-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T16:00:25.008414+00:00
- 结束：2026-11-24T16:00:36.421304+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-dspark-k1-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-dspark-k1-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-semantic-r1-dspark-k1-c32-
```

## 400. warmup-policy-mtp-r1-mtp-k5-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T16:00:28.009791+00:00
- 结束：2026-11-24T16:00:42.738372+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-k5-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-k5-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-policy-mtp-r1-mtp-k5-c1-
```

## 401. semantic-r1-dspark-k1-specbench-o256-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:00:36.450976+00:00
- 结束：2026-11-24T16:00:57.186759+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k1-specbench-o256-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k1-specbench-o256-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix semantic-r1-dspark-k1-specbench-o256-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k1-specbench-o256-c32-s42.json --metadata method_name=dspark-k1 dataset_name=spec_bench mode=dspark k=1 gpu=2 phase=semantic-r1 concurrency=32 seed=42 prefix_cache=false
```

## 402. policy-mtp-r1-mtp-k5-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:00:42.768186+00:00
- 结束：2026-11-24T16:01:35.132984+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k5-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k5-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix policy-mtp-r1-mtp-k5-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k5-i1024-o512-c1-s42.json --metadata method_name=mtp-k5 dataset_name=random mode=mtp k=5 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=42 prefix_cache=false
```

## 403. semantic-r1-dspark-k1-specbench-o256-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:00:57.221360+00:00
- 结束：2026-11-24T16:01:17.899358+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k1-specbench-o256-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k1-specbench-o256-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix semantic-r1-dspark-k1-specbench-o256-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k1-specbench-o256-c32-s43.json --metadata method_name=dspark-k1 dataset_name=spec_bench mode=dspark k=1 gpu=2 phase=semantic-r1 concurrency=32 seed=43 prefix_cache=false
```

## 404. semantic-r1-dspark-k1-specbench-o256-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:01:17.934388+00:00
- 结束：2026-11-24T16:01:38.759623+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k1-specbench-o256-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k1-specbench-o256-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix semantic-r1-dspark-k1-specbench-o256-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k1-specbench-o256-c32-s44.json --metadata method_name=dspark-k1 dataset_name=spec_bench mode=dspark k=1 gpu=2 phase=semantic-r1 concurrency=32 seed=44 prefix_cache=false
```

## 405. policy-mtp-r1-mtp-k5-i1024-o512-c1-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:01:35.164372+00:00
- 结束：2026-11-24T16:02:27.040528+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k5-i1024-o512-c1-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k5-i1024-o512-c1-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 43 --request-id-prefix policy-mtp-r1-mtp-k5-i1024-o512-c1-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k5-i1024-o512-c1-s43.json --metadata method_name=mtp-k5 dataset_name=random mode=mtp k=5 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=43 prefix_cache=false
```

## 406. warmup-semantic-r1-dspark-k1-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T16:01:38.793526+00:00
- 结束：2026-11-24T16:01:48.649062+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-dspark-k1-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-dspark-k1-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-semantic-r1-dspark-k1-c16-
```

## 407. semantic-r1-dspark-k1-specbench-o256-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:01:48.678798+00:00
- 结束：2026-11-24T16:02:13.691880+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k1-specbench-o256-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k1-specbench-o256-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix semantic-r1-dspark-k1-specbench-o256-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k1-specbench-o256-c16-s42.json --metadata method_name=dspark-k1 dataset_name=spec_bench mode=dspark k=1 gpu=2 phase=semantic-r1 concurrency=16 seed=42 prefix_cache=false
```

## 408. semantic-r1-dspark-k1-specbench-o256-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:02:13.727090+00:00
- 结束：2026-11-24T16:02:38.637747+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k1-specbench-o256-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k1-specbench-o256-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix semantic-r1-dspark-k1-specbench-o256-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k1-specbench-o256-c16-s43.json --metadata method_name=dspark-k1 dataset_name=spec_bench mode=dspark k=1 gpu=2 phase=semantic-r1 concurrency=16 seed=43 prefix_cache=false
```

## 409. policy-mtp-r1-mtp-k5-i1024-o512-c1-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:02:27.075727+00:00
- 结束：2026-11-24T16:03:16.257110+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k5-i1024-o512-c1-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k5-i1024-o512-c1-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 44 --request-id-prefix policy-mtp-r1-mtp-k5-i1024-o512-c1-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k5-i1024-o512-c1-s44.json --metadata method_name=mtp-k5 dataset_name=random mode=mtp k=5 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=44 prefix_cache=false
```

## 410. semantic-r1-dspark-k1-specbench-o256-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:02:38.672584+00:00
- 结束：2026-11-24T16:03:03.599880+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k1-specbench-o256-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k1-specbench-o256-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix semantic-r1-dspark-k1-specbench-o256-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k1-specbench-o256-c16-s44.json --metadata method_name=dspark-k1 dataset_name=spec_bench mode=dspark k=1 gpu=2 phase=semantic-r1 concurrency=16 seed=44 prefix_cache=false
```

## 411. 066-server-dspark-k3-gpu2

- 状态：completed；退出码：0
- 开始：2026-11-24T16:03:05.494872+00:00
- 结束：2026-11-24T16:06:34.874412+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[066-server-dspark-k3-gpu2.log](/home/genai/spec_decoding_study/logs/commands/066-server-dspark-k3-gpu2.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8102 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"dspark","model":"/home/genai/models/Qwen3.8-27B-DSpark-vLLM","num_speculative_tokens":3}'
```

## 412. 063-server-mtp-k6-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T16:03:18.150522+00:00
- 结束：2026-11-24T16:10:09.971890+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[063-server-mtp-k6-gpu3.log](/home/genai/spec_decoding_study/logs/commands/063-server-mtp-k6-gpu3.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8103 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"mtp","num_speculative_tokens":6}'
```

## 413. warmup-semantic-r1-dspark-k3-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T16:04:09.562683+00:00
- 结束：2026-11-24T16:04:19.900511+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-dspark-k3-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-dspark-k3-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-semantic-r1-dspark-k3-c32-
```

## 414. warmup-policy-mtp-r1-mtp-k6-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T16:04:18.215147+00:00
- 结束：2026-11-24T16:04:31.318780+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-k6-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-k6-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-policy-mtp-r1-mtp-k6-c32-
```

## 415. semantic-r1-dspark-k3-specbench-o256-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:04:19.929416+00:00
- 结束：2026-11-24T16:04:36.700601+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k3-specbench-o256-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k3-specbench-o256-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix semantic-r1-dspark-k3-specbench-o256-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k3-specbench-o256-c32-s42.json --metadata method_name=dspark-k3 dataset_name=spec_bench mode=dspark k=3 gpu=2 phase=semantic-r1 concurrency=32 seed=42 prefix_cache=false
```

## 416. policy-mtp-r1-mtp-k6-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:04:31.348929+00:00
- 结束：2026-11-24T16:04:44.225179+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k6-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k6-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix policy-mtp-r1-mtp-k6-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k6-i1024-o512-c32-s42.json --metadata method_name=mtp-k6 dataset_name=random mode=mtp k=6 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=42 prefix_cache=false
```

## 417. semantic-r1-dspark-k3-specbench-o256-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:04:36.734140+00:00
- 结束：2026-11-24T16:04:53.785098+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k3-specbench-o256-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k3-specbench-o256-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix semantic-r1-dspark-k3-specbench-o256-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k3-specbench-o256-c32-s43.json --metadata method_name=dspark-k3 dataset_name=spec_bench mode=dspark k=3 gpu=2 phase=semantic-r1 concurrency=32 seed=43 prefix_cache=false
```

## 418. policy-mtp-r1-mtp-k6-i1024-o512-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:04:44.258944+00:00
- 结束：2026-11-24T16:04:57.796322+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k6-i1024-o512-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k6-i1024-o512-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix policy-mtp-r1-mtp-k6-i1024-o512-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k6-i1024-o512-c32-s43.json --metadata method_name=mtp-k6 dataset_name=random mode=mtp k=6 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=43 prefix_cache=false
```

## 419. semantic-r1-dspark-k3-specbench-o256-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:04:53.817622+00:00
- 结束：2026-11-24T16:05:11.004699+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k3-specbench-o256-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k3-specbench-o256-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix semantic-r1-dspark-k3-specbench-o256-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k3-specbench-o256-c32-s44.json --metadata method_name=dspark-k3 dataset_name=spec_bench mode=dspark k=3 gpu=2 phase=semantic-r1 concurrency=32 seed=44 prefix_cache=false
```

## 420. policy-mtp-r1-mtp-k6-i1024-o512-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:04:57.827302+00:00
- 结束：2026-11-24T16:05:11.198918+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k6-i1024-o512-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k6-i1024-o512-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix policy-mtp-r1-mtp-k6-i1024-o512-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k6-i1024-o512-c32-s44.json --metadata method_name=mtp-k6 dataset_name=random mode=mtp k=6 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=44 prefix_cache=false
```

## 421. warmup-semantic-r1-dspark-k3-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T16:05:11.036195+00:00
- 结束：2026-11-24T16:05:21.453225+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-semantic-r1-dspark-k3-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-semantic-r1-dspark-k3-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-semantic-r1-dspark-k3-c16-
```

## 422. warmup-policy-mtp-r1-mtp-k6-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T16:05:11.229121+00:00
- 结束：2026-11-24T16:05:23.368925+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-k6-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-k6-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-policy-mtp-r1-mtp-k6-c16-
```

## 423. semantic-r1-dspark-k3-specbench-o256-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:05:21.482646+00:00
- 结束：2026-11-24T16:05:45.994265+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k3-specbench-o256-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k3-specbench-o256-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix semantic-r1-dspark-k3-specbench-o256-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k3-specbench-o256-c16-s42.json --metadata method_name=dspark-k3 dataset_name=spec_bench mode=dspark k=3 gpu=2 phase=semantic-r1 concurrency=16 seed=42 prefix_cache=false
```

## 424. policy-mtp-r1-mtp-k6-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:05:23.398268+00:00
- 结束：2026-11-24T16:05:38.965755+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k6-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k6-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix policy-mtp-r1-mtp-k6-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k6-i1024-o512-c16-s42.json --metadata method_name=mtp-k6 dataset_name=random mode=mtp k=6 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=42 prefix_cache=false
```

## 425. policy-mtp-r1-mtp-k6-i1024-o512-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:05:38.997190+00:00
- 结束：2026-11-24T16:05:53.285300+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k6-i1024-o512-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k6-i1024-o512-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix policy-mtp-r1-mtp-k6-i1024-o512-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k6-i1024-o512-c16-s43.json --metadata method_name=mtp-k6 dataset_name=random mode=mtp k=6 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=43 prefix_cache=false
```

## 426. semantic-r1-dspark-k3-specbench-o256-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:05:46.027055+00:00
- 结束：2026-11-24T16:06:09.329025+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k3-specbench-o256-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k3-specbench-o256-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix semantic-r1-dspark-k3-specbench-o256-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k3-specbench-o256-c16-s43.json --metadata method_name=dspark-k3 dataset_name=spec_bench mode=dspark k=3 gpu=2 phase=semantic-r1 concurrency=16 seed=43 prefix_cache=false
```

## 427. policy-mtp-r1-mtp-k6-i1024-o512-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:05:53.315797+00:00
- 结束：2026-11-24T16:06:07.226731+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k6-i1024-o512-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k6-i1024-o512-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix policy-mtp-r1-mtp-k6-i1024-o512-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k6-i1024-o512-c16-s44.json --metadata method_name=mtp-k6 dataset_name=random mode=mtp k=6 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=44 prefix_cache=false
```

## 428. warmup-policy-mtp-r1-mtp-k6-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T16:06:07.257056+00:00
- 结束：2026-11-24T16:06:17.257348+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-k6-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-k6-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-policy-mtp-r1-mtp-k6-c4-
```

## 429. semantic-r1-dspark-k3-specbench-o256-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:06:09.362271+00:00
- 结束：2026-11-24T16:06:32.884192+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[semantic-r1-dspark-k3-specbench-o256-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/semantic-r1-dspark-k3-specbench-o256-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=2 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8102 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name spec_bench --dataset-path /home/genai/spec_decoding_study/data/spec_bench/question.jsonl --spec-bench-output-len 256 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 128 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix semantic-r1-dspark-k3-specbench-o256-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename semantic-r1-dspark-k3-specbench-o256-c16-s44.json --metadata method_name=dspark-k3 dataset_name=spec_bench mode=dspark k=3 gpu=2 phase=semantic-r1 concurrency=16 seed=44 prefix_cache=false
```

## 430. policy-mtp-r1-mtp-k6-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:06:17.287576+00:00
- 结束：2026-11-24T16:06:38.850908+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k6-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k6-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix policy-mtp-r1-mtp-k6-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k6-i1024-o512-c4-s42.json --metadata method_name=mtp-k6 dataset_name=random mode=mtp k=6 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=42 prefix_cache=false
```

## 431. policy-mtp-r1-mtp-k6-i1024-o512-c4-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:06:38.882423+00:00
- 结束：2026-11-24T16:07:00.970396+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k6-i1024-o512-c4-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k6-i1024-o512-c4-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 43 --request-id-prefix policy-mtp-r1-mtp-k6-i1024-o512-c4-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k6-i1024-o512-c4-s43.json --metadata method_name=mtp-k6 dataset_name=random mode=mtp k=6 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=43 prefix_cache=false
```

## 432. policy-mtp-r1-mtp-k6-i1024-o512-c4-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:07:01.001969+00:00
- 结束：2026-11-24T16:07:22.380956+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k6-i1024-o512-c4-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k6-i1024-o512-c4-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 44 --request-id-prefix policy-mtp-r1-mtp-k6-i1024-o512-c4-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k6-i1024-o512-c4-s44.json --metadata method_name=mtp-k6 dataset_name=random mode=mtp k=6 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=44 prefix_cache=false
```

## 433. warmup-policy-mtp-r1-mtp-k6-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T16:07:22.411522+00:00
- 结束：2026-11-24T16:07:37.134916+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-k6-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-k6-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-policy-mtp-r1-mtp-k6-c1-
```

## 434. policy-mtp-r1-mtp-k6-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:07:37.163911+00:00
- 结束：2026-11-24T16:08:27.803743+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k6-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k6-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix policy-mtp-r1-mtp-k6-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k6-i1024-o512-c1-s42.json --metadata method_name=mtp-k6 dataset_name=random mode=mtp k=6 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=42 prefix_cache=false
```

## 435. policy-mtp-r1-mtp-k6-i1024-o512-c1-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:08:27.834644+00:00
- 结束：2026-11-24T16:09:19.796285+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k6-i1024-o512-c1-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k6-i1024-o512-c1-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 43 --request-id-prefix policy-mtp-r1-mtp-k6-i1024-o512-c1-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k6-i1024-o512-c1-s43.json --metadata method_name=mtp-k6 dataset_name=random mode=mtp k=6 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=43 prefix_cache=false
```

## 436. policy-mtp-r1-mtp-k6-i1024-o512-c1-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:09:19.827719+00:00
- 结束：2026-11-24T16:10:08.019583+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k6-i1024-o512-c1-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k6-i1024-o512-c1-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 44 --request-id-prefix policy-mtp-r1-mtp-k6-i1024-o512-c1-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k6-i1024-o512-c1-s44.json --metadata method_name=mtp-k6 dataset_name=random mode=mtp k=6 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=44 prefix_cache=false
```

## 437. 063-server-mtp-k7-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T16:10:09.911625+00:00
- 结束：2026-11-24T16:17:04.892101+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[063-server-mtp-k7-gpu3.log](/home/genai/spec_decoding_study/logs/commands/063-server-mtp-k7-gpu3.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8103 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"mtp","num_speculative_tokens":7}'
```

## 438. warmup-policy-mtp-r1-mtp-k7-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T16:11:13.977831+00:00
- 结束：2026-11-24T16:11:26.751252+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-k7-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-k7-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-policy-mtp-r1-mtp-k7-c32-
```

## 439. policy-mtp-r1-mtp-k7-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:11:26.781987+00:00
- 结束：2026-11-24T16:11:39.895875+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k7-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k7-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix policy-mtp-r1-mtp-k7-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k7-i1024-o512-c32-s42.json --metadata method_name=mtp-k7 dataset_name=random mode=mtp k=7 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=42 prefix_cache=false
```

## 440. policy-mtp-r1-mtp-k7-i1024-o512-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:11:39.927387+00:00
- 结束：2026-11-24T16:11:52.732064+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k7-i1024-o512-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k7-i1024-o512-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix policy-mtp-r1-mtp-k7-i1024-o512-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k7-i1024-o512-c32-s43.json --metadata method_name=mtp-k7 dataset_name=random mode=mtp k=7 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=43 prefix_cache=false
```

## 441. policy-mtp-r1-mtp-k7-i1024-o512-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:11:52.762560+00:00
- 结束：2026-11-24T16:12:05.513318+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k7-i1024-o512-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k7-i1024-o512-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix policy-mtp-r1-mtp-k7-i1024-o512-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k7-i1024-o512-c32-s44.json --metadata method_name=mtp-k7 dataset_name=random mode=mtp k=7 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=44 prefix_cache=false
```

## 442. warmup-policy-mtp-r1-mtp-k7-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T16:12:05.543486+00:00
- 结束：2026-11-24T16:12:17.497494+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-k7-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-k7-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-policy-mtp-r1-mtp-k7-c16-
```

## 443. policy-mtp-r1-mtp-k7-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:12:17.526773+00:00
- 结束：2026-11-24T16:12:31.557631+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k7-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k7-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix policy-mtp-r1-mtp-k7-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k7-i1024-o512-c16-s42.json --metadata method_name=mtp-k7 dataset_name=random mode=mtp k=7 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=42 prefix_cache=false
```

## 444. policy-mtp-r1-mtp-k7-i1024-o512-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:12:31.588793+00:00
- 结束：2026-11-24T16:12:45.886550+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k7-i1024-o512-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k7-i1024-o512-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix policy-mtp-r1-mtp-k7-i1024-o512-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k7-i1024-o512-c16-s43.json --metadata method_name=mtp-k7 dataset_name=random mode=mtp k=7 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=43 prefix_cache=false
```

## 445. policy-mtp-r1-mtp-k7-i1024-o512-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:12:45.917133+00:00
- 结束：2026-11-24T16:12:59.753219+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k7-i1024-o512-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k7-i1024-o512-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix policy-mtp-r1-mtp-k7-i1024-o512-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k7-i1024-o512-c16-s44.json --metadata method_name=mtp-k7 dataset_name=random mode=mtp k=7 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=44 prefix_cache=false
```

## 446. warmup-policy-mtp-r1-mtp-k7-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T16:12:59.783147+00:00
- 结束：2026-11-24T16:13:11.350693+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-k7-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-k7-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-policy-mtp-r1-mtp-k7-c4-
```

## 447. policy-mtp-r1-mtp-k7-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:13:11.380238+00:00
- 结束：2026-11-24T16:13:37.203760+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k7-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k7-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix policy-mtp-r1-mtp-k7-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k7-i1024-o512-c4-s42.json --metadata method_name=mtp-k7 dataset_name=random mode=mtp k=7 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=42 prefix_cache=false
```

## 448. policy-mtp-r1-mtp-k7-i1024-o512-c4-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:13:37.234520+00:00
- 结束：2026-11-24T16:14:00.392187+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k7-i1024-o512-c4-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k7-i1024-o512-c4-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 43 --request-id-prefix policy-mtp-r1-mtp-k7-i1024-o512-c4-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k7-i1024-o512-c4-s43.json --metadata method_name=mtp-k7 dataset_name=random mode=mtp k=7 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=43 prefix_cache=false
```

## 449. policy-mtp-r1-mtp-k7-i1024-o512-c4-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:14:00.426101+00:00
- 结束：2026-11-24T16:14:20.919168+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k7-i1024-o512-c4-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k7-i1024-o512-c4-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 44 --request-id-prefix policy-mtp-r1-mtp-k7-i1024-o512-c4-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k7-i1024-o512-c4-s44.json --metadata method_name=mtp-k7 dataset_name=random mode=mtp k=7 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=44 prefix_cache=false
```

## 450. warmup-policy-mtp-r1-mtp-k7-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T16:14:20.949434+00:00
- 结束：2026-11-24T16:14:34.992418+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-k7-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-k7-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-policy-mtp-r1-mtp-k7-c1-
```

## 451. policy-mtp-r1-mtp-k7-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:14:35.021639+00:00
- 结束：2026-11-24T16:15:25.601987+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k7-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k7-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix policy-mtp-r1-mtp-k7-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k7-i1024-o512-c1-s42.json --metadata method_name=mtp-k7 dataset_name=random mode=mtp k=7 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=42 prefix_cache=false
```

## 452. policy-mtp-r1-mtp-k7-i1024-o512-c1-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:15:25.633591+00:00
- 结束：2026-11-24T16:16:16.615928+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k7-i1024-o512-c1-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k7-i1024-o512-c1-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 43 --request-id-prefix policy-mtp-r1-mtp-k7-i1024-o512-c1-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k7-i1024-o512-c1-s43.json --metadata method_name=mtp-k7 dataset_name=random mode=mtp k=7 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=43 prefix_cache=false
```

## 453. policy-mtp-r1-mtp-k7-i1024-o512-c1-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:16:16.646825+00:00
- 结束：2026-11-24T16:17:02.838078+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-k7-i1024-o512-c1-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-k7-i1024-o512-c1-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 44 --request-id-prefix policy-mtp-r1-mtp-k7-i1024-o512-c1-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-k7-i1024-o512-c1-s44.json --metadata method_name=mtp-k7 dataset_name=random mode=mtp k=7 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=44 prefix_cache=false
```

## 454. 063-server-mtp-dynamic-oracle-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T16:17:04.930174+00:00
- 结束：2026-11-24T16:23:55.325431+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[063-server-mtp-dynamic-oracle-gpu3.log](/home/genai/spec_decoding_study/logs/commands/063-server-mtp-dynamic-oracle-gpu3.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8103 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"mtp","num_speculative_tokens":7,"num_speculative_tokens_per_batch_size":[[1,1,7],[2,4,6],[5,16,7],[17,256,5]]}'
```

## 455. warmup-policy-mtp-r1-mtp-dynamic-oracle-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T16:18:08.994124+00:00
- 结束：2026-11-24T16:18:21.941805+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-dynamic-oracle-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-dynamic-oracle-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-policy-mtp-r1-mtp-dynamic-oracle-c32-
```

## 456. policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:18:21.970372+00:00
- 结束：2026-11-24T16:18:34.646292+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c32-s42.json --metadata method_name=mtp-dynamic-oracle dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=42 prefix_cache=false
```

## 457. policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:18:34.676987+00:00
- 结束：2026-11-24T16:18:47.654447+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c32-s43.json --metadata method_name=mtp-dynamic-oracle dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=43 prefix_cache=false
```

## 458. policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:18:47.685214+00:00
- 结束：2026-11-24T16:19:00.343870+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c32-s44.json --metadata method_name=mtp-dynamic-oracle dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=44 prefix_cache=false
```

## 459. warmup-policy-mtp-r1-mtp-dynamic-oracle-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T16:19:00.374415+00:00
- 结束：2026-11-24T16:19:11.977008+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-dynamic-oracle-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-dynamic-oracle-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-policy-mtp-r1-mtp-dynamic-oracle-c16-
```

## 460. policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:19:12.007668+00:00
- 结束：2026-11-24T16:19:26.846040+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c16-s42.json --metadata method_name=mtp-dynamic-oracle dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=42 prefix_cache=false
```

## 461. policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:19:26.876805+00:00
- 结束：2026-11-24T16:19:40.765193+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c16-s43.json --metadata method_name=mtp-dynamic-oracle dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=43 prefix_cache=false
```

## 462. policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:19:40.796281+00:00
- 结束：2026-11-24T16:19:54.946577+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c16-s44.json --metadata method_name=mtp-dynamic-oracle dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=44 prefix_cache=false
```

## 463. warmup-policy-mtp-r1-mtp-dynamic-oracle-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T16:19:54.976950+00:00
- 结束：2026-11-24T16:20:05.090787+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-dynamic-oracle-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-dynamic-oracle-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-policy-mtp-r1-mtp-dynamic-oracle-c4-
```

## 464. policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:20:05.120651+00:00
- 结束：2026-11-24T16:20:26.818641+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c4-s42.json --metadata method_name=mtp-dynamic-oracle dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=42 prefix_cache=false
```

## 465. policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c4-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:20:26.849546+00:00
- 结束：2026-11-24T16:20:49.268927+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c4-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c4-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 43 --request-id-prefix policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c4-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c4-s43.json --metadata method_name=mtp-dynamic-oracle dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=43 prefix_cache=false
```

## 466. policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c4-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:20:49.303688+00:00
- 结束：2026-11-24T16:21:10.944276+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c4-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c4-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 44 --request-id-prefix policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c4-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c4-s44.json --metadata method_name=mtp-dynamic-oracle dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=44 prefix_cache=false
```

## 467. warmup-policy-mtp-r1-mtp-dynamic-oracle-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T16:21:10.975173+00:00
- 结束：2026-11-24T16:21:25.116263+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-dynamic-oracle-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-dynamic-oracle-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-policy-mtp-r1-mtp-dynamic-oracle-c1-
```

## 468. policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:21:25.145742+00:00
- 结束：2026-11-24T16:22:15.763490+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c1-s42.json --metadata method_name=mtp-dynamic-oracle dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=42 prefix_cache=false
```

## 469. 067-summary-mtp-fixed

- 状态：completed；退出码：0
- 开始：2026-11-24T16:21:33.152761+00:00
- 结束：2026-11-24T16:21:33.383773+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[067-summary-mtp-fixed.log](/home/genai/spec_decoding_study/logs/commands/067-summary-mtp-fixed.log)

```bash
python src/summarize_benchmarks.py --phase policy-mtp-r1 --output-stem policy-mtp-fixed-r1 --methods normal mtp-k3 mtp-k5 mtp-k6 mtp-k7 --best-fixed-methods mtp-k3 mtp-k5 mtp-k6 mtp-k7 --concurrencies 1 4 16 32 --seeds 42 43 44 --num-prompts 32
```

## 470. policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c1-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:22:15.794502+00:00
- 结束：2026-11-24T16:23:06.798316+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c1-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c1-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 43 --request-id-prefix policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c1-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c1-s43.json --metadata method_name=mtp-dynamic-oracle dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=43 prefix_cache=false
```

## 471. policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c1-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:23:06.832007+00:00
- 结束：2026-11-24T16:23:53.433758+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c1-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c1-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 44 --request-id-prefix policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c1-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-oracle-i1024-o512-c1-s44.json --metadata method_name=mtp-dynamic-oracle dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=44 prefix_cache=false
```

## 472. 068-figures-mtp-fixed

- 状态：completed；退出码：0
- 开始：2026-11-24T16:23:37.025532+00:00
- 结束：2026-11-24T16:23:43.961981+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[068-figures-mtp-fixed.log](/home/genai/spec_decoding_study/logs/commands/068-figures-mtp-fixed.log)

```bash
python src/make_figures.py --include-policies
```

## 473. 063-server-mtp-dynamic-smooth-gpu3

- 状态：completed；退出码：0
- 开始：2026-11-24T16:23:55.124718+00:00
- 结束：2026-11-24T16:30:49.588018+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[063-server-mtp-dynamic-smooth-gpu3.log](/home/genai/spec_decoding_study/logs/commands/063-server-mtp-dynamic-smooth-gpu3.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 VLLM_USE_RUST_FRONTEND=1 /home/genai/.pixi/envs/default/bin/vllm serve /home/model/Qwen3.8-27B-FP8 --served-model-name qwen-target --host 127.0.0.1 --port 8103 --tensor-parallel-size 1 --enable-auto-tool-choice --tool-call-parser qwen3_coder --reasoning-parser qwen3 --mm-encoder-tp-mode data --max-model-len 8192 --max-num-seqs 256 --gpu-memory-utilization 0.90 --generation-config vllm --disable-log-requests --disable-prefix-caching --seed 0 --speculative-config '{"method":"mtp","num_speculative_tokens":6,"num_speculative_tokens_per_batch_size":[[1,4,6],[5,256,5]]}'
```

## 474. 069-summary-mtp-oracle-interim

- 状态：completed；退出码：0
- 开始：2026-11-24T16:24:40.736198+00:00
- 结束：2026-11-24T16:24:40.989650+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[069-summary-mtp-oracle-interim.log](/home/genai/spec_decoding_study/logs/commands/069-summary-mtp-oracle-interim.log)

```bash
python src/summarize_benchmarks.py --phase policy-mtp-r1 --methods normal mtp-k3 mtp-k5 mtp-k6 mtp-k7 mtp-dynamic-oracle mtp-dynamic-smooth --best-fixed-methods mtp-k3 mtp-k5 mtp-k6 mtp-k7 --concurrencies 1 4 16 32 --seeds 42 43 44 --num-prompts 32 --allow-partial
```

## 475. warmup-policy-mtp-r1-mtp-dynamic-smooth-c32

- 状态：completed；退出码：0
- 开始：2026-11-24T16:25:03.191735+00:00
- 结束：2026-11-24T16:25:17.512605+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-dynamic-smooth-c32.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-dynamic-smooth-c32.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 1032 --request-id-prefix warmup-policy-mtp-r1-mtp-dynamic-smooth-c32-
```

## 476. policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c32-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:25:17.541658+00:00
- 结束：2026-11-24T16:25:29.934896+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c32-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c32-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 42 --request-id-prefix policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c32-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c32-s42.json --metadata method_name=mtp-dynamic-smooth dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=42 prefix_cache=false
```

## 477. policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c32-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:25:29.965608+00:00
- 结束：2026-11-24T16:25:42.412212+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c32-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c32-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 43 --request-id-prefix policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c32-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c32-s43.json --metadata method_name=mtp-dynamic-smooth dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=43 prefix_cache=false
```

## 478. policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c32-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:25:42.442580+00:00
- 结束：2026-11-24T16:25:54.871149+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c32-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c32-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 32 --seed 44 --request-id-prefix policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c32-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c32-s44.json --metadata method_name=mtp-dynamic-smooth dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=32 seed=44 prefix_cache=false
```

## 479. warmup-policy-mtp-r1-mtp-dynamic-smooth-c16

- 状态：completed；退出码：0
- 开始：2026-11-24T16:25:54.901945+00:00
- 结束：2026-11-24T16:26:06.280864+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-dynamic-smooth-c16.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-dynamic-smooth-c16.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 16 --num-warmups 0 --max-concurrency 16 --seed 1016 --request-id-prefix warmup-policy-mtp-r1-mtp-dynamic-smooth-c16-
```

## 480. policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c16-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:26:06.310048+00:00
- 结束：2026-11-24T16:26:20.206238+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c16-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c16-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 42 --request-id-prefix policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c16-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c16-s42.json --metadata method_name=mtp-dynamic-smooth dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=42 prefix_cache=false
```

## 481. policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c16-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:26:20.237167+00:00
- 结束：2026-11-24T16:26:34.217232+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c16-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c16-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 43 --request-id-prefix policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c16-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c16-s43.json --metadata method_name=mtp-dynamic-smooth dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=43 prefix_cache=false
```

## 482. policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c16-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:26:34.248258+00:00
- 结束：2026-11-24T16:26:48.052811+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c16-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c16-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 16 --seed 44 --request-id-prefix policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c16-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c16-s44.json --metadata method_name=mtp-dynamic-smooth dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=16 seed=44 prefix_cache=false
```

## 483. 070-summary-formal-final

- 状态：completed；退出码：0
- 开始：2026-11-24T16:26:36.601356+00:00
- 结束：2026-11-24T16:26:37.096717+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[070-summary-formal-final.log](/home/genai/spec_decoding_study/logs/commands/070-summary-formal-final.log)

```bash
python src/summarize_benchmarks.py --phase formal-r1 --methods normal mtp-k3 dspark-k7 --concurrencies 1 4 16 32 --seeds 42 43 44
```

## 484. 071-summary-kscan-final

- 状态：completed；退出码：0
- 开始：2026-11-24T16:26:37.124447+00:00
- 结束：2026-11-24T16:26:37.287832+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[071-summary-kscan-final.log](/home/genai/spec_decoding_study/logs/commands/071-summary-kscan-final.log)

```bash
python src/summarize_benchmarks.py --phase kscan-r1 --methods mtp-k1 mtp-k2 mtp-k3 mtp-k4 mtp-k5 mtp-k6 mtp-k7 --concurrencies 1 4 16 32 --seeds 42 --num-prompts 32
```

## 485. 072-summary-semantic-final

- 状态：completed；退出码：0
- 开始：2026-11-24T16:26:37.315676+00:00
- 结束：2026-11-24T16:26:37.662015+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[072-summary-semantic-final.log](/home/genai/spec_decoding_study/logs/commands/072-summary-semantic-final.log)

```bash
python src/summarize_benchmarks.py --phase semantic-r1 --methods normal mtp-k3 dspark-k7 dspark-adaptive --concurrencies 1 4 16 32 --seeds 42 43 44 --dataset-name spec_bench --num-prompts 128 --output-len 256
```

## 486. 073-summary-dspark-policy-final

- 状态：completed；退出码：0
- 开始：2026-11-24T16:26:37.690146+00:00
- 结束：2026-11-24T16:26:37.842903+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[073-summary-dspark-policy-final.log](/home/genai/spec_decoding_study/logs/commands/073-summary-dspark-policy-final.log)

```bash
python src/summarize_benchmarks.py --phase policy-dspark-r1 --methods dspark-k7 dspark-adaptive --baseline-method dspark-k7 --best-fixed-methods dspark-k7 --concurrencies 1 4 16 32 --seeds 42 43 44 --num-prompts 32
```

## 487. 074-summary-dspark-high-final

- 状态：failed；退出码：1
- 开始：2026-11-24T16:26:37.869918+00:00
- 结束：2026-11-24T16:26:37.947929+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[074-summary-dspark-high-final.log](/home/genai/spec_decoding_study/logs/commands/074-summary-dspark-high-final.log)

```bash
python src/summarize_benchmarks.py --phase policy-dspark-high-r1 --methods dspark-k1 dspark-k3 dspark-k7 dspark-adaptive --baseline-method dspark-k7 --best-fixed-methods dspark-k1 dspark-k3 dspark-k7 --concurrencies 16 32 --seeds 42 43 44 --num-prompts 32
```

## 488. warmup-policy-mtp-r1-mtp-dynamic-smooth-c4

- 状态：completed；退出码：0
- 开始：2026-11-24T16:26:48.083282+00:00
- 结束：2026-11-24T16:26:58.360210+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-dynamic-smooth-c4.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-dynamic-smooth-c4.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 4 --seed 1004 --request-id-prefix warmup-policy-mtp-r1-mtp-dynamic-smooth-c4-
```

## 489. 074b-summary-dspark-high-final

- 状态：completed；退出码：0
- 开始：2026-11-24T16:26:48.463854+00:00
- 结束：2026-11-24T16:26:48.660665+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[074b-summary-dspark-high-final.log](/home/genai/spec_decoding_study/logs/commands/074b-summary-dspark-high-final.log)

```bash
python src/summarize_benchmarks.py --phase policy-dspark-r1 --output-stem policy-dspark-high-r1 --methods dspark-k1 dspark-k3 dspark-k7 dspark-adaptive --baseline-method dspark-k7 --best-fixed-methods dspark-k1 dspark-k3 dspark-k7 --concurrencies 16 32 --seeds 42 43 44 --num-prompts 32
```

## 490. 075-summary-semantic-adaptive-final

- 状态：completed；退出码：0
- 开始：2026-11-24T16:26:48.688735+00:00
- 结束：2026-11-24T16:26:48.870452+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[075-summary-semantic-adaptive-final.log](/home/genai/spec_decoding_study/logs/commands/075-summary-semantic-adaptive-final.log)

```bash
python src/summarize_benchmarks.py --phase semantic-r1 --output-stem semantic-r1-dspark-adaptive --methods dspark-k7 dspark-adaptive --baseline-method dspark-k7 --concurrencies 1 4 16 32 --seeds 42 43 44 --dataset-name spec_bench --num-prompts 128 --output-len 256
```

## 491. 076-summary-semantic-high-final

- 状态：completed；退出码：0
- 开始：2026-11-24T16:26:48.901051+00:00
- 结束：2026-11-24T16:26:49.102160+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[076-summary-semantic-high-final.log](/home/genai/spec_decoding_study/logs/commands/076-summary-semantic-high-final.log)

```bash
python src/summarize_benchmarks.py --phase semantic-r1 --output-stem semantic-r1-dspark-high --methods dspark-k1 dspark-k3 dspark-k7 dspark-adaptive --baseline-method dspark-k7 --best-fixed-methods dspark-k1 dspark-k3 dspark-k7 --concurrencies 16 32 --seeds 42 43 44 --dataset-name spec_bench --num-prompts 128 --output-len 256
```

## 492. policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c4-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:26:58.389652+00:00
- 结束：2026-11-24T16:27:19.707921+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c4-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c4-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 42 --request-id-prefix policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c4-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c4-s42.json --metadata method_name=mtp-dynamic-smooth dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=42 prefix_cache=false
```

## 493. policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c4-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:27:19.739112+00:00
- 结束：2026-11-24T16:27:41.664325+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c4-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c4-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 43 --request-id-prefix policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c4-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c4-s43.json --metadata method_name=mtp-dynamic-smooth dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=43 prefix_cache=false
```

## 494. policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c4-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:27:41.695473+00:00
- 结束：2026-11-24T16:28:03.359312+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c4-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c4-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 4 --seed 44 --request-id-prefix policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c4-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c4-s44.json --metadata method_name=mtp-dynamic-smooth dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=4 seed=44 prefix_cache=false
```

## 495. warmup-policy-mtp-r1-mtp-dynamic-smooth-c1

- 状态：completed；退出码：0
- 开始：2026-11-24T16:28:03.390607+00:00
- 结束：2026-11-24T16:28:17.824150+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[warmup-policy-mtp-r1-mtp-dynamic-smooth-c1.log](/home/genai/spec_decoding_study/logs/commands/warmup-policy-mtp-r1-mtp-dynamic-smooth-c1.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 4 --num-warmups 0 --max-concurrency 1 --seed 1001 --request-id-prefix warmup-policy-mtp-r1-mtp-dynamic-smooth-c1-
```

## 496. policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c1-s42

- 状态：completed；退出码：0
- 开始：2026-11-24T16:28:17.853678+00:00
- 结束：2026-11-24T16:29:08.778146+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c1-s42.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c1-s42.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 42 --request-id-prefix policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c1-s42- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c1-s42.json --metadata method_name=mtp-dynamic-smooth dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=42 prefix_cache=false
```

## 497. policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c1-s43

- 状态：completed；退出码：0
- 开始：2026-11-24T16:29:08.809158+00:00
- 结束：2026-11-24T16:30:00.222865+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c1-s43.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c1-s43.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 43 --request-id-prefix policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c1-s43- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c1-s43.json --metadata method_name=mtp-dynamic-smooth dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=43 prefix_cache=false
```

## 498. 077-figures-policy-layout

- 状态：completed；退出码：0
- 开始：2026-11-24T16:29:41.784746+00:00
- 结束：2026-11-24T16:29:48.693731+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[077-figures-policy-layout.log](/home/genai/spec_decoding_study/logs/commands/077-figures-policy-layout.log)

```bash
python src/make_figures.py --include-policies
```

## 499. policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c1-s44

- 状态：completed；退出码：0
- 开始：2026-11-24T16:30:00.253838+00:00
- 结束：2026-11-24T16:30:47.675781+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c1-s44.log](/home/genai/spec_decoding_study/logs/commands/policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c1-s44.log)

```bash
/usr/bin/env CUDA_VISIBLE_DEVICES=3 /home/genai/.pixi/envs/default/bin/vllm bench serve --backend openai --base-url http://127.0.0.1:8103 --endpoint /v1/completions --model qwen-target --tokenizer /home/model/Qwen3.8-27B-FP8 --dataset-name random --random-input-len 1024 --random-output-len 512 --random-range-ratio 0 --request-rate inf --ignore-eos --temperature 0 --top-p 1 --top-k -1 --percentile-metrics ttft,tpot,itl,e2el --metric-percentiles 50,90,95,99 --disable-tqdm --num-prompts 32 --num-warmups 0 --max-concurrency 1 --seed 44 --request-id-prefix policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c1-s44- --save-result --save-detailed --result-dir /home/genai/spec_decoding_study/results/raw --result-filename policy-mtp-r1-mtp-dynamic-smooth-i1024-o512-c1-s44.json --metadata method_name=mtp-dynamic-smooth dataset_name=random mode=mtp k=-1 gpu=3 phase=policy-mtp-r1 concurrency=1 seed=44 prefix_cache=false
```

## 500. 078-summary-mtp-complete

- 状态：completed；退出码：0
- 开始：2026-11-24T16:33:48.826822+00:00
- 结束：2026-11-24T16:33:49.097723+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[078-summary-mtp-complete.log](/home/genai/spec_decoding_study/logs/commands/078-summary-mtp-complete.log)

```bash
python src/summarize_benchmarks.py --phase policy-mtp-r1 --methods normal mtp-k3 mtp-k5 mtp-k6 mtp-k7 mtp-dynamic-oracle mtp-dynamic-smooth --best-fixed-methods mtp-k3 mtp-k5 mtp-k6 mtp-k7 --concurrencies 1 4 16 32 --seeds 42 43 44 --num-prompts 32
```

## 501. 079-summary-mtp-complete-explicit-baselines

- 状态：completed；退出码：0
- 开始：2026-11-24T16:36:14.841997+00:00
- 结束：2026-11-24T16:36:15.116097+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[079-summary-mtp-complete-explicit-baselines.log](/home/genai/spec_decoding_study/logs/commands/079-summary-mtp-complete-explicit-baselines.log)

```bash
python src/summarize_benchmarks.py --phase policy-mtp-r1 --methods normal mtp-k3 mtp-k5 mtp-k6 mtp-k7 mtp-dynamic-oracle mtp-dynamic-smooth --additional-baseline-methods mtp-k3 mtp-k5 mtp-k6 mtp-k7 mtp-dynamic-smooth --best-fixed-methods mtp-k3 mtp-k5 mtp-k6 mtp-k7 --concurrencies 1 4 16 32 --seeds 42 43 44 --num-prompts 32
```

## 502. 080-figures-final

- 状态：completed；退出码：0
- 开始：2026-11-24T16:39:22.443617+00:00
- 结束：2026-11-24T16:39:30.430526+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[080-figures-final.log](/home/genai/spec_decoding_study/logs/commands/080-figures-final.log)

```bash
python src/make_figures.py --include-policies
```

## 503. 081-markdown-tables-final

- 状态：completed；退出码：0
- 开始：2026-11-24T16:39:30.588093+00:00
- 结束：2026-11-24T16:39:30.618827+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[081-markdown-tables-final.log](/home/genai/spec_decoding_study/logs/commands/081-markdown-tables-final.log)

```bash
python src/export_markdown_tables.py --phases formal-r1 semantic-r1 policy-mtp-fixed-r1 policy-mtp-r1 policy-dspark-r1 policy-dspark-high-r1 semantic-r1-dspark-adaptive semantic-r1-dspark-high
```

## 504. 082-figures-final-layout

- 状态：completed；退出码：0
- 开始：2026-11-24T16:40:44.927945+00:00
- 结束：2026-11-24T16:40:53.027253+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[082-figures-final-layout.log](/home/genai/spec_decoding_study/logs/commands/082-figures-final-layout.log)

```bash
python src/make_figures.py --include-policies
```

## 505. 083-artifact-validation-final

- 状态：completed；退出码：0
- 开始：2026-11-24T16:41:26.893028+00:00
- 结束：2026-11-24T16:41:27.712822+00:00
- 工作目录：`/home/genai/spec_decoding_study`
- 输出日志：[083-artifact-validation-final.log](/home/genai/spec_decoding_study/logs/commands/083-artifact-validation-final.log)

```bash
python src/validate_results.py --required-summaries formal-r1 kscan-r1 semantic-r1 policy-mtp-fixed-r1 policy-mtp-r1 policy-dspark-r1 policy-dspark-high-r1 semantic-r1-dspark-adaptive semantic-r1-dspark-high
```
