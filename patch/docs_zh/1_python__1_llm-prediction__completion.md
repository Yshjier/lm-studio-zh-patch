
使用 `llm.complete(...)` 从已加载的语言模型生成文本补全。
文本补全指：向模型发送一个未经格式化处理的字符串，期望模型补完这段文本。

这与多轮聊天对话不同。关于聊天补全的更多信息，参见[聊天补全](./chat-completion)。

## 1. 实例化模型

首先，你需要加载一个模型来生成补全。
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

## 2. 生成补全

一旦你有了一个已加载的模型，就可以通过向 `llm` 句柄上的 `complete` 方法传入一个字符串来生成补全。

```lms_code_snippet
  variants:
    "非流式（同步 API）":
      language: python
      code: |
        # The `chat` object is created in the previous step.
        result = model.complete("My name is", config={"maxTokens": 100})

        print(result)

    "流式（同步 API）":
      language: python
      code: |
        # The `chat` object is created in the previous step.
        prediction_stream = model.complete_stream("My name is", config={"maxTokens": 100})

        for fragment in prediction_stream:
            print(fragment.content, end="", flush=True)
        print() # Advance to a new line at the end of the response

    "非流式（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        # The `chat` object is created in the previous step.
        result = await model.complete("My name is", config={"maxTokens": 100})

        print(result)

    "流式（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        # The `chat` object is created in the previous step.
        prediction_stream = await model.complete_stream("My name is", config={"maxTokens": 100})

        async for fragment in prediction_stream:
            print(fragment.content, end="", flush=True)
        print() # Advance to a new line at the end of the response

```

## 3. 打印预测统计信息

你也可以打印预测元数据，例如用于生成的模型、生成的 token 数、首个 token 耗时以及停止原因。

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

## 示例：让 LLM 模拟终端

以下是一个你可能会用 `complete` 方法来模拟终端的示例。

```lms_code_snippet
  title: "terminal-sim.py"
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        model = lms.llm()
        console_history = []

        while True:
            try:
                user_command = input("$ ")
            except EOFError:
                print()
                break
            if user_command.strip() == "exit":
                break
            console_history.append(f"$ {user_command}")
            history_prompt = "\n".join(console_history)
            prediction_stream = model.complete_stream(
                history_prompt,
                config={ "stopStrings": ["$"] },
            )
            for fragment in prediction_stream:
                print(fragment.content, end="", flush=True)
            print()
            console_history.append(prediction_stream.result().content)

```

## 自定义推理参数

你可以通过 `.complete()` 上的 `config` 关键字参数传入推理参数。

```lms_code_snippet
  variants:
    "非流式（同步 API）":
      language: python
      code: |
        result = model.complete(initial_text, config={
            "temperature": 0.6,
            "maxTokens": 50,
        })

    "流式（同步 API）":
      language: python
      code: |
        prediction_stream = model.complete_stream(initial_text, config={
            "temperature": 0.6,
            "maxTokens": 50,
        })

    "非流式（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        result = await model.complete(initial_text, config={
            "temperature": 0.6,
            "maxTokens": 50,
        })

    "流式（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        prediction_stream = await model.complete_stream(initial_text, config={
            "temperature": 0.6,
            "maxTokens": 50,
        })

```

关于可配置内容的更多信息，参见[配置模型](./parameters)。

### 进度回调

长提示词往往会让首个 token 的耗时很长，也就是模型需要花很长时间来处理你的提示词。
如果你想获取这一过程进度的更新，可以给 `complete` 提供一个浮点回调，
它接收一个 0.0-1.0 的浮点数，表示提示词处理进度。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        llm = lms.llm()

        completion = llm.complete(
            "My name is",
            on_prompt_processing_progress = (lambda progress: print(f"{progress*100}% complete")),
        )

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
            llm = client.llm.model()

            completion = llm.complete(
                "My name is",
                on_prompt_processing_progress = (lambda progress: print(f"{progress*100}% processed")),
            )

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.AsyncClient() as client:
            llm = await client.llm.model()

            completion = await llm.complete(
                "My name is",
                on_prompt_processing_progress = (lambda progress: print(f"{progress*100}% processed")),
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
