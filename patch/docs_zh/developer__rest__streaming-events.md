
流式事件让你可以通过服务器发送事件（SSE）增量渲染聊天响应。当你以 `stream: true` 调用 `POST /api/v1/chat` 时，服务器会发出一系列具名事件供你消费。这些事件按顺序到达，可能包含多个增量（用于推理和消息内容）、工具调用的边界与负载，以及遇到的任何错误。流始终以 `chat.start` 开始，以 `chat.end` 结束，后者包含与一次非流式响应等价的聚合结果。

`/api/v1/chat` 响应流中可能发送的事件类型列表：

- `chat.start`
- `model_load.start`
- `model_load.progress`
- `model_load.end`
- `prompt_processing.start`
- `prompt_processing.progress`
- `prompt_processing.end`
- `reasoning.start`
- `reasoning.delta`
- `reasoning.end`
- `tool_call.start`
- `tool_call.arguments`
- `tool_call.success`
- `tool_call.failure`
- `message.start`
- `message.delta`
- `message.end`
- `error`
- `chat.end`

事件将按以下原始格式流出：

```bash
event: <event type>
data: <JSON event data>
```

### `chat.start`

````lms_hstack
在聊天响应流开始时发出的事件。
```lms_params
- name: model_instance_id
  type: string
  description: 将生成该响应的已加载模型实例的唯一标识符。
- name: type
  type: '"chat.start"'
  description: 事件类型。始终为 `chat.start`。
```
:::split:::
```lms_code_snippet
title: 示例事件数据
variants:
  json:
    language: json
    code: |
      {
        "type": "chat.start",
        "model_instance_id": "openai/gpt-oss-20b"
      }
```
````

### `model_load.start`

````lms_hstack
表示开始加载模型以完成聊天请求。如果所请求的模型已加载，则不会发出。
```lms_params
- name: model_instance_id
  type: string
  description: 正在加载的模型实例的唯一标识符。
- name: type
  type: '"model_load.start"'
  description: 事件类型。始终为 `model_load.start`。
```
:::split:::
```lms_code_snippet
title: 示例事件数据
variants:
  json:
    language: json
    code: |
      {
        "type": "model_load.start",
        "model_instance_id": "openai/gpt-oss-20b"
      }
```
````

### `model_load.progress`

````lms_hstack
模型加载的进度。
```lms_params
- name: model_instance_id
  type: string
  description: 正在加载的模型实例的唯一标识符。
- name: progress
  type: number
  description: 模型加载进度，为 `0` 到 `1` 之间的浮点数。
- name: type
  type: '"model_load.progress"'
  description: 事件类型。始终为 `model_load.progress`。
```
:::split:::
```lms_code_snippet
title: 示例事件数据
variants:
  json:
    language: json
    code: |
      {
        "type": "model_load.progress",
        "model_instance_id": "openai/gpt-oss-20b",
        "progress": 0.65
      }
```
````

### `model_load.end`

````lms_hstack
表示模型加载成功完成。
```lms_params
- name: model_instance_id
  type: string
  description: 已加载的模型实例的唯一标识符。
- name: load_time_seconds
  type: number
  description: 加载模型所花费的时间（秒）。
- name: type
  type: '"model_load.end"'
  description: 事件类型。始终为 `model_load.end`。
```
:::split:::
```lms_code_snippet
title: 示例事件数据
variants:
  json:
    language: json
    code: |
      {
        "type": "model_load.end",
        "model_instance_id": "openai/gpt-oss-20b",
        "load_time_seconds": 12.34
      }
```
````

### `prompt_processing.start`

````lms_hstack
表示模型开始处理提示。
```lms_params
- name: type
  type: '"prompt_processing.start"'
  description: 事件类型。始终为 `prompt_processing.start`。
```
:::split:::
```lms_code_snippet
title: 示例事件数据
variants:
  json:
    language: json
    code: |
      {
        "type": "prompt_processing.start"
      }
```
````

### `prompt_processing.progress`

````lms_hstack
模型处理提示的进度。
```lms_params
- name: progress
  type: number
  description: 提示处理进度，为 `0` 到 `1` 之间的浮点数。
- name: type
  type: '"prompt_processing.progress"'
  description: 事件类型。始终为 `prompt_processing.progress`。
```
:::split:::
```lms_code_snippet
title: 示例事件数据
variants:
  json:
    language: json
    code: |
      {
        "type": "prompt_processing.progress",
        "progress": 0.5
      }
```
````

### `prompt_processing.end`

````lms_hstack
表示模型处理提示结束。
```lms_params
- name: type
  type: '"prompt_processing.end"'
  description: 事件类型。始终为 `prompt_processing.end`。
```
:::split:::
```lms_code_snippet
title: 示例事件数据
variants:
  json:
    language: json
    code: |
      {
        "type": "prompt_processing.end"
      }
```
````

### `reasoning.start`

