# LM Studio 中文汉化 - 经验总结

> 51 轮迭代沉淀下来的工程经验、架构决策、踩坑教训
>
> 适用于所有"对闭源 Electron 应用做本地化"的类似项目

---

## 核心铁律（项目总纲）

### 铁律 1：**汉化最坏=没翻译，绝不能=功能没了**
- 任何补丁若破坏现有功能，立即回滚
- 用户对"功能缺失"的容忍度远低于"翻译缺失"
- 例：第 37 轮移植 CSS 防换行时，若影响布局立即回退

### 铁律 2：**绝不碰主 bundle**
- LM Studio 主 bundle 用 `webpack-obfuscator` 混淆字符串查表
- 任何注入字典的尝试都会让主进程崩溃
- 原因：obfuscator 函数被高频调用，每次重复 `const` 声明触发 `SyntaxError`
- 同类项目（VSCode、Discord 等）也适用此规则

### 铁律 3：**不动 bundle 字节布局**
- 只通过字典匹配（patch 模式）或字符串体替换（content 模式）改 bundle
- bundle 的 webpack 模块结构、变量名、函数签名**绝对不能动**
- 升级兼容性靠"字典可复用 + 文档重新抽取"实现

---

## 一、四条渲染路径（Electron 应用的 5 类 UI 来源）

LM Studio 的 UI 文本来自 5 个完全不同的渲染路径，每条路径需要不同翻译策略：

| 路径 | 表现 | 翻译手段 | 项目实现 |
|---|---|---|---|
| **React DOM 文本/属性** | 普通页面文字 | DOM 字典补丁 | `lms-zh-patch.js` v1.7 |
| **react-contexify ShadowRoot** | 部分右键菜单 | DOM 字典补丁 + ShadowRoot 穿透 | 同上 |
| **Electron 原生菜单（renderer 端）** | 三点菜单、内嵌菜单 | 字节级 patch renderer `n()` / `o()` 函数体 | `patch/patch_native_menus.py`（第 30 轮） |
| **Electron 原生菜单（main 进程端）** | 任务栏托盘菜单 | **放弃**（主 bundle 混淆） | 无 |
| **Chromium 内置菜单** | 输入框右键（Undo/Cut/Copy/Paste） | **放弃**（不可达） | 无 |

### 路径诊断方法
```bash
# 看 bundle 里此字符串的渲染位置
python -c "
src=open(r'C:\\Program Files\\LM Studio\\resources\\app\\.webpack\\renderer\\main_window.js',encoding='utf-8',errors='replace').read()
kw='Stop server'  # 待诊断的字符串
i=src.find(kw)
print(repr(src[max(0,i-300):i+len(kw)+150]))
"

# 重点看周围 300 字符：
# - children:\"Stop server\" → React DOM 路径
# - shadowRoot.appendChild(...) → react-contexify 路径
# - label:\"Stop server\" → Electron 原生菜单路径
# - 搜不到 → 主进程 bundle 或外部资源
```

---

## 二、字典补丁层设计

### 三个核心功能（v1.7）

#### 功能 1：DOM textNode 精确匹配
```javascript
function translateTextNode(node) {
  var v = node.nodeValue;
  if (!isPlainEnglish(v)) return;
  var r = dict[v] || dict[v.trim()];      // 双匹配（raw + trim）
  if (!r) { r = tryTemplate(v.trim()); }  // 模板字符串兜底
  if (r && r !== v) {
    node.nodeValue = r;
    window.__zhPatchCount++;
  }
}
```

#### 功能 2：ShadowRoot 穿透
react-contexify 的 ContextMenu 默认 `useShadowDOM=true`，DOM 树在 ShadowRoot 内：
```javascript
function collectRoots() {
  var roots = [document.body];
  // 遍历所有 ShadowRoot 加入扫描队列
  document.querySelectorAll('*').forEach(function(el) {
    if (el.shadowRoot) roots.push(el.shadowRoot);
  });
  return roots;
}
```

