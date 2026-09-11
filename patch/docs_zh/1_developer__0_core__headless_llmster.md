
`llmster` 是 LM Studio 的无头守护进程，可以配置为开机启动。本指南介绍如何在 Linux 上使用 `systemctl`，让 `llmster` 自动启动、加载模型并启动 HTTP 服务器。

```lms_info
本指南适用于没有图形界面的 Linux 系统。如果你的机器有 GUI，可以改为将 LM Studio 配置为[登录时作为服务运行](/docs/developer/core/headless)。
```

## 安装守护进程

运行以下命令安装 `llmster`：

```bash
curl -fsSL https://lmstudio.ai/install.sh | bash
```

验证安装：

```bash
lms --help
```

## 下载模型

下载一个供服务器使用的模型：

```bash
lms get openai/gpt-oss-20b
```

输出中会显示模型路径。配置 systemd 时你会用到它。

## 手动测试

在配置 systemd 之前，先手动验证一切正常。

加载模型：

```bash
lms load openai/gpt-oss-20b
```

启动服务器：

```bash
lms server start
```

验证 API 有响应：

```bash
curl http://localhost:1234/v1/models
```

测试完成后停止服务器：

```bash
lms server stop
```

## 创建 Systemd 服务

创建 `/etc/systemd/system/lmstudio.service`。把 `YOUR_USERNAME` 换成你的用户名。

```ini
[Unit]
Description=LM Studio Server

[Service]
Type=oneshot
RemainAfterExit=yes
User=YOUR_USERNAME
Environment="HOME=/home/YOUR_USERNAME"
ExecStartPre=/home/YOUR_USERNAME/.lmstudio/bin/lms daemon up
ExecStartPre=/home/YOUR_USERNAME/.lmstudio/bin/lms load openai/gpt-oss-20b --yes
ExecStart=/home/YOUR_USERNAME/.lmstudio/bin/lms server start
ExecStop=/home/YOUR_USERNAME/.lmstudio/bin/lms daemon down

[Install]
WantedBy=multi-user.target
```

该 unit 会在启动时自动加载 `openai/gpt-oss-20b` 模型。或者，你也可以不在启动时加载特定模型，而是依赖服务器中的[即时（JIT）加载与自动卸载](/docs/developer/core/ttl-and-auto-evict)。

## 启用并启动服务

```bash
sudo systemctl daemon-reload
sudo systemctl enable lmstudio.service
sudo systemctl start lmstudio.service
```

## 验证

查看服务状态：

```bash
systemctl status lmstudio
```

测试 API：

```bash
curl http://localhost:1234/v1/models
```

## 服务管理

```bash
# Stop the service
sudo systemctl stop lmstudio

# Restart the service
sudo systemctl restart lmstudio

# Disable auto-start
sudo systemctl disable lmstudio
```

## 社区

与其他 LM Studio 开发者交流 LLM、硬件等话题，欢迎加入 [LM Studio Discord 服务器](https://discord.gg/aPQfnNkxGC)。

请在 [lmstudio-bug-tracker](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues) GitHub 仓库中报告 bug 和问题。
