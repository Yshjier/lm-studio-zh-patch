
`lms ls` 命令显示已下载到你机器上的所有模型列表，包括它们的大小、架构和参数量。

### 标志

```lms_params
- name: "--llm"
  type: "flag"
  optional: true
  description: "只显示 LLM。未设置时，显示所有模型"
- name: "--embedding"
  type: "flag"
  optional: true
  description: "只显示嵌入模型"
- name: "--json"
  type: "flag"
  optional: true
  description: "以 JSON 格式输出列表"
- name: "--detailed"
  type: "flag"
  optional: true
  description: "显示每个模型的详细信息"
```

## 列出所有模型

显示所有已下载的模型：

```shell
lms ls
```

示例输出：

```
You have 47 models, taking up 160.78 GB of disk space.

LLMs (Large Language Models)                       PARAMS      ARCHITECTURE           SIZE
lmstudio-community/meta-llama-3.1-8b-instruct          8B         Llama            4.92 GB
hugging-quants/llama-3.2-1b-instruct                   1B         Llama            1.32 GB
mistral-7b-instruct-v0.3                                         Mistral           4.08 GB
zeta                                                   7B         Qwen2            4.09 GB

... (abbreviated in this example) ...

Embedding Models                                   PARAMS      ARCHITECTURE           SIZE
text-embedding-nomic-embed-text-v1.5@q4_k_m                     Nomic BERT        84.11 MB
text-embedding-bge-small-en-v1.5                     33M           BERT           24.81 MB
```

### 按模型类型筛选

只列出 LLM 模型：

```shell
lms ls --llm
```

只列出嵌入模型：

```shell
lms ls --embedding
```

### 其他输出格式

获取模型的详细信息：

```shell
lms ls --detailed
```

以 JSON 格式输出：

```shell
lms ls --json
```

## 操作远程 LM Studio 实例

`lms ls` 支持 `--host` 标志，用于连接到远程 LM Studio 实例：

```shell
lms ls --host <host>
```

为此，远程 LM Studio 实例必须正在运行，并且能从你本机访问，例如可在同一子网内访问。
