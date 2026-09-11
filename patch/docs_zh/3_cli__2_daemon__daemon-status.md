
`lms daemon status` 命令报告 llmster 当前是否正在运行。

### 标志

```lms_params
- name: "--json"
  type: "flag"
  optional: true
  description: "以 JSON 格式输出状态"
```

## 检查守护进程状态

```shell
lms daemon status
```

### JSON 输出

用于脚本或自动化：

```shell
lms daemon status --json
```

运行时的示例输出：

```json
{ "status": "running", "pid": 12345, "isDaemon": true }
```

未运行时的示例输出：

```json
{ "status": "not-running" }
```

### 启动或停止守护进程

- [`lms daemon up`](/docs/cli/daemon/daemon-up) —— 启动守护进程。
- [`lms daemon down`](/docs/cli/daemon/daemon-down) —— 停止守护进程。

要了解关于 llmster 的更多信息，参见 [无头模式](/docs/developer/core/headless)。
