# 复跑推测解码实验

`src/unified_framework.py` 使用 [统一配置](../../config/unified_framework.json) 和仓库内的 Spec-Bench 题目。各组实验的输入划分各自固定，复跑时按 `--study` 选择。

| `--study` | 配置名 | 负载 |
|---|---|---|
| `framework` | `normal`、`mtp`、`dspark`、`dflash` | Spec-Bench 留出集和随机压力，或 SPEED-Bench 与 BurstGPT |
| `paired` | `eagle4`、`dflash` | Spec-Bench 留出集和合成的重复代码编辑／JSON 输出 |
| `concurrency` | `mtp`、`dspark`、`dflash`、`eagle4` | 固定 Spec-Bench 输入，七档并发 |
| `high-load` | `mtp`、`dspark`、`dflash`、`eagle4` | 独立 Spec-Bench 留出集，并发 16、24、32 |

`eagle4` 默认使用 `paired`。DFlash 2 默认跑 `framework`，复跑 EAGLE-4 对照时指定 `--study paired`。每个方法使用同卡、同一服务构建的 Normal。[EAGLE-4 与 DFlash 2 复跑](eagle4_dflash_replay.md)

## 复跑公开负载

从仓库根目录运行。B200 主机需装好 vLLM 0.34.0 及其压测依赖，并下载 Qwen3.8-27B-FP8。用 `--vllm` 指定环境中的可执行文件。如果 pandas 单独安装，用 `--bench-deps` 传依赖目录。[vLLM 0.34.0](https://github.com/vllm-project/vllm/releases/tag/v0.34.0) · [主模型](https://huggingface.co/Qwen/Qwen3.8-27B-FP8)

```bash
target=/home/model/Qwen3.8-27B-FP8
draft_dir="$HOME/selected-drafts/Qwen3.8-27B-DFlash2"
dspark_dir="$HOME/selected-drafts/redhat-dspark"

hf download incoai/Qwen3.8-27B-DFlash2 config.json model.safetensors \
  --revision 015e795645c74b1a0eeef3b570031fb62e769bc5 --local-dir "$draft_dir"
hf download RedHatAI/Qwen3.8-27B-speculator.dspark config.json model.safetensors \
  --revision 87ca2fdc67f316f6c1f9ebc7ef7bbb0ad299a4ce --local-dir "$dspark_dir"
```

Native MTP 直接使用主模型的 MTP 头。DSpark 原实测使用服务器上的 Red Hat 兼容草稿，公开归档缺少该副本的权重哈希。上面的下载命令固定了 vLLM 模型配方列出的 Red Hat 草稿版本。手头有实测时的权重时，将 `dspark_dir` 指向该副本即可。[vLLM 的 Qwen3.8-27B 配方](https://github.com/vllm-project/recipes/blob/main/models/Qwen/Qwen3.8-27B.yaml) · [固定的 Red Hat 草稿](https://huggingface.co/RedHatAI/Qwen3.8-27B-speculator.dspark/tree/87ca2fdc67f316f6c1f9ebc7ef7bbb0ad299a4ce)

```bash
python src/unified_framework.py benchmark --method mtp --gpu 7 --model "$target" --output replay/mtp
python src/unified_framework.py benchmark --method dspark --gpu 7 --model "$target" \
  --draft-model "$dspark_dir" --output replay/dspark
python src/unified_framework.py benchmark --method dflash --gpu 7 --model "$target" \
  --draft-model "$draft_dir" --output replay/dflash
python src/unified_framework.py report --results replay --output replay/spec-report
```

每次 `benchmark` 都会自动启停服务并保存逐轮 JSON、GPU 信息、输入哈希和日志。中断后可用同一命令继续，已完成的配置会直接复用。想手动启动单个配置时用 `serve --method`，加 `--print-command` 可打印 vLLM 参数。用 `benchmark --print-plan` 可在没有 GPU 的机器上准备输入并查看实际运行矩阵。

### SPEED-Bench 和 BurstGPT

下载固定版本的 Parquet 和 CSV，再生成输入清单。SPEED-Bench 去掉了与 Spec-Bench 重复的提示。BurstGPT 保留请求长度和相对到达间隔。[SPEED-Bench Qualitative Parquet](https://huggingface.co/datasets/nvidia/SPEED-Bench/resolve/fa4e669bee2a4393c56aa8ed05a7c667897f9590/qualitative/test-00000-of-00001.parquet) · [BurstGPT v2.0 无失败轨迹 3](https://github.com/HPMLL/BurstGPT/releases/download/v2.0/BurstGPT_without_fails_3.csv)

```bash
python -m pip install pyarrow
python src/unified_framework.py prepare --study external --speed-parquet speed.parquet \
  --burst-csv BurstGPT_without_fails_3.csv --output replay/serving-inputs
python src/unified_framework.py benchmark --method dflash --gpu 7 --model "$target" \
  --draft-model "$draft_dir" --workloads replay/serving-inputs --output replay/external/dflash
```

对 `mtp` 和 `dspark` 分别运行外部负载压测，输出到 `replay/external/mtp` 和 `replay/external/dspark`。加入 `--external-results` 的报告会检查两组复跑的模型、服务版本、设备信息和配置。

```bash
python -m pip install matplotlib==3.11.2
python src/unified_framework.py report --results replay --external-results replay/external --output replay/full-report
```

### 调参

复制发布配置为 `tuning-plan.json`。在目标方法下给 `round1` 填候选的 `id` 和完整 vLLM `spec`，给 `round2` 填 `id` 和 `override`。第二轮在第一轮最快的配置上应用覆盖项，值为 `null` 时删除该选项。随后用同一份配置和同一个结果目录运行 `tune` 与 `benchmark`，后者会读取 `selection.json`。

```bash
python src/unified_framework.py --config tuning-plan.json tune --method dflash --gpu 7 \
  --model "$target" --draft-model "$draft_dir" --output replay/tuned/dflash
python src/unified_framework.py --config tuning-plan.json benchmark --method dflash --gpu 7 \
  --model "$target" --draft-model "$draft_dir" --output replay/tuned/dflash
```

### 图表格式

从仓库根目录执行 `python src/unified_framework.py report --output replay/report-hd`，可从已发布 JSON 重生成报告和 400 dpi PNG。吞吐柱为配对倍率的中位数，须线是不同种子观测到的最小值和最大值。随机压力每档测一轮。

分组柱形参考 ICML 2024 的 EAGLE 图 1。渲染前在系统安装 TeX Gyre Pagella 的常规及粗体 OpenType 字体。[EAGLE 图 1](https://proceedings.mlr.press/v235/li24bt.html) · [TeX Gyre Pagella](https://ctan.org/pkg/tex-gyre-pagella) · [NeurIPS 实验统计说明](https://neurips.cc/public/guides/PaperChecklist)

## 并发重测

并发档为 1、2、4、8、16、24、32。每个种子固定 64 条 Spec-Bench 输入，在所有并发档复用。种子之间的题目互不重叠，档位在种子内打乱。各方法使用同卡、同服务构建的 Normal。EAGLE-4 仍用作者的构建、同构建 Normal 和 vLLM 0.34.0 客户端。

```bash
export OMP_NUM_THREADS=4 MKL_NUM_THREADS=4 TOKENIZERS_PARALLELISM=false
python src/unified_framework.py benchmark --study concurrency --method mtp \
  --gpu 0 --model "$target" --output replay/concurrency/mtp
python src/unified_framework.py benchmark --study concurrency --method dspark \
  --gpu 1 --port 24821 --model "$target" --draft-model "$dspark_dir" --output replay/concurrency/dspark
python src/unified_framework.py benchmark --study concurrency --method dflash \
  --gpu 2 --port 24822 --model "$target" --draft-model "$draft_dir" --output replay/concurrency/dflash
```

EAGLE-4 按专用环境的说明提供 `--vllm`、`--client-vllm`、`--draft-model` 和 `--calibration`，将 `--study` 设为 `concurrency`，输出到 `replay/concurrency/eagle4`。多卡同时复跑时用不同端口。[EAGLE-4 环境](eagle4_dflash_replay.md)

```bash
python src/unified_framework.py report --study concurrency --results replay/concurrency \
  --output replay/concurrency-report
```

每档吞吐倍率先按种子配对，再取中位数。绝对值取各组独立中位数。并发档指压测客户端同时允许的在途请求数。

## 高并发发布配置

配置文件每种方法提供一套高并发调参后发布的设置。用 `--study high-load` 复跑并发 16、24、32。每轮 48 条 Spec-Bench 请求，同种子在三档使用相同输入。这 144 条留出输入来自七档并发重测未用的部分。四种方法的引擎、权重及线程设置沿用上述并发复跑说明。

```bash
python src/unified_framework.py benchmark --study high-load --method dflash \
  --gpu 2 --model "$target" --draft-model "$draft_dir" --output replay/high-load/dflash
python src/unified_framework.py report --study high-load --results replay/high-load \
  --output replay/high-load-report
```

把另外三个方法的结果放到同一父目录下的 `mtp`、`dspark` 和 `eagle4`。EAGLE-4 使用专用构建、权重和成本表，Normal 由框架按同一构建启动。公开负载和七档并发报告记录了各自实测时的配置。[高并发结果与 DFlash 2 延迟分析](high-load.md)

## DFlash 2 草稿量化

在同一张 B200 上从原始 BF16 权重加载各量化格式，目标模型、草稿长度和注意力后端一致。先用 Spec-Bench 调参子集筛选，再让最快的可用量化、BF16 和 Normal 一起跑 Spec-Bench 留出集、SPEED-Bench 和 BurstGPT。量化只在三套负载的等权综合吞吐超过 BF16、各套负载的降幅都在 3% 以内时成为发布设置。[量化和显存实测](results.md#dflash-2-草稿量化复测) · [vLLM 在线量化](https://docs.vllm.ai/en/v0.34.0/features/quantization/online/)

```bash
python src/unified_framework.py quantization-study --gpu 7 --port 24787 \
  --draft-model "$draft_dir" --workloads replay/serving-inputs --output replay/draft-study \
  --quantizations fp8_per_tensor fp8_per_block mxfp8 nvfp4_w4a16
python src/unified_framework.py report \
  --results results/processed/unified-framework/summary.json \
  --draft-study replay/draft-study --output replay/quantization-report
```

本机 vLLM 0.34.0 拒绝将 `nvfp4_w4a16` 用作草稿在线量化参数，服务未启动。三种 8 位候选完成了筛选。

量化试验选中 MXFP8，草稿长度为 K=7。三套负载的综合吞吐是 BF16 的 1.001×，模型加载显存从 31.31 GiB 降到 29.64 GiB。SPEED-Bench 并发 16 的 P95 首 token 延迟中位数从 188.47 ms 升到 204.37 ms，其中一轮 MXFP8 达到 1,008.14 ms。该轮计入中位数和范围。[逐轮统计](../../results/processed/unified-framework/summary.json)

DFlash 2 草稿端的服务日志记录了 `Using FlashAttention version 4`。安装的 vLLM 0.34.0 构建为 `62d4bc3c7`，包内 FA4 的接口和两份前向内核源码经哈希核对，与 vLLM 固定的 FlashAttention fork 提交 `d8dca8f0` 一致。2026-11-25 时，上游独立发行已到 `flash-attn-4 4.0.0b41`。本组实测使用 vLLM 自带的构建。[vLLM 构建配置](https://github.com/vllm-project/vllm/blob/v0.34.0/cmake/external_projects/vllm_flash_attn.cmake) · [固定提交](https://github.com/vllm-project/flash-attention/commit/d8dca8f06c7458a0c0e79dd9400c0446a4e77b9c) · [上游发行](https://pypi.org/project/flash-attn-4/4.0.0b41/)

## 早期调参结果

- DSpark 在草稿长度 K=8 和 FP8-per-tensor 量化下，将草稿端从自动选择改为 Triton，恢复了完整 CUDA Graph 捕获。留出集在并发 1、4、16 下分别达到原配置的 **3.60×、2.87×、2.26×**，综合 **2.86×**。
- MTP 固定 K=5 的综合留出集吞吐为动态 K=6/5 的 **0.986×**，因此保留动态配置。
- DFlash 2 保留 K=7。在最初的 BF16 试验中，FlashAttention 4 可以完整捕获 CUDA Graph。草稿端切到 FlashInfer 后 CUDA Graph 关闭，调参池并发 16 的吞吐从 1,794 降到 740 token/s。[早期 DFlash 2 结果](https://github.com/Zheng-Hanyu/Generative-Models-Final-Project/blob/63685a5e11358a45c9647b24e24a84ea43081fba/report/unified_framework/results.md)

早期 DFlash 2 BF16 实验的并发上限为 16。相对同期同卡 Normal，Spec-Bench、SPEED-Bench 和 BurstGPT 三轮配对吞吐倍率的中位数分别为 1.805×、1.804× 和 1.059×。

BurstGPT 回放中，DFlash 2 相对同期 Normal 的 P95 每 token 延迟从 10.85 ms 降至 8.91 ms，P95 首 token 延迟从 69.23 ms 升至 109.58 ms。

## 实验协议

- 每种方法的原配置、入选配置和 Normal 在同一张 B200 上测量。目标模型为 Qwen3.8-27B-FP8，使用 Triton Attention 和 TP=1。所有请求采用 greedy 生成，关闭 vLLM 前缀缓存。
- DSpark 使用服务器上的 Red Hat 兼容草稿权重。其原配置让 vLLM 自选草稿端注意力后端，后端对照显式指定草稿端 Triton。主模型在两种设置下都使用 Triton。
- DFlash 2 使用 Inco AI 针对 Qwen3.8-27B 发布的五层 BF16 草稿权重。vLLM 的 `dflash` 方法在加载时按发布配置量化权重。源权重文件 SHA-256 为 `67fc76d68dc5a9415511a4f394ef744d67510cd20e93b37cc2cc7d28e4bab65c`。[固定版本的权重和配置](https://huggingface.co/incoai/Qwen3.8-27B-DFlash2/tree/015e795645c74b1a0eeef3b570031fb62e769bc5) · [DFlash 2 技术说明](https://inco.ai/blog/dflash2/) · [DFlash 论文](https://arxiv.org/abs/2602.06036) · [vLLM 实现](https://github.com/vllm-project/vllm/pull/52816)
- 从仓库的 480 条 Spec-Bench 题目按类别抽出 144 条作为调参池，余下 336 条进入留出池。调参在并发 1、4、16 各跑 18 条。留出池按三组种子和三个并发档拆成九组互不重叠的子集，每组实测 30 条。对照配置使用相同的题目、采样顺序和输出上限 128，每次以四个独立提示预热。[Spec-Bench 数据版本](https://github.com/hemingkx/Spec-Bench/blob/66230f10cb0a02aced5ef3ce1e85163c16160454/data/spec_bench/question.jsonl) · [Xia 等，ACL Findings 2024](https://arxiv.org/abs/2401.07851)
- 第一轮筛选草稿长度。第二轮比较 MTP 动态草稿长度、DSpark 的草稿端注意力后端、块长、量化和自适应验证，以及 DFlash 2 的草稿端注意力后端和草稿长度。按三个并发档的输出 TPS 几何平均在调参池选定一个配置，再和同卡 Normal、该方法原配置配对复测。[vLLM 动态草稿长度](https://docs.vllm.ai/en/v0.34.0/features/speculative_decoding/dynamic_speculative_decoding/) · [vLLM 自适应验证](https://docs.vllm.ai/en/v0.34.0/features/speculative_decoding/adaptive_verification/)
- 随机压力测试在并发 16 和 32 各跑 64 条，分别使用种子 817 和 818，输入 1,024 tokens，输出 128 tokens，忽略 EOS。每个单元一轮。
- SPEED-Bench 使用 Qualitative 版本 `fa4e669`。先排除占位符、超过 3,500 字节的提示、重复项及与 Spec-Bench 重复的首轮提示，再得到覆盖代码、写作和多语言的 144 条独立输入。并发 1 每轮 16 条，并发 16 每轮 32 条，三轮互不重叠。强制每条生成 128 tokens，压测采用饱和到达。[SPEED-Bench 数据卡](https://huggingface.co/datasets/nvidia/SPEED-Bench) · [Abramovich 等，ICML 2026](https://proceedings.mlr.press/v306/abramovich26a.html)
- BurstGPT 使用 v2.0 发布包中第三份无失败轨迹。输入长度为 8 至 3,072 tokens，输出为 16 至 512 tokens。三轮各取 64 个连续的合格请求，保留相对到达间隔，每段缩放到 8 秒，客户端并发上限为 16。轨迹记录长度和时间，vLLM 以固定的 Python 哈希种子补全输入 token ID，并按轨迹设定输出长度。[BurstGPT v2.0](https://github.com/HPMLL/BurstGPT/releases/tag/v2.0) · [KDD 2025 论文目录](https://kdd.org/kdd2025/datasets-and-benchmarks-track-papers-2/) · [论文 DOI](https://doi.org/10.1145/3711896.3737413) · [vLLM Benchmark CLI](https://docs.vllm.ai/en/v0.34.0/benchmarking/cli/)
- 每个速度比配对同卡、同种子和同并发的运行。每套公开负载有三轮。TTFT 是首 token 耗时，TPOT 是首 token 之后的平均每 token 耗时。草稿接受率是 vLLM 记录的已接受 token 占全部草稿 token 的比例。

[统一配置](../../config/unified_framework.json) · [CLI](../../src/unified_framework.py) · [结构化结果](../../results/processed/unified-framework/summary.json)
