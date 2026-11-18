
## 添加新设备

<img src="/assets/marketing/docs/lmlink-adddevice.png" style="" data-caption="LM Link 中的添加设备弹窗" />

### 有图形界面的机器

要开始使用 LM Link，请向 Link 中添加另一台设备：

1. 在该设备上从 [https://lmstudio.ai/download](https://lmstudio.ai/download) 下载并安装 LM Studio
2. 点击侧栏中的 LM Link，并按步骤启用 LM Link。

一旦 LM Link 启用，你的设备就会自动相互连接。

### 没有图形界面的机器

要添加一台无头机器，请在终端中使用 llmster 进行远程连接：

1. 在这台无头机器上安装 `llmster`

```bash
curl -fsSL https://lmstudio.ai/install.sh | bash
```

2. 从终端登录

```bash
lms login
```

3. 按终端输出中的说明完成登录。
4. 登录后，运行以下命令：

```bash
lms link enable
```

你的设备会通过 Link 自动相互发现，你的无头机器会立即出现在你另一台设备的 LM Link 页面上。连接后，来自远程机器的模型会显示在本地，供加载和推理使用。

## 在远程机器上加载模型

<img src="/assets/marketing/docs/lmlink-useremotemodels.png" style="" data-caption="使用 LM Link 在远程设备上加载模型" />

使用 LM Link 时，模型加载器会同时显示本地模型和已链接设备上的远程模型。

你可以筛选模型加载器，只显示本地或远程模型，或一次显示全部可用模型。远程模型可以用同样熟悉的控件来加载和配置，无论是在图形界面中，还是在终端中使用 lms。 

如果你在多台设备上有同一个模型，它们会显示为不同的条目，并标明关联的设备名。如果你通过 API/SDK 加载模型，当存在多个选项时，你可以[设置首选设备](/docs/lmlink/basics/preferred-device)来指定从哪台设备加载模型。

借助 LM Studio 的并行请求，你还可以在 LM Link 网络中同时服务多个客户端。
