
_要求的 Python SDK 版本_：**1.2.0**

LM Studio 允许你在加载模型时配置某些参数，
[通过服务器界面](/docs/advanced/per-model)或[通过 API](/docs/api/sdk/load-model)。

你可以用 SDK 获取某个给定模型加载时所用的配置。

在下面的示例中，可以把 LLM 引用替换为
嵌入模型引用，而无需任何其他改动。

```lms_protip
上下文长度是一个特殊情况，它[有自己专门的方法](/docs/api/sdk/get-context-length)。
```

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        model = lms.llm()

        print(model.get_load_config())

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
            model = client.llm.model()

            print(model.get_load_config())

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.Client() as client:
            model = await client.llm.model()

            print(await model.get_load_config())

```
