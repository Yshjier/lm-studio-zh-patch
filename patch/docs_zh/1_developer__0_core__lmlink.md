
## 概述

借助 [LM Link](/docs/lmlink)，你可以像使用本地加载的模型一样，使用远程设备上加载的模型——在同一链路上的任意机器上都可以。这一点自然延伸到 REST API 与 SDK：你的笔记本可以向 `localhost` 发起请求，而由网络中性能强劲的远程机器来提供服务。

对 `localhost` 的请求依然照常工作。LM Studio 内部会像使用本地加载的模型那样，使用远程设备上的模型。对于存在于多台设备上的模型，REST API 会使用首选设备上的那一个。

<img src="/assets/marketing/docs/rest-link-diagram.png" data-caption="时序图：REST API 请求经 LM Link 路由到远程设备" />

首选设备设置是按机器保存的。链路上的每台设备各自独立地控制它偏好哪台远程机器。更多细节见[如何设置首选设备](/docs/lmlink/basics/preferred-device)。

## 照常使用 REST API

像在本地一样使用 REST API 即可。用法细节见 [REST API 文档](/docs/developer/rest)。

如果遇到问题，欢迎加入我们的 [Discord](https://discord.gg/lmstudio)
