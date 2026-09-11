
生成器可以替代本地 LLM。它们的作用就像一个 token 来源。当使用了带生成器的插件时，LM Studio 将不再使用本地模型生成文本，而是改用该生成器。

生成器适合用来实现面向外部模型的适配器，例如使用远程 LM Studio 实例或其他在线模型。

如果某个插件包含生成器，它就不再出现在插件列表中，而是出现在模型下拉列表中并作为一个模型使用。如果你的插件还包含[工具提供者](./tools-providers.md)或[提示词预处理器](./prompt-preprocessors.md)，它们会在你的生成器被选中时生效。

## 示例

以下是一些使用生成器的插件：

- [lmstudio/remote-lmstudio](https://lmstudio.ai/lmstudio/remote-lmstudio)

  使用远程 LM Studio 实例生成文本的基础支持。

- [lmstudio/openai-compat-endpoint](https://lmstudio.ai/lmstudio/openai-compat-endpoint)

  在 LM Studio 中使用任何 OpenAI 兼容的 API。
