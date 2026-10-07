"""Periodic bijection bound on K4, with a planted-crib control."""

from __future__ import annotations

import random
import unittest

from engine.k4_gromark_obstruction import CRIB_SPANS
from engine.k4_periodic_bijection import scan_periods

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def _planted(period: int, seed: int) -> str:
    rng = random.Random(seed)
    plain = [rng.choice(LETTERS) for _ in range(97)]
    for start, word in CRIB_SPANS:
        plain[start : start + len(word)] = word
    alphabets = ["".join(rng.sample(LETTERS, 26)) for _ in range(period)]
    return "".join(alphabets[i % period][LETTERS.index(ch)] for i, ch in enumerate(plain))


class K4PeriodicBijectionTest(unittest.TestCase):
    def test_k4_blocks_known_periods(self) -> None:
        report = scan_periods(max_period=32)
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["blocked"], [1, 2, 3, 4, 5, 6, 7, 9, 10, 14, 15, 17, 21, 25])
        self.assertIn(8, report["open"])

    def test_planted_cribs_are_never_blocked(self) -> None:
        for period in range(1, 33):
            ciphertext = _planted(period, seed=period)
            self.assertNotIn(period, scan_periods(ciphertext, max_period=32)["blocked"])


if __name__ == "__main__":
    unittest.main()
