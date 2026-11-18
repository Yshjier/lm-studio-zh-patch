# -*- coding: utf-8 -*-
"""
托盘菜单汉化（静态旁路，主进程）。

任务栏托盘菜单由主进程 Electron Menu.buildFromTemplate 直接创建，renderer
运行时观察者层够不到。本脚本在 main/index.js 头部注入一段 IIFE，hook
Menu.buildFromTemplate，把菜单 label 过一遍中文查表；模型名等未知 label 原样返回。

用法:
    python patch_tray_menu.py apply     # 幂等注入
环境:
    LMSZH_MAIN  主进程 index.js 路径
"""
import os, sys, json, io, subprocess
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", write_through=True)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MAIN = os.environ.get("LMSZH_MAIN") or \
    r"D:\Program Files\LM Studio\resources\app\.webpack\main\index.js"
MARKER = "// === LMS-ZH tray menu patch ==="

INJECT = r'''// === LMS-ZH tray menu patch ===
(function(){
  try{
    const { Menu } = require('electron');
    if(!Menu || Menu.__zhTrayPatched) return;
    Menu.__zhTrayPatched = true;
    const dict = {
      'Minimize to Tray':'最小化到托盘',
      'Open LM Studio':'打开 LM Studio',
      'Stop Server':'停止服务器',
      'Copy LLM Server Base URL':'复制 LLM 服务器地址',
      'Load Model':'加载模型',
      'Quit LM Studio':'退出 LM Studio',
      'No Models Loaded':'未加载模型',
      'Loaded Models:':'已加载模型：',
      'Unload All Models':'卸载所有模型'
    };
    function tr(label){
      if(!label || typeof label!=='string') return label;
      if(dict[label]) return dict[label];
      let m = label.match(/^LM Studio Server: Running on port (\d+)$/);
      if(m) return 'LM Studio 服务器：端口 '+m[1]+' 运行中';
      m = label.match(/^LM Studio Server: Not Running$/);
      if(m) return 'LM Studio 服务器：未运行';
      m = label.match(/^Start Server on Port (\d+)\.\.\.$/);
      if(m) return '在端口 '+m[1]+' 启动服务器...';
      m = label.match(/^Start Server on Port (\d+)$/);
      if(m) return '在端口 '+m[1]+' 启动服务器';
      m = label.match(/^(\d+) Model\(s\) Loaded$/);
      if(m) return '已加载 '+m[1]+' 个模型';
      return label;
    }
    function walk(items){
      if(!Array.isArray(items)) return items;
      return items.map(function(item){
        if(item && typeof item.label==='string') item.label=tr(item.label);
        if(item && item.subMenu) item.subMenu=walk(item.subMenu);
        return item;
      });
    }
    const orig = Menu.buildFromTemplate;
    Menu.buildFromTemplate = function(template){
      return orig.call(this, walk(template));
    };
  }catch(e){}
})();
// === LMS-ZH tray menu patch end ===
'''


def node_check(path):
    r = subprocess.run(["node", "--check", path], capture_output=True, text=True, shell=False)
    return r.returncode == 0, (r.stdout + r.stderr)[:1500]


def main():
    if not os.path.exists(MAIN):
        print("[跳过] 未找到主进程文件:", MAIN); return
    raw = open(MAIN, "rb").read()
    if MARKER.encode("utf-8") in raw:
        print("托盘菜单: 已注入，跳过"); return

    inject = INJECT.encode("utf-8")
    expected = inject + b"\n" + raw
    tmp = MAIN + ".patchtmp.js"
    with open(tmp, "wb") as f:
        f.write(expected)
    ok, detail = node_check(tmp)
    if not ok:
        os.remove(tmp); raise SystemExit("主进程 JS 语法校验未通过：\n" + detail)
    os.replace(tmp, MAIN)
    print("托盘菜单: 已注入（node --check 通过）")


if __name__ == "__main__":
    main()
