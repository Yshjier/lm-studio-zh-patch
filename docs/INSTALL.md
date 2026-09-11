# LM Studio 中文汉化 - 安装指南

> 给普通用户的极简安装方法
>
> 时间：3-5 分钟
>
> 适用：LM Studio 0.4.24+1（其他版本见末尾）

---

## 一键安装（推荐）

### 步骤 1：完全关闭 LM Studio

```powershell
# 方法 A：在任务管理器结束
# 方法 B：命令行（推荐）
taskkill /F /IM "LM Studio.exe"
```

### 步骤 2：双击运行安装脚本

打开 PowerShell（**以管理员身份**），执行：

```powershell
# 一键全量部署（推荐）：字典 + 补丁 + 原生菜单 + 156 篇中文文档
powershell -Command "Start-Process -FilePath 'C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe' -ArgumentList '\"C:\Users\Administrator\Desktop\workspace\LM Studio Chinese\patch\_deploy_all.py\"' -Verb RunAs -Wait"

# 查看部署日志
type "C:\Users\Administrator\Desktop\workspace\LM Studio Chinese\logs\apply.log"
```

会弹出 UAC 提窗，点击「是」即可。

> ⚠️ **必须提权 python 本体，不能提权 .bat**（提权 bat 会静默失败：返回成功但脚本根本没执行）。
> 判断是否真的跑成功：看 `logs\apply.log` 的**修改时间**是否更新，以及末尾是否出现 `DEPLOY ALL DONE`。

<details>
<summary>备选：分两步部署（旧方式）</summary>

```powershell
# 部署字典补丁（2 个文件复制）
powershell -Command "Start-Process -FilePath 'C:\Users\Administrator\Desktop\workspace\LM Studio Chinese\patch\_deploy_dict2.bat' -Verb RunAs -Wait"

# 部署文档汉化（替换 main_window.js 中 156 个字符串）
powershell -Command "Start-Process -FilePath 'C:\Users\Administrator\Desktop\workspace\LM Studio Chinese\patch\_apply_docs.bat' -Verb RunAs -Wait"
```

</details>

### 步骤 3：重启 LM Studio

启动 LM Studio，UI 应该是中文了。

---

## 验证是否成功

打开 LM Studio 后，按 `Ctrl+Shift+I` 打开开发者工具，在 Console 里输入：

```javascript
__zhPatchCount
```

应大于 100（说明字典补丁工作正常）。

---

## 卸载方法

```powershell
# 1. 关闭 LM Studio
taskkill /F /IM "LM Studio.exe"

# 2. 打开 PowerShell（管理员）
# 删除字典文件
del "C:\Program Files\LM Studio\resources\app\.webpack\renderer\zh_dict.js"
del "C:\Program Files\LM Studio\resources\app\.webpack\renderer\lms-zh-patch.js"

# 3. 还原主文件（命令进入 patch/ 目录）
cd "C:\Users\Administrator\Desktop\workspace\LM Studio Chinese\patch"
python apply_docs_zh.py rollback
```

完成后 LM Studio 回到原版英文 UI。

---

## 常见问题

### Q：UAC 弹窗没出现？
A：检查 PowerShell 是否以管理员身份运行。在开始菜单搜 "PowerShell"，右键 → "以管理员身份运行"。

### Q：执行后 UI 仍英文？
A：
1. 确认 `C:\Program Files\LM Studio\resources\app\.webpack\renderer\` 目录下有 `zh_dict.js` 和 `lms-zh-patch.js` 文件
2. 打开 `index.html`，确认末尾有 `<script src="zh_dict.js"></script>` 和 `<script src="lms-zh-patch.js"></script>`
3. 完全退出 LM Studio（包括托盘），再重新启动

### Q：发现某个英文 UI 没翻译？
A：在 LM Studio DevTools Console（`Ctrl+Shift+I`）跑：
```javascript
__zhDictMiss.slice(0, 10)
```
把输出反馈给开发者，会作为下一轮字典补丁的补充。

---

## 升级 LM Studio 后如何恢复汉化

⚠️ **实测（2026-09-10）**：LM Studio 升级/自动更新会把整个 `renderer/` 目录还原成原版，
**不仅 `main_window.js` 的文档汉化丢失，`zh_dict.js` / `lms-zh-patch.js` / `index.html` 的注入也一起没了**。
表现为：LM Studio 还在运行时界面看着仍是中文（内存残留），**一重启就全变回英文**。

升级后恢复（约 2 分钟）：

```powershell
# 1. 完全关闭 LM Studio（任务管理器确认进程为 0）
taskkill /F /IM "LM Studio.exe"

# 2. 【重要】重建回滚基线 —— 旧基线与新版本不匹配，rollback 会装回错误版本
copy /Y "C:\Program Files\LM Studio\resources\app\.webpack\renderer\main_window.js" `
        "C:\Users\Administrator\Desktop\workspace\LM Studio Chinese\backups\main_window.predocs.bak"

# 3. 一键全量部署（字典 + 补丁 + 原生菜单 + 156 篇文档）
powershell -Command "Start-Process -FilePath 'C:\Users\Administrator\AppData\Local\Programs\Python\Python312\python.exe' -ArgumentList '\"C:\Users\Administrator\Desktop\workspace\LM Studio Chinese\patch\_deploy_all.py\"' -Verb RunAs -Wait"

# 4. 确认日志末尾是 DEPLOY ALL DONE
type "C:\Users\Administrator\Desktop\workspace\LM Studio Chinese\logs\apply.log" | Select-Object -Last 12

# 5. 启动 LM Studio 验证
```

> 💡 第 2 步可以偷懒：`_deploy_all.py` 的第 3 步（`patch_native_menus.py`）会自动把当前原始 bundle
> 备份到 `backups/main_window_native_menu.bak`，部署完把它复制为新的 `main_window.predocs.bak` 即可。
> 但**手动先备份更保险**，因为那是唯一一次能看到纯净新版 bundle 的机会。

### 如果新版文档有变化（新增/改写了英文文档）

```powershell
cd "C:\Users\Administrator\Desktop\workspace\LM Studio Chinese\patch"

# 重新抽取新版英文文档（会重建 docs_src/）
python extract_docs.py

# 找出还没译的
python -c "
import json, os
m = json.load(open('docs_manifest.json', encoding='utf-8'))
zh = set(os.listdir('docs_zh'))
def fname(u): return u.replace('/', '__')
miss = [e for e in m if fname(e['pageRelUrl']) not in zh]
print('missing:', len(miss))
for e in miss: print(' ', e['pageRelUrl'])
"

# 译完放到 docs_zh/ 后，回到上面第 3 步跑 _deploy_all.py
```

详细说明见 [README.md § 兼容性](README.md#兼容性)。

---

## 不支持的版本

- **LM Studio 0.4.24 之前**：未测试，可能不兼容
- **LM Studio 0.4.24+1 之后**：需重新抽取文档（步骤如上），字典大概率仍可用

---

## 已知保留英文的部分

为保持最佳兼容性，以下场景保留英文：

| 场景 | 原因 |
|---|---|
| 任务栏右键 LM Studio 菜单 | 主进程限制（补丁会导致崩溃） |
| 输入框右键菜单（Undo/Cut/Copy/Paste） | Chromium 内置菜单 |
| Hugging Face 模型 README 正文 | 运行时从 HF API 动态拉取 |
| Staff Pick 模型描述 | LM Studio 服务器动态数据 |
| 国际化语种名 | 用户选项而非 UI 文本 |

---

需要帮助请提交 issue 或联系开发者。