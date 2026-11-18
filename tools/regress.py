# -*- coding: utf-8 -*-
"""端到端回归：临时布局模拟 renderer/main，跑 install -> 校验 -> uninstall -> 还原校验。"""
import io, os, sys, shutil, hashlib, subprocess, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", write_through=True)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REAL = r"D:\Program Files\LM Studio\resources\app\.webpack"
REG = os.path.join(ROOT, "tools", "tmp", "reg")
REND = os.path.join(REG, "renderer")
MAIND = os.path.join(REG, "main")

shutil.rmtree(REG, ignore_errors=True)
os.makedirs(REND); os.makedirs(MAIND)

# 原厂原始文件
shutil.copy2(os.path.join(REAL, "renderer", "main_window.js.bak"), os.path.join(REND, "main_window.js"))
shutil.copy2(os.path.join(REAL, "renderer", "index.html.bak"), os.path.join(REND, "index.html"))
shutil.copy2(os.path.join(REAL, "main", "index.js.bak"), os.path.join(MAIND, "index.js"))

os.environ["LM_STUDIO_RENDERER"] = REND
sys.path.insert(0, ROOT)
import install  # noqa: E402

install.require_admin = lambda *a, **k: None
install.kill_lmstudio = lambda: None
install._wait_exit = lambda: None


def sha(p):
    h = hashlib.sha256()
    h.update(open(p, "rb").read()); return h.hexdigest()


def node_check(p):
    r = subprocess.run(["node", "--check", p], capture_output=True, text=True, shell=False)
    return r.returncode == 0, (r.stdout + r.stderr)[:800]


print("===== 安装 =====")
install._install_steps()

bundle = os.path.join(REND, "main_window.js")
index = os.path.join(REND, "index.html")
mainjs = os.path.join(MAIND, "index.js")

checks = []
checks.append(("字典 JS 已拷贝", os.path.exists(os.path.join(REND, "zh_dict.js"))))
checks.append(("观察者 JS 已拷贝", os.path.exists(os.path.join(REND, "lms-zh-patch.js"))))
html = open(index, encoding="utf-8").read()
checks.append(("index.html 已注入", "lms-zh-patch.js" in html and "zh_dict.js" in html))
main = open(mainjs, encoding="utf-8", errors="ignore").read()
checks.append(("托盘 hook 已注入", install.TRAY_MARKER in main))
src = open(bundle, encoding="utf-8", errors="replace").read()
checks.append(("docs 中文已注入", "投机解码" in src or "对话补全" in src))
checks.append(("i18n 缺键已补", "推理预算" in src))
checks.append(("长文 FAQ 已替换", "端到端加密" in src))
ok_b, d_b = node_check(bundle)
ok_m, d_m = node_check(mainjs)
checks.append(("bundle node --check", ok_b))
checks.append(("main node --check", ok_m))

for name, ok in checks:
    print(("  [OK] " if ok else "  [FAIL] ") + name)
if not ok_b: print(d_b)
if not ok_m: print(d_m)

# 记录安装后大小
print("bundle 大小:", os.path.getsize(bundle), " main 大小:", os.path.getsize(mainjs))

print("\n===== 卸载 =====")
install.uninstall()

baks = {
    "bundle": os.path.join(REND, "main_window.js.bak"),
    "index": os.path.join(REND, "index.html.bak"),
    "main": os.path.join(MAIND, "index.js.bak"),
}
restored = [
    ("bundle 已还原", sha(bundle) == sha(baks["bundle"])),
    ("index 已还原", sha(index) == sha(baks["index"])),
    ("main 已还原", sha(mainjs) == sha(baks["main"])),
    ("字典 JS 已删除", not os.path.exists(os.path.join(REND, "zh_dict.js"))),
    ("观察者 JS 已删除", not os.path.exists(os.path.join(REND, "lms-zh-patch.js"))),
    ("index 注入已移除", "lms-zh-patch.js" not in open(index, encoding="utf-8").read()),
]
for name, ok in restored:
    print(("  [OK] " if ok else "  [FAIL] ") + name)

failed = [n for n, ok in checks + restored if not ok]
print("\n结果:", "全部通过 ✅" if not failed else "失败: %s" % failed)
sys.exit(1 if failed else 0)
