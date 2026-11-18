# -*- coding: utf-8 -*-
"""
LM Studio 简体中文汉化 — 单文件管理工具（stdlib only，无需 venv）

用法（双击 install.bat，或命令行）:
    python install.py             # 交互菜单
    python install.py install     # 安装 / 重装（幂等，重复运行安全）
    python install.py uninstall    # 卸载（还原原始文件，干净移除）
    python install.py update       # 适配新版：重抽文档 + 刷新备份 + 重部署 + 漏翻报告
    python install.py status       # 查看当前部署状态（不需要管理员）

机制:
- 运行时层: patch/zh_dict.js（window.__ZH_DICT__）+ patch/lms-zh-patch.js
  （MutationObserver + ShadowRoot 穿透，渲染后翻译可见 DOM），由 index.html 注入加载。
- 静态旁路（运行时层够不到的部分）:
  · docs 正文按 route 注入 bundle（patch/apply_docs_zh.py）
  · i18n 语言包缺键补注（patch/i18n_patch.py）
  · LM Link 长文 FAQ/引导字面量替换（patch/escaped_patch.py）
  · 主进程托盘菜单 hook（patch/patch_tray_menu.py）
- 原生 renderer 右键菜单（Electron n()/o() 通道）保持不动，本工具不处理。

原始锚点（与安装文件同目录的 .bak，是干净卸载/重装的唯一真相来源）:
  <renderer>/main_window.js.bak   未打补丁的原始 bundle
  <renderer>/index.html.bak      未注入的原始入口
  <main>/index.js.bak             未打补丁的主进程
install 永远从原始备份还原后再打补丁，因此幂等且不怕半途失败。
"""
import os, sys, io, subprocess, hashlib, json, shutil, time
import ctypes

if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "cp65001"):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", write_through=True)
    except Exception:
        pass

ROOT = os.path.dirname(os.path.abspath(__file__))
RENDERER = None
ZH_JS = os.path.join(ROOT, "patch", "zh_dict.js")
PATCH_JS = os.path.join(ROOT, "patch", "lms-zh-patch.js")
LOG = os.path.join(ROOT, "logs", "install.log")

INJECT = '<script src="zh_dict.js"></script><script src="lms-zh-patch.js"></script>'
ANCHOR = '<script defer="defer" src="main_window.js"></script>'
TRAY_MARKER = "// === LMS-ZH tray menu patch ==="


def log(*a):
    s = " ".join(str(x) for x in a)
    print(s)
    try:
        os.makedirs(os.path.dirname(LOG), exist_ok=True)
        with open(LOG, "a", encoding="utf-8") as f:
            f.write(time.strftime("%Y-%m-%d %H:%M:%S") + "  " + s + "\n")
    except Exception:
        pass


# ---------------- 权限 ----------------
def is_admin():
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except Exception:
        return False


def require_admin(action=None):
    if is_admin():
        return
    log("[*] 需要管理员权限，正在请求 UAC ...")
    args = [__file__]
    if action:
        args.append(action)
    elif len(sys.argv) > 1:
        args.extend(sys.argv[1:])
    params = subprocess.list2cmdline(args)
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    sys.exit(0)


def _wait_exit():
    # 仅在出错或交互式菜单退出前停留；成功的命令行调用直接关闭窗口
    try:
        input("\n按回车关闭窗口 ... ")
    except EOFError:
        pass


# ---------------- 路径探测 ----------------
def _reg_install_location():
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
                        disp = winreg.QueryValueEx(k, "DisplayName")[0]
                        if "LM Studio" in disp:
                            try:
                                loc = winreg.QueryValueEx(k, "InstallLocation")[0]
                            except Exception:
                                loc = ""
                            if loc:
                                cand = os.path.join(loc, "resources", "app", ".webpack", "renderer")
                                if os.path.isdir(cand):
                                    return cand
                    except Exception:
                        continue
    except Exception:
        pass
    return None


