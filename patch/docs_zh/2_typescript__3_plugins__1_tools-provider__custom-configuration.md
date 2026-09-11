
你可以为工具提供者添加自定义配置项，这样插件的使用者无需修改代码就能定制其行为。

在下面的示例中，我们会请用户指定一个文件夹名称，然后在工作目录中的该文件夹内创建文件。

首先，在 `config.ts` 中添加配置字段：

```lms_code_snippet
  title: "src/config.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        export const configSchematics = createConfigSchematics()
          .field(
            "folderName", // Key of the configuration field
            "string", // Type of the configuration field
            {
              displayName: "Folder Name",
              subtitle: "The name of the folder where files will be created.",
            },
            "default_folder", // Default value
          )
          .build();
```

```lms_info
在这个示例中，我们把字段加到了 `configSchematics`，也就是“按聊天”的配置。如果你想添加一个在不同聊天之间共享的全局配置字段，应该把它加到同一文件中 `globalConfigSchematics` 段落下面。

更多关于配置的内容参见[自定义配置](../plugins/configurations)。
```

然后，修改工具提供者以使用这个配置值：

```lms_code_snippet
  title: "src/toolsProvider.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        import { tool, Tool, ToolsProviderController } from "@lmstudio/sdk";
        import { existsSync } from "fs";
        import { mkdir, writeFile } from "fs/promises";
        import { join } from "path";
        import { z } from "zod";
        import { configSchematics } from "./config";

        export async function toolsProvider(ctl: ToolsProviderController) {
          const tools: Tool[] = [];

          const createFileTool = tool({
            name: `create_file`,
            description: "Create a file with the given name and content.",
            parameters: { file_name: z.string(), content: z.string() },
            implementation: async ({ file_name, content }) => {
              // Read the config field
              const folderName = ctl.getPluginConfig(configSchematics).get("folderName");
              const folderPath = join(ctl.getWorkingDirectory(), folderName);

              // Ensure the folder exists
              await mkdir(folderPath, { recursive: true });

              // Create the file
              const filePath = join(folderPath, file_name);
              if (existsSync(filePath)) {
                return "Error: File already exists.";
              }
              await writeFile(filePath, content, "utf-8");
              return "File created.";
            },
          });
          tools.push(createFileTool); // First tool

          return tools; // Return the tools array
        }
```
