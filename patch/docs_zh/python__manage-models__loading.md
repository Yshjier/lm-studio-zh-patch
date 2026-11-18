
AI 模型非常庞大。把它们加载到内存可能需要一段时间。LM Studio 的 SDK 让你能精确控制这一过程。

**模型命名空间：**

- LLM 通过 `client.llm` 命名空间访问
- 嵌入模型通过 `client.embedding` 命名空间访问
- `lmstudio.llm` 等价于默认客户端上的 `client.llm.model`
- `lmstudio.embedding_model` 等价于默认客户端上的 `client.embedding.model`

**最常用的：**

- 用 `.model()` 获取任何当前已加载的模型
- 用 `.model("model-key")` 使用某个特定模型

**高级（手动模型管理）：**

- 用 `.load_new_instance("model-key")` 加载一个模型的新实例
- 用 `.unload("model-key")` 或 `model_handle.unload()` 从内存中卸载一个模型

## 用 `.model()` 获取当前模型

如果你已经在 LM Studio 中加载了一个模型（无论是通过图形界面还是 `lms load`），
你可以不带任何参数调用 `.model()` 来使用它。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        model = lms.llm()

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
            model = client.llm.model()

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.AsyncClient() as client:
            model = await client.llm.model()

```

## 用 `.model("model-key")` 获取特定模型

如果你想使用某个特定模型，可以把模型 key 作为参数传给 `.model()`。

#### 已加载则获取，未加载则加载

调用 `.model("model-key")` 时，如果模型尚未加载，它会加载该模型；如果已加载，则返回现有的实例。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        model = lms.llm("qwen/qwen3-4b-2507")

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
            model = client.llm.model("qwen/qwen3-4b-2507")

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.AsyncClient() as client:
            model = await client.llm.model("qwen/qwen3-4b-2507")

```

<!--
Learn more about the `.model()` method and the parameters it accepts in the [API Reference](../api-reference/model).
-->

## 用 `.load_new_instance()` 加载模型的新实例

使用 `load_new_instance()` 加载一个模型的新实例，即便已经存在一个。
这让你可以同时加载同一个或不同模型的多个实例。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        client = lms.get_default_client()
        model = client.llm.load_new_instance("qwen/qwen3-4b-2507")
        another_model = client.llm.load_new_instance("qwen/qwen3-4b-2507", "my-second-model")

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
            model = client.llm.load_new_instance("qwen/qwen3-4b-2507")
            another_model = client.llm.load_new_instance("qwen/qwen3-4b-2507", "my-second-model")

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.AsyncClient() as client:
            model = await client.llm.load_new_instance("qwen/qwen3-4b-2507")
            another_model = await client.llm.load_new_instance("qwen/qwen3-4b-2507", "my-second-model")

```

<!--
Learn more about the `.load_new_instance()` method and the parameters it accepts in the [API Reference](../api-reference/load_new_instance).
-->

### 关于实例标识符的说明

如果你提供了一个已经存在的实例标识符，服务器会抛出一个错误。
所以如果你并不真的在意，更稳妥的做法是不提供标识符，这样
服务器会为你生成一个。你也可以随时在 LM Studio 的服务器选项卡中查看！

## 用 `.unload()` 从内存中卸载模型

一旦你不再需要一个模型，只需在其句柄上调用 `unload()` 即可卸载它。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        model = lms.llm()
        model.unload()

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
            model = client.llm.model()
            model.unload()

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.AsyncClient() as client:
            model = await client.llm.model()
            await model.unload()

```

## 设置自定义加载配置参数

你在加载模型时也可以指定相同的加载时配置选项，例如上下文长度和 GPU 卸载。

更多内容参见[加载时配置](../llm-prediction/parameters)。

## 设置自动卸载计时器（TTL）

你可以为你加载的模型指定一个_存活时间_（time to live），即在最后一次请求之后的空闲时间（以秒为单位），
超过后模型会卸载。更多内容参见[空闲 TTL](/docs/app/api/ttl-and-auto-evict)。

```lms_protip
如果你给 `model()` 指定了 TTL，它只在 `model()` 加载
一个新实例时生效，_不会_追溯性地改变已有实例的 TTL。
```

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        model = lms.llm("qwen/qwen3-4b-2507", ttl=3600)

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
            model = client.llm.model("qwen/qwen3-4b-2507", ttl=3600)

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.AsyncClient() as client:
            model = await client.llm.model("qwen/qwen3-4b-2507", ttl=3600)

```

<!--
(TODO?: Cover the JIT implications of setting a TTL, and the default TTL variations)
-->
