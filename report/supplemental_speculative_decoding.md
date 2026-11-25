# Qwen3.8-27B-FP8 · Suffix Decoding

Suffix Decoding 在三种候选方案中取得最高留出集得分 **1.249×**。得分是并发 1 和 16 下相对同 GPU Normal 的配对吞吐倍率中位数的几何平均。测试使用单张 NVIDIA B200、vLLM 0.34.0、Triton Attention 和标准验证。[原课程项目](https://github.com/Zheng-Hanyu/Generative-Models-Final-Project) · [vLLM 方法说明](https://docs.vllm.ai/en/v0.34.0/features/speculative_decoding/)

## 最终配置

```json
{
  "method": "suffix",
  "num_speculative_tokens": 4,
  "suffix_decoding_max_tree_depth": 12
}
```

## 留出集实测

| 并发 | Normal tok/s | 优胜方法 tok/s | 配对倍率中位数 | 三轮倍率范围 | P95 TPOT（ms，Normal / 优胜） | 草稿接受率 | 文本完全一致 |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 116.90 | 174.89 | 1.494× | 1.446–1.547× | 8.42 / 6.93 | 17.4% | 23/144 |
| 16 | 1349.96 | 1415.71 | 1.045× | 1.037–1.083× | 11.36 / 11.84 | 19.1% | 36/144 |

优胜方法和 Normal 各跑完 **288 条**请求，全部成功。Greedy 生成全文有 **59/288** 条和同种子、同并发的 Normal 完全一致。全文比较包含推理文本，128-token 上限会截断部分输出。该指标用于检查输出差异。留出集题目的答案正确率未评分。

另做 20 道有标准答案的短答检查，关闭思考、使用 greedy 解码。按预设答案规则，两种配置均通过 **17/20**，未通过的题目相同。[逐题结果](../results/raw/supplemental_speculative/short-answer.json)

每个种子在并发 1 和 16 各测 48 条，种子为 43、44、45。Spec-Bench 的 480 条原题按类别分成 144 条调参题和 336 条留出题。六个留出子集各有 56 条候选题，分组间题号和首轮提示文本均无重叠。每格测量前用 4 条额外问题预热，正式题没有被用作预热。两种配置均关闭 vLLM 前缀缓存，压测请求饱和到达。[Spec-Bench 原始数据](https://github.com/hemingkx/Spec-Bench/blob/66230f10cb0a02aced5ef3ce1e85163c16160454/data/spec_bench/question.jsonl)

P95 TPOT 表示每条请求首 token 之后的平均每 token 时间的第 95 百分位，再取三轮中位数。吞吐以实际输出 token 数和测试耗时计算。并发 16 下，Suffix 的整体吞吐更高，P95 TPOT 从 11.36 ms 升到 11.84 ms。

## 调参记录

第一轮扫描草稿上限 K，第二轮固定首轮最优 K，调整最大树深。每个设置在并发 1 和 16 各跑 24 条，使用两档输出 TPS 的几何平均作为调参分数。调参分数从首轮最优的 **528.23** 变化到最终的 **538.52**，变化 **+1.9%**。最终胜负使用独立留出集决定。

| 调参轮次 | 草稿上限 K | 匹配参数 | C=1 tok/s | C=16 tok/s | 调参分数 | 入选 |
|---:|---:|---:|---:|---:|---:|---|
| 1 | 4 | 24 | 173.15 | 1611.50 | 528.23 |  |
| 1 | 8 | 24 | 177.51 | 1561.28 | 526.45 |  |
| 1 | 12 | 24 | 153.66 | 1454.70 | 472.78 |  |
| 2 | 4 | 12 | 172.77 | 1678.56 | 538.52 | ✓ |
| 2 | 4 | 36 | 172.91 | 1636.30 | 531.92 |  |

后端探针发现默认 FlashInfer 在此配置下把推测解码的 CUDA Graph 模式降为 `NONE`。Triton Attention 的启动日志确认完整 CUDA Graph 捕获，正式调参和复测均采用 Triton。留出集比较表中的 Normal 也使用 Triton，控制后端差异。

## 复跑

在装有 B200、vLLM 0.34.0 和目标权重的主机上，从仓库根目录执行。复跑入口从仓库现有的 `data/spec_bench/question.jsonl` 生成留出子集。启动服务时使用 `serve`，复测时使用 `benchmark`。后者在同卡依次测试优胜配置和 Normal，并将 JSON 与日志写入新的结果目录。

```bash
python_bin=/home/genai/.pixi/envs/default/bin/python
"$python_bin" src/run_supplemental_benchmark.py serve --gpu 7 --port 24807
```

在该 GPU 空闲时复跑压测。如果 vLLM 环境缺少 pandas，可安装到单独的依赖目录并通过 `--bench-deps` 指定。模型和 vLLM 路径可用 `--model`、`--vllm` 覆盖。

```bash
"$python_bin" src/run_supplemental_benchmark.py benchmark --gpu 7 --port 24807 --output replay-supplemental
```

[最终复测汇总](../results/processed/supplemental_speculative_summary.json) · [原始复测 JSON](../results/raw/supplemental_speculative/) · [最终配置](../config/supplemental_speculative_config.json) · [复跑入口](../src/run_supplemental_benchmark.py)
