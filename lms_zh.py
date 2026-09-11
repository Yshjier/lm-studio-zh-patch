# -*- coding: utf-8 -*-
"""
LM Studio 中文汉化 — 单文件管理工具 (stdlib only, 无需 venv)
=============================================================
把"安装 / 卸载 / 适配新版"全部收进一个自提权、带菜单的命令。

用法(双击 lms_zh.bat，或在命令行):
    python lms_zh.py            # 交互菜单
    python lms_zh.py install    # 安装 / 重装 (幂等, 重复运行安全)
    python lms_zh.py uninstall  # 卸载 (还原原始文件, 干净移除)
    python lms_zh.py update     # 适配新版: 重抽文档 + 刷新备份 + 重新部署 + 漏翻报告
    python lms_zh.py status     # 查看当前部署状态 (不需要管理员)

需要写入 C:\\Program Files 的操作会自动请求 UAC 提权。

设计要点:
- 原始锚点(原地备份): <renderer>/main_window.js.bak (未打任何补丁的原始 bundle)
                      <renderer>/index.html.bak    (未注入的原始入口)
  这两个 .bak 与安装文件同目录, 是"干净卸载 / 重装"的唯一真相来源, 不依赖项目目录。
- install 永远从原始备份还原后再打补丁, 因此幂等且不怕半途失败。
- 适配新版(update): LM Studio 升级会覆盖 main_window.js/index.html, 此时安装目录里的
  文件就是"新版本原始", 探测到未打补丁且与旧备份不同 → 刷新备份 → 重新部署。
"""
import os, sys, io, subprocess, hashlib, json, shutil, time

# 保证 Windows 控制台中文不乱码
if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "cp65001"):
    try:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", write_through=True)
    except Exception:
        pass

ROOT = os.path.dirname(os.path.abspath(__file__))
RENDERER = None  # 运行时探测
ZH_JS = os.path.join(ROOT, "patch", "zh_dict.js")
PATCH_JS = os.path.join(ROOT, "patch", "lms-zh-patch.js")
# 原地备份: 原始备份与待修复文件放在同一安装目录 (renderer/), 而非项目 backups/
# 这样即使项目目录丢失, 卸载/还原也能独立完成。文件名用 .bak 后缀, Electron 不会加载。
LEGACY_BAK_DIR = os.path.join(ROOT, "backups")  # 仅首次迁移旧版本备份用


def bak_bundle():
    return os.path.join(find_renderer(), "main_window.js.bak")


def bak_index():
    return os.path.join(find_renderer(), "index.html.bak")
LOG = os.path.join(ROOT, "logs", "lms_zh.log")

INJECT = '<script src="zh_dict.js"></script><script src="lms-zh-patch.js"></script>'
ANCHOR = '<script defer="defer" src="main_window.js"></script>'


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
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def require_admin():
    if is_admin():
        return
    log("[提权] 需要管理员权限, 正在请求 UAC ...")
    import ctypes
    params = " ".join([__file__] + sys.argv[1:])
    ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
    sys.exit(0)


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
    cands = []
    reg = _reg_install_location()
    if reg:
        cands.append(reg)
    cands += [
        r"C:\Program Files\LM Studio\resources\app\.webpack\renderer",
        r"D:\Program Files\LM Studio\resources\app\.webpack\renderer",
        r"C:\Program Files (x86)\LM Studio\resources\app\.webpack\renderer",
    ]
    for c in cands:
        if os.path.isdir(c):
            RENDERER = c
            return RENDERER
    # 手动输入
    try:
        p = input("未自动找到 LM Studio 安装目录。\n请粘贴 renderer 目录路径"
                  " (含 .webpack\\renderer): ").strip().strip('"').strip("'")
    except EOFError:
        p = ""
    if p and os.path.isdir(p):
        RENDERER = p
        return RENDERER
    raise SystemExit("未找到 LM Studio 安装目录, 无法继续。")


def bundle_path():
    return os.path.join(find_renderer(), "main_window.js")


def index_path():
    return os.path.join(find_renderer(), "index.html")


# ---------------- 辅助 ----------------
def _sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for blk in iter(lambda: f.read(1 << 20), b""):
            h.update(blk)
    return h.hexdigest()


def is_index_patched():
    try:
        return "lms-zh-patch.js" in open(index_path(), encoding="utf-8").read()
    except Exception:
        return False


def is_bundle_patched():
    try:
        # 原生菜单补丁注入的标志字符串, bundle 原始不存在
        return "window.__ZH_DICT__" in open(bundle_path(), encoding="utf-8", errors="replace").read()
    except Exception:
        return False


