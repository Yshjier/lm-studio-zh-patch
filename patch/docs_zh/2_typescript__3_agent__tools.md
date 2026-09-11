
你可以用 `tool()` 函数定义工具，并在 `act()` 调用中把它们传给模型。

## 工具的构成

按以下标准格式把函数定义为工具：

```lms_code_snippet
  title: "index.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        import { tool } from "@lmstudio/sdk";
        import { z } from "zod";

        const exampleTool = tool({
          // The name of the tool
          name: "add",

          // A description of the tool
          description: "Given two numbers a and b. Returns the sum of them.",

          // zod schema of the parameters
          parameters: { a: z.number(), b: z.number() },

          // The implementation of the tool. Just a regular function.
          implementation: ({ a, b }) => a + b,
        });
```

**重要**：工具的名称、描述以及参数定义都会被传给模型！

这意味着你的措辞会影响生成的质量。请务必始终为工具提供清晰的描述，以便模型知道如何使用它。

## 具有外部效应的工具（如操作电脑或调用 API）

工具还可以具有外部效应，例如创建文件、调用程序甚至 API。通过实现具有外部效应的工具，
你基本上可以把 LLM 变成能在你本机上执行任务的自主智能体。

## 示例：`createFileTool`

### 工具定义

```lms_code_snippet
  title: "createFileTool.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        import { tool } from "@lmstudio/sdk";
        import { existsSync } from "fs";
        import { writeFile } from "fs/promises";
        import { z } from "zod";

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
```

### 使用 `createFile` 工具的示例代码：

```lms_code_snippet
  title: "index.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";
        import { createFileTool } from "./createFileTool";

        const client = new LMStudioClient();

        const model = await client.llm.model("qwen2.5-7b-instruct");
        await model.act(
          "Please create a file named output.txt with your understanding of the meaning of life.",
          [createFileTool],
        );
```
