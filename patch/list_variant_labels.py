# -*- coding: utf-8 -*-
"""统计 lms_code_snippet 的 variant 标签（代码块顶部 tab 显示文本）。

判定规则：在 ```lms_code_snippet 围栏内，缩进恰为 4 且以 ':' 结尾，
且其后的下一条非空行为 `      language: ...` 的行，即为 variant 标签。
（不能简单地按“连续缩进行”截取——variant 的代码体里可能含空行。）
"""
import os
import re
import sys
import io
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, 'patch', 'docs_src')
ZH = os.path.join(ROOT, 'patch', 'docs_zh')

FENCE = re.compile(r'^```([^\n]*)\n(.*?)^```', re.M | re.S)


def labels(text):
    out = []
    for m in FENCE.finditer(text):
        if m.group(1).strip() != 'lms_code_snippet':
            continue
        lines = m.group(2).split('\n')
        for i, ln in enumerate(lines):
            s = ln.rstrip('\r')
            if not s.strip() or not s.rstrip().endswith(':'):
                continue
            if len(s) - len(s.lstrip()) != 4:
                continue
            nxt = ''
            for j in range(i + 1, len(lines)):
                if lines[j].strip():
                    nxt = lines[j].strip()
                    break
            if not nxt.startswith('language:'):
                continue
            lab = s.strip()[:-1]
            if lab.startswith('"') and lab.endswith('"'):
                lab = lab[1:-1]
            out.append(lab)
    return out


def main():
    for d, name in ((SRC, 'docs_src'), (ZH, 'docs_zh')):
        cnt = Counter()
        files = 0
        for f in sorted(os.listdir(d)):
            if not f.endswith('.md'):
                continue
            files += 1
            t = open(os.path.join(d, f), encoding='utf-8', newline='').read()
            for lab in labels(t):
                cnt[lab] += 1
        print(f'=== {name} ({files} files), {len(cnt)} distinct, {sum(cnt.values())} total ===')
        for k, v in sorted(cnt.items()):
            print(f'  {v:>4}  {k}')
        print()


main()
