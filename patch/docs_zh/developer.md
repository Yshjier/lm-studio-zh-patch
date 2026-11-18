
```lms_hstack
## 了解这套技术栈

- TypeScript SDK：[lmstudio-js](/docs/typescript)
- Python SDK：[lmstudio-python](/docs/python)
- LM Studio REST API：[有状态对话、通过 API 使用 MCP](/docs/developer/rest)
- 兼容 OpenAI：[对话、响应、嵌入](/docs/developer/openai-compat)
- 兼容 Anthropic：[消息](/docs/developer/anthropic-compat)
- LM Studio CLI：[`lms`](/docs/cli)

:::split:::

## 你可以构建什么

- 带流式输出的对话与文本生成
- 通过 MCP 进行工具调用与本地智能体
- 结构化输出（JSON schema）
- 嵌入与分词
- 模型管理（加载、下载、列出）
```

## 为无头部署安装 `llmster`

`llmster` 是 LM Studio 的核心，被打包为守护进程，用于在服务器、云实例或 CI 上进行无头部署。该守护进程独立运行，不依赖 LM Studio 图形界面。

**Mac / Linux**

```bash
curl -fsSL https://lmstudio.ai/install.sh | bash
```

**Windows**

```powershell
irm https://lmstudio.ai/install.ps1 | iex
```

**基本用法**

```bash
lms daemon up          # Start the daemon
lms get <model>        # Download a model
lms server start       # Start the local server
lms chat               # Open an interactive session
```

了解更多：[无头部署](/blog/0.4.0#deploy-on-servers-deploy-in-ci-deploy-anywhere)

## 极速上手

### TypeScript（`lmstudio-js`）

```bash
npm install @lmstudio/sdk
```

```ts
import { LMStudioClient } from "@lmstudio/sdk";

const client = new LMStudioClient();
const model = await client.llm.model("openai/gpt-oss-20b");
const result = await model.respond("Who are you, and what can you do?");

console.info(result.content);
```

完整文档：[lmstudio-js](/docs/typescript)，源码：[GitHub](https://github.com/lmstudio-ai/lmstudio-js)

### Python（`lmstudio-python`）

```bash
pip install lmstudio
```

```python
import lmstudio as lms

with lms.Client() as client:
    model = client.llm.model("openai/gpt-oss-20b")
    result = model.respond("Who are you, and what can you do?")
    print(result)
```

完整文档：[lmstudio-python](/docs/python)，源码：[GitHub](https://github.com/lmstudio-ai/lmstudio-python)

### HTTP（LM Studio REST API）

```bash
lms server start --port 1234
```

```bash
curl http://localhost:1234/api/v1/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $LM_API_TOKEN" \
  -d '{
    "model": "openai/gpt-oss-20b",
    "input": "Who are you, and what can you do?"
  }'
```

完整文档：[LM Studio REST API](/docs/developer/rest)

## 实用链接

- [API 更新日志](/docs/developer/api-changelog)
- [本地服务器基础](/docs/developer/core/server)
- [CLI 参考](/docs/cli)
- [Discord 社区](https://discord.gg/lmstudio)
