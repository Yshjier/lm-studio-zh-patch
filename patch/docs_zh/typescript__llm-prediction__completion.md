
使用 `llm.complete(...)` 从已加载的语言模型生成文本补全。文本补全指：向模型发送一个未经格式化处理的字符串，期望模型补完这段文本。

这与多轮聊天对话不同。关于聊天补全的更多信息，参见[聊天补全](./chat-completion)。

## 1. 实例化模型

首先，你需要加载一个模型来生成补全。这可以使用 `llm` 句柄上的 `model` 方法来完成。

```lms_code_snippet
  title: "index.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";

        const client = new LMStudioClient();
        const model = await client.llm.model("qwen2.5-7b-instruct");
```

## 2. 生成补全

一旦你有了一个已加载的模型，就可以通过向 `llm` 句柄上的 `complete` 方法传入一个字符串来生成补全。

```lms_code_snippet
  variants:
    "流式":
      language: typescript
      code: |
        const completion = model.complete("My name is", {
          maxTokens: 100,
        });

        for await (const { content } of completion) {
          process.stdout.write(content);
        }

        console.info(); // Write a new line for cosmetic purposes

    "非流式":
      language: typescript
      code: |
        const completion = await model.complete("My name is", {
          maxTokens: 100,
        });

        console.info(completion.content);
```

## 3. 打印预测统计信息

你也可以打印预测元数据，例如用于生成的模型、生成的 token 数、首个 token 耗时以及停止原因。

```lms_code_snippet
  title: "index.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        console.info("Model used:", completion.modelInfo.displayName);
        console.info("Predicted tokens:", completion.stats.predictedTokensCount);
        console.info("Time to first token (seconds):", completion.stats.timeToFirstTokenSec);
        console.info("Stop reason:", completion.stats.stopReason);
```

## 示例：让 LLM 模拟终端

以下是一个你可能会用 `complete` 方法来模拟终端的示例。

```lms_code_snippet
  title: "terminal-sim.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";
        import { createInterface } from "node:readline/promises";

        const rl = createInterface({ input: process.stdin, output: process.stdout });
        const client = new LMStudioClient();
        const model = await client.llm.model();
        let history = "";

        while (true) {
          const command = await rl.question("$ ");
          history += "$ " + command + "\n";

          const prediction = model.complete(history, { stopStrings: ["$"] });
          for await (const { content } of prediction) {
            process.stdout.write(content);
          }
          process.stdout.write("\n");

          const { content } = await prediction.result();
          history += content;
        }
```

<!-- ## Advanced Usage

### Prediction metadata

Prediction responses are really returned as `PredictionResult` objects that contain additional dot-accessible metadata about the inference request.
This entails info about the model used, the configuration with which it was loaded, and the configuration for this particular prediction. It also provides
inference statistics like stop reason, time to first token, tokens per second, and number of generated tokens.

Please consult your specific SDK to see exact syntax.

### Progress callbacks

TODO: TS has onFirstToken callback which Python does not

Long prompts will often take a long time to first token, i.e. it takes the model a long time to process your prompt.
If you want to get updates on the progress of this process, you can provide a float callback to `complete`
that receives a float from 0.0-1.0 representing prompt processing progress.

```lms_code_snippet
  variants:
    Python:
      language: python
      code: |
        import lmstudio as lm

        llm = lm.llm()

        completion = llm.complete(
            "My name is",
            on_progress: lambda progress: print(f"{progress*100}% complete")
        )

    "Python（使用作用域资源）":
      language: python
      code: |
        import lmstudio

        with lmstudio.Client() as client:
            llm = client.llm.model()

            completion = llm.complete(
                "My name is",
                on_progress: lambda progress: print(f"{progress*100}% processed")
            )

    TypeScript:
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";

        const client = new LMStudioClient();
        const llm = await client.llm.model();

        const prediction = llm.complete(
          "My name is",
          {onPromptProcessingProgress: (progress) => process.stdout.write(`${progress*100}% processed`)});
```

### Prediction configuration

You can also specify the same prediction configuration options as you could in the
in-app chat window sidebar. Please consult your specific SDK to see exact syntax. -->
