# LM Studio 0.4.24+1 汉化补丁 — 部署与回滚说明

本补丁由两部分组成,已全部就位并验证:

| 部分 | 文件 | 作用 |
|---|---|---|
| A. 官方字典补全 | 修改 `renderer/main_window.js` 内嵌 zh_CN 字典 | 补齐官方缺失的 63 个翻译 key(设置/加载参数/开发者端点/模型加载保护等) |
| B. DOM 汉化层 | `renderer/zh_dict.js` + `renderer/lms-zh-patch.js` + 注入 `index.html` | 把官方 i18n 覆盖不到的 ~千处硬编码英文整段替换为中文 |

## 当前状态

- `main_window.js`:已补 63 key,`node --check` 语法通过,抽取复核缺失 = 0;
- `index.html`:已追加两行 `<script src="zh_dict.js">`、`<script src="lms-zh-patch.js">`;
- 词典:582 条(首批,聚焦侧栏/聊天/模型/下载/设置/开发者等高频 UI 文案)。

## 生效方式(重要)

1. 完全退出 LM Studio(托盘图标也退出);
2. 重新打开;
3. 保持「设置 → 语言 = 简体中文 (Beta)」;
4. 界面走 i18n 的文本此时已 100% 有中文(含新补 63 项),其余硬编码英文由汉化层在渲染后约一帧内替换为中文。

## 如何扩展词典(后续加词条)

编辑 `patch/zh_dict.json`(或直接改 `renderer/zh_dict.js`),按 `"英文原文": "中文译文"` 追加,然后执行:

```
python patch/gen_dict_js.py        # 重新生成 zh_dict.js
python patch/deploy.py             # 重新拷贝(幂等)
```

注意:词条为**整段精确匹配**(含大小写/标点),请照抄页面上实际显示的英文。

## 升级与回滚

- 官方大版本升级会还原 `index.html`/`main_window.js` → 重跑 `python patch/deploy.py` 即可恢复 B 部分;A 部分的模块 id 可能变化,需用 `analysis/` 下脚本重新解析后重跑 `gen_i18n_patch.py`。
- 回滚(全部还原为官方原样):
  - `python patch/deploy.py rollback`(移除注入与补丁文件);
  - 再用 `backups/` 中的 `main_window.js.bak` 覆盖还原(补 key 不可逆,备份保留原版)。

## 原始备份

`backups/main_window.js.bak`、`backups/index.html.bak`(修改前 2026-09-09 11:07 备份)。
