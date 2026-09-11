
##### 需要 [LM Studio 0.4.0](/download) 或更高版本。

LM Studio 支持用 API 令牌进行身份验证，提供了一种安全便捷的方式来访问 LM Studio API。

默认情况下，LM Studio API 运行**时不强制身份验证**。对于生产或共享环境，请启用 API 令牌身份验证以实现安全访问。

```lms_info
要启用 API 令牌身份验证、创建令牌并控制细粒度权限，请查看[此指南](/docs/developer/core/authentication)了解详情。
```

## 提供 API 令牌

API 令牌可以通过两种方式提供：

1. **环境变量（推荐）**：设置 `LM_API_TOKEN` 环境变量，SDK 会自动读取它。
2. **函数参数**：直接把令牌作为 `api_token` 参数传入。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        # Configure the default client with an API token
        lms.configure_default_client(api_token="your-token-here")

        model = lms.llm()
        result = model.respond("What is the meaning of life?")
        print(result)

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        # Pass api_token to the Client constructor
        with lms.Client(api_token="your-token-here") as client:
            model = client.llm.model()
            result = model.respond("What is the meaning of life?")
            print(result)

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        # Pass api_token to the AsyncClient constructor
        async with lms.AsyncClient(api_token="your-token-here") as client:
            model = await client.llm.model()
            result = await model.respond("What is the meaning of life?")
            print(result)
```
