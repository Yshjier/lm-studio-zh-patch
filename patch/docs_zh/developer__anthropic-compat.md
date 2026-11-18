
### 支持的端点

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
      <td><code>/v1/messages</code></td>
      <td><apimethod method="POST" /></td>
      <td><a href="/docs/developer/anthropic-compat/messages">消息</a></td>
    </tr>
  </tbody>
</table>

<hr>

## 在 LM Studio 中使用 Claude Code

完整操作指南见：[在 LM Studio 中使用 Claude Code](/docs/integrations/claude-code)。

```bash
export ANTHROPIC_BASE_URL=http://localhost:1234
export ANTHROPIC_AUTH_TOKEN=lmstudio
claude --model openai/gpt-oss-20b
```

## 身份验证请求头

当启用"要求身份验证"时，LM Studio 同时接受 `x-api-key` 和标准的 `Authorization: Bearer <token>` 请求头。要了解如何在 LM Studio 中启用身份验证，请查看[身份验证](/docs/developer/core/authentication)。

## 将 base URL 指向 LM Studio

把你的 Anthropic 客户端（或任意 HTTP 请求）指向本地 LM Studio 服务器。

注意：以下示例假设服务器端口为 `1234`。

### cURL 示例

```diff
- curl https://api.anthropic.com/v1/messages \
+ curl http://localhost:1234/v1/messages \
   -H "Content-Type: application/json" \
+  -H "x-api-key: $LM_API_TOKEN" \
   -d '{
-    "model": "claude-4-5-sonnet",
+    "model": "ibm/granite-4-micro",
     "max_tokens": 256,
     "messages": [
       {"role": "user", "content": "Write a haiku about local LLMs."}
     ]
   }'
```

### Python 示例

```python
from anthropic import Anthropic

client = Anthropic(
    base_url="http://localhost:1234",
    api_key="lmstudio",
)

message = client.messages.create(
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": "Hello from LM Studio",
        }
    ],
    model="ibm/granite-4-micro",
)

print(message.content)
```

如果你未启用"要求身份验证"，则 `x-api-key` 请求头是可选的。
对于 Python 示例，当身份验证被禁用时，你也可以省略 `api_key`。

如果你遇到问题，欢迎加入我们的 [Discord](https://discord.gg/lmstudio) 并进入开发者频道。
