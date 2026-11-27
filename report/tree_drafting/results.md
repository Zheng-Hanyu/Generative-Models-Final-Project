# B200 上的树形投机解码

固定 Qwen3.8-27B-FP8 和 drafter 权重，在单张 B200 上做 batch size 1 的 greedy 解码。4 条 SpecBench 提示，每条生成 64 个 token，重复两次。98 个配置共 784 条请求均与独立 AR 逐 token 一致。

| Drafter | 原生 Chain | Fixed Tree 最快 | Best-first 最快 | Best-first / Chain |
|---|---:|---:|---:|---:|
| DSpark | 50.68 | 70.54 | 77.86 | 1.54× |
| DFlash2 | 63.76 | 83.71 | 105.61 | 1.66× |

单位为端到端 tokens/s，含 prefill。节点预算包含 anchor。预算为 8、16、24、32 时，DFlash2 Best-first 的最高吞吐依次为 **81.03、92.64、84.10、105.61**。每个预算在同一批提示上选取分支数和深度的最快组合。固定这两个参数与节点预算后，Best-first 在 48 对对照中有 46 对吞吐更高。

**树搜索与验证。** DSpark 用 Markov head，DFlash2 用 Candidate Selector，为每个父节点计算子节点分数。Fixed 按层扩展，Best-first 按累计条件对数概率扩展。两者复用同一 Triton 建树核。目标模型通过原生 FlashAttention 读取各节点的祖先 KV，Gated DeltaNet 沿父索引更新分支状态，最终只提交被选路径。GPU 建树通过 768 次参考搜索对照。独立离线回放与在线运行有 158/784 条请求的提交轮次边界不同，最终 token 相同。[SpecPilot 参考实现](https://github.com/StargazerX0/SpecPilot/tree/1058dc29481150e66ae11b8e8cf55ed60caf254a)

**验证是主要耗时。** 在 32 节点、分支 8、深度 16 的预热对照中，DFlash2 每轮 draft、建树、验证分别为 4.57、0.053、37.06 ms。对目标模型的 64 层 MLP 使用 CUDA Graph，并融合 KV 收集后，验证降至 **29.80 ms**，端到端吞吐从 **104.05 升至 123.86 tokens/s**；相同设置下 DSpark 从 **79.24 升至 94.07**。Nsight 的独立采集中，GPU kernel 活跃时间占比从 30.2% 升至 34.0%。这些结果来自短提示、小样本，长上下文需另测。

[核心实现](../../tree_study/) 适配 vLLM 0.34.0 的同步 V2 worker、TP=1。集成入口在 tree_study.hooks.Study。构造引擎前安装一次 hooks，每次请求前选择策略、预算、分支数和深度；树实验为 32 节点预留 31 个草稿位置。
