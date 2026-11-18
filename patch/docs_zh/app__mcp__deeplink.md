
你可以使用 deeplink 一键在 LM Studio 中安装 MCP 服务器。

从 0.3.17 (10) 版本开始，LM Studio 可以作为 MCP 主机。更多内容见[此处](../mcp)。

---

# 生成你自己的 MCP 安装链接

输入你的 MCP JSON 条目，为 `Add to LM Studio` 按钮生成 deeplink。

```lms_mcp_deep_link_generator

```

## 试用一个示例

试着把以下内容复制粘贴到上面的链接生成器中。

```json
{
  "hf-mcp-server": {
    "url": "https://huggingface.co/mcp",
    "headers": {
      "Authorization": "Bearer <YOUR_HF_TOKEN>"
    }
  }
}
```

### Deeplink 格式

```bash
lmstudio://add_mcp?name=hf-mcp-server&config=eyJ1cmwiOiJodHRwczovL2h1Z2dpbmdmYWNlLmNvL21jcCIsImhlYWRlcnMiOnsiQXV0aG9yaXphdGlvbiI6IkJlYXJlciA8WU9VUl9IRl9UT0tFTj4ifX0%3D
```

#### 参数

```lms_params
- name: "lmstudio://"
  type: "protocol"
  description: "用于打开 LM Studio 的协议方案"
- name: "add_mcp"
  type: "path"
  description: "安装 MCP 服务器的动作"
- name: "name"
  type: "query parameter"
  description: "要安装的 MCP 服务器的名称"
- name: "config"
  type: "query parameter"
  description: "MCP 服务器的 Base64 编码 JSON 配置"
```
