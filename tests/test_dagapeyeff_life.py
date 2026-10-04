"""The life record is searchable, and the keys taken from it are not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_life import search_life, search_life_keys


class DagapeyeffLifeTest(unittest.TestCase):
    def test_search_finds_the_gazette_and_the_rejected_claim(self) -> None:
        service = search_life("87808")
        self.assertEqual(sorted(fact["id"] for fact in service), ["dismissal-1949", "raf-87808"])
        rejected = search_life("1969")
        self.assertEqual(rejected[0]["confidence"], "rejected")
        self.assertEqual(search_life("Rachel Wood")[0]["id"], "wife-rachel")
        self.assertEqual(search_life("forgot")[0]["id"], "forgot")

    def test_life_keys_are_not_a_reading(self) -> None:
        report = search_life_keys()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["facts"], 21)
        self.assertEqual(report["columns"]["1939"]["null_as_high"], 46)
        self.assertEqual(report["columns"]["later"]["null_as_high"], 8)
        self.assertEqual(report["running_digit"]["1939"]["best_digits"], "20051902")
        self.assertEqual(report["running_digit"]["1939"]["best_chi"], 21.64)
        self.assertEqual(report["running_digit"]["1939"]["null_as_low"], 71)
        self.assertEqual(report["running_digit"]["later"]["best_digits"], "87808")
        self.assertEqual(report["running_digit"]["later"]["best_chi"], 18.55)
        self.assertEqual(report["running_digit"]["later"]["null_as_low"], 66)
        self.assertNotIn("plaintext", report["running_digit"]["later"])


if __name__ == "__main__":
    unittest.main()
