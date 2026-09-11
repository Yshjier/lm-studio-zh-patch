
AI 模型体积巨大，加载进内存可能需要一些时间。LM Studio 的 SDK 允许你精确控制这个过程。

**最常用的方式：**

- 用 `.model()` 获取当前已加载的任意模型
- 用 `.model("model-key")` 使用某个指定模型

**进阶（手动管理模型）：**

- 用 `.load("model-key")` 加载一个模型的新实例
- 用 `model.unload()` 把模型从内存中卸载

## 用 `.model()` 获取当前模型

如果你已经在 LM Studio 中加载了模型（通过图形界面或 `lms load`），可以直接调用不带参数的 `.model()` 来使用它。

```lms_code_snippet
  variants:
    TypeScript:
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";
        const client = new LMStudioClient();

        const model = await client.llm.model();
```

## 用 `.model("model-key")` 获取指定模型

如果你想使用某个特定模型，可以把模型标识符作为参数传给 `.model()`。

#### 已加载则获取，未加载则加载

调用 `.model("model-key")` 时，如果模型尚未加载，它会加载该模型；如果已经加载，则返回现有实例。

```lms_code_snippet
  variants:
    TypeScript:
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";
        const client = new LMStudioClient();

        const model = await client.llm.model("qwen/qwen3-4b-2507");
```

<!-- Learn more about the `.model()` method and the parameters it accepts in the [API Reference](../api-reference/model). -->

## 用 `.load()` 加载一个模型的新实例

使用 `load()` 可以加载一个模型的新实例，即使该模型已经存在实例。这样你可以同时加载同一个模型的多个实例，或同时加载多个不同模型。

```lms_code_snippet
  variants:
    TypeScript:
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";
        const client = new LMStudioClient();

        const llama = await client.llm.load("qwen/qwen3-4b-2507");
        const another_llama = await client.llm.load("qwen/qwen3-4b-2507", {
          identifier: "second-llama"
        });
```

<!-- Learn more about the `.load()` method and the parameters it accepts in the [API Reference](../api-reference/load). -->

### 关于实例标识符

如果你提供的实例标识符已经存在，服务器会抛出错误。
所以如果你并不在意具体标识符，最好不要自己指定，而是让服务器自动生成一个。你随时可以在 LM Studio 的服务器选项卡中查看！

## 用 `.unload()` 把模型从内存中卸载

当你不再需要某个模型时，只需对它的句柄调用 `unload()` 即可卸载。

```lms_code_snippet
  variants:
    TypeScript:
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";

        const client = new LMStudioClient();

        const model = await client.llm.model();
        await model.unload();
```

## 设置自定义加载配置参数

加载模型时，你也可以指定与加载相关的配置选项，例如上下文长度和 GPU 卸载。

更多内容参见[加载时配置](../llm-prediction/parameters)。

## 设置自动卸载计时器（TTL）

你可以为加载的模型指定一个 _存活时间_（time to live），即最后一次请求之后的空闲秒数，超过该时间后模型会被卸载。更多内容参见 [空闲 TTL](/docs/api/ttl-and-auto-evict)。

```lms_code_snippet
  variants:
    "使用 .load":
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";

        const client = new LMStudioClient();

        const model = await client.llm.load("qwen/qwen3-4b-2507", {
          ttl: 300, // 300 seconds
        });
    "使用 .model":
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";

        const client = new LMStudioClient();

        const model = await client.llm.model("qwen/qwen3-4b-2507", {
          // Note: specifying ttl in `.model` will only set the TTL for the model if the model is
          // loaded from this call. If the model was already loaded, the TTL will not be updated.
          ttl: 300, // 300 seconds
        });
```
