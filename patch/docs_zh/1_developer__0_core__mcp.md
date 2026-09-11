
##### 需要 [LM Studio 0.4.0](/download) 或更高版本。

LM Studio 支持通过 API 使用模型上下文协议（MCP）。MCP 允许模型通过标准化的服务器与外部工具和服务交互。

## 工作原理

MCP 服务器提供模型可在聊天请求期间调用的工具。你可以通过两种方式启用 MCP 服务器：作为每次请求定义的临时服务器，或作为 `mcp.json` 文件中预配置的服务器。

## 临时服务器与 mcp.json 服务器

<table class="flexible-cols">
  <thead>
    <tr>
      <th>特性</th>
      <th>临时（Ephemeral）</th>
      <th>mcp.json</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>如何在请求中指定</td>
      <td><code>integrations</code> -> <code>"type": "ephemeral_mcp"</code></td>
      <td><code>integrations</code> -> <code>"type": "plugin"</code></td>
    </tr>
    <tr>
      <td>配置方式</td>
      <td>仅在每次请求中定义</td>
      <td>在 <code>mcp.json</code> 中预配置</td>
    </tr>
    <tr>
      <td>使用场景</td>
      <td>一次性请求、远程 MCP 工具执行</td>
      <td>需要 <code>command</code> 的 MCP 服务器、经常使用的服务器</td>
    </tr>
    <tr>
      <td>服务器 ID</td>
      <td>通过集成中的 <code>server_label</code> 指定</td>
      <td>通过集成中的 <code>id</code> 指定（例如 <code>mcp/playwright</code>）</td>
    </tr>
    <tr>
      <td>自定义请求头</td>
      <td>通过 <code>headers</code> 字段支持</td>
      <td>在 <code>mcp.json</code> 中配置</td>
    </tr>
  </tbody>
</table>

## 临时 MCP 服务器

临时 MCP 服务器在每次请求中即时定义。这适用于测试，或你不想预先配置服务器的场景。

```lms_info
临时 MCP 服务器需要先在[服务器设置](/docs/developer/core/server/settings)中启用"允许每次请求的 MCP"。
```

```lms_code_snippet
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/chat \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "ibm/granite-4-micro",
          "input": "What is the top trending model on hugging face?",
          "integrations": [
            {
              "type": "ephemeral_mcp",
              "server_label": "huggingface",
              "server_url": "https://huggingface.co/mcp",
              "allowed_tools": ["model_search"]
            }
          ],
          "context_length": 8000
        }'
  Python:
    language: python
    code: |
      import os
      import requests
      import json

      response = requests.post(
        "http://localhost:1234/api/v1/chat",
        headers={
          "Authorization": f"Bearer {os.environ['LM_API_TOKEN']}",
          "Content-Type": "application/json"
        },
        json={
          "model": "ibm/granite-4-micro",
          "input": "What is the top trending model on hugging face?",
          "integrations": [
            {
              "type": "ephemeral_mcp",
              "server_label": "huggingface",
              "server_url": "https://huggingface.co/mcp",
              "allowed_tools": ["model_search"]
            }
          ],
          "context_length": 8000
        }
      )
      print(json.dumps(response.json(), indent=2))
  TypeScript:
    language: typescript
    code: |
      const response = await fetch("http://localhost:1234/api/v1/chat", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${process.env.LM_API_TOKEN}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          "model": "ibm/granite-4-micro",
          "input": "What is the top trending model on hugging face?",
          "integrations": [
            {
              "type": "ephemeral_mcp",
              "server_label": "huggingface",
              "server_url": "https://huggingface.co/mcp",
              "allowed_tools": ["model_search"]
            }
          ],
          "context_length": 8000
        });
      const data = await response.json();
      console.log(data);
```

现在，模型可以调用指定 MCP 服务器上的工具了：

