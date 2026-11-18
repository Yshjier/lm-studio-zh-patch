
## 问答

对 LM Link 有疑问？我们在下方解答一些最常见的问题。

#### 问：LM Link 会把我的电脑暴露到公网吗？

答：不会！LM Link 网络中的所有设备都通过 Tailscale 的内部端到端加密连接相互通信。你的设备永远不会暴露在公共互联网上。

#### 问：我可以在 LM Studio 的本地服务器上使用远程模型吗？

答：可以。LM Link 网络中的任何模型都可以像本地模型一样使用。这意味着，任何已能连接到本地 LM Studio 的工具，也都能使用远程模型，只需像往常一样指向 localhost:1234 即可。

#### 问：我可以通过 LM Studio API/SDK 使用远程模型吗？

答：可以。LM Link 网络中的任何模型都可以像本地模型一样使用。只需像往常一样指定模型 key。如果模型能在远程设备上找到，就可以通过 LM Link 使用。

#### 问：LM Link 会干扰我现有的 Tailscale VPN 吗？

答：不会。LM Link 是对 Tailscale VPN 原语完全独立、自成一体的运用。LM Link 会与你机器或网络上的其他 Tailscale 用途共存，互不干扰、互不交织。

#### 问：LM Studio Hub 能看到我的聊天吗？

答：不能。LM Studio Hub 仅用于在 LM Studio/llmster 实例之间进行发现。之后的所有通信，包括聊天和模型列表，都发生在 Tailscale 的端到端加密连接之内。

#### 问：如何禁用 LM Link？

答：在 LM Studio 应用中，前往"设置"-> LM Link -> 启用 LM Link —— 关闭。如果你使用的是 llmster（我们的无头守护进程），请运行 `lms link disable`。

#### 问：为什么某台设备显示为"已断开"？

答：LM Link 使用端到端加密隧道相互连接。如果某台设备显示为"已断开"，可能是该设备已经崩溃，但未向发现服务器上报。请确认该设备上确实在运行 LM Studio/llmster。如果错误持续存在，请在 [bugs@lmstudio.ai](mailto:bugs@lmstudio.ai) 报告 bug。

#### 问：如果我在多台设备上有同一个模型，如何选择使用哪一个？

答：如果你通过 LM Studio 或 `lms load` 加载模型，不同设备上的同一模型会显示为不同的条目，并标明设备名。如果你通过 API/SDK 加载模型，可以在应用内的 LM Link 页面设置首选设备，或使用命令 `lms link set-preferred-device`。设置后，模型将始终在你的首选设备上加载。

#### 问：已链接的设备除了 LM Studio 任务外，还能在我的电脑上做别的事吗？

答：不能。LM Link 只让 LM Studio/llmster 之间为了模型和 API 访问而相互通信。它不会把你的操作系统、文件或其他服务暴露给已链接的设备。

#### 问：我可以使用我现有的 Tailscale 网络吗？

答：目前不行。当你启用 LM Link 时，我们会以编程方式创建一条专用网络，并完全掌控其 ACL。这无法与任何现有的 Tailscale 网络良好协作。如果你愿意，也可以自行 DIY LM Link 功能集的若干方面。
