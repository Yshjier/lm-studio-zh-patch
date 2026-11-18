生成器（Generator）用于替代本地 LLM。它充当词元来源。当使用带生成器的插件时，LM Studio 将不再使用本地模型生成文本，而是改用该生成器。

生成器适用于为外部模型实现适配器，例如接入远程 LM Studio 实例或其他在线模型。

如果插件包含生成器，它将不再出现在插件列表中，而是出现在模型下拉列表中并作为模型使用。如果你的插件包含[工具提供方](/docs/typescript/plugins/tools-providers)或[提示词预处理器](/docs/typescript/plugins/prompt-preprocessors)，在选择你的生成器时仍会被使用。

## 示例

以下是一些使用生成器的插件：

* [lmstudio/remote-lmstudio](/lmstudio/remote-lmstudio)

  支持使用远程 LM Studio 实例生成文本的基础能力。

* [lmstudio/openai-compat-endpoint](/lmstudio/openai-compat-endpoint)

  在 LM Studio 中使用任意 OpenAI 兼容 API。