#### 功能 3：模板字符串前缀规则
JSX 模板字符串 `` `More from ${author}` `` 渲染为单一 textNode：
```javascript
var TEMPLATE_RULES = [
  [/^More from (.+)$/, '来自 $1'],
  [/^Delete folder "(.+)"$/, '删除文件夹 "$1"'],
];
function tryTemplate(v) {
  for (var i = 0; i < TEMPLATE_RULES.length; i++) {
    var m = TEMPLATE_RULES[i][0].exec(v);
    if (m) return TEMPLATE_RULES[i][1].replace(/\$(\d)/g, function(_, n) {
      return m[parseInt(n)];
    });
  }
  return null;
}
```

### 跳过逻辑（保护代码块）

```javascript
function inSkippedContext(p) {
  while (p && p !== document.body) {
    if (/^(CODE|PRE|KBD|SAMP|VAR)$/.test(p.nodeName)) return true;
    if (p.isContentEditable) return true;
    // 向上查找含 className="language-*" 的容器
    if (p.className && /(?:^|\s)language-\w+/.test(p.className)) return true;
    p = p.parentNode;
  }
  return false;
}
```

**为什么重要**：通用短词（Yes/No/On/Off/Status/Active/Inactive）会出现在文档代码示例里，不跳过会破坏文档。

### CSS 防换行（v1.6 移植）

```javascript
(function injectZhCss() {
  var s = document.createElement('style');
  s.id = '__zh_lms_css';
  s.textContent =
    'button,[role="button"],a,label,[class*="Button"],[class*="Btn"],' +
    '[class*="Tab"],[class*="Heading"],[class*="Title"],[class*="Header"],' +
    '[class*="Label"],[class*="Caption"],[class*="NavLink"]{white-space:nowrap}' +
    '[class*="flex"]>[class*="grow"],[class*="flex"]>[class*="shrink"]{min-width:0}';
  document.head.appendChild(s);
})();
```

**为什么需要**：中文短词（"集成"、"搜索"、"配置"）按字换行（"集"/"成" 竖排）会破坏布局。CSS 强制 `white-space:nowrap` 解决。

---

## 三、文档汉化架构

### 文档数据结构（嵌套）

```javascript
e.documentationArticles = {
  "api-changelog.md": {
    metadata: { title: "API 更新日志", description: "LM Studio API 的历史更新记录", index: 0 },
    prettyName: "API 更新日志",
    sectionPrettyName: "开发者",
    content: "# LM Studio 0.4.1\n\n## Anthropic 兼容 API...",
    pageRelUrl: "1_developer/api-changelog.md"
  },
  // ... 156 篇
}
```

### 关键发现

1. **`pageRelUrl` 是唯一稳定 ID**——用于文档间互链，不能改
2. **content 混用单引号与双引号**——抽取器必须兼容两种
3. **content 字符串体可用 JS 转义**——注入时要正确处理 `\n`、`\t`、`\r`、`\\`、`\'`、`\"` 等
4. **bundle 是 CRLF 文本**——Python 读写必须 `newline=''`，否则 universal-newline 把 `\r\n` 归一化丢失 487 个 `\r`

### 抽取算法（`extract_docs.py`）

```python
# 从 pageRelUrl 反向定位（O(n) 但快）
for pageRelUrl_match in re.finditer(r'pageRelUrl:"([^"]+)"', src):
    url = pageRelUrl_match.group(1)
    pos = pageRelUrl_match.start()
    # 向前找最近的 content:' 开头
    window = src[max(0, pos - 120000):pos]
    k = window.rfind('content:')
    while k >= 0:
        j = max(0, pos - 120000) + k + len('content:')
        # 跳过空白
        while src[j] in ' \t': j += 1
        # 必须是单引号或双引号
        if src[j] in '\'"':
            # 找闭合（处理 JS 转义）
            end = find_str_end(src, j)
            # 校验：闭合后必须是 ,pageRelUrl:"<url>"
            if src[end+1:end+1+len(',pageRelUrl:"%s"' % url)] == ',pageRelUrl:"%s"' % url:
                # 找到！抽取并转义解码
                raw = src[j+1:end]
                text = unesc(raw)
                write(text)
                break
        k = window.rfind('content:', 0, k)
```

