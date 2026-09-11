
LM Studio 可以作为后台服务运行，无需图形界面。有两种方式：

1. **llmster**（推荐）——独立守护进程，无需图形界面
2. **桌面应用的无头模式**——隐藏界面，把桌面应用当作服务运行

## 方式一：llmster（推荐）

llmster 是 LM Studio 桌面应用的核心，被打包成服务器原生形态，不依赖图形界面。它可以在 Linux 机器、云服务器、GPU 主机或你的本地机器上运行，无需 GUI。详见 [LM Studio 0.4.0 发布说明](/blog/0.4.0)。

<img src="/assets/marketing/blog/0.4.0/llmster@2x.png" alt="llmster" style="" data-caption="" />

### 安装 llmster

**Linux / Mac**

```bash
curl -fsSL https://lmstudio.ai/install.sh | bash
```

**Windows**

```bash
irm https://lmstudio.ai/install.ps1 | iex
```

### 启动 llmster

```bash
lms daemon up
```

完整参数见 [daemon CLI 文档](/docs/cli/daemon/daemon-up)。

关于在 Linux 上把 llmster 配置为开机启动任务，请参见 [Linux 开机启动任务](/docs/developer/core/headless_llmster)。

## 方式二：桌面应用的无头模式

适用于带图形界面的 Mac、Windows 和 Linux 机器。如果你已经安装了桌面应用，并希望它作为后台服务运行，这种方式很合适。

### 登录时启动 LLM 服务

进入应用设置（`Cmd` / `Ctrl` + `,`），勾选"登录时运行 LLM 服务器"。

<img src="/assets/marketing/docs/headless-settings.webp" style="" data-caption="启用 LLM 服务器在登录时启动" />

启用该设置后，退出应用会将其最小化到系统托盘，LLM 服务器继续在后台运行。

### 自动启动服务器

你上次的服务器状态会被保存，并在应用或服务启动时恢复。

如需以编程方式实现：

```bash
lms server start
```

## REST 端点的即时（JIT）模型加载

以上两种方式均适用。当你把 LM Studio 作为 LLM 服务、供其他前端或应用使用时非常有用。

<img src="/assets/marketing/docs/jit-loading.webp" style="" data-caption="按需加载模型" />

#### 当 JIT 加载开启时：

- 对 OpenAI 兼容的 `/v1/models` 的调用会返回所有已下载的模型，而不只是已加载进内存的模型
- 对推理端点的调用会在模型尚未加载时自动将其载入内存

#### 当 JIT 加载关闭时：

- 对 OpenAI 兼容的 `/v1/models` 的调用只返回已加载进内存的模型
- 你必须先手动把模型载入内存才能使用

#### 关于自动卸载？

通过 JIT 加载的模型默认会在闲置一段时间后被自动从内存中卸载（[了解更多](/docs/developer/core/ttl-and-auto-evict)）。

### 社区

与其他 LM Studio 开发者交流 LLM、硬件等话题，欢迎加入 [LM Studio Discord 服务器](https://discord.gg/aPQfnNkxGC)。

请在 [lmstudio-bug-tracker](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues) GitHub 仓库中报告 bug 和问题。
