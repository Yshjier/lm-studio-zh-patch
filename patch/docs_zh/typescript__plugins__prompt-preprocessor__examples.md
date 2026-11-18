
### 示例：注入当前时间

下面是一个预处理器的示例，它在每条用户消息之前注入当前时间。

```lms_code_snippet
  title: "src/promptPreprocessor.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        import { type PromptPreprocessorController, type ChatMessage } from "@lmstudio/sdk";
        export async function preprocess(ctl: PromptPreprocessorController, userMessage: ChatMessage) {
          const textContent = userMessage.getText();
          const transformed = `Current time: ${new Date().toString()}\n\n${textContent}`;
          return transformed;
        }
```

### 示例：替换触发词

另一个只需处理纯文本的例子是替换某些触发词。例如，你可以把 `@init` 触发器替换为一段特殊的初始化消息。

```lms_code_snippet
  title: "src/promptPreprocessor.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        import { type PromptPreprocessorController, type ChatMessage, text } from "@lmstudio/sdk";

        const mySpecialInstructions = text`
          Here are some special instructions...
        `;

        export async function preprocess(ctl: PromptPreprocessorController, userMessage: ChatMessage) {
          const textContent = userMessage.getText();
          const transformed = textContent.replaceAll("@init", mySpecialInstructions);
          return transformed;
        }
```
