# -*- coding: utf-8 -*-
# _deploy_only.py — 提权部署补丁文件(不含主进程 hook 注入)
import os, sys, shutil

RENDERER = r'C:\Program Files\LM Studio\resources\app\.webpack\renderer'
HERE = os.path.dirname(os.path.abspath(__file__))
ZH_JS = os.path.join(HERE, 'zh_dict.js')
PATCH_JS = os.path.join(HERE, 'lms-zh-patch.js')
INDEX = os.path.join(RENDERER, 'index.html')
INJECT = '<script src="zh_dict.js"></script><script src="lms-zh-patch.js"></script>'
LOG = os.path.join(HERE, '..', 'logs', 'deploy.log')

lines = []
try:
    if not os.path.isdir(RENDERER): raise SystemExit('未找到 ' + RENDERER)
    for src in (ZH_JS, PATCH_JS):
        dst = os.path.join(RENDERER, os.path.basename(src))
        shutil.copyfile(src, dst)
        lines.append('copied: %s size=%d' % (dst, os.path.getsize(dst)))
    with open(INDEX, encoding='utf-8') as f: html = f.read()
    if 'lms-zh-patch.js' in html:
        lines.append('index.html already injected, skip')
    else:
        anchor = '<script defer="defer" src="main_window.js"></script>'
        if anchor not in html: raise SystemExit('main_window.js anchor not found')
        html = html.replace(anchor, anchor + INJECT, 1)
        with open(INDEX, 'w', encoding='utf-8') as f: f.write(html)
        lines.append('index.html injected')
    lines.append('DEPLOY OK')
except Exception:
    import traceback
    lines.append(traceback.format_exc())

os.makedirs(os.path.dirname(LOG), exist_ok=True)
with open(LOG, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))
