# -*- coding: utf-8 -*-
"""
i18n 语言包缺键补注（静态旁路）。

zh_CN 包里缺失的翻译键会回落到英文；本脚本按命名空间定位 bundle 内对应
JSON.parse('...') 载荷，只追加官方包缺失的键，不覆盖既有官方翻译。
模块 ID 由 bundle 动态推导，不写死，跨版本更稳。

用法:
    python i18n_patch.py apply     # 追加缺键（幂等）
    python i18n_patch.py report    # 只报告各命名空间可补键数
"""
import os, re, sys, json, io, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", write_through=True)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNDLE = os.environ.get("LMSZH_BUNDLE") or \
    r"D:\Program Files\LM Studio\resources\app\.webpack\renderer\main_window.js"
EXTRA = os.path.join(ROOT, "dict_src", "i18n.json")
BS = chr(92)
Q1 = chr(39)


def safe_value(zh):
    if not isinstance(zh, str) or not zh or zh.strip() != zh:
        return False
    bad = ('"', BS, "\n", "\r", "\t", "\x00", "${", "{{", "}}")
    return not any(x in zh for x in bad)


def load_extra():
    if not os.path.exists(EXTRA):
        return {}
    d = json.load(open(EXTRA, encoding="utf-8-sig"))
    out = {}
    for space, items in d.items():
        if isinstance(items, dict) and items:
            out[space] = items
    return out


def i18n_module_map(s):
    """从 bundle 的 i18n 模块表取 {命名空间: 简中语言包模块 id}。"""
    start = s.find("44856:")
    if start < 0:
        return {}
    seg = s[start:start + 20000]
    vm = dict(re.findall(r"([A-Za-z_$][\w$]*)=r\(a\((\d+)\)\)", seg))
    m = re.search(r"e\.ChineseCNStrings=(\w+);", s[start:start + 40000])
    if not m:
        return {}
    md = re.search(r"(?:^|[,;]|const\s+)" + re.escape(m.group(1)) + r"=\{([^}]+)\}", seg)
    if not md:
        return {}
    ns = dict(re.findall(r"(\w+):([\w$]+)\.default", md.group(1)))
    return {k: vm[v] for k, v in ns.items() if v in vm}


def payload_span(s, mid):
    """返回 JSON.parse('...') payload 的 [start, end) 区间。"""
    needle = str(mid) + ':t=>{"use strict";t.exports=JSON.parse(' + Q1
    pos = s.find(needle)
    if pos < 0:
        return None
    start = pos + len(needle)
    i = start
    esc = False
    while i < len(s):
        c = s[i]
        if esc:
            esc = False; i += 1; continue
        if c == BS:
            esc = True; i += 1; continue
        if c == Q1 and s[i + 1:i + 3] == ")}":
            return (start, i)
        i += 1
    return None


def js_unescape(p):
    out, esc = [], False
    for c in p:
        if esc:
            out.append(c); esc = False
        elif c == BS:
            esc = True
        else:
            out.append(c)
    return "".join(out)


def inject_i18n(content, extra):
    mods = i18n_module_map(content)
    edits, added, report = [], 0, []
    for space, keys in extra.items():
        mid = mods.get(space)
        if mid is None:
            report.append("[%s] 模块未定位" % space); continue
        span = payload_span(content, mid)
        if not span:
            report.append("[%s] 载荷未定位" % space); continue
        st, en = span
        payload = content[st:en]
        try:
            data = json.loads(js_unescape(payload))
        except Exception as e:
            raise RuntimeError("简中语言包（%s）解析失败：%s" % (space, e))
        if not isinstance(data, dict):
            continue
        entries = []
        for k, v in keys.items():
            if k in data or not safe_value(v):
                continue
            if any(c in k for c in ('"', BS)):
                continue
            entries.append((k, v))
        if not entries:
            report.append("[%s] 无缺键" % space); continue

        def jesc(x):
            return x.replace(BS, BS + BS).replace(Q1, BS + Q1)

        esc = "".join(',"%s":"%s"' % (jesc(k), jesc(v)) for k, v in entries)
        last = payload.rfind("}")
        if last < 0:
            continue
        newp = payload[:last] + esc + payload[last:]
        if len(json.loads(js_unescape(newp))) != len(data) + len(entries):
            raise RuntimeError("注入后键数不符（%s）" % space)
        edits.append((st, en, newp))
        added += len(entries)
        report.append("[%s] 新增 %d 键" % (space, len(entries)))
    for st, en, newp in sorted(edits, key=lambda x: -x[0]):
        content = content[:st] + newp + content[en:]
    return content, added, report


def node_check(path):
    r = subprocess.run(["node", "--check", path], capture_output=True, text=True, shell=False)
    return r.returncode == 0, (r.stdout + r.stderr)[:1500]


def main():
    cmd = sys.argv[1] if len(sys.argv) > 1 else "apply"
    extra = load_extra()
    src = open(BUNDLE, encoding="utf-8", newline="").read()
    content, added, report = inject_i18n(src, extra)
    for r in report:
        print("  ", r)
    print("合计新增缺键:", added)
    if cmd == "report":
        return
    if added == 0:
        print("无可操作"); return
    tmp = BUNDLE + ".i18ncheck.js"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    ok, detail = node_check(tmp)
    if not ok:
        os.remove(tmp); raise SystemExit("node --check 失败：\n" + detail)
    os.replace(tmp, BUNDLE)
    print("i18n 缺键补注完成，node --check 通过")


if __name__ == "__main__":
    main()
