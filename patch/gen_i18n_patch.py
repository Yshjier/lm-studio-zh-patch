# -*- coding: utf-8 -*-
"""补全 LM Studio main_window.js 中 zh_CN 缺失 key(仅新增,不覆盖官方已有翻译)"""
import re, json, sys, os

JS = r"C:\Program Files\LM Studio\resources\app\.webpack\renderer\main_window.js"
TRANS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'zh_CN_missing_translations.json')

# zh_CN namespace 模块 id(0.4.24+1 实证)
NS_MODULES = {
    "sidebar": "69976", "chat": "62968", "config": "98090",
    "developer": "15044", "discover": "78258", "download": "68938",
    "models": "26049", "onboarding": "54334", "settings": "46885",
    "shared": "95725",
}

def js_unescape(s):
    out, i = [], 0
    esc = {"'": "'", '"': '"', "\\": "\\", "n": "\n", "t": "\t", "r": "\r",
           "b": "\b", "f": "\f", "v": "\v", "0": "\0"}
    while i < len(s):
        c = s[i]
        if c == "\\" and i + 1 < len(s):
            n = s[i + 1]
            if n in esc:
                out.append(esc[n]); i += 2; continue
            if n == "u" and i + 5 < len(s):
                try:
                    out.append(chr(int(s[i+2:i+6], 16))); i += 6; continue
                except ValueError:
                    pass
            out.append(n); i += 2; continue
        out.append(c); i += 1
    return "".join(out)

def js_escape(text):
    """把 JSON 文本包进 JS 单引号字符串(转义 \\ ' 与 U+2028/2029 等)"""
    out = []
    for ch in text:
        o = ord(ch)
        if ch == "\\":
            out.append("\\\\")
        elif ch == "'":
            out.append("\\'")
        elif o == 0x2028:
            out.append("\\u2028")
        elif o == 0x2029:
            out.append("\\u2029")
        else:
            out.append(ch)
    return "".join(out)

def main():
    with open(JS, encoding="utf-8") as f:
        data = f.read()
    trans = json.load(open(TRANS, encoding="utf-8"))

    added_total = 0
    report = []
    for ns, mid in NS_MODULES.items():
        tdict = trans.get(ns)
        if not tdict:
            continue
        # 定位模块载荷: ID:t=>{"use strict";t.exports=JSON.parse('<json>')}
        head_pat = re.compile(re.escape(mid) + r':t=>\{"use strict";t\.exports=JSON\.parse\(\'')
        tail_pat = re.compile(r"'\)\}")
        hm = head_pat.search(data)
        if not hm:
            report.append(f"[{ns}] 模块 {mid} 未找到!"); continue
        start = hm.end()
        tm = tail_pat.search(data, start)
        if not tm:
            report.append(f"[{ns}] 模块 {mid} 载荷尾部未找到!"); continue
        end = tm.start()
        raw = data[start:end]
        try:
            obj = json.loads(js_unescape(raw))
        except Exception as ex:
            report.append(f"[{ns}] 解析失败: {ex}"); continue
        before = len(obj)
        added = 0
        for k, v in tdict.items():
            if k not in obj:      # 只新增缺失,不覆盖官方翻译
                obj[k] = v
                added += 1
        added_total += added
        new_raw = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))
        new_raw_js = js_escape(new_raw)
        data = data[:start] + new_raw_js + data[end:]
        report.append(f"[{ns}] 模块 {mid}: 原 {before} key,新增 {added} key")

    with open(JS, "w", encoding="utf-8") as f:
        f.write(data)
    print("\n".join(report))
    print(f"\n完成: 共新增 {added_total} 个 key")

if __name__ == "__main__":
    main()
