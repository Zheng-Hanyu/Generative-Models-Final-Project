# Qwen3.8-27B-FP8 推测解码实测

周熙言（`xiyanzhou`）提交的单卡 NVIDIA B200 推理实验和复现代码。使用同一份 Qwen3.8-27B-FP8 主模型，对每种推测解码设置跑同卡 Normal 对照，记录输出吞吐、P95 首 token 延迟（TTFT）、P95 每 token 延迟（TPOT）和草稿接受率。

## 主要结果

在最近一轮配对实验中，**DFlash 2 在 Spec-Bench 上的综合吞吐倍率最高，为 2.402×。自适应 Suffix 在重复代码编辑和 JSON 输出负载上最高，为 3.127×。** EAGLE-4 在两类负载上分别为 2.322× 和 2.288×。倍率均以各方法所在的引擎构建的 Normal 为基准，每档并发跑三轮。 [完整结果与绝对吞吐](report/unified_framework/eagle4_suffix.md)

![Spec-Bench 与重复代码／JSON 的配对吞吐倍率，按并发分面](report/unified_framework/figures/eagle4-suffix-throughput.png)

| 实验 | 测了什么 | 报告与产物 |
|---|---|---|
| 统一框架 | Native MTP、DSpark 和 DFlash 2 在 Spec-Bench、SPEED-Bench、BurstGPT v2.0 和随机压力下的表现。另测 DFlash 2 的草稿量化，MXFP8 将模型加载显存从 31.31 GiB 降到 29.64 GiB，综合吞吐为 BF16 的 1.001×。 | [结果和图表](report/unified_framework/results.md) · [实验协议与复跑](report/unified_framework/README.md) · [逐轮数据](results/processed/unified-framework/summary.json) |
| EAGLE-4 与自适应 Suffix | 各自选出一套设置，在 Spec-Bench 留出集与独立合成负载上对照 Normal 和 DFlash 2。 | [结果和图表](report/unified_framework/eagle4_suffix.md) · [复跑说明](report/unified_framework/eagle4_suffix_replay.md) · [逐轮数据](results/processed/unified-framework/eagle4-suffix-b200.json) |
| 早期标准 Suffix | 在另一套 Spec-Bench 留出划分上测固定 `K=4` 的 Suffix，以及输出一致性和短答结果。 | [报告与复跑](report/unified_framework/early_suffix.md) · [原始结果](results/raw/supplemental_speculative/) |

三组实验各自使用报告中的负载划分、控制组和统计口径。比较部署效果时，可结合同一组实验里的绝对吞吐和尾延迟。

## 复现图表

从仓库根目录运行以下命令。两条出图命令都从已发布的 JSON 读取数据，输出 PNG 和 SVG。

```bash
python -m pip install matplotlib==3.11.2
python src/unified_framework.py report \
  --results results/processed/unified-framework/summary.json --output replay/unified
python src/plot_eagle4_suffix.py --output replay/eagle4-suffix/figures
```

服务启动和重新压测需要 B200、匹配的 vLLM 构建及模型权重。仓库收录的 Spec-Bench 题目用于复跑，SPEED-Bench 和 BurstGPT 的版本、下载来源及使用方式见实验协议。 [Spec-Bench 上游](https://github.com/hemingkx/Spec-Bench) · [实验协议](report/unified_framework/README.md#实验协议)
