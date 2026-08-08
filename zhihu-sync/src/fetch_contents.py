#!/usr/bin/env python3
"""抓取本人全部知乎创作并缓存为本地 JSON（数据回流的数据源）。

用法:
    python3 src/fetch_contents.py                # 有缓存则直接用，不消耗配额
    python3 src/fetch_contents.py --incremental  # 只抓新增内容（推荐日常使用）
    python3 src/fetch_contents.py --force        # 忽略缓存，重新全量抓取

输出:
    data/contents.json   全部创作条目（me contents 全量，分页拉取）
    data/fetch_meta.json 抓取元信息（时间 / 总数 / 新增条数）

说明:
    - CLI 只读本人内容，符合开放平台只读能力；
    - 分页循环直到 IsEnd=true，避免漏数据；
    - --incremental 利用 me contents 的时间排序（--sort ts --order desc），
      从最新一页往回翻，碰到缓存里已有的旧条目即停止并合并，省配额；
    - 凭证由 zhihu-cli 自己从系统钥匙串或 ZHIHU_ACCESS_SECRET 读取，
      本脚本不接触任何凭证。
"""
import argparse
import datetime
import json
import os
import subprocess
import sys

CLI = os.environ.get("ZHIHU_CLI") or "/Users/jiaqi/Library/Application Support/zhihu-cli/current/zhihu-cli"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")
CACHE = os.path.join(DATA_DIR, "contents.json")
META = os.path.join(DATA_DIR, "fetch_meta.json")

PAGE_SIZE = 50  # me contents 单页上限


def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"CLI 调用失败: {r.stderr}")
    try:
        return json.loads(r.stdout)
    except json.JSONDecodeError:
        sys.exit(f"CLI 输出不是合法 JSON: {r.stdout[:300]}")


def fetch_page(offset, sort_ts=False):
    cmd = [CLI, "me", "contents", "--type", "all",
           "--limit", str(PAGE_SIZE), "--offset", str(offset)]
    if sort_ts:
        cmd += ["--sort", "ts", "--order", "desc"]
    d = run(cmd)
    data = d.get("Data") or {}
    return data


def fetch_all():
    """分页拉取全部创作，返回 (条目列表, 总数, 调用页数)。"""
    items, offset, total, pages = [], 0, None, 0
    while True:
        data = fetch_page(offset)
        pages += 1
        items += data.get("Items") or []
        total = data.get("Paging", {}).get("Totals", len(items))
        if data.get("Paging", {}).get("IsEnd", True):
            break
        offset = int(data["Paging"]["NextOffset"])
        if len(items) >= total:
            break
    return items, total, pages


def merge_items(cached_items, new_batch):
    """把新抓取的一批条目合并进缓存（纯函数，便于单测）。

    规则：同 URL 以新数据为准（赞/藏可能增长）；返回
    (合并后的条目列表, 新增条数, 本批是否命中缓存旧条目)。
    """
    merged = {it.get("Url"): it for it in cached_items}
    new_count, hit_old = 0, False
    for it in new_batch:
        u = it.get("Url")
        if u in merged:
            hit_old = True
            merged[u] = it  # 以新数据为准
        else:
            merged[u] = it
            new_count += 1
    return list(merged.values()), new_count, hit_old


def load_cache_items():
    if not os.path.exists(CACHE):
        return None
    with open(CACHE, encoding="utf-8") as f:
        raw = json.load(f)
    if isinstance(raw, dict) and "Data" in raw:
        return raw["Data"].get("Items") or []
    if isinstance(raw, list):
        return raw
    sys.exit(f"无法识别的缓存格式: {CACHE}")


def fetch_incremental(cached):
    """时间倒序抓取，碰到缓存中已存在的条目即停，合并新增部分。

    返回 (合并后的条目列表, 新增条数, 线上总数, 调用页数)。
    """
    merged = {it.get("Url"): it for it in cached}
    new_count, offset, total, pages = 0, 0, None, 0
    while True:
        data = fetch_page(offset, sort_ts=True)
        pages += 1
        batch = data.get("Items") or []
        total = data.get("Paging", {}).get("Totals", len(batch))
        merged, batch_new, hit_old = merge_items(list(merged.values()), batch)
        merged = {it.get("Url"): it for it in merged}
        new_count += batch_new
        if hit_old or data.get("Paging", {}).get("IsEnd", True):
            break
        offset = int(data["Paging"]["NextOffset"])
        if len(batch) == 0:
            break
    return list(merged.values()), new_count, total, pages


def write_cache(items, meta):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(items, f, ensure_ascii=False, indent=2)
    with open(META, "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)


def main():
    ap = argparse.ArgumentParser(description="抓取本人全部知乎创作并缓存")
    ap.add_argument("--force", action="store_true", help="忽略缓存，强制重新全量抓取")
    ap.add_argument("--incremental", action="store_true",
                    help="增量抓取：只拉新增内容并合并进缓存（推荐，省配额）")
    args = ap.parse_args()

    cached = load_cache_items()
    if args.force or cached is None:
        items, total, pages = fetch_all()
        new_count = len(items)
        fetched_at = datetime.datetime.now().isoformat(timespec="seconds")
        write_cache(items, {"fetched_at": fetched_at, "total": total,
                            "count": len(items), "new_count": new_count,
                            "mode": "full", "api_pages": pages})
        print(f"全量抓取完成: {len(items)} 条（Totals={total}），本次调用 {pages} 页，已缓存到 {CACHE}")
        return

    if not args.incremental:
        print(f"使用缓存: {CACHE}（{len(cached)} 条，--incremental 只抓新增，--force 全量重抓）")
        return

    items, new_count, total, pages = fetch_incremental(cached)
    fetched_at = datetime.datetime.now().isoformat(timespec="seconds")
    write_cache(items, {"fetched_at": fetched_at, "total": total,
                        "count": len(items), "new_count": new_count,
                        "mode": "incremental", "api_pages": pages,
                        "note": "按 CreatedAt 时间倒序抓取并与缓存合并去重"})
    if new_count:
        print(f"增量抓取完成: 新增 {new_count} 条，缓存共 {len(items)} 条"
              f"（Totals={total}，本次调用 {pages} 页）")
    else:
        print(f"增量抓取完成: 无新增内容，缓存仍为 {len(items)} 条"
              f"（Totals={total}，本次调用 {pages} 页）")


if __name__ == "__main__":
    main()
