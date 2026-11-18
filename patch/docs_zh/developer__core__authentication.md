
##### 需要 [LM Studio 0.4.0](/download) 或更高版本。

LM Studio 支持使用 API 令牌进行身份验证，为访问 LM Studio API 提供了一种安全便捷的方式。

### 为每个请求要求身份验证

默认情况下，LM Studio 不要求 API 请求进行身份验证。要启用身份验证，让只有携带有效 API 令牌的请求才会被接受，请打开「开发者页面 > 服务器设置」中的开关。

```lms_info
启用后，所有通过 REST API、Python SDK 或 TypeScript SDK 发出的请求都需要携带有效的 API 令牌。用法见[下文](#api-令牌用法)。
```

<img src="/assets/marketing/docs/require-auth.png" style="width: 75%;" data-caption="启用身份验证，要求所有请求携带有效的 API 令牌" />

<img src="/assets/marketing/docs/multiple-tokens.png" style="width: 75%;" data-caption="在服务器设置中管理令牌" />

### 创建 API 令牌

要创建 API 令牌，请点击「服务器设置」中的「管理令牌」。这会打开 API 令牌弹窗，你可以在其中创建、查看和删除 API 令牌。

<img src="/assets/marketing/docs/tokens-empty-modal.png" style="width: 75%;" data-caption="API 令牌弹窗" />

点击「创建令牌」按钮即可创建令牌。为令牌提供一个名称，并选择所需的权限。

<img src="/assets/marketing/docs/create-dave-token.png" style="width: 75%;" data-caption="创建 API 令牌" />

创建完成后，请务必复制该令牌，因为它不会再次显示。

<img src="/assets/marketing/docs/created-dave-token.png" style="width: 75%;" data-caption="API 令牌已创建" />

### 配置 API 令牌权限

要编辑现有 API 令牌的权限，请在 API 令牌弹窗中点击该令牌旁边的「编辑」按钮。你可以修改令牌的名称与权限。

<img src="/assets/marketing/docs/edit-token.png" style="width: 75%;" data-caption="编辑 API 令牌" />

## API 令牌用法

### 在 REST API 中使用 API 令牌：

```lms_noticechill
下面的示例需要启用[允许从 mcp.json 调用服务器](/docs/developer/core/server/settings)，并且 mcp.json 中要有 [Playwright MCP](https://github.com/microsoft/playwright-mcp)。
```

```bash
curl -X POST \
  http://localhost:1234/api/v1/chat \
  -H "Authorization: Bearer $LM_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "ibm/granite-4-micro",
    "input": "Open lmstudio.ai",
    "integrations": [
      {
        "type": "plugin",
        "id": "mcp/playwright",
        "allowed_tools": ["browser_navigate"]
      }
    ],
    "context_length": 8000
  }'
```

### 在 Python SDK 中使用 API 令牌

要在 Python SDK 中使用 API 令牌，请参阅 [Python SDK 指南](/docs/python/getting-started/authentication)。

### 在 TypeScript SDK 中使用 API 令牌

要在 TypeScript SDK 中使用 API 令牌，请参阅 [TS SDK 指南](/docs/typescript/authentication)。
