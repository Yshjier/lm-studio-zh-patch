# 汉化逻辑说明（v2.0 运行时 + 静态旁路）

面向 Windows 版 **LM Studio 0.4.28+2**。本文梳理工程结构、部署流程、各通道内部
机制与安全口径，便于后续补词与排查。

---

## 1. 改动对象

| 文件 | 角色 | 处理方式 |
|---|---|---|
| `renderer/main_window.js` | 渲染层主 bundle（界面文案主体） | 文档正文 / i18n 缺键 / 长文 FAQ 定点静态替换；界面文案不再静态改写，由运行时 observer 翻译 |
| `renderer/index.html` | 入口 | `main_window.js` 锚点后注入 `zh_dict.js` + `lms-zh-patch.js` 两个 script |
| `main/index.js` | 主进程（托盘菜单） | 文件头注入 IIFE，hook `Menu.buildFromTemplate` |
| `renderer` 其它懒加载 chunk | 子界面 | observer 运行时覆盖；无静态改写 |

原厂基底：`main_window.js.bak`、主进程 `main/index.js.bak`、`index.html.bak`
在首次安装时建立，是卸载/还原的原始副本。

## 2. 部署流程（`install.py`）

1. `require_admin`：非管理员走 UAC `ShellExecuteW runas` 重启自身。
2. 路径探测：环境变量 `LM_STUDIO_RENDERER` → 注册表 Uninstall `InstallLocation` →
   `C:/D:\Program Files\LM Studio\...\renderer` 候选 → 手动输入。
3. `taskkill` 结束 LM Studio 进程。
4. `ensure_inplace_backup`：缺 `.bak` 且当前未打补丁时，从当前文件就地建三份原始备份；
   已打补丁但缺备份则中止（不能从已改文件反推原始）。
5. 未打补丁且 bundle 与旧备份哈希不符 → 判定版本升级，`refresh_pristine` 刷新备份。
6. `restore_pristine`：从三份 `.bak` 还原 bundle / index.html / 主进程。
7. `step_extract_docs`：从当前 bundle 重抽 181 篇英文文档原文到 `patch/docs_src/`，
   作为译文结构/代码块校验基线（`update` 流程在部署前执行）。
8. 静态旁路依次落 bundle：长文 FAQ → i18n 缺键 → 文档正文注入。
9. 托盘 hook 落主进程。
10. 拷贝 `zh_dict.js`、`lms-zh-patch.js` 到 renderer 目录；`inject_index` 注入入口脚本。
11. `step_scan_report`：部署后跑 i18n / UI 漏翻扫描，汇总未覆盖键数与 P1 候选条数。

卸载：还原三份 `.bak` → 删除两个补丁 JS → 移除 index 注入行。

## 3. 运行时观察者层（`patch/lms-zh-patch.js`）

IIFE 守卫 `window.__zhPatchLoaded`；字典取 `window.__ZH_DICT__`，空字典则中止。

- **文本节点**：`dict[raw] || dict[trim]`；先过 `tryTemplate` 模板规则；
  含 CJK 的节点直接跳过；`code/pre/kbd/samp/var/textarea/contenteditable` 内跳过。
- **属性**：`placeholder / title / aria-label / alt`，整段匹配。
- **受控 input**：`value` 是 DOM property，textNode/属性都抓不到；仅当整段命中字典、
  元素未聚焦、类型非 `password/email/number/hidden` 时替换。
- **ShadowRoot**：`collectRoots` 递归收集 open shadow root；新挂载的 shadow 由
  二级 MutationObserver 补观察并处理。
- **模板规则 `TEMPLATE_RULES`**：正则前缀匹配，`$1/$2` 回填捕获组；覆盖相对时间、
  上下文用量浮层、草稿/停止原因/下载状态/结果数等带变量串。通用 `Delete $1` 放规则末尾。
- **短词 nowrap**：翻译结果为 1–3 字中文、父元素仅含空白与纯装饰图标、合并文本与
  译文一致时，给父元素 inline `white-space:nowrap`；`window.__ZH_NO_NOWRAP__=true` 可关停。
- **调度**：MutationObserver 监听 `childList/characterData/attributes`，rAF 批量处理；
  另每 1 秒全量扫描兜底。
- **诊断**：`__zhPatchCount` / `__zhNowrapCount` / `__zhDebug()` / `__zhNoWrapMisses`。

### 为什么不做「按位置门禁」

运行时 observer 只触碰渲染后的可见 DOM 文本与属性，读不到 JS 枚举、比较值、
对象键、码表，因此全局词与普通词并入同一扁平字典即可，不需要按显示属性做位置判定。

## 4. 静态旁路

### 4.1 文档正文（`patch/apply_docs_zh.py`）

0.4.28 文档结构为模块内 `articles:[{route, metadata:{title,description,prettyName},
content:"…"}]`。

- 定位：`route:"<route>"` 后 8000 字符内找 `content:"`，反斜杠感知扫描字符串尾。
- 替换：保留原引号风格，只重写引号之间正文；从后往前替换避免偏移失效。
- 幂等：当前正文 unescape 后与译文一致则跳过；写入前 `node --check`。
- 映射：`patch/docs_manifest.json` 登记每篇 route 与译文文件名（`zh` 字段）；
  未配译文的条目 `zh: null`。
- 原文基线：`tools/extract_docs.py` 按 0.4.28 `articles` 结构抽取英文原文到
  `patch/docs_src/`（生成物，不入库），供 `validate_docs.py` / `check_code_blocks.py`
  做结构与代码块对照。

