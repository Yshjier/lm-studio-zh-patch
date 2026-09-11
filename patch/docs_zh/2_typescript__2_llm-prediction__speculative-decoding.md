
推测解码是一种能显著提升大语言模型（LLM）生成速度、同时不降低回复质量的技术。更多信息参见[推测解码](./../../app/advanced/speculative-decoding)。

要在 `lmstudio-js` 中使用推测解码，只需在执行预测时提供一个 `draftModel` 参数。你无需单独加载草稿模型。

```lms_code_snippet
  variants:
    "非流式":
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";

        const client = new LMStudioClient();

        const mainModelKey = "qwen2.5-7b-instruct";
        const draftModelKey = "qwen2.5-0.5b-instruct";

        const model = await client.llm.model(mainModelKey);
        const result = await model.respond("What are the prime numbers between 0 and 100?", {
          draftModel: draftModelKey,
        });

        const { content, stats } = result;
        console.info(content);
        console.info(`Accepted ${stats.acceptedDraftTokensCount}/${stats.predictedTokensCount} tokens`);


    "流式":
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";

        const client = new LMStudioClient();

        const mainModelKey = "qwen2.5-7b-instruct";
        const draftModelKey = "qwen2.5-0.5b-instruct";

        const model = await client.llm.model(mainModelKey);
        const prediction = model.respond("What are the prime numbers between 0 and 100?", {
          draftModel: draftModelKey,
        });

        for await (const { content } of prediction) {
          process.stdout.write(content);
        }
        process.stdout.write("\n");

        const { stats } = await prediction.result();
        console.info(`Accepted ${stats.acceptedDraftTokensCount}/${stats.predictedTokensCount} tokens`);
```
