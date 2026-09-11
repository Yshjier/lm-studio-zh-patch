
默认情况下，插件脚手架会在 `src/` 目录下创建一个 `config.ts` 文件，其中包含配置的 schema。如果该文件不存在，你可以手动创建：

```lms_code_snippet
  title: "src/toolsProvider.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        import { createConfigSchematics } from "@lmstudio/sdk";

        export const configSchematics = createConfigSchematics()
          .field(
            "myCustomField", // The key of the field.
            "numeric", // Type of the field.
            // Options for the field. Different field types will have different options.
            {
              displayName: "My Custom Field",
              hint: "This is my custom field. Doesn't do anything special.",
              slider: { min: 0, max: 100, step: 1 }, // Add a slider to the field.
            },
            80, // Default Value
          )
          // You can add more fields by chaining the field method.
          // For example:
          //   .field("anotherField", ...)
          .build();

        export const globalConfigSchematics = createConfigSchematics()
          .field(
            "myGlobalCustomField", // The key of the field.
            "string",
            {
              displayName: "My Global Custom Field",
              hint: "This is my global custom field. Doesn't do anything special.",
            },
            "default value", // Default Value
          )
          // You can add more fields by chaining the field method.
          // For example:
          //  .field("anotherGlobalField", ...)
          .build();
```

如果你是手动添加配置 schema 的，还需要在插件的 `index.ts` 文件中注册这些配置。

具体做法是在插件的 `main` 函数中调用 `context.withConfigSchematics(configSchematics)` 和 `context.withGlobalConfigSchematics(globalConfigSchematics)`。

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

          // Register the configuration schematics.
          context.withConfigSchematics(configSchematics);
          // Register the global configuration schematics.
          context.withGlobalConfigSchematics(globalConfigSchematics);

          // ... other plugin setup code ...
        }
```
