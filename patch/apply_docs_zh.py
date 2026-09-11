# -*- coding: utf-8 -*-
"""
把 patch/docs_zh/<name>.md 的中文 markdown 注入到 main_window.js 里对应的
content:'...' 字符串（按 pageRelUrl 定位），原地替换，其它字节不动。

用法（需管理员权限，因为目标在 Program Files）:
    python apply_docs_zh.py            # 注入全部已有译文
    python apply_docs_zh.py rollback   # 从 <renderer>/main_window.js.bak 还原
    python apply_docs_zh.py report     # 只报告当前哪些 doc 已是中文

设计要点:
- 幂等：按 pageRelUrl 定位，不依赖历史偏移；重复运行结果一致
- 首次运行前自动备份到 main_window.js.bak（与 bundle 同目录, 已存在则跳过）
- 保留原引号风格（单引号/双引号），只重写引号之间的内容
- 从后往前替换，避免偏移失效
"""
import os, re, io, sys, json, shutil, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNDLE = os.environ.get('LMSZH_BUNDLE') or \
    r'C:\Program Files\LM Studio\resources\app\.webpack\renderer\main_window.js'
BAK = os.environ.get('LMSZH_BAK') or os.path.join(os.path.dirname(BUNDLE), 'main_window.js.bak')
SRC = os.path.join(ROOT, 'patch', 'docs_src')
ZH = os.path.join(ROOT, 'patch', 'docs_zh')
LOG = os.path.join(ROOT, 'logs', 'apply_docs.log')
os.makedirs(os.path.dirname(LOG), exist_ok=True)


def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s)
    with open(LOG, 'a', encoding='utf-8') as f:
        f.write(s + '\n')


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


def esc(text, quote):
    """把真实文本编码为 JS 字符串字面量的内容部分"""
    out = []
    for ch in text:
        if ch == '\\':
            out.append('\\\\')
        elif ch == quote:
            out.append('\\' + quote)
        elif ch == '\n':
            out.append('\\n')
        elif ch == '\r':
            out.append('\\r')
        elif ch == '\t':
            out.append('\\t')
        elif ch == '\u2028':
            out.append('\\u2028')
        elif ch == '\u2029':
            out.append('\\u2029')
        elif ord(ch) < 0x20:
            out.append('\\x%02x' % ord(ch))
        else:
            out.append(ch)
    return ''.join(out)


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


def locate_docs(src):
    """返回 [(url, quote, body_start, body_end)]，按出现顺序"""
    res = []
    seen = set()
    for um in re.finditer(r'pageRelUrl:"([^"]+)"', src):
        url = um.group(1)
        if url in seen:
            continue
        p = um.start()
        lo = max(0, p - 120000)
        win = src[lo:p]
        k = win.rfind('content:')
        while k >= 0:
            j = lo + k + len('content:')
            while j < p and src[j] in ' \t':
                j += 1
            if j < p and src[j] in '\'"':
                end = find_str_end(src, j)
                if end > 0:
                    expect = ',pageRelUrl:"%s"' % url
                    if src[end + 1:end + 1 + len(expect)] == expect:
                        seen.add(url)
                        res.append((url, src[j], j + 1, end))
                        break
            k = win.rfind('content:', 0, k)
    return res


def zh_path(url):
    base = url[:-3] if url.endswith('.md') else url
    return os.path.join(ZH, base.replace('/', '__') + '.md')


def cmd_report():
    src = open(BUNDLE, encoding='utf-8', newline='').read()
    docs = locate_docs(src)
    have = 0
    for url, q, a, b in docs:
        cur = unesc(src[a:b])
        zh = zh_path(url)
        if os.path.exists(zh):
            t = open(zh, encoding='utf-8', newline='').read()
            t = t.replace('\r\n', '\n').replace('\r', '\n')
            state = '已翻' if cur == t else 'EN(译文就绪)'
            if cur == t:
                have += 1
        else:
            state = '未翻'
        if state != '未翻':
            log(f'  {state:<12} {url}')
    log(f'共 {len(docs)} 篇; 已为中文: {have}')


def cmd_apply():
    if not os.path.exists(BAK):
        shutil.copy2(BUNDLE, BAK)
        log('[备份] 已建', BAK, os.path.getsize(BAK))
    else:
        log('[备份] 存在', BAK, os.path.getsize(BAK))

    src = open(BUNDLE, encoding='utf-8', newline='').read()
    before_len = len(src.encode('utf-8'))
    docs = locate_docs(src)
    log(f'在 bundle 中定位到 {len(docs)} 篇文档')

    plan = []
    skip = 0
    for url, q, a, b in docs:
        zh = zh_path(url)
        if not os.path.exists(zh):
            skip += 1
            continue
        text = open(zh, encoding='utf-8', newline='').read()
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        cur = unesc(src[a:b])
        if cur == text:
            continue
        plan.append((a, b, esc(text, q), url))

    log(f'待替换: {len(plan)}   缺译文: {skip}')
    out = src
    for a, b, body, url in sorted(plan, key=lambda x: -x[0]):
        out = out[:a] + body + out[b:]
        log(f'  已注入 {url}  ({b - a} -> {len(body)} chars)')

    if not plan:
        log('无可操作')
        return

    tmp = BUNDLE + '.zhcheck.js'
    with open(tmp, 'w', encoding='utf-8', newline='') as f:
        f.write(out)
    # 先验证语法再落地
    import subprocess
    r = subprocess.run(['node', '--check', tmp], capture_output=True, text=True, shell=False)
    if r.returncode != 0:
        log('[致命] node --check 校验失败, 中止。')
        log(r.stdout)
        log(r.stderr)
        os.remove(tmp)
        sys.exit(2)
    log('[检查] node --check 通过')
    shutil.move(tmp, BUNDLE)
    log(f'[完成] bundle {before_len} -> {os.path.getsize(BUNDLE)} bytes')
    log('[完成] 时间', time.strftime('%Y-%m-%d %H:%M:%S'))


def cmd_rollback():
    if not os.path.exists(BAK):
        log('[错误] 未找到备份', BAK)
        sys.exit(1)
    shutil.copy2(BAK, BUNDLE)
    log('[回滚] 已还原', BAK, '->', BUNDLE, os.path.getsize(BUNDLE))


if __name__ == '__main__':
    cmd = sys.argv[1] if len(sys.argv) > 1 else 'apply'
    log('=== apply_docs_zh.py', cmd, time.strftime('%Y-%m-%d %H:%M:%S'), '===')
    if cmd == 'apply':
        cmd_apply()
    elif cmd == 'rollback':
        cmd_rollback()
    elif cmd == 'report':
        cmd_report()
    else:
        log('未知命令', cmd)
        sys.exit(1)
