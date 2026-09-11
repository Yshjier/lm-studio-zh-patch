
你可以用 `getInfo` 方法访问已加载模型的信息。

```lms_code_snippet
  variants:
    LLM:
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";

        const client = new LMStudioClient();
        const model = await client.llm.model();

        const modelInfo = await model.getInfo();

        console.info("Model Key", modelInfo.modelKey);
        console.info("Current Context Length", model.contextLength);
        console.info("Model Trained for Tool Use", modelInfo.trainedForToolUse);
        // etc.
    嵌入模型:
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";

        const client = new LMStudioClient();
        const model = await client.embedding.model();

        const modelInfo = await model.getInfo();

        console.info("Model Key", modelInfo.modelKey);
        console.info("Current Context Length", modelInfo.contextLength);
        // etc.
```
