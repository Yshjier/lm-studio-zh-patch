
你可以用下面展示的函数和方法遍历已加载到内存中的模型。

结果是完整的 SDK 模型句柄，允许访问所有模型功能。

## 列出当前已加载到内存中的模型

这会给你等效于在 CLI 中使用 [`lms ps`](../../cli/ps) 的结果。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        all_loaded_models = lms.list_loaded_models()
        llm_only = lms.list_loaded_models("llm")
        embedding_only = lms.list_loaded_models("embedding")

        print(all_loaded_models)

    "Python（作用域资源 API）":
      language: python
      code: |
        import lms

        with lms.Client() as client:
            all_loaded_models = client.list_loaded_models()
            llm_only = client.llm.list_loaded()
            embedding_only = client.embedding.list_loaded()

            print(all_loaded_models)

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.AsyncClient() as client:
            all_loaded_models = await client.list_loaded_models()
            llm_only = await client.llm.list_loaded()
            embedding_only = await client.embedding.list_loaded()

            print(all_loaded_models)

```
