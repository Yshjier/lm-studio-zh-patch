# LM Studio 中文汉化 - 开发者指南

> 适用对象：要维护字典、迁移版本、调试遗漏问题的开发者
>
> 必备环境：Python 3.13+、Git Bash、LM Studio 0.4.24+1 安装在 `C:\Program Files\LM Studio`

---

## 目录

- [字典维护](#字典维护)
- [版本迁移](#版本迁移)
- [调试遗漏](#调试遗漏)
- [新增翻译条目工作流](#新增翻译条目工作流)
- [诊断工具](#诊断工具)

---

## 字典维护

### 字典文件位置
- **源**：`patch/zh_dict.json`（人类可读，2 空格缩进）
- **产物**：`patch/zh_dict.js`（注入 `window.__ZH_DICT__`）
- **安装位置**：`C:\Program Files\LM Studio\resources\app\.webpack\renderer\zh_dict.js`

### 添加/修改字典条目

#### 方式 A：直接编辑 JSON

```bash
# 1. 打开源字典
code patch/zh_dict.json    # VSCode / Sublime Text

# 2. 添加条目（最后一个键值对后面加逗号 + 新键值对）
{
  "..."
  "Old English Text": "新中文文本",
  "Another English Phrase": "另一段中文"
}

# 3. 生成 JS 产物
cd patch && python gen_dict_js.py

# 4. 验证
node --check zh_dict.js

# 5. 部署（UAC 提权）
powershell -Command "Start-Process -FilePath 'patch\_deploy_dict2.bat' -Verb RunAs -Wait"
cat $env:TEMP\lmszh_dict2.log
# 应看到 COPY_OK + DST_SIZE + SRC_SIZE 三个值相同

# 6. 重启 LM Studio 验证
```

#### 方式 B：写增量脚本（批量补字典）

```python
# patch/add_dict_roundXX.py
import json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)

PATH = r'patch\zh_dict.json'
d = json.load(open(PATH, encoding='utf-8', newline=''))

new_entries = {
    "My New English Text": "我的新中文文本",
    "Another One": "另一个",
    # ... 批量补
}

added = 0
for k, v in new_entries.items():
    if k in d:
        print(f'skip (exists): {k!r}')
        continue
    d[k] = v
    added += 1

print(f'added: {added}, total: {len(d)}')
open(PATH, 'w', encoding='utf-8', newline='').write(
    json.dumps(d, ensure_ascii=False, indent=2) + '\n'
)
```

```bash
# 部署流程同方式 A
```

### 字典条目编写原则

| 场景 | 规则 |
|---|---|
| 单个 UI 标签 | 完整字符串作为 key（"Stop server (Ctrl + .)"） |
| JSX children 数组拆分的文本 | 每个独立段分别作为 key（"Press "、"Ctrl + "、"L to load a model"） |
| 模板字符串前缀 | 不加字典，用 `lms-zh-patch.js` 的 `TEMPLATE_RULES`（如 `More from ${author}`） |
| 大小写敏感 | 字典精确匹配，"Stateful Chats" 和 "stateful chats" 是两条 |
| 含空格的字符串 | **保留末尾空格**（"Status: " 不是 "Status:"） |
| 含变量的字符串 | 两种方案：① 字典分条（"Press " + "Ctrl + " + "L to load a model"）② 模板规则（`^More from (.+)$`） |
| 状态词（On/Off/Yes/No） | 全收——v1.6 字典补丁的 `closest(code/pre/...)` 跳过逻辑保护代码块 |

### 字典补丁版本号管理

`patch/lms-zh-patch.js` 顶部注释 + `console.info` 都要更新：

```javascript
/*!
 * LM Studio 中文汉化补丁层 v1.7
 * ...
 * v1.8 升级:
 *   - 你的变更说明
 */
...
console.info('[lms-zh] patch v1.8 loaded, dict size:', dictKeys.length);
```

---

## 版本迁移

### 场景：LM Studio 升级到新版本

LM Studio 升级流程会**覆盖** `main_window.js`（文档汉化）和可能修改 `index.html`（注入标记丢失）。字典补丁通常不受影响。

#### 步骤 1：备份新版本 bundle

```bash
# 1. 关闭 LM Studio
taskkill /F /IM "LM Studio.exe"

# 2. 备份新 bundle
copy /Y "C:\Program Files\LM Studio\resources\app\.webpack\renderer\main_window.js" \
        "backups\main_window.predocs.vXXX.bak"  # vXXX = 新版本号

# 3. 备份新 index.html
copy /Y "C:\Program Files\LM Studio\resources\app\.webpack\renderer\index.html" \
        "backups\index.html.vXXX.bak"
```

#### 步骤 2：抽取新版本英文文档

```bash
cd "C:\Users\Administrator\Desktop\workspace\LM Studio Chinese\patch"

# 重新抽取（会覆写 docs_src/*.md）
python extract_docs.py

# 查看清单
python -c "
import json, os
m = json.load(open('docs_manifest.json', encoding='utf-8'))
print('total docs:', len(m))
print('first 5:')
for e in m[:5]: print(f'  {e[\"pageRelUrl\"]} ({e[\"raw_len\"]} chars)')
"
```

#### 步骤 3：核对差异（哪些是新增的 / 修改的 / 删除的）

```bash
python -c "
import json, os
m = json.load(open('docs_manifest.json', encoding='utf-8'))
zh = set(os.listdir('docs_zh'))
def fname(u): return u.replace('/', '__')

# 缺译文
miss = [e for e in m if fname(e['pageRelUrl']) not in zh]
print('missing translation:', len(miss))
for e in miss: print(f'  {e[\"pageRelUrl\"]} ({e[\"raw_len\"]} chars)')

# 多余译文（可能是官方删除的 doc）
ph = {fname(e['pageRelUrl']) for e in m}
extra = [f for f in zh if f not in ph]
print('orphan (no longer in bundle):', len(extra))
for f in extra: print(f'  {f}')
"
```

#### 步骤 4：翻译新增文档

按 `1_dev/2_rest/quickstart.md` 等路径模式，逐篇翻译到 `docs_zh/<name>.md`。

**翻译原则**（详细见 `validate_docs.py` 与 `check_code_blocks.py` 文档字符串）：
- **代码块逐字节保留**（真代码围栏）
- `lms_code_snippet` 标签可译（如 `Python (convenience API)` → `Python（便捷 API）`）
- `lms_params` 块标量（`description: |` 后的多行）可译；其余结构保留
- 图片 `src` 路径、链接 URL、命令名保留原样

#### 步骤 5：验证 + 注入

```bash
# 校验结构
python validate_docs.py

# 校验代码块
python check_code_blocks.py

# 注入（UAC）
powershell -Command "Start-Process -FilePath '_apply_docs.bat' -Verb RunAs -Wait"
cat $env:TEMP\lmszh_docs_apply.log

# 查看注入结果
python apply_docs_zh.py report
# 应看到 applied=N, already-zh=M, total=156
```

#### 步骤 6：注入 index.html 标记

```bash
# 如果新版 index.html 丢失了注入，手工在 <script src="main_window.js"></script> 后插入:
#   <script src="zh_dict.js"></script>
#   <script src="lms-zh-patch.js"></script>
# （如果未来加回翻译模块，追加 <script src="lms-zh-translate.js"></script>）
```

```bash
# 推荐方式：写脚本统一处理
python -c "
INSTALLED = r'C:\Program Files\LM Studio\resources\app\.webpack\renderer\index.html'
t = open(INSTALLED, encoding='utf-8', newline='').read()
if 'zh_dict.js' not in t:
    t = t.replace(
        '<script defer=\"defer\" src=\"main_window.js\"></script>',
        '<script defer=\"defer\" src=\"main_window.js\"></script>'
        '<script src=\"zh_dict.js\"></script>'
        '<script src=\"lms-zh-patch.js\"></script>'
    )
    open(INSTALLED, 'w', encoding='utf-8', newline='').write(t)
    print('injected')
else:
    print('already injected')
"
```

#### 步骤 7：扫描新版本的 UI 漏译

```bash
cd analysis
python scan_missing.py > scan_round52.txt  # 输出本次扫描结果
# 重点看 out/missing_p1.txt + out/missing_i18n.txt
# P1 是真 UI，i18n 残留是官方未覆盖的 i18n key
```

新发现的 UI 漏译 → 补字典 → 重新生成 → 部署 → 验证。

---

## 调试遗漏

### 运行时诊断（DevTools Console）

打开 LM Studio DevTools Console（`Ctrl+Shift+I`），运行：

```javascript
__zhPatchCount       // 命中数
__zhDictMiss         // 未命中样本（仅记录前 1000 个）
__zhDebug()          // 输出完整诊断（含 dict size、命中分布、容器类型统计）
```

典型场景：

```javascript
// 场景 1：刚装好补丁但全部 UI 没翻
__zhDictMiss.length === 0
// → 可能 dict 为空或被覆盖，检查 zh_dict.js 加载顺序

// 场景 2：某个具体标签没翻
__zhDictMiss.find(x => x.text === 'My UI Label')
// → bundle 实际是 'My UI Label' 但字典的 key 是 'My UI label'（大小写不一致）

// 场景 3：想看页面被处理过多少次
__zhPatchCount  // 应随交互递增
```

### 静态扫描（项目端）

```bash
cd analysis
python scan_missing.py
# 生成 out/missing_p1.txt + missing_p2.txt + missing_p3.txt + missing_i18n.txt
```

输出说明：
- **P1 明确 UI**：标签页/按钮/状态词（可补字典）
- **P2 疑似 UI**：可能是 UI 但需人工核实（端点/标识符混入）
- **P3 内部消息**：JS 内部错误/调试（保留原文）
- **i18n 残留**：官方 i18n 未覆盖的英文值（补字典即翻）

### Dev Palette 过滤

LM Studio 内置了一个开发者调试面板（默认隐藏），其字符串混入 P1 列表：
- 定位：bundle 模块 1310（@26231774-27586900）
- 过滤脚本：`analysis/filter_p1.py`

```bash
# 过滤后剩 393 条 P1（去除 145 条 Dev Palette 专用）
python filter_p1.py
```

### 模板字符串处理

JSX 模板字符串 `` `More from ${author}` `` 渲染为单一 textNode（变量部分不可整段匹配），需要在 `lms-zh-patch.js` 的 `TEMPLATE_RULES` 里加正则：

```javascript
var TEMPLATE_RULES = [
  [/^More from (.+)$/, '来自 $1'],
  [/^Delete folder "(.+)"$/, '删除文件夹 "$1"'],
  // 新增规则示例：[/^你的英文前缀 (.+)$/, '你的中文前缀 $1'],
];
```

正则格式：`$1` / `$2` 引用捕获组（即变量保留部分）。

### 大小写问题

字典精确匹配 "Stateful Chats" 但 bundle 是 "stateful chats"，两条都要加：

```json
{
  "Stateful Chats": "有状态聊天",
  "stateful chats": "有状态聊天"
}
```

### CSS 防换行失效

如果中文短词竖排显示（"集成" → "集"/"成"），确认：

```javascript
// DevTools Console
document.getElementById('__zh_lms_css')
// 应返回 <style> 节点，包含 white-space:nowrap
```

如果返回 `null`：
- 检查 `lms-zh-patch.js` 是否在 `main_window.js` 之前加载（index.html 注入顺序）
- 检查补丁是否被新版 LM Studio 覆盖

---

## 新增翻译条目工作流

### 场景：用户反馈某个 UI 标签未翻

#### 步骤 1：定位 bundle 实际字面量

```bash
cd analysis
# 1. 在 DevTools Console 复制未翻的英文
# 假设是 "Download (1.2 GB)"
# 2. 在 bundle 里搜
python -c "
import sys,io
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8',write_through=True)
src=open(r'C:\\Program Files\\LM Studio\\resources\\app\\.webpack\\renderer\\main_window.js',encoding='utf-8',errors='replace').read()
kw='Download (1.2 GB)'
i=src.find(kw)
print(f'@{i}:')
if i>=0: print(repr(src[max(0,i-100):i+len(kw)+100]))
"
```

注意：bundle 可能用 unicode 转义、单引号、模板字符串、JSX 数组等不同形态。

#### 步骤 2：判断匹配形态

| Bundle 形态 | 处理方式 |
|---|---|
| `"Download"` （双引号文本字面量） | 直接补字典 |
| `'Download'` （单引号文本字面量） | 直接补字典 |
| `` `Download ${size}` ``（模板字符串） | 加 `TEMPLATE_RULES` 正则 |
| `["Download ", size]`（JSX 数组） | 拆为多条字典："Download " / 后续单独处理 |
| `i18n.t("download.button")` （i18n key） | 看官方 zh-CN 是否翻译，没 → 补字典 |
| `\u0044\u006f\u0077\u006e\u006c\u006f\u0061\u0064` （unicode 转义） | 字典无解，需分析 |

#### 步骤 3：补字典并部署

```bash
cd "C:\Users\Administrator\Desktop\workspace\LM Studio Chinese\patch"
# 直接编辑 zh_dict.json 或写 add_dict_roundXX.py
python gen_dict_js.py
node --check zh_dict.js

# UAC 部署
powershell -Command "Start-Process -FilePath '_deploy_dict2.bat' -Verb RunAs -Wait"
cat $env:TEMP\lmszh_dict2.log

# 重启 LM Studio 验证
```

#### 步骤 4：复扫

```bash
cd analysis
python scan_missing.py
# 应看到 P1 数量下降
```

---

## 诊断工具

### 主要脚本清单

| 脚本 | 作用 |
|---|---|
| `analysis/scan_missing.py` | 主扫描器（4 档分级） |
| `analysis/extract_doc_meta.py` | 提取文档元数据（title/description） |
| `analysis/filter_p1.py` | Dev Palette 区域过滤 |
| `analysis/split_p1.py` | 按文件分布分拣 |
| `analysis/scan_all_ui.py` | 全量 UI 文本扫描 |
| `analysis/scan_specifier.py` | 找 IPC 菜单通道 |
| `analysis/extract_dicts.py` | 字典抽取 |
| `patch/check_code_blocks.py` | 代码块强校验 |
| `patch/validate_docs.py` | 文档结构校验 |
| `patch/apply_docs_zh.py report` | 注入状态报告 |
| `patch/gen_dict_js.py` | JSON → JS 编译器 |

### 备份检查

```bash
ls -la backups/
# 关键备份：
#   main_window.predocs.bak    # 文档汉化前（rollback 用）
#   main_window.js.bak          # 第 1 轮原始
#   index.html.bak              # 注入前原版
```

如果备份被误删，需要：
1. 重新安装 LM Studio 到临时目录
2. 复制临时目录的 `main_window.js` / `index.html` 作为新基线
3. 在原目录重新部署补丁

### bundle 升级检测脚本

```bash
# 检测当前安装目录 bundle 与备份的差异
python -c "
import hashlib
def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()

INSTALLED = r'C:\\Program Files\\LM Studio\\resources\\app\\.webpack\\renderer\\main_window.js'
BAK = r'C:\\Users\\Administrator\\Desktop\\workspace\\LM Studio Chinese\\backups\\main_window.predocs.bak'

print('installed:', md5(INSTALLED))
print('backup:   ', md5(BAK))
# 如相同 = 没被升级；不同 = 已升级，需要重新部署文档汉化
"
```

---

## 常见问题

### Q：部署后 UI 仍英文？
A：检查 `index.html` 注入顺序——`<script src="zh_dict.js"></script>` 必须在 `<script src="main_window.js"></script>` 之后（事实是之后，因为是同步脚本，但 `main_window.js` 是 `defer`）。

实际正确顺序：
```html
<script defer="defer" src="main_window.js"></script>  <!-- defer，先加载但延后执行 -->
<script src="zh_dict.js"></script>                    <!-- 同步，立即执行，定义 __ZH_DICT__ -->
<script src="lms-zh-patch.js"></script>               <!-- 同步，立即执行，使用 __ZH_DICT__ -->
```

### Q：补丁污染了代码块？
A：v1.6 字典补丁的 `closest(code/pre/...)` 跳过逻辑保护代码块。如果某条字典 key 出现在文档示例代码里，**字典仍会匹配**——这是已知风险。处理方式：将该 key 从字典中移除，或调整代码示例使其不再使用该英文短语。

### Q：bundle 文件大小变化？
A：`main_window.js` 应**只增不减**（字典汉化是内容替换，长度可能变化）。字节对比应只关注"体外"是否一致。

### Q：UAC 部署失败？
A：
1. 确认 LM Studio 已完全退出（tasklist 检查）
2. 确认 `backups\main_window.predocs.bak` 存在
3. 确认目标路径在 `C:\Program Files\LM Studio` 下（其他路径需修改部署脚本）
4. 看 `%TEMP%\lmszh_dict2.log` 或 `lmszh_docs_apply.log` 详细错误

### Q：翻译模块能否恢复？
A：第 35 轮下线后保留了 `patch/lms-zh-translate.js` 源码 + `backups/index.html.translate.bak` 备份。恢复方法：

```bash
# 1. 还原 index.html
copy /Y "backups\index.html.translate.bak" "C:\Program Files\LM Studio\resources\app\.webpack\renderer\index.html"

# 2. 复制翻译模块
copy /Y "patch\lms-zh-translate.js" "C:\Program Files\LM Studio\resources\app\.webpack\renderer\lms-zh-translate.js"

# 3. 重启 LM Studio
```

**警告**：翻译模块会调用在线翻译后端（Google / LM Studio / Ollama），恢复前请评估隐私影响。