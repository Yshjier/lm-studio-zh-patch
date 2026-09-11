# LM Studio 汉化深度分析报告

> 版本对象:LM Studio 0.4.24+1 (Windows, C:\Program Files\LM Studio)
> 分析日期:2026-09-09
> 目标:解答「切换官方中文后界面大部分仍是英文」的原因,并给出可落地的全面汉化方案

---

## 1. 现场与版本

| 项目 | 值 |
|---|---|
| 安装目录 | `C:\Program Files\LM Studio` |
| 版本 | `0.4.24+1` (resources/app/package.json) |
| 打包形态 | Electron,`resources/app/.webpack` 目录直出(非 app.asar) |
| 主进程 | `.webpack/main/index.js`(已混淆) |
| 渲染进程 | `.webpack/renderer/main_window.js`(35 MB,webpack,未混淆) |
| 语言设置 | `C:\Users\Administrator\.lmstudio\settings.json` → `"language": "zh_CN"`(已生效) |

结论先行:**官方简体中文不是没生效,而是只覆盖了 UI 文本的一小部分;真正的大头是写死在代码里的英文文案,任何语言切换都管不到它们。**

---

## 2. 官方 i18n 机制解剖(本机实证)

LM Studio 0.4.x 在渲染进程内置了完整的 react-i18next 体系,翻译资源**静态内嵌在 main_window.js 中**,不联网加载:

| 位置 | 内容 |
|---|---|
| 模块 `72114` | 语言字典组装厂:把每个语言的 10 个 namespace 模块导出对象合并成 `ChineseCNStrings` 等 |
| 模块 `82323` | `i18n.use(initReactI18next).init({lng:"en", fallbackLng:"en", resources:{...}})` |
| namespace 模块 | 形如 `39224:t=>{t.exports=JSON.parse('{...}')}`,每语言 10 个(chat/config/developer/discover/download/models/onboarding/settings/shared/sidebar) |
| zh_CN 资源 | `ChineseCNStrings`,由 sidebar=69976、chat=62968、config=98090、developer=15044、discover=78258、download=68938、models=26049、onboarding=54334、settings=46885、shared=95725 十个模块组成 |

字典键格式为 `ns/key` 风格的扁平 key(如 `models/loader.guardrails.gpu`、`settings/defaultContextLength`)。UI 组件通过 `useTranslation()` 拿到的 `t("...")` 取词,缺失时按 `fallbackLng:"en"` 回退英文。

## 3. 量化发现(硬数据)

### 3.1 官方 zh_CN 字典覆盖其实很高

对 10 个 namespace 的 en 与 zh_CN 字典做 key 级比对:

| namespace | EN keys | CN keys | 缺失 | 缺失示例 |
|---|---|---|---|---|
| sidebar | 7 | 7 | 0 | —(仅 7 个主菜单项走 i18n) |
| chat | 147 | 145 | 2 | actions/clearLastUsedModel 等 |
| config | 254 | 232 | 23 | llm.load.llama.autoFit、contextCheckpoints 等 |
| developer | 99 | 82 | 17 | 兼容 API 端点、MCP 开关等 |
| discover | 26 | 26 | 0 | — |
| download | 29 | 29 | 0 | — |
| models | 92 | 81 | 11 | 加载护栏、索引提示等 |
| onboarding | 6 | 6 | 0 | — |
| settings | 151 | 142 | 9 | 导航栏位置、默认上下文长度等 |
| shared | 52 | 51 | 1 | beta |
| **合计** | **861** | **799** | **63** | **覆盖 92.8%** |

缺失 key 全清单见同目录 `analysis/out/zh_CN_missing_keys.txt`(含英文原值,可直接补译)。

### 3.2 真正的问题:大量 UI 文本不经过 i18n

对渲染进程全量 127 个 chunk 做 JSX `children:"..."` 文本写法扫描:

| 统计项 | 数量 |
|---|---|
| `t("...")` / `t({...})` 调用点 | ≈289 处 |
| `children:"..."` 内联文本总数 | 1 471 |
| 其中英文 UI 类文本(样本抽查) | ≈1 254 |
| 分布 | 99% 集中在 main_window.js |

样本(均为真实可见 UI 文案):
`Your Models`、`Loaded models`、`No loaded models`、`Open model loader`、`Search for models...`、`Show advanced settings`、`Remember settings`、`Dev Renderer Port` ……

**结论:可见文本规模中,i18n 文本约占 18%,硬编码英文约占 82%。** 官方中文 Beta 字典再好,也只能作用于前者;后者就是「切了中文大部分还是英文」的直接原因。

---

## 4. 为什么官方会这样

