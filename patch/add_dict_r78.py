"""
add_dict_r78.py — 修正第 77 轮的 LM Link FAQ 答案条目。

第 77 轮的假设: textNode 包含 markdown 源码字符 (**No!** / `localhost:1234`)
实际情况:     React 把 ** 和反引号解析成 <strong>/<code> 元素,
              textNode 被切分成多段, 整段匹配永远命中不了

修正策略: 删除 3 条错误的整段条目, 新增 7 条按实际 textNode 拆分的小段条目
"""
import json

p = 'patch/zh_dict.json'
d = json.load(open(p, encoding='utf-8'))

# 1) 删除第 77 轮加错的 3 条整段条目 (key 含 ** 或 反引号整段)
wrong_keys = [
    "**No!** All your devices in the LM Link network communicate with each other using a mesh VPN connection powered by Tailscale. They use end-to-end encrypted connections and communicate without opening any ports to the internet.",
    "Moreover, LM Link runs entirely in userspace and does **not change** anything globally on your device, such as networking settings or firewall settings.",
    "Yes. Any model in your LM Link network can be used as if it is local. Any tool that already connects to your local LM Studio server will be able to use remote models as well, just by pointing to `localhost:1234` as usual.",
]

removed = 0
for k in wrong_keys:
    if k in d:
        del d[k]
        removed += 1
        print(f'[removed] {k[:60]}...')

# 2) 新增 7 条按实际 textNode 拆分的小段条目
new_entries = {
    # 图 1 段落 1: <strong>No!</strong> + 剩余 textNode
    "No!": "不!",
    " All your devices in the LM Link network communicate with each other using a mesh VPN connection powered by Tailscale. They use end-to-end encrypted connections and communicate without opening any ports to the internet.":
        "您的 LM Link 网络中的所有设备都通过 Tailscale 支持的网格 VPN 连接相互通信。它们使用端到端加密连接,无需向互联网开放任何端口即可通信。",

    # 图 1 段落 2: 开头 textNode + <strong>not change</strong> + 末尾 textNode
    "Moreover, LM Link runs entirely in userspace and does ":
        "此外,LM Link 完全在用户态运行,",
    "not change": "不会",
    " anything globally on your device, such as networking settings or firewall settings.":
        " 您设备上的任何全局设置,例如网络设置或防火墙设置。",

    # 图 2 段落 1: 开头 textNode (保留尾随反引号) + <code>localhost:1234</code> + 末尾 textNode
    "Yes. Any model in your LM Link network can be used as if it is local. Any tool that already connects to your local LM Studio server will be able to use remote models as well, just by pointing to `":
        "可以。您的 LM Link 网络中的任何模型都可以像本地模型一样使用。任何已连接到您本地 LM Studio 服务器的工具都可以使用远程模型,只需像往常一样指向 `",
    " as usual.": " 即可。",
}

added = 0
skipped = 0
for k, v in new_entries.items():
    if k in d:
        skipped += 1
        print(f'[skip-existing] {k[:60]}...')
        continue
    d[k] = v
    added += 1
    print(f'[added] {k[:60]}...')

# 3) 写回 zh_dict.json (保持原格式: 1 空格缩进 + 行尾 ", " + CRLF + 末项无尾逗号)
text = json.dumps(d, ensure_ascii=False, indent=1)
out_lines = []
for line in text.split('\n'):
    if line in ('{', '}', ''):
        out_lines.append(line)
        continue
    if line.endswith(','):
        out_lines.append(line + ' ')  # 行尾 ", "
    else:
        out_lines.append(line)  # 末项
text = '\r\n'.join(out_lines)
text = text.replace('\r\n', '\n').replace('\n', '\r\n')

with open(p, 'w', encoding='utf-8', newline='') as f:
    f.write(text)

# 4) 验证 JSON 合法性 + 重生成 zh_dict.js (紧凑格式)
d2 = json.load(open(p, encoding='utf-8'))
print()
print(f'removed: {removed}')
print(f'added:   {added}')
print(f'skipped: {skipped}')
print(f'before:  {len(d2) - added + removed}')
print(f'after:   {len(d2)}')

# 5) 重生成 zh_dict.js
js = 'window.__ZH_DICT__=' + json.dumps(d2, ensure_ascii=False, separators=(',', ':')) + ';\n'
with open('patch/zh_dict.js', 'w', encoding='utf-8', newline='') as f:
    f.write(js)
print(f'zh_dict.js: {len(js)} bytes')

# 6) 自检: 确认 7 条新 key 都在
print()
print('--- 自检 ---')
for k in new_entries.keys():
    print(f'  {repr(k[:50])}... -> {repr(d2.get(k, "<MISSING>")[:40])}...')
