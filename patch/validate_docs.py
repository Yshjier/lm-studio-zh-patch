# -*- coding: utf-8 -*-
"""
校验 docs_zh 译文是否保持与 docs_src 英文原文相同的 markdown 结构。
比对：代码围栏数、URL 集合、行内代码数、各级标题数、分隔线数、表格行数。
用法: python patch/validate_docs.py [文件名...]   不带参数=校验全部已有译文
"""
import os, re, io, sys, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'patch', 'docs_src')
ZH = os.path.join(ROOT, 'patch', 'docs_zh')

FENCE = re.compile(r'^\s*(```|~~~)', re.M)
INLINE = re.compile(r'(?<!`)(`+)(?!`)')
HEAD = re.compile(r'^(#{1,6})\s', re.M)
LINK = re.compile(r'\]\(([^)]+)\)')
IMG = re.compile(r'<img\b[^>]*?src="([^"]+)"')
SEP = re.compile(r'^-{3,}\s*$', re.M)
TABLE = re.compile(r'^\s*\|', re.M)


def feats(t):
    return {
        'fences': len(FENCE.findall(t)),
        'inline_backticks': len(re.findall(r'`', t)),
        'heads': {lvl: len(re.findall(r'^%s\s' % ('#' * lvl), t, re.M)) for lvl in range(1, 7)},
        'links': sorted(LINK.findall(t)),
        'imgs': sorted(IMG.findall(t)),
        'seps': len(SEP.findall(t)),
        'table_rows': len(TABLE.findall(t)),
    }


WARN = []


def split_links(ls):
    anc = [x for x in ls if x.startswith('#')]
    oth = [x for x in ls if not x.startswith('#')]
    return oth, anc


def main():
    names = sys.argv[1:]
    if not names:
        names = [os.path.basename(p) for p in sorted(glob.glob(os.path.join(ZH, '*.md')))]
    ok = bad = 0
    for n in names:
        a = os.path.join(SRC, n)
        b = os.path.join(ZH, n)
        if not (os.path.exists(a) and os.path.exists(b)):
            print(f'SKIP {n} (missing)'); continue
        fa = feats(open(a, encoding='utf-8', newline='').read())
        fb = feats(open(b, encoding='utf-8', newline='').read())
        diffs = []
        for k in ('fences', 'inline_backticks', 'seps', 'table_rows'):
            if fa[k] != fb[k]:
                diffs.append(f'{k}: {fa[k]} -> {fb[k]}')
        for lvl in range(1, 7):
            if fa['heads'][lvl] != fb['heads'][lvl]:
                diffs.append(f'h{lvl}: {fa["heads"][lvl]} -> {fb["heads"][lvl]}')
        oa, aa = split_links(fa['links'])
        ob, ab = split_links(fb['links'])
        if oa != ob:
            lost = set(oa) - set(ob)
            add = set(ob) - set(oa)
            if lost:
                diffs.append(f'links lost {len(lost)}: {list(lost)[:3]}')
            if add:
                diffs.append(f'links added {len(add)}: {list(add)[:3]}')
        if len(aa) != len(ab):
            diffs.append(f'in-page anchor count: {len(aa)} -> {len(ab)}')
        elif aa != ab:
            WARN.append(f'{n}: 页内锚点随标题本地化而改变 {aa} -> {ab}')
        if fa['imgs'] != fb['imgs']:
            diffs.append('img src changed')
        if diffs:
            bad += 1
            print(f'FAIL {n}')
            for d in diffs:
                print('     -', d)
        else:
            ok += 1
            print(f'OK   {n}')
    print(f'\n== {ok} ok, {bad} fail ==')
    if WARN:
        print('\n-- 页内锚点提示 (非致命) --')
        for w in WARN:
            print('  *', w)


if __name__ == '__main__':
    main()
