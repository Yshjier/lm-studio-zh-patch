
启用「在本地网络提供服务」选项后，你机器上运行的 LM Studio API 服务器就可以被同一本地网络中的其他设备访问。

这在以下场景中很有用：

- 在其他性能较弱的设备上使用本地 LLM，只需把它们连接到运行 LM Studio 的更强劲机器。
- 让多人在网络上共用同一个 LM Studio 实例。
- 从 IoT 设备、边缘计算单元或本地环境中的其他服务调用 API。

启用后，服务器将绑定到你的本地网络 IP 地址，而不是 localhost。API 访问 URL 会相应更新，你可以在自己的应用程序中使用它。

<img src="/assets/marketing/docs/serve-local-network.png" style="" data-caption="在本地网络提供 LM Studio API 服务器" />
