
`lms get` 命令允许你从在线仓库搜索并下载模型。如果未指定模型，它会显示官方精选推荐。

你通过 `lms get` 下载的模型会存储在你的 LM Studio 模型目录中。

### 标志

```lms_params
- name: "[modelName]"
  type: "string"
  optional: true
  description: "要下载的模型。如果省略，则显示官方精选。对于有多种量化版本的模型，追加 '@'（例如 'llama-3.1-8b@q4_k_m'）。"
- name: "--mlx"
  type: "flag"
  optional: true
  description: "在搜索结果中只包含 MLX 模型。如果设置了 '--mlx' 或 '--gguf' 之一，则只显示匹配格式；否则结果匹配已安装的运行时。"
- name: "--gguf"
  type: "flag"
  optional: true
  description: "在搜索结果中只包含 GGUF 模型。如果设置了 '--mlx' 或 '--gguf' 之一，则只显示匹配格式；否则结果匹配已安装的运行时。"
- name: "-n, --limit"
  type: "number"
  optional: true
  description: "限制显示的模型选项数量。"
- name: "--always-show-all-results"
  type: "flag"
  optional: true
  description: "始终提示你从搜索结果中选择，即使存在精确匹配。"
- name: "-a, --always-show-download-options"
  type: "flag"
  optional: true
  description: "始终提示你选择一种量化版本，即使已自动选中精确匹配。"
```

## 下载模型

按名称下载一个模型：

```shell
lms get llama-3.1-8b
```

### 指定量化版本

下载特定量化版本的模型：

```shell
lms get llama-3.1-8b@q4_k_m
```

### 按格式筛选

只显示 MLX 或 GGUF 模型：

```shell
lms get --mlx
lms get --gguf
```

### 控制搜索结果

限制结果数量：

```shell
lms get --limit 5
```

始终显示所有选项：

```shell
lms get --always-show-all-results
lms get --always-show-download-options
```
