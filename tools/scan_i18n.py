# -*- coding: utf-8 -*-
"""
从 main_window.js 提取英文 locale 块的全部 i18n 键值对，输出字典未覆盖清单。

背景：bundle 内嵌 ~30 种语言的 i18n 表，同一个键每种语言一份；
ASCII 过滤会被荷兰语/印尼语等纯 ASCII 语言污染，按位置分块 + 英文特征词打分判定英文块。

用法:
    python tools/scan_i18n.py [--dump-missing]
输出:
    tools/analysis/out/en_i18n_all.json     英文 locale 块全量 (key -> en value)
    tools/analysis/out/en_i18n_missing.json 运行时字典 + i18n 旁路未覆盖条目
"""
import re, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _scan_common import find_renderer, load_coverage, covered, OUT_DIR, ROOT

BUNDLE = os.path.join(find_renderer(), "main_window.js")

KEY_PAT = re.compile(
    r'"((?:llm|load|chat|app|settings|common|model|hardware)[A-Za-z0-9_.]*/[A-Za-z0-9]+|[a-z][A-Za-z0-9_.]*/[A-Za-z0-9]+)":"((?:[^"\\\n]|\\.){1,500})"'
)
EN_WORDS = re.compile(r'\b(the|whether|number|that|of|to|GPU|CPU|cache|Cache|model|Model|Use|Enable|Disable|'
                      r'How|This|If|Warning|when|with|for|and|is|are|can|may|will|seed|Seed|context|Context|'
                      r'token|Token|memory|Memory|layer|Layer|expert|Expert|template|Template|prompt|Prompt|'
                      r'Auto|Random|Unrestricted|Default|Off|On|None|Recommended)\b')
DIAC = re.compile(r'[\u00C0-\u024F\u0100-\u017F\u1E00-\u1EFF]')
STRONG = re.compile(r'\b(the|and|with|your|this|that|will|when|from|are|message|settings|model|preset|context)\b', re.I)
ANY = re.compile(r'"([A-Za-z][A-Za-z0-9_.]*)":"((?:[^"\\\n]|\\.){1,800})"')
SKIP = re.compile(r'^(className|style|color|theme|variant|size|width|height|icon|path|url|src|id|type|'
                  r'font|locale|lang|version|mode|platform|key|name)$', re.I)


def cluster(hits, gap=3000):
    hits.sort()
    blocks, cur = [], [hits[0]]
    for h in hits[1:]:
        if h[0] - cur[-1][0] < gap:
            cur.append(h)
        else:
            blocks.append(cur)
            cur = [h]
    blocks.append(cur)
    return blocks


def score(block):
    return sum(len(EN_WORDS.findall(v)) for _, _, v in block if all(ord(c) < 128 for c in v))


def unescape(v):
    return v.replace('\\n', '\n').replace("\\'", "'").replace('\\"', '"').replace('\\\\', '\\')


def main():
    raw = open(BUNDLE, encoding="utf-8", errors="replace").read()
    hits = [(m.start(), m.group(1), m.group(2)) for m in KEY_PAT.finditer(raw)]
    if not hits:
        print("无命中"); return
    blocks = cluster(hits)
    cov = load_coverage()

    en_blocks = []
    for b in blocks:
        vals = [v for _, _, v in b]
        if sum(1 for v in vals if DIAC.search(v)) / len(vals) > 0.05:
            continue
        dr = sum(1 for v in vals if v in cov["keys"]) / len(vals)
        sp = sum(len(STRONG.findall(v)) for v in vals) / len(vals)
        if dr >= 0.15 or sp >= 0.4:
            en_blocks.append(b)
    print(f"[命中] {len(hits)} 条 / {len(blocks)} 块; 判定为英文的块: {len(en_blocks)}")
    for b in en_blocks:
        print(f"   块 pos={b[0][0]}~{b[-1][0]} keys={len(b):4d}")

    en = {}
    for b in en_blocks:
        lo, hi = b[0][0], b[-1][0]
        for m in ANY.finditer(raw, lo, hi):
            en.setdefault(m.group(1), unescape(m.group(2)))
    en = {k: v for k, v in en.items() if not SKIP.match(k.split("/")[-1])}

    os.makedirs(OUT_DIR, exist_ok=True)
    json.dump(en, open(os.path.join(OUT_DIR, "en_i18n_all.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    miss = {k: v for k, v in en.items() if not covered(cov, v)}
    json.dump(miss, open(os.path.join(OUT_DIR, "en_i18n_missing.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=1)
    print(f"[合计] 英文块键数 {len(en)}, 未覆盖 {len(miss)}")

    if "--dump-missing" in sys.argv:
        for k in sorted(miss):
            print("  ", k, "=", json.dumps(miss[k], ensure_ascii=False)[:220])


if __name__ == "__main__":
    main()
