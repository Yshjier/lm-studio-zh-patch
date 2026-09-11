
你可以从 LM Studio 的「开发者」标签页在本机 `localhost` 或网络上提供本地 LLM 服务。

LM Studio 的 API 可以通过 [REST API](/docs/developer/rest)、客户端库（如 [lmstudio-js](/docs/typescript) 和 [lmstudio-python](/docs/python)），以及兼容端点（如 [OpenAI 兼容](/docs/developer/openai-compat) 和 [Anthropic 兼容](/docs/developer/anthropic-compat)）来使用。

<img src="/assets/marketing/docs/server.png" style="" data-caption="从 LM Studio 加载并提供 LLM 服务" />

### 运行服务器

要运行服务器，请进入 LM Studio 的「开发者」标签页，打开「启动服务器」开关即可启动 API 服务器。

<img src="/assets/marketing/docs/server-start.png" style="" data-caption="启动 LM Studio API 服务器" />

或者，你也可以使用 `lms`（[LM Studio 的 CLI](/docs/cli)）从终端启动服务器：

```bash
lms server start
```

### API 选项

- [LM Studio REST API](/docs/developer/rest)
- [TypeScript SDK](/docs/typescript) - `lmstudio-js`
- [Python SDK](/docs/python) - `lmstudio-python`
- [OpenAI 兼容端点](/docs/developer/openai-compat)
- [Anthropic 兼容端点](/docs/developer/anthropic-compat)
