## LM Studio 应用、llmster 与 lms

LM Studio 应用、llmster 和 `lms` 是 LM Studio 提供的三种不同工具，旨在让本地 AI 的使用变得简单易用。

## LM Studio（桌面应用）

LM Studio 应用是一个易用的图形界面，包含 LM Studio 的全部能力。

### 主要能力：

* 从 Hugging Face 搜索并下载模型
* 通过内置聊天界面与模型对话
* 上传并与文档聊天（RAG）
* 配置模型设置、提示词模板和预设
* 通过原生 REST API 或 OpenAI/Anthropic 兼容端点运行本地服务器
* 连接 MCP 服务器，并与本地模型配合使用

如果你刚接触本地运行模型，或偏好图形界面，桌面应用是最容易的起点。

## llmster（无头守护进程）

llmster 是 LM Studio 的无头守护进程——一个无需图形界面即可运行的独立后台服务。这意味着无需下载 LM Studio 应用，即可通过终端使用 llmster。

当你需要在以下场景运行 LM Studio 时，llmster 会很有用：

* Linux 服务器或云实例上
* 无屏幕或显示设备的 GPU 主机上
* CI/CD 流水线中
* 作为开机自启的后台服务
  以及更多场景！

由于 llmster 独立于桌面应用运行，在不便安装或启动图形应用的环境中，你也可以获得 LM Studio 完整的模型服务能力。

更多内容及安装 llmster 见[此处](/docs/developer/core/headless)。

## lms（命令行工具）

`lms` 是 LM Studio 的 CLI（命令行界面）。它让你可以同时与 LM Studio 桌面应用和 llmster 交互，并直接在终端中管理模型。

下载应用或 llmster 后会自动包含 `lms`。

**常用命令：**

```bash
lms get <model>        # Download a model
lms load <model>       # Load a model into memory
lms ls                 # List models available on disk
lms server start       # Start the local HTTP server
lms chat               # Start an interactive chat session in the terminal
lms log stream         # Stream incoming and outgoing request logs
```

如果运行 `lms` 命令时 LM Studio 尚未运行，它会自动启动。

**下载并提供模型的示例命令：**

```bash
lms get openai/gpt-oss-20b
lms load openai/gpt-oss-20b
lms server start
```

服务器启动后，会监听 <http://localhost:1234>。把任意 SDK 或兼容工具指向我们的 OpenAI 或 Anthropic 兼容端点，即可使用你的 LM Studio 模型。

简而言之，`lms` 是用于同时对接桌面应用或 llmster 的命令行工具。
