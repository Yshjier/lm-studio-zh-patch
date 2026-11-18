
你可以用已下载模型列表方法来遍历本地可用的模型。

列表结果提供 `.model()` 和 `.load_new_instance()` 方法，它们允许
把已下载模型引用转换为已加载模型的完整 SDK 句柄。

## LM Studio 服务器上可用的模型

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        downloaded = lms.list_downloaded_models()
        llm_only = lms.list_downloaded_models("llm")
        embedding_only = lms.list_downloaded_models("embedding")

        for model in downloaded:
            print(model)

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
            downloaded = client.list_downloaded_models()
            llm_only = client.llm.list_downloaded()
            embedding_only = client.embedding.list_downloaded()

        for model in downloaded:
            print(model)

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.AsyncClient() as client:
            downloaded = await client.list_downloaded_models()
            llm_only = await client.llm.list_downloaded()
            embedding_only = await client.embedding.list_downloaded()

        for model in downloaded:
            print(model)

```

这会给你等效于在 CLI 中使用 [`lms ls`](../../cli/ls) 的结果。

### 示例输出：

```python
DownloadedLlm(model_key='qwen2.5-7b-instruct-1m', display_name='Qwen2.5 7B Instruct 1M', architecture='qwen2', vision=False)
DownloadedEmbeddingModel(model_key='text-embedding-nomic-embed-text-v1.5', display_name='Nomic Embed Text v1.5', architecture='nomic-bert')
```
