
```lms_warning
LM Studio 现已推出 [v1 REST API](/docs/developer/rest)！新项目建议使用 v1 API！
```

##### 需要 [LM Studio 0.3.6](/download) 或更高版本。

LM Studio 现在除了 OpenAI 兼容端点（[了解更多](/docs/developer/openai-compat)）和 Anthropic 兼容端点（[了解更多](/docs/developer/anthropic-compat)）之外，还拥有自己的 REST API。

该 REST API 包含增强的统计信息，如 Token/秒 和首 token 时间（TTFT），以及关于模型的丰富信息，例如已加载/未加载、最大上下文、量化等。

#### 支持的 API 端点

- [`GET /api/v0/models`](#get-apiv0models) - 列出可用模型
- [`GET /api/v0/models/{model}`](#get-apiv0modelsmodel) - 获取特定模型的信息
- [`POST /api/v0/chat/completions`](#post-apiv0chatcompletions) - 聊天补全（消息 -> 助手回复）
- [`POST /api/v0/completions`](#post-apiv0completions) - 文本补全（提示 -> 补全）
- [`POST /api/v0/embeddings`](#post-apiv0embeddings) - 文本嵌入（文本 -> 嵌入向量）

---

### 启动 REST API 服务器

要启动服务器，请运行以下命令：

```bash
lms server start
```

```lms_protip
你可以把 LM Studio 作为服务运行，并让服务器在开机时自动启动，而无需启动 GUI。[了解无头模式](/docs/developer/core/headless)。
```

## 端点

### `GET /api/v0/models`

列出所有已加载和已下载的模型

**示例请求**

```bash
curl -H "Authorization: Bearer $LM_API_TOKEN" http://localhost:1234/api/v0/models
```

**响应格式**

```json
{
  "object": "list",
  "data": [
    {
      "id": "qwen2-vl-7b-instruct",
      "object": "model",
      "type": "vlm",
      "publisher": "mlx-community",
      "arch": "qwen2_vl",
      "compatibility_type": "mlx",
      "quantization": "4bit",
      "state": "not-loaded",
      "max_context_length": 32768
    },
    {
      "id": "meta-llama-3.1-8b-instruct",
      "object": "model",
      "type": "llm",
      "publisher": "lmstudio-community",
      "arch": "llama",
      "compatibility_type": "gguf",
      "quantization": "Q4_K_M",
      "state": "not-loaded",
      "max_context_length": 131072
    },
    {
      "id": "text-embedding-nomic-embed-text-v1.5",
      "object": "model",
      "type": "embeddings",
      "publisher": "nomic-ai",
      "arch": "nomic-bert",
      "compatibility_type": "gguf",
      "quantization": "Q4_0",
      "state": "not-loaded",
      "max_context_length": 2048
    }
  ]
}
```

---

### `GET /api/v0/models/{model}`

获取某一个特定模型的信息

**示例请求**

```bash
curl -H "Authorization: Bearer $LM_API_TOKEN" http://localhost:1234/api/v0/models/qwen2-vl-7b-instruct
```

**响应格式**

```json
{
  "id": "qwen2-vl-7b-instruct",
  "object": "model",
  "type": "vlm",
  "publisher": "mlx-community",
  "arch": "qwen2_vl",
  "compatibility_type": "mlx",
  "quantization": "4bit",
  "state": "not-loaded",
  "max_context_length": 32768
}
```

---

### `POST /api/v0/chat/completions`

聊天补全 API。你提供 messages 数组，然后收到对话中的下一条助手回复。

**示例请求**

```bash
curl http://localhost:1234/api/v0/chat/completions \
  -H "Authorization: Bearer $LM_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "granite-3.0-2b-instruct",
    "messages": [
      { "role": "system", "content": "Always answer in rhymes." },
      { "role": "user", "content": "Introduce yourself." }
    ],
    "temperature": 0.7,
    "max_tokens": -1,
    "stream": false
  }'
```

**响应格式**

```json
{
  "id": "chatcmpl-i3gkjwthhw96whukek9tz",
  "object": "chat.completion",
  "created": 1731990317,
  "model": "granite-3.0-2b-instruct",
  "choices": [
    {
      "index": 0,
      "logprobs": null,
      "finish_reason": "stop",
      "message": {
        "role": "assistant",
        "content": "Greetings, I'm a helpful AI, here to assist,\nIn providing answers, with no distress.\nI'll keep it short and sweet, in rhyme you'll find,\nA friendly companion, all day long you'll bind."
      }
    }
  ],
  "usage": {
    "prompt_tokens": 24,
    "completion_tokens": 53,
    "total_tokens": 77
  },
  "stats": {
    "tokens_per_second": 51.43709529007664,
    "time_to_first_token": 0.111,
    "generation_time": 0.954,
    "stop_reason": "eosFound"
  },
  "model_info": {
    "arch": "granite",
    "quant": "Q4_K_M",
    "format": "gguf",
    "context_length": 4096
  },
  "runtime": {
    "name": "llama.cpp-mac-arm64-apple-metal-advsimd",
    "version": "1.3.0",
    "supported_formats": ["gguf"]
  }
}
```

---

### `POST /api/v0/completions`

文本补全 API。你提供一个提示，然后收到补全结果。

**示例请求**

```bash
curl http://localhost:1234/api/v0/completions \
  -H "Authorization: Bearer $LM_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "granite-3.0-2b-instruct",
    "prompt": "the meaning of life is",
    "temperature": 0.7,
    "max_tokens": 10,
    "stream": false,
    "stop": "\n"
  }'
```

**响应格式**

```json
{
  "id": "cmpl-p9rtxv6fky2v9k8jrd8cc",
  "object": "text_completion",
  "created": 1731990488,
  "model": "granite-3.0-2b-instruct",
  "choices": [
    {
      "index": 0,
      "text": " to find your purpose, and once you have",
      "logprobs": null,
      "finish_reason": "length"
    }
  ],
  "usage": {
    "prompt_tokens": 5,
    "completion_tokens": 9,
    "total_tokens": 14
  },
  "stats": {
    "tokens_per_second": 57.69230769230769,
    "time_to_first_token": 0.299,
    "generation_time": 0.156,
    "stop_reason": "maxPredictedTokensReached"
  },
  "model_info": {
    "arch": "granite",
    "quant": "Q4_K_M",
    "format": "gguf",
    "context_length": 4096
  },
  "runtime": {
    "name": "llama.cpp-mac-arm64-apple-metal-advsimd",
    "version": "1.3.0",
    "supported_formats": ["gguf"]
  }
}
```

---

### `POST /api/v0/embeddings`

文本嵌入 API。你提供一段文本，将返回该文本的嵌入向量表示。

**示例请求**

```bash
curl http://localhost:1234/api/v0/embeddings \
  -H "Authorization: Bearer $LM_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-embedding-nomic-embed-text-v1.5",
    "input": "Some text to embed"
  }
```

**示例响应**

```json
{
  "object": "list",
  "data": [
    {
      "object": "embedding",
      "embedding": [
        -0.016731496900320053,
        0.028460891917347908,
        -0.1407836228609085,
        ... (truncated for brevity) ...,
        0.02505224384367466,
        -0.0037634256295859814,
        -0.04341062530875206
      ],
      "index": 0
    }
  ],
  "model": "text-embedding-nomic-embed-text-v1.5@q4_k_m",
  "usage": {
    "prompt_tokens": 0,
    "total_tokens": 0
  }
}
```

---

如遇 bug，请在 [Github](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues) 上提交 issue。
