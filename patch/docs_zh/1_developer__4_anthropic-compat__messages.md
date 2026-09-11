
- 方法：`POST`
- 端点：`/v1/messages`
- 参见 Anthropic 文档：https://platform.claude.com/docs/en/api/messages/create

##### cURL 示例

```bash
curl http://localhost:1234/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: $LM_API_TOKEN" \
  -d '{
    "model": "ibm/granite-4-micro",
    "max_tokens": 256,
    "messages": [
      {"role": "user", "content": "Say hello from LM Studio."}
    ]
  }'
```

如果你未启用"要求身份验证"，则 `x-api-key` 请求头是可选的。

##### cURL（流式）

```bash
curl http://localhost:1234/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: $LM_API_TOKEN" \
  -d '{
    "model": "ibm/granite-4-micro",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 256,
    "stream": true
  }'
```

你将收到 SSE 事件，例如 `message_start`、`content_block_start`、`content_block_delta`、`content_block_stop`、`message_delta` 和 `message_stop`。

##### cURL（工具）

```bash
curl http://localhost:1234/v1/messages \
  -H "Content-Type: application/json" \
  -H "x-api-key: $LM_API_TOKEN" \
  -d '{
    "model": "ibm/granite-4-micro",
    "max_tokens": 1024,
    "tools": [
      {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state, e.g. San Francisco, CA"
            }
          },
          "required": ["location"]
        }
      }
    ],
    "tool_choice": {"type": "any"},
    "messages": [
      {
        "role": "user",
        "content": "What is the weather like in San Francisco?"
      }
    ]
  }'
```
