#!/usr/bin/env python3
"""校验 output/ 产物完整性（供本地与 CI 使用，不调用 CLI）。

检查:
    - data.json / zhihu-stats.json / zhihu-card.html / zhihu-readme.md 存在且结构正确
    - 每个匹配项都有 badge；数字非负；totals 等于各项之和
    - 知乎 URL 合法；卡片与 README 覆盖所有匹配项
    - history.json 可解析、按日期有序

用法: python3 tests/validate_outputs.py [--out PATH]
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUT = os.path.join(ROOT, "output")

errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)


def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=DEFAULT_OUT)
    args = ap.parse_args()
    out = args.out

    data_path = os.path.join(out, "data.json")
    slim_path = os.path.join(out, "zhihu-stats.json")
    card_path = os.path.join(out, "zhihu-card.html")
    readme_path = os.path.join(out, "zhihu-readme.md")
    history_path = os.path.join(out, "history.json")
    trend_path = os.path.join(out, "trend.svg")
    total_badge = os.path.join(out, "badges", "zhihu-total.svg")
    changes_path = os.path.join(out, "CHANGES.md")
    weekly_path = os.path.join(out, "weekly.md")
    widget_path = os.path.join(out, "zhihu-widget.js")

    for p in (data_path, slim_path, card_path, readme_path, history_path,
              trend_path, total_badge, changes_path, weekly_path, widget_path):
        check(os.path.exists(p), f"缺少产物: {p}")

    if not errors:
        data = load_json(data_path)
        slim = load_json(slim_path)
        history = load_json(history_path)
        card = open(card_path, encoding="utf-8").read()
        readme = open(readme_path, encoding="utf-8").read()

        check(data.get("schema_version") == 3, "data.json schema_version 应为 3")
        check(data.get("items"), "data.json 缺少 items")
        check(bool(data.get("generated_at")), "data.json 缺少 generated_at")
        check(isinstance(data.get("history_points"), int) and data["history_points"] >= 1,
              "data.json history_points 非法")
        check(isinstance(data.get("cache_stale_days"), (int, type(None))),
              "data.json cache_stale_days 非法")
        check(isinstance(data.get("history"), list) and data["history"],
              "data.json 缺少 history 序列")
        check(isinstance(slim.get("history"), list), "zhihu-stats.json 缺少 history 序列")

        trend = open(trend_path, encoding="utf-8").read()
        check(trend.startswith("<svg"), "trend.svg 不是合法 SVG")
        changes = open(changes_path, encoding="utf-8").read()
        check(changes.startswith("# 知乎数据回流"), "CHANGES.md 结构异常")
        weekly = open(weekly_path, encoding="utf-8").read()
        check(weekly.startswith("# 知乎数据回流 · 周报"), "weekly.md 结构异常")
        widget = open(widget_path, encoding="utf-8").read()
        check("ZHIHU_STATS_URL" in widget and "render" in widget, "zhihu-widget.js 结构异常")
        total_svg = open(total_badge, encoding="utf-8").read()
        check("1102 藏" in total_svg or "藏" in total_svg, "zhihu-total.svg 缺少数据")

        matched = [it for it in data["items"] if it["matched"]]
        check(matched, "没有匹配成功的映射项")

        url_re = re.compile(r"^https?://(www\.zhihu\.com|zhuanlan\.zhihu\.com)/")
        t = {"like_count": 0, "favorite_count": 0, "comment_count": 0}
        for it in matched:
            s = it["stats"]
            for k in ("like_count", "favorite_count", "comment_count"):
                check(isinstance(s[k], int) and s[k] >= 0, f"{it['id']}.stats.{k} 非法")
                t[k] += s[k]
            check(it["contents"], f"{it['id']} 匹配成功但没有内容明细")
            for c in it["contents"]:
                check(url_re.match(c["url"] or ""), f"{it['id']} 内容 URL 非法: {c['url']}")
                check(bool(c["title"]), f"{it['id']} 内容缺少标题")
            safe = re.sub(r"[^A-Za-z0-9_-]", "-", it["id"])
            check(os.path.exists(os.path.join(out, "badges", f"zhihu-{safe}.svg")),
                  f"{it['id']} 缺少 badge")
            check(it["id"] in slim["items"], f"{it['id']} 不在 zhihu-stats.json 中")
            check(it["name"] in card, f"{it['id']} 未出现在卡片片段中")
            check(it["name"] in readme, f"{it['id']} 未出现在 README 片段中")

        check(data["totals"]["like_count"] == t["like_count"] and
              data["totals"]["favorite_count"] == t["favorite_count"] and
              data["totals"]["comment_count"] == t["comment_count"],
              "data.json totals 与各项之和不一致")

        dates = [p["date"] for p in history["points"]]
        check(dates == sorted(dates), "history.json 日期未按序排列")
        check(dates[-1] == data["generated_at"][:10], "history.json 最新点不是今天")
        check(data["history_points"] == len(history["points"]),
              "data.json history_points 与 history.json 不一致")

    if errors:
        print("❌ 校验失败:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print(f"✅ 产物校验通过（{out}）")


if __name__ == "__main__":
    main()
