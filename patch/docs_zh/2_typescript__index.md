
SDK 为你提供了一组编程工具，用于与 LLM、嵌入模型和智能体流程交互。

## 安装 SDK

`lmstudio-js` 以 npm 包的形式提供。你可以使用 npm、yarn 或 pnpm 安装它。

```lms_code_snippet
  variants:
    npm:
      language: bash
      code: |
        npm install @lmstudio/sdk --save
    yarn:
      language: bash
      code: |
        yarn add @lmstudio/sdk
    pnpm:
      language: bash
      code: |
        pnpm add @lmstudio/sdk
```

源码与开源贡献请访问 GitHub 上的 [lmstudio-js](https://github.com/lmstudio-ai/lmstudio-js)。

## 功能

- 使用 LLM [在聊天中回复](./typescript/llm-prediction/chat-completion) 或预测[文本补全](./typescript/llm-prediction/completion)
- 将函数定义为工具，把 LLM 变成完全本地运行的[自主智能体](./typescript/agent/act)
- 从内存中[加载](./typescript/manage-models/loading)、[配置](./typescript/llm-prediction/parameters)和[卸载](./typescript/manage-models/loading)模型
- 同时支持浏览器和任何兼容 Node 的环境
- 为文本生成嵌入，等等！

## 快速示例：与 Llama 模型聊天

```lms_code_snippet
  title: "index.ts"
  variants:
    TypeScript:
      language: typescript
      code: |
        import { LMStudioClient } from "@lmstudio/sdk";
        const client = new LMStudioClient();

        const model = await client.llm.model("qwen/qwen3-4b-2507");
        const result = await model.respond("What is the meaning of life?");

        console.info(result.content);
```

### 获取本地模型

上面的代码需要 [qwen3-4b-2507](https://lmstudio.ai/models/qwen/qwen3-4b-2507)。如果你没有该模型，请在终端中运行以下命令来下载它。

```bash
lms get qwen/qwen3-4b-2507
```

在 LM Studio 的 CLI [文档中](./cli/get)了解关于 `lms get` 的更多内容。