**为什么反向定位**：
- 正向扫描所有 `content:` 会超时（bundle 35MB）
- 反向定位（pageRelUrl → content）只需要 156 次扫描，每次限定 120KB 窗口
- 实测：1.5 秒完成 156 篇抽取

### 注入算法（`apply_docs_zh.py`）

```python
# 按 pageRelUrl 就地替换 content 字符串体
def inject_doc(src, url, new_content):
    # 找到 content 字符串的起始和结束位置
    a, b = locate_content_range(src, url)
    if a < 0:
        return src, 0

    # 用原文的引号风格
    q = src[a]  # 单引号或双引号
    old = src[a+1:b]

    # 编码为 JS 字符串字面量
    new_esc = esc(new_content, q)  # 转义 \n \t \r \\ \' \"

    # 从后往前替换（避免偏移失效）
    return src[:a+1] + new_esc + src[b:], len(new_content)
```

**幂等性保证**：先比较 `src[a+1:b]` 与 `esc(text, q)`，相同则跳过。多次运行结果一致。

### 严格校验（patch/check_code_blocks.py + patch/validate_docs.py）

`analysis/_verify_docs_install.py` 的三道独立校验已分别迁入：
- **结构校验** → `patch/validate_docs.py`（围栏/链接/标题/图片/表格）
- **代码块逐字节一致** → `patch/check_code_blocks.py`（按围栏类型分别判定）
- **注入状态** → `patch/apply_docs_zh.py report`（应 already-zh=156）

```python
# 三道独立校验
def verify(backup, installed):
    # 1. 定位：156 篇都能定位，顺序不变
    docs_a = locate(backup)
    docs_b = locate(installed)
    assert_same_order(docs_a, docs_b)

    # 2. 体外字节一致：除 content 外所有字节完全相同
    for url, a, b in sorted(docs_b, key=lambda x: -x[1]):
        installed = installed[:a] + '<<B>>' + installed[b:]
    for url, a, b in sorted(docs_a, key=lambda x: -x[1]):
        backup = backup[:a] + '<<B>>' + backup[b:]
    assert backup == installed

    # 3. 体内容与中文 md 逐字节相符
    for url, a, b in docs_b:
        zh_path = 'docs_zh/' + url.replace('/', '__')
        text = open(zh_path, encoding='utf-8').read()
        body = installed[a:b]
        assert body == esc(text, q)
```

**为什么三道独立校验**：
- 定位校验：确保所有文档仍能识别
- 体外一致：确保未误改其他字节
- 体内容：确保翻译正确写入

---

## 四、踩坑教训（精选）

### 教训 1：bundle 是 CRLF，不能用 universal-newline

```python
# 错误：丢 487 个 \r（universal-newline 默认开启）
src = open(BUNDLE, encoding='utf-8').read()  # ❌
open(BUNDLE, 'w', encoding='utf-8').write(new_src)  # ❌

# 正确：禁用 newline 转换
src = open(BUNDLE, encoding='utf-8', newline='').read()  # ✅
open(BUNDLE, 'w', encoding='utf-8', newline='').write(new_src)  # ✅
```

**症状**：写入后 bundle 字节数减少，bundle 不能正确解析。

### 教训 2：JSX 数组 vs 模板字符串

```javascript
// 数组形式：拆成多个 textNode（每段独立）
["Press ", platform.isMac ? "⌘" : "Ctrl + ", "L to load a model"]
// 字典需要 3-4 条："Press " / "⌘" / "Ctrl + " / "L to load a model"

// 模板字符串形式：拼成 1 个 textNode（整段匹配）
`Stop server (Ctrl + .)`  // 字典只需要 1 条
```

**诊断方式**：
```python
# 看 children 是 [..] 还是字符串
if 'children:[' in src[k:k+100]:
    # 数组形式 → 拆字典
elif 'children:`' in src[k:k+100]:
    # 模板字符串 → 整段匹配
elif 'children:"' in src[k:k+100]:
    # 字符串字面量 → 整段匹配
```

### 教训 3：CSS uppercase ≠ bundle 大写字面量

```javascript
// bundle 实际：
<span className="uppercase">{children}</span>  // children 是 "Params"（小写）

