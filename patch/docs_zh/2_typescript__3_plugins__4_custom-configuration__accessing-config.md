
你可以分别用 `ctl.getPluginConfig(configSchematics)` 和 `ctl.getGlobalConfig(globalConfigSchematics)` 方法访问配置。

例如，下面是在 promptPreprocessor 中访问配置的写法：

```lms_code_snippet
  title: "src/promptPreprocessor.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        import { type PreprocessorController, type ChatMessage } from "@lmstudio/sdk";
        import { configSchematics } from "./config";

        export async function preprocess(ctl: PreprocessorController, userMessage: ChatMessage) {
          const pluginConfig = ctl.getPluginConfig(configSchematics);
          const myCustomField = pluginConfig.get("myCustomField");

          const globalPluginConfig = ctl.getGlobalPluginConfig(configSchematics);
          const globalMyCustomField = globalPluginConfig.get("myCustomField");

          return (
            `${userMessage.getText()},` +
            `myCustomField: ${myCustomField}, ` +
            `globalMyCustomField: ${globalMyCustomField}`
          );
        }
```
