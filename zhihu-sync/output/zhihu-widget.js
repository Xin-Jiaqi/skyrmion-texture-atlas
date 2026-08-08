/* ============================================================
 * 知乎数据回流 · 通用站点组件（自动生成产物，勿手改）
 * 由 05-data-backflow/src/build.py 复制到 output/zhihu-widget.js
 *
 * 用法（任何 HTML 页面）：
 *   <div id="zhihu-widget"></div>
 *   <script src="zhihu-widget.js"></script>
 *   组件自动 fetch("zhihu-stats.json")（与页面同级），
 *   渲染：合计 + 各项目赞/藏/评 + 收藏/点赞迷你趋势（数据满 2 天自动出现）。
 *
 * 可配置（写在 zhihu-widget.js 之前）：
 *   window.ZHIHU_WIDGET_SELECTOR = "#myId";   // 容器选择器
 *   window.ZHIHU_STATS_URL = "./assets/zhihu-stats.json"; // 数据路径
 *   window.ZHIHU_STATS_FALLBACK = {...};      // fetch 失败时的内嵌兜底
 *   或页面里放 <script id="zhihuStatsFallback" type="application/json">...</script>
 * ============================================================ */
(function () {
  "use strict";
  var SEL = window.ZHIHU_WIDGET_SELECTOR || "#zhihu-widget";
  var URL = window.ZHIHU_STATS_URL || "zhihu-stats.json";
  var BLUE = "#0084ff", ORANGE = "#ff9f1c";

  function esc(s) {
    return String(s == null ? "" : s).replace(/[&<>"']/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c];
    });
  }

  function sparkline(history) {
    if (!history || history.length < 2) return "";
    var W = 520, H = 52, P = 4, T = 10;
    var favs = history.map(function (p) { return p.favorite || 0; });
    var likes = history.map(function (p) { return p.like || 0; });
    var vmax = Math.max.apply(null, favs.concat(likes)) || 1;
    var iw = W - P * 2, ih = H - T - P;
    function line(vals, color) {
      var pts = vals.map(function (v, i) {
        var x = P + iw * i / (vals.length - 1);
        var y = T + ih * (1 - v / vmax);
        return x.toFixed(1) + "," + y.toFixed(1);
      });
      return '<polyline points="' + pts.join(" ") + '" fill="none" stroke="' + color +
             '" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>';
    }
    return '<svg class="zhw-trend" viewBox="0 0 ' + W + " " + H + '" preserveAspectRatio="none" ' +
           'aria-label="收藏与点赞趋势">' +
           '<line x1="' + P + '" y1="' + (T + ih) + '" x2="' + (W - P) + '" y2="' + (T + ih) +
           '" stroke="#e3e8f0" stroke-width="1"/>' +
           line(favs, BLUE) + line(likes, ORANGE) +
           '<text x="' + (W - P) + '" y="9" fill="#8a93a6" font-size="8" text-anchor="end">' +
           '<tspan fill="' + BLUE + '">●</tspan> 收藏 <tspan fill="' + ORANGE + '">●</tspan> 点赞</text>' +
           "</svg>";
  }

  function render(d) {
    var el = document.querySelector(SEL);
    if (!el || !d || !d.items) return;
    var ids = Object.keys(d.items);
    if (!ids.length) return;
    var total = { like: 0, favorite: 0, comment: 0 };
    ids.forEach(function (id) {
      var it = d.items[id];
      total.like += it.like || 0;
      total.favorite += it.favorite || 0;
      total.comment += it.comment || 0;
    });
    var rows = ids.map(function (id) {
      var it = d.items[id];
      return '<a class="zhw-row" href="' + esc(it.url || "#") + '" target="_blank" rel="noopener">' +
        '<span class="zhw-row-name">' + esc(it.title || id) + "</span>" +
        '<span class="zhw-row-nums">' +
        '<b>' + (it.favorite || 0) + "</b>藏 <b>" + (it.like || 0) + "</b>赞 " +
        '<b>' + (it.comment || 0) + "</b>评</span></a>";
    }).join("");
    var upd = d.updated || (d.generated_at || "").slice(0, 10);
    el.innerHTML =
      '<div class="zhw-card">' +
      '<div class="zhw-head"><b>知乎创作 · 数据回流</b>' +
      '<a href="https://www.zhihu.com" target="_blank" rel="noopener">数据源：知乎开放平台</a></div>' +
      '<div class="zhw-grid">' +
      '<div class="zhw-stat"><b>' + total.favorite + "</b><span>累计收藏</span></div>" +
      '<div class="zhw-stat"><b>' + total.like + "</b><span>累计点赞</span></div>" +
      '<div class="zhw-stat"><b>' + total.comment + "</b><span>累计评论</span></div>" +
      "</div>" + sparkline(d.history) +
      '<div class="zhw-list">' + rows + "</div>" +
      '<div class="zhw-foot">更新于 ' + esc(upd) + " · Zhihu CLI 自动同步</div>" +
      "</div>";
  }

  function loadFallback() {
    if (window.ZHIHU_STATS_FALLBACK) return window.ZHIHU_STATS_FALLBACK;
    try {
      var n = document.getElementById("zhihuStatsFallback");
      if (n) return JSON.parse(n.textContent);
    } catch (e) { /* ignore */ }
    return null;
  }

  if (!document.querySelector(SEL)) return;
  var css = [
    ".zhw-card{background:rgba(255,255,255,.94);border:1px solid #e5e5ea;border-radius:20px;",
    "box-shadow:0 8px 26px rgba(0,0,0,.045);padding:20px;max-width:680px;font-family:-apple-system,",
    "\"PingFang SC\",\"Microsoft YaHei\",sans-serif;color:#1d1d1f}",
    ".zhw-head{display:flex;justify-content:space-between;align-items:baseline;margin-bottom:12px}",
    ".zhw-head b{font-size:16px}.zhw-head a{font-size:12px;color:#0066cc;text-decoration:none}",
    ".zhw-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:9px;margin-bottom:12px}",
    ".zhw-stat{background:#f7f7f9;border-radius:14px;padding:10px;text-align:center}",
    ".zhw-stat b{display:block;font-size:20px}.zhw-stat span{font-size:11.5px;color:#6b7078}",
    ".zhw-trend{width:100%;height:52px;display:block;margin-bottom:10px;border:1px solid #eef1f5;",
    "border-radius:12px;background:#fbfcfe}",
    ".zhw-list{display:grid;gap:2px}.zhw-row{display:flex;justify-content:space-between;gap:10px;",
    "align-items:center;padding:8px 2px;border-bottom:1px solid #f0f0f2;text-decoration:none;color:inherit}",
    ".zhw-row:last-child{border-bottom:none}",
    ".zhw-row-name{font-size:13px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}",
    ".zhw-row:hover .zhw-row-name{color:#0066cc}",
    ".zhw-row-nums{flex:none;font-size:12px;color:#3f4247}",
    ".zhw-row-nums b{font-weight:650;color:#1d1d1f}",
    ".zhw-foot{margin-top:10px;font-size:11px;color:#9a9ea6;text-align:right}"
  ].join("");
  var style = document.createElement("style");
  style.textContent = css;
  document.head.appendChild(style);

  fetch(URL).then(function (r) {
    if (!r.ok) throw new Error("no stats");
    return r.json();
  }).then(render).catch(function () {
    var f = loadFallback();
    if (f) render(f);
  });
})();
