
##### 需要 [LM Studio 0.4.0](/download) 或更高版本。

LM Studio 支持用 API 令牌进行身份验证，提供了一种安全便捷的方式来访问 LM Studio API。

默认情况下，LM Studio API 运行**时不强制身份验证**。对于生产或共享环境，请启用 API 令牌身份验证以实现安全访问。

```lms_info
要启用 API 令牌身份验证、创建令牌并控制细粒度权限，请查看[此指南](/docs/developer/core/authentication)了解详情。
```

## 提供 API 令牌

在创建 `LMStudioClient` 实例时，有两种方式提供 API 令牌：

1. **环境变量（推荐）**：设置 `LM_API_TOKEN` 环境变量，SDK 会自动读取它。
2. **函数参数**：在构造函数中直接把令牌作为 `apiToken` 参数传入。

```lms_code_snippet
  variants:
    "环境变量":
      language: typescript
      code: |
        // Set environment variables in your terminal before running the code:
        // export LM_API_TOKEN="your-token-here"

        import { LMStudioClient } from "@lmstudio/sdk";
        // The SDK automatically reads from LM_API_TOKEN environment variable
        const client = new LMStudioClient();

        const model = await client.llm.model("qwen/qwen3-4b-2507");
        const result = await model.respond("What is the meaning of life?");

        console.info(result.content);
    "函数参数":
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";
        const client = new LMStudioClient({
          apiToken: "your-token-here",
        });

        const model = await client.llm.model("qwen/qwen3-4b-2507");
        const result = await model.respond("What is the meaning of life?");

        console.info(result.content);
```
