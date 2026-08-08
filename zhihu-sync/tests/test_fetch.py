#!/usr/bin/env python3
"""fetch_contents.py 纯函数单元测试（不调用 CLI，不消耗配额）。

用法: python3 tests/test_fetch.py
"""
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
for _sub in ("src", "scripts"):
    if os.path.isdir(os.path.join(ROOT, _sub)):
        sys.path.insert(0, os.path.join(ROOT, _sub))
        break

import fetch_contents  # noqa: E402


def item(url, like=1):
    return {"Url": url, "Title": url, "LikeCount": like}


class TestMergeItems(unittest.TestCase):
    def test_merge_new_and_old(self):
        cached = [item("https://zhuanlan.zhihu.com/p/1", like=5)]
        batch = [item("https://zhuanlan.zhihu.com/p/2", like=1),
                 item("https://zhuanlan.zhihu.com/p/1", like=8)]  # 旧条目数据更新
        merged, new_count, hit_old = fetch_contents.merge_items(cached, batch)
        self.assertEqual(len(merged), 2)
        self.assertEqual(new_count, 1)
        self.assertTrue(hit_old)
        by_url = {it["Url"]: it for it in merged}
        self.assertEqual(by_url["https://zhuanlan.zhihu.com/p/1"]["LikeCount"], 8)

    def test_all_new_no_hit(self):
        cached = [item("https://zhuanlan.zhihu.com/p/1")]
        batch = [item("https://zhuanlan.zhihu.com/p/2"), item("https://zhuanlan.zhihu.com/p/3")]
        merged, new_count, hit_old = fetch_contents.merge_items(cached, batch)
        self.assertEqual(len(merged), 3)
        self.assertEqual(new_count, 2)
        self.assertFalse(hit_old)

    def test_duplicate_within_batch(self):
        cached = []
        batch = [item("https://zhuanlan.zhihu.com/p/1", like=1),
                 item("https://zhuanlan.zhihu.com/p/1", like=9)]
        merged, new_count, hit_old = fetch_contents.merge_items(cached, batch)
        self.assertEqual(len(merged), 1)
        self.assertEqual(new_count, 1)
        self.assertTrue(hit_old)  # 批内重复视作命中旧条目
        self.assertEqual(merged[0]["LikeCount"], 9)


if __name__ == "__main__":
    unittest.main(verbosity=2)
