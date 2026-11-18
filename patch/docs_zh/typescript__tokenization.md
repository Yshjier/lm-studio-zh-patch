模型使用分词器在内部把文本转换为更易处理的“词元”（token）。LM Studio 对外提供该分词器以供使用。

## 分词

可以使用 SDK，对已加载的 LLM 或嵌入模型分词某个字符串。在下面的示例中，`llm` 可以替换为嵌入模型 `emb`。

```typescript
import { LMStudioClient } from "@lmstudio/sdk";

const client = new LMStudioClient();
const model = await client.llm.model();

const tokens = await model.tokenize("Hello, world!");

console.info(tokens); // Array of token IDs.
```

## 统计词元数

如果只关心词元数量，可以改用 `.countTokens` 方法。

```typescript
const tokenCount = await model.countTokens("Hello, world!");
console.info("Token count:", tokenCount);
```

### 示例：统计上下文

可以按以下步骤判断给定对话是否能放入模型上下文：

1. 使用提示词模板把对话转换为字符串。
2. 统计该字符串的词元数量。
3. 把词元数与模型上下文长度对比。

```typescript
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

<!-- ### Context length comparisons

The below examples check whether a conversation is over a LLM's context length
(replace `llm` with `emb` to check for an embedding model).

```typescript
import { LMStudioClient, Chat } from "@lmstudio/sdk";

const client = new LMStudioClient();
const llm = await client.llm.model();

// To check for a string, simply tokenize
var tokens = await llm.tokenize("Hello, world!");

// To check for a Chat, apply the prompt template first
const chat = Chat.createEmpty().withAppended("user", "Hello, world!");
const templatedChat = await llm.applyPromptTemplate(chat);
tokens = await llm.tokenize(templatedChat);

// If the prompt's length in tokens is less than the context length, you're good!
const contextLength = await llm.getContextLength()
const isOkay = (tokens.length < contextLength)
``` -->
