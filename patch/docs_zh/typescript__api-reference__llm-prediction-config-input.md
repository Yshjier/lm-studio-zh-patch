
### 字段

```lms_params
- name: "maxTokens"
  type: "number | false"
  optional: true
  description: "最多预测的 token 数量。如果设为 false，模型会想预测多少就预测多少。\n\n当预测因该限制而停止时，预测统计中的 `stopReason` 会被设为 `maxPredictedTokensReached`。"

- name: "temperature"
  type: "number"
  optional: true
  description: "预测模型的 temperature 参数。取值越高，预测结果越随机；取值越低，预测结果越确定。数值应在 0 到 1 之间。"

- name: "stopStrings"
  type: "Array<string>"
  optional: true
  description: "一个字符串数组。如果模型生成了其中任一字符串，预测就会停止。\n\n当预测因该限制而停止时，预测统计中的 `stopReason` 会被设为 `stopStringFound`。"

- name: "toolCallStopStrings"
  type: "Array<string>"
  optional: true
  description: "一个字符串数组。如果模型生成了其中任一字符串，预测会以 `stopReason` `toolCalls` 停止。"

- name: "contextOverflowPolicy"
  type: "LLMContextOverflowPolicy"
  optional: true
  description: "当生成的 token 长度超出上下文窗口大小时的行为。允许的取值有：\n\n- `stopAtLimit`：当生成的 token 长度超出上下文窗口大小时停止预测。如果生成因该限制而停止，预测统计中的 `stopReason` 会被设为 `contextLengthReached`\n- `truncateMiddle`：保留系统提示词和第一条用户消息，截断中间部分。\n- `rollingWindow`：维护一个滚动窗口，截断较早的消息。"

- name: "structured"
  type: "ZodType<TStructuredOutputType> | LLMStructuredPredictionSetting"
  optional: true
  description: "把模型配置为输出遵循 Zod 定义的特定 schema 的结构化 JSON 数据。\n\n当你提供 Zod schema 时，模型会被要求生成符合该 schema 的 JSON，而不是自由形式的文本。\n\n这在从模型回复中提取特定数据点，或你需要输出能被应用直接使用的格式时特别有用。"

- name: "topKSampling"
  type: "number"
  optional: true
  description: "通过只考虑 K 个最可能的下一个 token 来控制采样多样性。\n\n例如，如果设为 40，那么在选择下一个 token 时只会考虑概率最高的 40 个 token。取值较低（例如 20）会让输出更聚焦、更保守，取值较高（例如 100）则允许更有创意、更多样的输出。\n\n典型取值范围是 20 到 100。"

- name: "repeatPenalty"
  type: "number | false"
  optional: true
  description: "对重复 token 施加惩罚，防止模型陷入重复的模式。\n\n取值为 1.0 表示不惩罚。大于 1.0 的取值会加大惩罚。例如 1.2 会把此前已用过的 token 的概率降低 20%。这对防止模型重复短语或陷入循环特别有用。\n\n设为 false 可完全禁用惩罚。"

- name: "minPSampling"
  type: "number | false"
  optional: true
  description: "设置一个 token 被纳入生成考虑所需达到的最低概率阈值。\n\n例如，如果设为 0.05，那么概率低于 5% 的 token 都会被排除在外。这有助于过滤掉不太可能或不相关的 token，可能提升输出质量。\n\n数值应在 0 到 1 之间。设为 false 可禁用该过滤。"

- name: "topPSampling"
  type: "number | false"
  optional: true
  description: "实现核采样（nucleus sampling）：只考虑累计概率达到指定阈值的 token。\n\n例如，如果设为 0.9，模型只会考虑那些累计起来占概率总量 90% 的最可能 token。它通过根据概率分布动态调整考虑的 token 数量，在多样性与质量之间取得平衡。\n\n数值应在 0 到 1 之间。设为 false 可禁用核采样。"

- name: "xtcProbability"
  type: "number | false"
  optional: true
  description: "控制生成过程中应用 XTC（Exclude Top Choices，排除最优选项）采样技术的频率。\n\nXTC 采样通过偶尔过滤掉常见 token 来提升创意、减少陈词滥调。例如，如果设为 0.3，那么生成每个 token 时有 30% 的概率会应用 XTC 采样。\n\n数值应在 0 到 1 之间。设为 false 可完全禁用 XTC。"

- name: "xtcThreshold"
  type: "number | false"
  optional: true
  description: "定义 XTC（Exclude Top Choices，排除最优选项）采样技术的下限概率阈值。\n\n当 XTC 采样被激活时（依据 xtcProbability 判断），算法会找出概率介于该阈值与 0.5 之间的 token，然后删除所有这些 token，只保留概率最低的那一个。这有助于让生成结果更多样、更出人意料。\n\n仅在 xtcProbability 启用时生效。"

- name: "cpuThreads"
  type: "number"
  optional: true
  description: "指定分配给模型推理的 CPU 线程数。\n\n在多数系统上，取值更高能提升性能，但可能会与其他进程争抢资源。例如在 8 核系统上，取值 4-6 可能在提供良好性能的同时为其他任务留出资源。\n\n如果未指定，系统会根据可用硬件使用默认值。"

- name: "draftModel"
  type: "string"
  optional: true
  description: "用于推测解码的草稿模型。推测解码是一种能大幅提升生成速度的技术（对较大的模型最多可提升 3 倍），做法是把主模型与一个更小的草稿模型配对。\n\n更多信息见此处：https://lmstudio.ai/docs/advanced/speculative-decoding\n\n你不需要自己加载草稿模型。在这里指定它的模型标识符就足够了。"
```
