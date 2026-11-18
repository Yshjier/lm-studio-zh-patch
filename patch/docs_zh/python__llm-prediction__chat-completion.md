
使用 `llm.respond(...)` 为一轮聊天对话生成补全。

## 快速示例：生成聊天回复

下面的片段展示了如何获取 AI 对一个简短聊天提示词的回复。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        model = lms.llm()
        print(model.respond("What is the meaning of life?"))

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
            model = client.llm.model()
            print(model.respond("What is the meaning of life?"))

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.AsyncClient() as client:
            model = await client.llm.model()
            print(await model.respond("What is the meaning of life?"))

```

## 流式输出聊天回复

下面的片段展示了如何流式输出 AI 对一个聊天提示词的回复，
在收到文本片段时就显示它们（而不是等整个回复生成完毕后才显示任何内容）。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms
        model = lms.llm()

        for fragment in model.respond_stream("What is the meaning of life?"):
            print(fragment.content, end="", flush=True)
        print() # Advance to a new line at the end of the response

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
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

        async with lms.AsyncClient() as client:
            model = await client.llm.model()

            async for fragment in model.respond_stream("What is the meaning of life?"):
                print(fragment.content, end="", flush=True)
            print() # Advance to a new line at the end of the response

```

## 取消聊天回复

关于如何取消进行中的预测，参见[取消预测](./cancelling-predictions)一节。

## 获取模型

首先，你需要获取一个模型句柄。
这可以使用顶层的 `llm` 便捷 API 来完成，
也可以在使用作用域资源 API 时，通过 `llm` 命名空间中的 `model` 方法完成。
例如，以下是如何使用 Qwen2.5 7B Instruct。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        model = lms.llm("qwen2.5-7b-instruct")

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
            model = client.llm.model("qwen2.5-7b-instruct")

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.AsyncClient() as client:
            model = await client.llm.model("qwen2.5-7b-instruct")

```

还有其他获取模型句柄的方式。更多信息参见[在内存中管理模型](./../manage-models/loading)。

## 管理聊天上下文

模型的输入被称为"上下文"。
从概念上讲，模型接收一轮多轮对话作为输入，
并被要求预测该对话中助手的回复。

```lms_code_snippet
  variants:
    "构造 Chat 对象":
      language: python
      code: |
        import lmstudio as lms

        # Create a chat with an initial system prompt.
        chat = lms.Chat("You are a resident AI philosopher.")

        # Build the chat context by adding messages of relevant types.
        chat.add_user_message("What is the meaning of life?")
        # ... continued in next example

  "From chat history data":
      language: python
      code: |
        import lmstudio as lms

        # Create a chat object from a chat history dict
        chat = lms.Chat.from_history({
            "messages": [
                { "role": "system", "content": "You are a resident AI philosopher." },
                { "role": "user", "content": "What is the meaning of life?" },
            ]
        })
        # ... continued in next example

```

关于管理聊天上下文的更多信息，参见[使用聊天](./working-with-chats)。

<!-- , and [`Chat`](./../api-reference/chat) for API reference for the `Chat` class. -->

## 生成回复

你可以用 `respond()` 方法让 LLM 预测聊天上下文中的下一个回复。

```lms_code_snippet
  variants:
    "非流式（同步 API）":
      language: python
      code: |
        # The `chat` object is created in the previous step.
        result = model.respond(chat)

        print(result)

    "流式（同步 API）":
      language: python
      code: |
        # The `chat` object is created in the previous step.
        prediction_stream = model.respond_stream(chat)

        for fragment in prediction_stream:
            print(fragment.content, end="", flush=True)
        print() # Advance to a new line at the end of the response

    "非流式（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        # The `chat` object is created in the previous step.
        result = await model.respond(chat)

        print(result)

    "流式（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        # The `chat` object is created in the previous step.
        prediction_stream = await model.respond_stream(chat)

        async for fragment in prediction_stream:
            print(fragment.content, end="", flush=True)
        print() # Advance to a new line at the end of the response

