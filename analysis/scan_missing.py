# -*- coding: utf-8 -*-
"""scan_missing.py v2 — 全量扫描 renderer 下所有 JS chunk 的 UI 可见英文，
   减去已收录字典 + 模板规则，按"来源模式 + 置信度"分级输出遗漏候选。

分级:
  P1 明确 UI  : children/label/placeholder/title/buttonText/... 且非错误消息
  P2 疑似 UI  : 其他 UI 字段(name/value/description/...)、模板前缀
  P3 内部消息 : 含 must be/Invalid/Cannot/Unexpected/Expected/No such/Error...
  P4 i18n     : key:"English" 形式（i18n 表残留）

用法: python analysis/scan_missing.py
输出: analysis/out/missing_p1.txt / missing_p2.txt / missing_p3.txt / missing_i18n.txt
"""
import re, json, os, sys, io, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', write_through=True)

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
RDIR = r'C:\Program Files\LM Studio\resources\app\.webpack\renderer'
DICT = os.path.join(ROOT, 'patch', 'zh_dict.json')
OUT = os.path.join(HERE, 'out')
os.makedirs(OUT, exist_ok=True)

SKIP = {'zh_dict.js', 'lms-zh-patch.js', 'lms-zh-translate.js'}

STRONG = ['children', 'label', 'labels', 'placeholder', 'placeholderText', 'title',
          'titleText', 'buttonText', 'ctaText', 'emptyText', 'emptyMessage',
          'confirmText', 'cancelText', 'successMessage', 'errorMessage', 'helperText',
          'helperMessage', 'tooltip', 'toolTip', 'tooltipText', 'noResults',
          'aria-label', 'ariaLabel', 'aria-description', 'headerText', 'subText',
          'statusText', 'description', 'subtitle', 'caption', 'hint', 'alt',
          'header', 'footer', 'displayName', 'message', 'text', 'promptTemplate']
WEAK = ['name', 'names', 'value', 'defaultValue', 'info', 'note', 'warning',
        'summary', 'content', 'desc']

S = '|'.join(re.escape(x) for x in STRONG)
W = '|'.join(re.escape(x) for x in WEAK)

PAT_STRONG_DQ = re.compile(r'\b(?:%s)\s*:\s*"((?:[^"\\\n]|\\.){1,300})"' % S)
PAT_STRONG_SQ = re.compile(r"\b(?:%s)\s*:\s*'((?:[^'\\\n]|\\.){1,300})'" % S)
PAT_WEAK_DQ = re.compile(r'\b(?:%s)\s*:\s*"((?:[^"\\\n]|\\.){1,300})"' % W)
PAT_WEAK_SQ = re.compile(r"\b(?:%s)\s*:\s*'((?:[^'\\\n]|\\.){1,300})'" % W)
PAT_ARR = re.compile(r'\b(?:children|items|labels|options)\s*:\s*\[([^\[\]]{1,4000})\]')
PAT_TPL = re.compile(r'''`([A-Z][A-Za-z0-9 '\-\.,:()/&+!?%$]{2,120})\$\{''')
PAT_I18N = re.compile(r'\b([a-z][a-zA-Z0-9_]{2,40}):"([A-Z][^"\n\\]{2,200})"')

BAD_RE = re.compile(
    r'https?://|\.css|\.scss|\.svg|\.png|\.jpe?g|\.gif|\.woff|\.ttf|\.ico|'
    r'\.js\b|\.ts\b|\.tsx\b|\.jsx\b|\.json\b|\.md\b|\.html\b|\.gguf\b|'
    r'__webpack|webpack|require\(|module\.|exports\.|'
    r'#([0-9a-fA-F]{3}|[0-9a-fA-F]{6}|[0-9a-fA-F]{8})\b|'
    r'rgb\(|rgba\(|hsl\(|linear-gradient|translate(?:X|Y|Z)?\(|rotate\(|scale\(|'
    r'\bpx\b|\brem\b|\bem\b|\bvh\b|\bvw\b|calc\(|var\(--|'
    r'\$\{|=>|function\s*\(|\{\{|\}\}|'
    r'^\s*(?:flex|grid|block|none|auto|solid|dashed|absolute|relative|hidden|visible|'
    r'center|start|end|left|right|top|bottom|row|column|wrap|nowrap|bold|normal|italic|'
    r'underline|pointer|default|inherit|initial|unset|transparent|currentColor)\s*$'
)

