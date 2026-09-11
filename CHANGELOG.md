# LM Studio 中文汉化 - 完整 CHANGELOG

> 51 轮迭代，覆盖 1699 → 4193 字典条 + 156 篇文档汉化 + 字典补丁 v1.7
>
> 适用版本：**LM Studio 0.4.24+1**（Electron + webpack 打包）
>
> 时间：2026-09-09 至 2026-09-10

---

## 第 1 阶段：项目奠基（第 1-29 轮，2026-09-09）

### 主要成果
- 完成 bundle 深度扫描（renderer 35MB + main 25MB）
- 建立**双补丁架构**（字典补丁 + 原生菜单字节补丁）
- 字典从 0 → 1615 条
- 解决四条渲染路径（React DOM / ShadowRoot / Electron 原生菜单 / Chromium 内置菜单）

### 关键决策
1. **不碰 bundle 字节布局**——只通过字典匹配 + 字节级 patch renderer `n()` / `o()` 函数体（原生菜单翻译器）
2. **主进程菜单方案放弃**——`webpack-obfuscator` 字符串查表不可达
3. **输入框右键菜单放弃**——Chromium 内置，DOM 模拟样式差异大

### 里程碑
- 第 27 轮上线**运行时翻译模块**（FAB 按钮 + 在线翻译后端），覆盖动态内容
- 第 29 轮翻译模块升级到 v1.1（FAB 可拖动、本地后端探测、白名单）

---

## 第 2 阶段：精度提升（第 30-35 轮）

### 第 30 轮（截图驱动的字典补全）
- **用户反馈 7 类遗漏**（截图）：
  - 点击后 "Copied!" 变英文
  - 搜索框 "Type to filter models." / "Currently Loaded" 英文
  - "Loaded Models" / "复制为 Markdown" → "Copied!" 英文
  - "集成" 按钮折行
  - 链接按钮 "Copy URL to Clipboard" 英文
- 字典 1615 → **1631 条**
- 翻译模块 v1.2 → v1.3（`TOAST_WHITELIST` / 模板前缀匹配 / 防换行 CSS / 副 MutationObserver）

### 第 31 轮（菜单与文档）
- "译" 按钮丢失
- 任务栏托盘菜单英文（Stop Server / Copy LLM Server Base URL / LM Studio Server）
- 开发者文档列表英文
- 字典 1631 → **1675 条**
- 翻译模块 v1.3 → v1.4（修死代码 `scheduleAttrRetry`、按钮 3 秒自检重建）
- **主进程 obfuscator 字节级补丁**（注入 `_ZHMAIN` 字典表，幂等可回滚）

### 第 32 轮（**主进程崩溃回滚**）⚠️ **铁律事件**
- 第 31 轮主进程补丁让 LM Studio 主进程崩溃（`_ZHMAIN` 在函数体内重复 `const` 声明 → `SyntaxError`）
- **诊断根因**：obfuscator 函数被高频调用，每次重复声明触发 SyntaxError
- **永久回滚** `main/index.js` → 备份原值 25371959B
- **铁律诞生**：**绝不碰主 bundle**——主进程 native UI 汉化一律判为"已知限制"
- 决策：托盘菜单保持英文

### 第 33 轮（v1.4 → v1.5 补丁升级）
- 字典 1675 → **1687 条**（7 个 onboarding + Unified KV Cache: + Embeddings + Completions (Legacy) + Status）
- **字典补丁 v1.5**：增加 ShadowRoot 穿透 + CSS 防换行注入
- 翻译模块 v1.4 → v1.5（修路径被翻译 bug）

### 第 34 轮（Stop server 按钮 tooltip）
- 字典 1687 → **1689 条**（`Stop server (Ctrl + .)` / `Start server (Ctrl + R)`）

### 第 35 轮（**翻译模块完全下线**）
- 用户决定去掉在线翻译功能
- `lms-zh-translate.js` 完全移除
- `index.html` 移除 `LMSZH_TRANSLATE_INJECT` 段（-102B）
- **字典补丁完全不动**——纯静态方案回归

