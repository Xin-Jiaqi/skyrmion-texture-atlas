#!/usr/bin/env python3
"""知乎数据回流 · 匹配与生成器。

读取映射表 config/mappings.yaml + 缓存 data/contents.json，
按 URL 精确 / 关键字模糊匹配出每条映射对应的赞 / 藏 / 评论，并生成:
    output/data.json          完整结构化数据（标题/URL/赞/藏/评论/时间/较昨日变化）
    output/zhihu-stats.json   网站 JS 直接读取的轻量数据
    output/zhihu-card.html    仿个人主页风格的 HTML 卡片片段（含变化量）
    output/zhihu-readme.md    GitHub README 可直接粘贴的 Markdown 片段
    output/badges/zhihu-<id>.svg  每项一个简洁 SVG badge
    output/history.json       按天记录的历史趋势（用于计算较昨日变化、画趋势图）

用法:
    python3 src/build.py                       # 用默认映射表与缓存
    python3 src/build.py --mapping PATH --cache PATH

说明:
    - 只读本地缓存，不调用 CLI，不消耗配额（重新抓取请先跑 fetch_contents.py）；
    - 匹配不到的条目会打印 WARN 并标记 matched=false，方便发现映射表错误；
    - 首次构建没有历史点，delta 为 null；之后每天一个历史点，
      同一天多次构建只覆盖当天点，趋势按天记录。
"""
import argparse
import datetime
import difflib
import html
import json
import os
import re
import shutil
import sys

try:
    import yaml
except ImportError:
    sys.exit("缺少 PyYAML，请先运行: pip install pyyaml")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_MAPPING = os.path.join(ROOT, "config", "mappings.yaml")
DEFAULT_CACHE = os.path.join(ROOT, "data", "contents.json")
OUTPUT_DIR = os.path.join(ROOT, "output")
BADGE_DIR = os.path.join(OUTPUT_DIR, "badges")
HISTORY = os.path.join(OUTPUT_DIR, "history.json")

TYPE_LABEL = {"answer": "回答", "article": "文章", "pin": "想法",
              "zvideo": "视频", "question": "提问"}

ZHIHU_BLUE = "#0084ff"
BADGE_DARK = "#3a3a3a"


# ---------------- 数据装载 ----------------

def load_cache(path):
    """缓存可能有两种格式：CLI 原始响应（{Code,Data:{Items}}）或纯条目列表。"""
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    if isinstance(raw, dict) and "Data" in raw and isinstance(raw["Data"], dict):
        return raw["Data"].get("Items") or []
    if isinstance(raw, list):
        return raw
    sys.exit(f"无法识别的缓存格式: {path}")


