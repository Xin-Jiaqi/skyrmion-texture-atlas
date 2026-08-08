#!/usr/bin/env python3
"""build.py 核心逻辑单元测试（不调用 CLI，不消耗配额）。

用法: python3 tests/test_build.py
"""
import datetime
import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 兼容本仓库 src/ 布局与目标仓库 scripts/ 布局
for _sub in ("src", "scripts"):
    if os.path.isdir(os.path.join(ROOT, _sub)):
        sys.path.insert(0, os.path.join(ROOT, _sub))
        break

import build  # noqa: E402


def make_item(url, title, ctype="article", like=0, fav=0, cmt=0):
    return {"Url": url, "Title": title, "ContentType": ctype,
            "LikeCount": like, "FavoriteCount": fav, "CommentCount": cmt,
            "CreatedAt": 1786169700}


SAMPLE_ITEMS = [
    make_item("https://zhuanlan.zhihu.com/p/2069027257536999823",
              "磁性 Skyrmion 家族综述", like=7, fav=14),
    make_item("https://zhuanlan.zhihu.com/p/2068673956043821125",
              "铁电性的统一定义", like=12, fav=29),
    make_item("https://www.zhihu.com/answer/3315158231",
              "shift current 怎么理解？", ctype="answer", like=25, fav=51, cmt=10),
    make_item("https://zhuanlan.zhihu.com/p/684716524",
              "科研论文写作之 pix2tex", like=23, fav=87, cmt=3),
]


class TestNormUrl(unittest.TestCase):
    def test_variants(self):
        self.assertEqual(build.norm_url("https://www.zhihu.com/p/123/"),
                         "www.zhihu.com/p/123")
        self.assertEqual(build.norm_url("https://zhuanlan.zhihu.com/p/123?x=1"),
                         "zhuanlan.zhihu.com/p/123")
        self.assertEqual(build.norm_url(""), "")


class TestMatchEntry(unittest.TestCase):
    def test_exact_url(self):
        e = {"id": "a", "zhihu": {"url": "https://zhuanlan.zhihu.com/p/2069027257536999823"}}
        hits = build.match_entry(e, SAMPLE_ITEMS)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["Title"], "磁性 Skyrmion 家族综述")

    def test_url_trailing_slash_ok(self):
        e = {"id": "a", "zhihu": {"url": "https://zhuanlan.zhihu.com/p/2069027257536999823/"}}
        self.assertEqual(len(build.match_entry(e, SAMPLE_ITEMS)), 1)

    def test_urls_list(self):
        e = {"id": "b", "zhihu": {"urls": [
            "https://zhuanlan.zhihu.com/p/2068673956043821125",
            "https://www.zhihu.com/answer/3315158231"]}}
        hits = build.match_entry(e, SAMPLE_ITEMS)
        self.assertEqual(len(hits), 2)

    def test_title_keywords(self):
        e = {"id": "c", "zhihu": {"keywords": ["pix2tex", "科研绘图"]}}
        hits = build.match_entry(e, SAMPLE_ITEMS)
        self.assertEqual(len(hits), 1)
        self.assertIn("pix2tex", hits[0]["Title"])

    def test_no_match(self):
        e = {"id": "d", "zhihu": {"url": "https://zhuanlan.zhihu.com/p/0"}}
        self.assertEqual(build.match_entry(e, SAMPLE_ITEMS), [])

    def test_empty_zhihu(self):
        self.assertEqual(build.match_entry({"id": "e"}, SAMPLE_ITEMS), [])


class TestCacheFormat(unittest.TestCase):
    def test_cli_response_format(self):
        raw = {"Code": 0, "Data": {"Items": SAMPLE_ITEMS, "Paging": {}}}
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(raw, f)
            path = f.name
        try:
            self.assertEqual(len(build.load_cache(path)), 4)
        finally:
            os.unlink(path)

    def test_bare_list_format(self):
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
            json.dump(SAMPLE_ITEMS, f)
            path = f.name
        try:
            self.assertEqual(len(build.load_cache(path)), 4)
        finally:
            os.unlink(path)


