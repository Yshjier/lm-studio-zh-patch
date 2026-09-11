
`lms link set-preferred-device` 命令设置当某个模型在多个相连设备上可用时，使用 Link 上的哪台设备。

## 设置首选设备

不带参数运行该命令，可从已连接设备的交互式列表中选择：

```shell
lms link set-preferred-device
```

或者直接传入设备标识符以跳过提示：

```shell
lms link set-preferred-device <deviceIdentifier>
```

设备标识符列在 [`lms link status`](/docs/cli/link/link-status) 的输出中。

关于首选设备如何影响模型路由的更多内容，参见[通过 REST API 使用 LM Link](/docs/developer/core/lmlink)。

### 了解更多

关于 LM Link 的完整概览，参见 [LM Link 文档](/docs/lmlink)。
