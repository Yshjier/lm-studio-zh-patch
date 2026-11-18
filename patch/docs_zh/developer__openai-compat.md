
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
      <td><code>/v1/models</code></td>
      <td><apimethod method="GET" /></td>
      <td><a href="/docs/developer/openai-compat/models">模型</a></td>
    </tr>
    <tr>
      <td><code>/v1/responses</code></td>
      <td><apimethod method="POST" /></td>
      <td><a href="/docs/developer/openai-compat/responses">响应</a></td>
    </tr>
    <tr>
      <td><code>/v1/chat/completions</code></td>
      <td><apimethod method="POST" /></td>
      <td><a href="/docs/developer/openai-compat/chat-completions">聊天补全</a></td>
    </tr>
    <tr>
      <td><code>/v1/embeddings</code></td>
      <td><apimethod method="POST" /></td>
      <td><a href="/docs/developer/openai-compat/embeddings">嵌入</a></td>
    </tr>
    <tr>
      <td><code>/v1/completions</code></td>
      <td><apimethod method="POST" /></td>
      <td><a href="/docs/developer/openai-compat/completions">补全</a></td>
    </tr>
  </tbody>
</table>

<hr>

## 将 `base url` 指向 LM Studio

你可以复用现有的 OpenAI 客户端（Python、JS、C# 等），只需把 "base URL" 属性改为指向你的 LM Studio，而不是 OpenAI 的服务器。

注意：以下示例假设服务器端口为 `1234`

### Python 示例

```diff
from openai import OpenAI

client = OpenAI(
+    base_url="http://localhost:1234/v1"
)

# ... the rest of your code ...
```

### Typescript 示例

```diff
import OpenAI from 'openai';

const client = new OpenAI({
+  baseUrl: "http://localhost:1234/v1"
});

// ... the rest of your code ...
```

### cURL 示例

```diff
- curl https://api.openai.com/v1/chat/completions \
+ curl http://localhost:1234/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
-     "model": "gpt-4o-mini",
+     "model": "use the model identifier from LM Studio here",
     "messages": [{"role": "user", "content": "Say this is a test!"}],
     "temperature": 0.7
   }'
```

## 在 LM Studio 中使用 Codex

之所以支持 Codex，是因为 LM Studio 实现了 OpenAI 兼容的 `POST /v1/responses` 端点。

参见：[在 LM Studio 中使用 Codex](/docs/integrations/codex) 和[响应](/docs/developer/openai-compat/responses)。

---

其他 OpenAI 客户端库应该也有类似的选项来设置 base URL。

如果你遇到问题，欢迎加入我们的 [Discord](https://discord.gg/lmstudio) 并进入 `#🔨-developers` 频道。
