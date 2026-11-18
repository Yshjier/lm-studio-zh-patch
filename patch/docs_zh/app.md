
要获取 LM Studio，请前往[下载页面](/download)并下载适合你操作系统的安装程序。

LM Studio 支持 macOS、Windows 和 Linux。

## 我能用 LM Studio 做什么？

1. 下载并运行本地 LLM，例如 gpt-oss、Llama、Qwen
2. 使用简单灵活的聊天界面
3. 连接 MCP 服务器并在本地模型上使用它们
4. 搜索与下载功能（通过 Hugging Face 🤗）
5. 在本地及局域网中，以类 OpenAI 端点提供本地模型服务
6. 管理你的本地模型、提示和配置

## 系统要求

LM Studio 通常支持 Apple Silicon Mac、x64/ARM64 Windows PC 和 x64 Linux PC。

更详细的信息请查阅[系统要求](app/system-requirements)页面。

## 运行 llama.cpp（GGUF）或 MLX 模型

LM Studio 支持在 Mac、Windows 和 Linux 上使用 [`llama.cpp`](https://github.com/ggerganov/llama.cpp) 运行 LLM。

在 Apple Silicon Mac 上，LM Studio 还支持使用 Apple 的 [`MLX`](https://github.com/ml-explore/mlx) 运行 LLM。

要安装或管理 LM Runtime，请在 Mac 上按 `⌘` `Shift` `R`，或在 Windows/Linux 上按 `Ctrl` `Shift` `R`。

## 作为 MCP 客户端的 LM Studio

你可以在 LM Studio 中安装 MCP 服务器，并将其与你的本地模型一起使用。

更多内容见文档：[使用 MCP 服务器](/docs/app/plugins/mcp)。

如果你正在开发 MCP 服务器，请查看[添加到 LM Studio 按钮](/docs/app/plugins/mcp/deeplink)。

## 在你的电脑上运行 `gpt-oss`、`Llama`、`Qwen`、`Mistral` 或 `DeepSeek R1` 等 LLM

要在你的电脑上运行 LLM，你首先需要下载模型权重。

你完全可以直接在 LM Studio 中完成！请参阅[下载 LLM](app/basics/download-model)。

## 完全离线地在电脑上与文档聊天

你可以将文档附加到聊天消息中，并完全离线地与之交互，也称为"RAG"。

更多关于如何使用此功能的内容，请参阅[与文档聊天](app/basics/rag)指南。

## 不使用 GUI 运行 LM Studio（llmster）

llmster 是 LM Studio 的无头版本，无需桌面应用。它非常适合服务器、CI 环境，或任何你不需要 GUI 的机器。

了解更多：[无头模式](/docs/developer/core/headless)。

## 在你自己的应用和脚本中使用 LM Studio 的 API

LM Studio 提供 REST API，你可以用它从自己的应用和脚本中与本地模型交互。

- [OpenAI 兼容 API](api/openai-api)
- [LM Studio REST API（beta）](api/rest-api)

<br />

## 社区

加入 [Discord](https://discord.gg/aPQfnNkxGC) 上的 LM Studio 社区，提问、分享知识，并从其他用户和 LM Studio 团队获得帮助。
