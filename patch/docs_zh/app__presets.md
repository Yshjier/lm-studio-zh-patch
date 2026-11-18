
预设（Preset）是一种把系统提示和其他参数打包成单个配置的方式，便于在不同聊天中轻松复用。

0.3.15 新增：你可以从文件或 URL [导入](/docs/app/presets/import)预设，甚至可以[发布](/docs/app/presets/publish)你自己的预设，分享到 LM Studio Hub 上与他人共享。

<hr>

## 保存、重置和取消选择预设

下面是预设管理器的构成示意：

<img src="/assets/marketing/docs/preset-widget-anatomy.webp" style="width:70%" data-caption="设置侧边栏中预设管理器的构成。">

## 导入、发布和更新已下载的预设

预设是 JSON 文件。你可以通过互相发送 JSON 来分享它们，也可以把它们发布到 LM Studio Hub 来分享。
你还可以通过 URL 导入其他用户的预设。更多细节见[导入](/docs/app/presets/import)和[发布](/docs/app/presets/publish)章节。

## 示例：构建你自己的提示库

你可以使用预设来创建自己的提示库。

<video autoplay loop muted playsinline style="width:60vh;" data-caption="把参数集合保存为预设，便于复用。" class="border border-border">
  <source src="https://files.lmstudio.ai/presets.mp4" type="video/mp4">
  你的浏览器不支持 video 标签。
</video>

除了系统提示之外，"高级配置"侧边栏下的每个参数都可以记录到具名预设中。

例如，你可能希望某个特定用例始终使用某个 Temperature、Top P 或 Max Tokens。你可以把这些设置保存为预设（可带或不带系统提示），并在它们之间轻松切换。

#### 预设的适用场景

- 把你的系统提示、推理参数保存为具名的 `Preset`。
- 在不同用例之间轻松切换，例如推理、创意写作、多轮对话或头脑风暴。

## 预设的存储位置

预设存储在以下目录中：

#### macOS 或 Linux

```xml
~/.lmstudio/config-presets
```

#### Windows

```xml
%USERPROFILE%\.lmstudio\config-presets
```

### 从 LM Studio 0.2.\* 预设迁移

- 你在 LM Studio 0.2.\* 中保存的预设可以直接在 0.3.3 中读取，无需任何迁移步骤。
- 如果你在**旧版预设**中保存了**新改动**，保存时会**复制**为新格式。
  - 旧文件**不会**被删除。
- 显著差异：新预设格式不包含加载参数。
  - 建议改为在"我的模型"中编辑模型的默认配置。参见[此处做法](/docs/configuration/per-model)。

<hr>

### 社区

与其他 LM Studio 用户交流 LLM、硬件等话题，欢迎加入 [LM Studio Discord 服务器](https://discord.gg/aPQfnNkxGC)。