# 开发/内部消息特征（表单校验、断言、库内部报错）
ERR_RE = re.compile(
    r'\b(must\s+be|must\s+contain|must\s+have|Invalid|Cannot|Can\'t|Unexpected|'
    r'Expected|Unknown|No\s+such|not\s+found|Not\s+a\b|Failed\s+to|Unhandled|'
    r'Unrecognized|Discriminator|ZodError|exceeded|Ignoring|Missing|Requires?\b|'
    r'only\s+be|Denied|Forbidden|Multiple\s+of|instance\s+of|exactly|at\s+least|'
    r'at\s+most|null|undefined|NaN|stack|assert|panic|overflow|deprecated)\b',
    re.I)

# CSS / tailwind 类串
CSS_RE = re.compile(
    r'\b(flex|grid|items-|justify-|text-|bg-|border-|rounded-|px-|py-|mt-|mb-|'
    r'gap-|w-|h-|opacity-|font-|truncate|mr-|ml-|pt-|pb-|left-|right-|top-|bottom-|'
    r'space-|z-|grid-|col-|row-)\b')

UI_WORDS = {
    "Cancel", "Save", "Delete", "Remove", "Edit", "Copy", "Close", "Open", "Apply",
    "Reset", "Confirm", "Retry", "Refresh", "Download", "Upload", "Import", "Export",
    "Settings", "Search", "Browse", "Select", "Create", "Rename", "Duplicate", "Move",
    "Enable", "Disable", "Start", "Stop", "Pause", "Resume", "Continue", "Back", "Next",
    "Finish", "Done", "Submit", "Send", "Clear", "Reload", "Restart", "Install",
    "Uninstall", "Update", "Upgrade", "Discard", "Yes", "No", "OK", "More", "Less",
}


def is_ui_text(s):
    s = s.strip()
    if not (2 <= len(s) <= 200):
        return False
    if not re.match(r'^[A-Za-z]', s):
        return False
    if BAD_RE.search(s) or CSS_RE.search(s):
        return False
    if not re.search(r'[aeiouAEIOU]', s):
        return False
    if len(re.findall(r'[A-Za-z]+', s)) > 24:
        return False
    if ' ' not in s:
        if s in UI_WORDS:
            return True
        if re.fullmatch(r'[a-z][a-zA-Z0-9]*', s):
            return False
        if re.fullmatch(r'[a-z]+(?:_[a-z]+)+', s):
            return False
        if re.fullmatch(r'[a-z]+(?:-[a-z]+)+', s):
            return False
        if re.fullmatch(r'[A-Z0-9_]+', s):
            return False
        if re.fullmatch(r'[A-Z][a-z]{2,}', s):
            return True
        return False
    if re.search(r'[;{}]|=>', s):
        return False
    return True


def unesc(s):
    if '\\' not in s:
        return s
    try:
        return json.loads('"' + s + '"')
    except Exception:
        return (s.replace('\\"', '"').replace("\\'", "'")
                 .replace('\\n', '\n').replace('\\t', '\t').replace('\\/', '/'))


zh = json.load(open(DICT, encoding='utf-8'))
zhkeys = set(zh.keys())
TPL_RULES = [
    re.compile(r'^Delete (\d+) folder\(s\) and (\d+) chat\(s\)$'),
    re.compile(r'^Delete (\d+) folder\(s\)$'),
    re.compile(r'^Delete (\d+) chat\(s\)$'),
    re.compile(r'^More from (.+)$'),
    re.compile(r'^Delete folder "(.+)"$'),
    re.compile(r'^Open Staff Pick page for (.+)$'),
    re.compile(r'^Delete (.+)$'),
]


