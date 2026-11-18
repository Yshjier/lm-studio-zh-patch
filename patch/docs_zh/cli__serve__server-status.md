
`lms server status` 命令显示 LM Studio 本地服务器的当前状态，包括它是否正在运行及其配置。

### 标志

```lms_params
- name: "--json"
  type: "flag"
  optional: true
  description: "以 JSON 格式输出状态"
- name: "--verbose"
  type: "flag"
  optional: true
  description: "启用详细日志输出"
- name: "--quiet"
  type: "flag"
  optional: true
  description: "抑制所有日志输出"
- name: "--log-level"
  type: "string"
  optional: true
  description: "使用的日志级别。默认为 'info'"
```

## 检查服务器状态

获取服务器的基本状态：

```shell
lms server status
```

示例输出：

```
The server is running on port 1234.
```

### 用法示例

```console
➜  ~ lms server start
Starting server...
Waking up LM Studio service...
Success! Server is now running on port 1234

➜  ~ lms server status
The server is running on port 1234.
```

### JSON 输出

以机器可读的 JSON 格式获取状态：

```shell
lms server status --json --quiet
```

示例输出：

```json
{ "running": true, "port": 1234 }
```

### 控制日志输出

调整日志详细程度：

```shell
lms server status --verbose
lms server status --quiet
lms server status --log-level debug
```

一次只能使用一个日志控制标志（`--verbose`、`--quiet` 或 `--log-level`）。
