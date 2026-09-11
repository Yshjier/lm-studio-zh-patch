# -*- coding: utf-8 -*-
"""从 zh_dict.json 生成 zh_dict.js(注入 window.__ZH_DICT__)"""
import json, os

base = os.path.dirname(os.path.abspath(__file__))
d = json.load(open(os.path.join(base, "zh_dict.json"), encoding="utf-8"))
js = "window.__ZH_DICT__=" + json.dumps(d, ensure_ascii=False, separators=(",", ":")) + ";\n"
out = os.path.join(base, "zh_dict.js")
with open(out, "w", encoding="utf-8") as f:
    f.write(js)
print("已生成", out, "大小", len(js))
