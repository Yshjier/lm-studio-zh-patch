# -*- coding: utf-8 -*-
"""
运行时字典构建：dict_src/zh_dict.json -> patch/zh_dict.json（扁平 en→zh）。

单一口径：dict_src/zh_dict.json 是唯一运行时词条源，直接维护；
本脚本只做校验、过滤、排序后产出构建产物，不再做多层合并覆盖。

过滤规则（兜底护栏，正常源文件应已满足）：
  - 丢弃 en==zh 占位（产品名/URL 保持英文，无需条目）
  - 丢弃空键/空值/非字符串
  - 丢弃纯代码形状键（小写标识符、路径、协议、颜色码、版本号等）

产物再由 patch/gen_dict_js.py 生成 zh_dict.js（window.__ZH_DICT__）。
"""
import io, os, re, json, sys, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", write_through=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "dict_src", "zh_dict.json")
OUT = os.path.join(ROOT, "patch", "zh_dict.json")

# 代码/标识符/路径/颜色等不作为文案键；全大写缩写（FAQ/OK/VRAM…）属可见 UI 标签，
# 不在此拦截；英文→英文的品牌/术语（CPU/GPU/MCP/URL…）由 en==zh 占位规则自然丢弃。
NOT_TEXT_RE = re.compile(
    r"^(?:var\(--|rgb\(|#[0-9a-fA-F]{3,8}$|M\d|\.js\b|"
    r"\.md$|\.json$|\.tsx?$|\.ya?ml$|\.svg$|\.png$|"
    r"^[a-z_$][\w$.-]*$|^[A-Z][a-z]+[A-Z][A-Za-z0-9]*$)")
URL_RE = re.compile(r"https?://|www\.")


def usable(k, z):
    if not isinstance(k, str) or not isinstance(z, str):
        return False, "类型"
    if not k.strip() or not z.strip():
        return False, "空值"
    if k == z:
        return False, "占位 en==zh"
    if URL_RE.search(k):
        return False, "URL/代码"
    if NOT_TEXT_RE.match(k):
        return False, "代码形状"
    return True, ""


def main():
    if not os.path.exists(SRC):
        raise SystemExit("字典源缺失: " + SRC)
    raw = json.load(open(SRC, encoding="utf-8"))

    merged, dropped = {}, []
    for k, z in raw.items():
        ok, reason = usable(k, z)
        if not ok:
            dropped.append((reason, k))
            continue
        merged[k] = z

    merged = {k: merged[k] for k in sorted(merged)}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        json.dump(merged, f, ensure_ascii=False, indent=1, sort_keys=True)
        f.write("\n")

    print("=== 字典构建完成 ===")
    print("源:", SRC)
    print("输出:", OUT)
    print("源条目:", len(raw), " 输出条目:", len(merged))
    if dropped:
        by_reason = collections.Counter(r for r, _ in dropped)
        print("丢弃条目:", len(dropped))
        for r, n in by_reason.items():
            print("  %-12s %d" % (r, n))
        for reason, k in dropped[:20]:
            print("  *", reason, repr(k))
    else:
        print("过滤丢弃: 0")


if __name__ == "__main__":
    main()