// CSS uppercase 把它显示成 "PARAMS"

{"Params"}  // ✅ 字典应加 "Params"
{"PARAMS"}  // ❌ 永远不命中
```

**诊断方式**：grep `text-transform:uppercase` 或 `className="uppercase"`，看 children 字段的小写字面量。

### 教训 4：bundle CRLF + Python 写入 = 字节不一致

```python
# Python 写文件默认会把 \n 转为系统换行符（Windows: \r\n）
# bundle 是 \r\n，读用 'r'，写用 'w' 会保持 CRLF
# 但若 bundle 内部某处只有 \n（少数情况），写回会被改为 \r\n
# → 字节数变化，node --check 可能通过但解析可能异常
```

**解决方案**：始终用 `newline=''` 禁用 newline 转换。

### 教训 5：truncate tail != truncate head

```python
# 错误：v1.3 scheduleAttrRetry 死代码
function scheduleAttrRetry() {
  run._manual = true;  // 设置标志
  run();                // 调用 run()，但 run() 用的是局部变量 _manual
}
// 结果：标志永远不起作用

# 正确：v1.4 修复
function scheduleAttrRetry() {
  manualRun();  // 直接调用 manualRun()
}
```

### 教训 6：regex 在 heredoc 中被二次转义

```bash
# bash -c "..." 里的反斜杠会被双重解释
python -c "
import re
re.search(r'variants:\n', text)  # ❌ 静默失效
"

# 正确：用 Write 写成 .py 文件
python my_script.py  # ✅
```

### 教训 7：UAC 部署的 false-positive

```powershell
# 错误：UAC 提权后 cwd 非工作区
Start-Process -FilePath "patch\_deploy_dict.bat" -Verb RunAs -Wait
# → 提权后 cmd 的 cwd 变成 system32，bat 里的相对路径全失败

# 正确：bat 内全用绝对路径
set SRC=D:/Workspace/LM Studio Chinese\patch\zh_dict.js
set DST="C:\Program Files\LM Studio\resources\app\.webpack\renderer\zh_dict.js"
```

### 教训 8：回滚的连锁反应

```bash
# 错误：rollback 一次后无法二次 rollback
python apply_docs_zh.py rollback   # 把 main_window.js 改回 35485062B
# 此时若再次 apply，不会报错（因为 dict 没变），
# 但若版本号变了，apply 会因 pageRelUrl 不匹配而失败
```

**解决方案**：rollback 前先 `apply_docs_zh.py report`，确认 `already-zh` 数字。

---

## 五、性能优化

### 性能 1：反向定位 vs 正向扫描

```python
# 慢：正向扫描 35MB 找所有 content:
content_count = src.count('content:')  # 156 次
# 每次 35MB 全扫 → 156 * 35MB = 5.5GB 读取

# 快：反向定位（pageRelUrl → content）
for url in urls:  # 156 次
    window = src[max(0, pos - 120000):pos]  # 只扫 120KB
# 总读取 156 * 120KB = 18MB
```

**实测**：抽取 156 篇从 60 秒（正向）降到 1.5 秒（反向）。

### 性能 2：从后往前替换

```python
# 错误：从前往后替换（偏移失效）
for url, a, b in docs:
    src = src[:a] + new + src[b:]  # b 已变化，后续定位错误

# 正确：从后往前替换（偏移稳定）
for url, a, b in sorted(docs, key=lambda x: -x[1]):  # 按 a 倒序
    src = src[:a] + new + src[b:]
```

### 性能 3：TreeWalker vs querySelectorAll

```javascript
// 慢：querySelectorAll 收集所有 textNode
var nodes = document.querySelectorAll('*');  // O(n²)
nodes.forEach(collect_text_nodes);

// 快：TreeWalker
var tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, null);
while (tw.nextNode()) process(tw.currentNode);  // O(n)
```

---

## 六、字典条目编写最佳实践

### 实践 1：避免添加"bundle 里永远不会出现"的词

```json
// ❌ 错误：游戏分类（bundle 里完全不会出现）
"Match-3 Games": "三消游戏",
"Tile Matching Games": "拼图游戏",
"Building Games": "建造游戏",