class TestAggregation(unittest.TestCase):
    def test_build_data_sums(self):
        matched = [{"entry": {"id": "x"}, "contents": SAMPLE_ITEMS[:2],
                    "matched": True, "match_method": "url"}]
        data = build.build_data(matched, "2026-08-08T10:00:00")
        self.assertEqual(data["totals"]["favorite_count"], 43)
        self.assertEqual(data["totals"]["like_count"], 19)
        self.assertEqual(data["items"][0]["stats"]["item_count"], 2)

    def test_slim_shape(self):
        matched = [{"entry": {"id": "x", "name": "X"}, "contents": SAMPLE_ITEMS[:1],
                    "matched": True, "match_method": "url"}]
        data = build.build_data(matched, "2026-08-08T10:00:00")
        slim = build.build_slim(data)
        self.assertEqual(slim["items"]["x"]["like"], 7)
        self.assertEqual(slim["items"]["x"]["favorite"], 14)


class TestDelta(unittest.TestCase):
    def test_delta_computation(self):
        matched = [{"entry": {"id": "a"}, "contents": SAMPLE_ITEMS[:1],
                    "matched": True, "match_method": "url"}]
        data = build.build_data(matched, "2026-08-09T10:00:00")
        prev = {"date": "2026-08-08", "totals": {"like_count": 5, "favorite_count": 10,
                                                 "comment_count": 0},
                "items": {"a": {"like_count": 5, "favorite_count": 10, "comment_count": 0}}}
        build.compute_delta(prev, data)
        self.assertEqual(data["items"][0]["delta"]["favorite_count"], 4)
        self.assertEqual(data["items"][0]["delta"]["like_count"], 2)
        self.assertEqual(data["totals"]["delta"]["favorite_count"], 4)

    def test_delta_none_without_history(self):
        matched = [{"entry": {"id": "a"}, "contents": SAMPLE_ITEMS[:1],
                    "matched": True, "match_method": "url"}]
        data = build.build_data(matched, "2026-08-09T10:00:00")
        build.compute_delta(None, data)
        self.assertIsNone(data["items"][0]["delta"])
        self.assertIsNone(data["totals"]["delta"])

    def test_history_roundtrip(self):
        matched = [{"entry": {"id": "a"}, "contents": SAMPLE_ITEMS[:1],
                    "matched": True, "match_method": "url"}]
        data = build.build_data(matched, "2026-08-09T10:00:00")
        with tempfile.TemporaryDirectory() as tmp:
            hist = os.path.join(tmp, "history.json")
            points = build.save_history(hist, data)
            self.assertEqual(len(points), 1)
            # 同一天再次构建 → 仍 1 个点（覆盖）
            points = build.save_history(hist, data)
            self.assertEqual(len(points), 1)
            # 不同天 → 2 个点
            data["generated_at"] = "2026-08-10T10:00:00"
            points = build.save_history(hist, data)
            self.assertEqual(len(points), 2)


class TestBadge(unittest.TestCase):
    def test_badge_shape(self):
        matched = [{"entry": {"id": "a", "name": "测试项目"},
                    "contents": SAMPLE_ITEMS[0], "matched": True,
                    "match_method": "url"}]
        # contents 应为列表，这里用单条测试 item_stats 之外的展示逻辑
        matched[0]["contents"] = [SAMPLE_ITEMS[0]]
        data = build.build_data(matched, "2026-08-09T10:00:00")
        svg = build.build_badge(data["items"][0], data)
        self.assertTrue(svg.startswith("<svg"))
        self.assertIn('width="', svg)
        self.assertIn("14 藏", svg)


