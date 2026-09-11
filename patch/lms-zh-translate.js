/*!
 * LM Studio 运行时英→中自动翻译模块 v1.4 (独立模块, 不依赖 lms-zh-patch.js)
 *
 * 目标: 翻译运行时从 HuggingFace / 文档 API 动态拉取的英文段落
 *       (模型描述, README, REST API 文档正文, 开发者页长句提示等),
 *       这些字符串不在 bundle 里, 字典补丁无法覆盖。
 *
 * 设计原则(铁律):
 *   1. 最坏结果 = 不翻译, 绝不显示半中半英或破坏布局
 *   2. 只改 textNode.nodeValue, 绝不动 DOM 结构 (保护 React fiber)
 *   3. 已翻译节点存原文到 data-zh-original, 可一键还原
 *   4. 任何异常都 catch 并保留原文
 *   5. 翻译接口全部失败/超时才跳过, 不影响其它功能
 *
 * 退回方式:
 *   - 运行时: window.__ZH_TRANSLATE__.restoreAll()  还原已翻译文本
 *             window.__ZH_TRANSLATE__.disable()     停用(写 localStorage, 重启后也失效)
 *   - 文件级: python patch_translate.py rollback    移除 index.html 注入
 *   - 持久关: localStorage.setItem('lmszh_translate','off')
 *
 * 触发:
 *   - 右下角「译」按钮 (可拖动, 位置保存)
 *       - 单击: 翻译当前页可见英文
 *       - 双击: 还原全部已翻译
 *       - 右键: 弹出菜单 (还原 / 切换自动 / 设置后端 / 不透明度)
 *       - 拖动 5px 以上: 移动按钮位置 (松手若落在左半屏/顶部则自动归位右侧)
 *   - 快捷键 Ctrl+Shift+T
 *   - 自动模式(默认开): 新内容出现时自动翻译
 *
 * v1.5 升级:
 *   - 修路径面包屑被误翻: "developer › rest › endpoints" 整段 30 字符过自动阈值, 走在线翻译
 *     变成"开发者 › 休息 › 端点"破坏 URL 路径。
 *     新增 looksCode 路径分隔符识别 + 父元素 nav/breadcrumb 容器跳过, 双重保险。
 * v1.4 升级:
 *   - 修复 v1.3 的 _attrRetry 死代码: scheduleAttrRetry() 之前误设 run._manual=true 但调用的
 *     run() 直接传 manual=false, 完全无效; 改为直接调 manualRun() 走手动阈值路径
 *   - 按钮自我保护: 每 3 秒检查, 按钮 DOM 不存在则自动重建(防止 React/视图切换时丢失)
 * v1.3 升级:
 *   - 全局 CSS 防换行: 防止 "Integrations" → "集成" 后按钮/侧栏宽度不足导致中文竖排
 *   - title/placeholder 即时重翻: React 重设 raw value 也能在下一帧重新翻译
 *     (通过 attributeMutation 监听 + 下一 microtask 重翻)
 *   - 模板前缀匹配: Delete folder "..." / Are you sure? This will ... 等模板
 *     字串里变量不可枚举, 整段匹配失败; 改成前缀 + 变量保留的拼接翻译
 *   - toast 短词白名单 (Copied!/Saved!/Failed!/Done!/...): 即便字典没补,
 *     也对 7 字符以下的常见反馈文案尝试翻译
 *
 * v1.2 升级:
 *   - 光标: 仅在拖动时显示抓手(grabbing), 悬停时恢复指针
 *   - 右键弹出菜单 (替代长按); 触屏保留长按弹出菜单
 *   - 拖动范围限制在视口内; 松手若落在左半屏或顶部区域则自动归位到右下
 *   - 鼠标移开后半透明, 悬停恢复
 *   - 右键菜单可调不透明度 (20% 一档, 持久化到 localStorage)
 *   - 已知短词白名单 (Arch/Quant/Quantization/Context 等模型属性标签)
 *   - 短文本阈值细化: 长段落 ≥20 字符; 已知短词白名单不限长度; 其它 4-19 字符可手动触发
 */
