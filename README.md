# Qwen3.8-27B-FP8 推测解码实测

周熙言（`xiyanzhou`）在单张 NVIDIA B200 上测量 Qwen3.8-27B-FP8 的输出吞吐、P95 首 token 延迟（TTFT）、P95 每 token 延迟（TPOT）和草稿接受率。每种方法都用同一张卡、同一引擎构建下的 Normal 做对照。

| 实验 | 方法和负载 |
|---|---|
| [公开负载](report/unified_framework/results.md) | Native MTP、DSpark、DFlash 2。测 Spec-Bench、SPEED-Bench、BurstGPT v2.0 和随机压力，另测 DFlash 2 草稿量化。 |
| [重复输出对照](report/unified_framework/eagle4_suffix.md) | EAGLE-4、自适应 Suffix、DFlash 2。测 Spec-Bench 留出集，以及合成的重复代码编辑和 JSON 输出。 |
| [标准 Suffix](report/unified_framework/early_suffix.md) | 固定 K=4。在另一套 Spec-Bench 划分上测吞吐、延迟和输出一致性，另做了短答检查。 |

公开负载实验中，Native MTP 和 DSpark 在 Spec-Bench 上分别达到 Normal 的 1.998× 和 2.282×。DFlash 2 的 MXFP8 草稿把模型加载显存从 31.31 GiB 降到 29.64 GiB，综合吞吐为 BF16 的 1.001×。[公开负载结果](report/unified_framework/results.md)

在 EAGLE-4 与自适应 Suffix 的对照中，Spec-Bench 上 DFlash 2 的综合吞吐倍率最高（2.402×），合成重复负载上则是自适应 Suffix（3.127×）。EAGLE-4 在这两类负载上分别达到 2.322× 和 2.288×。综合倍率先取每档并发三轮的配对中位数，再作几何平均。[绝对吞吐和尾延迟](report/unified_framework/eagle4_suffix.md)

![Spec-Bench 与合成重复负载的配对吞吐曲线](report/unified_framework/figures/eagle4-suffix-throughput.png)

## 使用

从仓库根目录运行。下面的命令会列出发布配置、生成 DSpark 的压测计划，并从现有 JSON 重生成三组实验的 Markdown 和三种图表格式（PDF、SVG、300 dpi PNG）。查看计划和出图只需要 Python 3.11 或更新版本，出图还需 Matplotlib。

```bash
python src/unified_framework.py profiles
python src/unified_framework.py benchmark --method dspark --print-plan --output replay/dspark-plan
python -m pip install matplotlib==3.11.2
python src/unified_framework.py report --output replay/report
```

在 B200 上复跑时，用 `prepare` 生成输入，用 `serve` 单独启动某个配置，或用 `benchmark` 自动跑方法和 Normal。公开负载支持 `tune`，DFlash 2 草稿量化使用 `quantization-study`。Native MTP 使用主模型内置的头，DSpark 和 DFlash 2 需要各自的草稿权重，EAGLE-4 还需要独立的 vLLM 构建。[实验协议和复跑](report/unified_framework/README.md) · [EAGLE-4 环境](report/unified_framework/eagle4_suffix_replay.md) · [统一配置](config/unified_framework.json)
