LM Studio 现支持带 OAuth 的 MCP。无需复制令牌或配置请求头，即可顺畅接入需要认证的集成。只需添加你的集成，在浏览器中登录，其工具即可在 LM Studio 中供模型使用。

<img src="https://lmstudio.ai/assets/marketing/docs/mcp-auth.webp" style="width: 100%;" data-caption="已登录的 Atlassian MCP 与需要认证的 Notion MCP" />

## 工作原理

添加基于 OAuth 的 MCP 集成时，LM Studio 会：

1. 打开浏览器窗口到该服务的授权页面
2. 在你批准访问后安全存储令牌
3. 在聊天中提供该服务器的工具

此后，你的模型就可以像调用其他 MCP 服务器一样调用该服务的工具。

***

## 使用自己的 OAuth 凭据连接

部分服务要求你自带 OAuth 应用，原因可能是它们不支持动态客户端注册，或需要在开发者门户中加入特定回调 URL 的白名单。

这种情况下，在 `mcp.json` 的服务器条目中添加一个 `auth` 对象。配置 OAuth 应用时，使用以下回调 URL：

```
http://127.0.0.1:33389/mcp-oauth-callback
```

```json
{
  "mcpServers": {
    "oauth-server": {
      "url": "https://api.example.com/mcp",
      "auth": {
        "CLIENT_ID": "TEST_CLIENT_ID",
        "CLIENT_SECRET": "TEST_CLIENT_SECRET"
      }
    }
  }
}
```
