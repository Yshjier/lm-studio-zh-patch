
## 安装 `lms`

`lms` 随 LM Studio 一同提供，所以如果你已安装 LM Studio，就无需任何额外的安装步骤。

只需打开一个终端窗口，然后运行 `lms`：

```shell
lms --help
```

## 开源

`lms` 采用 **MIT 许可证**，并在 GitHub 上的这个仓库中开发：https://github.com/lmstudio-ai/lms

## 命令快速链接

| 命令                       | 语法             | 文档                                  |
| ----------------------------- | ------------------ | ------------------------------------- |
| 在终端中聊天          | `lms chat`         | [指南](/docs/cli/local-models/chat)  |
| 下载模型               | `lms get`          | [指南](/docs/cli/local-models/get)   |
| 列出你的模型              | `lms ls`           | [指南](/docs/cli/local-models/ls)    |
| 查看已加载到内存的模型 | `lms ps`           | [指南](/docs/cli/local-models/ps)    |
| 控制服务器            | `lms server start` | [指南](/docs/cli/serve/server-start) |
| 管理推理运行时  | `lms runtime`      | [指南](/docs/cli/runtime)            |
| 管理无头守护进程    | `lms daemon`       | [指南](/docs/cli/daemon/daemon-up)   |
| 管理 LM Link                | `lms link`         | [指南](/docs/cli/link/link-enable)   |

### 验证安装

```lms_info
👉 你必须_至少运行一次_ LM Studio 才能使用 `lms`。
```

打开一个终端窗口并运行 `lms`。

```lms_terminal
$ lms

lms is LM Studio's CLI utility for your models, server, and inference runtime. (v0.0.47)

Usage: lms [options] [command]

Local models
   chat               Start an interactive chat with a model
   get                Search and download models
   load               Load a model
   unload             Unload a model
   ls                 List the models available on disk
   ps                 List the models currently loaded in memory
   import             Import a model file into LM Studio

Serve
   server             Commands for managing the local server
   log                Log incoming and outgoing messages

Runtime
   runtime            Manage and update the inference runtime

Develop & Publish (Beta)
   clone              Clone an artifact from LM Studio Hub to a local folder
   push               Uploads the artifact in the current folder to LM Studio Hub
   dev                Starts a plugin dev server in the current folder
   login              Authenticate with LM Studio

Learn more:           https://lmstudio.ai/docs/developer
Join our Discord:     https://discord.gg/lmstudio
```

## 用 `lms` 自动化并调试你的工作流

### 启动和停止本地服务器

```bash
lms server start
lms server stop
```

了解更多关于 [`lms server`](/docs/cli/serve/server-start) 的内容。

### 列出机器上的本地模型

```bash
lms ls
```

了解更多关于 [`lms ls`](/docs/cli/local-models/ls) 的内容。

这会反映当前的 LM Studio 模型目录，你可以在应用的 **📂 我的模型** 选项卡中设置它。

### 列出当前已加载的模型

```bash
lms ps
```

了解更多关于 [`lms ps`](/docs/cli/local-models/ps) 的内容。

### 加载模型（带选项）

```bash
lms load [--gpu=max|auto|0.0-1.0] [--context-length=1-N]
```

`--gpu=1.0` 表示"尝试将 100% 的计算卸载到 GPU"。

- 可选地，为你的本地 LLM 指定一个标识符：

```bash
lms load openai/gpt-oss-20b --identifier="my-model-name"
```

如果你想保持模型标识符一致，这会很有用。

### 卸载模型

```
lms unload [--all]
```

了解更多关于 [`lms load and unload`](/docs/cli/local-models/load) 的内容。
