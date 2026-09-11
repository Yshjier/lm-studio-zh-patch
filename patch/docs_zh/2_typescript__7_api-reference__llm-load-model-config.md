
### 参数

```lms_params
- name: gpu
  description: |
    如何把工作分配到你的 GPU 上。更多信息参见 {@link GPUSetting}。
  public: true
  type: GPUSetting
  optional: true

- name: contextLength
  description: |
    上下文长度的 token 数量。它同时包含提示词和回复。一旦超出上下文长度，
    就会用 {@link LLMPredictionConfigBase#contextOverflowPolicy} 中设置的值来决定行为。

    更多信息参见 {@link LLMContextOverflowPolicy}。
  type: number
  optional: true

- name: ropeFrequencyBase
  description: |
    旋转位置嵌入（RoPE）的自定义基频。

    这个高级参数会调整位置信息如何嵌入到模型的表示中。增大该值可以改善高上下文长度下的
    性能，因为它改变了模型处理与位置相关信息的方式。
  type: number
  optional: true

- name: ropeFrequencyScale
  description: |
    RoPE（旋转位置编码）频率的缩放系数。

    该系数通过改变位置信息的编码方式来缩放有效上下文窗口。更高的取值让位置编码更精细，
    从而让模型能够处理更长的上下文，这在把模型扩展到超出其原始训练上下文长度时特别有用。
  type: number
  optional: true

- name: evalBatchSize
  description: |
    在评估过程中单批次一起处理的输入 token 数量。

    增大该值通常能借助并行化提升处理速度和吞吐量，但需要更多内存。寻找最优批次大小
    往往需要在性能收益与可用硬件资源之间取得平衡。
  type: number
  optional: true

- name: flashAttention
  description: |
    启用 Flash Attention 以优化注意力计算。

    Flash Attention 是一种高效实现，它通过优化注意力机制的计算方式，降低内存占用并加速
    生成。在兼容的硬件上，这可以显著提升性能，尤其是对较长的序列。
  type: boolean
  optional: true

- name: keepModelInMemory
  description: |
    启用后，阻止模型被换出系统内存。

    该选项会为模型保留系统内存，即使部分内容已卸载到 GPU，也能确保模型需要被使用时访问更快。
    这尤其能提升交互式应用的性能，但会增加整体内存需求。
  type: boolean
  optional: true

- name: seed
  description: |
    用于模型初始化的随机种子，以确保输出可复现。

    设置特定的种子可以确保模型内部的随机操作（例如采样）在不同运行之间产生相同的结果，
    这对测试与开发场景中的可复现性很重要。
  type: number
  optional: true

- name: useFp16ForKVCache
  description: |
    启用后，以半精度（FP16）格式存储键值缓存。

    该选项通过对注意力缓存使用 16 位浮点数而不是 32 位，显著降低推理期间的内存占用。
    虽然这可能略微降低数值精度，但对大多数应用而言，对输出质量的影响通常很小。
  type: boolean
  optional: true

- name: tryMmap
  description: |
    加载模型时尝试使用内存映射（mmap）文件访问。

    内存映射通过把模型文件直接从磁盘映射到内存来缩短初始加载时间，让操作系统来处理分页。
    这对快速启动尤其有利，但如果模型比可用系统内存更大，会导致频繁磁盘访问，从而降低性能。
  type: boolean
  optional: true

- name: numExperts
  description: |
    为采用混合专家（MoE）架构的模型指定要使用的专家数量。

    MoE 模型包含多个"专家"网络，各自擅长任务的不同方面。该参数控制在推理期间有多少专家参与，
    会影响性能与输出质量。仅适用于采用 MoE 架构设计的模型。
  type: number
  optional: true

- name: llamaKCacheQuantizationType
  description: |
    Llama 模型键缓存的量化类型。

    该选项决定用于存储注意力机制缓存中键部分的精度等级。较低的精度取值（例如 4 位或 8 位量化）
    会显著降低推理期间的内存占用，但可能略微影响输出质量。不同模型的效果不同，有些模型对量化
    更耐受。

    设为 false 可禁用量化并使用完整精度。
  type: LLMLlamaCacheQuantizationType | false
  optional: true

- name: llamaVCacheQuantizationType
  description: |
    Llama 模型值缓存的量化类型。

    与键缓存量化类似，该选项控制注意力机制缓存中值部分所使用的精度。降低精度可以节省内存，
    但可能影响生成质量。该选项需要启用 Flash Attention 才能正常工作。

    不同模型对值缓存量化的反应不同，因此可能需要试验才能为具体用例找到最优设置。
    设为 false 可禁用量化。
  type: LLMLlamaCacheQuantizationType | false
  optional: true
```
