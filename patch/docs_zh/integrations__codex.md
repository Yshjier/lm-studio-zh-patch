
Codex 可以通过 OpenAI 兼容的 `POST /v1/responses` 端点与 LM Studio 通信。
参见：[OpenAI 兼容的 Responses 端点](/docs/developer/openai-compat/responses)。

<img src="/assets/marketing/docs/codex.webp" style="width: 100%;" data-caption="Codex 配置为通过 OpenAI 兼容 API 使用 LM Studio" />

```lms_protip
有一台强力 LLM 主机？使用 [LM Link](/docs/integrations/lmlink) 就能在你的笔记本上运行 Codex，而模型在你的主机上运行。
```

### 1) 启动 LM Studio 的本地服务器

确保 LM Studio 正作为服务器运行（默认端口 `1234`）。

你可以在应用内启动它，也可以在终端中用 `lms` 启动：

```bash
lms server start --port 1234
```

### 2) 让 Codex 针对本地模型运行

像平常一样运行 Codex，但加上 `--oss` 标志让它指向 LM Studio。

示例：

```bash
codex --oss
```

默认情况下，Codex 会下载并使用 [openai/gpt-oss-20b](https://lmstudio.ai/models/openai/gpt-oss-20b)。

```lms_protip
使用上下文长度超过约 25k 的模型（以及服务器/模型设置）。像 Codex 这样的工具会消耗大量上下文。
```

你也可以使用你在 LM Studio 中已有的任何其他模型。例如：

```bash
codex --oss -m ibm/granite-4-micro
```

如果遇到问题，欢迎加入我们的 [Discord](https://discord.gg/lmstudio)
