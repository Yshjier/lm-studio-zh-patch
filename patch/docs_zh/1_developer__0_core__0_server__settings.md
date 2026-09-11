
你可以配置服务器设置，例如端口号、是否允许其他 API 客户端访问服务器，以及 MCP 功能。

<img src="/assets/marketing/docs/server-settings.png" style="" data-caption="配置 LM Studio API 服务器设置" />

### 设置说明

```lms_params
- name: 服务器端口
  type: Integer
  optional: false
  description: LM Studio API 服务器监听传入连接的端口号。
  unstyledName: true
- name: 要求身份验证
  type: Switch
  description: 要求 API 客户端通过 `Authorization` 头提供有效的 API 令牌。更多内容见[身份验证](/docs/developer/core/authentication)章节。
  unstyledName: true
- name: 在本地网络提供服务
  type: Switch
  description: 允许同一本地网络中的其他设备访问 API 服务器。更多内容见[在本地网络提供服务](/docs/developer/core/server/serve-on-network)章节。
  unstyledName: true
- name: 允许按请求使用 MCP
  type: Switch
  description: 允许 API 客户端使用不在你的 mcp.json 中的 MCP（模型上下文协议）服务器。这些 MCP 连接是临时的，仅在请求期间存在。目前仅支持远程 MCP。
  unstyledName: true
- name: 允许从 mcp.json 调用服务器
  type: Switch
  description: 允许 API 客户端使用你在 LM Studio 的 mcp.json 中定义的服务器。如果你定义的 MCP 服务器可以访问你的文件系统或私有数据，这可能带来安全风险。此选项要求先启用「要求身份验证」。
  unstyledName: true
- name: 启用 CORS
  type: Switch
  description: 启用跨源资源共享（CORS），允许来自不同源的应用程序访问 API。
  unstyledName: true
- name: 即时模型加载
  type: Switch
  description: 在请求时动态加载模型，以节省内存。
  unstyledName: true
- name: 自动卸载未使用的 JIT 模型
  type: Switch
  description: 当 JIT 加载的模型不再被使用时，自动将其从内存中卸载。
  unstyledName: true
- name: 仅保留最后加载的 JIT 模型
  type: Switch
  description: 仅在内存中保留最近使用的 JIT 加载模型，以尽量减少 RAM 占用
  unstyledName: true
```