### 第 36 轮（Status 字典空格修正）
- 发现 bundle 实际是 `"Status:"`（无空格），字典 `"Status: "` 不匹配
- 字典修正 → 1694 条

### 第 37 轮（v1.5 → v1.6：CSS 防换行移植）
- 删除翻译模块时**遗漏移植 CSS 防换行**到字典补丁
- v1.6 字典补丁**接管** `white-space:nowrap` 全局注入
- 修复"集成"按钮按字换行

### 第 38 轮（Ctrl + L 提示）
- JSX 数组形式文本节点 `["Press ", "⌘", "L to load a model"]`
- 字典 1694 → **1693 条**（4 条拆分文本）

### 第 39 轮（PARAMS 标签）
- 字典 1693 → **1694 条**（`Params` → `参数`）
- 发现 README 正文是 Hugging Face 动态内容

### 第 40 轮（README / Staff Picks）
- 字典 1694 → **1699 条**（5 条 README / Staff Picks 提示）
- **双语/英文 README 区分**：bundle 静态标签 = 已翻；HF 动态正文 = 已知保留

### 第 41 轮（More from 模板字符串 + v1.6 → v1.7）
- 字典补丁 v1.6 → **v1.7**：新增 `TEMPLATE_RULES`（`^More from (.+)$` → `来自 $1`）

---

## 第 3 阶段：文档汉化（第 42-44 轮）

### 第 42 轮（**诊断：开发者文档为何半中半英**）
- bundle 内嵌 **156 篇 Markdown 文档**，约 917KB（`@28932175 ~ @29453921`）
- 渲染路径：`react-markdown` + `remark` + `rehype` + `micromark` 管线
- **4 类原因**：
  1. 917KB 正文未收录（主因）
  2. 大小写不一致（`Stateful Chats` vs `stateful chats`）
  3. Markdown 内联元素撕裂 textNode（``endpoint: `POST /v1/messages`.``）
  4. `translateTextNode.trim()` 丢空格导致"模型download"粘连

### 第 43 轮（**文档管线建成 + 首批 7 篇**）
- 写 `patch/extract_docs.py`（按 pageRelUrl 反向定位，快且稳）
- 写 `patch/apply_docs_zh.py`（apply/rollback/report，幂等）
- 写 `patch/validate_docs.py`（结构校验：围栏/链接/标题/图片）
- 部署首批：**index / api-changelog / authentication / lmlink / server/index / server/settings / server/serve-on-network**
- bundle 35485062 → 35484552B，`node --check` OK

### 第 44 轮（**156 篇全部译完** + variant 标签）
- 全部 156 篇覆盖：
  - `0_app` 24 篇
  - `1_developer` 32 篇
  - `1_python` 22 篇
  - `2_typescript` 43 篇
  - `3_cli` 26 篇
  - `4_integrations` 4 篇
  - `5_lmlink` 5 篇
- 新增 `lms_code_snippet` variant 标签汉化（21 类 / 145 处）
- 新增 `patch/check_code_blocks.py`（代码块强校验）
- 字典补丁 v1.6 → v1.7 包含模板规则

---

## 第 4 阶段：全量扫描与收敛（第 45-51 轮）

### 第 45 轮（**首轮全量扫描 + 文档元数据**）
- 发现 **renderer 下还有 128 个懒加载 chunk**——之前只扫 main_window.js
- 写 `analysis/scan_missing.py`（4 档分级：P1/P2/P3/i18n）
- 写 `analysis/extract_doc_meta.py`（提取文档 title/description/sectionPrettyName）
- 字典 1699 → **1828 条**（+129 文档元数据 + 官方提示）

### 第 46 轮（首批真 UI 文本）
- 模型参数、发现页、LM Link、下载、令牌、聊天、插件、MCP、编辑器
- 字典 1828 → **2247 条**（+419）

### 第 47 轮（编辑器菜单/命令面板）
- Monaco 编辑器右键菜单、命令面板
- 字典 2247 → **2523 条**（+276）

### 第 48 轮（通用 UI 标签）
- 操作按钮、状态、通用操作
- 字典 2523 → **2755 条**（+232）

