
## 用 `npm` 为插件添加依赖

LM Studio 插件支持 `npm` 包。你可以直接用 `npm install` 安装它们。

插件安装时，LM Studio 会自动下载 `package.json` 和 `package-lock.json` 中声明的所有必需依赖。（用户无需安装 Node.js/npm。）

### `postinstall` 脚本

出于安全考虑，我们**不会**运行 `postinstall` 脚本。因此请确保你没有使用任何必须依赖 postinstall 脚本才能正常工作的 npm 包。

## 使用其他包管理器

由于我们依赖 `package-lock.json`，其他包管理器生成的锁文件无法工作。因此在开发 LM Studio 插件时，我们建议只使用 `npm`。
