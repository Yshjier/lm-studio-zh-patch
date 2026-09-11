
你可以通过向 `/v1/chat/completions` 端点提供 JSON schema（经由 LM Studio 的 REST API，或任意 OpenAI 客户端），来强制 LLM 输出特定的响应格式。

<hr>

### 将 LM Studio 作为服务器启动

若要在你自己的代码中以编程方式使用 LM Studio，请将 LM Studio 作为本地服务器运行。

你可以在 LM Studio 的"开发者"选项卡中打开服务器，也可以通过 `lms` CLI：

```
lms server start
```

###### 运行 `npx lmstudio install-cli` 安装 `lms`

这将允许你通过 REST API 与 LM Studio 交互。关于 LM Studio REST API 的介绍，请参见 [REST API 概览](/docs/developer/rest)。

### 结构化输出

当提供 [JSON schema](https://json-schema.org/overview/what-is-jsonschema) 时，API 支持通过 `/v1/chat/completions` 端点输出结构化 JSON。这样做会让 LLM 以符合所提供 schema 的合法 JSON 进行响应。

它遵循 OpenAI 近期发布的 [结构化输出](https://platform.openai.com/docs/guides/structured-outputs) API 的相同格式，预期可通过 OpenAI 客户端 SDK 使用。

**使用 `curl` 的示例**

此示例演示使用 `curl` 工具发起一次结构化输出请求。

在 Mac 或 Linux 上运行此示例，可使用任意终端。在 Windows 上，请使用 [Git Bash](https://git-scm.com/download/win)。

```bash
curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "{{model}}",
    "messages": [
      {
        "role": "system",
        "content": "You are a helpful jokester."
      },
      {
        "role": "user",
        "content": "Tell me a joke."
      }
    ],
    "response_format": {
      "type": "json_schema",
      "json_schema": {
        "name": "joke_response",
        "strict": "true",
        "schema": {
          "type": "object",
          "properties": {
            "joke": {
              "type": "string"
            }
          },
          "required": ["joke"]
        }
      }
    },
    "temperature": 0.7,
    "max_tokens": 50,
    "stream": false
  }'
```

`/v1/chat/completions` 识别的所有参数都会被遵循，JSON schema 应在 `response_format` 的 `json_schema` 字段中提供。

该 JSON 对象会以 `string` 形式出现在典型的响应字段 `choices[0].message.content` 中，需要再解析为 JSON 对象。

**使用 `python` 的示例**

```python
from openai import OpenAI
import json

# Initialize OpenAI client that points to the local LM Studio server
client = OpenAI(
    base_url="http://localhost:1234/v1",
    api_key="lm-studio"
)

# Define the conversation with the AI
messages = [
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": "Create 1-3 fictional characters"}
]

# Define the expected response structure
character_schema = {
    "type": "json_schema",
    "json_schema": {
        "name": "characters",
        "schema": {
            "type": "object",
            "properties": {
                "characters": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "name": {"type": "string"},
                            "occupation": {"type": "string"},
                            "personality": {"type": "string"},
                            "background": {"type": "string"}
                        },
                        "required": ["name", "occupation", "personality", "background"]
                    },
                    "minItems": 1,
                }
            },
            "required": ["characters"]
        },
    }
}

# Get response from AI
response = client.chat.completions.create(
    model="your-model",
    messages=messages,
    response_format=character_schema,
)

# Parse and display the results
results = json.loads(response.choices[0].message.content)
print(json.dumps(results, indent=2))
```

**重要**：并非所有模型都具备结构化输出能力，尤其是参数量低于 7B 的 LLM。

如果你不确定某个模型是否支持结构化输出，请查看其模型卡 README。

### 结构化输出引擎

- 对 `GGUF` 模型：使用 `llama.cpp` 基于语法的采样 API。
- 对 `MLX` 模型：使用 [Outlines](https://github.com/dottxt-ai/outlines)。

MLX 实现在 Github 上提供：[lmstudio-ai/mlx-engine](https://github.com/lmstudio-ai/mlx-engine)。

<hr>

### 社区

与其他 LM Studio 用户交流 LLM、硬件等话题，欢迎加入 [LM Studio Discord 服务器](https://discord.gg/aPQfnNkxGC)。
