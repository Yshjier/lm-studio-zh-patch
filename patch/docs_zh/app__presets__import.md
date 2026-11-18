
你可以通过文件或 URL 导入预设。这对与他人分享预设，或导入其他用户的预设很有用。

<hr>

# 导入预设

首先，点击侧边栏中的预设下拉菜单。你会看到你的预设列表，以及 2 个按钮：`+ 新建预设` 和 `导入`。

点击 `导入` 按钮以导入预设。

<img src="/assets/marketing/docs/preset-import-button.png" data-caption="导入预设" />

## 从文件导入预设

点击导入按钮后，你可以选择要导入的预设来源。你既可以从文件导入，也可以从 URL 导入。
<img src="/assets/marketing/docs/import-preset-from-file.png" data-caption="从文件导入一个或多个预设" />

## 从 URL 导入预设

已[发布](/docs/app/presets/publish)到 LM Studio Hub 的预设，可以通过提供其 URL 来导入。

导入公开预设无需在 LM Studio 内登录。

<img src="/assets/marketing/docs/import-preset-from-url.png" data-caption="通过 URL 导入预设" />

### 使用 `lms` CLI

你也可以使用 CLI 从 URL 导入预设。这对与他人分享预设很有用。

```
lms get {author}/{preset-name}
```

示例：

```bash
lms get neil/qwen3-thinking
```

### 找到你的 config-presets 目录

LM Studio 在磁盘上管理配置预设。预设默认是本地的、私有的。你或其他人都可以选择通过分享该文件来共享它们。

点击预设下拉菜单中的 `•••` 按钮，然后选择"在访达中显示"（Windows 上为"在资源管理器中显示"）。
<img src="/assets/marketing/docs/preset-reveal-in-finder.png" data-caption="在本地文件系统中显示预设" />

这会下载预设文件，并自动将其显示在应用的预设下拉菜单中。

### Hub 共享预设的存储位置

你分享的预设，以及你从 LM Studio Hub 下载的预设，都保存在 macOS 和 Linux 上的 `~/.lmstudio/hub`，或 Windows 上的 `%USERPROFILE%\.lmstudio\hub`。
