# LM Studio 中文汉化项目

> ⚠️ **声明**：本项目是**非官方第三方汉化补丁**，与 LM Studio 官方无任何关联。
> - 使用本补丁会修改 LM Studio 的安装文件，请自行承担风险
> - 因使用本补丁造成的任何问题（数据丢失、程序崩溃等），作者不承担责任
> - 分发本补丁前请确认你遵守 LM Studio 的用户协议

把 LM Studio（0.4.24+1）的 UI **完整汉化**。官方 i18n 仅覆盖约 18% 可见文本，本项目通过**字典补丁 + 文档注入 + 原生菜单 hook** 三轨实现 90%+ 中文覆盖率。

## 成果（截至 2026-09-11）

| 项目 | 数字 |
|---|---|
| 字典条目 | **4578 条**（覆盖侧栏、菜单、按钮、状态、属性等所有 UI 文本） |
| 开发者文档 | **156 / 156 篇**（`0_app` 24 / `1_developer` 32 / `1_python` 22 / `2_typescript` 43 / `3_cli` 26 / `4_integrations` 4 / `5_lmlink` 5） |
| 字典补丁层 | **v1.10.2**（DOM 文本/属性精确匹配 + ShadowRoot 穿透 + 模板字符串前缀 + 短词 nowrap 防竖排） |
| 原生菜单 | 右键菜单 + 任务栏托盘菜单 全部汉化 |
| 适用版本 | LM Studio **0.4.24+1**（Electron 框架，2026-09 验证） |
| 安装目录改动 | 5 个文件：`zh_dict.js` / `lms-zh-patch.js` / `main_window.js` / `index.html` / `main/index.js`（主进程托盘补丁） |

## 一键管理工具 (推荐)

所有安装 / 卸载 / 适配新版操作都收进一个自提权、带菜单的单文件工具。

**前置**：
- Windows 10/11，LM Studio 已安装（默认 `C:\Program Files\LM Studio`，其他盘/自定义路径会自动探测，也可设环境变量 `LM_STUDIO_RENDERER`）
- 对该目录有管理员权限（工具在需要时自动弹 UAC）

**用法**：

```powershell
# 双击 lms_zh.bat  -> 出现菜单，选 1/2/3/4
# 或命令行：
python lms_zh.py install     # 安装 / 重装（幂等，重复运行安全）
python lms_zh.py uninstall   # 卸载，还原官方英文原版
python lms_zh.py update      # LM Studio 升级后：重抽文档 + 刷新备份 + 重新部署 + 漏翻报告
python lms_zh.py status      # 查看当前部署状态（不需管理员）
```

**菜单说明**：

| 选项 | 作用 |
|---|---|
| 1) 安装 / 重装 | 杀进程 -> 从原始备份还原 -> 汉化右键菜单 -> 汉化任务栏托盘菜单 -> 注入 156 篇文档 -> 拷贝字典+补丁 -> 注入 index.html。幂等，不怕中断 |
| 2) 卸载 | 还原 `main_window.js`/`index.html`/`main/index.js` 原始备份 + 删除 2 个补丁文件，干净回到官方英文 |
| 3) 适配新版 | LM Studio 自动升级覆盖了 bundle 后，重抽开发者文档、刷新原始备份、重新部署，并扫描新版漏翻键 |
| 4) 查看状态 | 报告补丁文件、注入状态、右键菜单、托盘菜单、备份完整性 |

**要点**：
- 原始备份采用**原地备份**：三个 `.bak` 文件与待修复文件同目录，是"干净卸载/重装"的唯一真相来源，不依赖项目目录。
- 适配新版 = 重跑 `install`（或菜单 3）；字典补丁为版本无关层，旧版字符串仍命中，仅新版新增文案需补字典。
- 改了 `patch/zh_dict.json` 后先 `python patch/gen_dict_js.py` 重新编译，再 `python lms_zh.py install`。

## 卸载

```powershell
# 方式一：一键（推荐）
python lms_zh.py uninstall      # 还原原始备份 + 删除补丁文件
```

## 兼容性

| LM Studio 版本 | 状态 | 备注 |
|---|---|---|
| 0.4.24+1（已验证） | ✅ 完全汉化 | 本项目的目标版本 |
| 0.4.24+1 之前 | ❌ 未测试 | bundle 结构差异未知 |
| 0.4.24+1 之后 | ⚠️ 字典可复用 | 文档需重新抽取 + 翻译 |

## 已知限制

| 限制 | 原因 |
|---|---|
| 输入框右键菜单（Undo/Cut/Copy/Paste）保持英文 | Chromium 用内置 `en-US.pak` 渲染，JS 不可达 |
| Hugging Face 模型 README 正文保持英文 | 运行时从 HF API 动态拉取，不在 bundle |
| Staff Pick 描述（如 "State-of-the-art laptop size model..."）保持英文 | LM Studio 自家服务器数据 |
| 国际化语种名（Bahasa Indonesia / Dansk / Deutsch 等）保持英文 | 用户选项而非 UI 文本 |

## 项目结构

```
LM Studio Chinese/
├── README.md                       # 本文档
├── LICENSE                         # MIT
├── .gitignore
├── lms_zh.py                       # ★ 单文件管理工具（安装/卸载/适配新版/状态）
├── lms_zh.bat                      # 双击启动器（自动 UAC 提权）
│
├── patch/                          # 补丁与部署脚本（产品核心）
│   ├── zh_dict.json                # 字典源（4578 条）
│   ├── zh_dict.js                  # 字典编译产物（注入 window.__ZH_DICT__）
│   ├── lms-zh-patch.js             # 汉化补丁 v1.10.2（DOM 匹配 + nowrap 防竖排）
│   ├── patch_native_menus.py       # 右键菜单字节补丁
│   ├── patch_tray_menu.py          # 任务栏托盘菜单补丁（主进程 hook）
│   ├── apply_docs_zh.py            # 文档注入/回滚/报告
│   ├── extract_docs.py             # 从 main_window.js 抽英文 markdown
│   └── ...                         # 其他辅助脚本
│
└── analysis/                       # 分析工具（扫描/诊断，不改 bundle）
```

## 验证清单（部署后）

打开 LM Studio DevTools Console（`Ctrl+Shift+I`）：

```js
__zhPatchCount    // 应大于 100（命中数）
__zhDebug()       // 输出完整诊断（含 nowrapCount 等）
```

具体场景验证：
- [ ] 侧栏 "Integrations" → "集成"（一行不换行）
- [ ] 底部小锤子弹出面板 "集成" 单行显示
- [ ] 右键菜单全部中文
- [ ] 任务栏托盘右键菜单全部中文
- [ ] 开发者文档正文全中文
