
`草稿`

[`model.yaml`](https://modelyaml.org) 用单个可移植文件描述一个模型及其所有变体。LM Studio [模型目录](https://lmstudio.ai/models)中的模型全部都是用 model.yaml 实现的。

这样可以抽象掉底层格式（GGUF、MLX 等），为给定模型呈现单一的入口点。此外，model.yaml 文件还支持内置额外的元数据、加载与推理选项，甚至自定义逻辑（例如启用/禁用思考）。

**你可以在 LM Studio Hub 上克隆现有的 model.yaml 文件，甚至可以[发布你自己的](./modelyaml/publish)！**

## 核心字段

### `model`

规范标识符，形式为 `publisher/model`。

```yaml
model: qwen/qwen3-8b
```

### `base`

指向"具体"的模型文件或其他虚拟模型。每个条目使用唯一的 `key` 以及一个或多个可从其获取文件的 `sources`。

下面的片段展示了一种情况：该模型（`qwen/qwen3-8b`）可以解析为 3 个不同的具体模型之一。

```yaml
model: qwen/qwen3-8b
base:
  - key: lmstudio-community/qwen3-8b-gguf
    sources:
      - type: huggingface
        user: lmstudio-community
        repo: Qwen3-8B-GGUF
  - key: lmstudio-community/qwen3-8b-mlx-4bit
    sources:
      - type: huggingface
        user: lmstudio-community
        repo: Qwen3-8B-MLX-4bit
  - key: lmstudio-community/qwen3-8b-mlx-8bit
    sources:
      - type: huggingface
        user: lmstudio-community
        repo: Qwen3-8B-MLX-8bit
```

具体模型文件指的是实际的权重。

### `metadataOverrides`

覆盖基础模型的元数据。这对展示用途很有用，例如在 LM Studio 的模型目录或应用内模型搜索中。它不会用于对模型做任何功能性修改。

```yaml
metadataOverrides:
  domain: llm
  architectures:
    - qwen3
  compatibilityTypes:
    - gguf
    - safetensors
  paramsStrings:
    - 8B
  minMemoryUsageBytes: 4600000000
  contextLengths:
    - 40960
  vision: false
  reasoning: true
  trainedForToolUse: true
```

### `config`

用它来"内置"默认运行时设置（例如采样参数），甚至加载时选项。
其工作方式类似于[单模型默认值](/docs/app/advanced/per-model)。

- `operation:` 推理时参数
- `load:` 加载时参数

```yaml
config:
  operation:
    fields:
      - key: llm.prediction.topKSampling
        value: 20
      - key: llm.prediction.temperature
        value: 0.7
  load:
    fields:
      - key: llm.load.contextLength
        value: 42690
```

### `customFields`

定义模型专属的自定义字段。

```yaml
customFields:
  - key: enableThinking
    displayName: Enable Thinking
    description: Controls whether the model will think before replying
    type: boolean
    defaultValue: true
    effects:
      - type: setJinjaVariable
        variable: enable_thinking
```

要让上面的示例生效，jinja 模板中需要有一个名为 `enable_thinking` 的变量。

## 完整示例

取自 https://lmstudio.ai/models/qwen/qwen3-8b

```yaml
# model.yaml is an open standard for defining cross-platform, composable AI models
# Learn more at https://modelyaml.org
model: qwen/qwen3-8b
base:
  - key: lmstudio-community/qwen3-8b-gguf
    sources:
      - type: huggingface
        user: lmstudio-community
        repo: Qwen3-8B-GGUF
  - key: lmstudio-community/qwen3-8b-mlx-4bit
    sources:
      - type: huggingface
        user: lmstudio-community
        repo: Qwen3-8B-MLX-4bit
  - key: lmstudio-community/qwen3-8b-mlx-8bit
    sources:
      - type: huggingface
        user: lmstudio-community
        repo: Qwen3-8B-MLX-8bit
metadataOverrides:
  domain: llm
  architectures:
    - qwen3
  compatibilityTypes:
    - gguf
    - safetensors
  paramsStrings:
    - 8B
  minMemoryUsageBytes: 4600000000
  contextLengths:
    - 40960
  vision: false
  reasoning: true
  trainedForToolUse: true
config:
  operation:
    fields:
      - key: llm.prediction.topKSampling
        value: 20
      - key: llm.prediction.minPSampling
        value:
          checked: true
          value: 0
customFields:
  - key: enableThinking
    displayName: Enable Thinking
    description: Controls whether the model will think before replying
    type: boolean
    defaultValue: true
    effects:
      - type: setJinjaVariable
        variable: enable_thinking
```

[GitHub 规范](https://github.com/modelyaml/modelyaml)中包含更多细节和最新的 schema。
