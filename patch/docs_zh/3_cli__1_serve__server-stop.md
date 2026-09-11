
`lms server stop` 命令优雅地停止正在运行的 LM Studio 服务器。

```shell
lms server stop
```

示例输出：

```
Stopped the server on port 1234.
```

服务器停止时，任何进行中的请求都会被终止。你可以使用 [`lms server start`](/docs/cli/serve/server-start) 重新启动服务器。
