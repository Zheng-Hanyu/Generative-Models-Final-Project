# Qwen3.8-27B 推测解码实验

<img src="report/unified_framework/icon.svg" width="58" alt="推测解码框架图标">

在 NVIDIA B200 上，我们用 vLLM 0.34.0 测量 Qwen3.8-27B-FP8 的输出吞吐和延迟。当前版本用 Spec-Bench、NVIDIA SPEED-Bench 和 BurstGPT v2.0 比较自回归基线 Normal 与 Native MTP、DSpark、DFlash 2。每种方法发布一套配置。

运行 `python src/unified_framework.py profiles` 查看发布配置。同一 CLI 可启动 vLLM、调参、配对压测和出图。[复跑命令](report/unified_framework.md) · [当前实测与图表](report/unified_framework/results.md)

课程实验记录了固定草稿长度扫描、按 batch size 动态选 K 和 DSpark Adaptive Verification。早期 Suffix 实验另有两轮调参和三轮留出集复测。[课程实验报告](report/speculative_decoding_report.md) · [Suffix 实验](report/supplemental_speculative_decoding.md)

## 课程实验的模型与方法

| 名称 | 使用的模型 | 工作方式 |
|---|---|---|
| Normal | Qwen3.8-27B-FP8，27B | 标准自回归解码，作为吞吐和延迟基线。 |
| Native MTP | 目标模型自带的 MTP head | 递归生成 $K$ 个候选 token，再由目标模型并行验证。 |
| DSpark | 本地 Qwen3.8-27B-DSpark-vLLM，1.86B，BF16 | 独立草稿模型按块生成候选。课程实验用 K=7 作为初始值，并通过 confidence head 测试 Adaptive Verification。 |

请在运行环境中准备权重。原实验的目标模型位于 `/home/model/Qwen3.8-27B-FP8`，DSpark 草稿模型位于 `/home/genai/models/Qwen3.8-27B-DSpark-vLLM`。[实验协议](config/experiment_protocol.json)

设第 $i$ 个草稿位置的无条件接受概率为 $p_i$。期望接受长度包含一个 bonus token。

$$
A(K)=1+\sum_{i=1}^{K}p_i.
$$

在持续有 $C$ 个请求解码的理想稳态下，吞吐约为

$$
\mathrm{OutputTPS}\approx C\cdot\frac{A(K)}{T_{\mathrm{cycle}}(C,K)}.
$$

草稿越长，每步可接受的 token 越多，起草、验证和调度也会花更多时间。净收益取决于这两项变化的幅度。

## 课程实验的随机负载基线

每轮有 128 个随机请求，固定输入为 1,024 tokens，输出为 512 tokens。每个方法和并发组合使用种子 42、43、44 各跑一次。表中为三轮平均输出吞吐，括号内为与同种子 Normal 配对后的平均倍率。

| 并发 | Normal (tokens/s) | MTP K=3 (tokens/s) | DSpark K=7 (tokens/s) |
|---:|---:|---:|---:|
| 1 | 117.10 | 325.82（2.783×） | 235.12（2.008×） |
| 4 | 432.54 | 1085.63（2.510×） | 753.72（1.743×） |
| 16 | 1438.59 | 2382.18（1.656×） | 1832.41（1.274×） |
| 32 | 2325.83 | 3913.63（1.683×） | 2362.21（1.016×） |

Spec-Bench 的 36 次运行使用含 480 条提示的数据集，涵盖写作、角色扮演、推理、数学、编程、翻译和 RAG。两套负载的草稿接受行为和方法排序有差异。[随机负载与 Spec-Bench 对比](report/speculative_decoding_report.md)

## 动态草稿长度

扫描 $K=1\ldots7$ 后，我们在同一张 GPU 上对 Normal、固定 K 和动态策略各复测三轮。固定 K 按三轮平均吞吐选出。

| 并发 | 三轮均值最佳固定 K | Dynamic-Smooth 相对 Normal 的配对加速 |
|---:|---:|---:|
| 1 | K=7 | 3.361× |
| 4 | K=7 | 2.766× |
| 16 | K=5 | 1.967× |
| 32 | K=3 | 1.558× |

Dynamic-Smooth 按 batch size 选 K，在 $C=16,32$ 的吞吐接近同批复测中各自最好的固定配置。三轮数据不足以确认它能稳定超过各并发下的固定最优值。

DSpark Adaptive Verification 在部分高负载下快于默认 K=7。随机负载 $C=32$ 时，它的吞吐约为固定 K=3 的 0.900×。

详细数据见 [MTP 策略汇总](results/processed/policy-mtp-r1-summary.json)、[DSpark 策略汇总](results/processed/policy-dspark-r1-summary.json) 和 [报告第 5–7 节](report/speculative_decoding_report.md)。

## 仓库目录

- 课程实验有 41 张图，每张提供 PNG 和 SVG。数据表可直接阅读。[图表](report/figures/) · [汇总表](report/tables/)
- 第一阶段有 274 份原始 JSON，另有 GPU 时间序列。原报告的 80 份派生文件包括汇总、逐轮 CSV、实验清单和校验记录。[原始数据](results/raw/) · [汇总数据](results/processed/)
- 第一阶段的服务与压测日志按运行标签查找。[命令记录](report/command_audit.md) · [日志](logs/)
- 源码包含统一 CLI、课程实验复跑脚本和日志工具。[源码](src/) · [日志工具](bin/)
- 仓库提供模型清单、协议和策略参数。[配置](config/) · [Spec-Bench 输入](data/spec_bench/)


