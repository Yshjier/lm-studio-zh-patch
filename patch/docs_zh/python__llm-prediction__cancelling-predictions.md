
使用流式 API 的一个好处，是能够基于那些无法用
`stopStrings` 或 `maxPredictedTokens` 配置设置来表达的条件，来取消预测请求。

下面的片段展示了如何响应一个应用特定的取消条件（例如轮询
另一个线程设置的事件）来取消请求。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms
        model = lms.llm()

        prediction_stream = model.respond_stream("What is the meaning of life?")
        cancelled = False
        for fragment in prediction_stream:
            if ...: # Cancellation condition will be app specific
                cancelled = True
                prediction_stream.cancel()
                # Note: it is recommended to let the iteration complete,
                # as doing so allows the partial result to be recorded.
                # Breaking the loop *is* permitted, but means the partial result
                # and final prediction stats won't be available to the client
        # The stream allows the prediction result to be retrieved after iteration
        if not cancelled:
            print(prediction_stream.result())

    "Python（作用域资源 API）":
      language: python
      code: |
        import lmstudio as lms

        with lms.Client() as client:
            model = client.llm.model()

            prediction_stream = model.respond_stream("What is the meaning of life?")
            cancelled = False
            for fragment in prediction_stream:
                if ...: # Cancellation condition will be app specific
                    cancelled = True
                    prediction_stream.cancel()
                    # Note: it is recommended to let the iteration complete,
                    # as doing so allows the partial result to be recorded.
                    # Breaking the loop *is* permitted, but means the partial result
                    # and final prediction stats won't be available to the client
            # The stream allows the prediction result to be retrieved after iteration
            if not cancelled:
                print(prediction_stream.result())

    "Python（异步 API）":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        async with lms.AsyncClient() as client:
            model = await client.llm.model()

            prediction_stream = await model.respond_stream("What is the meaning of life?")
            cancelled = False
            async for fragment in prediction_stream:
                if ...: # Cancellation condition will be app specific
                    cancelled = True
                    await prediction_stream.cancel()
                    # Note: it is recommended to let the iteration complete,
                    # as doing so allows the partial result to be recorded.
                    # Breaking the loop *is* permitted, but means the partial result
                    # and final prediction stats won't be available to the client
            # The stream allows the prediction result to be retrieved after iteration
            if not cancelled:
                print(prediction_stream.result())

```
