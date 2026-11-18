
`lmstudio` 是发布在 PyPI 上的一个库，让你可以在自己的项目中使用 `lmstudio-python`。
它是开源的，在 GitHub 上开发。
你可以在[此处](https://github.com/lmstudio-ai/lmstudio-python)找到源码。

## 安装 `lmstudio-python`

由于它发布到 PyPI，`lmstudio-python` 可以使用 `pip` 或你偏好的项目依赖管理器来安装（这里展示了 `pdm` 和 `uv`，但其他 Python 项目管理工具也提供类似的添加依赖命令）。

```lms_code_snippet
  variants:
    pip:
      language: bash
      code: |
        pip install lmstudio
    pdm:
      language: bash
      code: |
        pdm add lmstudio
    uv:
      language: bash
      code: |
        uv add lmstudio
```

## 自定义服务器 API 主机和 TCP 端口

本文档中的所有示例都假设服务器 API 运行在本机的某个默认应用端口上（注意：在 Python SDK 1.5.0 之前的版本中，SDK 还要求启用可选的 HTTP REST 服务器）。

服务器 API 的网络位置可以在创建客户端实例时传入一个 `"host:port"` 字符串来覆盖。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms
        SERVER_API_HOST = "localhost:1234"

        # This must be the *first* convenience API interaction (otherwise the SDK
        # implicitly creates a client that accesses the default server API host)
        lms.configure_default_client(SERVER_API_HOST)

        # Note: the dedicated configuration API was added in lmstudio-python 1.3.0
        # For compatibility with earlier SDK versions, it is still possible to use
        # lms.get_default_client(SERVER_API_HOST) to configure the default client

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms
        SERVER_API_HOST = "localhost:1234"

        # When using the scoped resource API, each client instance
        # can be configured to use a specific server API host
        with lms.Client(SERVER_API_HOST) as client:
            model = client.llm.model()

            for fragment in model.respond_stream("What is the meaning of life?"):
                print(fragment.content, end="", flush=True)
            print() # Advance to a new line at the end of the response

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms
        SERVER_API_HOST = "localhost:1234"

        # When using the asynchronous API, each client instance
        # can be configured to use a specific server API host
        async with lms.AsyncClient(SERVER_API_HOST) as client:
            model = await client.llm.model()

            for fragment in await model.respond_stream("What is the meaning of life?"):
                print(fragment.content, end="", flush=True)
            print() # Advance to a new line at the end of the response
```

### 检查指定的 API 服务器主机是否正在运行

_要求的 Python SDK 版本_：**1.5.0**

虽然最常见的连接模式是让 SDK 在无法连接到指定的 API 服务器主机时抛出异常，但 SDK 也支持在创建 SDK 客户端实例之前，直接运行 API 检查：

```lms_code_snippet
  variants:
    "Python（同步 API）":
      language: python
      code: |
        import lmstudio as lms
        SERVER_API_HOST = "localhost:1234"

        if lms.Client.is_valid_api_host(SERVER_API_HOST):
            print(f"An LM Studio API server instance is available at {SERVER_API_HOST}")
        else:
            print("No LM Studio API server instance found at {SERVER_API_HOST}")

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms
        SERVER_API_HOST = "localhost:1234"

        if await lms.AsyncClient.is_valid_api_host(SERVER_API_HOST):
            print(f"An LM Studio API server instance is available at {SERVER_API_HOST}")
        else:
            print("No LM Studio API server instance found at {SERVER_API_HOST}")
```

### 确定默认的本地 API 服务器端口

_要求的 Python SDK 版本_：**1.5.0**

当未指定 API 服务器主机时，SDK 会在本地回环接口上查询若干端口，以寻找正在运行的 API 服务器实例。这个扫描会为每个新建的客户端实例重复执行。除了让 SDK 隐式执行此扫描外，SDK 也支持显式运行扫描，并在创建客户端时传入所报告的 API 服务器详情：

```lms_code_snippet
  variants:
    "Python（同步 API）":
      language: python
      code: |
        import lmstudio as lms

        api_host = lms.Client.find_default_local_api_host()
        if api_host is not None:
            print(f"An LM Studio API server instance is available at {api_host}")
          else:
            print("No LM Studio API server instance found on any of the default local ports")

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        api_host = await lms.AsyncClient.find_default_local_api_host()
        if api_host is not None:
            print(f"An LM Studio API server instance is available at {api_host}")
          else:
            print("No LM Studio API server instance found on any of the default local ports")
```
