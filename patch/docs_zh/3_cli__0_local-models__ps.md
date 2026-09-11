
`lms ps` 命令显示当前加载在内存中的所有模型的信息。

## 列出已加载的模型

显示所有当前已加载的模型：

```shell
lms ps
```

示例输出：

```
   LOADED MODELS

Identifier: unsloth/deepseek-r1-distill-qwen-1.5b
  • Type:  LLM
  • Path: unsloth/DeepSeek-R1-Distill-Qwen-1.5B-GGUF/DeepSeek-R1-Distill-Qwen-1.5B-Q4_K_M.gguf
  • Size: 1.12 GB
  • Architecture: Qwen2
```

### JSON 输出

以机器可读的格式获取列表：

```shell
lms ps --json
```

## 操作远程 LM Studio 实例

`lms ps` 支持 `--host` 标志，用于连接到远程 LM Studio 实例：

```shell
lms ps --host <host>
```

为此，远程 LM Studio 实例必须正在运行，并且能从你本机访问，例如可在同一子网内访问。