````lms_hstack
表示模型开始流式输出推理内容。
```lms_params
- name: type
  type: '"reasoning.start"'
  description: 事件类型。始终为 `reasoning.start`。
```
:::split:::
```lms_code_snippet
title: 示例事件数据
variants:
  json:
    language: json
    code: |
      {
        "type": "reasoning.start"
      }
```
````

### `reasoning.delta`

````lms_hstack
一段推理内容。可能会到达多个增量。
```lms_params
- name: content
  type: string
  description: 推理文本片段。
- name: type
  type: '"reasoning.delta"'
  description: 事件类型。始终为 `reasoning.delta`。
```
:::split:::
```lms_code_snippet
title: 示例事件数据
variants:
  json:
    language: json
    code: |
      {
        "type": "reasoning.delta",
        "content": "Need to"
      }
```
````

### `reasoning.end`

````lms_hstack
表示推理流结束。
```lms_params
- name: type
  type: '"reasoning.end"'
  description: 事件类型。始终为 `reasoning.end`。
```
:::split:::
```lms_code_snippet
title: 示例事件数据
variants:
  json:
    language: json
    code: |
      {
        "type": "reasoning.end"
      }
```
````

### `tool_call.start`

````lms_hstack
当模型开始一次工具调用时发出。
```lms_params
- name: tool
  type: string
  description: 被调用工具的名称。
- name: provider_info
  type: object
  description: 关于工具提供方的信息。对可能的提供方类型采用可辨识联合。
  children:
    - name: 插件提供方信息
      type: object
      description: 当工具由插件提供时存在。
      children:
        - name: type
          type: '"plugin"'
          description: 提供方类型。
        - name: plugin_id
          type: string
          description: 插件的标识符。
    - name: 临时 MCP 提供方信息
      type: object
      description: 当工具由临时 MCP 服务器提供时存在。
      children:
        - name: type
          type: '"ephemeral_mcp"'
          description: 提供方类型。
        - name: server_label
          type: string
          description: MCP 服务器的标签。
- name: type
  type: '"tool_call.start"'
  description: 事件类型。始终为 `tool_call.start`。
```
:::split:::
```lms_code_snippet
title: 示例事件数据
variants:
  json:
    language: json
    code: |
      {
        "type": "tool_call.start",
        "tool": "model_search",
        "provider_info": {
          "type": "ephemeral_mcp",
          "server_label": "huggingface"
        }
      }
```
````

### `tool_call.arguments`

````lms_hstack
为当前工具调用流式输出的参数。
```lms_params
- name: tool
  type: string
  description: 被调用工具的名称。
- name: arguments
  type: object
  description: 传给工具的参数。根据工具定义的不同，可以有任何键/值。
- name: provider_info
  type: object
  description: 关于工具提供方的信息。对可能的提供方类型采用可辨识联合。
  children:
    - name: 插件提供方信息
      type: object
      description: 当工具由插件提供时存在。
      children:
        - name: type
          type: '"plugin"'
          description: 提供方类型。
        - name: plugin_id
          type: string
          description: 插件的标识符。
    - name: 临时 MCP 提供方信息
      type: object
      description: 当工具由临时 MCP 服务器提供时存在。
      children:
        - name: type
          type: '"ephemeral_mcp"'
          description: 提供方类型。
        - name: server_label
          type: string
          description: MCP 服务器的标签。
- name: type
  type: '"tool_call.arguments"'
  description: 事件类型。始终为 `tool_call.arguments`。
```
:::split:::
```lms_code_snippet
title: 示例事件数据
variants:
  json:
    language: json
    code: |
      {
        "type": "tool_call.arguments",
        "tool": "model_search",
        "arguments": {
          "sort": "trendingScore",
          "limit": 1
        },
        "provider_info": {
          "type": "ephemeral_mcp",
          "server_label": "huggingface"
        }
      }
```
````

### `tool_call.success`

````lms_hstack
工具调用的结果，以及所用的参数。
```lms_params
- name: tool
  type: string
  description: 被调用工具的名称。
- name: arguments
  type: object
  description: 传给工具的参数。
- name: output
  type: string
  description: 原始工具输出字符串。
- name: provider_info
  type: object
  description: 关于工具提供方的信息。对可能的提供方类型采用可辨识联合。
  children:
    - name: 插件提供方信息
      type: object
      description: 当工具由插件提供时存在。
      children:
        - name: type
          type: '"plugin"'
          description: 提供方类型。
        - name: plugin_id
          type: string
          description: 插件的标识符。
    - name: 临时 MCP 提供方信息
      type: object
      description: 当工具由临时 MCP 服务器提供时存在。
      children:
        - name: type
          type: '"ephemeral_mcp"'
          description: 提供方类型。
        - name: server_label
          type: string
          description: MCP 服务器的标签。
- name: type
  type: '"tool_call.success"'
  description: 事件类型。始终为 `tool_call.success`。
```
:::split:::
```lms_code_snippet
title: 示例事件数据
variants:
  json:
    language: json
    code: |
      {
        "type": "tool_call.success",
        "tool": "model_search",
        "arguments": {
          "sort": "trendingScore",
          "limit": 1
        },
        "output": "[{\"type\":\"text\",\"text\":\"Showing first 1 models...\"}]",
        "provider_info": {
          "type": "ephemeral_mcp",
          "server_label": "huggingface"
        }
      }
```
````

