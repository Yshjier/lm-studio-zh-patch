
- 方法：`POST`
- 对聊天微调模型会自动应用提示模板
- 在负载中提供推理参数（temperature、top_p 等）
- 参见 OpenAI 文档：https://platform.openai.com/docs/api-reference/chat
- 提示：保持一个终端打开并运行 [`lms log stream`](/docs/cli/serve/log-stream) 以检查模型输入

##### Python 示例

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

completion = client.chat.completions.create(
  model="model-identifier",
  messages=[
    {"role": "system", "content": "Always answer in rhymes."},
    {"role": "user", "content": "Introduce yourself."}
  ],
  temperature=0.7,
)

print(completion.choices[0].message)
```

### 支持的负载参数

参数语义参见 https://platform.openai.com/docs/api-reference/chat/create 。

```py
model
top_p
top_k
messages
temperature
max_tokens
stream
stop
presence_penalty
frequency_penalty
logit_bias
repeat_penalty
seed
```
