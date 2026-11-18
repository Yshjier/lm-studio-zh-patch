# -*- coding: utf-8 -*-
"""运行时字典审计：异常条目、占位 en==zh、代码形状键、首尾空格键、纯 CJK 键。"""
import sys, io, os, json, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", write_through=True)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = json.load(open(os.path.join(ROOT, "patch", "zh_dict.json"), encoding="utf-8"))

NOT_TEXT_RE = re.compile(
    r"^(?:var\(--|rgb\(|#[0-9a-fA-F]{3,8}$|M\d|\.js\b|"
    r"\.md$|\.json$|\.tsx?$|\.ya?ml$|\.svg$|\.png$|"
    r"^[a-z_$][\w$.-]*$|^[A-Z][a-z]+[A-Z][A-Za-z0-9]*$)")
URL_RE = re.compile(r"https?://|www\.")

bad, space_keys, cjk_keys, code_shape = [], [], [], []
for k, z in D.items():
    if not isinstance(k, str) or not isinstance(z, str) or not z.strip() or k == z:
        bad.append((k, z)); continue
    if URL_RE.search(k) or NOT_TEXT_RE.match(k):
        code_shape.append(k)
    if k != k.strip():
        space_keys.append(k)
    if k and all(ord(c) > 0x2E80 for c in k):
        cjk_keys.append(k)

print("总条数:", len(D))
print("异常(空值/en==zh/类型):", len(bad))
for b in bad[:20]:
    print("  ", b)
print("代码形状键:", len(code_shape), code_shape[:10])
print("含首尾空格键:", len(space_keys), "样例:", [repr(x) for x in space_keys[:8]])
print("纯 CJK 键:", len(cjk_keys), cjk_keys[:10])

# 译文重复（同一中文对应多个英文，仅供参考，不算错误）
val_groups = collections.defaultdict(list)
for k, z in D.items():
    val_groups[z].append(k)
dup = {z: ks for z, ks in val_groups.items() if len(ks) > 1}
print("多对一译文组数:", len(dup))

# 源字典与产物一致性核对
src_path = os.path.join(ROOT, "dict_src", "zh_dict.json")
if os.path.exists(src_path):
    sd = json.load(open(src_path, encoding="utf-8"))
    src_keys, out_keys = set(sd), set(D)
    print("源条目:", len(sd), " 产物条目:", len(D))
    only_src = sorted(src_keys - out_keys)
    only_out = sorted(out_keys - src_keys)
    print("  有源无产物:", len(only_src), only_src[:10])
    print("  有产物无源:", len(only_out), only_out[:10])
    val_diff = [k for k in src_keys & out_keys if sd[k] != D[k]]
    print("  译文不一致:", len(val_diff), val_diff[:10])
