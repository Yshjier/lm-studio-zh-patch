
LLM 和嵌入模型由于其基础架构，都有一个称为 `context length`（上下文长度）的属性，更确切地说是**最大**上下文长度。粗略地说，这就是模型在生成文本或嵌入时能"记住"多少 token。超过这个上限会导致模型行为异常。

## 在模型对象上使用 `getContextLength()` 函数

能够检查模型的上下文长度很有用，尤其是在向模型提供可能很长的输入之前做额外检查。

```lms_code_snippet
  title: "index.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        const contextLength = await model.getContextLength();
```

上面代码片段中的 `model` 是你从 `llm.model` 方法获得的已加载模型实例。更多信息参见[管理内存中的模型](../manage-models/loading)。

### 示例：检查输入是否能放进模型的上下文窗口

你可以通过以下步骤判断一段对话是否能放进模型的上下文中：

1. 使用提示词模板把对话转换为字符串。
2. 统计该字符串中的 token 数量。
3. 把 token 数量与模型的上下文长度做比较。

```lms_code_snippet
  variants:
    TypeScript:
      language: typescript
      code: |
        import { Chat, type LLM, LMStudioClient } from "@lmstudio/sdk";

        async function doesChatFitInContext(model: LLM, chat: Chat) {
          // Convert the conversation to a string using the prompt template.
          const formatted = await model.applyPromptTemplate(chat);
          // Count the number of tokens in the string.
          const tokenCount = await model.countTokens(formatted);
          // Get the current loaded context length of the model
          const contextLength = await model.getContextLength();
          return tokenCount < contextLength;
        }

        const client = new LMStudioClient();
        const model = await client.llm.model();

        const chat = Chat.from([
          { role: "user", content: "What is the meaning of life." },
          { role: "assistant", content: "The meaning of life is..." },
          // ... More messages
        ]);

        console.info("Fits in context:", await doesChatFitInContext(model, chat));
```
