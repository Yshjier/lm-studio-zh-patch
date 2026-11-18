# -*- coding: utf-8 -*-
"""漏翻扫描公共件：renderer 路径探测、覆盖集加载、模板规则解析。

被 scan_i18n.py / scan_ui_missing.py 复用；不参与安装部署。
"""
import os, re, json, sys, io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", write_through=True)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DICT_JSON = os.path.join(ROOT, "patch", "zh_dict.json")
I18N_JSON = os.path.join(ROOT, "dict_src", "i18n.json")
ESCAPED_JSON = os.path.join(ROOT, "dict_src", "escaped.json")
PATCH_JS = os.path.join(ROOT, "patch", "lms-zh-patch.js")
OUT_DIR = os.path.join(ROOT, "tools", "analysis", "out")


def find_renderer():
    env = os.environ.get("LM_STUDIO_RENDERER")
    if env and os.path.isdir(env):
        return env
    try:
        import winreg
        for root in (winreg.HKEY_LOCAL_MACHINE, winreg.HKEY_CURRENT_USER):
            for sk in (r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall",
                       r"SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall"):
                try:
                    h = winreg.OpenKey(root, sk)
                except Exception:
                    continue
                for i in range(winreg.QueryInfoKey(h)[0]):
                    try:
                        k = winreg.OpenKey(h, winreg.EnumKey(h, i))
                        if "LM Studio" in (winreg.QueryValueEx(k, "DisplayName")[0] or ""):
                            loc = winreg.QueryValueEx(k, "InstallLocation")[0]
                            cand = os.path.join(loc, "resources", "app", ".webpack", "renderer")
                            if os.path.isdir(cand):
                                return cand
                    except Exception:
                        continue
    except Exception:
        pass
    for c in (r"C:\Program Files\LM Studio\resources\app\.webpack\renderer",
              r"D:\Program Files\LM Studio\resources\app\.webpack\renderer",
              r"C:\Program Files (x86)\LM Studio\resources\app\.webpack\renderer"):
        if os.path.isdir(c):
            return c
    raise SystemExit("未找到 LM Studio renderer 目录，可设置环境变量 LM_STUDIO_RENDERER")


def _flatten_strings(obj, out):
    if isinstance(obj, str):
        out.add(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            _flatten_strings(v, out)
    elif isinstance(obj, list):
        for v in obj:
            _flatten_strings(v, out)


def load_template_rules():
    """从观察者 JS 的 TEMPLATE_RULES 解析正则，供覆盖判定（与运行时规则同源，避免漂移）。"""
    rules = []
    if not os.path.exists(PATCH_JS):
        return rules
    js = open(PATCH_JS, encoding="utf-8").read()
    for m in re.finditer(r"\[/\^(.+?)\$/,", js):
        src = m.group(1)
        try:
            rules.append(re.compile("^" + src + "$"))
        except re.error:
            continue
    return rules


def load_coverage():
    """返回覆盖集：runtime 字典键、i18n 旁路译文、长文旁路、模板规则。"""
    cov = {"keys": set(), "i18n": set(), "escaped": set(), "rules": []}
    if os.path.exists(DICT_JSON):
        cov["keys"] = set(json.load(open(DICT_JSON, encoding="utf-8")).keys())
    if os.path.exists(I18N_JSON):
        _flatten_strings(json.load(open(I18N_JSON, encoding="utf-8")), cov["i18n"])
    if os.path.exists(ESCAPED_JSON):
        for it in json.load(open(ESCAPED_JSON, encoding="utf-8")):
            if isinstance(it, dict):
                cov["escaped"].add(it.get("old", ""))
                cov["escaped"].add(it.get("new", ""))
    cov["rules"] = load_template_rules()
    return cov


def covered(cov, s):
    t = (s or "").strip()
    if not t:
        return True
    for cand in (s, t, s + " ", t + " "):
        if cand in cov["keys"] or cand in cov["i18n"] or cand in cov["escaped"]:
            return True
    for r in cov["rules"]:
        if r.match(t):
            return True
    return False


# ---------------- 文档抽取公共辅助 ----------------
SIMPLE = {"n": "\n", "t": "\t", "r": "\r", "\\": "\\", "'": "'",
          '"': '"', "`": "`", "/": "/", "b": "\b", "f": "\f", "v": "\v", "0": "\0"}


def unesc(s):
    r"""完整解码 bundle 字符串字面量（\n \' \uXXXX \xXX 等）。"""
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


def str_end(s, i):
    """从字符串引号位置 i 找到匹配的闭合引号下标。"""
    q = s[i]; j = i + 1; n = len(s)
    while j < n:
        if s[j] == "\\":
            j += 2; continue
        if s[j] == q:
            return j
        j += 1
    return -1


def slug(route):
    """route -> docs_src/docs_zh 文件名（/ 转 __）。"""
    return route.replace("/", "__") + ".md"


def parse_articles(src, unescape=False):
    """解析 bundle 中 articles:[{route,title,prettyName,...}] 块。"""
    am = re.search(r"articles:\[", src)
    if not am:
        return []
    start = am.end()
    depth = 1; i = start
    while i < len(src) and depth:
        if src[i] == "[":
            depth += 1
        elif src[i] == "]":
            depth -= 1
        i += 1
    block = src[start:i - 1]
    arts = []
    for rm in re.finditer(r'\{route:"([^"]*)"', block):
        p = rm.start(); route = rm.group(1)
        seg = block[p:p + 6000]
        tm = re.search(r'title:"((?:[^"\\]|\\.)*)"', seg)
        pm = re.search(r'prettyName:"((?:[^"\\]|\\.)*)"', seg)
        title = tm.group(1) if tm else ""
        pretty = pm.group(1) if pm else ""
        if unescape:
            title, pretty = unesc(title), unesc(pretty)
        arts.append({"route": route, "title": title, "prettyName": pretty})
    return arts
