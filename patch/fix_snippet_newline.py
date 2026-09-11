# -*- coding: utf-8 -*-
"""修复 variant_labels.py 引入的多余换行。

variant_labels.py 重建 lms_code_snippet 围栏时，在收尾 ``` 前多加了一个 \n，
使 `code: |` 块标量尾部多出一个空行（YAML 语义无害，但破坏“代码体逐字节一致”）。

判定方式：先把围栏内的 variant 标签行归一化为占位符（因为标签已被汉化，
直接比 body 会不等），再判断 zh 是否恰为 src + '\n'。
"""
import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)

ROOT = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(ROOT, 'docs_src')
ZH = os.path.join(ROOT, 'docs_zh')

F = re.compile(r'^```([^\n]*)\n(.*?)^```', re.M | re.S)


def _label_at(lines, i):
    """lines[i] 是否为 variant 标签行（缩进 4、以 ':' 结尾、下一非空行以 language: 开头）。"""
    s = lines[i].rstrip('\r')
    if not s.strip() or not s.rstrip().endswith(':'):
        return False
    if len(s) - len(s.lstrip()) != 4:
        return False
    nxt = ''
    for j in range(i + 1, len(lines)):
        if lines[j].strip():
            nxt = lines[j].strip()
            break
    return nxt.startswith('language:')


def norm(body):
    lines = body.split('\n')
    for i in range(len(lines)):
        if _label_at(lines, i):
            lines[i] = '    <LABEL>:'
    return '\n'.join(lines)


def main():
    apply = len(sys.argv) > 1 and sys.argv[1] == 'apply'
    files = fences = 0
    for f in sorted(os.listdir(ZH)):
        if not f.endswith('.md'):
            continue
        sp = os.path.join(SRC, f)
        zp = os.path.join(ZH, f)
        if not os.path.exists(sp):
            continue
        src = open(sp, encoding='utf-8', newline='').read()
        zh = open(zp, encoding='utf-8', newline='').read()
        sa = [(m.group(1), m.group(2)) for m in F.finditer(src)]
        out = []
        pos = 0
        n = 0
        for idx, m in enumerate(F.finditer(zh)):
            out.append(zh[pos:m.start()])
            info, body = m.group(1), m.group(2)
            if idx < len(sa) and sa[idx][0] == info and info.strip() == 'lms_code_snippet':
                if norm(body) == norm(sa[idx][1]) + '\n':
                    body = body[:-1]
                    n += 1
            out.append('```%s\n%s```' % (info, body))
            pos = m.end()
        out.append(zh[pos:])
        if n:
            files += 1
            fences += n
            print(f'{f}: fixed {n} fence(s)')
            if apply:
                open(zp, 'w', encoding='utf-8', newline='').write(''.join(out))
    print(f'\n{"APPLIED" if apply else "PREVIEW"}: {fences} fences in {files} files')


main()
