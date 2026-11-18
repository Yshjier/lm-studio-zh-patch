# LM Studio 简体中文汉化补丁 v2.0

面向 Windows 版 **LM Studio 0.4.28+2** 的汉化补丁。采用「运行时观察者注入 +
少量静态旁路」的混合机制：界面文案在渲染后由 observer 翻译可见 DOM；文档正文、
i18n 缺键、长文 FAQ、主进程托盘菜单这四类 observer 够不到的内容走定点静态注入。

不修改引擎、不改全局样式布局；最坏结果是「某处没翻译」，不会出现功能丢失或界面错版。

> **声明**：本项目为非官方第三方汉化补丁，与 LM Studio 官方无关联。补丁会修改 LM Studio
> 安装文件，请自行承担风险；因使用补丁造成的数据丢失、程序崩溃等，作者不承担责任。
> 分发前请遵守 LM Studio 用户协议。

**边界（既定决策）**
- 原生 renderer 右键菜单（Electron `n()/o()` 通道）保持原样，本补丁不处理。
- 用户数据默认名（如 `Empty Folder`）不翻译，避免与磁盘文件名/重命名状态不一致。
- Monaco 命令码表、第三方库内部报错、协议路径/语言码、外部产品名保持英文。

---

## 一、快速使用

```
cd <补丁所在目录>
$env:PYTHONIOENCODING = "utf-8"

python install.py install     # 安装 / 重装（幂等，自动 UAC 提权）
python install.py uninstall   # 还原官方英文原版
python install.py update      # 适配新版：重抽文档原文 → 刷新备份 → 重部署 → 漏翻报告
python install.py status       # 查看部署状态（不需要管理员）
```

也可双击 `install.bat` 进入交互菜单。生效前必须**完全退出** LM Studio（托盘 → Quit），
仅关窗口不会重新加载渲染层。

### 改完字典后重新生成产物

`patch/zh_dict.json` 与 `patch/zh_dict.js` 是构建产物，不要手改；词条源在 `dict_src/`：

```
python tools/build_dict.py     # dict_src/zh_dict.json -> patch/zh_dict.json（校验、过滤、排序）
python patch/gen_dict_js.py    # zh_dict.json -> zh_dict.js（window.__ZH_DICT__）
```

---

## 二、目录结构

| 路径 | 作用 |
|---|---|
| `install.py` | 单文件安装器：路径探测 / UAC 提权 / 原地备份 / 部署 / 卸载 / 状态 |
| `install.bat` | Python 启动器（探测解释器后调用 `install.py`；UAC 提权由 `install.py` 完成） |
| `patch/zh_dict.json` | 运行时字典产物（扁平 `en → zh`，5,561 条） |
| `patch/zh_dict.js` | 字典脚本，注入 `window.__ZH_DICT__` |
| `patch/lms-zh-patch.js` | 运行时观察者层（MutationObserver + ShadowRoot 穿透） |
| `patch/apply_docs_zh.py` | 按 `route` 定位文档 `content` 串并注入中文 markdown |
| `patch/docs_manifest.json` | 0.4.28 文档路由 ↔ 译文映射（181 篇，180 篇有译文） |
| `patch/docs_zh/` | 文档中文译文（180 篇 markdown，文件名 = route 转义） |
| `patch/docs_src/` | 181 篇英文原文抽取基线（生成物，不入库，`extract_docs.py` 重抽） |
| `patch/i18n_patch.py` | 简中语言包缺键补注（动态推导模块 ID，只增键不覆盖） |
| `patch/escaped_patch.py` | LM Link 长文 FAQ / 引导正文的转义字面量整段替换 |
| `patch/patch_tray_menu.py` | 主进程托盘菜单 `Menu.buildFromTemplate` hook |
| `dict_src/` | 字典与旁路词条源（见下节） |
| `tools/_scan_common.py` | 扫描/抽取公共件：渲染层定位、覆盖集加载、文档解析与转义辅助 |
| `tools/build_dict.py` | 单源字典构建：校验、过滤、排序后产出 `patch/zh_dict.json` |
| `patch/gen_dict_js.py` | `zh_dict.json → zh_dict.js`（`window.__ZH_DICT__`） |
| `tools/audit_dict.py` | 字典审计：异常值 / 代码形状键 / 首尾空格 / 源产物 parity 核对 |
| `tools/extract_docs.py` | 从原厂 bundle 抽取英文文档原文到 `patch/docs_src/`（译文校验对照基线） |
| `tools/scan_ui_missing.py` | UI 英文漏翻分级扫描：P1 明确 UI / P2 疑似 / P3 内部消息 / i18n 残留 |
| `tools/scan_i18n.py` | 提取英文 locale 块并列出未覆盖 i18n 键 |
| `tools/validate_docs.py` | 译文 markdown 结构对齐校验（围栏/行内代码/标题/链接/图片/表格） |
| `tools/check_code_blocks.py` | 代码块按围栏类型逐字节强校验 |

### `dict_src/` 词条源

| 文件 | 内容 | 运行时归属 |
|---|---|---|
| `zh_dict.json` | 唯一运行时扁平字典（`en → zh`，5,561 条），直接维护 | 并入运行时字典 |
| `i18n.json` | 官方简中包缺键（5 组 70 键，嵌套命名空间） | i18n 静态旁路 |
| `escaped.json` | 含 `\n` 的长文对（6 条 FAQ/引导） | 长文静态旁路 |

