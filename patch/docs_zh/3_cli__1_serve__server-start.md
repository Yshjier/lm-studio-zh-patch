
`lms server start` 命令启动 LM Studio 本地服务器，让你可以通过 HTTP API 调用来与已加载的模型交互。

### 标志

```lms_params
- name: "--port"
  type: "number"
  optional: true
  description: "运行服务器的端口。如果未提供，使用上次使用的端口"
- name: "--cors"
  type: "flag"
  optional: true
  description: "为 Web 应用开发启用 CORS 支持。未设置时，CORS 处于禁用状态"
```

## 启动服务器

以默认设置启动服务器：

```shell
lms server start
```

### 指定自定义端口

在特定端口上运行服务器：

```shell
lms server start --port 3000
```

### 启用 CORS 支持

为了配合 Web 应用或某些 VS Code 扩展使用，你可能需要启用 CORS 支持：

```shell
lms server start --cors
```

请注意，启用 CORS 可能会让你的服务器面临安全风险，因此仅在必要时使用。

### 检查服务器状态

关于检查服务器状态的更多信息，参见 [`lms server status`](/docs/cli/serve/server-status)。
