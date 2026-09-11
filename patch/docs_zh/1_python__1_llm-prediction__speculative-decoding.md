
_要求的 Python SDK 版本_：**1.2.0**

推测解码是一种能显著提升大语言模型（LLM）生成速度、同时不降低回复质量的技术。更多信息参见[推测解码](./../../app/advanced/speculative-decoding)。

要在 `lmstudio-python` 中使用推测解码，只需在执行预测时提供一个 `draftModel` 参数。你无需单独加载草稿模型。

```lms_code_snippet
  variants:
    "非流式":
      language: python
      code: |
        import lmstudio as lms

        main_model_key = "qwen2.5-7b-instruct"
        draft_model_key = "qwen2.5-0.5b-instruct"

        model = lms.llm(main_model_key)
        result = model.respond(
            "What are the prime numbers between 0 and 100?",
            config={
                "draftModel": draft_model_key,
            }
        )

        print(result)
        stats = result.stats
        print(f"Accepted {stats.accepted_draft_tokens_count}/{stats.predicted_tokens_count} tokens")


    "流式":
      language: python
      code: |
        import lmstudio as lms

        main_model_key = "qwen2.5-7b-instruct"
        draft_model_key = "qwen2.5-0.5b-instruct"

        model = lms.llm(main_model_key)
        prediction_stream = model.respond_stream(
            "What are the prime numbers between 0 and 100?",
            config={
                "draftModel": draft_model_key,
            }
        )
        for fragment in prediction_stream:
            print(fragment.content, end="", flush=True)
        print() # Advance to a new line at the end of the response

        stats = prediction_stream.result().stats
        print(f"Accepted {stats.accepted_draft_tokens_count}/{stats.predicted_tokens_count} tokens")
```
