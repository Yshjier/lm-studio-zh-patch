# LM Studio 中文汉化项目

把 LM Studio（0.4.24+1）的 UI **完整汉化**。官方 i18n 仅覆盖约 18% 可见文本，本项目通过**字典补丁 + 文档注入**双轨实现 90%+ 中文覆盖率。

## 成果（截至 2026-09-10）

| 项目 | 数字 |
|---|---|
| 字典条目 | **4578 条**（覆盖侧栏、菜单、按钮、状态、属性等所有 UI 文本） |
| 开发者文档 | **156 / 156 篇**（`0_app` 24 / `1_developer` 32 / `1_python` 22 / `2_typescript` 43 / `3_cli` 26 / `4_integrations` 4 / `5_lmlink` 5） |
| 字典补丁层 | v1.7（DOM 文本/属性精确匹配 + ShadowRoot 穿透 + 模板字符串前缀 + CSS 防换行） |
| 适用版本 | LM Studio **0.4.24+1**（Electron 框架，2026-09 验证） |
| 安装目录改动 | 3 个文件：`zh_dict.js` / `lms-zh-patch.js` / `main_window.js`（文档注入）+ `index.html` 注入 2 个 `<script>` |
| 部署方式 | **零补丁式**——不动 bundle 字节级布局（仅替换 156 个 content 字符串体） |

## 一键管理工具 (推荐)

所有安装 / 卸载 / 适配新版操作都收进一个自提权、带菜单的单文件工具，覆盖不变（字典补丁 + 156 篇文档注入 + 原生菜单字节补丁）。

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
| 1) 安装 / 重装 | 杀进程 -> 从原始备份还原 -> 打原生菜单补丁 -> 注入 156 篇文档 -> 拷贝字典+补丁 -> 注入 index.html。幂等，不怕中断 |
| 2) 卸载 | 还原 `main_window.js`/`index.html` 原始备份 + 删除 2 个补丁文件，干净回到官方英文 |
| 3) 适配新版 | LM Studio 自动升级覆盖了 bundle 后，重抽开发者文档、刷新原始备份、重新部署，并扫描新版漏翻键 |
| 4) 查看状态 | 报告补丁文件、注入状态、原生菜单、备份完整性 |

**要点**：
- 原始备份 `backups/main_window.predocs.bak` 与 `backups/index.html.bak` 是"干净卸载/重装"的唯一真相来源，首次 `install` 自动从当前安装创建。
- 适配新版 = 重跑 `install`（或菜单 3）；字典补丁为版本无关层，旧版字符串仍命中，仅新版新增文案需补字典。
- 改了 `patch/zh_dict.json` 后先 `python patch/gen_dict_js.py` 重新编译，再 `python lms_zh.py install`。

## 卸载

```powershell
# 方式一：一键（推荐）
python lms_zh.py uninstall      # 还原原始备份 + 删除补丁文件

# 方式二：手动（无原始备份时的兜底）
taskkill /F /IM "LM Studio.exe"
del "C:\Program Files\LM Studio\resources\app\.webpack\renderer\zh_dict.js"
del "C:\Program Files\LM Studio\resources\app\.webpack\renderer\lms-zh-patch.js"
copy /Y "backups\main_window.predocs.bak" "C:\Program Files\LM Studio\resources\app\.webpack\renderer\main_window.js"
copy /Y "backups\index.html.bak" "C:\Program Files\LM Studio\resources\app\.webpack\renderer\index.html"
```

## 兼容性

| LM Studio 版本 | 状态 | 备注 |
|---|---|---|
| 0.4.24+1（已验证） | ✅ 完全汉化 | 本项目的目标版本 |
| 0.4.24+1 之前 | ❌ 未测试 | bundle 结构差异未知 |
| 0.4.24+1 之后 | ⚠️ 字典可复用 | 文档需重新抽取 + 翻译（见下） |

**升级后兼容方案**：

