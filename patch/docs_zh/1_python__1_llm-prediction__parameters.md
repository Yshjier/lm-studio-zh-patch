
你可以为模型同时自定义推理时参数和加载时参数。推理参数可以按请求逐次设置，而加载参数在加载模型时设置。

# 推理参数

设置推理时参数，例如 `temperature`、`maxTokens`、`topP` 等。

```lms_code_snippet
  variants:
    ".respond()":
      language: python
      code: |
        result = model.respond(chat, config={
            "temperature": 0.6,
            "maxTokens": 50,
        })

    ".complete()":
      language: python
      code: |
        result = model.complete(chat, config={
            "temperature": 0.6,
            "maxTokens": 50,
            "stopStrings": ["\n\n"],
          })

```

关于所有可配置字段，参见 Typescript SDK 文档中的 [`LLMPredictionConfigInput`](./../../typescript/api-reference/llm-prediction-config-input)。

请注意，虽然 `structured` 可以作为一个推理时配置参数设为 JSON schema 定义
（Python SDK 不支持 Zod schema），但更推荐的做法是改为设置
[专用的 `response_format` 参数](<(./structured-responses)>)，它让你可以用基于 JSON 或类的 schema 定义，
更严格地强制输出的结构。

# 加载参数

设置加载时参数，例如上下文长度、GPU 卸载比例等。

### 用 `.model()` 设置加载参数

`.model()` 会获取一个已加载模型的句柄，或按需加载一个新模型（JIT 加载）。

**注意**：如果模型已经加载，给定的配置将被**忽略**。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        model = lms.llm("qwen2.5-7b-instruct", config={
            "contextLength": 8192,
            "gpu": {
              "ratio": 0.5,
            }
        })

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
            model = client.llm.model(
                "qwen2.5-7b-instruct",
                config={
                    "contextLength": 8192,
                    "gpu": {
                      "ratio": 0.5,
                    }
                }
            )

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.AsyncClient() as client:
            model = await client.llm.model(
                "qwen2.5-7b-instruct",
                config={
                    "contextLength": 8192,
                    "gpu": {
                      "ratio": 0.5,
                    }
                }
            )

```

关于所有可配置字段，参见 Typescript SDK 文档中的 [`LLMLoadModelConfig`](./../../typescript/api-reference/llm-load-model-config)。

### 用 `.load_new_instance()` 设置加载参数

`.load_new_instance()` 方法会创建一个新的模型实例，并用指定的配置加载它。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        client = lms.get_default_client()
        model = client.llm.load_new_instance("qwen2.5-7b-instruct", config={
            "contextLength": 8192,
            "gpu": {
              "ratio": 0.5,
            }
        })

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
            model = client.llm.load_new_instance(
                "qwen2.5-7b-instruct",
                config={
                    "contextLength": 8192,
                    "gpu": {
                      "ratio": 0.5,
                    }
                }
            )

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.AsyncClient() as client:
            model = await client.llm.load_new_instance(
                "qwen2.5-7b-instruct",
                config={
                    "contextLength": 8192,
                    "gpu": {
                      "ratio": 0.5,
                    }
                }
            )

```

关于所有可配置字段，参见 Typescript SDK 文档中的 [`LLMLoadModelConfig`](./../../typescript/api-reference/llm-load-model-config)。
