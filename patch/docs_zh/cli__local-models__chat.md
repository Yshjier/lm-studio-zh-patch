
使用 `lms chat` 在终端中直接与本地模型对话。这对于快速实验或编写脚本很方便。

### 标志

```lms_params
- name: "[model]"
  type: "string"
  optional: true
  description: "要使用的模型的标识符。如果省略，会提示你选择一个。"
- name: "-p, --prompt"
  type: "string"
  optional: true
  description: "发送一次性提示词，并打印回复到 stdout 后退出"
- name: "-s, --system-prompt"
  type: "string"
  optional: true
  description: "为聊天定制系统提示词"
- name: "--stats"
  type: "flag"
  optional: true
  description: "在每次回复后显示详细的预测统计信息"
- name: "--ttl"
  type: "number"
  optional: true
  description: "聊天结束后保持模型加载的秒数（默认：3600）"
```

### 开始交互式聊天

```shell
lms chat
```

如果未提供模型，会提示你选择一个。

### 与特定模型聊天

```shell
lms chat my-model
```

### 发送单条提示词并退出

使用 `-p` 打印回复到 stdout 并退出，而不是停留在交互模式：

```shell
lms chat my-model -p "Summarize this release note"
```

### 设置系统提示词

```shell
lms chat my-model -s "You are a terse assistant. Reply in two sentences."
```

### 聊天后保持模型加载

```shell
lms chat my-model --ttl 600
```

### 从其他命令管道传入输入

`lms chat` 会从 stdin 读取，因此你可以将内容直接管道传入提示词：

```shell
cat my_file.txt | lms chat -p "Summarize this, please"
```
