/*!
 * LM Studio 简体中文汉化 · 运行时观察者层 v2.0.0
 *
 * 机制（适配 LM Studio 0.4.28）：
 * - 整段 textNode 精确匹配（raw + trim 双查）
 * - 元素属性 placeholder / title / aria-label / alt 整段匹配
 * - 递归穿透 ShadowRoot（react-contexify 等把菜单挂在 attachShadow 内）
 * - 不动 inline 子元素结构，避免破坏 React reconciler 的 DOM 引用
 * - 跳过 script/style/code/pre/kbd/samp/var/textarea/contenteditable；原文已含中文则跳过
 * - 受控 input：仅未聚焦且整段命中字典时改 value；排除 password/email/number/hidden
 * - TEMPLATE_RULES：模板字符串前缀正则匹配，保留变量（$1/$2）
 * - 1–3 字中文短词命中时，给父元素精准 inline nowrap（可被 __ZH_NO_NOWRAP__ 关停）
 * - MutationObserver 增量监听 + 每 1 秒全 body 兜底扫描（含 ShadowRoot）
 * - 诊断：__zhPatchCount / __zhNowrapCount / __zhDebug() / __zhNoWrapMisses
 *
 * 边界（用户决策）：
 * - 原生 renderer 右键菜单（Electron 侧 n()/o() 通道）不在本层处理，保持原样
 * - 用户数据默认名（如 Empty Folder）不翻译
 * - Monaco 命令码表、第三方库内部报错、协议路径/语言码/外部产品名保持英文
 */
