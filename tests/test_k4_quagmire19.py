"""Quagmire I, II, IV annealing: cipher round trip, a planted key found blind, K4 claims nothing."""

from __future__ import annotations

import random
import shutil
import unittest

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


@unittest.skipUnless(shutil.which("cc") or shutil.which("gcc"), "needs a C compiler")
class K4Quagmire19Test(unittest.TestCase):
    def test_round_trip_and_kernel_score(self) -> None:
        from engine import k4_quagmire19 as q
        from engine.language import get_model

        model = get_model()
        rng = random.Random(4)
        plain = q.plant_windows(1)[0]
        pool = q._keyword_pool()
        for family in ("q1", "q2", "q4"):
            for kind in ("random", "keyword"):
                p = q.plant(family, plain, kind, 19, rng, pool)
                self.assertEqual(q.decipher(family, p["cipher"], p["alpha_a"], p["alpha_b"], p["key"]), plain)
                got = q.score_key(family, p["cipher"], p["alpha_a"], p["alpha_b"], p["key"])
                self.assertEqual(got["plaintext"], plain)
                self.assertEqual(got["violations"], 0)
                self.assertAlmostEqual(got["lang"], model.full_score([LETTERS.index(c) for c in plain]), places=6)
        self.assertEqual(q.keyword_alphabet("KRYPTOS"), "KRYPTOSABCDEFGHIJLMNQUVWXZ")

    def test_planted_quagmire_one_is_recovered_blind(self) -> None:
        from engine import k4_quagmire19 as q

        plain = q.plant_windows(2, seed=5)[1]
        alpha = q.keyword_alphabet("KRYPTOS")
        key = [random.Random(9).randrange(26) for _ in range(7)]
        cipher = q.encipher("q1", plain, alpha, LETTERS, key)
        got = q.solve(cipher, "q1", period=7, restarts=2, iters=300_000, seed=3)
        best = got["feasible"]
        self.assertIsNotNone(best)
        right = sum(a == b for a, b in zip(best["plaintext"], plain))
        self.assertGreaterEqual(right, 90)
        truth = q.score_key("q1", cipher, alpha, LETTERS, key)["lang"]
        self.assertGreaterEqual(got["feasible_lang"], truth - 1.0)

    def test_k4_report_claims_nothing(self) -> None:
        from engine import k4_quagmire19 as q

        report = q.k4(("q1", "q2", "q4"), restarts=1, iters=20_000)
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(len(report["rows"]), 3)


if __name__ == "__main__":
    unittest.main()
