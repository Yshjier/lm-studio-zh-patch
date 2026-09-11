
LM Studio 插件支持自定义配置。也就是说，你可以定义一份配置 schema，LM Studio 会向用户呈现相应的界面，让他们无需编辑任何代码就能配置你的插件。

配置有两种类型：

- **按聊天的配置**：绑定到某个具体聊天。不同聊天可以有不同的配置。影响插件行为的大部分配置都应属于这种类型。
- **全局配置**：应用于_所有_聊天，在整个应用内共享。这适用于 API 密钥之类的全局设置。

## 配置的类型

你可以在 TypeScript 中使用 `@lmstudio/sdk` 包提供的 `createConfigSchematics` 函数来定义配置。该函数允许你定义各种类型和选项的字段。

支持的类型包括：

- `string`：文本输入框。
- `numeric`：数字输入框，可选校验和滑块界面。
- `boolean`：复选框或开关输入框。
- `stringArray`：带可配置约束条件的字符串数组。
- `select`：带预定义选项的下拉选择框。

关于如何定义这些字段的更多细节，参见[定义新字段](./custom-configuration/defining-new-fields)章节。

## 示例

以下是一些使用自定义配置的插件：

- [lmstudio/wikipedia](https://lmstudio.ai/lmstudio/wikipedia)

  为 LLM 提供搜索和阅读维基百科文章的工具。

- [lmstudio/openai-compat-endpoint](https://lmstudio.ai/lmstudio/openai-compat-endpoint)

  在 LM Studio 中使用任何 OpenAI 兼容的 API。
