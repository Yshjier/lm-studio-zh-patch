
LLM 和嵌入模型由于其基础架构，都有一个称为 `context length`（上下文长度）的属性，更具体地说是一个**最大**上下文长度。粗略地说，这就是模型在生成文本或嵌入时能"记住"多少 token。超过这个上限会导致模型行为异常。

## 在模型对象上使用 `get_context_length()` 函数

能够检查一个模型的上下文长度是很有用的，尤其是在向模型提供可能很长的输入之前作为一项额外检查。

```lms_code_snippet
  title: "example.py"
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        context_length = model.get_context_length()
```

上面代码片段中的 `model` 是你从 `llm.model` 方法获得的已加载模型实例。更多信息参见[在内存中管理模型](../manage-models/loading)。

### 示例：检查输入能否放入模型的上下文窗口

你可以通过以下步骤判断一段给定对话能否放入模型的上下文：

1. 使用提示词模板把对话转换为一个字符串。
2. 统计该字符串中的 token 数量。
3. 把 token 数量与模型的上下文长度进行比较。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        def does_chat_fit_in_context(model: lms.LLM, chat: lms.Chat) -> bool:
            # Convert the conversation to a string using the prompt template.
            formatted = model.apply_prompt_template(chat)
            # Count the number of tokens in the string.
            token_count = len(model.tokenize(formatted))
            # Get the current loaded context length of the model
            context_length = model.get_context_length()
            return token_count < context_length

        model = lms.llm()

        chat = lms.Chat.from_history({
            "messages": [
                { "role": "user", "content": "What is the meaning of life." },
                { "role": "assistant", "content": "The meaning of life is..." },
                # ... More messages
            ]
        })

        print("Fits in context:", does_chat_fit_in_context(model, chat))

```
