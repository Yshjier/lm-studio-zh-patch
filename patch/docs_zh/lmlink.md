
<img src="/assets/marketing/docs/lmlink-animation.gif" style="width: 75%;" data-caption="隆重推出 LM Link" />

LM Link 是 LM Studio 中的一项新功能，它提供了一种无论你身在何处、都能跨设备访问本地模型的方式。Link 是与 Tailscale 合作实现的、专为你拥有的设备之间加载和提供 LLM 服务而设计的定制化、端到端加密网络。

## 我可以用 LM Link 做什么？

LM Link 通过在相连设备间共享算力，充分释放你硬件的潜力。例如，你可能在家中书房有一台强力台式机，还有一台随身携带的轻便笔记本。有了 LM Link，你可以在强力的机器上运行大型开放权重模型，并从笔记本上无缝使用它们，就好似它们本地存在一样。得益于 Tailscale，设备之间的所有通信和数据传输始终采用端到端加密。

## 使用场景

LM Link 的使用场景既涵盖个人，也涵盖团队。

你可以管理一条私有 Link，让你珍爱的游戏 GPU 在你外出时也保持忙碌。此外，LM Link 还能让你在一台服务器上搭建 LLM 服务，只需几次点击即可开始使用。

## 将 LM Link 与以下工具配合使用

- **CLI** —— 在终端中用 [`lms link`](/docs/cli/link/link-enable) 管理 LM Link
- **REST API** —— 借助 [LM Link](/docs/developer/core/lmlink) 通过 REST API 使用远程模型
- **集成** —— 借助 [LM Link](/docs/integrations/lmlink) 在 Claude Code、Codex 等编程工具中使用远程模型
