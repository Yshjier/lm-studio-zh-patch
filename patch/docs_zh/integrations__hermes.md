Hermes Agent 现支持将 LM Studio 作为一等模型提供方。它带 JIT 加载、更高上下文长度（64K）和推理强度支持。

参见：[Hermes Agent 文档](https://hermes-agent.nousresearch.com/docs/integrations/providers#lm-studio--desktop-app-with-local-models)。

![Hermes Agent 通过 LM Link 以 LM Studio 作为模型提供方](https://lmstudio.ai/assets/marketing/docs/hermes-agent.webp)

```lms_protip
**实用提示**

有一台高性能 LLM 主机？使用 [LM Link](/docs/integrations/lmlink)，让 Hermes Agent 在你的笔记本上运行，模型则在主机上运行。
```

## 设置

### 启动 LM Studio 本地服务器

确保 LM Studio 作为服务器运行（默认端口 `1234`）。

你可以从应用中启动，或在终端用 `lms` 启动：

```bash
lms server start --port 1234
```

### 以 LM Studio 作为模型提供方运行 Hermes Agent

用以下命令运行 hermes 设置：

```bash
hermes setup
```

如果已经配置过 hermes，运行

```bash
hermes model
```

并完成以 LM Studio 作为模型提供方的交互式设置。

<details><summary>另一种方式：非交互式 CLI 设置</summary>

```bash
hermes config set model.provider lmstudio
hermes config set model.base_url http://localhost:1234/v1
hermes config set model.default your-model-name
hermes config set LM_API_KEY your-key
```

</details>

```lms_protip
**实用提示**

使用上下文长度大于约 64k 的模型。Hermes Agent 这类工具会消耗大量上下文，更长的上下文体验更好。
```

如果遇到问题，欢迎加入我们的 [Discord](https://discord.gg/lmstudio)。
