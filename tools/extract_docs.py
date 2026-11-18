# -*- coding: utf-8 -*-
"""
从原厂 bundle 抽取全部开发者文档英文 markdown，作为译文校验对照基线。

0.4.28 结构：模块内 `articles:[{route, metadata:{title,description,prettyName},
content:"..."}]`。

输出:
  patch/docs_src/<route 转义>.md   英文原文（未转义后的纯 markdown）

默认读原厂备份 main_window.js.bak（原始英文）；备份缺失时回退当前 bundle。
译文映射见 patch/docs_manifest.json。

用法:
    python tools/extract_docs.py
"""
import io, os, re, sys, json, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", write_through=True)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _scan_common import unesc, str_end, slug, parse_articles

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RDIR = os.environ.get("LM_STUDIO_RENDERER")
if RDIR:
    BUNDLE = os.path.join(RDIR, "main_window.js")
else:
    for c in (r"D:\Program Files\LM Studio\resources\app\.webpack\renderer",
              r"C:\Program Files\LM Studio\resources\app\.webpack\renderer"):
        if os.path.isdir(c):
            BUNDLE = os.path.join(c, "main_window.js"); break
    else:
        BUNDLE = os.environ.get("LMSZH_BUNDLE", "")
BAK = os.environ.get("LMSZH_BAK") or os.path.join(os.path.dirname(BUNDLE), "main_window.js.bak")
SRC = os.environ.get("LMSZH_SRC") or (BAK if os.path.exists(BAK) else BUNDLE)
OUT = os.path.join(ROOT, "patch", "docs_src")
os.makedirs(OUT, exist_ok=True)


def locate_content(src, route):
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
    end = str_end(src, j)
    if end < 0:
        return None
    return j + 1, end


def main():
    if not SRC or not os.path.exists(SRC):
        raise SystemExit("未找到 bundle: " + SRC)
    src = open(SRC, encoding="utf-8", errors="replace").read()
    arts = parse_articles(src)
    print("bundle:", SRC, " 字符数:", len(src))
    print("articles:", len(arts))

    ok = miss = 0
    total = 0
    for a in arts:
        loc = locate_content(src, a["route"])
        if not loc:
            miss += 1
            print("  [未定位 content]", a["route"])
            continue
        body = unesc(src[loc[0]:loc[1]])
        with open(os.path.join(OUT, slug(a["route"])), "w", encoding="utf-8", newline="\n") as f:
            f.write(body)
        ok += 1
        total += len(body)

    print("抽取成功: %d 篇, 未定位: %d 篇, 原文总字符: %d (~%d KB)" % (
        ok, miss, total, total // 1024))


if __name__ == "__main__":
    main()