```lms_code_snippet
variants:
  response:
    language: json
    code: |
      {
        "model_instance_id": "ibm/granite-4-micro",
        "output": [
          {
            "type": "reasoning",
            "content": "..."
          },
          {
            "type": "message",
            "content": "..."
          },
          {
            "type": "tool_call",
            "tool": "model_search",
            "arguments": {
              "sort": "trendingScore",
              "limit": 1
            },
            "output": "...",
            "provider_info": {
              "server_label": "huggingface",
              "type": "ephemeral_mcp"
            }
          },
          {
            "type": "reasoning",
            "content": "\n"
          },
          {
            "type": "message",
            "content": "The top trending model is ..."
          }
        ],
        "stats": {
          "input_tokens": 419,
          "total_output_tokens": 362,
          "reasoning_output_tokens": 195,
          "tokens_per_second": 27.620159487314744,
          "time_to_first_token_seconds": 1.437
        },
        "response_id": "resp_7c1a08e3d6e279efcfecb02df9de7cbd316e93422d0bb5cb"
      }
```

## 来自 mcp.json 的 MCP 服务器

MCP 服务器可以在 `mcp.json` 文件中预先配置。对于会在你电脑上执行操作的 MCP 服务器（如 [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)），以及你经常使用的服务器，这是推荐的做法。

```lms_info
来自 mcp.json 的 MCP 服务器需要先在[服务器设置](/docs/developer/core/server/settings)中启用"允许调用 mcp.json 中的服务器"。
```

<img src="/assets/marketing/docs/mcp-editor.png" style="" data-caption="在 LM Studio 中编辑 mcp.json" />

```lms_code_snippet
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/chat \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "ibm/granite-4-micro",
          "input": "Open lmstudio.ai",
          "integrations": ["mcp/playwright"],
          "context_length": 8000,
          "temperature": 0
        }'
  Python:
    language: python
    code: |
      import os
      import requests
      import json

      response = requests.post(
        "http://localhost:1234/api/v1/chat",
        headers={
          "Authorization": f"Bearer {os.environ['LM_API_TOKEN']}",
          "Content-Type": "application/json"
        },
        json={
          "model": "ibm/granite-4-micro",
          "input": "Open lmstudio.ai",
          "integrations": ["mcp/playwright"],
          "context_length": 8000,
          "temperature": 0
        }
      )
      print(json.dumps(response.json(), indent=2))
  TypeScript:
    language: typescript
    code: |
      const response = await fetch("http://localhost:1234/api/v1/chat", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${process.env.LM_API_TOKEN}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "ibm/granite-4-micro",
          input: "Open lmstudio.ai",
          integrations: ["mcp/playwright"],
          context_length: 8000,
          temperature: 0
        })
      });
      const data = await response.json();
      console.log(data);
```

响应中包含来自所配置 MCP 服务器的工具调用：

```lms_code_snippet
variants:
  response:
    language: json
    code: |
      {
        "model_instance_id": "ibm/granite-4-micro",
        "output": [
          {
            "type": "reasoning",
            "content": "..."
          },
          {
            "type": "message",
            "content": "..."
          },
          {
            "type": "tool_call",
            "tool": "browser_navigate",
            "arguments": {
              "url": "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
            },
            "output": "...",
            "provider_info": {
              "plugin_id": "mcp/playwright",
              "type": "plugin"
            }
          },
          {
            "type": "reasoning",
            "content": "..."
          },
          {
            "type": "message",
            "content": "The YouTube video page for ..."
          }
        ],
        "stats": {
          "input_tokens": 2614,
          "total_output_tokens": 594,
          "reasoning_output_tokens": 389,
          "tokens_per_second": 26.293245822877495,
          "time_to_first_token_seconds": 0.154
        },
        "response_id": "resp_cdac6a9b5e2a40027112e441ce6189db18c9040f96736407"
      }
```

## 限制工具访问

对于临时服务器和 mcp.json 服务器，你都可以使用 `allowed_tools` 字段限制模型可以调用的工具。当你希望屏蔽某个 MCP 服务器上的特定工具时，这很有用；同时由于模型收到的工具定义更少，还能加快提示处理速度。

