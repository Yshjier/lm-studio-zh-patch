为输入文本生成嵌入向量。嵌入向量是文本的向量表示，用于捕捉语义含义。嵌入向量是 RAG（检索增强生成）及其他基于相似度的任务的基础构件。

### 前置条件：获取嵌入模型

如果还没有嵌入模型，可以用以下命令下载 `nomic-ai/nomic-embed-text-v1.5` 这类模型：

```bash
lms get nomic-ai/nomic-embed-text-v1.5
```

## 创建嵌入

要把字符串转换为向量表示，将其传给对应嵌入模型句柄的 `embed` 方法。

```python title="example.py"
import lmstudio as lms

model = lms.embedding_model("nomic-embed-text-v1.5")

embedding = model.embed("Hello, world!")
```
