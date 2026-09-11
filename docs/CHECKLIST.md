# LM Studio 中文汉化 - 验证清单

> 部署后逐项打勾，确保汉化覆盖完整

---

## 1. 文件级验证

```bash
# 1.1 三个文件存在
[ -f "C:\Program Files\LM Studio\resources\app\.webpack\renderer\zh_dict.js" ]
[ -f "C:\Program Files\LM Studio\resources\app\.webpack\renderer\lms-zh-patch.js" ]
[ ! -f "C:\Program Files\LM Studio\resources\app\.webpack\renderer\lms-zh-translate.js" ]  # 应不存在
```

```bash
# 1.2 文件大小合理
ls -la "C:\Program Files\LM Studio\resources\app\.webpack\renderer\zh_dict.js"  # ~196KB
ls -la "C:\Program Files\LM Studio\resources\app\.webpack\renderer\lms-zh-patch.js"  # ~11KB
```

```bash
# 1.3 main_window.js 文档汉化已注入
python patch\apply_docs_zh.py report
# 应看到 applied=N, already-zh=156, missing=0
```

---

## 2. 注入顺序验证

打开 `C:\Program Files\LM Studio\resources\app\.webpack\renderer\index.html`，确认：

```html
<script defer="defer" src="main_window.js"></script>
<script src="zh_dict.js"></script>           ← ✅ 必须有
<script src="lms-zh-patch.js"></script>      ← ✅ 必须有
```

❌ 错误顺序：
```html
<script src="lms-zh-patch.js"></script>     ← 在 main_window.js 之前会出错
<script src="zh_dict.js"></script>
```

---

## 3. 运行时验证（DevTools Console）

打开 LM Studio，按 `Ctrl+Shift+I` 打开 DevTools，切换到 Console 标签：

```javascript
// 3.1 字典加载
window.__ZH_DICT__                       // 应是对象，length > 4000

// 3.2 补丁加载
window.__zhPatchLoaded === true          // 应为 true

// 3.3 命中统计
__zhPatchCount > 100                     // 应大于 100（操作几下应该 > 500）

// 3.4 完整诊断
__zhDebug()                              // 输出诊断信息
```

---

## 4. UI 场景验证（按顺序）

### 4.1 启动界面
- [ ] 侧栏 "Integrations" → "集成"（**一行不换行**）
- [ ] 顶部导航 "Discover / Search / Chat" 全部中文
- [ ] 状态栏 "Ready" / "Loaded" 中文显示

### 4.2 开发者文档（156 篇全译）
- [ ] 开发者 → API 更新日志 → 正文全中文
- [ ] 开发者 → REST 概览 → 正文全中文
- [ ] 开发者 → 快速上手 → 代码块标签 `Python (convenience API)` → `Python（便捷 API）`
- [ ] Python 集成 → 22 篇文档中文
- [ ] TypeScript 集成 → 43 篇文档中文（含 Plugins）
- [ ] CLI 参考 → 26 篇文档中文

### 4.3 设置页面
- [ ] 设置 → 外观 → 8 个 Onboarding 标题全部中文（`应用入门引导` / `工具使用入门` / ...）
- [ ] 设置 → 常规 → 全部标签中文
- [ ] 设置 → 高级 → 全部标签中文

### 4.4 模型管理
- [ ] 模型详情 → "Params" → "参数"
- [ ] 模型详情 → "Arch" → "架构"
- [ ] 模型详情 → "Domain" → "模型领域"
- [ ] 模型详情 → "Format" → "格式"
- [ ] 模型详情 → README 标签 → "说明文档"
- [ ] "More from qwen" → "来自 qwen"
- [ ] "Based on estimated model capacity of 8.2 GB" → "基于估算的模型容量 8.2 GB"

### 4.5 模型加载流程
- [ ] 加载按钮 "Load" → "加载"
- [ ] 加载提示 "Loading the model, progress:" → "正在加载模型，进度："
- [ ] 加载完成 "Model loaded successfully" → 中文
- [ ] 工具提示 "Stop server (Ctrl + .)" → "停止服务器 (Ctrl + .)"

### 4.6 聊天界面
- [ ] 输入框 placeholder "Type to filter models." → "输入以筛选模型"
- [ ] 提示 "Press Ctrl + L to load a model" → "按 Ctrl + L 加载模型"
- [ ] 消息工具栏按钮（Send / Copy / Regenerate / Edit）中文
- [ ] 复制消息后 "Copied!" → "已复制！"

### 4.7 发现页（Search / Discover）
- [ ] "Staff Picks that can fit on this device" → "可在当前设备加载的官方推荐模型"
- [ ] 搜索框 placeholder 中文
- [ ] 模型分类筛选器中文

### 4.8 插件页面
- [ ] "Plugins (Beta)" → "插件（Beta）"
- [ ] 安装提示中文
- [ ] 插件详情页中文