def find_renderer():
    global RENDERER
    if RENDERER:
        return RENDERER
    env = os.environ.get("LM_STUDIO_RENDERER")
    if env and os.path.isdir(env):
        RENDERER = env
        return RENDERER
    reg = _reg_install_location()
    cands = [reg] if reg else []
    cands += [
        r"C:\Program Files\LM Studio\resources\app\.webpack\renderer",
        r"D:\Program Files\LM Studio\resources\app\.webpack\renderer",
        r"C:\Program Files (x86)\LM Studio\resources\app\.webpack\renderer",
    ]
    for c in cands:
        if c and os.path.isdir(c):
            RENDERER = c
            return RENDERER
    try:
        p = input("未自动找到 LM Studio 安装目录。\n请粘贴 renderer 目录路径"
                  "（含 .webpack\\renderer）: ").strip().strip('"').strip("'")
    except EOFError:
        p = ""
    if p and os.path.isdir(p):
        RENDERER = p
        return RENDERER
    raise SystemExit("未找到 LM Studio 安装目录，无法继续。")


def find_main():
    r = find_renderer()
    p = os.path.join(os.path.dirname(r), "main", "index.js")
    if os.path.isfile(p):
        return p
    raise SystemExit("未找到主进程 index.js: " + p)


def bundle_path():
    return os.path.join(find_renderer(), "main_window.js")


def index_path():
    return os.path.join(find_renderer(), "index.html")


def bak_bundle():
    return bundle_path() + ".bak"


def bak_index():
    return index_path() + ".bak"


def bak_main():
    return find_main() + ".bak"


def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


# ---------------- 状态判定 ----------------
_file_text_cache = {}


def _read_text(path, errors="strict"):
    if path not in _file_text_cache:
        try:
            with open(path, encoding="utf-8", errors=errors) as f:
                _file_text_cache[path] = f.read()
        except Exception:
            _file_text_cache[path] = ""
    return _file_text_cache[path]


def is_index_patched():
    return "lms-zh-patch.js" in _read_text(index_path())


def is_tray_patched():
    return TRAY_MARKER in _read_text(find_main(), errors="ignore")


def is_patched():
    return is_index_patched() or is_tray_patched()