(function () {
  'use strict';
  if (window.__ZH_TRANSLATE__) return;            // 防重复加载

  var OFF = false;
  try { OFF = localStorage.getItem('lmszh_translate') === 'off'; } catch (e) {}
  var AUTO = !OFF;
  try { if (localStorage.getItem('lmszh_translate') === 'auto') AUTO = true; } catch (e) {}

  var cache = new Map();           // 原文 -> 译文
  var translatedNodes = [];        // 已翻译的 textNode
  var pending = false;
  var BACKEND = 'auto';            // auto | lmstudio | ollama | google
  var detected = null;
  var CJK = /[㐀-䶿一-鿿豈-﫿]/;

  // ---------------- 全局 CSS: 防换行 + 防宽度塌陷 ----------------
  // "Integrations" (12 字符) → "集成" (2 字符) 后, 部分 flex 容器按英文宽度
  // 算的 min-width 偏大, 中文容不下导致按字换行 ("集" / "成" 竖排).
  // 注入一段保守 CSS 强制常见控件 white-space: nowrap, 同时允许整体 min-width: 0.
  (function injectZhCss() {
    try {
      if (document.getElementById('__zh_tr_css')) return;
      var s = document.createElement('style');
      s.id = '__zh_tr_css';
      s.textContent =
        // LMS 汉化专用: 中英文长度差异, 防止按钮/标签/侧栏按字换行
        'button,[role="button"],a,label,[class*="Button"],[class*="Btn"],[class*="Tab"],[class*="Heading"],[class*="Title"],[class*="Header"],[class*="Label"],[class*="Caption"]{white-space:nowrap}' +
        // 允许 flex 子项收缩到内容宽度 (中文短词不会撑容器)
        '[class*="flex"]>[class*="grow"],[class*="flex"]>[class*="shrink"]{min-width:0}' +
        // 已翻译的 textNode 加微弱虚线下划线, 提示"这是机器翻译"
        '[data-zh-translated]{text-decoration-style:dotted;text-decoration-color:rgba(127,209,255,.3);text-underline-offset:2px}' +
        // 自带的 FAB 拖动时抢 cursor
        '#__zh_tr_btn{cursor:pointer !important;transition:opacity .15s ease}';
      (document.head || document.documentElement).appendChild(s);
    } catch (e) {}
  })();

  // ---------------- toast 短词白名单 (7 字符以下常见反馈) ----------------
  // 即便字典漏补, 也能即时翻译; 不需要 20 字符阈值
  var TOAST_WHITELIST = {
    'Copied!':'\u5df2\u590d\u5236!','Copied':'\u5df2\u590d\u5236',
    'Saved!':'\u5df2\u4fdd\u5b58!','Saved':'\u5df2\u4fdd\u5b58',
    'Failed!':'\u5931\u8d25!','Failed':'\u5931\u8d25',
    'Done!':'\u5b8c\u6210!','Done':'\u5b8c\u6210',
    'Deleted!':'\u5df2\u5220\u9664!','Deleted':'\u5df2\u5220\u9664',
    'Removed!':'\u5df2\u79fb\u9664!','Removed':'\u5df2\u79fb\u9664',
    'Cancelled':'\u5df2\u53d6\u6d88','Cancelled!':'\u5df2\u53d6\u6d88!',
    'Error!':'\u9519\u8bef!','Error':'\u9519\u8bef',
    'OK!':'\u5b8c\u6210!','Loading…':'\u52a0\u8f7d\u4e2d\u2026',
    'Loading...':'\u52a0\u8f7d\u4e2d\u2026','Success!':'\u6210\u529f!',
    'Success':'\u6210\u529f','Cancel':'\u53d6\u6d88','Confirm':'\u786e\u5b9a'
  };

  // ---------------- 已知短词白名单 ----------------
  // 模型属性/技术术语, 单个词不需要 20 字符阈值
  var SHORT_KW = {
    'Arch':'\u67b6\u6784','Architecture':'\u67b6\u6784','Archs':'\u67b6\u6784',
    'Domain':'\u6a21\u578b\u9886\u57df','Domains':'\u6a21\u578b\u9886\u57df',
    'Quant':'\u91cf\u5316','Quantization':'\u91cf\u5316',
    'Context':'\u4e0a\u4e0b\u6587','Parameters':'\u53c2\u6570\u91cf','Tensor':'\u5f20\u91cf','Tensors':'\u5f20\u91cf',
    'Vocab':'\u8bcd\u8868','Tokenizer':'\u5206\u8bcd\u5668','Sampler':'\u91c7\u6837\u5668',
    'Backend':'\u540e\u7aef','Engine':'\u5f15\u64ce','Format':'\u683c\u5f0f','Type':'\u7c7b\u578b',
    'Status':'\u72b6\u6001','State':'\u72b6\u6001','Role':'\u89d2\u8272','Mode':'\u6a21\u5f0f',
    'Memory':'\u5185\u5b58','VRAM':'\u663e\u5b58','RAM':'\u5185\u5b58',
    'Cache':'\u7f13\u5b58','Cached':'\u5df2\u7f13\u5b58',
    'Active':'\u6d3b\u52a8','Running':'\u8fd0\u884c\u4e2d','Loaded':'\u5df2\u52a0\u8f7d','Loading':'\u52a0\u8f7d\u4e2d',
    'Stopped':'\u5df2\u505c\u6b62','Paused':'\u5df2\u6682\u505c','Ready':'\u5c31\u7eea',
    'Allowed':'\u5141\u8bb8','Blocked':'\u963b\u6b62','Disabled':'\u5df2\u7981\u7528','Enabled':'\u5df2\u542f\u7528',
    'Default':'\u9ed8\u8ba4','Custom':'\u81ea\u5b9a\u4e49','Advanced':'\u9ad8\u7ea7','Basic':'\u57fa\u7840',
    'Local':'\u672c\u5730','Remote':'\u8fdc\u7a0b','Network':'\u7f51\u7edc',
    'Save':'\u4fdd\u5b58','Load':'\u52a0\u8f7d','Open':'\u6253\u5f00','Close':'\u5173\u95ed','Delete':'\u5220\u9664','Edit':'\u7f16\u8f91','New':'\u65b0\u5efa',
    'Yes':'\u662f','No':'\u5426','OK':'\u786e\u5b9a','Cancel':'\u53d6\u6d88',
    'Auto':'\u81ea\u52a8','Manual':'\u624b\u52a8'
  };

  // ---------------- 模板前缀匹配 (整段含变量不可枚举, 改用前缀 + 变量保留) ----------------
  // 例: `Delete folder "${name}"` React 渲染成完整 title "Delete folder \"Empty Folder\"",
  //     字典里没有这个完整 key —— 改用以下正则匹配, 把变量部分原样保留
  // 返回 {prefixZh, suffixZh, rx} — translateBatch 命中后用 prefixZh + 变量 + suffixZh 拼接
  var TEMPLATE_PREFIXES = [
    // template_regex       prefix_zh                suffix_zh
    { rx: /^Delete folder "(.*)"$/,           pZh: '\u5220\u9664\u6587\u4ef6\u5939 "', sZh: '"' },
    { rx: /^Delete file "(.*)"$/,             pZh: '\u5220\u9664\u6587\u4ef6 "',     sZh: '"' },
    { rx: /^Rename "(.*)"$/,                  pZh: '\u91cd\u547d\u540d "',           sZh: '"' },
    { rx: /^Delete "(.*)"$/,                  pZh: '\u5220\u9664 "',                 sZh: '"' },
    { rx: /^Are you sure\? .*$/,              pZh: '\u786e\u5b9a\u5417\uff1f',       sZh: ''   },
  ];
  function lookupTemplatePrefix(text) {
    for (var i = 0; i < TEMPLATE_PREFIXES.length; i++) {
      var t = TEMPLATE_PREFIXES[i];
      var m = t.rx.exec(text);
      if (m) return { pZh: t.pZh, mid: m[1] || '', sZh: t.sZh };
    }
    return null;
  }

  // ---------------- 工具 ----------------
  function hasCJK(s) { return CJK.test(s); }
  function isPureNonText(s) { return /^[\s\d\W]+$/.test(s); }
  function looksCode(s) {
    if (/\/api\/v\d+\//.test(s)) return true;
    if (/^\s*[<{[(]/.test(s) && /[}>)\]]$/.test(s.trim())) return true;
    if (/(=>|;\s*$|::|->|=>)/.test(s)) return true;
    if (/[{};=]/.test(s) && s.length < 140 && /^[\w\s{};=:.\-/]+$/.test(s)) return true;
    // v1.5: 面包屑/路径导航片段 ("developer › rest › endpoints" / "docs / api / v0")
    // 多个路径分隔符 + 全英文小写片段, 一旦走在线翻译会破坏 URL — 视为代码
    if (/^[A-Za-z][A-Za-z0-9_-]*(\s[›»→/]+\s[A-Za-z0-9_-]+){2,}$/.test(s.trim())) return true;
    return false;
  }

  // ---------------- 节点筛选 ----------------
  // 四档阈值:
  //   A. 已知短词白名单 (SHORT_KW) / Toast 白名单 (TOAST_WHITELIST): 直接放行
  //   B. 模板前缀命中 (lookupTemplatePrefix): 整段中长度, 不限
  //   C. 手动模式或 CLICK 触发: 4-19 字符也可尝试
  //   D. 自动模式: ≥20 字符
  function shouldTranslate(node, opts) {
    opts = opts || {};
    var manual = !!opts.manual;
    if (!node || node.nodeType !== 3) return false;
    var t = node.nodeValue;
    if (!t || !t.trim()) return false;
    var trimmed = t.trim();
    if (hasCJK(t)) return false;
    if (isPureNonText(t)) return false;
    if (looksCode(t)) return false;

    var len = trimmed.length;
    var allow = false;
    if (SHORT_KW[trimmed]) {
      allow = true;                                   // A1 档: 已知属性词
    } else if (TOAST_WHITELIST[trimmed]) {
      allow = true;                                   // A2 档: toast / 反馈
    } else if (lookupTemplatePrefix(trimmed)) {
      allow = true;                                   // B 档: 模板前缀 (整段匹配)
    } else if (manual) {
      allow = len >= 2 && len <= 300;                 // C 档: 手动模式放宽
    } else {
      allow = len >= 20;                              // D 档: 自动模式严阈值
    }
    if (!allow) return false;

    var p = node.parentNode;
    while (p) {
      var tag = p.tagName ? p.tagName.toLowerCase() : '';
      if (tag === 'code' || tag === 'pre' || tag === 'script' || tag === 'style' ||
          tag === 'textarea' || tag === 'input') return false;
      if (tag === 'button' || tag === 'a') {
        // button/a 直接文本节点常是 UI 控件, 交给字典; 但其子段落长文/模板前缀可翻
        if (p.childNodes.length <= 1 && !SHORT_KW[trimmed] && !TOAST_WHITELIST[trimmed] && !lookupTemplatePrefix(trimmed)) return false;
      }
      if (p.hasAttribute && (p.hasAttribute('data-zh-translated') || p.hasAttribute('data-zh-skip'))) return false;
      // v1.5: nav / breadcrumb 容器内文本不翻译, 避免破坏 URL 路径
      if (p.tagName === 'NAV' || (p.getAttribute && p.getAttribute('role') === 'navigation')) return false;
      if (p.className && typeof p.className === 'string' && /breadcrumb|crumb/i.test(p.className)) return false;
      p = p.parentNode;
    }
    return true;
  }

  function collect(manual) {
    var nodes = [], n;
    var walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null, false);
    while ((n = walker.nextNode())) {
      if (shouldTranslate(n, {manual: manual}) && !n.__zhMarked) {
        n.__zhMarked = true;
        nodes.push(n);
      }
    }
    return nodes;
  }

  // ---------------- 后端探测 ----------------
  function getFirstModel(backend) {
    return new Promise(function (res) {
      var url = backend === 'lmstudio' ? 'http://localhost:1234/v1/models' : 'http://localhost:11434/api/tags';
      fetch(url).then(function (r) { return r.json(); }).then(function (j) {
        if (backend === 'lmstudio' && j.data && j.data.length) res(j.data[0].id);
        else if (backend === 'ollama' && j.models && j.models.length) res(j.models[0].name);
        else res('');
      }).catch(function () { res(''); });
    });
  }

  function detectBackend() {
    if (detected) return Promise.resolve(detected);
    return new Promise(function (res) {
      fetch('http://localhost:1234/v1/models').then(function (r) {
        if (r.ok) { detected = 'lmstudio'; return res('lmstudio'); }
        return fetch('http://localhost:11434/api/tags');
      }).then(function (r) {
        if (r && r.ok) { detected = 'ollama'; return res('ollama'); }
        detected = 'google'; res('google');
      }).catch(function () { detected = 'google'; res('google'); });
    });
  }

  // ---------------- 翻译执行 ----------------
  function extractJsonArray(s) {
    try {
      var a = s.indexOf('['), b = s.lastIndexOf(']');
      if (a >= 0 && b > a) return JSON.parse(s.slice(a, b + 1));
    } catch (e) {}
    return null;
  }

  // 优先查字典, 再走在线翻译 (短词白名单命中时直接用)
  function tryFromDict(texts) {
    var dict = window.__ZH_DICT__ || {};
    var out = [], allInDict = true;
    for (var i = 0; i < texts.length; i++) {
      var t = texts[i];
      var trimmed = t.trim();
      // 1) 静态字典精确匹配
      var hit = dict[t] || dict[trimmed];
      // 2) 已知属性词
      if (!hit) hit = SHORT_KW[trimmed];
      // 3) toast / 短反馈白名单
      if (!hit) hit = TOAST_WHITELIST[trimmed];
      // 4) 模板前缀: 拼接 中文前缀 + 变量原文 + 中文后缀
      if (!hit) {
        var tpl = lookupTemplatePrefix(trimmed);
        if (tpl) hit = tpl.pZh + tpl.mid + tpl.sZh;
      }
      if (hit) { out.push(hit); }
      else { out.push(null); allInDict = false; }
    }
    return allInDict ? out : null;
  }

  function doTranslateGoogle(texts) {
    return Promise.all(texts.map(function (t) {
      return fetch('https://translate.googleapis.com/translate_a/single?client=gtx&sl=en&tl=zh-CN&dt=t&q=' +
        encodeURIComponent(t))
        .then(function (r) { return r.json(); })
        .then(function (j) { return (j[0] || []).map(function (x) { return x[0]; }).join(''); })
        .catch(function () { return null; });
    }));
  }

  function doTranslateLLM(backend, texts) {
    var prompt = 'You are a translation engine. Translate the following JSON array of English text ' +
      'fragments into Simplified Chinese. Return ONLY a valid JSON array of the same length with the ' +
      'translations, in the same order. RULES: do NOT translate code, API paths (e.g. /api/v1/...), ' +
      'file names, or model/brand proper nouns; preserve line breaks and formatting.';
    return getFirstModel(backend).then(function (model) {
      var url = backend === 'lmstudio' ? 'http://localhost:1234/v1/chat/completions' : 'http://localhost:11434/api/chat';
      var body;
      if (backend === 'lmstudio') {
        body = { model: model, messages: [{ role: 'system', content: prompt }, { role: 'user', content: JSON.stringify(texts) }], temperature: 0 };
      } else {
        body = { model: model, stream: false, messages: [{ role: 'system', content: prompt }, { role: 'user', content: JSON.stringify(texts) }] };
      }
      return fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(body) })
        .then(function (r) { return r.json(); })
        .then(function (j) {
          var content = backend === 'lmstudio' ? (j.choices && j.choices[0].message.content) : (j.message && j.message.content);
          if (!content) return null;
          var arr = extractJsonArray(content);
          return arr && arr.length === texts.length ? arr : null;
        });
    }).catch(function () { return null; });
  }

  function translateBatch(texts) {
    // 1) 字典优先
    var fromDict = tryFromDict(texts);
    if (fromDict) return Promise.resolve(fromDict);
    // 2) 在线后端
    if (BACKEND === 'google') return doTranslateGoogle(texts);
    if (BACKEND === 'lmstudio' || BACKEND === 'ollama') return doTranslateLLM(BACKEND, texts);
    return detectBackend().then(function (b) {
      return b === 'google' ? doTranslateGoogle(texts) : doTranslateLLM(b, texts);
    });
  }

  // ---------------- 应用 ----------------
  function applyOne(node, zh) {
    if (!zh || zh === node.nodeValue) return;
    node.__zhOriginal = node.nodeValue;
    node.nodeValue = zh;
    var p = node.parentNode;
    if (p && p.setAttribute) {
      p.setAttribute('data-zh-translated', '1');
      try { p.setAttribute('data-zh-original', node.__zhOriginal); p.title = node.__zhOriginal; } catch (e) {}
    }
    translatedNodes.push(node);
  }

  // ---------------- 主流程 ----------------
  function run() {
    var manual = !!run._manual;
    if (!manual) { if (!AUTO) return; }
    if (pending) return;
    pending = true;
    setTimeout(function () {
      try {
        var nodes = collect(manual);
        pending = false;
        run._manual = false;
        if (!nodes.length) return;
        var batch = nodes.slice(0, 12);
        var texts = batch.map(function (n) { return n.nodeValue; });
        var need = [], needIdx = [];
        texts.forEach(function (t, i) { if (!cache.has(t)) { need.push(t); needIdx.push(i); } });
        var resolved = function (res) {
          if (res) needIdx.forEach(function (i, k) { if (res[k]) cache.set(texts[i], res[k]); });
          batch.forEach(function (n, i) {
            var zh = cache.get(texts[i]) || (res && res[i]);
            if (zh) applyOne(n, zh);
          });
        };
        if (need.length) {
          translateBatch(need).then(resolved).catch(function () { resolved(null); });
        } else {
          resolved(null);
        }
      } catch (e) {
        pending = false;
        run._manual = false;
      }
    }, 400);
  }
  run._manual = false;

  function manualRun() { run._manual = true; run(); }

  // ---------------- UI: 按钮 (可拖动) ----------------
  function loadPos() {
    try {
      var s = localStorage.getItem('lmszh_tr_fab_pos');
      if (s) return JSON.parse(s);
    } catch (e) {}
    return null;
  }
  function savePos(x, y) {
    try { localStorage.setItem('lmszh_tr_fab_pos', JSON.stringify({x:x, y:y})); } catch (e) {}
  }

  // ---- FAB 不透明度 (右键菜单可调, 20% 一档) ----
  var gFab = null, gHover = false, gBaseOpacity = 1;
  function loadOpacity() {
    try { var v = parseFloat(localStorage.getItem('lmszh_tr_fab_opacity'));
          if (v >= 0.2 && v <= 1) return v; } catch (e) {}
    return 1;
  }
  function saveOpacity(v) { try { localStorage.setItem('lmszh_tr_fab_opacity', String(v)); } catch (e) {} }
  function applyOpacity() {
    if (!gFab) return;
    // 悬停 = 基准透明度; 移开 = 半透明 (至少 0.15 保证可见)
    var eff = gHover ? gBaseOpacity : Math.max(0.15, gBaseOpacity * 0.5);
    gFab.style.opacity = eff;
  }

  function makeButton() {
    if (document.getElementById('__zh_tr_btn')) return;
    var b = document.createElement('div');
    b.id = '__zh_tr_btn';
    b.textContent = '译';
    b.title = '翻译当前页面英文 · 单击翻译 · 双击还原 · 右键菜单 · 拖动移动';

    var pos = loadPos();
    var initX = pos && typeof pos.x === 'number' ? pos.x : (window.innerWidth - 58);
    var initY = pos && typeof pos.y === 'number' ? pos.y : (window.innerHeight - 58);
    // 边界裁剪
    initX = Math.max(8, Math.min(window.innerWidth - 50, initX));
    initY = Math.max(8, Math.min(window.innerHeight - 50, initY));

    b.style.cssText = 'position:fixed;left:' + initX + 'px;top:' + initY + 'px;' +
      'z-index:2147483646;width:42px;height:42px;' +
      'border-radius:50%;background:#2b6cff;color:#fff;display:flex;align-items:center;justify-content:center;' +
      'cursor:pointer;font:15px/1 -apple-system,"Microsoft YaHei",sans-serif;' +
      'box-shadow:0 4px 14px rgba(0,0,0,.45);user-select:none;-webkit-user-select:none;' +
      'touch-action:none;';

    // ---- 拖动 vs 点击 区分 ----
    var startX = 0, startY = 0, moved = false, dragging = false;
    var DRAG_THRESHOLD = 5;
    function clampX(x){ return Math.max(0, Math.min(window.innerWidth - 42, x)); }
    function clampY(y){ return Math.max(0, Math.min(window.innerHeight - 42, y)); }

    // 鼠标移入: 完全不透明; 移出: 半透明
    b.addEventListener('mouseenter', function () { gHover = true; applyOpacity(); });
    b.addEventListener('mouseleave', function () { gHover = false; applyOpacity(); });

    // 右键弹出菜单 (桌面端)
    b.addEventListener('contextmenu', function (e) {
      e.preventDefault();
      if (dragging) return;
      showMenu();
    });

    b.addEventListener('mousedown', function (e) {
      if (e.button !== 0) return;          // 仅左键拖动, 右键交给 contextmenu
      e.preventDefault();
      startX = e.clientX; startY = e.clientY;
      moved = false; dragging = false;
    });

    document.addEventListener('mousemove', function (e) {
      if (e.buttons !== 1) return;
      var dx = e.clientX - startX, dy = e.clientY - startY;
      if (!moved && Math.abs(dx) + Math.abs(dy) > DRAG_THRESHOLD) {
        moved = true; dragging = true;
        b.style.cursor = 'grabbing';       // 拖动时才显示抓手
      }
      if (dragging) {
        b.style.left = clampX(e.clientX - 21) + 'px';
        b.style.top  = clampY(e.clientY - 21) + 'px';
      }
    });

    document.addEventListener('mouseup', function () {
      if (!dragging) return;
      b.style.cursor = 'pointer';
      var r = b.getBoundingClientRect();
      // 拖到左半屏 或 顶部区域 → 松手自动归位到右侧
      if ((r.left + r.width / 2) < window.innerWidth / 2 || r.top < 80) {
        b.style.left = (window.innerWidth - 58) + 'px';
        b.style.top  = (window.innerHeight - 58) + 'px';
      }
      var rr = b.getBoundingClientRect();
      savePos(rr.left, rr.top);
      dragging = false;
    });

    b.addEventListener('click', function (e) {
      // 拖动后不触发
      if (moved || dragging) { e.stopPropagation(); return; }
      manualRun();
    });
    b.addEventListener('dblclick', function (e) {
      e.preventDefault();
      window.__ZH_TRANSLATE__.restoreAll();
    });

    // 触屏: 单击翻译 / 双击还原 / 长按菜单 / 拖动移动
    var lastTap = 0, touchTimer = null;
    b.addEventListener('touchstart', function (e) {
      var t = e.touches[0]; startX = t.clientX; startY = t.clientY;
      moved = false; dragging = false;
      touchTimer = setTimeout(function () { if (!moved) showMenu(); }, 600);
    }, {passive:true});
    b.addEventListener('touchmove', function (e) {
      var t = e.touches[0];
      var dx = t.clientX - startX, dy = t.clientY - startY;
      if (!moved && Math.abs(dx) + Math.abs(dy) > DRAG_THRESHOLD) {
        moved = true; dragging = true;
        if (touchTimer) { clearTimeout(touchTimer); touchTimer = null; }
      }
      if (dragging) {
        b.style.left = clampX(t.clientX - 21) + 'px';
        b.style.top  = clampY(t.clientY - 21) + 'px';
        e.preventDefault();
      }
    }, {passive:false});
    b.addEventListener('touchend', function () {
      if (touchTimer) { clearTimeout(touchTimer); touchTimer = null; }
      if (dragging) {
        var r = b.getBoundingClientRect();
        if ((r.left + r.width / 2) < window.innerWidth / 2 || r.top < 80) {
          b.style.left = (window.innerWidth - 58) + 'px';
          b.style.top  = (window.innerHeight - 58) + 'px';
        }
        var rr = b.getBoundingClientRect();
        savePos(rr.left, rr.top);
        dragging = false;
      } else {
        var now = Date.now();
        if (now - lastTap < 300) {
          window.__ZH_TRANSLATE__.restoreAll();
          lastTap = 0;
        } else {
          lastTap = now;
          setTimeout(function () { if (lastTap === now) manualRun(); }, 250);
        }
      }
    });

    gFab = b; gBaseOpacity = loadOpacity(); gHover = false; applyOpacity();
    document.body.appendChild(b);
  }

  // ---- 右键/长按弹出的菜单 ----
  function showMenu() {
    var old = document.getElementById('__zh_tr_menu');
    if (old) old.remove();
    var m = document.createElement('div');
    m.id = '__zh_tr_menu';
    var btn = document.getElementById('__zh_tr_btn');
    var r = btn.getBoundingClientRect();
    var left = r.left, top = r.top - 4;
    m.style.cssText = 'position:fixed;left:' + left + 'px;top:' + (top - 110) + 'px;z-index:2147483647;' +
      'background:#1f232a;color:#e6e8eb;border-radius:8px;padding:6px 0;font:13px/1.4 ' +
      '-apple-system,"Microsoft YaHei",sans-serif;min-width:140px;' +
      'box-shadow:0 6px 20px rgba(0,0,0,.5);';
    var items = [
      {label:'翻译当前页',  act:function(){ manualRun(); }},
      {label:'还原全部',    act:function(){ window.__ZH_TRANSLATE__.restoreAll(); }},
      {label:'自动模式: ' + (AUTO?'开':'关'), act:function(){
          if (AUTO) window.__ZH_TRANSLATE__.disable();
          else window.__ZH_TRANSLATE__.enableAuto();
          window.__ZH_TRANSLATE__.status();
      }},
      {label:'后端: ' + (BACKEND === 'auto' ? '自动' : BACKEND), act:function(){
          var order = ['auto','lmstudio','ollama','google'];
          var i = order.indexOf(BACKEND);
          var next = order[(i + 1) % order.length];
          window.__ZH_TRANSLATE__.setBackend(next);
          alert('翻译后端切换为: ' + next);
      }},
      {label:'重置按钮位置', act:function(){
          try { localStorage.removeItem('lmszh_tr_fab_pos'); } catch(e){}
          var b = document.getElementById('__zh_tr_btn');
          if (b) { b.style.left = (window.innerWidth - 58) + 'px'; b.style.top = (window.innerHeight - 58) + 'px'; }
      }},
    ];
    items.forEach(function (it) {
      var row = document.createElement('div');
      row.textContent = it.label;
      row.style.cssText = 'padding:6px 14px;cursor:pointer;';
      row.onmouseenter = function () { row.style.background = '#2b6cff33'; };
      row.onmouseleave = function () { row.style.background = ''; };
      row.onclick = function (e) { e.stopPropagation(); it.act(); m.remove(); };
      m.appendChild(row);
    });

    // 不透明度分隔线 + 选项 (20% 一档)
    var sep = document.createElement('div');
    sep.style.cssText = 'height:1px;background:rgba(255,255,255,.12);margin:4px 0;';
    m.appendChild(sep);
    [1.0, 0.8, 0.6, 0.4, 0.2].forEach(function (ov) {
      var pct = Math.round(ov * 100);
      var cur = Math.abs(gBaseOpacity - ov) < 0.001;
      var row = document.createElement('div');
      row.textContent = '不透明度 ' + pct + '%' + (cur ? '  ✓' : '');
      row.style.cssText = 'padding:6px 14px;cursor:pointer;' + (cur ? 'color:#7fd1ff;' : '');
      row.onmouseenter = function () { row.style.background = '#2b6cff33'; };
      row.onmouseleave = function () { row.style.background = ''; };
      row.onclick = function (e) { e.stopPropagation(); gBaseOpacity = ov; saveOpacity(ov); applyOpacity(); m.remove(); };
      m.appendChild(row);
    });

    document.body.appendChild(m);
    // 点击其它处关闭
    setTimeout(function () {
      var closeFn = function () { m.remove(); document.removeEventListener('click', closeFn, true); };
      document.addEventListener('click', closeFn, true);
    }, 50);
  }

  // ---------------- 全局 API ----------------
  window.__ZH_TRANSLATE__ = {
    version: 'v1.3-translate',
    setBackend: function (b) { BACKEND = b; detected = null; },
    backend: function () { return BACKEND === 'auto' ? (detected || 'auto') : BACKEND; },
    enable: function () { AUTO = true; try { localStorage.removeItem('lmszh_translate'); } catch (e) {} manualRun(); },
    disable: function () { AUTO = false; try { localStorage.setItem('lmszh_translate', 'off'); } catch (e) {} },
    enableAuto: function () { AUTO = true; try { localStorage.setItem('lmszh_translate', 'auto'); } catch (e) {} },
    translateVisible: function () { manualRun(); },
    restoreAll: function () {
      translatedNodes.forEach(function (n) {
        if (n.__zhOriginal != null) n.nodeValue = n.__zhOriginal;
        var p = n.parentNode;
        if (p && p.removeAttribute) { p.removeAttribute('data-zh-translated'); p.removeAttribute('data-zh-original'); p.title = ''; }
        n.__zhMarked = false;
      });
      translatedNodes = [];
      var w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT), x;
      while ((x = w.nextNode())) x.__zhMarked = false;
      return 'restored ' + translatedNodes.length + ' nodes';
    },
    clearCache: function () { cache.clear(); return 'cache cleared'; },
    status: function () { return { auto: AUTO, backend: this.backend(), translated: translatedNodes.length, cacheSize: cache.size }; },
    // 调试: 把已翻译节点全部标红
    markTranslated: function () {
      var n = 0;
      translatedNodes.forEach(function (x) {
        var p = x.parentNode;
        if (p && p.style) { p.style.outline = '2px solid #ff5050'; n++; }
      });
      return 'marked ' + n;
    }
  };

  // ---------------- 启动(仅在未 OFF 时) ----------------
  if (!OFF) {
    if (document.body) makeButton();
    function startObs() {
      makeButton();
      // 主监听: 子节点变化触发自动翻译
      var mo = new MutationObserver(function () { if (AUTO) run(); });
      mo.observe(document.body, { childList: true, subtree: true, characterData: true });
      // 副监听: attribute 变化(placeholder/title/aria-label 等 React 强制重设时)
      // → 在下个 microtask 重跑一次, 确保我们的中文不被 React 覆盖回去
      var moAttr = new MutationObserver(function (muts) {
        if (!AUTO) return;
        // 仅关心 ATTRS 类 (placeholder/title/aria-label/alt), 其它忽略
        for (var i = 0; i < muts.length; i++) {
          var m = muts[i];
          var an = m.attributeName || '';
          if (an === 'placeholder' || an === 'title' || an === 'aria-label' || an === 'alt') {
            scheduleAttrRetry();
            return;
          }
        }
      });
      try {
        moAttr.observe(document.body, {
          attributes: true, subtree: true,
          attributeFilter: ['placeholder', 'title', 'aria-label', 'alt']
        });
      } catch (e) { /* 旧浏览器不支持 attributeFilter, 退化到全部 */ }
    }
    var _attrRetryTimer = null;
    function scheduleAttrRetry() {
      if (_attrRetryTimer) return;
      _attrRetryTimer = (window.requestAnimationFrame || setTimeout)(function () {
        _attrRetryTimer = null;
        manualRun();     // 直接调 manualRun(), 走放宽阈值路径
      }, 16);                  // 一帧后重试
    }
    if (document.body) startObs();
    else document.addEventListener('DOMContentLoaded', startObs);
    setTimeout(function () { if (AUTO) manualRun(); }, 2000);
    setInterval(function () { if (AUTO) manualRun(); }, 6000);
    // ---- 按钮自我保护(每 3 秒检查, 丢失则重建) ----
    setInterval(function () {
      if (!document.getElementById('__zh_tr_btn')) {
        try { makeButton(); console.info('[lms-zh-translate] FAB 丢失, 已自动重建'); }
        catch (e) { console.warn('[lms-zh-translate] FAB 重建失败:', e); }
      }
    }, 3000);
    document.addEventListener('keydown', function (e) {
      if (e.ctrlKey && e.shiftKey && (e.key === 'T' || e.key === 't')) { e.preventDefault(); manualRun(); }
    });
    console.info('[lms-zh-translate] v1.5 loaded, auto=', AUTO);
  } else {
    console.info('[lms-zh-translate] disabled by localStorage (lmszh_translate=off)');
  }
})();