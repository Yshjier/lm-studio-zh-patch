
`lms link enable` 命令在本设备上启用 LM Link，使其能够与同一 Link 上的其他设备连接。

```lms_info
LM Link 需要一个 LM Studio 账号。如果你还没有，请先运行 `lms login`。
```

## 启用 LM Link

```shell
lms link enable
```

启用后，CLI 会等待连接建立。如果有问题，会打印相关的下一步操作。

### 检查连接状态

参见 [`lms link status`](/docs/cli/link/link-status) 验证连接并查看已连接的对端。

### 禁用 LM Link

参见 [`lms link disable`](/docs/cli/link/link-disable) 关闭 LM Link。

### 了解更多

关于 LM Link 的完整概览，参见 [LM Link 文档](/docs/lmlink)。