def covered(s):
    t = s.strip()
    for cand in (s, t, s + ' ', t + ' '):
        if cand in zhkeys:
            return True
    for r in TPL_RULES:
        if r.match(t):
            return True
    return False


cands = collections.Counter()
srcs = collections.defaultdict(set)
modes = collections.defaultdict(set)
i18n_vals = collections.Counter()

files = [f for f in sorted(os.listdir(RDIR)) if f.endswith('.js') and f not in SKIP]
print(f'scanning {len(files)} js files ...')

for fn in files:
    data = open(os.path.join(RDIR, fn), encoding='utf-8', errors='replace').read()
    got = []
    for m in PAT_STRONG_DQ.finditer(data):
        got.append((m.group(1), 'strong'))
    for m in PAT_STRONG_SQ.finditer(data):
        got.append((m.group(1), 'strong'))
    for m in PAT_ARR.finditer(data):
        for piece in re.findall(r'"((?:[^"\\\n]|\\.){1,300})"', m.group(1)):
            got.append((piece, 'strong'))
        for piece in re.findall(r"'((?:[^'\\\n]|\\.){1,300})'", m.group(1)):
            got.append((piece, 'strong'))
    for m in PAT_WEAK_DQ.finditer(data):
        got.append((m.group(1), 'weak'))
    for m in PAT_WEAK_SQ.finditer(data):
        got.append((m.group(1), 'weak'))
    for m in PAT_TPL.finditer(data):
        got.append((m.group(1), 'tpl'))
    for t, mode in got:
        u = unesc(t).strip()
        if u:
            cands[u] += 1
            srcs[u].add(fn)
            modes[u].add(mode)
    for m in PAT_I18N.finditer(data):
        v = m.group(2).strip()
        if v:
            i18n_vals[v] += 1

print(f'candidates (dedup): {len(cands):,}')

P1, P2, P3 = [], [], []
for s, c in cands.items():
    if not is_ui_text(s):
        continue
    if covered(s):
        continue
    rec = (s, c, sorted(srcs[s]))
    if ERR_RE.search(s):
        P3.append(rec)
    elif 'strong' in modes[s]:
        P1.append(rec)
    else:
        P2.append(rec)

for lst in (P1, P2, P3):
    lst.sort(key=lambda x: (-x[1], x[0]))

i18n_miss = sorted(((v, c) for v, c in i18n_vals.items()
                    if is_ui_text(v) and not covered(v)), key=lambda x: (-x[1], x[0]))

print(f'P1 明确 UI : {len(P1):,}')
print(f'P2 疑似 UI : {len(P2):,}')
print(f'P3 内部消息: {len(P3):,}')
print(f'i18n 残留  : {len(i18n_miss):,}')

with open(os.path.join(OUT, 'missing_p1.txt'), 'w', encoding='utf-8') as f:
    for s, c, fl in P1:
        f.write(f'[{c:>4}] {s}\n')
with open(os.path.join(OUT, 'missing_p2.txt'), 'w', encoding='utf-8') as f:
    for s, c, fl in P2:
        f.write(f'[{c:>4}] {s}\n')
with open(os.path.join(OUT, 'missing_p3.txt'), 'w', encoding='utf-8') as f:
    for s, c, fl in P3:
        f.write(f'[{c:>4}] {s}\n')
with open(os.path.join(OUT, 'missing_i18n.txt'), 'w', encoding='utf-8') as f:
    for s, c in i18n_miss:
        f.write(f'[{c:>4}] {s}\n')
with open(os.path.join(OUT, 'missing_p1.json'), 'w', encoding='utf-8') as f:
    json.dump([{'en': s, 'hits': c, 'files': fl} for s, c, fl in P1], f,
              ensure_ascii=False, indent=1)

print('\n=== P1 前 120 条（明确 UI，最该翻）===')
for s, c, fl in P1[:120]:
    print(f'  [{c:>4}] {s}')