### `tool_call.failure`

````lms_hstack
表示工具调用失败。
```lms_params
- name: reason
  type: string
  description: 工具调用失败的原因。
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
- name: type
  type: '"tool_call.failure"'
  description: 事件类型。始终为 `tool_call.failure`。
```
:::split:::
```lms_code_snippet
title: 示例事件数据
variants:
  json:
    language: json
    code: |
      {
        "type": "tool_call.failure",
        "reason": "Cannot find tool with name open_browser.",
        "metadata": {
          "type": "invalid_name",
          "tool_name": "open_browser"
        }
      }
```
````

### `message.start`

````lms_hstack
表示模型即将开始流式输出一条消息。
```lms_params
- name: type
  type: '"message.start"'
  description: 事件类型。始终为 `message.start`。
```
:::split:::
```lms_code_snippet
title: 示例事件数据
variants:
  json:
    language: json
    code: |
      {
        "type": "message.start"
      }
```
````

### `message.delta`

````lms_hstack
一段消息内容。可能会到达多个增量。
```lms_params
- name: content
  type: string
  description: 消息文本片段。
- name: type
  type: '"message.delta"'
  description: 事件类型。始终为 `message.delta`。
```
:::split:::
```lms_code_snippet
title: 示例事件数据
variants:
  json:
    language: json
    code: |
      {
        "type": "message.delta",
        "content": "The current"
      }
```
````

### `message.end`

````lms_hstack
表示消息流结束。
```lms_params
- name: type
  type: '"message.end"'
  description: 事件类型。始终为 `message.end`。
```
:::split:::
```lms_code_snippet
title: 示例事件数据
variants:
  json:
    language: json
    code: |
      {
        "type": "message.end"
      }
```
````

### `error`

````lms_hstack
流式输出期间发生错误。最终负载仍会在 `chat.end` 中随已生成的内容一并发送。
```lms_params
- name: error
  type: object
  description: 错误信息。
  children:
    - name: type
      type: '"invalid_request" | "unknown" | "mcp_connection_error" | "plugin_connection_error" | "not_implemented" | "model_not_found" | "job_not_found" | "internal_error"'
      description: 高层级错误类型。
    - name: message
      type: string
      description: 人类可读的错误消息。
    - name: code
      type: string
      optional: true
      description: 更详细的错误码（例如校验问题码）。
    - name: param
      type: string
      optional: true
      description: 与该错误相关的参数（如适用）。
- name: type
  type: '"error"'
  description: 事件类型。始终为 `error`。
```
:::split:::
```lms_code_snippet
title: 示例事件数据
variants:
  json:
    language: json
    code: |
      {
        "type": "error",
        "error": {
          "type": "invalid_request",
          "message": "\"model\" is required",
          "code": "missing_required_parameter",
          "param": "model"
        }
      }
```
````

### `chat.end`

````lms_hstack
最终事件，包含完整的聚合响应，等价于非流式的 `POST /api/v1/chat` 响应体。
```lms_params
- name: result
  type: object
  description: 最终响应，包含 `model_instance_id`、`output`、`stats` 以及可选的 `response_id`。更多细节见[非流式聊天文档](/docs/developer/rest/chat)。
- name: type
  type: '"chat.end"'
  description: 事件类型。始终为 `chat.end`。
```
:::split:::
```lms_code_snippet
title: 示例事件数据
variants:
  json:
    language: json
    code: |
      {
        "type": "chat.end",
        "result": {
          "model_instance_id": "openai/gpt-oss-20b",
          "output": [
            { "type": "reasoning", "content": "Need to call function." },
            {
              "type": "tool_call",
              "tool": "model_search",
              "arguments": { "sort": "trendingScore", "limit": 1 },
              "output": "[{\"type\":\"text\",\"text\":\"Showing first 1 models...\"}]",
              "provider_info": { "type": "ephemeral_mcp", "server_label": "huggingface" }
            },
            { "type": "message", "content": "The current top‑trending model is..." }
          ],
          "stats": {
            "input_tokens": 329,
            "total_output_tokens": 268,
            "reasoning_output_tokens": 5,
            "tokens_per_second": 43.73,
            "time_to_first_token_seconds": 0.781
          },
          "response_id": "resp_02b2017dbc06c12bfc353a2ed6c2b802f8cc682884bb5716"
        }
      }
```
````
