# -*- coding: utf-8 -*-
"""
_deploy_all.py — 一键全量部署（需管理员权限）

顺序执行:
  1. 复制 zh_dict.js / lms-zh-patch.js 到 renderer
  2. 注入 index.html（在 main_window.js 脚本标签后）
  3. patch_native_menus.py  —— 原生菜单字节补丁（幂等）
  4. apply_docs_zh.py apply —— 156 篇中文开发者文档注入（幂等）

日志: logs/apply.log
"""
import os, sys, io, shutil, subprocess, traceback, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RENDERER = r'C:\Program Files\LM Studio\resources\app\.webpack\renderer'
ZH_JS = os.path.join(ROOT, 'patch', 'zh_dict.js')
PATCH_JS = os.path.join(ROOT, 'patch', 'lms-zh-patch.js')
INDEX = os.path.join(RENDERER, 'index.html')
INJECT = '<script src="zh_dict.js"></script><script src="lms-zh-patch.js"></script>'
LOG = os.path.join(ROOT, 'logs', 'apply.log')

PY = sys.executable
lines = []


def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s)
    lines.append(s)


def flush():
    os.makedirs(os.path.dirname(LOG), exist_ok=True)
    with open(LOG, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))


try:
    log('=== _deploy_all.py', time.strftime('%Y-%m-%d %H:%M:%S'), '===')

    # ---------- 0. 前置检查 ----------
    if not os.path.isdir(RENDERER):
        raise SystemExit('未找到安装目录: ' + RENDERER)
    for src in (ZH_JS, PATCH_JS):
        if not os.path.isfile(src):
            raise SystemExit('源文件缺失: ' + src)
    log('[0] 前置检查 OK; 字典 %d bytes, 补丁 %d bytes'
        % (os.path.getsize(ZH_JS), os.path.getsize(PATCH_JS)))

    # ---------- 1. 复制补丁文件 ----------
    for src in (ZH_JS, PATCH_JS):
        dst = os.path.join(RENDERER, os.path.basename(src))
        shutil.copyfile(src, dst)
        log('[1] copied %s -> %d bytes' % (os.path.basename(dst), os.path.getsize(dst)))

    # ---------- 2. 注入 index.html ----------
    with open(INDEX, encoding='utf-8') as f:
        html = f.read()
    if 'lms-zh-patch.js' in html:
        log('[2] index.html 已注入, 跳过')
    else:
        anchor = '<script defer="defer" src="main_window.js"></script>'
        if anchor not in html:
            raise SystemExit('index.html 未找到 main_window.js 锚点')
        html = html.replace(anchor, anchor + INJECT, 1)
        with open(INDEX, 'w', encoding='utf-8') as f:
            f.write(html)
        log('[2] index.html 注入成功')

    # ---------- 3. 原生菜单字节补丁 ----------
    r = subprocess.run([PY, os.path.join(ROOT, 'patch', 'patch_native_menus.py')],
                       capture_output=True, text=True, encoding='utf-8', errors='replace')
    log('[3] patch_native_menus rc=%d' % r.returncode)
    log((r.stdout or '').strip() or '(no stdout)')
    if r.stderr.strip():
        log('  stderr:', r.stderr.strip()[:2000])

    # ---------- 4. 中文文档注入 ----------
    r = subprocess.run([PY, os.path.join(ROOT, 'patch', 'apply_docs_zh.py'), 'apply'],
                       capture_output=True, text=True, encoding='utf-8', errors='replace',
                       cwd=os.path.join(ROOT, 'patch'))
    log('[4] apply_docs_zh rc=%d' % r.returncode)
    log((r.stdout or '').strip() or '(no stdout)')
    if r.stderr.strip():
        log('  stderr:', r.stderr.strip()[:2000])

    # ---------- 5. 最终核对 ----------
    log('[5] --- 安装目录最终状态 ---')
    for name in ('zh_dict.js', 'lms-zh-patch.js', 'index.html', 'main_window.js'):
        p = os.path.join(RENDERER, name)
        log('    %-20s %d bytes' % (name, os.path.getsize(p) if os.path.exists(p) else -1))
    with open(INDEX, encoding='utf-8') as f:
        h = f.read()
    log('    index 注入 zh_dict: %s' % ('zh_dict.js' in h))
    log('    index 注入 patch  : %s' % ('lms-zh-patch.js' in h))
    log('DEPLOY ALL DONE')

except SystemExit as e:
    log('[FATAL]', e)
except Exception:
    log(traceback.format_exc())
finally:
    flush()