(function () {
  'use strict';
  if (window.__zhPatchLoaded) { return; }
  window.__zhPatchLoaded = true;

  var dict = window.__ZH_DICT__ || {};
  var dictKeys = Object.keys(dict);
  if (!dictKeys.length) { console.warn('[lms-zh] dict empty, abort'); return; }
  console.info('[lms-zh] patch v2.0.0 loaded, dict size:', dictKeys.length);

  var CJK = /[一-鿿㐀-䶿豈-﫿]/;
  function hasCJK(s) { return CJK.test(s); }
  function isPlainEnglish(s) {
    if (!s || hasCJK(s)) { return false; }
    return /[A-Za-z]/.test(s);
  }

  // 模板字符串前缀规则：变量部分每次不同，字典整段匹配失败，用正则保留捕获组。
  // 格式: [正则, 替换模板]（$1/$2 引用捕获组）
  var TEMPLATE_RULES = [
    [/^Delete (\d+) folder\(s\) and (\d+) chat\(s\)$/, '删除 $1 个文件夹和 $2 个对话'],
    [/^Delete (\d+) folder\(s\)$/, '删除 $1 个文件夹'],
    [/^Delete (\d+) chat\(s\)$/, '删除 $1 个对话'],
    [/^More from (.+)$/, '来自 $1'],
    [/^Delete folder "(.+)"$/, '删除文件夹 "$1"'],
    [/^Open Staff Pick page for (.+)$/, '打开 $1 的官方推荐页面'],
    [/^Accepted (\d+)\/(\d+) draft tokens \((\d+)%\)$/, '已接受 $1/$2 草稿词元（$3%）'],
    [/^Accepted (\d+)\/(\d+) draft tokens$/, '已接受 $1/$2 草稿词元'],
    [/^(\d+)% draft tokens accepted$/, '$1% 草稿词元被接受'],
    [/^Draft model: (.+)$/, '草稿模型：$1'],
    [/^Stop reason: Context Length Limit Reached$/, '停止原因：已达到上下文长度上限'],
    [/^Stop reason: EOS Token Found$/, '停止原因：遇到 EOS 词元'],
    [/^Stop reason: Generation Failed$/, '停止原因：生成失败'],
    [/^Stop reason: Max Predicted Tokens Reached$/, '停止原因：已达到最大预测词元数'],
    [/^Stop reason: Model Unloaded$/, '停止原因：模型已卸载'],
    [/^Stop reason: Stop String Found$/, '停止原因：遇到停止字符串'],
    [/^Stop reason: Tool Calls$/, '停止原因：工具调用'],
    [/^Stop reason: User Stopped$/, '停止原因：用户已停止'],
    [/^Stop reason: (.+)$/, '停止原因：$1'],
    [/^Updated to (.+)$/, '已更新至 $1'],
    [/^Downloading (.+)\.\.\.$/, '正在下载 $1...'],
    [/^Preset from the Hub by (.+)$/, '来自 Hub 的预设，作者：$1'],
    [/^(\d+) plugins$/, '$1 个插件'],
    [/^(\d+) tokens$/, '$1 词元'],
    [/^(\d+(?:\.\d+)?) tok\/sec$/, '$1 词元/秒'],
    [/^(\d+(?:\.\d+)?)s to first token$/, '距首个词元 $1 秒'],
    [/^You have (\d+) local models?, taking up (.+) of disk space$/, '你有 $1 个本地模型，占用 $2 磁盘空间'],
    [/^(\d+) results? found$/, '找到 $1 个结果'],
    [/^Newly loaded (.+) models will use the updated runtime\.$/, '新加载的 $1 模型将使用更新后的运行时。'],
    [/^Your preset will be created as (.+)$/, '你的预设将创建为 $1'],
    [/^You are all up to date! The current version is (.+)$/, '你已是最新版本！当前版本为 $1'],
    [/^Incorrect placement of the virtual model\. Expected to be at (.+)\. Found at (.+)\.$/, '虚拟模型位置不正确。应位于 $1，实际位于 $2。'],
    // 聊天列表相对时间（模板字符串生成，字典无法整段命中）
    [/^Less than 1 minute ago$/, '不到 1 分钟前'],
    [/^1 min ago$/, '1 分钟前'],
    [/^(\d+) mins ago$/, '$1 分钟前'],
    [/^1 hour ago$/, '1 小时前'],
    [/^(\d+) hours ago$/, '$1 小时前'],
    [/^1 day ago$/, '1 天前'],
    [/^(\d+) days ago$/, '$1 天前'],
    // 上下文用量浮层（模板带变量）
    [/^(\d+(?:\.\d+)?)% used \((\d+(?:\.\d+)?)% left\)$/, '$1% 已用（剩余 $2%）'],
    [/^Conversation token usage is unavailable\. Loaded context: (.+) tokens\.$/, '对话令牌用量不可用。已加载上下文：$1 个令牌。'],
    [/^Delete (.+)$/, '删除 $1'] // 通用 Delete 前缀放最后（具体规则优先）
  ];

  function tryTemplate(v) {
    if (!v) return null;
    for (var i = 0; i < TEMPLATE_RULES.length; i++) {
      var re = TEMPLATE_RULES[i][0], tpl = TEMPLATE_RULES[i][1];
      var m = re.exec(v);
      if (m) {
        return tpl.replace(/\$(\d)/g, function (_, n) { return m[+n] == null ? '' : m[+n]; });
      }
    }
    return null;
  }

  function inSkippedContext(el) {
    if (!el || !el.closest) { return false; }
    return !!el.closest('script,style,code,pre,kbd,samp,var,textarea,[contenteditable="true"],[contenteditable=""]');
  }

  var ATTRS = ['placeholder', 'title', 'aria-label', 'alt'];

  function translateElement(el) {
    if (!el || !el.getAttribute) return;
    for (var i = 0; i < ATTRS.length; i++) {
      var a = ATTRS[i];
      if (!el.hasAttribute(a)) continue;
      var v = el.getAttribute(a);
      if (!v) continue;
      var r = dict[v] || dict[v.trim()];
      if (!r) {
        if (!isPlainEnglish(v)) continue;
        r = tryTemplate(v.trim());
      }
      if (r && r !== v) {
        try { el.setAttribute(a, r); window.__zhPatchCount = (window.__zhPatchCount || 0) + 1; } catch (e) {}
      }
    }
    // React 受控 input 的 value 是 DOM property，textNode/属性补丁抓不到。
    // 仅整段精确命中字典且元素未聚焦时替换，避免打断用户输入；最坏 = 没翻译。
    if (el.nodeName === 'INPUT') {
      var ty = (el.type || 'text').toLowerCase();
      if (ty !== 'password' && ty !== 'email' && ty !== 'number' && ty !== 'hidden') {
        var iv = el.value;
        if (iv && iv === iv.trim() && isPlainEnglish(iv)) {
          var ir = dict[iv];
          if (ir && ir !== iv && document.activeElement !== el) {
            try { el.value = ir; window.__zhPatchCount = (window.__zhPatchCount || 0) + 1; } catch (e) {}
          }
        }
      }
    }
  }

  // 诊断：卡在 nowrap 条件但已翻译的样本，控制台 __zhDebug() 查看
  window.__zhNoWrapMisses = window.__zhNoWrapMisses || [];
  function _miss(reason, txt, p) {
    if (window.__zhNoWrapMisses.length < 30) {
      window.__zhNoWrapMisses.push({
        reason: reason,
        text: txt,
        tag: p && p.tagName,
        kids: p ? p.childNodes.length : 0,
        ctx: p ? (p.parentElement ? (p.parentElement.className || '').toString().slice(0, 60) : '') : ''
      });
    }
  }

  // 精准 inline nowrap：修 "集成"/"搜索" 等 1–3 字中文在窄容器竖排。
  // 副作用范围 = 该父元素，不靠 class 猜容器，不会扩散。
  // 紧急关停：控制台 `window.__ZH_NO_NOWRAP__ = true` 后刷新页面。
  function markCnShortNoWrap(node, newText) {
    if (window.__ZH_NO_NOWRAP__) return;
    if (!node || !node.parentElement) return;
    if (!/^[一-鿿＀-￯]{1,3}$/.test(newText)) return;
    var p = node.parentElement;

    var kids = p.childNodes;
    var hasTextElementKid = false;
    for (var i = 0; i < kids.length; i++) {
      if (kids[i].nodeType === 1) {
        if ((kids[i].textContent || '').trim()) { hasTextElementKid = true; break; }
      }
    }
    if (hasTextElementKid) { _miss('has-text-element-kid', newText, p); return; }

    var joined = '';
    for (var j = 0; j < kids.length; j++) {
      if (kids[j].nodeType === 3) joined += kids[j].nodeValue;
    }
    if (joined.trim() !== newText) { _miss('joined-mismatch', newText + ' vs joined=' + joined.slice(0, 20), p); return; }

    p.style.whiteSpace = 'nowrap';
    window.__zhNowrapCount = (window.__zhNowrapCount || 0) + 1;
  }

  function translateTextNode(node) {
    if (!node) return;
    var v = node.nodeValue;
    if (!v) return;
    // 字典整句精确匹配优先；模板变量规则只兜底字典未命中的串。
    var r = dict[v] || dict[v.trim()];
    if (!r) {
      if (!isPlainEnglish(v)) return;
      r = tryTemplate(v.trim());
    }
    if (r && r !== v) {
      try {
        node.nodeValue = r;
        window.__zhPatchCount = (window.__zhPatchCount || 0) + 1;
        markCnShortNoWrap(node, r);
      } catch (e) {}
    }
  }

  function processNode(root) {
    if (!root) return;
    if (root.nodeType === 3) { translateTextNode(root); return; }
    if (root.nodeType !== 1) return;
    if (/^(SCRIPT|STYLE)$/.test(root.nodeName)) return;
    translateElement(root);
    var ew = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT, {
      acceptNode: function (n) {
        if (/^(SCRIPT|STYLE)$/.test(n.nodeName)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    while (ew.nextNode()) translateElement(ew.currentNode);
    var tw = document.createTreeWalker(root, NodeFilter.SHOW_TEXT, {
      acceptNode: function (n) {
        var p = n.parentNode;
        if (!p) return NodeFilter.FILTER_REJECT;
        if (/^(SCRIPT|STYLE|TEXTAREA)$/.test(p.nodeName)) return NodeFilter.FILTER_REJECT;
        if (p.isContentEditable) return NodeFilter.FILTER_REJECT;
        if (inSkippedContext(p)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    while (tw.nextNode()) translateTextNode(tw.currentNode);
  }

  // 递归穿透 ShadowRoot：TreeWalker 不跨 ShadowRoot 边界，需手动遍历。
  function collectRoots(root, list) {
    if (!root) return list;
    if (root.nodeType === 1 || root.nodeType === 9 || root.nodeType === 11) {
      list.push(root);
      if (root.shadowRoot) {
        list.push(root.shadowRoot);
        collectRoots(root.shadowRoot, list);
      }
      var children = root.children || root.childNodes;
      if (children) {
        for (var i = 0; i < children.length; i++) collectRoots(children[i], list);
      }
    }
    return list;
  }

  function processAllRoots() {
    if (!document.body) return;
    var roots = [];
    collectRoots(document.documentElement, roots);
    for (var i = 0; i < roots.length; i++) processNode(roots[i]);
  }

  // 增量 MutationObserver 调度
  var queue = [];
  var scheduled = false;
  function flush() {
    scheduled = false;
    var batch = queue; queue = [];
    for (var i = 0; i < batch.length; i++) {
      var node = batch[i];
      if (node && node.parentNode) processNode(node);
    }
  }
  function schedule(node) {
    if (!node) return;
    queue.push(node);
    if (!scheduled) {
      scheduled = true;
      if (typeof requestAnimationFrame === 'function') requestAnimationFrame(flush);
      else setTimeout(flush, 0);
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { processAllRoots(); });
  } else {
    processAllRoots();
  }

  setInterval(processAllRoots, 1000);

  var mo = new MutationObserver(function (muts) {
    for (var i = 0; i < muts.length; i++) {
      var m = muts[i];
      if (m.type === 'characterData') {
        if (m.target && m.target.nodeType === 3) schedule(m.target.parentNode);
      } else if (m.type === 'childList') {
        for (var j = 0; j < m.addedNodes.length; j++) {
          var n = m.addedNodes[j];
          if (n.nodeType === 3) { var p = n.parentNode; if (p) schedule(p); }
          else if (n.nodeType === 1) schedule(n);
        }
      } else if (m.type === 'attributes') {
        if (m.target && m.target.nodeType === 1) translateElement(m.target);
      }
    }
  });

  function observe(root) {
    if (!root || root.__zhObserved) return;
    root.__zhObserved = true;
    mo.observe(root, {
      childList: true, subtree: true,
      characterData: true,
      attributes: true, attributeFilter: ATTRS
    });
  }

  function observeAll() {
    if (!document.documentElement) return;
    observe(document.documentElement);
    var roots = [];
    collectRoots(document.documentElement, roots);
    for (var i = 0; i < roots.length; i++) observe(roots[i]);
  }

  if (document.documentElement) observeAll();
  else document.addEventListener('DOMContentLoaded', observeAll);

  // 监听新出现的 ShadowRoot（react-contexify 创建菜单时动态 attachShadow）
  var newShadowObserver = new MutationObserver(function (muts) {
    for (var i = 0; i < muts.length; i++) {
      var m = muts[i];
      for (var j = 0; j < m.addedNodes.length; j++) {
        var n = m.addedNodes[j];
        if (n && n.nodeType === 1 && n.shadowRoot) {
          observe(n.shadowRoot);
          processNode(n.shadowRoot);
        }
      }
    }
  });
  if (document.documentElement) {
    newShadowObserver.observe(document.documentElement, { childList: true, subtree: true });
  }

  // 诊断接口
  window.__zhDebug = function () {
    var info = {
      version: 'v2.0.0',
      dictSize: dictKeys.length,
      patchCount: window.__zhPatchCount || 0,
      nowrapCount: window.__zhNowrapCount || 0,
      nowrapKilled: !!window.__ZH_NO_NOWRAP__,
      shadowRoots: [],
      shadowTexts: [],
      missedSamples: [],
      nowrapMisses: (window.__zhNoWrapMisses || []).slice(0, 30)
    };
    var roots = [];
    collectRoots(document.documentElement, roots);
    info.shadowRoots = roots.filter(function (r) { return r.nodeType === 11; }).length;
    for (var i = 0; i < roots.length; i++) {
      var r = roots[i];
      if (r.nodeType !== 11) continue;
      var tw = document.createTreeWalker(r, NodeFilter.SHOW_TEXT, null);
      while (tw.nextNode()) {
        var v = tw.currentNode.nodeValue;
        if (v && v.length > 1 && v.length < 100 && /^[A-Z][a-zA-Z\s.’‘…]+$/.test(v)) {
          info.shadowTexts.push(v);
          if (info.shadowTexts.length >= 30) break;
        }
      }
    }
    return info;
  };
})();
