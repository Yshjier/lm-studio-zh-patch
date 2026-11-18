# -*- coding: utf-8 -*-
"""
把 patch/docs_zh/<route 转义>.md 的中文 markdown 注入 main_window.js 中对应
articles 条目的 content:"..." 字符串（0.4.28 结构：route + metadata + content）。

用法（需管理员权限，目标在 Program Files）:
    python apply_docs_zh.py            # 注入全部已有译文
    python apply_docs_zh.py report      # 只报告覆盖情况
    python apply_docs_zh.py rollback    # 从 main_window.js.bak 还原

设计要点:
- 幂等：按 route 定位，不依赖历史偏移；重复运行结果一致
- 保留原引号风格（单/双引号），只重写引号之间的内容
- 从后往前替换，避免偏移失效
- 写入前 node --check 校验语法
"""
import os, re, io, sys, json, shutil, time, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", write_through=True)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNDLE = os.environ.get("LMSZH_BUNDLE") or \
    r"D:\Program Files\LM Studio\resources\app\.webpack\renderer\main_window.js"
BAK = os.environ.get("LMSZH_BAK") or os.path.join(os.path.dirname(BUNDLE), "main_window.js.bak")
ZH_DIR = os.path.join(ROOT, "patch", "docs_zh")
MANIFEST = os.path.join(ROOT, "patch", "docs_manifest.json")
LOG = os.path.join(ROOT, "logs", "apply_docs.log")
os.makedirs(os.path.dirname(LOG), exist_ok=True)


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(s + "\n")


def find_str_end(s, i):
    q = s[i]; j = i + 1; n = len(s)
    while j < n:
        c = s[j]
        if c == "\\":
            j += 2; continue
        if c == q:
            return j
        j += 1
    return -1


def esc(text, quote):
    out = []
    for ch in text:
        if ch == "\\":
            out.append("\\\\")
        elif ch == quote:
            out.append("\\" + quote)
        elif ch == "\n":
            out.append("\\n")
        elif ch == "\r":
            out.append("\\r")
        elif ch == "\t":
            out.append("\\t")
        elif ord(ch) == 0x2028:
            out.append("\\u2028")
        elif ord(ch) == 0x2029:
            out.append("\\u2029")
        elif ord(ch) < 0x20:
            out.append("\\x%02x" % ord(ch))
        else:
            out.append(ch)
    return "".join(out)


SIMPLE = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", "'": "'",
          '"': '"', "`": "`", "/": "/", "b": "\b", "f": "\f", "v": "\v", "0": "\0"}


def unesc(s):
    if "\\" not in s:
        return s
    out, i, n = [], 0, len(s)
    while i < n:
        ch = s[i]
        if ch == "\\" and i + 1 < n:
            nx = s[i + 1]
            if nx in SIMPLE:
                out.append(SIMPLE[nx]); i += 2
            elif nx == "u" and i + 6 <= n:
                out.append(chr(int(s[i + 2:i + 6], 16))); i += 6
            elif nx == "x" and i + 4 <= n:
                out.append(chr(int(s[i + 2:i + 4], 16))); i += 4
            else:
                out.append(nx); i += 2
        else:
            out.append(ch); i += 1
    return "".join(out)


def load_manifest():
    if not os.path.exists(MANIFEST):
        return []
    return json.load(open(MANIFEST, encoding="utf-8"))


def locate_article(src, route):
    """返回 (quote, body_start, body_end)；未定位到返回 None。"""
    needle = 'route:"%s"' % route
    p = src.find(needle)
    if p < 0:
        return None
    c = src.find("content:", p, p + 8000)
    if c < 0:
        return None
    j = c + len("content:")
    while j < len(src) and src[j] in " \t":
        j += 1
    if j >= len(src) or src[j] not in "'\"":
        return None
    end = find_str_end(src, j)
    if end < 0:
        return None
    return src[j], j + 1, end


def read_zh(entry):
    if not entry.get("zh"):
        return None
    p = os.path.join(ZH_DIR, entry["zh"])
    if not os.path.exists(p):
        return None
    t = open(p, encoding="utf-8", newline="").read()
    return t.replace("\r\n", "\n").replace("\r", "\n")


def cmd_report():
    src = open(BUNDLE, encoding="utf-8", newline="").read()
    entries = load_manifest()
    have = miss = 0
    for e in entries:
        if not e.get("zh"):
            continue
        loc = locate_article(src, e["route"])
        if not loc:
            log("  [未定位] %s" % e["route"]); miss += 1; continue
        _, a, b = loc
        cur = unesc(src[a:b])
        zh = read_zh(e)
        if zh is not None and cur == zh:
            have += 1; log("  [已翻] %s" % e["route"])
        else:
            miss += 1; log("  [待注入] %s" % e["route"])
    log("可注入译文 %d 篇；已中文 %d；待注入/缺失 %d" % (
        sum(1 for e in entries if e.get("zh")), have, miss))


def cmd_apply():
    if not os.path.exists(BAK):
        shutil.copy2(BUNDLE, BAK)
        log("[备份] 已建", BAK, os.path.getsize(BAK))
    else:
        log("[备份] 存在", BAK, os.path.getsize(BAK))

    src = open(BUNDLE, encoding="utf-8", newline="").read()
    entries = load_manifest()
    plan, skip = [], 0
    for e in entries:
        zh = read_zh(e)
        if zh is None:
            continue
        loc = locate_article(src, e["route"])
        if not loc:
            skip += 1; continue
        quote, a, b = loc
        cur = unesc(src[a:b])
        if cur == zh:
            continue
        plan.append((a, b, esc(zh, quote), e["route"]))

    log("待替换: %d   未定位/缺译文: %d" % (len(plan), skip))
    out = src
    for a, b, body, route in sorted(plan, key=lambda x: -x[0]):
        out = out[:a] + body + out[b:]
        log("  已注入 %s (%d -> %d chars)" % (route, b - a, len(body)))

    if not plan:
        log("无可操作"); return

    tmp = BUNDLE + ".zhcheck.js"
    with open(tmp, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True, shell=False)
    if r.returncode != 0:
        log("[致命] node --check 校验失败，中止。")
        log(r.stdout); log(r.stderr)
        os.remove(tmp); sys.exit(2)
    log("[检查] node --check 通过")
    shutil.move(tmp, BUNDLE)
    log("[完成] bundle -> %d bytes" % os.path.getsize(BUNDLE))


def cmd_rollback():
    if not os.path.exists(BAK):
        log("[错误] 未找到备份", BAK); sys.exit(1)
    shutil.copy2(BAK, BUNDLE)
    log("[回滚] 已还原", BAK, "->", BUNDLE, os.path.getsize(BUNDLE))


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "apply"
    log("=== apply_docs_zh.py %s %s ===" % (cmd, time.strftime("%Y-%m-%d %H:%M:%S")))
    if cmd == "apply":
        cmd_apply()
    elif cmd == "rollback":
        cmd_rollback()
    elif cmd == "report":
        cmd_report()
    else:
        log("未知命令", cmd); sys.exit(1)
