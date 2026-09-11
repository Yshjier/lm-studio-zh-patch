
有时你可能想在预测完成之前中止它。例如，用户可能改变主意，或者你的界面可能导航到别处。`lmstudio-js` 提供了两种简单的方式来取消正在运行的预测。

## 1. 在预测上调用 `.cancel()`

每个预测方法都返回一个 `OngoingPrediction` 实例。调用 `.cancel()` 会停止生成，并使最终的 `stopReason` 为 `"userStopped"`。在下面的示例中，我们把取消调用安排在一个计时器上：

```lms_code_snippet
  variants:
    TypeScript:
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";

        const client = new LMStudioClient();
        const model = await client.llm.model("qwen2.5-7b-instruct");

        const prediction = model.respond("What is the meaning of life?", {
          maxTokens: 50,
        });
        setTimeout(() => prediction.cancel(), 1000); // cancel after 1 second

        const result = await prediction.result();
        console.info(result.stats.stopReason); // "userStopped"
```

## 2. 使用 `AbortController`

如果你的应用已经在使用 `AbortController` 来传播取消，你可以把它的 `signal` 传给预测方法。中止该控制器会以相同的 `stopReason` 停止预测：

```lms_code_snippet
  variants:
    TypeScript:
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";

        const client = new LMStudioClient();
        const model = await client.llm.model("qwen2.5-7b-instruct");

        const controller = new AbortController();
        const prediction = model.respond("What is the meaning of life?", {
          maxTokens: 50,
          signal: controller.signal,
        });
        setTimeout(() => controller.abort(), 1000); // cancel after 1 second

        const result = await prediction.result();
        console.info(result.stats.stopReason); // "userStopped"
```

两种方式都会立即停止生成，而返回的统计信息表明该预测因为你停止了它而结束。
