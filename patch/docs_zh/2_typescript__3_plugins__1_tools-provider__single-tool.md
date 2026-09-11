
要设置工具提供者，首先在插件的 `src` 目录中创建文件 `toolsProvider.ts`：

```lms_code_snippet
  title: "src/toolsProvider.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        import { tool, Tool, ToolsProviderController } from "@lmstudio/sdk";
        import { z } from "zod";
        import { existsSync } from "fs";
        import { writeFile } from "fs/promises";
        import { join } from "path";

        export async function toolsProvider(ctl: ToolsProviderController) {
          const tools: Tool[] = [];

          const createFileTool = tool({
            // Name of the tool, this will be passed to the model. Aim for concise, descriptive names
            name: `create_file`,
            // Your description here, more details will help the model to understand when to use the tool
            description: "Create a file with the given name and content.",
            parameters: { file_name: z.string(), content: z.string() },
            implementation: async ({ file_name, content }) => {
              const filePath = join(ctl.getWorkingDirectory(), file_name);
              if (existsSync(filePath)) {
                return "Error: File already exists.";
              }
              await writeFile(filePath, content, "utf-8");
              return "File created.";
            },
          });
          tools.push(createFileTool);

          return tools;
        }
```

上面的工具提供者定义了一个名为 `create_file` 的工具，让模型可以在工作目录中按指定名称和内容创建文件。关于工具定义的更多内容，参见[工具定义](../agent/tools)。

然后在插件的 `index.ts` 中注册这个工具提供者：

```lms_code_snippet
  title: "src/index.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        // ... other imports ...
        import { toolsProvider } from "./toolsProvider";

        export async function main(context: PluginContext) {
          // ... other plugin setup code ...

          // Register the tools provider.
          context.withToolsProvider(toolsProvider); // <-- Register the tools provider

          // ... other plugin setup code ...
        }
```

现在，你可以试着让 LLM 创建一个文件，它应该能用你刚刚创建的工具完成。

## 提示

- **使用有描述性的名称和说明**：定义工具时，请使用有描述性的名称和详细的说明。这有助于模型理解何时以及如何有效地使用每个工具。
- **把错误作为字符串返回**：有时模型在调用工具时可能出错。这种情况下，你可以把错误信息作为字符串返回。多数情况下，模型会尝试自我纠正，并用正确的参数再次调用该工具。