### 4.2 i18n 缺键（`patch/i18n_patch.py`）

- `i18n_module_map`：从 bundle 模块表动态推导 `{命名空间: 简中包模块 ID}`，不写死 ID。
- `payload_span`：定位 `ID:t=>{"use strict";t.exports=JSON.parse('…')}` 载荷区间。
- 只追加官方包缺失的键，不覆盖既有官方翻译；注入后重新解析校验键数。
- 源：`dict_src/i18n.json`（config/developer/settings/models/shared，70 键）。

### 4.3 长文 FAQ / 引导（`patch/escaped_patch.py`）

`dict_src/escaped.json` 中 6 条含 `\n\n` 的 LM Link 长文，字面量整段替换。
相对时间等带变量串由观察者模板规则在渲染层覆盖，不在此静态替换。

### 4.4 托盘菜单（`patch/patch_tray_menu.py`）

主进程 `Menu.buildFromTemplate` 包一层 `walk`，固定标签查表 + 端口/数量/状态正则；
模型名等未知 label 原样返回。幂等 marker `// === LMS-ZH tray menu patch ===`。

## 5. 字典构建（`tools/build_dict.py`）

`dict_src/zh_dict.json` 是唯一运行时词条源（扁平 `en → zh`）；构建脚本只做校验、
过滤、排序后产出 `patch/zh_dict.json`，不再做多表合并覆盖。

- 丢弃：`en == zh` 占位、空值、非字符串、URL/代码形状键（小写标识符、扩展名、
  颜色码、全大写枚举、驼峰组件名）。URL 判定只匹配 `http(s)://` / `www.`，
  含普通英文单词（如 prose 中的 `function`）不会被误判为代码。
- 产物 `patch/zh_dict.json` → `patch/gen_dict_js.py` 生成 `zh_dict.js`。

## 5.1 扫描与校验工具链（`tools/`）

| 脚本 | 作用 | 产物 |
|---|---|---|
| `scan_ui_missing.py` | 全 chunk 扫描英文候选，按 P1 明确 UI / P2 疑似 / P3 内部消息 / i18n 残留分级；覆盖集含运行时字典、i18n 译文、escaped 条目；模板规则从 observer JS 解析，不硬抄 | `tools/analysis/out/missing_p1/p2/p3.txt/json`、`missing_i18n.txt` |
| `scan_i18n.py` | 按位置分块 + 英文特征词打分判定英文 locale 块，列出未覆盖键 | `tools/analysis/out/en_i18n_all.json`、`en_i18n_missing.json` |
| `validate_docs.py` | 译文 markdown 结构对齐：围栏、行内代码、标题、链接、图片、表格 | 控制台 ok/fail 清单 |
| `check_code_blocks.py` | 代码块按围栏类型逐字节强校验，识别链接改写 / 版本漂移 / 真代码体差异 | 控制台 ok/fail 清单 |

收录口径：仅收整段可见 UI 字面量；React 拆分片段、品牌/CLI/语言名/主题名/SDK 名、
枚举值、CSS 类、SVG 路径数据不收；ICU 复数与统计串由 observer 模板规则在渲染层覆盖。

## 6. 安全机制

- 先还原原厂备份再部署，幂等；重复运行不叠加补丁。
- bundle / 主进程写入前 `node --check` 真实语法校验，失败不落地。
- 卸载从 `.bak` 按字节还原；回归脚本做 SHA256 比对。
- observer 不改 inline 子元素结构，避免破坏 React reconciler 的 DOM 引用。
- 原生 renderer 右键菜单（`n()/o()` 通道）不注入、不翻译。

## 7. 补一条翻译的标准流程

0. 先跑 `python tools/scan_ui_missing.py` / `python tools/scan_i18n.py` 定位候选，
   对照 `tools/analysis/out/` 分级清单，P1 再逐条进 bundle 核实上下文。
1. 在原厂 `main_window.js.bak` 里搜带引号的精确字面量；搜不到先判断是否前导空格
   裸串、模板字符串内部、转义串。
2. 归类落点：
   - 普通可见词 / 引擎参数名 / 提示 → 直接进 `dict_src/zh_dict.json`。
   - `t("ns:key",{defaultValue})` 回落英文 → `dict_src/i18n.json` 对应分组补键。
   - 含 `\n` 长文 → `dict_src/escaped.json` 加 `{old,new}`。
   - 文档译文 → `patch/docs_zh/<route 转义>.md`，并在 `docs_manifest.json` 登记。
3. `python tools/build_dict.py` → `python patch/gen_dict_js.py` 重建字典产物。
4. `python tools/regress.py` 临时布局闭环回归；`python tools/audit_dict.py` 查异常。
5. 全部通过后再对真实目录 `python install.py install`；操作前退出 LM Studio。

## 8. 已知限制与刻意保留

- 181 篇文档中 180 篇已有译文；仅 `CONTRIBUTING` 在 bundle 中无英文基线，保持英文。
- 引擎 schema 文案来自 `lms.exe`，运行时 observer 翻译其渲染结果；原始参数名不改。
- 模型名、外部产品名、CLI 命令、语言码、协议路径保持英文。
- Monaco 命令/码表、第三方库内部报错刻意不翻。
- 用户数据默认名（空会话、空文件夹）不翻，避免与磁盘记录状态不一致。
- 官方语言包升级后，i18n 补键可能被官方翻译覆盖，需复核。
- 部分 i18n 命名空间长文案（引导、工具说明、预设发布提示等）需先定位所属模块分组
  再补键；ICU 复数统计串由模板规则在渲染层覆盖，不进字典。