### 4.9 编辑器（Monaco）
- [ ] 右键菜单（Cut / Copy / Paste 等）**保持英文**（已知保留：Chromium 内置菜单）
- [ ] 命令面板（Ctrl+Shift+P）标签中文（如有命令）

### 4.10 输入框右键菜单（**已知保留**）
- [ ] 输入框右键 → Undo / Cut / Copy / Paste / Select All 英文显示
- [ ] 样式与 OS 原生一致（这是有意的，不修复）

### 4.11 系统托盘（**已知保留**）
- [ ] 任务栏右键 LM Studio → "Stop Server" / "Copy LLM Server Base URL" 等英文
- [ ] 保持英文（主进程限制）

---

## 5. 高级验证（DevTools Console）

```javascript
// 5.1 检查字典命中分布
__zhPatchCount                            // 命中数
__zhDictMiss.slice(0, 10)                 // 未命中样本前 10 个

// 5.2 字典覆盖率（粗略）
var total = document.querySelectorAll('*').length;
var hits = __zhPatchCount;
console.log('覆盖率（粗略）:', hits, '/', total);

// 5.3 强制刷新补丁
window.__ZH_DICT__ && console.log('字典已加载')
```

---

## 6. 错误检查

### 6.1 DevTools Console 无报错
- [ ] 没有 `Failed to load resource: zh_dict.js` 错误
- [ ] 没有 `lms-zh-patch is not defined` 错误
- [ ] 没有 `Uncaught SyntaxError` 错误

### 6.2 React 树正常
```javascript
document.getElementById('root').children.length > 0  // 应大于 0
```

### 6.3 交互正常
- [ ] 点击按钮有响应
- [ ] 输入框可输入
- [ ] 模型加载/卸载正常
- [ ] 菜单弹出正常

---

## 7. bundle 字节一致性验证（开发端）

```bash
# 7.1 计算安装目录与备份的字节差异
python -c "
import hashlib
def md5(p):
    return hashlib.md5(open(p, 'rb').read()).hexdigest()
INSTALLED = r'C:\\Program Files\\LM Studio\\resources\\app\\.webpack\\renderer\\main_window.js'
BAK = r'C:\\Users\\Administrator\\Desktop\\workspace\\LM Studio Chinese\\backups\\main_window.predocs.bak'
print('installed:', md5(INSTALLED))
print('backup:   ', md5(BAK))
# 不同 = 已升级或未汉化
# 相同 = 已汉化（其他方式如 extract_docs / apply_docs 会修改）
"
```

```bash
# 7.2 严格校验（开发端）— 三道独立校验
cd "C:\Users\Administrator\Desktop\workspace\LM Studio Chinese\patch"
python validate_docs.py           # 文档结构校验（围栏/链接/标题/图片/表格）
python check_code_blocks.py       # 代码块逐字节一致校验
python apply_docs_zh.py report    # 注入状态报告（应 already-zh=156）
```

---

## 8. 卸载验证

```bash
# 8.1 删除字典 + 补丁
del "C:\Program Files\LM Studio\resources\app\.webpack\renderer\zh_dict.js"
del "C:\Program Files\LM Studio\resources\app\.webpack\renderer\lms-zh-patch.js"

# 8.2 还原 main_window.js
python patch\apply_docs_zh.py rollback

# 8.3 还原 index.html（可选）
copy /Y "backups\index.html.bak" "C:\Program Files\LM Studio\resources\app\.webpack\renderer\index.html"

# 8.4 重启验证
# 应看到完整英文 UI
```

---

## 9. 常见问题快速检查

| 症状 | 检查项 |
|---|---|
| 完全不翻 | 1.2 注入顺序；1.3 zh_dict.js 是否部署；3.1 `window.__ZH_DICT__` 是否非空 |
| 部分不翻 | 4.x 章节逐项验证；3.4 `__zhDictMiss` 找出遗漏 |
| 中文竖排 | 1.3 lms-zh-patch.js 是否部署；CSS 防换行是否注入（`document.getElementById('__zh_lms_css')`） |
| 代码块被翻 | 字典补丁的跳过逻辑（应已保护）；若被翻应回滚该字典条目 |
| 输入框右键异常 | 这是 Chromium 原生菜单，已有意保留，**不要尝试修复** |
| 托盘菜单中文 | 不应发生；若是说明部署出错 |

---

## 10. 完成后报告

如果所有 ✓，说明汉化成功。可以向开发者反馈：

```
LM Studio 0.4.24+1 中文汉化已部署完成
- 字典: 4193 条
- 文档: 156 篇
- 字典补丁: v1.7
- 安装目录: C:\Program Files\LM Studio\
- 已知保留: 托盘菜单 / 输入框右键 / HF README / Staff Pick 描述
```

发现新遗漏 → 见 [HANDS_ON.md § 新增翻译条目工作流](HANDS_ON.md#新增翻译条目工作流)