
- 方法：`POST`
- 参见 OpenAI 文档：https://platform.openai.com/docs/api-reference/embeddings

##### Python 示例

```python
from openai import OpenAI
client = OpenAI(base_url="http://localhost:1234/v1", api_key="lm-studio")

def get_embedding(text, model="model-identifier"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input=[text], model=model).data[0].embedding

print(get_embedding("Once upon a time, there was a cat."))
```
