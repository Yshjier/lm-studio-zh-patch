
`lms link status` 命令显示本设备上是否启用了 LM Link，并列出已连接的对端及其已加载的模型。

### 标志

```lms_params
- name: "--json"
  type: "flag"
  optional: true
  description: "以 JSON 格式输出状态"
```

## 检查状态

```shell
lms link status
```

显示本设备的名称、连接状态，以及一份已连接对端及其当前已加载模型的列表。

### JSON 输出

用于脚本或自动化：

```shell
lms link status --json
```

### 启用或禁用 LM Link

- [`lms link enable`](/docs/cli/link/link-enable) —— 在本设备上启用 LM Link。
- [`lms link disable`](/docs/cli/link/link-disable) —— 在本设备上禁用 LM Link。

### 了解更多

关于 LM Link 的完整概览，参见 [LM Link 文档](/docs/lmlink)。
