# 早期 Suffix Decoding 实验

这次实验在单张 NVIDIA B200 上运行 Qwen3.8-27B-FP8，使用 vLLM 0.34.0、Triton Attention 和标准验证。三种候选方案中，Suffix Decoding 的留出集得分最高，为 1.249×。这个分数取并发 1 和 16 的相对吞吐倍率中位数，再作几何平均。每轮与同卡 Normal 配对。[原课程项目](https://github.com/Zheng-Hanyu/Generative-Models-Final-Project) · [vLLM 方法说明](https://docs.vllm.ai/en/v0.34.0/features/speculative_decoding/)

## 最终配置

```json
{
  "method": "suffix",
  "num_speculative_tokens": 4,
  "suffix_decoding_max_tree_depth": 12
}
```

## 留出集实测

| 并发 | Normal (tok/s) | Suffix (tok/s) | 配对倍率中位数 | 三轮倍率范围 | P95 TPOT（ms，Normal / Suffix） | 草稿接受率 | 文本完全一致 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 116.90 | 174.89 | 1.494× | 1.446–1.547× | 8.42 / 6.93 | 17.4% | 23/144 |
| 16 | 1349.96 | 1415.71 | 1.045× | 1.037–1.083× | 11.36 / 11.84 | 19.1% | 36/144 |

Suffix 和 Normal 各成功处理了 288 条请求。按相同种子和并发配对后，59 条 greedy 输出全文一致。比较包含推理文本，部分输出在 128 tokens 处截断。留出集记录的是全文是否一致，答案得分只用于另做的短答检查。

短答检查使用 20 道有标准答案的题。关闭思考后用 greedy 解码，两种配置按预设规则均通过 17 道，失分题相同。[逐题结果](../../results/raw/supplemental_speculative/short-answer.json)

Spec-Bench 的 480 条原题按类别分为 144 条调参题和 336 条留出题。种子 43、44、45 各在并发 1 和 16 测量一次。六个留出子集各有 56 条候选题，题号和首轮提示互不重叠。每轮用 4 条额外问题预热，正式计时测 48 条。两种配置都关闭 vLLM 前缀缓存，压测请求饱和到达。[Spec-Bench 原始数据](https://github.com/hemingkx/Spec-Bench/blob/66230f10cb0a02aced5ef3ce1e85163c16160454/data/spec_bench/question.jsonl)

每轮先求逐请求 TPOT 的第 95 百分位，再取三轮中位数。TPOT 是首 token 之后的平均每 token 时间。吞吐用实际输出 token 数除以耗时。并发 16 时，Suffix 的吞吐有小幅提升，P95 TPOT 从 11.36 ms 升至 11.84 ms。

## 调参记录

第一轮扫描草稿上限 K，第二轮固定选出的 K，再调整最大树深。每个设置在并发 1 和 16 各跑 24 条，以两档输出 TPS 的几何平均打分。分数从首轮最高的 528.23 升至 538.52，增加 1.9%。候选方案的排名由独立留出集决定。

| 调参轮次 | 草稿上限 K | 匹配参数 | C=1 tok/s | C=16 tok/s | 调参分数 | 入选 |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 4 | 24 | 173.15 | 1611.50 | 528.23 |  |
| 1 | 8 | 24 | 177.51 | 1561.28 | 526.45 |  |
| 1 | 12 | 24 | 153.66 | 1454.70 | 472.78 |  |
| 2 | 4 | 12 | 172.77 | 1678.56 | 538.52 | ✓ |
| 2 | 4 | 36 | 172.91 | 1636.30 | 531.92 |  |

在这组配置下，启动日志显示默认 FlashInfer 将推测解码的 CUDA Graph 模式设为 `NONE`。Triton Attention 可以完整捕获 CUDA Graph，因此 Suffix 和 Normal 都使用 Triton。

## 复跑

在装有 vLLM 0.34.0 和目标权重的 B200 主机上，从仓库根目录运行。用 `serve` 单独启动 Suffix 服务。

```bash
python_bin=/home/genai/.pixi/envs/default/bin/python
"$python_bin" src/run_supplemental_benchmark.py serve --gpu 7 --port 24807
```

GPU 空闲时可用 `benchmark` 复跑。脚本从 `data/spec_bench/question.jsonl` 生成留出子集，在同卡依次测 Suffix 和 Normal，并把 JSON 和日志写到新的结果目录。pandas 如安装在单独目录，可通过 `--bench-deps` 指定。用 `--model` 和 `--vllm` 设置本机路径。

```bash
"$python_bin" src/run_supplemental_benchmark.py benchmark --gpu 7 --port 24807 --output replay-supplemental
```

[最终复测汇总](../../results/processed/supplemental_speculative_summary.json) · [原始复测 JSON](../../results/raw/supplemental_speculative/) · [最终配置](../../config/supplemental_speculative_config.json) · [复跑入口](../../src/run_supplemental_benchmark.py)