> `i18n.json` 是「命名空间 → 键 → 译文」嵌套结构、`escaped.json` 是 `{old, new}` 列表，
> 与扁平运行时字典结构不同，因此保留为独立旁路文件，不并入 `zh_dict.json`。

---

## 三、汉化机制

### 1. 运行时观察者层（主通道）

`index.html` 在 `main_window.js` 锚点后注入两个脚本：先 `zh_dict.js` 写字典，
再 `lms-zh-patch.js` 启动观察者。

- **textNode 整段匹配**：raw 与 trim 双查；原文已含中文则跳过。
- **属性翻译**：`placeholder / title / aria-label / alt`。
- **受控 input**：仅未聚焦且整段命中字典时改 `value`；排除 `password/email/number/hidden`。
- **ShadowRoot 穿透**：递归收集 open shadow root 并观察新挂载的影子树。
- **模板规则**：`TEMPLATE_RULES` 正则前缀匹配，捕获组回填变量（相对时间、用量浮层、
  草稿/停止原因/下载状态等带变量串）。
- **短词 nowrap**：1–3 字中文命中时给父元素精准 inline `white-space:nowrap`，
  可用 `window.__ZH_NO_NOWRAP__ = true` 紧急关停。
- **增量 + 兜底**：MutationObserver 增量处理，另每 1 秒全量扫描一次。
- **诊断**：控制台 `__zhDebug()` 查看命中数、未加 nowrap 样本、影子树英文残留。

### 2. 静态旁路（observer 覆盖不到）

| 旁路 | 为什么必须静态 | 落点 |
|---|---|---|
| 文档正文 | markdown 长文被 React 拆成多段，observer 无法整段命中；且内容量大不宜进字典 | bundle 内按 `route` 替换 `content` 串 |
| i18n 缺键 | 文案走 `t("ns:key",{defaultValue})`，简中包缺键时回落英文，必须补进语言包 payload | bundle 简中 JSON.parse 载荷追加键 |
| 长文 FAQ/引导 | 带 `\n\n` 转义的整段正文，字面量整段替换最稳 | bundle 字面量替换 |
| 托盘菜单 | 主进程 Electron 原生菜单，renderer DOM 层够不到 | 主进程 `index.js` 头部 hook |

### 3. 字典口径

`tools/build_dict.py` 以 `dict_src/zh_dict.json` 为唯一源，校验过滤后产出产物。

过滤（兜底护栏，正常源文件应已满足）：丢弃 `en == zh` 占位（产品名/URL 保留英文）、
空值、非字符串、URL/代码形状键（小写标识符、路径扩展名、颜色码、全大写枚举）。

---

## 四、安全与回滚

- **原地备份**：首次安装在安装目录旁生成 `main_window.js.bak`、`index.html.bak`、
  主进程 `index.js.bak`，是干净卸载/重装的唯一真相来源，不依赖项目目录。
- **先还原再部署**：install 永远从原始备份还原后再打补丁，幂等且不怕半途失败。
- **语法校验**：bundle / 主进程写入前 `node --check` 通过才落盘。
- **卸载**：从三份 `.bak` 还原，删除补丁脚本与 index 注入行；还原后做 SHA256 比对。
- **适配新版**：LM Studio 升级覆盖 bundle 后，`update` 探测到未打补丁且与旧备份哈希
  不同 → 刷新备份 → 重新部署。

---

## 五、漏翻扫描与文档校验

扫描产物在 `tools/analysis/out/`（生成物，不入库）：

```
python tools/scan_ui_missing.py   # 分级漏翻候选 -> missing_p1/p2/p3.txt/json
python tools/scan_i18n.py          # i18n 英文块 -> en_i18n_all.json / en_i18n_missing.json
python tools/validate_docs.py      # 译文结构对齐校验
python tools/check_code_blocks.py  # 代码块逐字节强校验
```

词条收录口径：仅收「作为整段可见 UI 字面量、且非 React 拆分片段、非品牌/CLI/语言名/
主题名/SDK 名」的条目；ICU 复数与统计消息运行时由观察者 `TEMPLATE_RULES` 覆盖；
品牌/产品名/枚举值/路径占位保持英文。

## 六、已知限制与待办

- 文档 181 篇中 180 篇已有译文；仅 `CONTRIBUTING` 在 0.4.28 bundle 中无英文基线，
  保持英文（清单见 `patch/docs_manifest.json` 中 `zh: null` 条目）。
- 部分 i18n 命名空间长文案（引导、工具说明、预设发布提示等）需先定位所属模块分组
  再补进 `i18n.json`，当前按扫描清单暂缓；ICU 复数统计串由模板规则在渲染层覆盖。
- 文档校验检出的链接改写、围栏类型版本漂移、个别代码体差异为待审候选，未逐条回改译文。
- 懒加载 chunk 内的文案、第三方库内部报错不在本补丁覆盖范围。
- 官方简中语言包升级后，`i18n.json` 补键可能被官方翻译覆盖（属正常）。

## 七、许可

本项目补丁代码、汉化字典与文档译文采用 **CC BY-NC-SA 4.0** 协议（全文见 `LICENSE`）。
LM Studio 软件本体、商标及相关版权归 LM Studio 官方所有；本项目为第三方补丁，
不包含任何官方代码，与官方无关联。
