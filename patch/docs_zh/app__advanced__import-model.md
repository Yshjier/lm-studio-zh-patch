
你可以把在 LM Studio 之外下载的兼容模型，按预期的目录结构放置后使用。

<hr>

### 使用 `lms import`（实验性）

要导入你在 LM Studio 之外下载的 `GGUF` 模型，请在终端中运行以下命令：

```bash
lms import <path/to/model.gguf>
```

###### 按交互式提示完成导入过程。

### LM Studio 预期的模型目录结构

<img src="/assets/marketing/docs/reveal-models-dir.png" style="width:80%" data-caption="在'我的模型'选项卡中管理你的模型目录">

LM Studio 力求保留从 Hugging Face 下载的模型的目录结构。预期的目录结构如下：

```xml
~/.lmstudio/models/
└── publisher/
    └── model/
        └── model-file.gguf
```

例如，如果你有一个由 `infra-ai` 发布的名为 `ocelot-v1` 的模型，结构会像这样：

```xml
~/.lmstudio/models/
└── infra-ai/
    └── ocelot-v1/
        └── ocelot-v1-instruct-q4_0.gguf
```

<hr>

### 社区

与其他 LM Studio 用户交流 LLM、硬件等话题，欢迎加入 [LM Studio Discord 服务器](https://discord.gg/aPQfnNkxGC)。
