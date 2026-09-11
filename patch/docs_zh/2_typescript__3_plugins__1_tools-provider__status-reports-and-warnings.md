
有时一个工具可能需要执行很久。这种情况下，提供状态更新会让用户知道正在发生什么。另一些时候，你可能想就潜在问题向用户发出警告。

你可以使用工具实现函数第二个参数上的 `status` 和 `warn` 方法发送状态更新和警告。

下面的示例展示如何实现一个等待指定秒数的工具，并在等待时间超过 10 秒时提供状态更新和警告：

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

          const waitTool = tool({
            name: `wait`,
            description: "Wait for a specified number of seconds.",
            parameters: { seconds: z.number().min(1) },
            implementation: async ({ seconds }, { status, warn }) => {
              if (seconds > 10) {
                warn("The model asks to wait for more than 10 seconds.");
              }
              for (let i = 0; i < seconds; i++) {
                status(`Waiting... ${i + 1}/${seconds} seconds`);
                await new Promise((resolve) => setTimeout(resolve, 1000));
              }
            },
          });
          tools.push(waitTool);

          return tools; // Return the tools array
        }
```

注意，状态更新和警告只有用户能看到。如果你希望模型也能看到这些消息，应该把它们作为工具返回值的一部分返回。

## 处理中止

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