// ✅ 正确：只加 bundle 里实际出现的 UI 标签
"Plugins (Beta)": "插件（Beta）",
"Loading the model, progress:": "正在加载模型，进度：",
```

**判断方式**：grep 整个 bundle 确认条目出现位置。

### 实践 2：JSX 数组拆分 vs 整段匹配

```python
# 整段优先（如有则用它）
{"Stop server (Ctrl + .)": "停止服务器 (Ctrl + .)"}

# JSX 数组拆分
{"Press ": "按 "}
{"Ctrl + ": "Ctrl + "}  # 保留原文
{"⌘": "⌘"}  # 保留原文
{"L to load a model": "L 加载模型"}
```

### 实践 3：模板字符串 vs 字典

```javascript
// 模板字符串（含变量）：用 TEMPLATE_RULES
{`More from ${author}`}
// → /^More from (.+)$/ → '来自 $1'

// 字符串字面量（无变量）：用字典
{`Loading ${count} items...`}
// → "Loading items...:": "加载 {count} 个项目..."
```

### 实践 4：大小写要精确

```python
# ❌ 错误：以为大写小写都能命中
{"Stateful Chats": "有状态聊天"}

# ✅ 正确：大小写分别补
{"Stateful Chats": "有状态聊天"}  # 设置页出现
{"stateful chats": "有状态聊天"}  # 文档正文出现
```

### 实践 5：保留末尾空格

```python
# 模板字符串末尾空格重要
{"capacity of ": "容量 "}  # ✅ 保留
{"capacity of": "容量"}    # ❌ 永远不命中
```

---

## 七、版本兼容策略

### 兼容性矩阵

| 组件 | 跨版本兼容性 | 失效原因 | 修复方法 |
|---|---|---|---|
| `zh_dict.js` | **95% 可复用** | 官方可能调整 UI 文案 | 复扫 + 补字典 |
| `lms-zh-patch.js` | **100% 可复用** | 纯 JS，与 bundle 无关 | 无需改动 |
| `index.html` 注入 | **90% 可复用** | 升级可能改 index.html 模板 | 重新注入 2 个 `<script>` |
| `main_window.js` 文档汉化 | **0% 可复用** | content 字符串被官方重新生成 | 重新抽取 + 翻译 + 注入 |

### 升级迁移流程（5 分钟）

```
升级 LM Studio
   ↓
备份新版本 bundle → backups/main_window.predocs.vXXX.bak
   ↓
python extract_docs.py       # 重新抽取英文文档
   ↓
python -c "..."               # 找出新增/缺失的文档
   ↓
人工翻译新文档到 docs_zh/    # 通常仅 0-5 篇新增
   ↓
python validate_docs.py      # 结构校验
python check_code_blocks.py  # 代码块强校验
   ↓
python apply_docs_zh.py       # 注入文档汉化
   ↓
python scan_missing.py        # 扫描新版本 UI 漏译
   ↓
补字典 → 部署 → 验证
```

---

## 八、调试常见问题

### Q：补丁加载但 UI 不翻？

```javascript
// DevTools Console 检查
__zhPatchCount    // 应 > 100（命中数）
window.__ZH_DICT__  // 应是对象且 size > 1000
```

可能原因：
1. `index.html` 注入顺序错（lms-zh-patch.js 在 zh_dict.js 之前）
2. `lms-zh-patch.js` 被新版 LM Studio 覆盖
3. 字典文件未部署

### Q：字典命中但 UI 仍显示原文？

```javascript
__zhDictMiss.find(x => x.text === 'My UI Label')
// 返回 undefined → 字典有，但被跳过逻辑拦截
// 返回 {text: 'My UI Label'} → 字典没有这条
```

### Q：升级后字典不命中？

```python
# 找出 bundle 实际字符串
import re
src = open(r'C:\Program Files\LM Studio\resources\app\.webpack\renderer\main_window.js', encoding='utf-8').read()
for m in re.finditer(r'"Stop Server"', src):
    print(repr(src[max(0,m.start()-50):m.end()+50]))
