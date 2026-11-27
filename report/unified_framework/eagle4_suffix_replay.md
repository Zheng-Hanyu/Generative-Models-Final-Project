# 复跑 EAGLE-4、自适应 Suffix 和 DFlash 2 对照

从仓库根目录执行。使用单张 NVIDIA B200、同一份 Qwen3.8-27B-FP8 权重和 NVIDIA CUDA 13 驱动。安装 vLLM 0.34.0 及其压测依赖，包括 pandas。客户端和 Suffix、DFlash 2 服务都用这套版本。每个方法的 Normal 在同一个服务二进制下运行。

```bash
standard_vllm=/home/genai/.pixi/envs/default/bin/vllm
target=/home/model/Qwen3.8-27B-FP8
bench_deps=/home/genai/dspark-bench/bench-deps
gpu=7
replay_root="$(pwd)/replay/eagle4-suffix-b200"
mkdir -p "$replay_root"

python src/replay_selected_speculation.py --method suffix --gpu "$gpu" \
  --vllm "$standard_vllm" --client-vllm "$standard_vllm" \
  --bench-deps "$bench_deps" --model "$target" --output "$replay_root/suffix"
```

如果 pandas 已安装在客户端环境中，可以省略 --bench-deps。每套压测生成 18 组输入，各组均记录 SHA-256。方法和配对 Normal 各完成 540 条请求，逐组的 JSON 和服务日志保存在输出目录。

## EAGLE-4

在独立 Python 3.12 环境安装作者构建。实测环境复用了服务器上已有的 Torch 2.14.0，并在独立环境中安装匹配的 vLLM、EAGLE Harness、FlashInfer 和 Transformers。 [固定的 wheel 和草稿版本](../../config/eagle4_suffix_b200.json)

```bash
eagle_env="$replay_root/.venv-eagle"
eagle_draft="$replay_root/draft-eagle"
calibration="$(pwd)/config/eagle4_b200_calibration"

python3.12 -m venv "$eagle_env"
"$eagle_env/bin/python" -m pip install \
  'eagle-harness[vllm]==0.1.4' 'vllm==0.32.0rc1.dev283+eagle.5' \
  --extra-index-url https://eagle-hq.github.io/EAGLE-4/whl/cu130/ \
  --extra-index-url https://download.pytorch.org/whl/cu130
"$eagle_env/bin/eagle-harness-check"

hf download EAGLE-Corp/Qwen3.8-27B-EAGLE4 config.json model.safetensors \
  --revision f58a5985223040552ad404fba98f0dd27f5f676a --local-dir "$eagle_draft"
python src/replay_selected_speculation.py --method eagle4 --gpu "$gpu" \
  --vllm "$eagle_env/bin/vllm" --client-vllm "$standard_vllm" \
  --bench-deps "$bench_deps" --model "$target" --draft-model "$eagle_draft" --calibration "$calibration" \
  --output "$replay_root/eagle4"
```

成本表与引擎版本、GPU 型号和模型配置绑定，也会校验模型目录的最后一级名称。使用其他名称、模型配置或 GPU 时，先把 calibration 指到一个新目录，再在该 GPU 上重新校准。 [EAGLE-4 vLLM 指南](https://github.com/eagle-hq/EAGLE-4/blob/main/docs/quickstart-vllm.md)

```bash
calibration="$replay_root/calibration-tp1"
CUDA_VISIBLE_DEVICES="$gpu" VLLM_USE_V2_MODEL_RUNNER=1 HF_HUB_OFFLINE=1 \
  "$eagle_env/bin/eagle-harness" calibrate --engine vllm --tp 1 \
  --model "$target" --draft "$eagle_draft" --output "$calibration" \
  --engine-args '{"linear_backend":"flashinfer_cutedsl","language_model_only":true,"enable_prefix_caching":false}'
```

## DFlash 2 对照

使用统一框架发布的 DFlash 2 MXFP8 设置和固定版本的草稿。 [下载与原有负载说明](README.md)

```bash
dflash_draft="$replay_root/Qwen3.8-27B-DFlash2"
hf download incoai/Qwen3.8-27B-DFlash2 config.json model.safetensors \
  --revision 015e795645c74b1a0eeef3b570031fb62e769bc5 --local-dir "$dflash_draft"
python src/replay_selected_speculation.py --method dflash --gpu "$gpu" \
  --vllm "$standard_vllm" --client-vllm "$standard_vllm" \
  --bench-deps "$bench_deps" --model "$target" --draft-model "$dflash_draft" --output "$replay_root/dflash"
```

[实测结果](eagle4_suffix.md)
