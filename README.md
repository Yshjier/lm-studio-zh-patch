# LM Studio 中文汉化补丁

> ⚠️ **声明**：本项目是**非官方第三方汉化补丁**，与 LM Studio 官方无任何关联。
> - 使用本补丁会修改 LM Studio 的安装文件，请自行承担风险
> - 因使用本补丁造成的任何问题（数据丢失、程序崩溃等），作者不承担责任
> - 分发本补丁前请确认你遵守 LM Studio 的用户协议

为 LM Studio（0.4.24+1）提供完整中文界面。官方 i18n 仅覆盖约 18% 可见文本，本项目通过**字典补丁 + 文档注入 + 原生菜单 hook** 实现 90%+ 中文覆盖率。

## 效果

| 项目 | 说明 |
|---|---|
| 字典条目 | **4578 条**（覆盖侧栏、菜单、按钮、状态、属性等所有 UI 文本） |
| 开发者文档 | **156 篇** 全部汉化 |
| 补丁版本 | **v1.10.2**（DOM 匹配 + ShadowRoot 穿透 + 短词 nowrap 防竖排） |
| 原生菜单 | 右键菜单 + 任务栏托盘菜单 全部汉化 |
| 适用版本 | LM Studio **0.4.24+1** |

## 快速开始

**前置要求**：
- Windows 10/11，已安装 LM Studio
- 管理员权限（工具会自动请求 UAC 提权）

**安装**：
```
双击 lms_zh.bat → 选 1
```

**命令行用法**：
```powershell
python lms_zh.py install     # 安装 / 重装
python lms_zh.py uninstall   # 卸载，还原官方英文原版
python lms_zh.py update      # LM Studio 升级后重新适配
python lms_zh.py status      # 查看部署状态
```

## 已汉化范围

- ✅ 侧边栏所有菜单和按钮
- ✅ 设置页全部选项
- ✅ 右键菜单（组件级）
- ✅ 任务栏托盘右键菜单
- ✅ 开发者文档 156 篇全文
- ✅ 模型参数标签（架构/量化/上下文等）

## 已知限制

| 限制 | 原因 |
|---|---|
| 输入框右键菜单（Undo/Cut/Copy/Paste）保持英文 | Chromium 内置菜单，JS 不可达 |
| Hugging Face 模型 README 正文保持英文 | 运行时从 API 动态拉取，不在 bundle |
| Staff Pick 描述保持英文 | LM Studio 自家服务器数据 |
| 部分语种名保持英文 | 用户选项而非 UI 文本 |

## 项目结构

```
LM Studio Chinese/
├── lms_zh.py                  # 部署管理工具
├── lms_zh.bat                 # 双击启动器
│
├── patch/                     # 核心补丁文件
│   ├── zh_dict.json           # 词典源
│   ├── zh_dict.js             # 编译后词典
│   ├── lms-zh-patch.js        # DOM 汉化补丁
│   ├── patch_native_menus.py  # 右键菜单补丁
│   ├── patch_tray_menu.py     # 托盘菜单补丁
│   └── docs_zh/               # 中文译文
│
└── docs/                      # 开发文档
```

## 版权与许可

- 本项目**补丁代码**采用 **MIT License**，可自由使用、修改、分发
- **LM Studio 及相关商标版权归 LM Studio 官方所有**，本项目不包含任何 LM Studio 官方代码
- 本项目仅作为第三方汉化工具使用，不参与任何商业用途

## 反馈

发现遗漏的英文 UI 文本：
1. 在 LM Studio 里按 `Ctrl+Shift+I` 打开 DevTools
2. 控制台运行 `__zhDebug()`，复制未翻译样本
3. 提交 Issue 附上样本
