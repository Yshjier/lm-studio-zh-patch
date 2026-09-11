
`lms log stream` 让你可以查看 LM Studio 发送给模型和从模型接收的精确字符串，并（0.3.26 新增）流式查看服务器日志。这对于调试提示词模板、模型 IO 和服务器操作很有用。

### 标志

```lms_params
- name: "-s, --source"
  type: "string"
  optional: true
  description: "日志来源：model 或 server（默认：model）"
- name: "--stats"
  type: "flag"
  optional: true
  description: "在可用时打印预测统计信息"
- name: "--filter"
  type: "string"
  optional: true
  description: "针对 model 来源的筛选：input、output 或 both"
- name: "--json"
  type: "flag"
  optional: true
  description: "以 JSON 格式输出日志（换行分隔）"
```

### 快速开始

流式查看模型 IO（默认）：

```shell
lms log stream
```

流式查看服务器日志：

```shell
lms log stream --source server
```

### 筛选模型日志

```bash
# Only the formatted user input
lms log stream --source model --filter input

# Only the model output (emitted once the message completes)
lms log stream --source model --filter output

# Both directions
lms log stream --source model --filter input,output
```

### JSON 输出与统计信息

输出 JSON：

```shell
lms log stream --source model --filter input,output --json
```

包含预测统计信息：

```shell
lms log stream --source model --filter output --stats
```