LM Studio 升级时通常保留 `lms-zh-patch.js` / `zh_dict.js` / `index.html` 注入（这些是独立文件，不在升级范围），但 `main_window.js` 会被官方覆盖：

- **字典补丁** 4193 条大概率仍命中（官方极少改动现有 UI 文案）
- **开发者文档汉化** 100% 丢失（content 字符串体被官方重新生成）

升级后只需 5 分钟恢复文档汉化：

```powershell
# 1. 备份新版本 bundle
copy /Y "C:\Program Files\LM Studio\resources\app\.webpack\renderer\main_window.js" `
        backups\main_window.predocs.bak

# 2. 重新抽取英文文档
cd "D:/Workspace/LM Studio Chinese\patch"
python extract_docs.py    # 会从新版 main_window.js 抽出英文到 docs_src/（中转目录）

# 3. 对比 docs_zh 缺哪些（通常 pageRelUrl 不会改，只是个别篇章新增）
python -c "
import json,os
m=json.load(open('docs_manifest.json',encoding='utf-8'))
zh=set(os.listdir('docs_zh'))
def f(u): return u.replace('/','__')
miss=[e for e in m if f(e['pageRelUrl']) not in zh]
print('missing:', len(miss))
for e in miss: print(' ',e['pageRelUrl'])
"

# 4. 仅翻译新出现的 doc 后注入；旧的 docs_zh 可直接复用
python apply_docs_zh.py report    # 看哪些已有译文已被新 bundle 覆盖
python apply_docs_zh.py           # 注入
```

## 已知限制

| 限制 | 原因 |
|---|---|
| 主进程托盘菜单（Stop Server / Copy LLM Server Base URL）保持英文 | 主进程使用 `webpack-obfuscator` 混淆字符串，第 31 轮曾尝试字节级注入 → 主进程崩溃（`SyntaxError: Identifier already declared`），已永久放弃 |
| 输入框右键菜单（Undo/Cut/Copy/Paste）保持英文 | Chromium 用内置 `en-US.pak` 渲染，JS 不可达，DOM 模拟菜单样式与 OS 原生差异过大已被否决 |
| Hugging Face 模型 README 正文保持英文 | 运行时从 HF API 动态拉取，不在 bundle |
| Staff Pick 描述（如 "State-of-the-art laptop size model..."）保持英文 | LM Studio 自家服务器数据 |
| 国际化语种名（Bahasa Indonesia / Dansk / Deutsch 等）保持英文 | 用户选项而非 UI 文本 |

## 项目结构

```
LM Studio Chinese/
├── README.md                       # 本文档
├── LICENSE                         # MIT
├── .gitignore                      # 忽略 backups/ logs/ *.bak / .workbuddy 等
├── lms_zh.py                       # ★ 单文件管理工具（安装/卸载/适配新版/状态）
├── lms_zh.bat                      # 双击启动器（自动 UAC 提权）
├── .github/                         # GitHub 标准配置
│   ├── ISSUE_TEMPLATE/              # Bug 报告 / 功能请求模板
│   ├── PULL_REQUEST_TEMPLATE.md     # PR 模板
│   └── workflows/ci.yml             # CI：编译校验 + 字典/补丁语法 parity
│
├── docs/                           # 项目文档
│   ├── INSTALL.md                  # 安装与启用说明
│   ├── HANDS_ON.md                 # 开发者指南（迁移版本、补字典、调试）
│   ├── HANDS_ON_EXPERIENCE.md      # 汉化经验总结（架构决策、踩坑教训）
│   ├── CHECKLIST.md                # 发布检查清单
│   ├── DOCS_INDEX.md               # 文档索引
│   └── LM_Studio汉化深度分析报告.md # 第 1 轮分析报告（项目原始需求）
│
├── patch/                          # 补丁与部署脚本（产品核心）
│   ├── zh_dict.json                # 字典源（4578 条）
│   ├── zh_dict.js                  # 字典编译产物（注入 window.__ZH_DICT__）
│   ├── lms-zh-patch.js             # 汉化补丁 v1.9.2（DOM 匹配 + 模板规则）
│   ├── gen_dict_js.py              # JSON → JS 编译器
│   ├── gen_i18n_patch.py           # 补全官方 zh_CN 缺失 key
│   ├── deploy.py                   # [遗留] 部署/回滚工具（已被 lms_zh.py 取代）
│   ├── _deploy_all.py / _deploy_all.bat   # [遗留] 一键全量部署（已被 lms_zh.py 取代）
│   ├── _deploy_only.py             # [遗留] 仅部署字典+补丁（热部署）
│   ├── patch_native_menus.py       # 原生菜单字节补丁（幂等，被 lms_zh.py 调用）
│   ├── extract_docs.py             # 从 main_window.js 抽英文 markdown
│   ├── docs_zh/<name>.md           # 中文译文（156 篇）— 部署唯一依赖
│   ├── docs_manifest.json          # 文档清单
│   ├── apply_docs_zh.py            # 注入/回滚/报告
│   ├── validate_docs.py            # 结构校验
│   ├── check_code_blocks.py        # 代码块强校验
│   ├── variant_labels.py           # lms_code_snippet 标签汉化
│   ├── fix_snippet_newline.py      # 围栏多余换行修复
│   ├── list_variant_labels.py      # 标签清单导出
│   ├── README_部署与回滚.md         # patch/ 子目录内简明部署说明
│   └── lms-zh-translate.js         # 已下线翻译模块（仅保留供回滚）
│
├── analysis/                       # 分析工具（扫描/诊断，不改 bundle）
│   ├── extract_en_i18n.py          # 提取英文 i18n 块（升级后增量补齐）
│   └── scan_missing.py            # 全量 UI 英文扫描（P1/P2/P3/i18n 分级）
│
├── backups/                        # bundle 原始备份（gitignore，不入库）
│   ├── main_window.predocs.bak     # 文档汉化前的主 bundle（rollback 用）
│   ├── main_index.js.bak           # 主进程 bundle 原始备份
│   ├── index.html.bak              # 注入前的 index.html
│   └── index.html.translate.bak    # 含翻译模块注入的 index.html（回滚用）
│
├── logs/                           # 部署日志（gitignore，不入库）
│   └── apply.log / deploy.log      # 部署日志
│
└── .workbuddy/memory/              # 项目长期笔记（gitignore，不入库）
    └── MEMORY.md                   # 关键经验与决策
