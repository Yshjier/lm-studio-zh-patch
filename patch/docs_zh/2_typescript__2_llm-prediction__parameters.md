
你可以为模型同时自定义推理时参数和加载时参数。推理参数可以按请求逐次设置，而加载参数在加载模型时设置。

# 推理参数

设置推理时参数，例如 `temperature`、`maxTokens`、`topP` 等。

```lms_code_snippet
  variants:
    ".respond()":
      language: typescript
      code: |
        const prediction = model.respond(chat, {
          temperature: 0.6,
          maxTokens: 50,
        });
    ".complete()":
        language: typescript
        code: |
          const prediction = model.complete(prompt, {
            temperature: 0.6,
            maxTokens: 50,
            stop: ["\n\n"],
          });
```

关于所有可配置字段，参见 [`LLMPredictionConfigInput`](./../api-reference/llm-prediction-config-input)。

另一个有用的推理时配置参数是 [`structured`](<(./structured-responses)>)，它让你可以用 JSON 或 zod schema 严格强制输出的结构。

# 加载参数

设置加载时参数，例如上下文长度、GPU 卸载比例等。

### 用 `.model()` 设置加载参数

`.model()` 会获取一个已加载模型的句柄，或按需加载一个新模型（JIT 加载）。

**注意**：如果模型已经加载，该配置将被**忽略**。

```lms_code_snippet
  variants:
    TypeScript:
      language: typescript
      code: |
        const model = await client.llm.model("qwen2.5-7b-instruct", {
          config: {
            contextLength: 8192,
            gpu: {
              ratio: 0.5,
            },
          },
        });
```

关于所有可配置字段，参见 [`LLMLoadModelConfig`](./../api-reference/llm-load-model-config)。

### 用 `.load()` 设置加载参数

`.load()` 方法会创建一个新的模型实例，并用指定的配置加载它。

```lms_code_snippet
  variants:
    TypeScript:
      language: typescript
      code: |
        const model = await client.llm.load("qwen2.5-7b-instruct", {
          config: {
            contextLength: 8192,
            gpu: {
              ratio: 0.5,
            },
          },
        });
```

关于所有可配置字段，参见 [`LLMLoadModelConfig`](./../api-reference/llm-load-model-config)。
