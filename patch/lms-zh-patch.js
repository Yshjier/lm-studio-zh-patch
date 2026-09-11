/*!
 * LM Studio 中文汉化补丁层 v1.10
 * - 整段 textNode 精确匹配(同时支持 raw 和 trim)
 * - 元素属性(placeholder/title/aria-label/alt)整段匹配
 * - **递归穿透 ShadowRoot**(react-contexify ContextMenu 默认 useShadowDOM=true)
 * - 不动 inline 子元素结构(避免破坏 React reconciler DOM 引用)
 * - 跳过 代码块 / 输入区 / 可编辑区;原文已含中文则跳过
 * - MutationObserver 增量监听 + 每 1 秒全 body 兜底扫描
 * - 通过 window.__zhPatchCount 暴露命中计数,window.__zhDictMiss 暴露未命中样本
 * - 通过 window.__zhDebug() 输出诊断信息
 *
 * v1.10 升级 (第 72 轮): 精准 inline nowrap 修 "集成" 等 1-3 字中文竖排
 *   - 第 54 轮 / v1.8 两次拒全局 CSS 防换行 (副作用不可控, 铁律)
 *   - 第 72 轮用户改口 "接受改样式了", 改用**精准 inline 方式**:
 *     仅当 textNode 翻译结果为 1-3 字中文 且 textNode 是父元素唯一子节点
 *     且父元素不是 flex/grid 布局时, 给父元素加 inline
 *     `style="white-space:nowrap"`, 不靠 class 猜容器
 *   - 副作用范围 = 命中的那个父元素, 不会扩散; 已有 nowrap 的无影响
 *   - 紧急关停: 浏览器控制台 `window.__ZH_NO_NOWRAP__ = true` 后刷新页面
 *   - 诊断: `window.__zhNowrapCount` 计数; `__zhDebug()` 看 wrap 命中数
 *
 * v1.6 升级: [已于第 54 轮按用户要求移除]
 *   - 曾移植翻译模块的全局 CSS 防换行 (white-space:nowrap), 用于修 "集成" 竖排
 *   - **已移除**: 全局 CSS 会无差别影响所有匹配容器, 副作用不可控
 *     → 第 72 轮改用精准 inline 方式重新引入, 副作用收敛到单元素
 *     → 仍遵守铁律: 最坏必须是「没修好」, 绝不能是「样式大改让用户不认」
 *
 * v1.7 升级: (保留)
 *   - TEMPLATE_RULES: 模板字符串前缀匹配 (变量保留)
 *     处理 JSX 模板字符串 `` `More from ${author}` `` 渲染出的单一 textNode —— 变量部分
 *     每次不同(作者名), 字典无法整段命中, 用正则前缀匹配 + $1 保留变量
 *
 * v1.8 升级: (当前版本)
 *   - TEMPLATE_RULES 新增 Delete 系列 (删聊天/文件夹确认框标题 `Delete ${name}` 等)
 *
 * v1.9 升级:
 *   - TEMPLATE_RULES 新增 i18n 插值串系列 ({{var}} 渲染后变成具体值, 字典无法整段命中):
 *     草稿模型/停止原因/已更新至/正在下载/词元数/tok per sec/首个词元耗时/
 *     本地模型占用磁盘/结果数/预设将创建为/已是最新版本 等 18 条
 *   - 配套字典补齐 214 条 (analysis/extract_en_i18n.py 全量 i18n 块提取, 见 add_dict_r59.py)
 *   - 新增 INPUT 受控值兜底: React 受控 input 的 value 是 DOM property,
 *     textNode/属性补丁都抓不到 (如新建文件夹默认名 "Empty Folder")。
 *     仅当 value 整段精确命中字典【且元素未聚焦】时替换 → 最坏=没翻译
 *
 * v1.9.1 调整:
 *   - 从字典移除 "Empty Folder" → "空文件夹" 的映射。
 *     新建文件夹的默认名属于用户数据(磁盘文件名),补丁翻译后会导致
 *     重命名输入框显示中文、但实际保存/删除确认仍用英文 "Empty Folder",
 *     状态不一致。用户决策:默认文件夹名保持英文不翻译。
 *
 * v1.9.2 调整:
 *   - TEMPLATE_RULES 优先于 isPlainEnglish 检查。
 *     模板串(如 `Delete folder "${name}"`) 的变量部分可能是中文用户名/文件名,
 *     整段含 CJK 会被旧逻辑跳过,导致前缀 "Delete folder" 漏翻。
 *     现在先尝试模板匹配,命中即翻译前缀并保留变量,不受 CJK 影响。
 *
 * 已知限制: 4 字及以上中文如 "加载模型" / "插件市场" 在极窄容器仍可能竖排,
 *           词典换更短词可缓解 (e.g. "加载模型" → "加载", "插件市场" → "插件"),
 *           这是词典范畴不是补丁范畴, 留给后续按需补
 */
