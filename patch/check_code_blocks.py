# -*- coding: utf-8 -*-
"""代码块强校验（按围栏类型分别判定）。

规则：
- 真代码围栏（bash/python/typescript/json/xml/... 或空 info）内部必须逐字节一致
- lms_code_snippet：仅 `code: |` 之后的代码行必须逐字节一致（variant 标签可译）
- lms_params：仅 `description:` 的值可译，其余行必须一致
- 其他 lms_* 围栏（warning/info/protip/noticechill/tip/hstack...）是散文，可自由翻译
"""
import os
import re
import sys
import io
import difflib

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'patch', 'docs_src')
ZH = os.path.join(ROOT, 'patch', 'docs_zh')

FENCE = re.compile(r'^```([^\n]*)\n(.*?)^```', re.M | re.S)
CODE_LANGS = {'', 'bash', 'sh', 'shell', 'python', 'py', 'typescript', 'ts',
              'javascript', 'js', 'json', 'jsonc', 'xml', 'yaml', 'yml',
              'text', 'txt', 'http', 'sql', 'console', 'diff', 'ini', 'toml',
              'powershell', 'ps1', 'cmd', 'lms_json_schema'}


def parse(text):
    return [(m.group(1).strip(), m.group(2)) for m in FENCE.finditer(text)]


def snippet_code(body):
    """取 lms_code_snippet 里所有 `code: |` 段落的代码行。"""
    lines = body.split('\n')
    out = []
    i = 0
    while i < len(lines):
        if re.match(r'^\s*code:\s*\|', lines[i]):
            i += 1
            while i < len(lines) and (not lines[i].strip() or lines[i].startswith(' ' * 8)):
                out.append(lines[i])
                i += 1
            continue
        i += 1
    return '\n'.join(out)


def params_nondesc(body):
    """lms_params 骨架：把 name/description 的值归一化，保留结构。

    - 值形如 `description: xxx`  → 归一化该行
    - 值形如 `description: |`   → 归一化后续的块标量内容行（保留行数与缩进）
    注意：条目形如 YAML 列表项 `- name: xxx`，前导 '- ' 必须容错。
    """
    lines = body.split('\n')
    out = []
    i = 0
    while i < len(lines):
        ln = lines[i]
        m = re.match(r'^(\s*(?:-\s*)?description:\s*)(.*)$', ln)
        if m:
            prefix, rest = m.group(1), m.group(2)
            out.append(prefix + '<X>')
            if rest.strip().startswith('|'):
                base = len(ln) - len(ln.lstrip())
                i += 1
                in_para = False
                while i < len(lines):
                    cur = lines[i]
                    if not cur.strip():
                        out.append('')
                        in_para = False
                        i += 1
                        continue
                    ind = len(cur) - len(cur.lstrip())
                    if ind <= base:
                        break
                    # 同一段落内的软换行折叠为一个标记（行宽可随译文变化，段落结构不可变）
                    if not in_para:
                        out.append(' ' * ind + '<X>')
                        in_para = True
                    i += 1
                continue
            i += 1
            continue
        m2 = re.match(r'^(\s*(?:-\s*)?name:\s*)(.*)$', ln)
        if m2:
            out.append(m2.group(1) + '<X>')
            i += 1
            continue
        out.append(ln)
        i += 1
    return '\n'.join(out)


def main():
    names = sys.argv[1:]
    files = names if names else [f for f in sorted(os.listdir(ZH)) if f.endswith('.md')]
    ok = bad = 0
    for f in files:
        a = os.path.join(SRC, f)
        b = os.path.join(ZH, f)
        if not (os.path.exists(a) and os.path.exists(b)):
            print('SKIP', f)
            continue
        pa = parse(open(a, encoding='utf-8', newline='').read())
        pb = parse(open(b, encoding='utf-8', newline='').read())
        probs = []
        if len(pa) != len(pb):
            probs.append(f'fence count {len(pa)} -> {len(pb)}')
        else:
            for idx, ((ia, ba), (ib, bb)) in enumerate(zip(pa, pb)):
                if ia != ib:
                    probs.append(f'#{idx+1} info "{ia}" -> "{ib}"')
                    continue
                if ia in CODE_LANGS:
                    if ba != bb:
                        probs.append(f'#{idx+1} [{ia}] code changed')
                elif ia == 'lms_code_snippet':
                    if snippet_code(ba) != snippet_code(bb):
                        probs.append(f'#{idx+1} code: | body changed')
                elif ia == 'lms_params':
                    if params_nondesc(ba) != params_nondesc(bb):
                        probs.append(f'#{idx+1} lms_params skeleton changed')
        if probs:
            bad += 1
            print(f'FAIL {f}')
            for p in probs:
                print('   -', p)
            # 打印首个真代码差异细节
            for idx, ((ia, ba), (ib, bb)) in enumerate(zip(pa, pb)):
                if ia in CODE_LANGS and ba != bb:
                    print(f'   --- #{idx+1} [{ia}] diff ---')
                    for line in list(difflib.unified_diff(
                            ba.split('\n'), bb.split('\n'), lineterm='', n=1))[:20]:
                        print('     ' + line)
                    break
                if ia == 'lms_code_snippet' and snippet_code(ba) != snippet_code(bb):
                    print(f'   --- #{idx+1} snippet code diff ---')
                    for line in list(difflib.unified_diff(
                            snippet_code(ba).split('\n'),
                            snippet_code(bb).split('\n'), lineterm='', n=1))[:20]:
                        print('     ' + line)
                    break
        else:
            ok += 1
    print(f'\n== {ok} ok, {bad} fail ==')


main()