```

## 自定义推理参数

你可以通过 `.respond()` 上的 `config` 关键字参数传入推理参数。

```lms_code_snippet
  variants:
    "非流式（同步 API）":
      language: python
      code: |
        result = model.respond(chat, config={
            "temperature": 0.6,
            "maxTokens": 50,
        })

    "流式（同步 API）":
      language: python
      code: |
        prediction_stream = model.respond_stream(chat, config={
            "temperature": 0.6,
            "maxTokens": 50,
        })

    "非流式（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        result = await model.respond(chat, config={
            "temperature": 0.6,
            "maxTokens": 50,
        })

    "流式（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        prediction_stream = await model.respond_stream(chat, config={
            "temperature": 0.6,
            "maxTokens": 50,
        })

```

关于可配置内容的更多信息，参见[配置模型](./parameters)。

## 打印预测统计信息

你也可以打印预测元数据，例如用于生成的模型、生成的
token 数、首个 token 耗时以及停止原因。

```lms_code_snippet
  variants:
    "非流式":
      language: python
      code: |
        # `result` is the response from the model.
        print("Model used:", result.model_info.display_name)
        print("Predicted tokens:", result.stats.predicted_tokens_count)
        print("Time to first token (seconds):", result.stats.time_to_first_token_sec)
        print("Stop reason:", result.stats.stop_reason)

    "流式":
      language: python
      code: |
        # After iterating through the prediction fragments,
        # the overall prediction result may be obtained from the stream
        result = prediction_stream.result()

        print("Model used:", result.model_info.display_name)
        print("Predicted tokens:", result.stats.predicted_tokens_count)
        print("Time to first token (seconds):", result.stats.time_to_first_token_sec)
        print("Stop reason:", result.stats.stop_reason)

```

非流式和流式的结果访问在同步与异步 API 之间都是一致的，
因为 `prediction_stream.result()` 是一个非阻塞 API，如果结果尚不可用
（要么因为预测仍在运行，要么因为预测请求失败），它会抛出异常。预测流还提供了一个
阻塞（同步 API）或可等待（异步 API）的 `prediction_stream.wait_for_result()` 方法，
它在内部会先把流迭代到完成，然后返回结果。

## 示例：多轮聊天

```lms_code_snippet
  title: "chatbot.py"
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        model = lms.llm()
        chat = lms.Chat("You are a task focused AI assistant")

        while True:
            try:
                user_input = input("You (leave blank to exit): ")
            except EOFError:
                print()
                break
            if not user_input:
                break
            chat.add_user_message(user_input)
            prediction_stream = model.respond_stream(
                chat,
                on_message=chat.append,
            )
            print("Bot: ", end="", flush=True)
            for fragment in prediction_stream:
                print(fragment.content, end="", flush=True)
            print()

```

### 进度回调

长提示词往往会让首个 token 的耗时很长，也就是模型需要花很长时间来处理你的提示词。
如果你想获取这一过程进度的更新，可以给 `respond` 提供一个浮点回调，
它接收一个 0.0-1.0 的浮点数，表示提示词处理进度。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        llm = lms.llm()

        response = llm.respond(
            "What is LM Studio?",
            on_prompt_processing_progress = (lambda progress: print(f"{progress*100}% complete")),
        )

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
            llm = client.llm.model()

            response = llm.respond(
                "What is LM Studio?",
                on_prompt_processing_progress = (lambda progress: print(f"{progress*100}% complete")),
            )

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.AsyncClient() as client:
            llm = await client.llm.model()

            response = await llm.respond(
                "What is LM Studio?",
                on_prompt_processing_progress = (lambda progress: print(f"{progress*100}% complete")),
            )


```

除了 `on_prompt_processing_progress` 之外，其他可用的进度回调还有：

- `on_first_token`：在提示词处理完成、首个 token 正在发出之后调用。
  不接收任何参数（使用流式迭代 API 或 `on_prediction_fragment`
  来在 token 发出时处理它们）。
- `on_prediction_fragment`：对客户端收到的每个预测片段调用。
  接收的预测片段与迭代流式迭代 API 时相同。
- `on_message`：在预测完成时，用一个助手回复消息调用。
  用于把收到的消息追加到一个聊天历史实例。
