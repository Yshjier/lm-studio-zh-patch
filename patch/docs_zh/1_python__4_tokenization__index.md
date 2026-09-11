
模型使用分词器把文本在内部转换成它们能更容易处理的"token"。LM Studio 把这个分词器暴露出来以供实用。

## 分词

你可以用 SDK 对一个字符串进行分词，使用已加载的 LLM 或嵌入模型。
在下面的示例中，可以把 LLM 引用替换为
嵌入模型引用，而无需任何其他改动。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        import lmstudio as lms

        model = lms.llm()

        tokens = model.tokenize("Hello, world!")

        print(tokens) # Array of token IDs.
```

## 统计 token 数

如果你只关心 token 的数量，只需检查结果数组的长度。

```lms_code_snippet
  variants:
    "Python（便捷 API）":
      language: python
      code: |
        token_count = len(model.tokenize("Hello, world!"))
        print("Token count:", token_count)
```

### 示例：统计上下文

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
