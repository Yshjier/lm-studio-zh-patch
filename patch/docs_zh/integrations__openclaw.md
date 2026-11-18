OpenClaw 现支持将 LM Studio 作为原生模型提供方。
参见：[OpenClaw 文档](https://docs.openclaw.ai/providers/lmstudio)。

![OpenClaw 以 LM Studio 作为模型提供方](https://lmstudio.ai/assets/marketing/docs/openclaw.webp)

```lms_protip
**实用提示**

有一台高性能 LLM 主机？使用 [LM Link](/docs/integrations/lmlink)，让 OpenClaw 在你的笔记本上运行，模型则在主机上运行。
```

## 设置

### 启动 LM Studio 本地服务器

确保 LM Studio 作为服务器运行（默认端口 `1234`）。

你可以从应用中启动，或在终端用 `lms` 启动：

```bash
lms server start --port 1234
```

### 以 LM Studio 作为模型提供方运行 OpenClaw

按常规方式安装 OpenClaw，或按如下方式运行 OpenClaw 引导命令*（推荐）*：

```bash
openclaw onboard
```

并完成以 LM Studio 作为模型提供方的交互式设置。

也可以使用以下命令以非交互式方式完成引导：

```bash
openclaw onboard \
  --non-interactive \
  --accept-risk \
  --auth-choice lmstudio \
  --custom-base-url http://localhost:1234/v1 \
  --lmstudio-api-key "$LM_API_TOKEN" \
  --custom-model-id qwen/qwen3.5-9b
```

```lms_protip
**实用提示**

使用上下文长度大于约 50k 的模型（以及服务器/模型设置）。OpenClaw 这类工具会消耗大量上下文。
```

### 把 LM Studio 设置为默认记忆搜索提供方

要把 LM Studio 用作记忆搜索的嵌入模型提供方，运行以下命令并重启 openclaw 网关：

```bash
openclaw config set agents.defaults.memorySearch.provider lmstudio
openclaw gateway restart
```

如果遇到问题，欢迎加入我们的 [Discord](https://discord.gg/lmstudio)。
