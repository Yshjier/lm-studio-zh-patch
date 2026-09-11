"""
add_dict_r79.py - 修正 r78 图 2 第一段 key 的尾随字符 (4599 -> 4599)

[背景]
r78 假设 textNode 包含尾随反引号 (\`), 实际 React 渲染时:
JSX `<p>...just by pointing to \`localhost:1234\` as usual.</p>`
textNode A = "...just by pointing to " (带尾空格, 不含 \`)
textNode B = " as usual." (带前导空格)
反引号是 JSX 标记 <code> 边界的语法字符, 不会进 textNode

[诊断证据]
用户部署 r78 后, 截图显示 "...just by pointing to \`localhost:1234\` 即可。"
中间只 "即可。" 翻译了 (textNode B 对得上), 整段 "Yes...pointing to " 未翻译
(对不上 r78 的 key "...just by pointing to \`")

[修正]
- 删除 key 末尾的反引号: "...just by pointing to \`" -> "...just by pointing to "
- value 同步去反引号: "...指向 \`" -> "...指向 "
"""
import json

p = 'patch/zh_dict.json'
d = json.load(open(p, encoding='utf-8'))

# 1) 删除 r78 错的 key (尾随反引号版本)
wrong_key = 'Yes. Any model in your LM Link network can be used as if it is local. Any tool that already connects to your local LM Studio server will be able to use remote models as well, just by pointing to `'
wrong_value = '可以。您的 LM Link 网络中的任何模型都可以像本地模型一样使用。任何已连接到您本地 LM Studio 服务器的工具都可以使用远程模型,只需像往常一样指向 `'

if d.get(wrong_key) == wrong_value:
    del d[wrong_key]
    print('[removed] tail-backtick version')
else:
    print('[WARN] r78 wrong key/value not found or value mismatch, skip remove')
    print('  current value:', repr(d.get(wrong_key, '<MISSING>')[:60]))

# 2) 新增正确的 key (尾随空格版本)
new_key = 'Yes. Any model in your LM Link network can be used as if it is local. Any tool that already connects to your local LM Studio server will be able to use remote models as well, just by pointing to '
new_value = '可以。您的 LM Link 网络中的任何模型都可以像本地模型一样使用。任何已连接到您本地 LM Studio 服务器的工具都可以使用远程模型,只需像往常一样指向 '

added = 0
if new_key in d:
    print('[skip-existing] tail-space version already in dict')
else:
    d[new_key] = new_value
    added = 1
    print('[added] tail-space version')

# 3) 写回 (保持格式)
text = json.dumps(d, ensure_ascii=False, indent=1)
out_lines = []
for line in text.split('\n'):
    if line in ('{', '}', ''):
        out_lines.append(line)
        continue
    if line.endswith(','):
        out_lines.append(line + ' ')
    else:
        out_lines.append(line)
text = '\r\n'.join(out_lines)
text = text.replace('\r\n', '\n').replace('\n', '\r\n')
with open(p, 'w', encoding='utf-8', newline='') as f:
    f.write(text)

d2 = json.load(open(p, encoding='utf-8'))
print()
print(f'removed: {1 if added == 1 else 0}')  # r78 wrong -> 删了 1 条
print(f'added:   {added}')
print(f'before:  {len(d2) - added + (1 if added else 0)}')
print(f'after:   {len(d2)}')

# 4) 重生成 zh_dict.js
js = 'window.__ZH_DICT__=' + json.dumps(d2, ensure_ascii=False, separators=(',', ':')) + ';\n'
with open('patch/zh_dict.js', 'w', encoding='utf-8', newline='') as f:
    f.write(js)
print(f'zh_dict.js: {len(js)} bytes')

# 5) 自检
print()
print('--- 自检 ---')
print('new key (tail-space) exists:', new_key in d2)
print('new key (tail-backtick) gone:', wrong_key not in d2)
print('current value:', repr(d2.get(new_key, '<MISSING>')[:60]))