* 方法：`POST`
* 端点：`/v1/systemone`
* 参见 llama.cpp 文档：[System One API](https://github.com/ggml-org/llama.cpp/blob/master/tools/server/README.md#post-v1systemone-typesafe-compatible-system-one-api)

使用[已加载决策模型](/docs/developer/rest/load)的标识符，而不是普通聊天模型。

提供 `state`，以及以问题 ID 为键的 `questions` 对象。问题类型包括 `noul`（条件成立的概率）、`choice`（从 `criteria` 对象中选择）和 `score`（按有序的 `criteria` 数组评分）。响应包含以问题 ID 为键的 `answers` 对象。

图片必须是内联 base64 数据 URL，且需要支持图片输入的模型。

##### cURL

```bash
curl http://localhost:1234/v1/systemone \
  -H "Content-Type: application/json" \
  -d '{
    "model": "your-decision-model",
    "state": "I was charged twice.",
    "questions": {
      "angry": {"type": "noul", "instructions": "Is the customer angry?"}
    }
  }'
```

OpenAI 兼容的请求与响应格式，参见 [Decisions](/docs/developer/openai-compat/decisions)。
