* 方法：`POST`
* 参见 OpenAI 文档：[Decisions 指南](https://developers.openai.com/api/docs/guides/decisions) 和 [API 参考](https://developers.openai.com/api/reference/resources/decisions/methods/create)

需要一个[已加载的决策模型](/docs/developer/rest/load)，而不是普通聊天模型。

##### Python 示例

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

decision = client.decisions.create(
  model="model-identifier",
  input="I was charged twice.",
  questions=[
    {"type": "predicate", "name": "angry", "instructions": "Is the customer angry?"}
  ],
)

print(decision.answers)
```

需要 OpenAI Python 3.26.0 或更高版本。
