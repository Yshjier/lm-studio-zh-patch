
`高级`

默认情况下，LM Studio 会根据模型文件的元数据自动配置提示模板。

不过，你可以为任何模型自定义提示模板。

<hr>

### 为特定模型覆盖提示模板

前往"我的模型"选项卡，点击齿轮 ⚙️ 图标来编辑该模型的默认参数。

###### 小技巧：在 Mac 上按 `⌘` + `3`、在 Windows / Linux 上按 `ctrl` + `3`，即可从任意位置跳转到"我的模型"选项卡。

### 自定义提示模板

###### 💡 大多数情况下你不需要更改提示模板

当模型没有附带提示模板信息时，LM Studio 会在 **🧪 高级配置**侧边栏中显示 `Prompt Template` 配置框。

<img src="/assets/marketing/docs/prompt-template.png" style="width:80%" data-caption="聊天侧边栏中的 Prompt Template 配置框">

你可以右键点击侧边栏并选择 **Always Show Prompt Template**，让该配置框始终显示。

### 提示模板选项

#### Jinja Template

你可以用 Jinja 来表达提示模板。

###### 💡 [Jinja](<https://en.wikipedia.org/wiki/Jinja_(template_engine)>) 是一种模板引擎，用于在若干流行的 LLM 模型文件格式中编码提示模板。

#### Manual

你也可以通过指定消息角色的前缀和后缀来手动表达提示模板。

<hr>

#### 你可能想编辑提示模板的原因：

1. 模型的元数据不正确、不完整，或 LM Studio 无法识别它
2. 模型的元数据中没有提示模板（例如自定义模型或较旧的模型）
3. 你想为特定用例自定义提示模板
