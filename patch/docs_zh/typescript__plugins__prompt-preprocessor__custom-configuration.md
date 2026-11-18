
你可以通过 `ctl.getPluginConfig` 和 `ctl.getGlobalPluginConfig` 访问自定义配置。更多细节参见[自定义配置](./configurations)。

下面是一个示例，展示如何让 `specialInstructions` 和 `triggerWord` 变成可配置的：

首先，在 `config.ts` 中添加配置字段：

```lms_code_snippet
  title: "src/config.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        import { createConfigSchematics } from "@lmstudio/sdk";
        export const configSchematics = createConfigSchematics()
          .field(
            "specialInstructions",
            "string",
            {
              displayName: "Special Instructions",
              subtitle: "Special instructions to be injected when the trigger word is found.",
            },
            "Here is some default special instructions.",
          )
          .field(
            "triggerWord",
            "string",
            {
              displayName: "Trigger Word",
              subtitle: "The word that will trigger the special instructions.",
            },
            "@init",
          )
          .build();
```

```lms_info
在这个示例中，我们把字段加到了 `configSchematics`，也就是“按聊天”的配置。如果你想添加一个在不同聊天之间共享的全局配置字段，应该把它加到同一文件中 `globalConfigSchematics` 段落下面。

更多关于配置的内容参见[自定义配置](../plugins/configurations)。
```

然后，修改提示词预处理器以使用该配置：

```lms_code_snippet
  title: "src/promptPreprocessor.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        import { type PromptPreprocessorController, type ChatMessage } from "@lmstudio/sdk";
        import { configSchematics } from "./config";

        export async function preprocess(ctl: PromptPreprocessorController, userMessage: ChatMessage) {
          const textContent = userMessage.getText();
          const pluginConfig = ctl.getPluginConfig(configSchematics);

          const triggerWord = pluginConfig.get("triggerWord");
          const specialInstructions = pluginConfig.get("specialInstructions");

          const transformed = textContent.replaceAll(triggerWord, specialInstructions);
          return transformed;
        }
```
