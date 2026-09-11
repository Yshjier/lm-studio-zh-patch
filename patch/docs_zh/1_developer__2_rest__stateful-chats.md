
`/api/v1/chat` 端点默认是有状态的。这意味着你无需在每次请求中传入完整的对话历史——LM Studio 会为你自动存储和管理上下文。

## 工作原理

当你发送聊天请求时，LM Studio 会把对话存入一个聊天线程，并在响应中返回 `response_id`。在后续请求中使用该 `response_id` 即可继续对话。

```lms_code_snippet
title: 开始一段新对话
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/chat \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "ibm/granite-4-micro",
          "input": "My favorite color is blue."
        }'
```

响应中包含 `response_id`：

```lms_info
每个响应都包含一个唯一的 `response_id`，你可以用它来引用对话中的这个特定位置，供未来请求使用。这让你能够对对话进行分支。
```

```lms_code_snippet
title: 响应
variants:
  response:
    language: json
    code: |
      {
        "model_instance_id": "ibm/granite-4-micro",
        "output": [
          {
            "type": "message",
            "content": "That's great! Blue is a beautiful color..."
          }
        ],
        "response_id": "resp_abc123xyz..."
      }
```

## 继续对话

在下一次请求中传入 `previous_response_id` 即可继续对话。模型会记住此前的上下文。

```lms_code_snippet
title: 继续对话
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/chat \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "ibm/granite-4-micro",
          "input": "What color did I just mention?",
          "previous_response_id": "resp_abc123xyz..."
        }'
```

模型可以引用此前的消息，无需你重新发送，并会返回一个新的 `response_id` 供继续使用。

## 禁用有状态存储

如果你不想存储对话，请将 `store` 设为 `false`。响应中将不再包含 `response_id`。

```lms_code_snippet
title: 无状态聊天
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/chat \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "ibm/granite-4-micro",
          "input": "Tell me a joke.",
          "store": false
        }'
```

这适用于无需维护上下文的一次性请求。
