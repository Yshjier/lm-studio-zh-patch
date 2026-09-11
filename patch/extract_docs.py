# -*- coding: utf-8 -*-
"""
从 main_window.js 抽取全部开发者文档 markdown（按 pageRelUrl 反向定位，快且稳）。
输出:
  patch/docs_src/<pageRelUrl 转义>.md
  patch/docs_manifest.json
"""
import re, io, sys, os, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNDLE = os.environ.get('LMSZH_BUNDLE') or \
    r'C:\Program Files\LM Studio\resources\app\.webpack\renderer\main_window.js'
OUT = os.path.join(ROOT, 'patch', 'docs_src')
os.makedirs(OUT, exist_ok=True)

src = open(BUNDLE, encoding='utf-8', newline='').read()
print('bundle chars:', len(src))


def find_str_end(s, i):
    q = s[i]
    j = i + 1
    n = len(s)
    while j < n:
        c = s[j]
        if c == '\\':
            j += 2
            continue
        if c == q:
            return j
        j += 1
    return -1


SIMPLE = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', "'": "'",
          '"': '"', '`': '`', '/': '/', 'b': '\b', 'f': '\f', 'v': '\v', '0': '\0'}


def unesc(s):
    if '\\' not in s:
        return s
    out = []
    i = 0
    n = len(s)
    while i < n:
        ch = s[i]
        if ch == '\\' and i + 1 < n:
            nx = s[i + 1]
            if nx in SIMPLE:
                out.append(SIMPLE[nx]); i += 2
            elif nx == 'u' and i + 6 <= n:
                out.append(chr(int(s[i + 2:i + 6], 16))); i += 6
            elif nx == 'x' and i + 4 <= n:
                out.append(chr(int(s[i + 2:i + 4], 16))); i += 4
            else:
                out.append(nx); i += 2
        else:
            out.append(ch); i += 1
    return ''.join(out)


entries = []
used_urls = set()
for um in re.finditer(r'pageRelUrl:"([^"]+)"', src):
    url = um.group(1)
    if url in used_urls:
        continue
    p = um.start()
    lo = max(0, p - 120000)
    win = src[lo:p]
    k = win.rfind('content:')
    found = None
    while k >= 0:
        j = lo + k + len('content:')
        while j < p and src[j] in ' \t':
            j += 1
        if j < p and src[j] in '\'"':
            end = find_str_end(src, j)
            if end > 0:
                expect = ',pageRelUrl:"%s"' % url
                if src[end + 1:end + 1 + len(expect)] == expect:
                    found = (src[j], j + 1, end)
                    break
        k = win.rfind('content:', 0, k)
    if not found:
        print('MISS locate:', url)
        continue
    quote, bstart, bend = found
    used_urls.add(url)
    back = src[max(0, bstart - 6000):bstart]
    tm = None
    for t in re.finditer(r'metadata:\{title:"((?:[^"\\]|\\.)*)"', back):
        tm = t
    pm = None
    for t in re.finditer(r'prettyName:"((?:[^"\\]|\\.)*)"', back):
        pm = t
    raw = src[bstart:bend]
    entries.append({
        'pageRelUrl': url,
        'quote': quote,
        'body_start': bstart,
        'body_end': bend,
        'raw_len': len(raw),
        'title': unesc(tm.group(1)) if tm else '',
        'prettyName': unesc(pm.group(1)) if pm else '',
    })
    base = url[:-3] if url.endswith('.md') else url
    with open(os.path.join(OUT, base.replace('/', '__') + '.md'), 'w',
              encoding='utf-8', newline='') as f:
        f.write(unesc(raw))

entries.sort(key=lambda e: e['body_start'])
with open(os.path.join(ROOT, 'patch', 'docs_manifest.json'), 'w', encoding='utf-8') as f:
    json.dump(entries, f, ensure_ascii=False, indent=2)

tot = sum(e['raw_len'] for e in entries)
print(f'entries: {len(entries)}   total raw md chars: {tot} (~{tot/1024:.0f} KB)')
sec = {}
for e in entries:
    k = e['pageRelUrl'].split('/')[0]
    sec[k] = sec.get(k, 0) + 1
print('sections:', sec)