def load_history(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        raw = json.load(f)
    return raw.get("points", []) if isinstance(raw, dict) else []


def load_meta(path):
    """读取抓取元信息（新鲜度判断用）。"""
    if not os.path.exists(path):
        return None
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def cache_stale_days(meta, now=None):
    """缓存距今多少天；无元信息返回 None。"""
    if not meta or not meta.get("fetched_at"):
        return None
    try:
        fetched = datetime.datetime.fromisoformat(meta["fetched_at"])
    except ValueError:
        return None
    now = now or datetime.datetime.now()
    return (now - fetched).days


# ---------------- 匹配 ----------------

def norm_url(u):
    """URL 归一化：去协议头、尾斜杠与查询串，便于模糊比较。"""
    if not u:
        return ""
    u = u.strip().rstrip("/")
    u = re.sub(r"^https?://", "", u)
    return u.split("?")[0]


def match_entry(entry, items):
    """按映射条目匹配缓存条目，返回匹配到的内容列表。"""
    zh = entry.get("zhihu") or {}
    if not zh:
        return []
    if zh.get("url"):
        target = norm_url(zh["url"])
        return [it for it in items if norm_url(it.get("Url")) == target]
    if zh.get("urls"):
        targets = {norm_url(u) for u in zh["urls"]}
        return [it for it in items if norm_url(it.get("Url")) in targets]
    if zh.get("keywords"):
        kws = [k.lower() for k in zh["keywords"]]
        return [it for it in items
                if any(k in (it.get("Title") or "").lower() for k in kws)]
    return []


def suggest_matches(entry, items, top=3):
    """未匹配时给出候选：按标题相似度（difflib）推荐缓存中最接近的条目。

    查询词：keywords 映射用关键字，其余用条目 name。
    """
    zh = entry.get("zhihu") or {}
    queries = zh.get("keywords") or [entry.get("name") or entry.get("id")]
    titles = [(it.get("Title") or "", it.get("Url") or "") for it in items]
    scored = []
    for t, u in titles:
        if not t:
            continue
        best = max(difflib.SequenceMatcher(None, q.lower(), t.lower()).ratio()
                   for q in queries)
        if best > 0.35:
            scored.append((best, t, u))
    scored.sort(key=lambda x: x[0], reverse=True)
    return scored[:top]


def item_stats(it):
    return {
        "like_count": it.get("LikeCount") or 0,
        "favorite_count": it.get("FavoriteCount") or 0,
        "comment_count": it.get("CommentCount") or 0,
    }


def content_summary(it):
    return {
        "title": it.get("Title") or "",
        "url": it.get("Url") or "",
        "type": it.get("ContentType") or "",
        "type_label": TYPE_LABEL.get(it.get("ContentType"), it.get("ContentType") or ""),
        "created_at": fmt_ts(it.get("CreatedAt")),
        **item_stats(it),
    }


def fmt_ts(ts):
    if not ts:
        return None
    try:
        return datetime.datetime.fromtimestamp(int(ts)).strftime("%Y-%m-%d")
    except (ValueError, OSError):
        return None


# ---------------- 数据组装 ----------------

def build_data(items_matched, generated_at, cache_meta=None, history_points=0):
    """生成 data.json 结构。"""
    out_items = []
    totals = {"like_count": 0, "favorite_count": 0, "comment_count": 0}
    for m in items_matched:
        contents = [content_summary(it) for it in m["contents"]]
        stats = {
            "like_count": sum(c["like_count"] for c in contents),
            "favorite_count": sum(c["favorite_count"] for c in contents),
            "comment_count": sum(c["comment_count"] for c in contents),
            "item_count": len(contents),
        }
        for k in ("like_count", "favorite_count", "comment_count"):
            totals[k] += stats[k]
        out_items.append({
            "id": m["entry"]["id"],
            "name": m["entry"].get("name", m["entry"]["id"]),
            "kind": m["entry"].get("kind", "repo"),
            "repo": m["entry"].get("repo"),
            "page": m["entry"].get("page"),
            "note": (m["entry"].get("zhihu") or {}).get("note"),
            "matched": m["matched"],
            "match_method": m["match_method"],
            "stats": stats,
            "contents": contents,
        })
    stale_days = cache_stale_days(cache_meta)
    return {
        "schema_version": 3,
        "generated_at": generated_at,
        "source": "zhihu-cli me contents（缓存 data/contents.json）",
        "cache_fetched_at": (cache_meta or {}).get("fetched_at"),
        "cache_stale_days": stale_days,
        "history_points": history_points,
        "items": out_items,
        "totals": totals,
    }


def compute_delta(prev_point, data):
    """基于上一个历史点，给 data 的每项与 totals 附上 delta（无历史则为 None）。"""
    prev_items = (prev_point or {}).get("items", {})
    for it in data["items"]:
        if not it["matched"]:
            it["delta"] = None
            continue
        prev = prev_items.get(it["id"])
        if not prev:
            it["delta"] = None
            continue
        cur = {"like_count": it["stats"]["like_count"],
               "favorite_count": it["stats"]["favorite_count"],
               "comment_count": it["stats"]["comment_count"]}
        it["delta"] = {k: cur[k] - prev[k] for k in cur}
    prev_totals = (prev_point or {}).get("totals")
    if prev_totals:
        data["totals"]["delta"] = {k: data["totals"][k] - prev_totals[k]
                                   for k in ("like_count", "favorite_count", "comment_count")}
    else:
        data["totals"]["delta"] = None
    return data


def save_history(history_path, data):
    """按天追加/覆盖一个历史点，返回历史点列表（供下次对比）。"""
    points = load_history(history_path)
    today = data["generated_at"][:10]
    point = {
        "date": today,
        "totals": {k: v for k, v in data["totals"].items() if k in
                   ("like_count", "favorite_count", "comment_count")},
        "items": {
            it["id"]: {"like_count": it["stats"]["like_count"],
                       "favorite_count": it["stats"]["favorite_count"],
                       "comment_count": it["stats"]["comment_count"]}
            for it in data["items"] if it["matched"]
        },
    }
    points = [p for p in points if p.get("date") != today]
    points.append(point)
    points.sort(key=lambda p: p["date"])
    os.makedirs(os.path.dirname(history_path), exist_ok=True)
    with open(history_path, "w", encoding="utf-8") as f:
        json.dump({"points": points}, f, ensure_ascii=False, indent=2)
    return points


def build_slim(data):
    """生成网站 JS 直接读取的轻量 JSON（含近 30 天趋势序列）。"""
    return {
        "generated_at": data["generated_at"],
        "updated": data["generated_at"][:10],
        "history": [{"date": p["date"], "like": p["totals"].get("like_count", 0),
                     "favorite": p["totals"].get("favorite_count", 0)}
                    for p in data.get("history", [])][-30:],
        "items": {
            it["id"]: {
                "title": it["name"],
                "url": (it["contents"][0]["url"] if it["contents"] else ""),
                "like": it["stats"]["like_count"],
                "favorite": it["stats"]["favorite_count"],
                "comment": it["stats"]["comment_count"],
            }
            for it in data["items"] if it["matched"]
        },
    }


# ---------------- 生成器：HTML 卡片 ----------------

def _delta_html(delta, cls):
    """把 delta 渲染成 +x / -x 小标，无变化返回空串。"""
    if not delta or delta["favorite_count"] == delta["like_count"] == delta["comment_count"] == 0:
        return ""
    fav, like, cmt = (delta["favorite_count"], delta["like_count"], delta["comment_count"])
    parts = []
    for v, unit in ((like, "赞"), (fav, "藏"), (cmt, "评")):
        if v > 0:
            parts.append(f"+{v}{unit}")
        elif v < 0:
            parts.append(f"{v}{unit}")
    return f'<small class="{cls}">{" ".join(parts)}</small>' if parts else ""


def build_card(data):
    """仿个人主页卡片风格（Xin-Jiaqi.github.io：白卡片 + 圆角 + chip 标签）。"""
    t = data["totals"]
    rows = []
    for it in data["items"]:
        if not it["matched"]:
            continue
        badge = it["stats"]
        link = (it["contents"][0]["url"] if it["contents"] else it.get("page")) or "#"
        zh = it["contents"]
        sub = f'{len(zh)} 条' if len(zh) > 1 else TYPE_LABEL.get(zh[0]["type"], "")
        delta = _delta_html(it.get("delta"), "zhfb-delta")
        rows.append(f"""      <li class="zhfb-row">
        <div class="zhfb-row-main">
          <a class="zhfb-row-title" href="{html.escape(link, quote=True)}" target="_blank" rel="noopener">{html.escape(it['name'])}</a>
          <span class="zhfb-chip">{html.escape(sub)}</span>
        </div>
        <div class="zhfb-row-stats">
          <span class="zhfb-num">{badge['favorite_count']}</span><span class="zhfb-unit">藏</span>
          <span class="zhfb-num">{badge['like_count']}</span><span class="zhfb-unit">赞</span>
          <span class="zhfb-num">{badge['comment_count']}</span><span class="zhfb-unit">评</span>
          {delta}
        </div>
      </li>""")
    updated = data["generated_at"][:10]
    t_delta = _delta_html(t.get("delta"), "zhfb-delta")
    return f"""<!-- ============================================================
 知乎数据回流卡片 · 由 05-data-backflow/src/build.py 自动生成，请勿手改
 重新生成: python3 src/build.py（映射表: config/mappings.yaml）
 ============================================================ -->
<style>
  .zhfb-card {{ background: rgba(255,255,255,.94); border: 1px solid #e5e5ea;
    border-radius: 24px; box-shadow: 0 8px 26px rgba(0,0,0,.045);
    padding: 22px 24px; max-width: 720px; font-family: -apple-system,"PingFang SC","Microsoft YaHei",sans-serif; }}
  .zhfb-head {{ display: flex; align-items: baseline; justify-content: space-between; margin-bottom: 14px; }}
  .zhfb-head b {{ font-size: 17px; color: #1d1d1f; }}
  .zhfb-head a {{ font-size: 12.5px; color: #0066cc; text-decoration: none; }}
  .zhfb-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-bottom: 14px; }}
  .zhfb-stat {{ background: #f7f7f9; border-radius: 16px; padding: 12px; text-align: center; }}
  .zhfb-stat b {{ display: block; font-size: 22px; color: #1d1d1f; }}
  .zhfb-stat span {{ font-size: 12px; color: #6b7078; }}
  .zhfb-delta {{ font-size: 10.5px; color: #1a7f37; background: #eef7ee; border-radius: 999px;
    padding: 1px 7px; margin-left: 2px; white-space: nowrap; }}
  .zhfb-list {{ list-style: none; margin: 0; padding: 0; }}
  .zhfb-row {{ display: flex; align-items: center; justify-content: space-between; gap: 12px;
    padding: 9px 0; border-bottom: 1px solid #f0f0f2; }}
  .zhfb-row:last-child {{ border-bottom: none; padding-bottom: 0; }}
  .zhfb-row-main {{ display: flex; align-items: center; gap: 8px; min-width: 0; }}
  .zhfb-row-title {{ font-size: 13.5px; color: #1d1d1f; text-decoration: none; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
  .zhfb-row-title:hover {{ color: #0066cc; }}
  .zhfb-chip {{ flex: none; padding: 2px 9px; border-radius: 999px; background: #f2f2f4; color: #52565c; font-size: 11.5px; }}
  .zhfb-row-stats {{ flex: none; display: flex; align-items: baseline; gap: 4px; }}
  .zhfb-num {{ font-size: 13px; font-weight: 650; color: #3f4247; }}
  .zhfb-unit {{ font-size: 11px; color: #6b7078; }}
  .zhfb-foot {{ margin-top: 12px; font-size: 11px; color: #9a9ea6; text-align: right; }}
</style>
<div class="zhfb-card">
  <div class="zhfb-head">
    <b>知乎创作 · 数据回流</b>
    <a href="https://www.zhihu.com" target="_blank" rel="noopener">数据源：知乎开放平台</a>
  </div>
  <div class="zhfb-grid">
    <div class="zhfb-stat"><b>{t['favorite_count']}</b><span>累计收藏 {t_delta}</span></div>
    <div class="zhfb-stat"><b>{t['like_count']}</b><span>累计点赞</span></div>
    <div class="zhfb-stat"><b>{t['comment_count']}</b><span>累计评论</span></div>
  </div>
  <ul class="zhfb-list">
{chr(10).join(rows)}
  </ul>
  <div class="zhfb-foot">更新于 {updated} · 数据由 Zhihu CLI 抓取</div>
</div>
"""


# ---------------- 生成器：README Markdown ----------------

def build_readme(data):
    """生成 GitHub README 可直接粘贴的 Markdown 片段（含 badge 与较昨日变化）。"""
    t = data["totals"]
    d = t.get("delta")
    delta_txt = "—"
    if d and (d["like_count"] or d["favorite_count"] or d["comment_count"]):
        parts = []
        for v, u in ((d["like_count"], "赞"), (d["favorite_count"], "藏"), (d["comment_count"], "评")):
            if v:
                parts.append(f"{v:+d} {u}")
        delta_txt = " / ".join(parts)
    lines = [
        "<!-- 知乎数据回流 · 由 05-data-backflow/src/build.py 自动生成，请勿手改 -->",
        "## 知乎数据回流",
        "",
        "实时展示本项目配套知乎内容的赞 / 藏 / 评论（数据源：知乎开放平台 Zhihu CLI）。",
        "",
        "![知乎全项目合计](badges/zhihu-total.svg)",
        "",
        "![收藏与点赞趋势](trend.svg)",
        "",
    ]
    for it in data["items"]:
        if it["matched"]:
            safe = re.sub(r"[^A-Za-z0-9_-]", "-", it["id"])
            lines.append(f"![知乎 · {it['stats']['like_count']} 赞 · {it['stats']['favorite_count']} 藏](badges/zhihu-{safe}.svg)")
    lines += ["", "| 项目 / 页面 | 知乎内容 | 赞 | 藏 | 评 | 较昨日 |", "|---|---|---|---|---|---|"]
    for it in data["items"]:
        if not it["matched"]:
            continue
        s = it["stats"]
        link = (it["contents"][0]["url"] if it["contents"] else it.get("page")) or "#"
        dlt = it.get("delta")
        cell = "—"
        if dlt and (dlt["like_count"] or dlt["favorite_count"] or dlt["comment_count"]):
            parts = [f"{v:+d}{u}" for v, u in
                     ((dlt["like_count"], "赞"), (dlt["favorite_count"], "藏"), (dlt["comment_count"], "评")) if v]
            cell = " ".join(parts)
        lines.append(f"| [{it['name']}]({it.get('page') or link}) | [{s['item_count']} 条]({link}) | "
                     f"{s['like_count']} | {s['favorite_count']} | {s['comment_count']} | {cell} |")
    lines += ["", f"_更新于 {data['generated_at'][:10]} · 共 {len([i for i in data['items'] if i['matched']])} 个项目 · "
                  f"{t['favorite_count']} 藏 / {t['like_count']} 赞 / {t['comment_count']} 评 · 较昨日 {delta_txt}_",
              ""]
    return "\n".join(lines)


# ---------------- 生成器：SVG badge ----------------

def text_width(s, size):
    """粗略估算文本像素宽度（拉丁 ~0.62em，CJK ~1.05em）。"""
    w = 0.0
    for ch in s:
        w += 1.05 if ord(ch) > 0x2E7F else 0.62
    return w * size


def build_badge(item, data):
    """生成 shields.io 风格 flat badge：label=知乎，value=赞/藏/评。"""
    s = item["stats"]
    value = f"{s['like_count']} 赞 · {s['favorite_count']} 藏"
    if s["comment_count"]:
        value += f" · {s['comment_count']} 评"
    label = "知乎"
    fs, height, pad = 11, 20, 6
    lw = round(text_width(label, fs) + pad * 2)
    vw = round(text_width(value, fs) + pad * 2)
    width = lw + vw
    title = f"{item['name']}：知乎 {value}"
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" role="img" aria-label="{html.escape(title, quote=True)}">
  <title>{html.escape(title)}</title>
  <rect width="{lw}" height="{height}" fill="{ZHIHU_BLUE}"/>
  <rect x="{lw}" width="{vw}" height="{height}" fill="{BADGE_DARK}"/>
  <text x="{lw / 2}" y="14" fill="#fff" font-family="Verdana,DejaVu Sans,sans-serif" font-size="{fs}" text-anchor="middle">{html.escape(label)}</text>
  <text x="{lw + vw / 2}" y="14" fill="#fff" font-family="Verdana,DejaVu Sans,sans-serif" font-size="{fs}" text-anchor="middle">{html.escape(value)}</text>
</svg>
"""


# ---------------- 生成器：趋势图 / 总徽章 / 变更摘要 ----------------

def build_trend_svg(points, max_points=30):
    """基于历史点画收藏/点赞双线 sparkline（近 max_points 天）。

    点数 < 2 时输出占位说明（历史在积累，数据不造假）。
    """
    W, H, PAD_L, PAD_R, PAD_T, PAD_B = 520, 150, 10, 14, 26, 24
    pts = points[-max_points:]
    if len(pts) < 2:
        return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" role="img" '
                f'aria-label="知乎数据趋势（历史积累中）">\n'
                f'  <rect width="{W}" height="{H}" fill="#fbfcfe"/>\n'
                f'  <text x="{W / 2}" y="{H / 2}" fill="#8a93a6" font-family="Verdana,sans-serif" '
                f'font-size="13" text-anchor="middle">历史积累中：已有 {len(pts)} 个数据点，'
                f'满 2 天后自动出趋势图</text>\n</svg>\n')
    favs = [p.get("totals", {}).get("favorite_count", 0) for p in pts]
    likes = [p.get("totals", {}).get("like_count", 0) for p in pts]
    vmax = max(max(favs), max(likes), 1)
    inner_w, inner_h = W - PAD_L - PAD_R, H - PAD_T - PAD_B
    xs = [PAD_L + inner_w * i / (len(pts) - 1) for i in range(len(pts))]
    def yof(v):
        return PAD_T + inner_h * (1 - v / vmax)
    def poly(vals):
        return " ".join(f"{xs[i]:.1f},{yof(v):.1f}" for i, v in enumerate(vals))
    def dots(vals, color):
        return "".join(
            f'<circle cx="{xs[i]:.1f}" cy="{yof(v):.1f}" r="2.6" fill="{color}"/>'
            for i, v in enumerate(vals))
    d1 = pts[0]["date"][5:].replace("-", "/")
    d2 = pts[-1]["date"][5:].replace("-", "/")
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" role="img" aria-label="知乎收藏与点赞趋势">
  <rect width="{W}" height="{H}" rx="14" fill="#fbfcfe" stroke="#e5e9f0"/>
  <line x1="{PAD_L}" y1="{PAD_T + inner_h}" x2="{W - PAD_R}" y2="{PAD_T + inner_h}" stroke="#dfe4ec" stroke-width="1"/>
  <polyline points="{poly(favs)}" fill="none" stroke="#0084ff" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
  <polyline points="{poly(likes)}" fill="none" stroke="#ff9f1c" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>
  {dots(favs, '#0084ff')}{dots(likes, '#ff9f1c')}
  <text x="{W - PAD_R}" y="16" fill="#8a93a6" font-family="Verdana,sans-serif" font-size="10" text-anchor="end">
    <tspan fill="#0084ff">●</tspan> 收藏 <tspan fill="#ff9f1c">●</tspan> 点赞
  </text>
  <text x="{PAD_L}" y="{H - 8}" fill="#8a93a6" font-family="Verdana,sans-serif" font-size="10">{d1}</text>
  <text x="{W - PAD_R}" y="{H - 8}" fill="#8a93a6" font-family="Verdana,sans-serif" font-size="10" text-anchor="end">{d2}</text>
</svg>
"""


def build_total_badge(data):
    """全项目合计 badge：知乎 · N 藏 · N 赞。"""
    t = data["totals"]
    label = "知乎"
    value = f"{t['favorite_count']} 藏 · {t['like_count']} 赞"
    if t.get("comment_count"):
        value += f" · {t['comment_count']} 评"
    fs, height, pad = 11, 20, 6
    lw = round(text_width(label, fs) + pad * 2)
    vw = round(text_width(value, fs) + pad * 2)
    width = lw + vw
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" role="img" aria-label="知乎全项目合计 {value}">
  <title>知乎全项目合计 {value}</title>
  <rect width="{lw}" height="{height}" fill="{ZHIHU_BLUE}"/>
  <rect x="{lw}" width="{vw}" height="{height}" fill="{BADGE_DARK}"/>
  <text x="{lw / 2}" y="14" fill="#fff" font-family="Verdana,DejaVu Sans,sans-serif" font-size="{fs}" text-anchor="middle">{html.escape(label)}</text>
  <text x="{lw + vw / 2}" y="14" fill="#fff" font-family="Verdana,DejaVu Sans,sans-serif" font-size="{fs}" text-anchor="middle">{html.escape(value)}</text>
</svg>
"""


def delta_parts(delta):
    """把 delta 变成 [('赞', +2), ...] 便于各处复用。"""
    if not delta:
        return []
    return [(u, v) for v, u in ((delta["like_count"], "赞"),
                                (delta["favorite_count"], "藏"),
                                (delta["comment_count"], "评")) if v]


def build_changes(data):
    """生成变更摘要 Markdown（供人看 + 作 CI commit message）。"""
    t = data["totals"]
    lines = ["# 知乎数据回流 · 变更摘要", ""]
    if data.get("history_points", 1) == 1:
        lines.append(f"- {data['generated_at'][:10]} · 初始记录：{len([i for i in data['items'] if i['matched']])} 个项目，"
                     f"{t['favorite_count']} 藏 / {t['like_count']} 赞 / {t['comment_count']} 评")
        lines.append("")
        return "\n".join(lines)
    d = t.get("delta")
    if not d or not delta_parts(d):
        lines.append(f"- {data['generated_at'][:10]} · 较昨日无变化")
    else:
        parts = delta_parts(d)
        lines.append(f"- {data['generated_at'][:10]} · 较昨日 " +
                     " / ".join(f"{v:+d} {u}" for u, v in parts))
        for it in data["items"]:
            if it["matched"] and it.get("delta") and delta_parts(it["delta"]):
                sub = " ".join(f"{v:+d} {u}" for u, v in delta_parts(it["delta"]))
                lines.append(f"  - {it['name']}：{sub}")
    lines.append("")
    return "\n".join(lines)


def build_weekly(data, points):
    """周报：最近 7 天 vs 更早基线的总量变化 + 各项目增长排名。

    历史不足 8 个点时不输出推测，给出占位说明（不造假数据）。
    """
    if len(points) < 2:
        return ("# 知乎数据回流 · 周报\n\n"
                f"- 历史数据不足：已有 {len(points)} 个数据点，"
                "需要至少 2 个点才能计算增长（建议每天自动构建，积累后自动出周报）\n")
    last = points[-1]
    today = last["date"]
    week_ago = (datetime.datetime.strptime(today, "%Y-%m-%d")
                - datetime.timedelta(days=7)).strftime("%Y-%m-%d")
    base = None
    for p in reversed(points[:-1]):
        if p["date"] <= week_ago:
            base = p
            break
    if base is None:
        return ("# 知乎数据回流 · 周报\n\n"
                f"- 历史数据不足：最早记录 {points[0]['date']}，需要跨满 7 天才能出周报\n")
    lt, bt = last["totals"], base["totals"]
    d = {k: lt.get(k, 0) - bt.get(k, 0)
         for k in ("like_count", "favorite_count", "comment_count")}
    lines = ["# 知乎数据回流 · 周报", "",
             f"- 统计区间：{base['date']} → {last['date']}（{today}）",
             f"- 总量变化：{d['favorite_count']:+d} 藏 / {d['like_count']:+d} 赞 / "
             f"{d['comment_count']:+d} 评"]
    growth = []
    for item_id, b in base.get("items", {}).items():
        c = last.get("items", {}).get(item_id)
        if not c:
            continue
        growth.append((c.get("favorite_count", 0) - b.get("favorite_count", 0),
                       c.get("like_count", 0) - b.get("like_count", 0), item_id))
    growth.sort(reverse=True)
    lines.append("")
    lines.append("### 收藏增长 Top 3")
    for fav_d, like_d, item_id in growth[:3]:
        lines.append(f"- {item_id}：{fav_d:+d} 藏 / {like_d:+d} 赞")
    lines.append("")
    return "\n".join(lines)


# ---------------- 主流程 ----------------

def main():
    ap = argparse.ArgumentParser(description="知乎数据回流：匹配 + 生成产物")
    ap.add_argument("--mapping", default=DEFAULT_MAPPING, help="映射表 YAML 路径")
    ap.add_argument("--cache", default=DEFAULT_CACHE, help="me contents 缓存 JSON 路径")
    ap.add_argument("--out", default=OUTPUT_DIR, help="输出目录")
    ap.add_argument("--history", default=HISTORY, help="历史趋势 JSON 路径")
    args = ap.parse_args()

    with open(args.mapping, encoding="utf-8") as f:
        mapping = yaml.safe_load(f)
    items = load_cache(args.cache)

    matched_all = []
    for entry in mapping["items"]:
        zh = entry.get("zhihu") or {}
        method = ("url" if zh.get("url") else "urls" if zh.get("urls")
                  else "title_contains" if zh.get("keywords") else "none")
        hits = match_entry(entry, items)
        matched = bool(hits)
        if not matched:
            target = zh.get("url") or (zh.get("urls") or [None])[0] or zh.get("keywords")
            print(f"WARN [{entry['id']}] 未匹配到内容: {target}")
            for score, t, u in suggest_matches(entry, items):
                print(f"      候选 (相似度 {score:.2f}): {t[:36]} | {u}")
        matched_all.append({"entry": entry, "contents": hits, "matched": matched,
                            "match_method": method})

    generated_at = datetime.datetime.now().isoformat(timespec="seconds")
    history = load_history(args.history)
    prev_point = history[-1] if history else None
    meta = load_meta(os.path.join(ROOT, "data", "fetch_meta.json"))
    data = build_data(matched_all, generated_at, cache_meta=meta,
                      history_points=len(history))
    data = compute_delta(prev_point, data)
    points = save_history(args.history, data)
    data["history_points"] = len(points)
    data["history"] = points
    slim = build_slim(data)
    stale = data.get("cache_stale_days")
    if stale is not None and stale >= 7:
        print(f"WARN 缓存已 {stale} 天，建议运行: python3 src/fetch_contents.py --incremental")

    os.makedirs(os.path.join(args.out, "badges"), exist_ok=True)
    with open(os.path.join(args.out, "data.json"), "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    with open(os.path.join(args.out, "zhihu-stats.json"), "w", encoding="utf-8") as f:
        json.dump(slim, f, ensure_ascii=False, indent=2)
    with open(os.path.join(args.out, "zhihu-card.html"), "w", encoding="utf-8") as f:
        f.write(build_card(data))
    with open(os.path.join(args.out, "zhihu-readme.md"), "w", encoding="utf-8") as f:
        f.write(build_readme(data))
    for it in data["items"]:
        if it["matched"]:
            safe_id = re.sub(r"[^A-Za-z0-9_-]", "-", it["id"])
            with open(os.path.join(args.out, "badges", f"zhihu-{safe_id}.svg"),
                      "w", encoding="utf-8") as f:
                f.write(build_badge(it, data))
    with open(os.path.join(args.out, "badges", "zhihu-total.svg"),
              "w", encoding="utf-8") as f:
        f.write(build_total_badge(data))
    with open(os.path.join(args.out, "trend.svg"), "w", encoding="utf-8") as f:
        f.write(build_trend_svg(points))
    with open(os.path.join(args.out, "CHANGES.md"), "w", encoding="utf-8") as f:
        f.write(build_changes(data))
    with open(os.path.join(args.out, "weekly.md"), "w", encoding="utf-8") as f:
        f.write(build_weekly(data, points))
    widget_src = os.path.join(ROOT, "src", "zhihu-widget.js")
    if os.path.exists(widget_src):
        shutil.copy(widget_src, os.path.join(args.out, "zhihu-widget.js"))

    t = data["totals"]
    print(f"生成完成: {os.path.abspath(args.out)}")
    print(f"  映射 {len(data['items'])} 条 / 匹配成功 {sum(1 for i in data['items'] if i['matched'])} 条")
    print(f"  累计: {t['favorite_count']} 藏 · {t['like_count']} 赞 · {t['comment_count']} 评"
          f"（历史点 {len(points)} 个）")
    for it in data["items"]:
        if it["matched"]:
            s = it["stats"]
            d = it.get("delta")
            d_txt = ""
            if d and (d["like_count"] or d["favorite_count"] or d["comment_count"]):
                d_txt = f"  较昨日 +{d['favorite_count']}藏/+{d['like_count']}赞" if d["favorite_count"] >= 0 else ""
                parts = [f"{v:+d}{u}" for v, u in
                         ((d["like_count"], "赞"), (d["favorite_count"], "藏"), (d["comment_count"], "评")) if v]
                d_txt = "  " + " ".join(parts)
            print(f"  - {it['id']:<32} {s['favorite_count']:>4} 藏 {s['like_count']:>4} 赞 "
                  f"{s['comment_count']:>3} 评 ({len(it['contents'])} 条, {it['match_method']}){d_txt}")


if __name__ == "__main__":
    main()
