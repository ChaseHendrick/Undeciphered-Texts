"""Columnar branch and bound: agrees with full enumeration, finds planted keys."""

from __future__ import annotations

import random
import shutil
import unittest

from engine.k4_gromark_obstruction import CRIB_SPANS

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


@unittest.skipUnless(shutil.which("cc") or shutil.which("gcc"), "needs a C compiler")
class K4ColumnarBnbTest(unittest.TestCase):
    def test_counts_match_full_enumeration(self) -> None:
        from engine.k4_columnar_bnb import search
        from engine.k4_transposition_sub import run_columnar, setup

        for n in (97, 98):
            s = setup(n)
            for w in (5, 7):
                ref = run_columnar(s, widths=(w,), maxp=12, threads=1)["by_width"][w]
                for comp in (0, 1):
                    for p in range(1, 13):
                        for v in range(5):
                            got = sum(search(s, w, d, comp, p, v)["leaves"] for d in (0, 1))
                            self.assertEqual(got, int(ref[comp][p][1 if v == 4 else 2 + v]), (n, w, comp, p, v))

    def test_planted_width_twelve_key_is_found(self) -> None:
        from engine.k4_columnar_bnb import search
        from engine.k4_transposition_sub import columnar_perm, encipher, setup, shift_alphabets

        rng = random.Random(12)
        for comp in (0, 1):
            plain = [rng.randrange(26) for _ in range(97)]
            for start, word in CRIB_SPANS:
                plain[start : start + len(word)] = [LETTERS.index(ch) for ch in word]
            order = list(range(12))
            rng.shuffle(order)
            direction, p, variant = comp, 9, 2
            key = [rng.randrange(26) for _ in range(p)]
            perm = columnar_perm(97, order, direction)
            cipher = "".join(LETTERS[x] for x in encipher(plain, perm, comp, shift_alphabets(variant, key)))
            result = search(setup(97, cipher), 12, direction, comp, p, variant, cap=200000)
            self.assertGreaterEqual(result["leaves"], 1)
            self.assertIn(tuple(order), result["orders"])

    def test_k4_width_ten_has_no_survivor_to_period_twenty(self) -> None:
        from engine.k4_columnar_bnb import scan

        report = scan([10], periods=range(1, 21), lengths=(97,))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(sum(row["survivors"] for row in report["rows"]), 0)


if __name__ == "__main__":
    unittest.main()
