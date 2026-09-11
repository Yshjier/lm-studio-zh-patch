# -*- coding: utf-8 -*-
"""
LM Studio 汉化补丁 - 部署/回滚工具
用法:
  python deploy.py          # 部署(幂等:重复执行安全)
  python deploy.py rollback # 回滚(删除注入行与两个补丁文件)
说明:
  - 适用于 LM Studio 0.4.24+1 的 resources/app/.webpack/renderer
  - 官方大版本升级会重置 main_window.js/index.html,升级后重跑 deploy.py 即可;
    若同时想重补官方字典缺失 key,需先用 analysis/ 脚本重新解析模块 id 再跑 gen_i18n_patch.py
"""
import os, sys, shutil

RENDERER = r"C:\Program Files\LM Studio\resources\app\.webpack\renderer"
HERE = os.path.dirname(os.path.abspath(__file__))
ZH_JS = os.path.join(HERE, "zh_dict.js")
PATCH_JS = os.path.join(HERE, "lms-zh-patch.js")
INDEX = os.path.join(RENDERER, "index.html")
INJECT = '<script src="zh_dict.js"></script><script src="lms-zh-patch.js"></script>'

def deploy():
    if not os.path.isdir(RENDERER):
        sys.exit("未找到 renderer 目录: " + RENDERER)
    # 1) 拷贝补丁文件
    for src in (ZH_JS, PATCH_JS):
        dst = os.path.join(RENDERER, os.path.basename(src))
        shutil.copyfile(src, dst)
        print("已拷贝:", dst)
    # 2) 注入 index.html(幂等)
    with open(INDEX, encoding="utf-8") as f:
        html = f.read()
    if "lms-zh-patch.js" in html:
        print("index.html 已包含注入,跳过")
    else:
        anchor = '<script defer="defer" src="main_window.js"></script>'
        if anchor not in html:
            sys.exit("未找到 main_window.js script 锚点,可能版本已变化")
        html = html.replace(anchor, anchor + INJECT, 1)
        with open(INDEX, "w", encoding="utf-8") as f:
            f.write(html)
        print("已注入 index.html")
    print("\n部署完成。重启 LM Studio 生效。")

def rollback():
    with open(INDEX, encoding="utf-8") as f:
        html = f.read()
    html = html.replace(INJECT, "")
    html = html.replace('<script src="zh_dict.js"></script>', "")
    html = html.replace('<script src="lms-zh-patch.js"></script>', "")
    with open(INDEX, "w", encoding="utf-8") as f:
        f.write(html)
    for name in ("zh_dict.js", "lms-zh-patch.js"):
        p = os.path.join(RENDERER, name)
        if os.path.exists(p):
            os.remove(p)
            print("已删除:", p)
    print("已回滚:index.html 注入行已移除,补丁文件已删除")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "rollback":
        rollback()
    else:
        deploy()