```

## 验证清单（部署后）

打开 LM Studio DevTools Console（`Ctrl+Shift+I`）：

```js
__zhPatchCount    // 应大于 100（命中数）
__zhDictMiss      // 未命中样本（看是否有同模式遗漏）
__zhDebug()       // 输出完整诊断
```

具体场景验证：
- [ ] 侧栏 "Integrations" → "集成"（一行不换行）
- [ ] 设置 → 外观页 → 8 个 Onboarding 标题全部中文
- [ ] 开发者 → 任一文档（如 REST / API changelog）正文全中文
- [ ] 加载模型后悬浮按钮 "Stop server (Ctrl + .)" → "停止服务器 (Ctrl + .)"
- [ ] 模型详情 → README 标签变 "说明文档"
- [ ] 标签 `Params` 变 `参数`、`Arch` / `Domain` / `Format` 同步变中文
- [ ] 开发者文档 "Plugins (Beta)" 显示中文
- [ ] 浏览器开发者页 "Coming soon" / "Beta" 标识保持英文（**已知保留**）

## 反馈与协作

发现遗漏的英文 UI 文本：
1. 在 LM Studio DevTools Console 运行 `__zhDictMiss` 复制前 20 条样本
2. 检查 `patch/zh_dict.json` 是否已有该 key（如有则是 bug，否则是字典缺失）
3. 补字典后跑 `python patch/gen_dict_js.py` + `_deploy_dict2.bat` 重启 LM Studio

## 致谢

- LM Studio 官方提供 i18n 框架（虽然仅 18% 覆盖）
- GitHub 上的 lms-i18n-zh 早期版本启发