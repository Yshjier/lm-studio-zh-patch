
````lms_hstack
`POST /api/v1/chat`

**请求体**
```lms_params
- name: model
  type: string
  optional: false
  description: 要使用的模型的唯一标识符。
- name: input
  type: string | array<object>
  optional: false
  description: 要发送给模型的消息。
  children:
    - name: 输入文本
      unstyledName: true
      type: string
      description: 消息的文本内容。
    - name: 输入对象
      unstyledName: true
      type: object
      description: 表示带附加元数据消息的对象。
      children:
        - name: 文本输入
          type: object
          optional: true
          description: 用于提供用户消息的文本输入
          children:
            - name: type
              type: '"message"'
              optional: false
              description: 输入项的类型。
            - name: content
              type: string
              description: 消息的文本内容。
              optional: false
        - name: 图像输入
          type: object
          optional: true
          description: 用于提供用户消息的图像输入
          children:
            - name: type
              type: '"image"'
              optional: false
              description: 输入项的类型。
            - name: data_url
              type: string
              description: 以 base64 编码的 data URL 表示的图像数据。
              optional: false
- name: system_prompt
  type: string
  optional: true
  description: 用于设定模型行为或指令的系统消息。
- name: integrations
  type: array<string | object>
  optional: true
  description: 为本次请求启用的集成列表（插件、临时 MCP 服务器等）。
  children:
    - name: 插件 id
      unstyledName: true
      type: string
      description: 要使用的插件的唯一标识符。插件包含 `mcp.json` 中安装的 MCP 服务器（id 为 `mcp/<server_label>`）。这是无自定义配置的插件对象的简写形式。
    - name: 插件
      unstyledName: true
      type: object
      description: 要使用的插件的规范。插件包含 `mcp.json` 中安装的 MCP 服务器（id 为 `mcp/<server_label>`）。
      children:
        - name: type
          type: '"plugin"'
          optional: false
          description: 集成类型。
        - name: id
          type: string
          optional: false
          description: 插件的唯一标识符。
        - name: allowed_tools
          type: array<string>
          optional: true
          description: 模型可从此插件调用的工具名称列表。如果未提供，则允许使用该插件的所有工具。
    - name: 临时 MCP 服务器规范
      unstyledName: true
      type: object
      description: 临时 MCP 服务器的规范。允许即时定义 MCP 服务器，而无需在 `mcp.json` 中预先配置。
      children:
        - name: type
          type: '"ephemeral_mcp"'
          optional: false
          description: 集成类型。
        - name: server_label
          type: string
          optional: false
          description: 用于标识 MCP 服务器的标签。
        - name: server_url
          type: string
          optional: false
          description: MCP 服务器的 URL。
        - name: allowed_tools
          type: array<string>
          optional: true
          description: 模型可从此服务器调用的工具名称列表。如果未提供，则允许使用该服务器的所有工具。
        - name: headers
          type: object
          optional: true
          description: 随请求发送到服务器的自定义 HTTP 请求头。
- name: stream
  type: boolean
  optional: true
  description: 是否通过 SSE 流式输出部分结果。默认 `false`。更多信息见[流式事件](/docs/developer/rest/streaming-events)。
- name: temperature
  type: number
  optional: true
  description: token 选择的随机性。0 表示确定性，更高的值会增加创造性 [0,1]。
- name: top_p
  type: number
  optional: true
  description: 可能的下一批 token 的最小累积概率 [0,1]。
- name: top_k
  type: integer
  optional: true
  description: 将下一个 token 的选择限制为概率最高的前 k 个 token。
- name: min_p
  type: number
  optional: true
  description: 一个 token 被选为输出的最小基础概率 [0,1]。
- name: repeat_penalty
  type: number
  optional: true
  description: 重复 token 序列的惩罚。1 表示不惩罚，更高的值会抑制重复。
- name: max_output_tokens
  type: integer
  optional: true
  description: 要生成的最大 token 数。
- name: reasoning
  type: '"off" | "low" | "medium" | "high" | "on"'
  optional: true
  description: 推理设置。如果所用模型不支持该推理设置，将会报错。默认为该模型自动选择的设置。
- name: context_length
  type: integer
  optional: true
  description: 作为上下文考虑的 token 数。使用 MCP 时建议使用更高的值。
- name: store
  type: boolean
  optional: true
  description: 是否存储该聊天。若设置，响应将返回 `"response_id"` 字段。默认 `true`。
- name: previous_response_id
  type: string
  optional: true
  description: 要追加到的现有响应的标识符。必须以 `"resp_"` 开头。
```
:::split:::
```lms_code_snippet
variants:
  带 MCP 的请求:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/chat \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "ibm/granite-4-micro",
          "input": "Tell me the top trending model on hugging face and navigate to https://lmstudio.ai",
          "integrations": [
            {
              "type": "ephemeral_mcp",
              "server_label": "huggingface",
              "server_url": "https://huggingface.co/mcp",
              "allowed_tools": [
                "model_search"
              ]
            },
            {
              "type": "plugin",
              "id": "mcp/playwright",
              "allowed_tools": [
                "browser_navigate"
              ]
            }
          ],
          "context_length": 8000,
          "temperature": 0
        }'
  带图像的请求:
    language: bash
    code: |
      # Image is a small red square encoded as a base64 data URL
      curl http://localhost:1234/api/v1/chat \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "qwen/qwen3-vl-4b",
          "input": [
            {
              "type": "text",
              "content": "Describe this image in two sentences"
            },
            {
              "type": "image",
              "data_url": "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVR42mP8z8BQz0AEYBxVSF+FABJADveWkH6oAAAAAElFTkSuQmCC"
            }
          ],
          "context_length": 2048,
          "temperature": 0
        }'
```
````

