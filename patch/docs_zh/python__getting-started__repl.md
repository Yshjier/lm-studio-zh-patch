
为了简化交互式使用，`lmstudio-python` 提供一个便捷 API，它通过 `atexit` 钩子管理其资源，从而允许一个默认的同步客户端会话在多个交互式命令之间使用。

这个便捷 API 在本文档的示例中显示为 `Python (convenience API)` 标签页（与使用 `with` 语句来确保网络通信资源确定性清理的 `Python (scoped resource API)` 示例并列）。

该便捷 API 允许使用标准的 Python REPL，或 Jupyter Notebook 之类的更灵活替代品，来与加载到 LM Studio 中的 AI 模型交互。例如：

```lms_code_snippet
  title: "Python REPL"
  variants:
    "交互式聊天会话":
      language: python
      code: |
        >>> import lmstudio as lms
        >>> loaded_models = lms.list_loaded_models()
        >>> for idx, model in enumerate(loaded_models):
        ...     print(f"{idx:>3} {model}")
        ...
          0 LLM(identifier='qwen2.5-7b-instruct')
        >>> model = loaded_models[0]
        >>> chat = lms.Chat("You answer questions concisely")
        >>> chat = lms.Chat("You answer questions concisely")
        >>> chat.add_user_message("Tell me three fruits")
        UserMessage(content=[TextData(text='Tell me three fruits')])
        >>> print(model.respond(chat, on_message=chat.append))
        Banana, apple, orange.
        >>> chat.add_user_message("Tell me three more fruits")
        UserMessage(content=[TextData(text='Tell me three more fruits')])
        >>> print(model.respond(chat, on_message=chat.append))
        Mango, strawberry, avocado.
        >>> chat.add_user_message("How many fruits have you told me?")
        UserMessage(content=[TextData(text='How many fruits have you told me?')])
        >>> print(model.respond(chat, on_message=chat.append))
        You asked for three initial fruits and three more, so I've listed a total of six fruits.

```

虽然主要并非为此用途设计，但 SDK 的异步结构化并发 API 与由 `python -m asyncio` 启动的异步 Python REPL 兼容。
例如：

```lms_code_snippet
  title: "Python REPL"
  variants:
    "异步聊天会话":
      language: python
      code: |
        # Note: assumes use of the "python -m asyncio" asynchronous REPL (or equivalent)
        # Requires Python SDK version 1.5.0 or later
        >>> from contextlib import AsyncExitStack
        >>> import lmstudio as lms
        >>> resources = AsyncExitStack()
        >>> client = await resources.enter_async_context(lms.AsyncClient())
        >>> loaded_models = await client.llm.list_loaded()
        >>> for idx, model in enumerate(loaded_models):
        ...     print(f"{idx:>3} {model}")
        ...
          0 AsyncLLM(identifier='qwen2.5-7b-instruct-1m')
        >>> model = loaded_models[0]
        >>> chat = lms.Chat("You answer questions concisely")
        >>> chat.add_user_message("Tell me three fruits")
        UserMessage(content=[TextData(text='Tell me three fruits')])
        >>> print(await model.respond(chat, on_message=chat.append))
        Apple, banana, and orange.
        >>> chat.add_user_message("Tell me three more fruits")
        UserMessage(content=[TextData(text='Tell me three more fruits')])
        >>> print(await model.respond(chat, on_message=chat.append))
        Mango, strawberry, and pineapple.
        >>> chat.add_user_message("How many fruits have you told me?")
        UserMessage(content=[TextData(text='How many fruits have you told me?')])
        >>> print(await model.respond(chat, on_message=chat.append))
        You asked for three fruits initially, then three more, so I've listed six fruits in total.

```
