# Qwen3.8-27B-FP8 推测解码实测

周熙言（`xiyanzhou`）在单张 NVIDIA B200 上测量 Qwen3.8-27B-FP8 的输出吞吐、P95 首 token 延迟（TTFT）、P95 每 token 延迟（TPOT）和草稿接受率。每个吞吐倍率先按同卡、同引擎构建、同输入和同种子配对 Normal，再取每档并发的中位数。综合倍率取各档的几何平均。

## 并发 16、24、32 的发布配置

每种方法筛选五套配置，再让最佳挑战者、原配置和同卡 Normal 跑 144 条独立留出输入。三档吞吐等权，达到最快配置的 97% 时，优先保留并发 32 的 P95 首 token 延迟较低的设置。

| 方法 | 发布配置 | 三档综合吞吐 / 原配置 | C32 P95 TTFT（原配置 → 发布） |
|---|---|---:|---:|
| Native MTP | 固定 K=4 | 1.016× | 557 → 547 ms |
| DSpark | Triton，FP8 per-tensor，K=4 | 1.043× | 565 → 550 ms |
| DFlash 2 | MXFP8，K=7，调度预算 4,096 tokens | 1.000× | 553 → 553 ms |
| EAGLE-4 | 验证宽度 6，树深 8 | 1.018× | 606 → 569 ms |

DFlash 2 在早期压测中从 C24 的 307 ms 升至 C32 的 530 ms。其中一轮遇到运行中 CuTeDSL JIT。控制实验把调度前排队压到 0.03 ms 后，重输入仍有明显尾延迟，主要耗时落在首次调度到首 token 之间。

[验证结果与 DFlash 2 延迟分析](report/unified_framework/high-load.md) · [逐轮数据](results/processed/unified-framework/high-load-summary.json)

## 早期 Spec-Bench 七档并发重测

重新测试了四种推测解码方法和各自的同卡 Normal。并发覆盖 1、2、4、8、16、24、32，每档三轮，每轮 64 条请求。同一种子在七档并发使用同一批输入。

DFlash 2 在并发 32 时达到 Normal 的 **1.310×**，P95 首 token 延迟增加约 51%，P95 每 token 延迟降低约 14%。DSpark 在并发 8 时的吞吐倍率最高，为 **1.953×**。[完整结果与图表](report/unified_framework/concurrency.md) · [逐轮数据](results/processed/unified-framework/concurrency-summary.json)

## 其他负载的实测

| 方法 | 实测表现 |
|---|---|
| Normal | 关闭推测解码。EAGLE-4 对照组使用作者的 vLLM 构建，其余方法使用 vLLM 0.34.0。每组实验都使用同期 Normal。 |
| Native MTP | 主模型自带的动态 MTP 在公开 Spec-Bench 达到 1.998×。BurstGPT 回放的吞吐为 1.057×，P95 TPOT 从 10.61 ms 降到 6.60 ms，P95 TTFT 从 63.07 ms 升到 75.91 ms。 |
| DSpark | Triton 草稿端和 K=8 在公开 Spec-Bench 达到 2.282×。随机压力并发 32 的单轮吞吐为 1.035×，P95 TPOT 从 19.45 ms 升到 28.10 ms。 |
| DFlash 2 | MXFP8 草稿在公开 Spec-Bench 达到 2.385×，在后续配对实验中为 2.402×。量化将模型加载显存从 31.31 GiB 降到 29.64 GiB，三套负载综合吞吐为 BF16 的 1.001×。 |
| EAGLE-4 | 相对作者构建的 Normal，Spec-Bench 为 2.322×，合成重复代码与 JSON 为 2.288×。Spec-Bench 并发 16 三轮吞吐倍率为 1.016× 至 2.879×，含一次对照组额外编译。 |

[公开负载与量化](report/unified_framework/results.md) · [EAGLE-4 与 DFlash 2 对照](report/unified_framework/eagle4_dflash.md)

![Spec-Bench、SPEED-Bench、BurstGPT 和随机压力的输出吞吐](report/unified_framework/figures/serving-throughput.png)

## 复现

从仓库根目录运行。预览计划和重生成报告只需 Python 3.11 或更新版本，出图需 Matplotlib 和系统安装的 TeX Gyre Pagella 常规及粗体。每张图输出一份 400 dpi PNG。[字体下载](https://ctan.org/pkg/tex-gyre-pagella)

```bash
python src/unified_framework.py profiles
python src/unified_framework.py benchmark --study high-load --method dspark --print-plan --output replay/dspark-plan
python -m pip install matplotlib==3.11.2
python src/unified_framework.py report --output replay/report-hd
```

B200 上可用同一入口准备输入、启动服务、配对压测、调参和复跑草稿量化。Native MTP 使用主模型内置的头，DSpark 和 DFlash 2 需要各自的草稿权重，EAGLE-4 需要作者的 vLLM 构建。[实验协议与命令](report/unified_framework/README.md) · [EAGLE-4 环境](report/unified_framework/eagle4_dflash_replay.md) · [统一配置](config/unified_framework.json)
