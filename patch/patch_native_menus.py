#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
patch_native_menus.py  v2

LM Studio 的右键/下拉菜单在 FEATURE_FLAG_NATIVE_CONTEXT_MENUS=true 时走
renderer -> IPC -> main 进程 Menu.buildFromTemplate, 渲染为**操作系统原生菜单**,
不进入 DOM, 因此 lms-zh-patch.js 的 DOM 补丁完全抓不到。

renderer 侧有 **两个** spec -> ipc-spec 的转换函数, 所有 label 都从这里流过:
  1) 模块 6405 (openNativeFromSpec) 里的 n(t,e)  —— 供 <ContextMenu spec={...}> / TabChip 使用
  2) 模块 59332 (useContextMenu)     里的 o(t,e)  —— 供 useContextMenu(...) hook 使用

本脚本把两个函数的 `label: X.label` 全部改为 `label: _tr(X.label)`,
_tr 在调用时读取 window.__ZH_DICT__ (由 zh_dict.js 注入)。

- 幂等: 已 patch 过则跳过
- 备份: backups/main_window.predocs.bak (与 native_menu.bak 字节相同, 复用之)
- 需要管理员权限(写入 C:\\Program Files)
"""
import os, sys, shutil

BUNDLE = os.environ.get('LMSZH_BUNDLE') or \
    r'C:\Program Files\LM Studio\resources\app\.webpack\renderer\main_window.js'
BACKUP = os.environ.get('LMSZH_BAK') or \
    os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'backups', 'main_window.predocs.bak')

TR = 'const ZH=window.__ZH_DICT__||{},_tr=s=>(ZH&&ZH[s])||s;'

PATCHES = []

# ---------- 1) 模块 6405 : n() ----------
PATCHES.append((
    'function n(t,e){switch(t.type){case"separator":return[{type:"separator"}];'
    'case"label":return[{id:e.add(void 0),label:t.label,enabled:!1}];'
    'case"item":return t.hide?[]:[{id:e.add(t.onSelect),label:t.label,enabled:!1!==t.enabled,'
    'icon:t.icon,iconDark:t.iconDark,accelerator:t.accelerator}];'
    'case"checkbox":return[{id:e.add((()=>t.onChange?.(!t.checked))),label:t.label,'
    'enabled:!1!==t.enabled,checked:!!t.checked,accelerator:t.accelerator}];'
    'case"radioGroup":{const a=[];for(const n of t.items){const r=e.add((()=>t.onChange?.(n.value)));'
    'a.push({id:r,label:n.label,enabled:!1!==n.enabled,checked:t.value===n.value,'
    'accelerator:n.accelerator})}return a}'
    'case"submenu":{const a=[];for(const r of t.items)a.push(...n(r,e));'
    'return 0===a.length?[]:[{id:e.add(void 0),label:t.label,enabled:!0,subMenu:a}]}}',

    'function n(t,e){' + TR + 'switch(t.type){case"separator":return[{type:"separator"}];'
    'case"label":return[{id:e.add(void 0),label:_tr(t.label),enabled:!1}];'
    'case"item":return t.hide?[]:[{id:e.add(t.onSelect),label:_tr(t.label),enabled:!1!==t.enabled,'
    'icon:t.icon,iconDark:t.iconDark,accelerator:t.accelerator}];'
    'case"checkbox":return[{id:e.add((()=>t.onChange?.(!t.checked))),label:_tr(t.label),'
    'enabled:!1!==t.enabled,checked:!!t.checked,accelerator:t.accelerator}];'
    'case"radioGroup":{const a=[];for(const n of t.items){const r=e.add((()=>t.onChange?.(n.value)));'
    'a.push({id:r,label:_tr(n.label),enabled:!1!==n.enabled,checked:t.value===n.value,'
    'accelerator:n.accelerator})}return a}'
    'case"submenu":{const a=[];for(const r of t.items)a.push(...n(r,e));'
    'return 0===a.length?[]:[{id:e.add(void 0),label:_tr(t.label),enabled:!0,subMenu:a}]}}',
))

# ---------- 2) 模块 59332 : o() ----------
PATCHES.append((
    'function o(t,e){return"separator"===t.type?{type:"separator"}:{id:t.onClick?e.addCallback(t.onClick):e.obtainId(),'
    'label:t.label,enabled:t.enabled,icon:t.icon,iconDark:t.iconDark,checked:t.checked,'
    'accelerator:t.accelerator,subMenu:t.subMenu?.map((t=>o(t,e)))}}',

    'function o(t,e){' + TR + 'return"separator"===t.type?{type:"separator"}:{id:t.onClick?e.addCallback(t.onClick):e.obtainId(),'
    'label:_tr(t.label),enabled:t.enabled,icon:t.icon,iconDark:t.iconDark,checked:t.checked,'
    'accelerator:t.accelerator,subMenu:t.subMenu?.map((t=>o(t,e)))}}',
))


def main():
    if not os.path.isfile(BUNDLE):
        sys.exit('未找到 bundle: ' + BUNDLE)

    with open(BUNDLE, 'r', encoding='utf-8', errors='ignore') as f:
        raw = f.read()
    orig_len = len(raw)

    new_raw = raw
    changed = []
    for i, (orig, patched) in enumerate(PATCHES):
        name = ('n()', 'o()')[i] if i < 2 else 'patch%d' % i
        if patched in new_raw:
            print('  [%s] 已 patch 过, 跳过' % name)
            continue
        if orig not in new_raw:
            print('  [%s] !! 未找到原始函数(版本可能已变化), 请更新脚本' % name)
            continue
        cnt = new_raw.count(orig)
        if cnt > 1:
            print('  [%s] 注意: 出现 %d 次, 仅替换第一个' % (name, cnt))
        new_raw = new_raw.replace(orig, patched, 1)
        changed.append(name)
        print('  [%s] 已 patch (%d -> %d chars)' % (name, len(orig), len(patched)))

    if not changed:
        print('无需改动。')
        return

    # 备份(仅首次)
    if not os.path.exists(BACKUP):
        shutil.copy2(BUNDLE, BACKUP)
        print('已备份原 bundle -> %s' % BACKUP)

    try:
        with open(BUNDLE, 'w', encoding='utf-8') as f:
            f.write(new_raw)
    except PermissionError:
        sys.exit('Permission denied: 需要管理员权限写入 C:\\Program Files。'
                 '请以管理员身份运行本脚本(或由 _apply_all.py 提权调用)。')

    print('bundle size: %d -> %d' % (orig_len, len(new_raw)))
    print('完成, 重启 LM Studio 生效。')


if __name__ == '__main__':
    main()
