# LM Studio 汉化项目 — 开发笔记

## 项目架构

### 四条渲染路径
| 路径 | 表现 | 翻译手段 |
|---|---|---|
| React DOM 文本/属性 | 普通页面文字 | `lms-zh-patch.js` DOM 补丁（ShadowRoot 穿透 + 模板字符串前缀 + 短词 nowrap 防竖排） |
| i18n 表直查 | 模型配置/加载/预设/插件/更新页 | 字典直接匹配 key |
| react-contexify ShadowRoot | 部分右键菜单 | 同上，`collectRoots` 穿透 ShadowRoot |
| Electron 原生菜单（renderer IPC） | 右键菜单、三点下拉 | 字节级 patch renderer 里的菜单转换函数 |
| Electron 原生菜单（主进程） | 任务栏托盘右键 | hook `Menu.buildFromTemplate` |
| Chromium 内置菜单 | 输入框右键（Undo/Cut/Copy/Paste） | 不碰，保持原生英文 |
| 开发者文档正文（内嵌 Markdown） | 文档页面右侧正文 | 字节级替换 bundle 内 `content:'...'` 字符串 |

### 铁律
- **最坏结果 = 没翻译**，绝不能是「功能没了」或「样式大改让用户不认」
- 只改 textNode.nodeValue，绝不动 DOM 结构（保护 React fiber）
- 已翻译节点可一键还原

---

## 关键模块说明

### 短词竖排修复（v1.10+）
**现象**：侧栏 `Integrations` → `集成` 后，"集"/"成" 竖排成两行。

**方案**：精准 inline `white-space:nowrap`，仅当满足以下条件才给父元素加样式：
1. 翻译结果 = 1-3 字中文
2. 父元素只含 textNode（允许空白 textNode），不能含 elementNode 子节点
3. 合并后纯文本 == 翻译结果（排除兄弟 textNode 拼接的复合文本）
4. 用户未设置 `window.__ZH_NO_NOWRAP__` 紧急关停

**诊断**：
- `window.__zhNowrapCount` — 命中数
- `window.__zhDebug().nowrapMisses` — 卡条件的样本

### 原生菜单补丁（renderer 侧）
两个转换器都要 patch：
- 模块 6405 `n(t,e)` — 供 `<ContextMenu spec>` / TabChip
- 模块 59332 `o(t,e)` — 供 `useContextMenu()` hook

**手段**：在函数体开头注入 `const ZH=window.__ZH_DICT__||{},_tr=s=>(ZH&&ZH[s])||s;`，把所有 `label:X.label` 改为 `label:_tr(X.label)`

### 托盘菜单补丁（主进程侧）
**方案**：在 `main/index.js` 最开头注入代码， hook Electron 的 `Menu.buildFromTemplate`，自动翻译所有菜单 label。

**覆盖范围**：
- 任务栏托盘右键菜单
- 任何主进程直接 `buildFromTemplate` 创建的菜单

---

## 踩坑经验

### React/JSX DOM 结构
- 父元素 `childNodes.length` 通常 ≥2（文本节点 + `"\n  "` 空白 textNode），不是直觉的 1
- 判定"父元素只含这段中文"：把所有 textNode 的 `nodeValue` 拼起来，再与翻译结果比较

### 富文本 textNode 边界
- JSX 里的 markdown 控制符（`**` `` ` `` `__` 等）不会进入 textNode
- 富文本相邻 textNode 的真实边界字符只有：字面空格、字面标点、字面字母
- **不要猜测 textNode 边界**，用 `__zhDebug()` 或 React DevTools 看真实值

### Windows 部署
- 写 `C:\Program Files` 需要管理员权限
- `.bat` 文件用纯 ASCII，不要带中文注释（CMD 按 GBK 读会乱码）
- 子脚本调用要设 `PYTHONIOENCODING=utf-8` 避免编码乱码

### 字节级 patch
- patch 后必须 `node --check` 验证语法
- 改 bundle 前 LM Studio 必须完全退出
- Python 读写 bundle 必须 `newline=''`（bundle 是 CRLF）

### 字典文件格式
- `zh_dict.json`: 1 空格缩进 + 每行尾 `", "` + 末项无尾逗号 + CRLF
- 不要用 `json.dumps(indent=1)` 直出，会丢尾空格

---

## 部署流程

**单文件管理工具**：`lms_zh.py` + `lms_zh.bat`

```
install: 杀进程 → 备份 → 汉化右键菜单 → 汉化托盘菜单 → 注入文档 → 拷贝补丁 → 注入 index.html
uninstall: 还原所有 .bak → 删除补丁文件
update: 重抽文档 → 刷新备份 → 重新部署 → 漏翻报告
status: 查看部署状态
```

**原地备份**：`.bak` 文件与 bundle 同目录，不依赖项目目录。

---

## 已知限制

| 限制 | 原因 |
|---|---|
| 输入框右键菜单（Undo/Cut/Copy/Paste）保持英文 | Chromium 内置菜单，JS 不可达 |
| 模型 README 正文（HF 拉取）保持英文 | 运行时动态拉取，不在 bundle |
| Staff Pick 描述保持英文 | LM Studio 自家服务器数据 |
| 4 字+ 中文在极窄容器仍可能竖排 | 词典范畴，换更短词可缓解 |

---

## 项目结构

```
patch/
├── zh_dict.json          # 字典源
├── zh_dict.js            # 字典编译产物
├── lms-zh-patch.js       # DOM 汉化补丁
├── patch_native_menus.py # renderer 右键菜单补丁
├── patch_tray_menu.py    # 主进程托盘菜单补丁
├── apply_docs_zh.py      # 文档注入
├── extract_docs.py       # 文档抽取
└── docs_zh/              # 中文译文
```
