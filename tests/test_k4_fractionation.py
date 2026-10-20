"""Fractionating ciphers on K4: the 25-cell letter bound and trifid as SAT."""

from __future__ import annotations

import importlib.util
import random
import unittest

_HAS_SAT = importlib.util.find_spec("pysat") is not None


class K4SquareBoundTest(unittest.TestCase):
    def test_k4_uses_more_letters_than_a_square_holds(self) -> None:
        from engine.k4_fractionation import square_count_bound

        report = square_count_bound()
        self.assertEqual(report["distinct_letters"], 26)
        self.assertTrue(report["excluded"])
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])

    def test_a_bifid_ciphertext_never_exceeds_25_letters(self) -> None:
        from engine.k4_fractionation import square_count_bound
        from engine.solvers.bifid import bifid_encrypt

        rng = random.Random(25)
        text = "".join(rng.choice("ABCDEFGHIKLMNOPQRSTUVWXYZ") for _ in range(400))
        square = "".join(rng.sample("ABCDEFGHIKLMNOPQRSTUVWXYZ", 25))
        cipher = bifid_encrypt(text, square, 7)
        self.assertFalse(square_count_bound(cipher)["excluded"])


@unittest.skipUnless(_HAS_SAT, "optional python-sat not installed")
class K4TrifidSatTest(unittest.TestCase):
    def test_planted_trifid_texts_are_never_blocked(self) -> None:
        from engine.k4_fractionation import check, planted

        rng = random.Random(27)
        for trial in range(12):
            n = (97, 98)[trial % 2]
            period = rng.randint(2, n)
            self.assertEqual(check(period, n, planted(period, n, seed=500 + trial)), "sat", (n, period))

    def test_k4_is_blocked_at_sample_periods(self) -> None:
        from engine.k4_fractionation import check

        for n in (97, 98):
            for period in (2, 5, 7, 13, 41, 97):
                self.assertEqual(check(period, n), "unsat", (n, period))

    def test_report_claims_nothing(self) -> None:
        from engine.k4_fractionation import scan

        report = scan(periods=(5,), lengths=(97,))
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
