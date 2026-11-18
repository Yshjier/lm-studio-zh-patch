SDK 提供一组编程工具，用于与 LLM、嵌入模型及智能体流程交互。

## 安装 SDK

`lmstudio-js` 以 npm 包形式发布，可以用 npm、yarn 或 pnpm 安装。

```lms_code_snippet
variants:
  npm:
    language: bash
    code: npm install @lmstudio/sdk --save
  yarn:
    language: bash
    code: yarn add @lmstudio/sdk
  pnpm:
    language: bash
    code: pnpm add @lmstudio/sdk

```

源码与开源贡献请访问 GitHub 上的 [lmstudio-js](https://github.com/lmstudio-ai/lmstudio-js)。

## 功能

* 使用 LLM 在[对话中回复](/docs/typescript/llm-prediction/chat-completion)或预测[文本补全](/docs/typescript/llm-prediction/completion)
* 把函数定义为工具，将 LLM 变成完全在本地运行的[自主智能体](/docs/typescript/agent/act)
* 从内存中[加载](/docs/typescript/manage-models/loading)、[配置](/docs/typescript/llm-prediction/parameters)和[卸载](/docs/typescript/manage-models/loading)模型
* 同时支持浏览器和任意 Node 兼容环境
* 为文本生成嵌入向量等更多能力！

## 快速示例：与 Llama 模型对话

```typescript title="index.ts"
import { LMStudioClient } from "@lmstudio/sdk";
const client = new LMStudioClient();

const model = await client.llm.model("qwen/qwen3-4b-2507");
const result = await model.respond("What is the meaning of life?");

console.info(result.content);
```

### 获取本地模型

上面的代码需要 [qwen3-4b-2507](/models/qwen/qwen3-4b-2507)。如果还没有该模型，在终端运行以下命令下载。

```bash
lms get qwen/qwen3-4b-2507
```

关于 `lms get` 的更多说明，见 LM Studio CLI [此处](/docs/cli/local-models/get)。