def is_patched():
    return is_index_patched() or is_bundle_patched()


def kill_lmstudio():
    log("[*] 结束 LM Studio 进程 ...")
    try:
        subprocess.run(["taskkill", "/IM", "LM Studio.exe", "/F"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    except Exception:
        pass
    time.sleep(0.6)
    log("    完成 (若原本未运行则无影响)")


def _run(py_script, *args, env_extra=None):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    # 让底层脚本用我们探测到的 renderer
    env.setdefault("LMSZH_BUNDLE", bundle_path())
    env.setdefault("LMSZH_BAK", bak_bundle())
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
    """确保安装目录旁的 .bak 原始备份存在。

    - 已存在 → 直接返回
    - 缺失但项目旧 backups/ 有原始 → 迁移过来 (兼容旧版布局)
    - 缺失且当前未打补丁 → 从当前官方文件就地创建
    - 缺失且当前已打补丁且无旧备份 → 报错 (不能从已打补丁文件反推原始)
    """
    bb, bi = bak_bundle(), bak_index()
    if os.path.isfile(bb) and os.path.isfile(bi):
        return
    legacy_b = os.path.join(LEGACY_BAK_DIR, "main_window.predocs.bak")
    legacy_i = os.path.join(LEGACY_BAK_DIR, "index.html.bak")
    if os.path.isfile(legacy_b) and os.path.isfile(legacy_i):
        log("[*] 迁移旧备份 -> 安装目录原地备份 ...")
        shutil.copyfile(legacy_b, bb)
        shutil.copyfile(legacy_i, bi)
        log("    已生成 %s / %s" % (os.path.basename(bb), os.path.basename(bi)))
        return
    if is_patched():
        raise SystemExit("检测到已打补丁但缺少原始备份, 无法安全继续。\n"
                         "请先运行 install 让工具从官方文件重建 .bak 备份。")
    log("[*] 首次运行: 在安装目录就地创建原始备份 ...")
    shutil.copyfile(bundle_path(), bb)
    shutil.copyfile(index_path(), bi)
    log("    已备份 -> %s / %s" % (os.path.basename(bb), os.path.basename(bi)))


def refresh_pristine():
    log("[*] 适配新版: 用当前安装文件刷新原地备份 ...")
    shutil.copyfile(bundle_path(), bak_bundle())
    shutil.copyfile(index_path(), bak_index())
    log("    备份已刷新为新版本原始")


def restore_pristine():
    log("[*] 还原原始文件 (main_window.js + index.html) ...")
    shutil.copyfile(bak_bundle(), bundle_path())
    shutil.copyfile(bak_index(), index_path())
    log("    已还原为未打补丁状态")


# ---------------- 部署步骤 ----------------
def copy_patch():
    for src in (ZH_JS, PATCH_JS):
        dst = os.path.join(find_renderer(), os.path.basename(src))
        shutil.copyfile(src, dst)
        log("    拷贝 %s (%d bytes)" % (os.path.basename(dst), os.path.getsize(dst)))


def inject_index():
    html = open(index_path(), encoding="utf-8").read()
    if "lms-zh-patch.js" in html:
        log("    index.html 已注入, 跳过")
        return
    if ANCHOR not in html:
        raise SystemExit("index.html 未找到 main_window.js 锚点, 可能 LM Studio 版本已大改。")
    html = html.replace(ANCHOR, ANCHOR + INJECT, 1)
    open(index_path(), "w", encoding="utf-8").write(html)
    log("    index.html 已注入补丁脚本")


def remove_inject():
    html = open(index_path(), encoding="utf-8").read()
    new = html.replace(INJECT, "").replace(
        '<script src="zh_dict.js"></script>', "").replace(
        '<script src="lms-zh-patch.js"></script>', "")
    open(index_path(), "w", encoding="utf-8").write(new)
    log("    index.html 注入行已移除")


def delete_patch_files():
    for name in ("zh_dict.js", "lms-zh-patch.js"):
        p = os.path.join(find_renderer(), name)
        if os.path.exists(p):
            os.remove(p)
            log("    已删除 %s" % name)


def step_native_menu():
    log("[*] 原生菜单字节补丁 ...")
    rc = _run(os.path.join(ROOT, "patch", "patch_native_menus.py"))
    if rc != 0:
        log("    [警告] 原生菜单补丁返回非零, 可能该版本锚点变化, 右键菜单仍将英文。")


def step_doc_inject():
    log("[*] 中文开发者文档注入 (156 篇) ...")
    rc = _run(os.path.join(ROOT, "patch", "apply_docs_zh.py"), "apply")
    if rc != 0:
        log("    [警告] 文档注入返回非零, 部分开发文档可能仍英文。")


def step_extract_docs():
    log("[*] 重新抽取开发者文档 (适配新版) ...")
    _run(os.path.join(ROOT, "patch", "extract_docs.py"))


def step_scan_report():
    log("[*] 扫描新版漏翻字符串 ...")
    rc = _run(os.path.join(ROOT, "analysis", "extract_en_i18n.py"), "--dump-missing")
    if rc != 0:
        return
    miss = os.path.join(ROOT, "analysis", "out", "en_i18n_missing.json")
    if os.path.isfile(miss):
        try:
            d = json.load(open(miss, encoding="utf-8"))
            log("    字典未覆盖的 i18n 键: %d 个" % len(d))
            log("    (如需补全, 翻译后加入 patch/zh_dict.json 并重新 install)")
        except Exception:
            pass


# ---------------- 命令 ----------------
def install():
    require_admin()
    find_renderer()
    kill_lmstudio()
    if not (os.path.isfile(ZH_JS) and os.path.isfile(PATCH_JS)):
        raise SystemExit("源文件缺失: zh_dict.js / lms-zh-patch.js")
    ensure_inplace_backup()
    # 适配新版: 当前未打补丁但和旧备份不同 → 新版本
    if (not is_patched()) and os.path.isfile(bak_bundle()):
        try:
            if _sha(bundle_path()) != _sha(bak_bundle()):
                refresh_pristine()
        except Exception:
            pass
    restore_pristine()
    log("=== 开始部署 ===")
    step_native_menu()
    step_doc_inject()
    copy_patch()
    inject_index()
    log("=== 部署完成 ✅ 重启 LM Studio 生效 ===")


def uninstall():
    require_admin()
    find_renderer()
    kill_lmstudio()
    try:
        ensure_inplace_backup()
    except SystemExit:
        pass  # 备份缺失, 走下方最小化清理
    if os.path.isfile(bak_bundle()) and os.path.isfile(bak_index()):
        restore_pristine()
    else:
        log("[*] 缺少可用的原始备份, 尝试最小化清理 ...")
        remove_inject()
    delete_patch_files()
    log("=== 卸载完成 ✅ 已还原为官方英文原版 ===")


def update():
    require_admin()
    find_renderer()
    kill_lmstudio()
    step_extract_docs()
    if not is_patched():
        # 升级后安装目录里是"新版本原始"
        try:
            if (os.path.isfile(bak_bundle())
                    and _sha(bundle_path()) != _sha(bak_bundle())):
                refresh_pristine()
        except Exception:
            pass
    install()
    step_scan_report()


def status():
    try:
        r = find_renderer()
    except SystemExit as e:
        print("安装目录:", "未找到")
        print(e)
        return
    print("\n========== LM Studio 汉化状态 ==========")
    print("安装目录 :", r)
    for name in ("zh_dict.js", "lms-zh-patch.js"):
        p = os.path.join(r, name)
        print("  %-16s %s" % (name, ("%d bytes" % os.path.getsize(p)) if os.path.exists(p) else "缺失"))
    try:
        h = open(index_path(), encoding="utf-8").read()
        print("  index.html 注入 :", "是" if "lms-zh-patch.js" in h else "否")
    except Exception:
        print("  index.html      : 读取失败")
    print("  原生菜单补丁   :", "已打" if is_bundle_patched() else "未打")
    try:
        n = len([f for f in os.listdir(os.path.join(ROOT, "patch", "docs_zh")) if f.endswith(".md")])
    except Exception:
        n = 0
    print("  中文文档译文   :", "%d 篇就绪" % n)
    print("  原始备份(原地) :", "完整" if (os.path.isfile(bak_bundle()) and os.path.isfile(bak_index())) else "缺失")
    print("=======================================")
    if not (os.path.isfile(os.path.join(r, "lms-zh-patch.js")) and "lms-zh-patch.js" in
            open(index_path(), encoding="utf-8").read()):
        print("提示: 当前未部署, 运行 install 即可汉化。")


# ---------------- 菜单 ----------------
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
        print("未知命令: %s" % cmd)
    # 交互菜单
    while True:
        print("\n========== LM Studio 中文汉化管理 ==========")
        print("  1) 安装 / 重装      (幂等, 适配当前版本)")
        print("  2) 卸载             (还原官方英文原版)")
        print("  3) 适配新版         (LM Studio 升级后重抽文档+重部署)")
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
        elif c == "0" or c == "":
            break
        else:
            print("无效选择")
        if c in ("1", "2", "3"):
            try:
                input("按回车返回菜单 ... ")
            except EOFError:
                break


if __name__ == "__main__":
    menu()