```lms_code_snippet
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/chat \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "ibm/granite-4-micro",
          "input": "What is the top trending model on hugging face?",
          "integrations": [
            {
              "type": "ephemeral_mcp",
              "server_label": "huggingface",
              "server_url": "https://huggingface.co/mcp",
              "allowed_tools": ["model_search"]
            }
          ],
          "context_length": 8000
        }'
  Python:
    language: python
    code: |
      import os
      import requests
      import json

      response = requests.post(
        "http://localhost:1234/api/v1/chat",
        headers={
          "Authorization": f"Bearer {os.environ['LM_API_TOKEN']}",
          "Content-Type": "application/json"
        },
        json={
          "model": "ibm/granite-4-micro",
          "input": "What is the top trending model on hugging face?",
          "integrations": [
            {
              "type": "ephemeral_mcp",
              "server_label": "huggingface",
              "server_url": "https://huggingface.co/mcp",
              "allowed_tools": ["model_search"]
            }
          ],
          "context_length": 8000
        }
      )
      print(json.dumps(response.json(), indent=2))
  TypeScript:
    language: typescript
    code: |
      const response = await fetch("http://localhost:1234/api/v1/chat", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${process.env.LM_API_TOKEN}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "ibm/granite-4-micro",
          input: "What is the top trending model on hugging face?",
          integrations: [
            {
              type: "ephemeral_mcp",
              server_label: "huggingface",
              server_url: "https://huggingface.co/mcp",
              allowed_tools: ["model_search"]
            }
          ],
          context_length: 8000
        })
      });
      const data = await response.json();
      console.log(data);
```

如果未提供 `allowed_tools`，则服务器上的所有工具都可供模型使用。

## 临时服务器的自定义请求头

使用需要身份验证的临时 MCP 服务器时，你可以传入自定义请求头：

```lms_code_snippet
variants:
  curl:
    language: bash
    code: |
      curl http://localhost:1234/api/v1/chat \
        -H "Authorization: Bearer $LM_API_TOKEN" \
        -H "Content-Type: application/json" \
        -d '{
          "model": "ibm/granite-4-micro",
          "input": "Give me details about my SUPER-SECRET-PRIVATE Hugging face model",
          "integrations": [
            {
              "type": "ephemeral_mcp",
              "server_label": "huggingface",
              "server_url": "https://huggingface.co/mcp",
              "allowed_tools": ["model_search"],
              "headers": {
                "Authorization": "Bearer <YOUR_HF_TOKEN>"
              }
            }
          ],
          "context_length": 8000
        }'
  Python:
    language: python
    code: |
      import os
      import requests
      import json

      response = requests.post(
        "http://localhost:1234/api/v1/chat",
        headers={
          "Authorization": f"Bearer {os.environ['LM_API_TOKEN']}",
          "Content-Type": "application/json"
        },
        json={
          "model": "ibm/granite-4-micro",
          "input": "Give me details about my SUPER-SECRET-PRIVATE Hugging face model",
          "integrations": [
            {
              "type": "ephemeral_mcp",
              "server_label": "huggingface",
              "server_url": "https://huggingface.co/mcp",
              "allowed_tools": ["model_search"],
              "headers": {
                "Authorization": "Bearer <YOUR_HF_TOKEN>"
              }
            }
          ],
          "context_length": 8000
        }
      )
      print(json.dumps(response.json(), indent=2))
  TypeScript:
    language: typescript
    code: |
      const response = await fetch("http://localhost:1234/api/v1/chat", {
        method: "POST",
        headers: {
          "Authorization": `Bearer ${process.env.LM_API_TOKEN}`,
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          model: "ibm/granite-4-micro",
          input: "Give me details about my SUPER-SECRET-PRIVATE Hugging face model",
          integrations: [
            {
              type: "ephemeral_mcp",
              server_label: "huggingface",
              server_url: "https://huggingface.co/mcp",
              allowed_tools: ["model_search"],
              headers: {
                Authorization: "Bearer <YOUR_HF_TOKEN>"
              }
            }
          ],
          context_length: 8000
        })
      const data = await response.json();
      console.log(data);
```
