
借助 [LM Link](/docs/lmlink)，你的编程工具可以在远程设备（比如你网络中一台专用的 LLM 主机）上运行模型，而你在笔记本上工作。

<img src="/assets/marketing/docs/lmlink-claudecode.gif" style="width: 100%;" data-caption="Claude Code 通过 LM Link 使用在远程设备上加载的模型" />

## 照常使用你的集成

在你本机上启动 LM Studio 的服务器，并将你的工具配置为指向它。模型加载会被路由到模型所加载的设备，或者（若设置了）首选设备。

本机负责处理 `localhost:1234` 上的 API 接口，而模型运行在它所在的设备上。

```bash
lms server start --port 1234
```

### Claude Code

```bash
export ANTHROPIC_BASE_URL=http://localhost:1234
export ANTHROPIC_AUTH_TOKEN=lmstudio
claude --model qwen3-8b
```

参见完整的 [Claude Code](/docs/integrations/claude-code) 指南。

### Codex

```bash
codex --oss -m qwen3-8b
```

参见完整的 [Codex](/docs/integrations/codex) 指南。

## 设置首选设备

要在某个特定的远程设备上使用模型，请把该设备设为首选设备。

详情参见[设置首选设备](/docs/lmlink/basics/preferred-device)。

如果遇到问题，欢迎加入我们的 [Discord](https://discord.gg/lmstudio)