(function () {
  'use strict';
  if (window.__zhPatchLoaded) { return; }
  window.__zhPatchLoaded = true;

  // ---------------- 全局 CSS 防换行:已于第 54 轮按用户要求移除 ----------------
  // 原 v1.6 为修 "集成" 折行引入 injectZhCss(),但全局 white-space:nowrap 会
  // 无差别影响全站所有匹配容器(潜在副作用:长文本不换行/布局溢出)。
  // 用户决策:宁可保留 "集成" 两行,也不要全局样式副作用 —— 遵守铁律
  // 「最坏结果必须是没翻译/没修好,绝不能是样式大改让用户不认」。

  var dict = window.__ZH_DICT__ || {};
  var dictKeys = Object.keys(dict);
  if (!dictKeys.length) { console.warn('[lms-zh] dict empty, abort'); return; }
  console.info('[lms-zh] patch v1.10 loaded, dict size:', dictKeys.length);

  var CJK = /[\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]/;
  function hasCJK(s) { return CJK.test(s); }
  function isPlainEnglish(s) {
    if (!s || hasCJK(s)) { return false; }
    return /[A-Za-z]/.test(s);
  }

  // ★ v1.7 模板字符串前缀规则 (变量保留)
  // 处理 JSX 模板字符串 `` `More from ${author}` `` 渲染出的单一 textNode:
  // 变量部分(作者名)每次不同, 字典整段匹配失败 → 用正则前缀匹配 + $1 保留变量
  // 格式: [正则, 替换模板]  (替换模板里 $1/$2 引用捕获组)
  var TEMPLATE_RULES = [
    [/^Delete (\d+) folder\(s\) and (\d+) chat\(s\)$/, '删除 $1 个文件夹和 $2 个对话'],
    [/^Delete (\d+) folder\(s\)$/, '删除 $1 个文件夹'],
    [/^Delete (\d+) chat\(s\)$/, '删除 $1 个对话'],
    [/^More from (.+)$/, '来自 $1'],
    [/^Delete folder "(.+)"$/, '删除文件夹 "$1"'],
    [/^Open Staff Pick page for (.+)$/, '打开 $1 的官方推荐页面'],
    // --- v1.9: i18n 模板串 ({{var}} 插值), 见 analysis/out/en_i18n_missing.json ---
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
    [/^Delete (.+)$/, '删除 $1']  // 通用 Delete 前缀放最后(具体规则优先)
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
      // v1.9.2: 模板规则优先于 isPlainEnglish,变量里含中文(CJK)也应翻译前缀
      var r = tryTemplate(v.trim());
      if (!r && !isPlainEnglish(v)) continue;
      if (!r) { r = dict[v] || dict[v.trim()]; }
      if (r && r !== v) {
        try { el.setAttribute(a, r); window.__zhPatchCount = (window.__zhPatchCount||0)+1; } catch(e){}
      }
    }
    // ★ v1.8: React 受控 input 的 value 是 DOM property (新建文件夹默认名 "Empty Folder" 等),
    // textNode/属性补丁都抓不到。仅当【整段精确命中字典】且【元素未聚焦】时替换,
    // 避免打断用户输入。最坏情况 = 没翻译, 无功能副作用。
    if (el.nodeName === 'INPUT') {
      var ty = (el.type || 'text').toLowerCase();
      if (ty !== 'password' && ty !== 'email' && ty !== 'number' && ty !== 'hidden') {
        var iv = el.value;
        if (iv && iv === iv.trim() && isPlainEnglish(iv)) {
          var ir = dict[iv];
          if (ir && ir !== iv && document.activeElement !== el) {
            try { el.value = ir; window.__zhPatchCount = (window.__zhPatchCount||0)+1; } catch(e){}
          }
        }
      }
    }
  }

  // v1.10 精准 inline nowrap 修 "集成" / "搜索" 等 1-3 字中文在窄容器竖排
  // 副作用范围 = 该父元素, 不靠 class 猜容器, 不会扩散
  // 紧急关停: 控制台 `window.__ZH_NO_NOWRAP__ = true` 后刷新页面
  function markCnShortNoWrap(node, newText) {
    if (window.__ZH_NO_NOWRAP__) return;
    if (!node || !node.parentElement) return;
    // 仅 1-3 字中文 (高发竖排词组范围: 集成/搜索/设置/插件/加载中...)
    if (!/^[一-鿿＀-￯]{1,3}$/.test(newText)) return;
    var p = node.parentElement;
    // textNode 必须是父元素唯一子节点, 避免影响兄弟内容
    if (p.childNodes.length !== 1) return;
    // flex/grid 容器自身管理布局, 加 nowrap 可能破坏现有布局 → 跳过
    var d = p.ownerDocument.defaultView.getComputedStyle(p).display;
    if (d === 'flex' || d === 'inline-flex' || d === 'grid' || d === 'inline-grid') return;
    p.style.whiteSpace = 'nowrap';
    window.__zhNowrapCount = (window.__zhNowrapCount || 0) + 1;
  }

  function translateTextNode(node) {
    if (!node) return;
    var v = node.nodeValue;
    if (!v) return;
    // v1.9.2: 模板规则优先,允许变量部分含 CJK(如中文文件夹名)
    var r = tryTemplate(v.trim());
    if (!r && !isPlainEnglish(v)) return;
    if (!r) { r = dict[v] || dict[v.trim()]; }
    if (r && r !== v) {
      try {
        node.nodeValue = r;
        window.__zhPatchCount = (window.__zhPatchCount||0)+1;
        markCnShortNoWrap(node, r);  // v1.10
      } catch(e){}
    }
  }

  function processNode(root) {
    if (!root) return;
    // TEXT 节点
    if (root.nodeType === 3) { translateTextNode(root); return; }
    // ELEMENT 节点
    if (root.nodeType !== 1) return;
    if (/^(SCRIPT|STYLE)$/.test(root.nodeName)) return;
    translateElement(root);
    // 遍历所有后代 ELEMENT 节点,处理它们的属性(placeholder/title/aria-label/alt)
    // 注意:这里**不**套用 inSkippedContext —— textarea/code/pre/contenteditable 内部
    // 的 textNode 不能动(可能是用户输入),但元素自身的属性仍是 UI 文案,应当翻译
    var ew = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT, {
      acceptNode: function (n) {
        if (/^(SCRIPT|STYLE)$/.test(n.nodeName)) return NodeFilter.FILTER_REJECT;
        return NodeFilter.FILTER_ACCEPT;
      }
    });
    while (ew.nextNode()) translateElement(ew.currentNode);
    // 遍历所有后代 textNode
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

  // ★ v1.5 核心:递归穿透 ShadowRoot
  // react-contexify ContextMenu 默认 useShadowDOM=true,把菜单 DOM 渲染到 attachShadow 的 ShadowRoot
  // TreeWalker 不会跨 ShadowRoot 边界,所以必须手动遍历
  function collectRoots(root, list) {
    if (!root) return list;
    if (root.nodeType === 1 || root.nodeType === 9 /* Document */ || root.nodeType === 11 /* DocumentFragment */) {
      list.push(root);
      // 如果是 Element 且有 shadowRoot(open),加入扫描目标
      if (root.shadowRoot) {
        list.push(root.shadowRoot);
        // ShadowRoot 内也可能嵌套 ShadowRoot
        collectRoots(root.shadowRoot, list);
      }
      // 遍历子元素继续找 ShadowRoot
      var children = root.children || root.childNodes;
      if (children) {
        for (var i = 0; i < children.length; i++) {
          collectRoots(children[i], list);
        }
      }
    }
    return list;
  }

  function processAllRoots() {
    if (!document.body) return;
    var roots = [];
    collectRoots(document.documentElement, roots);
    for (var i = 0; i < roots.length; i++) {
      processNode(roots[i]);
    }
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

  // 启动:初次全扫描(含 ShadowRoot)
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', function () { processAllRoots(); });
  } else {
    processAllRoots();
  }

  // 兜底:每 1 秒扫描(含 ShadowRoot)
  setInterval(processAllRoots, 1000);

  // MutationObserver:监听 childList/characterData/attributes,穿透 ShadowRoot
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

  // 初次观察 + 监听新出现的 ShadowRoot
  function observeAll() {
    if (!document.documentElement) return;
    observe(document.documentElement);
    // 也观察 ShadowRoot
    var roots = [];
    collectRoots(document.documentElement, roots);
    for (var i = 0; i < roots.length; i++) {
      observe(roots[i]);
    }
  }

  if (document.documentElement) observeAll();
  else document.addEventListener('DOMContentLoaded', observeAll);

  // 监听新出现的 ShadowRoot(react-contexify 创建菜单时会动态 attachShadow)
  var newShadowObserver = new MutationObserver(function (muts) {
    for (var i = 0; i < muts.length; i++) {
      var m = muts[i];
      for (var j = 0; j < m.addedNodes.length; j++) {
        var n = m.addedNodes[j];
        if (n && n.nodeType === 1 && n.shadowRoot) {
          // 新 ShadowRoot 出现,立即观察 + 处理
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
  window.__zhDebug = function() {
    var info = {
      version: 'v1.10',
      dictSize: dictKeys.length,
      patchCount: window.__zhPatchCount || 0,
      nowrapCount: window.__zhNowrapCount || 0,
      nowrapKilled: !!window.__ZH_NO_NOWRAP__,
      shadowRoots: [],
      shadowTexts: [],
      missedSamples: []
    };
    var roots = [];
    collectRoots(document.documentElement, roots);
    info.shadowRoots = roots.filter(function(r) { return r.nodeType === 11; }).length;
    // 抓 ShadowRoot 里所有英文 textNode 样本
    for (var i = 0; i < roots.length; i++) {
      var r = roots[i];
      if (r.nodeType !== 11) continue;
      var tw = document.createTreeWalker(r, NodeFilter.SHOW_TEXT, null);
      while (tw.nextNode()) {
        var v = tw.currentNode.nodeValue;
        if (v && v.length > 1 && v.length < 100 && /^[A-Z][a-zA-Z\s.\u2026\u2019\u2018]+$/.test(v)) {
          info.shadowTexts.push(v);
          if (info.shadowTexts.length >= 30) break;
        }
      }
    }
    return info;
  };
})();