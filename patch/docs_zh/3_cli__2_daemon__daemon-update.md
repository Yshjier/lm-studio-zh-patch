
`lms daemon update` 命令获取并安装最新版本的 llmster。

### 标志

```lms_params
- name: "--beta"
  type: "flag"
  optional: true
  description: "更新到最新的 beta 版本"
```

## 更新守护进程

先停止守护进程：

```shell
lms daemon down
```

然后运行更新：

```shell
lms daemon update
```

获取最新的稳定版本并安装它。

### 更新到 beta 通道

```shell
lms daemon update --beta
```

### 更新之后

再次启动守护进程以使用新版本：

```shell
lms daemon up
```

要了解关于 llmster 的更多信息，参见 [无头模式](/docs/developer/core/headless)。