def kill_lmstudio():
    log("[*] 结束 LM Studio 进程 ...")
    try:
        subprocess.run(["taskkill", "/IM", "LM Studio.exe", "/F"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    except Exception:
        pass
    time.sleep(0.6)
    log("    完成（若原本未运行则无影响）")


def _run(py_script, *args, env_extra=None):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    env.setdefault("LMSZH_BUNDLE", bundle_path())
    env.setdefault("LMSZH_BAK", bak_bundle())
    env["PYTHONIOENCODING"] = "utf-8"
    r = subprocess.run([sys.executable, py_script, *args], capture_output=True,
                       text=True, encoding="utf-8", errors="replace", env=env, cwd=ROOT)
    out = (r.stdout or "").strip()
    if out:
        for line in out.splitlines():
            log("    | " + line)
    if r.stderr.strip():
        log("    | [stderr] " + r.stderr.strip()[:1500])
    return r.returncode


# ---------------- 备份管理 ----------------
def ensure_inplace_backup():
    bb, bi, bm = bak_bundle(), bak_index(), bak_main()
    # index.html 只可能被本补丁注入；未注入即视为原始，缺备份可直接补建。
    if not os.path.isfile(bi) and not is_index_patched():
        shutil.copyfile(index_path(), bi)
    if os.path.isfile(bb) and os.path.isfile(bi) and os.path.isfile(bm):
        return
    if is_patched():
        raise SystemExit("检测到已打补丁但缺少原始备份，无法安全继续。\n"
                         "请先 uninstall 还原，或手动补齐 .bak 原始备份。")
    log("[*] 首次运行: 在安装目录就地创建原始备份 ...")
    if not os.path.isfile(bb):
        shutil.copyfile(bundle_path(), bb)
    if not os.path.isfile(bi):
        shutil.copyfile(index_path(), bi)
    if not os.path.isfile(bm):
        shutil.copyfile(find_main(), bm)
    log("    已备份 main_window.js / index.html / main index.js")


def refresh_pristine():
    log("[*] 适配新版: 用当前安装文件刷新原地备份 ...")
    shutil.copyfile(bundle_path(), bak_bundle())
    shutil.copyfile(index_path(), bak_index())
    try:
        shutil.copyfile(find_main(), bak_main())
    except Exception:
        pass
    log("    备份已刷新为新版本原始")


def restore_pristine():
    log("[*] 还原原始文件（main_window.js + index.html + 主进程）...")
    shutil.copyfile(bak_bundle(), bundle_path())
    shutil.copyfile(bak_index(), index_path())
    try:
        shutil.copyfile(bak_main(), find_main())
    except Exception:
        pass
    for p in (bundle_path(), index_path(), find_main()):
        _file_text_cache.pop(p, None)
    log("    已还原为未打补丁状态")


# ---------------- 部署步骤 ----------------
def copy_patch():
    for src in (ZH_JS, PATCH_JS):
        dst = os.path.join(find_renderer(), os.path.basename(src))
        shutil.copyfile(src, dst)
        log("    已拷贝 %s (%d bytes)" % (os.path.basename(dst), os.path.getsize(dst)))


def inject_index():
    html = open(index_path(), encoding="utf-8").read()
    if "lms-zh-patch.js" in html:
        log("    index.html 已注入，跳过")
        return
    if ANCHOR not in html:
        raise SystemExit("index.html 未找到 main_window.js 锚点，可能 LM Studio 版本已大改。")
    html = html.replace(ANCHOR, ANCHOR + INJECT, 1)
    open(index_path(), "w", encoding="utf-8").write(html)
    _file_text_cache.pop(index_path(), None)
    log("    index.html 已注入补丁脚本")


def remove_inject():
    html = _read_text(index_path())
    new = html.replace(INJECT, "").replace(
        '<script src="zh_dict.js"></script>', "").replace(
        '<script src="lms-zh-patch.js"></script>', "")
    open(index_path(), "w", encoding="utf-8").write(new)
    _file_text_cache.pop(index_path(), None)
    log("    index.html 注入行已移除")


def delete_patch_files():
    for name in ("zh_dict.js", "lms-zh-patch.js"):
        p = os.path.join(find_renderer(), name)
        if os.path.exists(p):
            os.remove(p)
            log("    已删除 %s" % name)


def step_static_bundle():
    log("[*] 静态旁路: 长文 FAQ/引导 ...")
    _run(os.path.join(ROOT, "patch", "escaped_patch.py"))
    log("[*] 静态旁路: i18n 缺键补注 ...")
    _run(os.path.join(ROOT, "patch", "i18n_patch.py"))
    log("[*] 静态旁路: 上下文菜单标签 ...")
    _run(os.path.join(ROOT, "patch", "patch_context_menus.py"))
    log("[*] 静态旁路: 中文开发者文档注入 ...")
    rc = _run(os.path.join(ROOT, "patch", "apply_docs_zh.py"), "apply")
    if rc != 0:
        log("    [警告] 文档注入返回非零，部分开发文档可能仍英文。")


def step_tray():
    log("[*] 汉化任务栏托盘菜单 ...")
    env_extra = {"LMSZH_MAIN": find_main()}
    rc = _run(os.path.join(ROOT, "patch", "patch_tray_menu.py"), env_extra=env_extra)
    if rc != 0:
        log("    [警告] 托盘菜单汉化失败，任务栏右键仍将是英文。")


def step_extract_docs():
    log("[*] 重新抽取开发者文档英文原文 ...")
    env_extra = {"LMSZH_SRC": bundle_path()}
    rc = _run(os.path.join(ROOT, "tools", "extract_docs.py"), env_extra=env_extra)
    if rc != 0:
        log("    [警告] 文档原文抽取失败，docs_src 可能滞后于新版本。")


def step_scan_report():
    log("[*] 扫描新版漏翻候选 ...")
    _run(os.path.join(ROOT, "tools", "scan_i18n.py"))
    _run(os.path.join(ROOT, "tools", "scan_ui_missing.py"))
    try:
        miss_i18n = json.load(open(os.path.join(
            ROOT, "tools", "analysis", "out", "en_i18n_missing.json"), encoding="utf-8"))
        log("    i18n 未覆盖键: %d 个" % len(miss_i18n))
        p1 = os.path.join(ROOT, "tools", "analysis", "out", "missing_p1.json")
        if os.path.exists(p1):
            p1d = json.load(open(p1, encoding="utf-8"))
            log("    P1 明确 UI 漏翻候选: %d 条（详见 tools/analysis/out/）" % len(p1d))
    except Exception as e:
        log("    [警告] 漏翻报告读取失败: %s" % e)


# ---------------- 命令 ----------------
def _install_steps():
    require_admin("install")
    find_renderer()
    kill_lmstudio()
    if not (os.path.isfile(ZH_JS) and os.path.isfile(PATCH_JS)):
        raise SystemExit("源文件缺失: zh_dict.js / lms-zh-patch.js，请先运行 gen_dict_js.py")
    ensure_inplace_backup()
    if not is_patched() and os.path.isfile(bak_bundle()):
        try:
            if _sha(bundle_path()) != _sha(bak_bundle()):
                refresh_pristine()
        except Exception:
            pass
    restore_pristine()
    log("=== 开始部署 ===")
    step_static_bundle()
    step_tray()
    copy_patch()
    inject_index()
    log("=== 部署完成 ✅ 重启 LM Studio 生效 ===")


def install():
    _install_steps()


def uninstall():
    require_admin("uninstall")
    find_renderer()
    kill_lmstudio()
    try:
        ensure_inplace_backup()
    except SystemExit:
        pass
    if os.path.isfile(bak_bundle()) and os.path.isfile(bak_index()):
        restore_pristine()
    else:
        log("[*] 缺少可用原始备份，尝试最小化清理 ...")
        remove_inject()
    delete_patch_files()
    log("=== 卸载完成 ✅ 已还原为官方英文原版 ===")


def update():
    require_admin("update")
    find_renderer()
    kill_lmstudio()
    if not is_patched():
        try:
            if os.path.isfile(bak_bundle()) and _sha(bundle_path()) != _sha(bak_bundle()):
                refresh_pristine()
        except Exception:
            pass
    step_extract_docs()
    _install_steps()
    step_scan_report()


def status():
    try:
        r = find_renderer()
    except SystemExit as e:
        print("安装目录:", "未找到"); print(e); return
    print("\n========== LM Studio 汉化状态 ==========")
    print("安装目录:", r)
    for name in ("zh_dict.js", "lms-zh-patch.js"):
        p = os.path.join(r, name)
        print("  %-16s %s" % (name, ("%d bytes" % os.path.getsize(p)) if os.path.exists(p) else "缺失"))
    try:
        h = open(index_path(), encoding="utf-8").read()
        print("  index.html 注入 :", "是" if "lms-zh-patch.js" in h else "否")
    except Exception:
        print("  index.html      : 读取失败")
    print("  托盘菜单补丁   :", "已打" if is_tray_patched() else "未打")
    try:
        n = len([f for f in os.listdir(os.path.join(ROOT, "patch", "docs_zh")) if f.endswith(".md")])
    except Exception:
        n = 0
    print("  中文文档译文   :", "%d 篇就绪" % n)
    bak_ok = os.path.isfile(bak_bundle()) and os.path.isfile(bak_index()) and os.path.isfile(bak_main())
    print("  原始备份(原地) :", "完整" if bak_ok else "缺失")
    print("=======================================")
    if not (os.path.isfile(os.path.join(r, "lms-zh-patch.js")) and is_index_patched()):
        print("提示: 当前未部署，运行 install 即可汉化。")


def menu():
    if len(sys.argv) > 1:
        cmd = sys.argv[1].lower()
        if cmd == "install":
            return install()
        if cmd == "uninstall":
            return uninstall()
        if cmd == "update":
            return update()
        if cmd == "status":
            return status()
        print("未知命令:", cmd)
    while True:
        print("\n========== LM Studio 中文汉化管理 ==========")
        print("  1) 安装 / 重装      (幂等, 适配当前版本)")
        print("  2) 卸载             (还原官方英文原版)")
        print("  3) 适配新版         (LM Studio 升级后刷新备份+重部署)")
        print("  4) 查看状态")
        print("  0) 退出")
        print("==========================================")
        try:
            c = input("请选择 [1/2/3/4/0]: ").strip()
        except EOFError:
            break
        if c == "1":
            install()
        elif c == "2":
            uninstall()
        elif c == "3":
            update()
        elif c == "4":
            status()
        elif c in ("0", ""):
            break
        else:
            print("无效选择")


def _main():
    rc = 0
    try:
        menu()
    except SystemExit as e:
        if str(e):
            print(str(e), file=sys.stderr)
        rc = 1
    except Exception as e:
        log("[ERROR] %s" % e)
        rc = 1
    if rc != 0:
        _wait_exit()
    return rc


if __name__ == "__main__":
    sys.exit(_main())
