
当你的工具仍在运行时，用户可能会中止这次预测。这种情况下，你应该通过处理传入工具实现函数第二个参数的 `AbortSignal` 对象，来优雅地处理中止。

```lms_code_snippet
  title: "src/toolsProvider.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        import { tool, Tool, ToolsProviderController } from "@lmstudio/sdk";
        import { z } from "zod";

        export async function toolsProvider(ctl: ToolsProviderController) {
          const tools: Tool[] = [];

          const fetchTool = tool({
            name: `fetch`,
            description: "Fetch a URL using GET method.",
            parameters: { url: z.string() },
            implementation: async ({ url }, { signal }) => {
              const response = await fetch(url, {
                method: "GET",
                signal, // <-- Here, we pass the signal to fetch to allow cancellation
              });
              if (!response.ok) {
                return `Error: Failed to fetch ${url}: ${response.statusText}`;
              }
              const data = await response.text();
              return {
                status: response.status,
                headers: Object.fromEntries(response.headers.entries()),
                data: data.substring(0, 1000), // Limit to 1000 characters
              };
            },
          });
          tools.push(fetchTool);

          return tools;
        }
```

更多关于 `AbortSignal` 的内容参见 [MDN 文档](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal)。
