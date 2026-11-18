
要启用工具调用会稍微复杂一些。要查看一个适配 OpenAI API 的完整示例，参见 [openai-compat-endpoint 插件](https://lmstudio.ai/lmstudio/openai-compat-endpoint)。

你可以用 `ctl.getToolDefinitions()` 读取可用工具的定义。例如，如果你在做在线模型适配器，就需要把工具定义传给模型。

一旦模型开始发起工具调用，你需要把这些调用告知 LM Studio。

用 `ctl.toolCallGenerationStarted` 上报一次工具调用生成的开始（即模型开始生成一个工具调用）。

用 `ctl.toolCallGenerationEnded` 上报一次工具调用生成成功，或用 `ctl.toolCallGenerationFailed` 上报一次工具调用生成失败。

你还可以选择用 `ctl.toolCallGenerationNameReceived` 在工具名称可用时立即上报它。也可以用 `ctl.toolCallGenerationArgumentFragmentGenerated` 在工具调用参数生成过程中上报其片段。这两个方法有助于提供更好的用户体验，但并非严格必需。

总的来说，你的生成器必须按以下顺序调用这些 ctl 方法：

1. 调用 0 - N 次 `ctl.fragmentGenerated`，上报生成的非工具调用文本片段。
2. 对每个工具调用：
   1. 调用 `ctl.toolCallGenerationStarted`，表示一次工具调用生成的开始。
   2. （可选）调用 `ctl.toolCallGenerationNameReceived` 上报被调用工具的名称。
   3. （可选）调用任意次数 `ctl.toolCallGenerationArgumentFragmentGenerated` 上报工具调用参数生成的片段。
   4. 调用 `ctl.toolCallGenerationEnded` 上报该工具调用生成成功，或调用 `ctl.toolCallGenerationFailed` 上报其生成失败。
   5. 如果模型在工具调用之间或之后还生成了更多文本，则调用 0 - N 次 `ctl.fragmentGenerated` 上报生成的非工具调用文本片段。（正常情况下不应发生，但某些较小的模型在技术上确实可能这样。**关键点：这与模型收到工具结果后继续对话不是一回事。这只是模型在发出工具请求后拒绝停止输出 —— 此时工具结果还没有提供给模型。** 当发生多轮预测时，也就是模型真正收到该工具调用时，你的生成器函数会带着更新后的对话状态被再次调用。）

有些 API 格式可能会把工具名称与工具调用生成的起始一起上报，这种情况下你可以在 `ctl.toolCallGenerationStarted` 之后立即调用 `ctl.toolCallGenerationNameReceived`。

有些 API 格式可能没有增量的工具调用更新（即整个工具调用请求一次性给出），这种情况下你只需先调用 `ctl.toolCallGenerationStarted`，然后立即调用 `ctl.toolCallGenerationEnded`。
