
## 选择首选设备

当同一个模型在 Link 中的多台设备上都可用时，LM Link 会使用首选设备来加载和使用该模型。此设置是按机器保存的：Link 上的每台设备都独立控制它更偏好哪台远程机器。

这在通过 SDK 或 [REST API](/docs/developer/core/lmlink) 访问远程模型时尤其重要。

### 有图形界面的机器

在应用中，前往 LM Link 页面，选择该设备并切换"设为首选设备"选项。

<img src="/assets/marketing/docs/lmlink-preferred.png" style="width: 75%;" data-caption="将一台设备设为首选设备" />

### 没有图形界面的机器

要从终端设置首选设备，请使用以下命令：

```bash
lms link set-preferred-device
```
