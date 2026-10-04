"""Running-key K4 check must not emit a claimed plaintext."""

from __future__ import annotations

import unittest

from engine.alphabet import letters_only
from engine.k4_running_key import search_k4_running_key
from engine.solvers.columnar import KRYPTOS_K3_PLAINTEXT


class K4RunningKeyTest(unittest.TestCase):
    def test_search_does_not_claim_a_plaintext(self) -> None:
        report = search_k4_running_key()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        key_letters = len(letters_only(KRYPTOS_K3_PLAINTEXT))
        k3 = next(
            row for row in report["tallies"] if row["key"] == "KRYPTOS_K3_PLAINTEXT"
        )
        self.assertEqual(k3["offsets"], max(0, key_letters - 96))
        self.assertEqual(k3["tried"], k3["offsets"])
        self.assertGreater(k3["offsets"], 0)
        self.assertLessEqual(len(report["unverified"]), 20)
        for item in report["unverified"]:
            self.assertEqual(item["status"], "unverified")
        k1 = next(
            row
            for row in report["skipped"]
            if row["key"] == "PUBLISHED_K1_PLAINTEXT"
        )
        self.assertLess(k1["letters"], 97)
        self.assertIn("shorter than 97", k1["reason"])


if __name__ == "__main__":
    unittest.main()
