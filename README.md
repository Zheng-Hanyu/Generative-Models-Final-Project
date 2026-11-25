# 生成模型推理加速：Speculative Decoding 性能研究

本仓库记录基于 **vLLM 0.34.0、Qwen3.8-27B-FP8 与 NVIDIA B200** 的投机解码实验，当前内容对应 **2026-11-24 已完成的第一阶段研究**。实验覆盖 Normal、Native MTP、DSpark、固定草稿长度扫描、按 batch size 动态选 K，以及 DSpark Adaptive Verification。

完整分析见 **[中文技术报告](report/speculative_decoding_report.md)**；原始 Benchmark JSON、处理结果、图表和运行日志均保留在仓库中。

## 1. 模型与方法

| 名称 | 使用的模型 | 工作方式 |
|---|---|---|
| Normal | Qwen3.8-27B-FP8，27B | 标准自回归解码，不使用草稿模型，是性能基线。 |
| Native MTP | 同一 Target checkpoint 自带的 MTP head | 递归产生 $K$ 个候选 token，再由 Target 并行验证；无需额外加载独立 draft checkpoint。 |
| DSpark | 本地 Qwen3.8-27B-DSpark-vLLM，1.86B，BF16 | 使用独立 drafter 按块生成候选，默认块长为 7；checkpoint 带 confidence head，可启用 Adaptive Verification。 |

模型权重未放入 GitHub。原始服务器中的 Target 路径为 `/home/model/Qwen3.8-27B-FP8`，DSpark drafter 路径为 `/home/genai/models/Qwen3.8-27B-DSpark-vLLM`；完整环境记录见 [experiment_protocol.json](config/experiment_protocol.json)。

设第 $i$ 个草稿位置的无条件接受概率为 $p_i$，包含 bonus token 的期望接受长度为：

$$
A(K)=1+\sum_{i=1}^{K}p_i.
$$

在持续有 $C$ 个请求解码的理想化稳态下，可用下式理解吞吐与草稿长度、周期成本的关系：

$$
\mathrm{OutputTPS}\approx C\cdot\frac{A(K)}{T_{\mathrm{cycle}}(C,K)}.
$$

因此，更长的草稿并不必然更快：它既提高接受长度，也增加 Draft、Verify 和调度成本。

## 2. 已完成的 Baseline

正式随机负载使用固定输入 1024 tokens、输出 512 tokens，每次 128 请求；并发为 $C\in\{1,4,16,32\}$，每种配置以 seed 42、43、44 独立运行三次。下表为三轮平均输出吞吐，括号内为相对同 seed Normal 的平均配对加速比。

| 并发 | Normal (tokens/s) | MTP K=3 (tokens/s) | DSpark K=7 (tokens/s) |
|---:|---:|---:|---:|
| 1 | 117.10 | 325.82（2.783×） | 235.12（2.008×） |
| 4 | 432.54 | 1085.63（2.510×） | 753.72（1.743×） |
| 16 | 1438.59 | 2382.18（1.656×） | 1832.41（1.274×） |
| 32 | 2325.83 | 3913.63（1.683×） | 2362.21（1.016×） |

此外，已使用 **Spec-Bench 480 条真实语义问题**完成 36 次正式 Benchmark，覆盖 writing、roleplay、reasoning、math、coding、translation、RAG 等类别。真实任务改变了部分草稿接受行为和模型排序，因此报告分别呈现随机负载与语义负载，没有用合成分布代替真实任务结论。

## 3. 初步动态优化结果

MTP 已完成 $K=1\ldots7$ 扫描，并在同一 GPU 上对 Normal、固定 K 和动态策略做三轮复测。三轮均值下，各并发点的最佳固定配置与 Dynamic-Smooth 结果如下。

| 并发 | 三轮均值最佳固定 K | Dynamic-Smooth 相对 Normal 的配对加速 |
|---:|---:|---:|
| 1 | K=7 | 3.361× |
| 4 | K=7 | 2.766× |
| 16 | K=5 | 1.967× |
| 32 | K=3 | 1.558× |

Dynamic-Smooth 使用按 batch size 选择 K 的表，在 $C=16,32$ 接近当轮最佳固定 K，但**尚未证明稳定超过每个负载上的最佳固定配置**。因此，当前更准确的结论是“动态选 K 能接近负载相关的固定最优”，而不是“动态策略已经全面优于固定 K”。

DSpark Adaptive Verification 已分别完成随机与 Spec-Bench 负载评估。它在部分高负载场景中优于默认 K=7，但随机 $C=32$ 时仍仅为固定 K=3 的约 **0.900×**，说明自适应验证不能替代针对目标负载的固定 K 调优。

详细数据见 [MTP 策略汇总](results/processed/policy-mtp-r1-summary.json)、[DSpark 策略汇总](results/processed/policy-dspark-r1-summary.json) 和 [报告第 5–7 节](report/speculative_decoding_report.md)。

## 4. 仓库目录

- [report/speculative_decoding_report.md](report/speculative_decoding_report.md)：完整中文技术报告。
- [report/figures/](report/figures/)：41 组 PNG 图及对应 SVG，共 82 个文件。
- [report/tables/](report/tables/)：报告使用的 Markdown 汇总表。
- [report/command_audit.md](report/command_audit.md)：第一阶段主要命令审计。
- [src/](src/)：Benchmark 矩阵、K 扫描、统计汇总、校验和绘图代码。
- [bin/](bin/)：日志包装、后台服务启动与停止工具。
- [config/](config/)：模型环境、实验协议和各策略的 speculative config。
- [data/spec_bench/](data/spec_bench/)：Spec-Bench 输入数据及其原始记录。
- [results/raw/](results/raw/)：274 份第一阶段原始 JSON 与 GPU 时间序列。
- [results/processed/](results/processed/)：80 份汇总、逐次运行 CSV、manifest 和校验文件。
- [logs/](logs/)：第一阶段服务与 Benchmark 日志；运行记录按 label 对应。

## 5. 复现入口

建议使用 Python 3.12、vLLM 0.34.0 和与实验兼容的 PyTorch/CUDA 环境。脚本保留了原始服务器的模型与 vLLM 可执行文件路径；在其他机器复现时，请先修改 `src/run_server_suite.py`、`src/run_k_scan.py` 中的 `TARGET`、`VLLM` 等路径常量。

在仓库根目录运行以下命令，可顺序启动服务并复测 Normal、MTP K=3 和 Dynamic-Smooth：

```bash
python src/run_server_suite.py \
  --config config/mtp_policy_comparison.json \
  --gpu 0 \
  --port 8100 \
  --phase reproduce-mtp-r1 \
  --label-prefix local \
  --methods normal mtp-k3 mtp-dynamic-smooth \
  --num-prompts 32 \
  --seeds 42 43 44 \
  --concurrencies 1 4 16 32 \
  --input-len 1024 \
  --output-len 512
```

每个配置会自动完成 warmup、保存逐次 JSON 和 manifest，并在结束后停止对应服务。结果汇总、校验和绘图的完整命令见技术报告第 8 节；不要在已有正式结果上使用相同 phase 覆盖原始记录。

## 6. 数据完整性与协作约定

第一阶段共校验 **274 份原始 JSON、260 次核心 Benchmark、17,816 个完成请求**，校验错误数为 0。逐文件 SHA-256 见 [raw-sha256.csv](results/processed/raw-sha256.csv)，完整检查见 [artifact-validation.json](results/processed/artifact-validation.json)。

后续协作建议为新实验使用新的 `phase` 和结果标签，保持原始 JSON 只追加、不修改；性能结论应保留同 seed 配对、三轮重复和关键配置的同卡顺序复测。
