
你可以用 `listLoaded` 方法遍历已加载到内存中的模型。该方法位于 `LMStudioClient` 对象的 `llm` 和 `embedding` 命名空间下。

## 列出当前已加载到内存中的模型

这会给你等效于在 CLI 中使用 [`lms ps`](../../cli/ps) 的结果。

```lms_code_snippet
  variants:
    TypeScript:
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";

        const client = new LMStudioClient();

        const llmOnly = await client.llm.listLoaded();
        const embeddingOnly = await client.embedding.listLoaded();
```

<!-- Learn more about `client.llm` namespace in the [API Reference](../api-reference/llm-namespace). -->
