LM Studio 插件支持自定义配置。也就是说，你可以定义配置模式（schema），LM Studio 会向用户呈现界面，让他们无需编辑代码即可配置你的插件。

配置分为两类：

* **按对话配置**：绑定到特定对话。不同对话可以有不同配置。大多数影响插件行为的配置都应属于这一类。
* **全局配置**：应用于*所有*对话，并在整个应用中共享。适用于 API 密钥等全局设置。

## 配置类型

可以使用 `@lmstudio/sdk` 包中的 `createConfigSchematics` 函数在 TypeScript 中定义配置。该函数允许你定义带有各种类型和选项的字段。

支持的类型包括：

* `string`：文本输入框。
* `numeric`：数字输入框，可选校验和滑块界面。
* `boolean`：复选框或开关输入。
* `stringArray`：带可配置约束的字符串值数组。
* `select`：带预定义选项的下拉选择框。

关于如何定义这些字段，详见[定义新字段](/docs/typescript/plugins/custom-configuration/defining-new-fields)一节。

## 示例

以下是一些使用自定义配置的插件

* [lmstudio/wikipedia](/lmstudio/wikipedia)

  为 LLM 提供搜索和阅读维基百科文章的工具。

* [lmstudio/openai-compat-endpoint](/lmstudio/openai-compat-endpoint)

  在 LM Studio 中使用任意 OpenAI 兼容 API。
