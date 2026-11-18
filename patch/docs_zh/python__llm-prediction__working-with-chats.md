
SDK 方法（例如 `llm.respond()`、`llm.applyPromptTemplate()` 或 `llm.act()`）都以一个 chat 参数作为输入。
在使用 SDK 时，有几种表示聊天的方式。

## 方式 1：输入单个字符串

如果你的聊天只有一条单个用户消息，你可以用单个字符串来表示聊天。
以下是用 `.respond` 方法的一个示例。

```lms_code_snippet
variants:
  "Single string":
    language: python
    code: |
      prediction = llm.respond("What is the meaning of life?")
```

## 方式 2：使用 `Chat` 辅助类

对于更复杂的任务，推荐使用 `Chat` 辅助类。
它提供了各种常用方法来管理聊天。
以下是用 `Chat` 类的一个示例，其中初始系统提示词在初始化 chat 实例时提供，
随后通过相应的方法调用添加初始用户消息。

```lms_code_snippet
variants:
  "Simple chat":
    language: python
    code: |
      chat = Chat("You are a resident AI philosopher.")
      chat.add_user_message("What is the meaning of life?")

      prediction = llm.respond(chat)
```

你也可以用 `Chat.from_history` 方法快速构造一个 `Chat` 对象。

```lms_code_snippet
variants:
  "Chat history data":
    language: python
    code: |
      chat = Chat.from_history({"messages": [
        { "role": "system", "content": "You are a resident AI philosopher." },
        { "role": "user", "content": "What is the meaning of life?" },
      ]})

  "Single string":
    language: python
    code: |
      # This constructs a chat with a single user message
      chat = Chat.from_history("What is the meaning of life?")

```

## 方式 3：直接提供聊天历史数据

由于接受聊天历史的 API 在内部使用 `Chat.from_history`，
它们也接受聊天历史数据格式作为普通字典：

```lms_code_snippet
variants:
  "Chat history data":
    language: python
    code: |
      prediction = llm.respond({"messages": [
        { "role": "system", "content": "You are a resident AI philosopher." },
        { "role": "user", "content": "What is the meaning of life?" },
      ]})
```
