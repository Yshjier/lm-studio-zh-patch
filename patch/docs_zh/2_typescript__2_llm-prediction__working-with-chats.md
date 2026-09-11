
SDK 方法（例如 `model.respond()`、`model.applyPromptTemplate()` 或 `model.act()`）
以一个 chat 参数作为输入。在 SDK 中有几种表示聊天的方式。

## 方式 1：消息数组

你可以用一组消息数组来表示聊天。以下是用 `.respond()` 方法的一个示例。

```lms_code_snippet
variants:
  "Text-only":
    language: typescript
    code: |
      const prediction = model.respond([
        { role: "system", content: "You are a resident AI philosopher." },
        { role: "user", content: "What is the meaning of life?" },
      ]);
  With Images:
    language: typescript
    code: |
      const image = await client.files.prepareImage("/path/to/image.jpg");

      const prediction = model.respond([
        { role: "system", content: "You are a state-of-art object recognition system." },
        { role: "user", content: "What is this object?", images: [image] },
      ]);
```

## 方式 2：输入单个字符串

如果你的聊天只有一条单个用户消息，你可以用单个字符串来表示聊天。以下是用 `.respond` 方法的一个示例。

```lms_code_snippet
variants:
  TypeScript:
    language: typescript
    code: |
      const prediction = model.respond("What is the meaning of life?");
```

## 方式 3：使用 `Chat` 辅助类

对于更复杂的任务，推荐使用 `Chat` 辅助类。它提供了各种常用方法来管理聊天。以下是用 `Chat` 类的一个示例。

```lms_code_snippet
variants:
  "Text-only":
    language: typescript
    code: |
      const chat = Chat.empty();
      chat.append("system", "You are a resident AI philosopher.");
      chat.append("user", "What is the meaning of life?");

      const prediction = model.respond(chat);
  With Images:
    language: typescript
    code: |
      const image = await client.files.prepareImage("/path/to/image.jpg");

      const chat = Chat.empty();
      chat.append("system", "You are a state-of-art object recognition system.");
      chat.append("user", "What is this object?", { images: [image] });

      const prediction = model.respond(chat);
```

你也可以用 `Chat.from` 方法快速构造一个 `Chat` 对象。

```lms_code_snippet
variants:
  "Array of messages":
    language: typescript
    code: |
      const chat = Chat.from([
        { role: "system", content: "You are a resident AI philosopher." },
        { role: "user", content: "What is the meaning of life?" },
      ]);
  "Single string":
    language: typescript
    code: |
      // This constructs a chat with a single user message
      const chat = Chat.from("What is the meaning of life?");
```
