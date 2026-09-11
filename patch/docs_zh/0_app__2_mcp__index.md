
从 LM Studio 0.3.17 开始，LM Studio 充当 **模型上下文协议（MCP）主机**。这意味着你可以把 MCP 服务器连接到应用中，并让你的模型使用它们。

### 务必谨慎

切勿安装来自不受信任来源的 MCP。

```lms_warning
某些 MCP 服务器可以运行任意代码、访问你的本地文件并使用你的网络连接。安装和使用 MCP 服务器时请务必谨慎。如果你不信任来源，就不要安装。
```

# 在 LM Studio 中使用 MCP 服务器

从 0.3.17 (b10) 开始，LM Studio 同时支持本地和远程 MCP 服务器。你可以通过编辑应用的 `mcp.json` 文件，或在可用时使用["添加到 LM Studio"按钮](mcp/deeplink)来添加 MCP。LM Studio 目前沿用 Cursor 的 `mcp.json` 记法。

## 安装新服务器：`mcp.json`

切换到右侧边栏的"程序"选项卡。点击 `安装 > 编辑 mcp.json`。

<img src="/assets/marketing/docs/install-mcp.png"  data-caption="" style="width: 80%;" className="" />

这会在应用内编辑器中打开 `mcp.json` 文件。你可以通过编辑此文件来添加 MCP 服务器。

<img src="/assets/marketing/docs/mcp-editor.png"  data-caption="使用应用内编辑器编辑 mcp.json" style="width: 100%;" className="" />

### 可试用的 MCP 示例：Hugging Face MCP 服务器

此 MCP 服务器提供模型和数据集搜索等功能。

<div className="w-fit">
  <a style="background: rgb(255,255,255)" href="https://lmstudio.ai/install-mcp?name=hf-mcp-server&config=eyJ1cmwiOiJodHRwczovL2h1Z2dpbmdmYWNlLmNvL21jcCIsImhlYWRlcnMiOnsiQXV0aG9yaXphdGlvbiI6IkJlYXJlciA8WU9VUl9IRl9UT0tFTj4ifX0%3D">
    <LightVariant>
      <img src="https://files.lmstudio.ai/deeplink/mcp-install-light.svg" alt="将 MCP 服务器 hf-mcp-server 添加到 LM Studio" />
    </LightVariant>
    <DarkVariant>
      <img src="https://files.lmstudio.ai/deeplink/mcp-install-dark.svg" alt="将 MCP 服务器 hf-mcp-server 添加到 LM Studio" />
    </DarkVariant>
  </a>
</div>

```json
{
  "mcpServers": {
    "hf-mcp-server": {
      "url": "https://huggingface.co/mcp",
      "headers": {
        "Authorization": "Bearer <YOUR_HF_TOKEN>"
      }
    }
  }
}
```

###### 你需要把 `<YOUR_HF_TOKEN>` 替换为你实际的 Hugging Face 令牌。更多内容见[此处](https://huggingface.co/docs/hub/en/security-tokens)。

使用[deeplink 按钮](mcp/deeplink)，或复制上面的 JSON 片段并粘贴到你的 `mcp.json` 文件中。

---

## 注意事项与故障排查

- 切勿安装来自不受信任来源的 MCP 服务器。某些 MCP 可能对你的系统拥有影响深远的访问权限。

- 某些 MCP 服务器是为配合 Claude、ChatGPT、Gemini 而设计的，可能会消耗过多的 token。
  - 请留意这一点。它可能很快拖慢你的本地模型，并频繁触发上下文溢出。

- 手动添加 MCP 服务器时，只复制 `"mcpServers": {` 之后、结尾 `}` 之前的内容。