class TestTrendBadgeChanges(unittest.TestCase):
    def _sample_data(self):
        matched = [{"entry": {"id": "a", "name": "A"}, "contents": SAMPLE_ITEMS[:1],
                    "matched": True, "match_method": "url"}]
        data = build.build_data(matched, "2026-08-09T10:00:00")
        return data

    def test_trend_placeholder_under_two_points(self):
        svg = build.build_trend_svg([{"date": "2026-08-08", "totals": {}}])
        self.assertIn("历史积累中", svg)
        self.assertIn("<svg", svg)

    def test_trend_polylines_with_history(self):
        pts = [{"date": f"2026-08-0{i}", "totals": {"like_count": i * 10,
                                                     "favorite_count": i * 20}}
               for i in range(1, 6)]
        svg = build.build_trend_svg(pts)
        self.assertEqual(svg.count("<polyline"), 2)
        self.assertIn("08/01", svg)
        self.assertIn("08/05", svg)

    def test_total_badge(self):
        data = self._sample_data()
        data["totals"] = {"like_count": 398, "favorite_count": 1102, "comment_count": 53}
        svg = build.build_total_badge(data)
        self.assertTrue(svg.startswith("<svg"))
        self.assertIn("1102 藏", svg)
        self.assertIn("53 评", svg)

    def test_changes_initial(self):
        data = self._sample_data()
        data["history_points"] = 1
        md = build.build_changes(data)
        self.assertIn("初始记录", md)

    def test_changes_with_delta(self):
        data = self._sample_data()
        data["history_points"] = 3
        data["totals"]["delta"] = {"like_count": 2, "favorite_count": 5, "comment_count": 0}
        data["items"][0]["delta"] = {"like_count": 2, "favorite_count": 5, "comment_count": 0}
        md = build.build_changes(data)
        self.assertIn("较昨日", md)
        self.assertIn("+5 藏", md)

    def test_changes_no_change(self):
        data = self._sample_data()
        data["history_points"] = 3
        data["totals"]["delta"] = {"like_count": 0, "favorite_count": 0, "comment_count": 0}
        md = build.build_changes(data)
        self.assertIn("无变化", md)

    def test_cache_stale_days(self):
        meta = {"fetched_at": "2026-08-01T10:00:00"}
        now = datetime.datetime(2026, 8, 8, 12, 0, 0)
        self.assertEqual(build.cache_stale_days(meta, now=now), 7)
        self.assertIsNone(build.cache_stale_days(None))
        self.assertIsNone(build.cache_stale_days({"fetched_at": "bad"}))


class TestSuggest(unittest.TestCase):
    def test_keyword_suggest_finds_close_title(self):
        items = [make_item("https://zhuanlan.zhihu.com/p/678923831",
                           "层群 the 80 Layer Groups：概念、点群与空间群关系", fav=92),
                 make_item("https://zhuanlan.zhihu.com/p/2", "铁电材料体光伏效应", fav=51)]
        e = {"id": "x", "name": "群论工具库",
             "zhihu": {"keywords": ["Layer Groups"]}}
        hits = build.suggest_matches(e, items)
        self.assertTrue(hits)
        self.assertIn("Layer Groups", hits[0][1])

    def test_name_suggest(self):
        items = [make_item("https://zhuanlan.zhihu.com/p/2069027257536999823",
                           "磁性 Skyrmion 家族综述：从 Néel、Bloch 到 Meron、Hopfion", fav=14),
                 make_item("https://zhuanlan.zhihu.com/p/2", "无关内容", fav=1)]
        e = {"id": "skyrmion-texture-atlas", "name": "磁性 Skyrmion 家族 · 交互纹理图鉴",
             "zhihu": {"url": "https://zhuanlan.zhihu.com/p/0"}}
        hits = build.suggest_matches(e, items)
        self.assertTrue(hits)
        self.assertIn("Skyrmion", hits[0][1])


class TestWeekly(unittest.TestCase):
    def _points(self, n=8, start="2026-07-25"):
        import datetime as _dt
        pts = []
        for i in range(n):
            d = _dt.datetime.strptime(start, "%Y-%m-%d") + _dt.timedelta(days=i)
            pts.append({"date": d.strftime("%Y-%m-%d"),
                        "totals": {"like_count": 300 + i * 10,
                                   "favorite_count": 900 + i * 15,
                                   "comment_count": 40 + i},
                        "items": {"a": {"like_count": 5 + i,
                                        "favorite_count": 10 + i * 2,
                                        "comment_count": 0}}})
        return pts

    def test_placeholder_when_insufficient(self):
        md = build.build_weekly({}, [{"date": "2026-08-08", "totals": {}}])
        self.assertIn("历史数据不足", md)

    def test_weekly_delta_and_growth(self):
        md = build.build_weekly({}, self._points(8))
        self.assertIn("统计区间：2026-07-25", md)
        self.assertIn("+105 藏", md)
        self.assertIn("收藏增长 Top 3", md)
        self.assertIn("a：+14 藏", md)


if __name__ == "__main__":
    unittest.main(verbosity=2)
