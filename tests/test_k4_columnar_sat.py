"""Columnar SAT model: agrees with branch and bound, finds planted wide keys."""

from __future__ import annotations

import importlib.util
import random
import shutil
import unittest

from engine.k4_gromark_obstruction import CRIB_SPANS

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
_READY = importlib.util.find_spec("pysat") is not None and bool(shutil.which("cc") or shutil.which("gcc"))


@unittest.skipUnless(_READY, "needs python-sat and a C compiler")
class K4ColumnarSatTest(unittest.TestCase):
    def test_agrees_with_branch_and_bound(self) -> None:
        from engine.k4_columnar_bnb import search
        from engine.k4_columnar_sat import solve
        from engine.k4_transposition_sub import setup

        for n in (97, 98):
            s = setup(n)
            for w in (6, 11):
                for d in (0, 1):
                    for comp in (0, 1):
                        for p in (5, 19, 20):
                            for v in (0, 3):
                                want = search(s, w, d, comp, p, v)["leaves"] > 0
                                self.assertEqual(solve(s, w, d, comp, p, v)["sat"], want, (n, w, d, comp, p, v))

    def test_planted_wide_key_is_found_and_verified(self) -> None:
        from engine.k4_columnar_sat import solve
        from engine.k4_transposition_sub import columnar_perm, encipher, setup, shift_alphabets

        rng = random.Random(18)
        for direction, comp in ((0, 0), (1, 1)):
            plain = [rng.randrange(26) for _ in range(97)]
            for start, word in CRIB_SPANS:
                plain[start : start + len(word)] = [LETTERS.index(ch) for ch in word]
            order = list(range(18))
            rng.shuffle(order)
            key = [rng.randrange(26) for _ in range(7)]
            perm = columnar_perm(97, order, direction)
            cipher = "".join(LETTERS[x] for x in encipher(plain, perm, comp, shift_alphabets(2, key)))
            self.assertTrue(solve(setup(97, cipher), 18, direction, comp, 7, 2)["sat"])

    def test_report_claims_nothing(self) -> None:
        from engine.k4_columnar_sat import scan

        report = scan([4], periods=(2,), variants=(0,), lengths=(97,))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