### 第 49 轮（同步/服务器/排序）
- 字典 2755 → **2906 条**（+151）

### 第 50 轮（**通用短词全收**）
- 通用短词（Status / Yes / No / On / Off / Active / Inactive 等）+ 完整 UI 操作
- 字典 2906 → **4056 条**（+1150）
- v1.6 字典补丁 `closest(code/pre/...)` 跳过逻辑保护代码块，**通用短词字典补丁安全**

### 第 51 轮（最后冲刺）
- 文档元数据 description 完整版 + 13 类模型领域
- 字典 → 4595 条
- **回退 402 条**：游戏分类 251 条 + 建设/施工类 151 条（这些是 bundle 里永远不会出现的）
- **最终 4193 条**

### 复扫对比
| 类别 | 起点 | 终点 | 降幅 |
|---|---|---|---|
| P1 明确 UI | 1029 | **290** | **-72%** |
| P2 疑似 UI | 218 | 160 | -27% |
| i18n 残留 | 500 | 302 | -40% |

P1 剩余 290 条几乎都是已知保留项：产品名（LM Studio 12）/ HTTP 头（Bearer 11）/ 系统名（Windows 4）/ 模型名（Parakeet 4）/ Dev Palette 调试项 / CSS 类名 / CLI 命令 / 单语种名。

---

## 字典条目演进

```
第 1 阶段（1-29 轮）  →    0 →  1615
第 2 阶段（30-41 轮）  → 1615 →  1699
第 3 阶段（42-44 轮）  → 1699 →  1699（字典不动，文档汉化）
第 4 阶段（45-51 轮）  → 1699 →  4193（+2494，纯人工精选）
```

## 字典补丁版本演进

```
v1.0（2026-09-09）  →  基础 DOM textNode 匹配
v1.5（2026-09-10）  →  ShadowRoot 穿透 + CSS 防换行
v1.6（2026-09-10）  →  CSS 防换行接管（翻译模块下线后）
v1.7（2026-09-10）  →  + TEMPLATE_RULES（模板字符串前缀匹配）
```

## 文档汉化演进

```
第 42 轮诊断   →  发现 156 篇文档 + 917KB 正文
第 43 轮       →  7 篇已部署（管线验证）
第 44 轮       →  156 篇全部译完 + variant 标签汉化
```

## 备份演进

```
backups/
├── main_window.predocs.bak     # 文档汉化前的 35485062B（用于 rollback）
├── main_window.js.bak          # 第 1 轮备份（原始 35371959B）
├── main_window_native_menu.bak # 第 30 轮原生菜单字节级 patch 前
├── main_index.js.bak           # 第 31 轮主进程备份（已弃用）
├── main.index.obfuscator.bak   # 第 31 轮 obfuscator 注入前
├── index.html.bak              # 注入脚本前的原版
├── index.html.translate.bak    # 翻译模块注入标记前的原版
└── index_input_ctx.bak         # 输入框右键菜单 patch 前的原版
```

## 关键铁律

1. **绝不碰主 bundle**——`webpack-obfuscator` 注入任何字典都会让主进程崩溃
2. **不动 bundle 字节布局**——只替换 156 个 content 字符串体（其余字节完全一致）
3. **汉化最坏=没翻译，绝不能=功能没了**——任何补丁若破坏现有功能立即回滚
4. **翻译模块删除时遗漏副产物**——CSS 防换行、模板规则都要独立归属字典补丁层
5. **bundle 升级时**——字典可复用，文档需重新抽取

## 已知保留英文

- 主进程托盘菜单（Stop Server / Copy LLM Server Base URL）
- 输入框右键菜单（Undo/Cut/Copy/Paste）
- Hugging Face 模型 README 正文
- LM Studio Staff Pick 描述
- Dev Palette 调试面板（默认隐藏）
- HTTP 头（Bearer / Authorization）
- 国际化语种名（Bahasa Indonesia / Dansk 等）
- CLI 命令名（lms daemon up）
- CSS 类名
- 单语种名（Beta 标识）