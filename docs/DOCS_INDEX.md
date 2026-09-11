# LM Studio 中文汉化 - 文档导航

> 项目所有文档的入口与导读

---

## 📚 新人必读（按顺序）

1. **[README.md](README.md)**（10 分钟）
   - 项目是什么、覆盖什么、适用版本
   - 一键安装/卸载方法
   - 已知限制与兼容性说明

2. **[CHANGELOG.md](CHANGELOG.md)**（15 分钟）
   - 51 轮迭代完整记录
   - 4 个阶段：项目奠基 / 精度提升 / 文档汉化 / 全量扫描
   - 字典条目演进（0 → 4193）

3. **[HANDS_ON.md](HANDS_ON.md)**（30 分钟，需要时再读）
   - 字典维护实操
   - LM Studio 升级迁移流程
   - 调试遗漏问题
   - 常见问题 Q&A

4. **[HANDS_ON_EXPERIENCE.md](HANDS_ON_EXPERIENCE.md)**（深度阅读）
   - 4 条渲染路径分类
   - 字典补丁层设计哲学
   - 文档汉化架构
   - 10 个踩坑教训

---

## 📂 项目结构总览

```
LM Studio Chinese/
│
├── 📄 README.md                ← 项目总览（先看这个）
├── 📄 CHANGELOG.md             ← 51 轮迭代记录
├── 📄 HANDS_ON.md              ← 开发者指南
├── 📄 HANDS_ON_EXPERIENCE.md   ← 经验总结
├── 📄 LM_Studio汉化深度分析报告.md  ← 第 1 轮分析报告
│
├── 🔧 patch/                   ← 补丁与部署脚本
│   ├── zh_dict.json            ← 4193 字典源
│   ├── zh_dict.js              ← 字典编译产物
│   ├── lms-zh-patch.js         ← 字典补丁 v1.7
│   │
│   ├── gen_dict_js.py          ← JSON → JS 编译器
│   ├── _deploy_dict2.bat       ← UAC 部署入口
│   │
│   ├── extract_docs.py         ← 文档抽取（156 篇英文 → 临时目录，供翻译参考）
│   ├── docs_zh/*.md            ← 中文译文（156 篇，部署唯一依赖）
│   ├── docs_manifest.json      ← 文档清单
│   │
│   ├── apply_docs_zh.py        ← 文档注入/回滚/报告
│   ├── _apply_docs.bat         ← UAC 入口
│   ├── validate_docs.py        ← 结构校验
│   ├── check_code_blocks.py    ← 代码块强校验
│   ├── variant_labels.py       ← lms_code_snippet 标签汉化
│   ├── fix_snippet_newline.py  ← 重建围栏后多余换行修复
│   ├── list_variant_labels.py  ← 标签清单导出
│   │
│   ├── patch_native_menus.py   ← 原生菜单字节补丁（v2 幂等）
│   ├── _deploy_dict2.bat       ← UAC 部署字典+补丁
│   ├── _deploy_only.py         ← 字典部署底层
│   ├── _apply_docs.bat         ← UAC 部署文档汉化
│   ├── _rollback_main.bat/.py  ← 还原主 bundle
│   ├── _remove_translate.py / _remove_translate_run.bat  ← 第 35 轮移除翻译模块
│   ├── lms-zh-translate.js     ← 第 35 轮已下线（仅保留供回滚）
│
├── 🔍 analysis/                ← 诊断工具（只读扫描）
│   ├── scan_missing.py         ← 主扫描器（4 档分级）
│   ├── extract_doc_meta.py     ← 提取文档元数据
│   ├── filter_p1.py            ← Dev Palette 过滤
│   ├── split_p1.py             ← 按文件分拣
│   ├── scan_all_ui.py          ← 全量 UI 文本扫描
│   ├── scan_specifier.py       ← 找 IPC 菜单通道
│   ├── scan_menu_labels.py     ← 菜单标签扫描
│   ├── check_missing.py        ← 缺失条目检查
│   ├── extract_dicts.py        ← 字典抽取
│   ├── find_label_paste.py     ← 粘贴标签查找
│   ├── find_str.py             ← 字符串定位
│   ├── dump_ctx.py / dump_module.py ← 模块上下文 dump
│   ├── scan_ctx_specs.py       ← 上下文规格扫描
│   ├── menu_labels.txt         ← 菜单标签清单
│
├── 💾 backups/                 ← bundle 原始备份（4 个）
│   ├── main_window.predocs.bak ← 文档汉化前（rollback 用，35MB）
│   ├── main_index.js.bak       ← 主进程 bundle 原始备份（25MB）
│   ├── index.html.bak          ← 注入前原版
│   └── index.html.translate.bak ← 含翻译模块注入的 index.html（回滚用）
│
├── 📋 logs/                    ← 部署日志
│
└── 🧠 .workbuddy/memory/       ← 项目长期笔记
    ├── 2026-09-09.md           ← 第 1-29 轮日志
    ├── 2026-09-10.md           ← 第 30-51 轮日志
    └── MEMORY.md               ← 关键经验与决策
```

---

## 🎯 按场景找文档

### 场景：用户反馈某 UI 标签未翻
→ **[HANDS_ON.md § 新增翻译条目工作流](HANDS_ON.md#新增翻译条目工作流)**

### 场景：LM Studio 升级到新版本
→ **[HANDS_ON.md § 版本迁移](HANDS_ON.md#版本迁移)**

### 场景：补丁部署后 UI 不翻
→ **[HANDS_ON.md § 调试遗漏](HANDS_ON.md#调试遗漏)**

### 场景：想理解为什么"集成"按钮按字换行
→ **[HANDS_ON_EXPERIENCE.md § 字典补丁层设计](HANDS_ON_EXPERIENCE.md#字典补丁层设计)**

### 场景：想了解为什么主进程托盘菜单是英文
→ **[HANDS_ON_EXPERIENCE.md § 核心铁律](HANDS_ON_EXPERIENCE.md#核心铁律项目总纲)**

### 场景：想添加新字典条目
→ **[HANDS_ON.md § 字典维护](HANDS_ON.md#字典维护)**

### 场景：需要回滚已部署的补丁
→ **[README.md § 卸载](README.md#卸载)**

### 场景：想用 Python 脚本自动部署
→ **[HANDS_ON_EXPERIENCE.md § CI/CD 集成建议](HANDS_ON_EXPERIENCE.md#cicd-集成建议)**

---

## 📊 关键数字速查

| 项目 | 数字 |
|---|---|
| 字典条目 | **4193 条** |
| 开发者文档 | **156 / 156 篇**（100% 译完） |
| 字典补丁版本 | v1.7（DOM + ShadowRoot + 模板规则 + CSS） |
| bundle 大小 | 35469794B（汉化后） |
| 字典 JS 大小 | 196406B |
| 补丁 JS 大小 | 11570B |
| index.html 改动 | +2 个 `<script>` 标签 |
| 备份文件数 | 8 个 |
| 已知限制项 | 5 类（托盘菜单/输入框右键/HF README/Staff Pick/语种名） |

---

## 🔗 文档版本

- 最后更新：2026-09-10
- 适用版本：LM Studio 0.4.24+1
- 文档语言：中文（与项目一致）