---

````lms_hstack
**响应字段**
```lms_params
- name: model_instance_id
  type: string
  description: 生成该响应的已加载模型实例的唯一标识符。
- name: output
  type: array<object>
  description: 生成的输出项数组。每一项可以是三种类型之一。
  children:
    - name: 消息
      unstyledName: true
      type: object
      description: 来自模型的一条文本消息。
      children:
        - name: type
          type: '"message"'
          description: 输出项的类型。
        - name: content
          type: string
          description: 消息的文本内容。
    - name: 工具调用
      unstyledName: true
      type: object
      description: 模型发起的一次工具调用。
      children:
        - name: type
          type: '"tool_call"'
          description: 输出项的类型。
        - name: tool
          type: string
          description: 被调用工具的名称。
        - name: arguments
          type: object
          description: 传给工具的参数。根据工具定义的不同，可以有任何键/值。
        - name: output
          type: string
          description: 工具返回的结果。
        - name: provider_info
          type: object
          description: 关于工具提供方的信息。
          children:
            - name: type
              type: '"plugin" | "ephemeral_mcp"'
              description: 提供方类型。
            - name: plugin_id
              type: string
              optional: true
              description: 插件的标识符（当 `type` 为 `"plugin"` 时）。
            - name: server_label
              type: string
              optional: true
              description: MCP 服务器的标签（当 `type` 为 `"ephemeral_mcp"` 时）。
    - name: 推理
      unstyledName: true
      type: object
      description: 来自模型的推理内容。
      children:
        - name: type
          type: '"reasoning"'
          description: 输出项的类型。
        - name: content
          type: string
          description: 推理的文本内容。
    - name: 无效的工具调用
      unstyledName: true
      type: object
      description: 模型发起的一次无效工具调用——由于工具名称或工具参数无效。
      children:
        - name: type
          type: '"invalid_tool_call"'
          description: 输出项的类型。
        - name: reason
          type: string
          description: 该工具调用无效的原因。
        - name: metadata
          type: object
          description: 关于该无效工具调用的元数据。
          children:
            - name: type
              type: '"invalid_name" | "invalid_arguments"'
              description: 发生的错误类型。
            - name: tool_name
              type: string
              description: 尝试调用的工具名称。
            - name: arguments
              type: object
              optional: true
              description: 传给工具的参数（仅在 `invalid_arguments` 错误时存在）。
            - name: provider_info
              type: object
              optional: true
              description: 关于工具提供方的信息（仅在 `invalid_arguments` 错误时存在）。
              children:
                - name: type
                  type: '"plugin" | "ephemeral_mcp"'
                  description: 提供方类型。
                - name: plugin_id
                  type: string
                  optional: true
                  description: 插件的标识符（当 `type` 为 `"plugin"` 时）。
                - name: server_label
                  type: string
                  optional: true
                  description: MCP 服务器的标签（当 `type` 为 `"ephemeral_mcp"` 时）。
- name: stats
  type: object
  description: token 用量和性能指标。
  children:
    - name: input_tokens
      type: number
      description: 输入 token 数。包含格式、工具定义以及聊天中的此前消息。
    - name: total_output_tokens
      type: number
      description: 生成的输出 token 总数。
    - name: reasoning_output_tokens
      type: number
      description: 用于推理的 token 数。
    - name: tokens_per_second
      type: number
      description: 生成速度（token/秒）。
    - name: time_to_first_token_seconds
      type: number
      description: 生成首个 token 所需的时间（秒）。
    - name: model_load_time_seconds
      type: number
      optional: true
      description: 为本次请求加载模型所花费的时间（秒）。仅当模型此前未加载时存在。
- name: response_id
  type: string
  optional: true
  description: 用于后续请求的响应标识符。以 `"resp_"` 开头。当 `store` 为 `true` 时存在。
```
:::split:::
```lms_code_snippet
variants:
  带 MCP 的请求:
    language: json
    code: |
      {
        "model_instance_id": "ibm/granite-4-micro",
        "output": [
          {
            "type": "tool_call",
            "tool": "model_search",
            "arguments": {
              "sort": "trendingScore",
              "query": "",
              "limit": 1
            },
            "output": "...",
            "provider_info": {
              "server_label": "huggingface",
              "type": "ephemeral_mcp"
            }
          },
          {
            "type": "message",
            "content": "..."
          },
          {
            "type": "tool_call",
            "tool": "browser_navigate",
            "arguments": {
              "url": "https://lmstudio.ai"
            },
            "output": "...",
            "provider_info": {
              "plugin_id": "mcp/playwright",
              "type": "plugin"
            }
          },
          {
            "type": "message",
            "content": "**Top Trending Model on Hugging Face** ... Below is a quick snapshot of what’s on the landing page ... more details on the model or LM Studio itself!"
          }
        ],
        "stats": {
          "input_tokens": 646,
          "total_output_tokens": 586,
          "reasoning_output_tokens": 0,
          "tokens_per_second": 29.753900615398926,
          "time_to_first_token_seconds": 1.088,
          "model_load_time_seconds": 2.656
        },
        "response_id": "resp_4ef013eba0def1ed23f19dde72b67974c579113f544086de"
      }
  带图像的请求:
    language: json
    code: |
      {
        "model_instance_id": "qwen/qwen3-vl-4b",
        "output": [
          {
            "type": "message",
            "content": "This image is a solid, vibrant red square that fills the entire frame, with no discernible texture, pattern, or other elements. It presents a minimalist, uniform visual field of pure red, evoking a sense of boldness or urgency."
          }
        ],
        "stats": {
          "input_tokens": 17,
          "total_output_tokens": 50,
          "reasoning_output_tokens": 0,
          "tokens_per_second": 51.03762685242662,
          "time_to_first_token_seconds": 0.814
        },
        "response_id": "resp_0182bd7c479d7451f9a35471f9c26b34de87a7255856b9a4"
      }
```
````
