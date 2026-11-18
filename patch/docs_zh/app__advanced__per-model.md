
`高级`

你可以为 LM Studio 中的每个模型设置默认加载设置。

当该模型在应用中被加载时（包括通过 [`lms load`](/docs/cli#load-a-model-with-options)），这些设置都会被采用。

<hr>

### 为模型设置默认参数

前往"我的模型"选项卡，点击齿轮 ⚙️ 图标来编辑该模型的默认参数。

<img src="/assets/marketing/docs/model-settings-gear.webp" style="width:80%" data-caption="点击齿轮图标可编辑模型的默认加载设置。">

这会打开一个对话框，你可以在其中设置该模型的默认参数。

<video autoplay loop muted playsinline style="width:50%" data-caption="你可以在该对话框中为模型设置默认参数。">
  <source src="https://files.lmstudio.ai/default-params.mp4" type="video/mp4">
  你的浏览器不支持 video 标签。
</video>

下次加载该模型时，就会使用这些设置。

```lms_protip
#### 为什么要设置默认加载参数（并非必需，完全可选）

- 为某个模型设置特定的 GPU 卸载设置
- 为某个模型设置特定的上下文长度
- 为某个模型决定是否启用 Flash Attention

```

## 进阶主题

### 在加载模型前更改加载设置

加载模型时，你可以选择更改默认加载设置。

<img src="/assets/marketing/docs/load-model.png" style="width:80%" data-caption="你可以在加载模型前更改加载设置。">

### 把你的改动保存为模型的默认设置

如果你在加载模型时改动了加载设置，可以将其保存为该模型的默认设置。

<img src="/assets/marketing/docs/save-load-changes.png" style="width:80%" data-caption="如果你在加载模型时改动了加载设置，可以将其保存为该模型的默认设置。">

<hr>

### 社区

与其他 LM Studio 高级用户交流配置、模型、硬件等话题，欢迎加入 [LM Studio Discord 服务器](https://discord.gg/aPQfnNkxGC)。
