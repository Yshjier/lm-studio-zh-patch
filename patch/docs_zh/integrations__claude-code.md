
Claude Code 可以通过 Anthropic 兼容的 `POST /v1/messages` 端点与 LM Studio 通信。
参见：[Anthropic 兼容的 Messages 端点](/docs/developer/anthropic-compat/messages)。

<img src="/assets/marketing/docs/claude-code.webp" style="width: 100%;" data-caption="Claude Code 配置为通过 Anthropic 兼容 API 使用 LM Studio" />

```lms_protip
有一台强力 LLM 主机？使用 [LM Link](/docs/integrations/lmlink) 就能在你的笔记本上运行 Claude Code，而模型在你的主机上运行。
```

### 1) 启动 LM Studio 的本地服务器

确保 LM Studio 正作为服务器运行（默认端口 `1234`）。

你可以在应用内启动它，也可以在终端中用 `lms` 启动：

```bash
lms server start --port 1234
```

### 2) 配置 Claude Code

设置以下环境变量，使 `claude` CLI 指向你本地的 LM Studio：

```bash
export ANTHROPIC_BASE_URL=http://localhost:1234
export ANTHROPIC_AUTH_TOKEN=lmstudio
```

说明：

- 如果启用了"需要身份验证"，请把 `ANTHROPIC_AUTH_TOKEN` 设为你的 LM Studio API 令牌。了解更多，参见：[身份验证](/docs/developer/core/authentication)。

### 3) 让 Claude Code 针对本地模型运行

```bash
claude --model openai/gpt-oss-20b
```

```lms_protip
使用上下文长度超过约 25k 的模型（以及服务器/模型设置）。像 Claude Code 这样的工具会消耗大量上下文。
```

### 4) 如果启用了"需要身份验证"，请使用你的 LM Studio API 令牌

如果你在 LM Studio 中开启了"需要身份验证"，请创建一个 API 令牌并设置：

```bash
export LM_API_TOKEN=<LMSTUDIO_TOKEN>
export ANTHROPIC_AUTH_TOKEN=$LM_API_TOKEN
```

当"需要身份验证"启用时，LM Studio 同时接受 `x-api-key` 和 `Authorization: Bearer <token>`。

如果遇到问题，欢迎加入我们的 [Discord](https://discord.gg/lmstudio)
