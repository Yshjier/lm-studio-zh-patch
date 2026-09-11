
生成器接收生成器控制器和当前对话状态，开始生成，然后通过 `ctl.fragmentGenerated` 方法上报生成的文本。

下面是一个简单生成器的示例，它把最后一条用户消息回显出来，每个单词之间延迟 200 毫秒：

```lms_code_snippet
  title: "src/toolsProvider.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        import { Chat, GeneratorController } from "@lmstudio/sdk";

        export async function generate(ctl: GeneratorController, chat: Chat) {
          // Just echo back the last message
          const lastMessage = chat.at(-1).getText();
          // Split the last message into words
          const words = lastMessage.split(/(?= )/);
          for (const word of words) {
            ctl.fragmentGenerated(word); // Send each word as a fragment
            ctl.abortSignal.throwIfAborted(); // Allow for cancellation
            await new Promise((resolve) => setTimeout(resolve, 200)); // Simulate some processing time
          }
        }
```

## 自定义配置

你可以通过 `ctl.getPluginConfig` 和 `ctl.getGlobalPluginConfig` 访问自定义配置。更多细节参见[自定义配置](./configurations)。

## 处理中止

当你的生成器仍在运行时，用户可能会中止这次预测。这种情况下，你应该通过处理 `ctl.abortSignal` 来优雅地处理中止。

更多关于 `AbortSignal` 的内容参见 [MDN 文档](https://developer.mozilla.org/en-US/docs/Web/API/AbortSignal)。
