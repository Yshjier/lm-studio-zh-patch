模型使用分词器在内部把文本转换为更易处理的“词元”（token）。LM Studio 对外提供该分词器以供使用。

## 分词

可以使用 SDK，对已加载的 LLM 或嵌入模型分词某个字符串。
在下面的示例中，LLM 引用可以替换为嵌入模型引用，无需其他改动。

```python
import lmstudio as lms

model = lms.llm()

tokens = model.tokenize("Hello, world!")

print(tokens) # Array of token IDs.
```

## 统计词元数

如果只关心词元数量，直接检查所得数组的长度即可。

```python
token_count = len(model.tokenize("Hello, world!"))
print("Token count:", token_count)
```

### 示例：判断是否放入上下文

可以按以下步骤判断给定对话是否能放入模型上下文：

1. 使用提示词模板把对话转换为字符串。
2. 统计该字符串的词元数量。
3. 把词元数与模型上下文长度对比。

```python
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
