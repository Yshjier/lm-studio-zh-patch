
为输入文本生成嵌入。嵌入是捕捉语义含义的文本向量表示。嵌入是 RAG（检索增强生成）以及其他基于相似度的任务的构建模块。

### 前置条件：获取一个嵌入模型

如果你还没有嵌入模型，可以用以下命令下载一个像 `nomic-ai/nomic-embed-text-v1.5` 这样的模型：

```bash
lms get nomic-ai/nomic-embed-text-v1.5
```

## 创建嵌入

要把一个字符串转换为向量表示，把它传给相应嵌入模型句柄上的 `embed` 方法。

```lms_code_snippet
  title: "example.py"
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        model = lms.embedding_model("nomic-embed-text-v1.5")

        embedding = model.embed("Hello, world!")

```
