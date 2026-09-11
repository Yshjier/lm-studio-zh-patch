
- 方法：`POST`
- 参见 OpenAI 文档：https://platform.openai.com/docs/api-reference/responses

##### cURL（非流式）

```bash
curl http://localhost:1234/v1/responses \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-oss-20b",
    "input": "Provide a prime number less than 50",
    "reasoning": { "effort": "low" }
  }'
```

##### 有状态后续请求

使用前一个响应的 `id` 作为 `previous_response_id`。

```bash
curl http://localhost:1234/v1/responses \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-oss-20b",
    "input": "Multiply it by 2",
    "previous_response_id": "resp_123"
  }'
```

##### 流式输出

```bash
curl http://localhost:1234/v1/responses \
  -H "Content-Type: application/json" \
  -d '{
    "model": "openai/gpt-oss-20b",
    "input": "Hello",
    "stream": true
  }'
```

你将收到 SSE 事件，例如 `response.created`、`response.output_text.delta` 和 `response.completed`。

##### 工具与远程 MCP（可选启用）

在应用中启用远程 MCP（开发者 → 设置）。以下是使用 MCP 服务器工具的示例负载：

```bash
curl http://localhost:1234/v1/responses \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ibm/granite-4-micro",
    "input": "What is the top trending model on hugging face?",
    "tools": [
      {
        "type": "mcp",
        "server_label": "huggingface",
        "server_url": "https://huggingface.co/mcp",
        "allowed_tools": [
          "model_search"
        ]
      }
    ]
  }'
```
