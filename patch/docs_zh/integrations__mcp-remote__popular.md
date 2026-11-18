## Linear

直接在 LM Studio 中于 Linear 创建议题、搜索项目、更新状态等。

[![Add Linear MCP to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-light.svg)![Add Linear MCP to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-dark.svg)](/install-mcp?name=linear&config=eyJ1cmwiOiJodHRwczovL21jcC5saW5lYXIuYXBwL21jcCJ9)

```json
{
  "mcpServers": {
    "linear": {
      "url": "https://mcp.linear.app/mcp"
    }
  }
}
```

***

## Notion

在你的 Notion 工作区中搜索页面、创建文档并读取内容。

[![Add Notion MCP to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-light.svg)![Add Notion MCP to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-dark.svg)](/install-mcp?name=notion&config=eyJ1cmwiOiJodHRwczovL21jcC5ub3Rpb24uY29tL21jcCJ9)

```json
{
  "mcpServers": {
    "notion": {
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

***

## Atlassian

在 LM Studio 中处理 Jira 议题和 Confluence 页面。

[![Add Atlassian MCP to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-light.svg)![Add Atlassian MCP to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-dark.svg)](/install-mcp?name=atlassian&config=eyJ1cmwiOiJodHRwczovL21jcC5hdGxhc3NpYW4uY29tL3YxL21jcCJ9)

```json
{
  "mcpServers": {
    "atlassian": {
      "url": "https://mcp.atlassian.com/v1/mcp"
    }
  }
}
```

***

## Sentry

查询议题、检视堆栈跟踪，并分析你 Sentry 项目中的错误。

[![Add Sentry MCP to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-light.svg)![Add Sentry MCP to LM Studio](https://files.lmstudio.ai/deeplink/mcp-install-dark.svg)](/install-mcp?name=sentry&config=eyJ1cmwiOiJodHRwczovL21jcC5zZW50cnkuZGV2L21jcCJ9)

```json
{
  "mcpServers": {
    "sentry": {
      "url": "https://mcp.sentry.dev/mcp"
    }
  }
}
```

***

还支持更多集成。任何使用 OAuth 或标准 HTTP 传输的 MCP 服务器都可以接入 LM Studio。关于如何通过 `mcp.json` 手动添加自定义服务器，参见[使用 MCP 服务器](/docs/app/mcp)。
