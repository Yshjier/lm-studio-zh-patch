# -*- coding: utf-8 -*-
"""
上下文菜单标签静态旁路（右键 / 下拉 / 排序菜单）。

这类菜单由 renderer 的两个 spec→菜单转换函数生成，标签不进入 DOM，
运行时观察者抓不到；在转换函数出口把 label 过一遍 window.__ZH_DICT__。

- 幂等：已注入 _tr 则跳过
- 版本漂移：未命中原始代码形态时告警跳过，不中断安装
- 备份 / 还原由 install.py 统一管理，本脚本不重复备份
"""
import os, sys, io, subprocess

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", write_through=True)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNDLE = os.environ.get("LMSZH_BUNDLE") or \
    r"D:\Program Files\LM Studio\resources\app\.webpack\renderer\main_window.js"

TR = 'const ZH=window.__ZH_DICT__||{},_tr=s=>(ZH&&ZH[s])||s;'

# 转换器 1：switch 形态（ContextMenu spec / 标签页右键菜单）
ORIG1 = ('function r(t,e){switch(t.type){case"separator":return[{type:"separator"}];'
'case"label":return[{id:e.add(void 0),label:t.label,enabled:!1}];'
'case"item":return t.hide?[]:[{id:e.add(t.onSelect),label:t.label,enabled:!1!==t.enabled,'
'icon:t.icon,iconDark:t.iconDark,accelerator:t.accelerator}];'
'case"checkbox":return[{id:e.add((()=>t.onChange?.(!t.checked))),label:t.label,'
'enabled:!1!==t.enabled,checked:!!t.checked,accelerator:t.accelerator}];'
'case"radioGroup":{const a=[];for(const r of t.items){const i=e.add((()=>t.onChange?.(r.value)));'
'a.push({id:i,label:r.label,enabled:!1!==r.enabled,checked:t.value===r.value,accelerator:r.accelerator})}'
'return a}case"submenu":{const a=[];for(const i of t.items)a.push(...r(i,e));'
'return 0===a.length?[]:[{id:e.add(void 0),label:t.label,enabled:!0,subMenu:a}]}}}')

# 转换器 2：扁平形态（useContextMenu hook 下拉菜单）
ORIG2 = ('function l(t,e){return"separator"===t.type?{type:"separator"}:'
'{id:t.onClick?e.addCallback(t.onClick):e.obtainId(),label:t.label,enabled:t.enabled,'
'icon:t.icon,iconDark:t.iconDark,checked:t.checked,accelerator:t.accelerator,'
'subMenu:t.subMenu?.map((t=>l(t,e)))}}')

PAIRS = [("标签页/组件菜单", ORIG1, "r"), ("Hook 下拉菜单", ORIG2, "l")]


def build_patched(orig, fn):
    p = orig.replace("label:t.label", "label:_tr(t.label)")
    p = p.replace("label:r.label", "label:_tr(r.label)")
    p = p.replace("function %s(t,e){" % fn, "function %s(t,e){" % fn + TR, 1)
    return p


def node_check(path):
    r = subprocess.run(["node", "--check", path], capture_output=True,
                       text=True, shell=False)
    return r.returncode == 0, (r.stdout + r.stderr)[:1500]


def main():
    if not os.path.isfile(BUNDLE):
        sys.exit("错误: 未找到 bundle: " + BUNDLE)

    src = open(BUNDLE, encoding="utf-8", errors="ignore").read()
    if "_tr(t.label)" in src or "_tr(r.label)" in src:
        print("菜单标签旁路: 已注入，跳过")
        return

    out = src
    changed = []
    for name, orig, fn in PAIRS:
        patched = build_patched(orig, fn)
        if patched in out:
            continue
        if orig not in out:
            print("  [%s] 未命中原始代码形态，该部分菜单仍将英文" % name)
            continue
        out = out.replace(orig, patched, 1)
        changed.append(name)
        print("  [%s] 标签已接入字典" % name)

    if not changed:
        print("菜单标签旁路: 无需改动")
        return

    tmp = BUNDLE + ".menucheck.js"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    ok, detail = node_check(tmp)
    if not ok:
        os.remove(tmp)
        raise SystemExit("node --check 失败：\n" + detail)
    os.replace(tmp, BUNDLE)
    print("菜单标签旁路完成，node --check 通过")


if __name__ == "__main__":
    main()
