
`lms load` 命令将模型加载到内存。你可以选择性地设置上下文长度、GPU 卸载和 TTL 等参数。本指南也涵盖用 `lms unload` 卸载模型。

### 标志

```lms_params
- name: "[path]"
  type: "string"
  optional: true
  description: "要加载的模型的路径。如果未提供，会提示你选择一个"
- name: "--ttl"
  type: "number"
  optional: true
  description: "如果提供，则当模型在这段时间（秒）内未被使用时，它将被卸载"
- name: "--gpu"
  type: "string"
  optional: true
  description: "向 GPU 卸载多少。取值：0-1、off、max"
- name: "--context-length"
  type: "number"
  optional: true
  description: "生成文本时用作上下文的 token 数量"
- name: "--identifier"
  type: "string"
  optional: true
  description: "为已加载模型分配的、用于 API 引用的标识符"
- name: "--estimate-only"
  type: "boolean"
  optional: true
  description: "打印资源（内存）估算值，并在不加载模型的情况下退出"
```

## 加载模型

通过运行以下命令将模型加载到内存：

```shell
lms load <model_key>
```

你可以先运行 [`lms ls`](/docs/cli/local-models/ls) 列出本地已下载的模型，从而找到 `model_key`。

### 设置自定义标识符

你也可以可选择性地为已加载的模型分配一个自定义标识符，用于 API 引用：

```shell
lms load <model_key> --identifier "my-custom-identifier"
```

之后，你就可以在后续命令和 API 调用中通过标识符 `my_model`（`model` 参数）来引用该模型。

### 设置上下文长度

你可以在加载模型时用 `--context-length` 标志设置上下文长度：

```shell
lms load <model_key> --context-length 4096
```

这决定了模型在生成文本时会把多少 token 视为上下文。

### 设置 GPU 卸载

用 `--gpu` 标志控制 GPU 内存使用：

```shell
lms load <model_key> --gpu 0.5    # Offload 50% of layers to GPU
lms load <model_key> --gpu max    # Offload all layers to GPU
lms load <model_key> --gpu off    # Disable GPU offloading
```

如果未指定，LM Studio 会自动确定最优的 GPU 使用方式。

### 设置 TTL

用 `--ttl` 标志设置自动卸载计时器（以秒为单位）：

```shell
lms load <model_key> --ttl 3600   # Unload after 1 hour of inactivity
```

### 不加载模型而估算资源

在加载模型前用 `--estimate-only` 预览内存需求：

```shell
lms load --estimate-only <model_key>
```

`--context-length` 和 `--gpu` 等可选的标志会被采纳并反映在估算值中。估算器会考虑上下文长度、flash attention 以及模型是否启用了视觉等因素。

示例：

```bash
$ lms load --estimate-only gpt-oss-120b
Model: openai/gpt-oss-120b
Estimated GPU Memory:   65.68 GB
Estimated Total Memory: 65.68 GB

Estimate: This model may be loaded based on your resource guardrails settings.
```

## 卸载模型

使用 `lms unload` 将模型从内存中移除。

### 标志

```lms_params
- name: "[model_key]"
  type: "string"
  optional: true
  description: "要卸载的模型的 key。如果未提供，会提示你选择一个"
- name: "--all"
  type: "flag"
  optional: true
  description: "卸载当前所有已加载的模型"
- name: "--host"
  type: "string"
  optional: true
  description: "要连接的远程 LM Studio 实例的主机地址"
```

### 卸载特定模型

```shell
lms unload <model_key>
```

如果未提供模型 key，会提示你从当前已加载的模型中选择。

### 卸载所有模型

```shell
lms unload --all
```

### 从远程 LM Studio 实例卸载

```shell
lms unload <model_key> --host <host>
```

## 操作远程 LM Studio 实例

`lms load` 支持 `--host` 标志，用于连接到远程 LM Studio 实例。

```shell
lms load <model_key> --host <host>
```

为此，远程 LM Studio 实例必须正在运行，并且能从你本机访问，例如可在同一子网内访问。
