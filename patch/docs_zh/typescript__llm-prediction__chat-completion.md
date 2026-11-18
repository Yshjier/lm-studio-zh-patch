
使用 `llm.respond(...)` 为一轮聊天对话生成补全。

## 快速示例：生成聊天回复

下面的片段展示了如何流式输出 AI 对一个简短聊天提示词的回复。

```lms_code_snippet
  title: "index.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";
        const client = new LMStudioClient();

        const model = await client.llm.model();

        for await (const fragment of model.respond("What is the meaning of life?")) {
          process.stdout.write(fragment.content);
        }
```

## 获取模型

首先，你需要获取一个模型句柄。这可以使用 `llm` 命名空间中的 `model` 方法来完成。例如，以下是如何使用 Qwen2.5 7B Instruct。

```lms_code_snippet
  title: "index.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";
        const client = new LMStudioClient();

        const model = await client.llm.model("qwen2.5-7b-instruct");
```

还有其他获取模型句柄的方式。更多信息参见[在内存中管理模型](./../manage-models/loading)。

## 管理聊天上下文

模型的输入被称为"上下文"。从概念上讲，模型接收一轮多轮对话作为输入，并被要求预测该对话中助手的回复。

```lms_code_snippet
  variants:
    "使用消息数组":
      language: typescript
      code: |
        import { Chat } from "@lmstudio/sdk";

        // Create a chat object from an array of messages.
        const chat = Chat.from([
          { role: "system", content: "You are a resident AI philosopher." },
          { role: "user", content: "What is the meaning of life?" },
        ]);
    "构造 Chat 对象":
      language: typescript
      code: |
        import { Chat } from "@lmstudio/sdk";

        // Create an empty chat object.
        const chat = Chat.empty();

        // Build the chat context by appending messages.
        chat.append("system", "You are a resident AI philosopher.");
        chat.append("user", "What is the meaning of life?");
```

关于管理聊天上下文的更多信息，参见[使用聊天](./working-with-chats)。

<!-- , and [`Chat`](./../api-reference/chat) for API reference for the `Chat` class. -->

## 生成回复

你可以用 `respond()` 方法让 LLM 预测聊天上下文中的下一个回复。

```lms_code_snippet
  variants:
    "流式":
      language: typescript
      code: |
        // The `chat` object is created in the previous step.
        const prediction = model.respond(chat);

        for await (const { content } of prediction) {
          process.stdout.write(content);
        }

        console.info(); // Write a new line to prevent text from being overwritten by your shell.

    "非流式":
      language: typescript
      code: |
        // The `chat` object is created in the previous step.
        const result = await model.respond(chat);

        console.info(result.content);
```

## 自定义推理参数

你可以把推理参数作为第二个参数传给 `.respond()`。

```lms_code_snippet
  variants:
    "流式":
      language: typescript
      code: |
        const prediction = model.respond(chat, {
          temperature: 0.6,
          maxTokens: 50,
        });

    "非流式":
      language: typescript
      code: |
        const result = await model.respond(chat, {
          temperature: 0.6,
          maxTokens: 50,
        });
```

关于可配置内容的更多信息，参见[配置模型](./parameters)。

## 打印预测统计信息

你也可以打印预测元数据，例如用于生成的模型、生成的
token 数、首个 token 耗时以及停止原因。

```lms_code_snippet
  variants:
    "流式":
      language: typescript
      code: |
        // If you have already iterated through the prediction fragments,
        // doing this will not result in extra waiting.
        const result = await prediction.result();

        console.info("Model used:", result.modelInfo.displayName);
        console.info("Predicted tokens:", result.stats.predictedTokensCount);
        console.info("Time to first token (seconds):", result.stats.timeToFirstTokenSec);
        console.info("Stop reason:", result.stats.stopReason);
    "非流式":
      language: typescript
      code: |
        // `result` is the response from the model.
        console.info("Model used:", result.modelInfo.displayName);
        console.info("Predicted tokens:", result.stats.predictedTokensCount);
        console.info("Time to first token (seconds):", result.stats.timeToFirstTokenSec);
        console.info("Stop reason:", result.stats.stopReason);
```

## 示例：多轮聊天

<!-- TODO: Probably needs polish here: -->

```lms_code_snippet
  variants:
    TypeScript:
      language: typescript
      code: |
        import { Chat, LMStudioClient } from "@lmstudio/sdk";
        import { createInterface } from "readline/promises";

        const rl = createInterface({ input: process.stdin, output: process.stdout });
        const client = new LMStudioClient();
        const model = await client.llm.model();
        const chat = Chat.empty();

        while (true) {
          const input = await rl.question("You: ");
          // Append the user input to the chat
          chat.append("user", input);

          const prediction = model.respond(chat, {
            // When the model finish the entire message, push it to the chat
            onMessage: (message) => chat.append(message),
          });
          process.stdout.write("Bot: ");
          for await (const { content } of prediction) {
            process.stdout.write(content);
          }
          process.stdout.write("\n");
        }
```

<!-- ### Progress callbacks

TODO: Cover onFirstToken callback (Python SDK has this now)

Long prompts will often take a long time to first token, i.e. it takes the model a long time to process your prompt.
If you want to get updates on the progress of this process, you can provide a float callback to `respond`
that receives a float from 0.0-1.0 representing prompt processing progress.

```lms_code_snippet
  variants:
    Python:
      language: python
      code: |
        import lmstudio as lm

        llm = lm.llm()

        response = llm.respond(
            "What is LM Studio?",
            on_progress: lambda progress: print(f"{progress*100}% complete")
        )

    "Python（使用作用域资源）":
      language: python
      code: |
        import lmstudio

        with lmstudio.Client() as client:
            llm = client.llm.model()

            response = llm.respond(
                "What is LM Studio?",
                on_progress: lambda progress: print(f"{progress*100}% processed")
            )

    TypeScript:
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";

        const client = new LMStudioClient();
        const llm = await client.llm.model();

        const prediction = llm.respond(
          "What is LM Studio?",
          {onPromptProcessingProgress: (progress) => process.stdout.write(`${progress*100}% processed`)});
```

### Prediction configuration

You can also specify the same prediction configuration options as you could in the
in-app chat window sidebar. Please consult your specific SDK to see exact syntax. -->
