
`lms daemon up` 命令启动 llmster

### 标志

```lms_params
- name: "--json"
  type: "flag"
  optional: true
  description: "以 JSON 格式输出结果"
```

## 启动守护进程

```shell
lms daemon up
```

如果守护进程尚未运行，此命令会启动它并打印 PID。如果它已在运行，则会报告当前状态。

### JSON 输出

用于脚本或自动化：

```shell
lms daemon up --json
```

示例输出：

```json
{ "status": "running", "pid": 26754, "isDaemon": true, "version": "0.4.4+1" }
```

### 检查守护进程状态

参见 [`lms daemon status`](/docs/cli/daemon/daemon-status) 检查守护进程是否正在运行。

### 了解更多

要了解关于 llmster 的更多信息，参见 [无头模式](/docs/developer/core/headless)。
