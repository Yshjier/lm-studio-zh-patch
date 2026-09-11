#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
patch_tray_menu.py  v1

托盘菜单（任务栏图标右键）是**主进程直接创建的**，不是 renderer 通过 IPC 发起的，
因此 patch_native_menus.py 处理的 renderer 侧 n()/o() 函数管不到它。

本脚本在 main/index.js 最开头注入一段代码，hook Electron 的 Menu.buildFromTemplate，
自动把所有主进程创建的菜单 label 过一遍中文翻译字典。

覆盖范围：
  - 托盘菜单（Minimize to Tray / Stop Server / Load Model / Quit 等）
  - 任何主进程直接 buildFromTemplate 创建的菜单

幂等：已 patch 过则跳过
备份：main/index.js.bak（原地备份）
"""
import os, sys, shutil

MAIN_JS = None

def find_main():
    global MAIN_JS
    if MAIN_JS:
        return MAIN_JS
    # 从环境变量读（由部署脚本传入）
    env = os.environ.get('LMSZH_MAIN')
    if env and os.path.isfile(env):
        MAIN_JS = env
        return MAIN_JS
    # 常见路径
    cands = [
        r'C:\Program Files\LM Studio\resources\app\.webpack\main\index.js',
        r'D:\Program Files\LM Studio\resources\app\.webpack\main\index.js',
    ]
    for c in cands:
        if os.path.isfile(c):
            MAIN_JS = c
            return c
    raise SystemExit('未找到主进程 index.js')


MARKER = '// === LMS-ZH tray menu patch ==='

# 注入到主进程最开头的代码
INJECT_JS = r'''// === LMS-ZH tray menu patch ===
(function() {
  try {
    const { Menu } = require('electron');
    const origBuild = Menu.buildFromTemplate;
    if (!origBuild || Menu.__zhPatched) return;
    Menu.__zhPatched = true;

    function tr(label) {
      if (!label || typeof label !== 'string') return label;
      const dict = {
        'Minimize to Tray': '最小化到托盘',
        'Stop Server': '停止服务器',
        'Copy LLM Server Base URL': '复制 LLM 服务器地址',
        'Load Model': '加载模型',
        'Quit LM Studio': '退出 LM Studio',
        'No Models Loaded': '未加载模型',
        'Loaded Models:': '已加载模型：',
        'Unload All Models': '卸载所有模型',
      };
      if (dict[label]) return dict[label];
      let m = label.match(/^LM Studio Server: Running on port (\d+)$/);
      if (m) return 'LM Studio 服务器：端口 ' + m[1] + ' 运行中';
      m = label.match(/^(\d+) Model\(s\) Loaded$/);
      if (m) return '已加载 ' + m[1] + ' 个模型';
      return label;
    }

    function walk(items) {
      if (!Array.isArray(items)) return items;
      return items.map(item => {
        if (item && typeof item.label === 'string') {
          item.label = tr(item.label);
        }
        if (item && item.subMenu) {
          item.subMenu = walk(item.subMenu);
        }
        return item;
      });
    }

    Menu.buildFromTemplate = function(template) {
      template = walk(template);
      return origBuild.call(this, template);
    };
    console.log('[lms-zh] tray menu patch loaded');
  } catch(e) {
    console.error('[lms-zh] tray menu patch failed:', e);
  }
})();
// === LMS-ZH tray menu patch end ===
'''


def main():
    main_path = find_main()
    bak_path = main_path + '.bak'

    if MARKER in open(main_path, 'r', encoding='utf-8', errors='ignore').read():
        print('    托盘菜单已汉化, 跳过')
        return

    # 备份（仅首次）
    if not os.path.exists(bak_path):
        shutil.copy2(main_path, bak_path)
        print('    已备份主进程原始文件')

    raw = open(main_path, 'r', encoding='utf-8', errors='ignore').read()
    new_raw = INJECT_JS + '\n' + raw

    try:
        with open(main_path, 'w', encoding='utf-8') as f:
            f.write(new_raw)
    except PermissionError:
        sys.exit('错误: 写入被拒, 需要管理员权限')

    print('    托盘菜单汉化完成')


if __name__ == '__main__':
    main()
