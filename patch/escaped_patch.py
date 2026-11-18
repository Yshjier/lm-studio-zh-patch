# -*- coding: utf-8 -*-
"""
长文转义文案静态旁路（FAQ / 新手引导多段落正文）。

这类内容在 bundle 里是带 \\n\\n 转义的长字符串，运行时被 React 拆成多个段落
文本节点，观察者无法整段命中；保留字面量整段替换。

相对时间等带变量串由观察者 TEMPLATE_RULES 在渲染后翻译，不在此静态替换。
"""
import os, sys, json, io, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", write_through=True)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUNDLE = os.environ.get("LMSZH_BUNDLE") or \
    r"D:\Program Files\LM Studio\resources\app\.webpack\renderer\main_window.js"
ESC = os.path.join(ROOT, "dict_src", "escaped.json")


def is_function_body(old):
    # 相对时间等 JS 函数体：运行时模板规则接管，不做静态整段改写
    return "=>{" in old or "function" in old


def load_entries():
    data = json.loads(open(ESC, "rb").read().decode("utf-8-sig"))
    out = []
    for it in data:
        if isinstance(it, dict) and it.get("old") and it.get("new"):
            if not is_function_body(it["old"]):
                out.append((it["old"], it["new"]))
    return out


def node_check(path):
    r = subprocess.run(["node", "--check", path], capture_output=True, text=True, shell=False)
    return r.returncode == 0, (r.stdout + r.stderr)[:1500]


def main():
    entries = load_entries()
    src = open(BUNDLE, encoding="utf-8", newline="").read()
    plan = []
    for old, new in entries:
        if new in src:
            continue  # 幂等：已替换
        if old in src:
            plan.append((old, new))
    print("长文旁路: 待替换 %d / 共 %d" % (len(plan), len(entries)))
    if not plan:
        return
    out = src
    for old, new in plan:
        out = out.replace(old, new, 1)
    tmp = BUNDLE + ".esccheck.js"
    with open(tmp, "w", encoding="utf-8", newline="") as f:
        f.write(out)
    ok, detail = node_check(tmp)
    if not ok:
        os.remove(tmp); raise SystemExit("node --check 失败：\n" + detail)
    os.replace(tmp, BUNDLE)
    print("长文旁路完成，node --check 通过")


if __name__ == "__main__":
    main()
