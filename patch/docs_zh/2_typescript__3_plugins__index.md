
插件通过提供在运行期间特定时机执行的“钩子函数”来扩展 LM Studio 的功能。

插件目前使用 JavaScript/TypeScript 编写，运行在 Node.js v22.21.1 上。Python 支持正在开发中。

## 快速上手

LM Studio 内置了 Node.js，因此无需单独安装。

### 创建新插件

要创建新插件，请前往 LM Studio…… [未完待续]

### 以开发模式运行插件

插件创建完成后，在插件目录中运行以下命令即可启动开发模式：

```bash
lms dev
```

你的插件会出现在 LM Studio 的插件列表中。当你修改代码时，开发模式会自动重新构建并重新加载插件。

只有在开发阶段才需要 `lms dev`。插件安装后，LM Studio 会在需要时自动运行它们。更多关于分发和安装插件的内容，参见[分享插件](./plugins/publish-plugins)章节。

## 后续步骤

- [工具提供者](./plugins/tools-provider)

  让模型在生成过程中可以使用额外的工具，从而获得更多能力，例如访问外部 API 或执行计算。

- [提示词预处理器](./plugins/prompt-preprocessor)

  在用户输入到达模型之前修改它 —— 处理文件上传、注入上下文，或转换查询。

- [生成器](./plugins/generator)

  创建可替代本地模型的自定义文本生成来源，非常适合在线模型适配器。

- [自定义配置](./plugins/custom-configuration)

  添加配置界面，让用户可以自定义插件的行为。

- [第三方依赖](./plugins/dependencies)

  使用 npm 包，在插件中复用现有的库。

- [分享插件](./plugins/publish-plugins)

  打包你的插件并与社区分享。
