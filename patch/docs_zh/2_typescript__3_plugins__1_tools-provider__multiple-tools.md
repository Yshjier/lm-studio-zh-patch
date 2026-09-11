
一个工具提供者可以为模型定义多个工具。只需再创建额外的工具实例，并把它们加入 tools 数组即可。

下面的示例中，我们再添加一个用于读取文件内容的工具：

```lms_code_snippet
  title: "src/toolsProvider.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        import { tool, Tool, ToolsProviderController } from "@lmstudio/sdk";
        import { z } from "zod";
        import { existsSync } from "fs";
        import { readFile, writeFile } from "fs/promises";
        import { join } from "path";

        export async function toolsProvider(ctl: ToolsProviderController) {
          const tools: Tool[] = [];

          const createFileTool = tool({
            name: `create_file`,
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
          tools.push(createFileTool); // First tool

          const readFileTool = tool({
            name: `read_file`,
            description: "Read the content of a file with the given name.",
            parameters: { file_name: z.string() },
            implementation: async ({ file_name }) => {
              const filePath = join(ctl.getWorkingDirectory(), file_name);
              if (!existsSync(filePath)) {
                return "Error: File does not exist.";
              }
              const content = await readFile(filePath, "utf-8");
              return content;
            },
          });
          tools.push(readFileTool); // Second tool

          return tools; // Return the tools array
        }
```
