
## 自动工具调用

我们引入执行"轮次"（round）的概念，用来描述运行一个工具、把其输出提供给 LLM、然后等待 LLM 决定下一步做什么这一组合过程。

**执行轮次**

```
 • run a tool ->
 ↑   • provide the result to the LLM ->
 │       • wait for the LLM to generate a response
 │
 └────────────────────────────────────────┘ └➔ (return)
```

一个模型可能会选择在返回最终结果之前多次运行工具。例如，如果 LLM 在写代码，它可能会选择编译或运行程序、修复错误，然后再运行一次，如此反复，直到得到想要的结果。

基于这一点，我们说 `.act()` API 是一个自动的"多轮"工具调用 API。

### 快速示例

```lms_code_snippet
  variants:
    TypeScript:
      language: typescript
      code: |
        import { LMStudioClient, tool } from "@lmstudio/sdk";
        import { z } from "zod";

        const client = new LMStudioClient();

        const multiplyTool = tool({
          name: "multiply",
          description: "Given two numbers a and b. Returns the product of them.",
          parameters: { a: z.number(), b: z.number() },
          implementation: ({ a, b }) => a * b,
        });

        const model = await client.llm.model("qwen2.5-7b-instruct");
        await model.act("What is the result of 12345 multiplied by 54321?", [multiplyTool], {
          onMessage: (message) => console.info(message.toString()),
        });
```

> **_注意：_** 目前，这段代码需要 zod v3

### 对 LLM 来说"使用工具"意味着什么？

LLM 基本上是文本进、文本出的程序。所以你可能会问"LLM 怎么能使用工具呢？"。答案是：有些 LLM 经过训练，会请求人类替它调用工具，并期望工具的输出以某种格式回传给它。

想象你在通过电话为某人提供电脑技术支持。你可能会说"帮我运行这条命令……好，它输出了什么？……好，现在点那里，然后告诉我它显示了什么……"。在这种情况下，你就是那个 LLM！而你是通过电话另一端的人间接地"调用工具"。

### 重要：模型选择

为工具使用所选的模型会极大影响性能。

选择模型时的一些通用指导：

- 并非所有模型都能进行智能的工具使用
- 越大越好（即，7B 参数模型的表现通常优于 3B 参数模型）
- 我们观察到 [Qwen2.5-7B-Instruct](https://model.lmstudio.ai/download/lmstudio-community/Qwen2.5-7B-Instruct-GGUF) 在各种各样的场景中表现良好
- 此指导可能会变化

### 示例：多个工具

以下代码演示了如何在单次 `.act()` 调用中提供多个工具。

```lms_code_snippet
  variants:
    TypeScript:
      language: typescript
      code: |
        import { LMStudioClient, tool } from "@lmstudio/sdk";
        import { z } from "zod";

        const client = new LMStudioClient();

        const additionTool = tool({
          name: "add",
          description: "Given two numbers a and b. Returns the sum of them.",
          parameters: { a: z.number(), b: z.number() },
          implementation: ({ a, b }) => a + b,
        });

        const isPrimeTool = tool({
          name: "isPrime",
          description: "Given a number n. Returns true if n is a prime number.",
          parameters: { n: z.number() },
          implementation: ({ n }) => {
            if (n < 2) return false;
            const sqrt = Math.sqrt(n);
            for (let i = 2; i <= sqrt; i++) {
              if (n % i === 0) return false;
            }
            return true;
          },
        });

        const model = await client.llm.model("qwen2.5-7b-instruct");
        await model.act(
          "Is the result of 12345 + 45668 a prime? Think step by step.",
          [additionTool, isPrimeTool],
          { onMessage: (message) => console.info(message.toString()) },
        );
```

### 示例：带创建文件工具的聊天循环

以下代码创建了一个与能够创建文件的 LLM 智能体的对话循环。

```lms_code_snippet
  variants:
    TypeScript:
      language: typescript
      code: |
        import { Chat, LMStudioClient, tool } from "@lmstudio/sdk";
        import { existsSync } from "fs";
        import { writeFile } from "fs/promises";
        import { createInterface } from "readline/promises";
        import { z } from "zod";

        const rl = createInterface({ input: process.stdin, output: process.stdout });
        const client = new LMStudioClient();
        const model = await client.llm.model();
        const chat = Chat.empty();

        const createFileTool = tool({
          name: "createFile",
          description: "Create a file with the given name and content.",
          parameters: { name: z.string(), content: z.string() },
          implementation: async ({ name, content }) => {
            if (existsSync(name)) {
              return "Error: File already exists.";
            }
            await writeFile(name, content, "utf-8");
            return "File created.";
          },
        });

        while (true) {
          const input = await rl.question("You: ");
          // Append the user input to the chat
          chat.append("user", input);

          process.stdout.write("Bot: ");
          await model.act(chat, [createFileTool], {
            // When the model finish the entire message, push it to the chat
            onMessage: (message) => chat.append(message),
            onPredictionFragment: ({ content }) => {
              process.stdout.write(content);
            },
          });
          process.stdout.write("\n");
        }
```