```

很可能官方改了字符串（如 "Stop Server" → "Stop the server"），补字典即可。

### Q：补丁破坏 React？

如果 `__zhPatchCount` 异常低（< 10），可能是补丁破坏了 React 协调：

```javascript
// 检查 React DOM 是否正常
document.getElementById('root').children.length > 0
// 应大于 0
```

如果为 0，立即回滚补丁。

---

## 九、CI/CD 集成建议

### 自动化部署脚本（推荐）

```bash
#!/bin/bash
# deploy_zh.sh - 一键部署（CI 环境用）
set -e

# 1. 关闭 LM Studio
taskkill /F /IM "LM Studio.exe" || true
sleep 2

# 2. 校验 bundle
python analysis/scan_missing.py > /dev/null

# 3. 部署字典（UAC）
powershell -Command "Start-Process -FilePath 'patch\_deploy_dict2.bat' -Verb RunAs -Wait"
[ "$(grep COPY_OK /tmp/lmszh_dict2.log)" ] || exit 1

# 4. 注入文档（UAC）
powershell -Command "Start-Process -FilePath 'patch\_apply_docs.bat' -Verb RunAs -Wait"
[ "$(grep 'done' /tmp/lmszh_docs_apply.log)" ] || exit 1

# 5. 校验
python -c "
import hashlib
def md5(p): return hashlib.md5(open(p,'rb').read()).hexdigest()
INSTALLED = r'C:\\Program Files\\LM Studio\\resources\\app\\.webpack\\renderer\\main_window.js'
BAK = r'backups\\main_window.predocs.bak'
print('installed:', md5(INSTALLED))
"

# 6. 重启 LM Studio（可选）
# "C:\Program Files\LM Studio\LM Studio.exe"
```

### 自动回滚（部署失败时）

```bash
trap 'echo "deploy failed, rolling back..." && python patch/apply_docs_zh.py rollback && del "C:\Program Files\LM Studio\resources\app\.webpack\renderer\zh_dict.js"' ERR
```

---

## 十、贡献指南

### 添加遗漏条目的完整流程

1. **收集样本**：DevTools Console 跑 `__zhDictMiss` 取前 20 条
2. **确认来源**：grep bundle 确认字符串真实存在
3. **判断路径**：React DOM / ShadowRoot / 原生菜单 / 模板字符串
4. **写字典条目**：补充到 `patch/zh_dict.json` 或写 `add_dict_roundXX.py`
5. **生成 + 校验**：`python gen_dict_js.py && node --check zh_dict.js`
6. **UAC 部署**：`_deploy_dict2.bat`
7. **重启验证**：截图确认 UI 已翻
8. **提交 PR**（如项目开源）：包含 diff 和截图

### 代码贡献

- `patch/lms-zh-patch.js` 的 `TEMPLATE_RULES` 补充
- `patch/check_code_blocks.py` 增加新的围栏类型支持
- `analysis/scan_missing.py` 增加新的扫描规则

---

## 附录 A：关键文件字节数演进

```
zh_dict.json:  1699 → 4193 条（+2494，纯人工精选）
zh_dict.js:    90909B → 196406B（+105KB）
lms-zh-patch.js: 8931B → 11570B（v1.5 → v1.7）
main_window.js: 35485062B → 35469794B（文档汉化，体外字节完全一致）
index.html:  2845B → 2743B（注入 2 个 <script> 标签，但移除翻译模块反而 -102B）
```

## 附录 B：51 轮里程碑时间线

```
Round  1-29: 项目奠基 → 1615 字典条 + 双补丁架构
Round 30-35: 精度提升 → 1699 字典条 + 翻译模块下线
Round 36-41: 补丁完善 → 字典补丁 v1.7（含 CSS + 模板规则）
Round 42-44: 文档汉化 → 156 篇开发者文档全译
Round 45-51: 全量扫描 → 4193 字典条（+2494）
```

## 附录 C：项目符号

- 🟢 字典补丁（DOM 路径）
- 🔵 原生菜单补丁（字节级 patch renderer）
- 🔴 主进程路径（永久放弃）
- ⚪ 已知保留（HF README / 托盘菜单 / 输入框右键）