1. LM Studio 0.4.x 的语言功能仍标注 `(Beta)`,属于"逐步 i18n 化"阶段——只有部分结构界面(设置、加载参数、部分导航)被改造为 `t()`。
2. 聊天、模型管理、发现、下载等核心工作流页面,大量按钮/标签/空状态仍是直接写死的英文字符串。
3. 历史上下文:此前第三方汉化补丁(针对 0.2/0.3.x)都是靠改 bundle 文本实现;0.4.x 有了官方字典后,补丁逻辑不再适用,汉化需要切换到"官方字典 + 硬编码覆盖"双轨。

---

## 5. 汉化方案

### 5.1 三条路线

| | A 补全官方字典 | B 直改 bundle 文本 | C DOM 词典汉化层 |
|---|---|---|---|
| 做法 | 往 zh_CN 的 10 个 namespace JSON 里补 63 个缺失 key | 把 ~1 254 处 `children:"英文"` 字符串替换成中文回写 | 不改 bundle;往 index.html 注入汉化脚本,词典实时替换 DOM 文本 |
| 收益 | 只补 i18n 文本,≈18% | 全界面中文 | 覆盖硬编码英文,≈82% |
| 风险 | 低(纯数据增补) | **中高**:英文串若同时用于 class/key/逻辑比较会被改坏;升级必重打 | 低(逻辑零接触,可回滚) |
| 维护 | 升级后重打 | 需维护替换清单 | 词典可独立迭代,升级大概率仍可用 |
| 开销 | 低 | 中 | 中(需逐页面积累词典) |

### 5.2 推荐组合:A + C

- **第一步(一次性)**:补全官方字典 63 key —— 直接编辑 `main_window.js` 中 zh_CN 各 namespace 模块的 `JSON.parse('...')` 载荷,把缺失 key 的中文翻译写入。收益小但干净,让"走 i18n 的部分"彻底完整。
- **第二步(核心)**:在 `resources/app/.webpack/renderer/index.html` 末尾追加一行 `<script src="lms-zh-patch.js">`,同目录放置汉化脚本 + `zh_dict.json` 词典:
  - 用 `MutationObserver` 监听页面文本节点变化;
  - 命中词典的**完整短语**(如 `"My Models"` → `"我的模型"`)做整段替换,不做子串替换,避免误伤;
  - 词典采用"原文 → 译文"扁平映射,按页面分批补充,先在 sidebar / chat / models 三个最高频页面见效;
  - 通过 `zh_CN` 语言开关 + 白名单(避开代码/数字/URL 节点)控制行为。

### 5.3 关键可行性证据

- `index.html` **无 CSP、无 SRI、无完整性校验**,注入外部 `<script>` 没有任何拦截;
- 渲染进程文件未混淆,文本形态规整(`children:"..."`),词典条目可稳定命中;
- 官方语言设置持久化在 `~/.lmstudio/settings.json` 的 `language` 字段,脚本可读取该值判断是否启用汉化层,保证英文用户界面不受影响。

### 5.4 风险与回滚

| 风险 | 说明 | 对策 |
|---|---|---|
| 官方字典补 key 破坏 JS | 需要小心处理 JSON 内转义 | 脚本化补丁:先备份 main_window.js,补 key 用生成器写入,不手改 |
| DOM 替换误伤动态值 | 例如把用户输入的英文也替换 | 只替换叶子文本节点 + 词典整段匹配 + 跳过 input/textarea/contenteditable |
| 升级覆盖 | 官方更新后 index.html / bundle 被还原 | 汉化补丁做成"备份 + 一键重打"脚本,升级后重跑一次即可 |
| 回滚 | — | 全部操作先备份原文件,还原 = 覆盖回原文件/删注入行 |

---

## 6. 建议的执行顺序

1. 备份 `main_window.js`、`index.html`;
2. 跑"补 63 key"补丁(生成器写回 bundle),启动验证设置页缺失项已中文化;
3. 放置 `lms-zh-patch.js` + `zh_dict.json`,在 index.html 追加注入行;
4. 词典首批 200~300 条,覆盖:侧栏导航、聊天页工具栏/输入框占位、My Models 页按钮与空状态;
5. 逐页面截图比对,按批次扩充词典(可与自研 Ollama 模型管理器的翻译工作流复用同一套词典维护思路)。

---

## 7. 附录

### 7.1 关键文件速查

| 路径 | 作用 |
|---|---|
| `...\resources\app\.webpack\renderer\main_window.js` | 全部 UI 逻辑 + 内嵌翻译字典(唯一需要动的大文件) |
| `...\resources\app\.webpack\renderer\index.html` | 渲染入口,注入点(无 CSP) |
| `...\.webpack\main\index.js` | 主进程(已混淆,不需要动) |
| `C:\Users\Administrator\.lmstudio\settings.json` | `language:"zh_CN"` 语言开关 |

### 7.2 本分析产出的附件

- `analysis/out/dicts.json` —— en / zh_CN 全量字典(已抽取,JSON)
- `analysis/out/zh_CN_missing_keys.txt` —— 63 个缺失 key + 英文原值
- `analysis/*.py` —— 抽取/统计脚本,可复跑验证新版本
