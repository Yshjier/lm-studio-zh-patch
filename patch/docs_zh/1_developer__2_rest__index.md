
LM Studio 提供功能强大的 REST API，对本地推理和模型管理提供一流的支持。除了我们的原生 API 之外，我们还提供 OpenAI 兼容端点（[了解更多](/docs/developer/openai-compat)）和 Anthropic 兼容端点（[了解更多](/docs/developer/anthropic-compat)）。

## 新特性

此前存在一个 [v0 REST API](/docs/developer/rest/endpoints)。随着 LM Studio 0.4.0 发布，我们正式推出了位于 `/api/v1/*` 端点的原生 v1 REST API，并推荐使用它。

v1 REST API 包含以下增强特性：

- [通过 API 使用 MCP](/docs/developer/core/mcp)
- [有状态聊天](/docs/developer/rest/stateful-chats)
- 使用 API 令牌的[身份验证](/docs/developer/core/authentication)配置
- 模型[下载](/docs/developer/rest/download)、[加载](/docs/developer/rest/load)和[卸载](/docs/developer/rest/unload)端点

## 支持的端点

LM Studio 的 v1 REST API 提供以下端点。

<table class="flexible-cols">
  <thead>
    <tr>
      <th>端点</th>
      <th>方法</th>
      <th>文档</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><code>/api/v1/chat</code></td>
      <td><apimethod method="POST" /></td>
      <td><a href="/docs/developer/rest/chat">聊天</a></td>
    </tr>
    <tr>
      <td><code>/api/v1/models</code></td>
      <td><apimethod method="GET" /></td>
      <td><a href="/docs/developer/rest/list">列出模型</a></td>
    </tr>
    <tr>
      <td><code>/api/v1/models/load</code></td>
      <td><apimethod method="POST" /></td>
      <td><a href="/docs/developer/rest/load">加载</a></td>
    </tr>
    <tr>
        <td><code>/api/v1/models/unload</code></td>
        <td><apimethod method="POST" /></td>
        <td><a href="/docs/developer/rest/unload">卸载</a></td>
    </tr>
    <tr>
      <td><code>/api/v1/models/download</code></td>
      <td><apimethod method="POST" /></td>
      <td><a href="/docs/developer/rest/download">下载</a></td>
    </tr>
    <tr>
      <td><code>/api/v1/models/download/status</code></td>
      <td><apimethod method="GET" /></td>
      <td><a href="/docs/developer/rest/download-status">下载状态</a></td>
    </tr>
  </tbody>
</table>

## 推理端点对比

下表对比了 LM Studio 的 `/api/v1/chat` 端点与 OpenAI 兼容、Anthropic 兼容推理端点的功能。

<table class="flexible-cols">
  <thead>
    <tr>
      <th>特性</th>
      <th><a href="/docs/developer/rest/chat"><code>/api/v1/chat</code></a></th>
      <th><a href="/docs/developer/openai-compat/responses"><code>/v1/responses</code></a></th>
      <th><a href="/docs/developer/openai-compat/chat-completions"><code>/v1/chat/completions</code></a></th>
      <th><a href="/docs/developer/anthropic-compat/messages"><code>/v1/messages</code></a></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>流式输出</td>
      <td>✅</td>
      <td>✅</td>
      <td>✅</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>有状态聊天</td>
      <td>✅</td>
      <td>✅</td>
      <td>❌</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>远程 MCP</td>
      <td>✅</td>
      <td>✅</td>
      <td>❌</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>你已在 LM Studio 中配置的 MCP</td>
      <td>✅</td>
      <td>✅</td>
      <td>❌</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>自定义工具</td>
      <td>❌</td>
      <td>✅</td>
      <td>✅</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>在请求中包含助手消息</td>
      <td>❌</td>
      <td>✅</td>
      <td>✅</td>
      <td>✅</td>
    </tr>
    <tr>
      <td>模型加载流式事件</td>
      <td>✅</td>
      <td>❌</td>
      <td>❌</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>提示处理流式事件</td>
      <td>✅</td>
      <td>❌</td>
      <td>❌</td>
      <td>❌</td>
    </tr>
    <tr>
      <td>在请求中指定上下文长度</td>
      <td>✅</td>
      <td>❌</td>
      <td>❌</td>
      <td>❌</td>
    </tr>
  </tbody>
</table>

---

如遇 bug，请在 [Github](https://github.com/lmstudio-ai/lmstudio-bug-tracker/issues) 上提交 issue。
