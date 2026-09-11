# -*- coding: utf-8 -*-
"""把 docs_zh 中 lms_code_snippet 的 variant 标签（代码块顶部 tab 显示文本）汉化。

- 只改标签行，绝不触碰 `language:` / `code: |` / 代码体
- 幂等：已是中文的标签不会被再次替换
- 统一输出带引号形式（源码中已有大量带引号标签在正常渲染）
- 误伤防护：只处理 ```lms_code_snippet 围栏内、缩进恰为 4、以 ':' 结尾、
  且下一条非空行以 `language:` 开头的行

用法：
    python patch/variant_labels.py          # 预览（不改文件）
    python patch/variant_labels.py apply    # 实际写入
"""
import os
import re
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ZH = os.path.join(ROOT, 'patch', 'docs_zh')

MAP = {
    'Python (convenience API)': 'Python（便捷 API）',
    'Python (asynchronous API)': 'Python（异步 API）',
    'Python (synchronous API)': 'Python（同步 API）',
    'Python (scoped resource API)': 'Python（作用域资源 API）',
    'Python (with scoped resources)': 'Python（使用作用域资源）',
    'Non-streaming': '非流式',
    'Non-streaming (asynchronous API)': '非流式（异步 API）',
    'Non-streaming (synchronous API)': '非流式（同步 API）',
    'Streaming': '流式',
    'Streaming (asynchronous API)': '流式（异步 API）',
    'Streaming (synchronous API)': '流式（同步 API）',
    'Example': '示例',
    'Constructing a Chat object': '构造 Chat 对象',
    'Asynchronous chat session': '异步聊天会话',
    'Interactive chat session': '交互式聊天会话',
    'Environment Variable': '环境变量',
    'Function Argument': '函数参数',
    'Python function': 'Python 函数',
    'Using an array of messages': '使用消息数组',
    'Using .load': '使用 .load',
    'Using .model': '使用 .model',
    'Embedding Model': '嵌入模型',
    'TypeScript (Recommended)': 'TypeScript（推荐）',
}

FENCE = re.compile(r'^```([^\n]*)\n(.*?)^```', re.M | re.S)


def label_span(lines, i):
    """若 lines[i] 是 variant 标签行，返回 (标签文本, 是否带引号)；否则 None。"""
    s = lines[i].rstrip('\r')
    if not s.strip() or not s.rstrip().endswith(':'):
        return None
    if len(s) - len(s.lstrip()) != 4:
        return None
    nxt = ''
    for j in range(i + 1, len(lines)):
        if lines[j].strip():
            nxt = lines[j].strip()
            break
    if not nxt.startswith('language:'):
        return None
    lab = s.strip()[:-1]
    quoted = lab.startswith('"') and lab.endswith('"')
    if quoted:
        lab = lab[1:-1]
    return lab, quoted


def process(text):
    """返回 (新文本, [(旧, 新), ...])。"""
    changes = []

    def repl(m):
        if m.group(1).strip() != 'lms_code_snippet':
            return m.group(0)
        body = m.group(2)
        lines = body.split('\n')
        for i, ln in enumerate(lines):
            got = label_span(lines, i)
            if not got:
                continue
            lab, _ = got
            new = MAP.get(lab)
            if not new or new == lab:
                continue
            changes.append((lab, new))
            lines[i] = '    "%s":' % new
        # 注意：m.group(2) 已含收尾换行（`.*?` 在 re.S 下会把 ``` 前的 \n 吃进来），
        # 因此这里绝不能再补一个 \n —— 否则会给 `code: |` 块标量尾部多加一个空行。
        return '```%s\n%s```' % (m.group(1), '\n'.join(lines))

    return FENCE.sub(repl, text), changes


def main():
    apply = len(sys.argv) > 1 and sys.argv[1] == 'apply'
    total = 0
    files = 0
    for f in sorted(os.listdir(ZH)):
        if not f.endswith('.md'):
            continue
        p = os.path.join(ZH, f)
        t = open(p, encoding='utf-8', newline='').read()
        nt, changes = process(t)
        if not changes:
            continue
        files += 1
        total += len(changes)
        print(f'{f}: {len(changes)} -> {[c[1] for c in changes]}')
        if apply:
            open(p, 'w', encoding='utf-8', newline='').write(nt)
    print(f'\n{"APPLIED" if apply else "PREVIEW"}: {total} labels in {files} files')


main()
