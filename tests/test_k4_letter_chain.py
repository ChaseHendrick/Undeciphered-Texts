"""Lagged-Fibonacci letter keys on K4: linear algebra and SAT cross-checked."""

from __future__ import annotations

import unittest


class LetterChainLinearTest(unittest.TestCase):
    def test_canonical_lag_excluded_at_short_primers_add_stream(self) -> None:
        from engine.k4_letter_chain import linear_probe

        for m in range(2, 11):
            report = linear_probe(m, rec_sign=1, apply_sign=1)
            self.assertEqual(report["answer"], "excluded", m)
            self.assertEqual(report["primers"], 0, m)
            self.assertIs(report["solved"], False)
            self.assertIsNone(report["claimed_plaintext"])

    def test_canonical_lag_excluded_at_short_primers_subtract_stream(self) -> None:
        from engine.k4_letter_chain import linear_probe

        for m in range(2, 12):
            report = linear_probe(m, rec_sign=-1, apply_sign=1)
            self.assertEqual(report["answer"], "excluded", m)

    def test_apply_senses_agree_on_k4(self) -> None:
        from engine.k4_letter_chain import linear_probe

        for m in range(2, 11):
            plus = linear_probe(m, rec_sign=1, apply_sign=1)
            minus = linear_probe(m, rec_sign=1, apply_sign=-1)
            self.assertEqual(plus["answer"], minus["answer"], m)

    def test_planted_primers_are_recovered(self) -> None:
        from engine.k4_letter_chain import linear_probe, planted

        for m, seed in ((3, 9), (5, 10), (13, 91)):
            text = planted(m, seed=seed)
            report = linear_probe(m, ciphertext=text["ciphertext"])
            self.assertEqual(report["answer"], "fits", m)
            self.assertGreaterEqual(report["primers"], 1, m)

    def test_bad_shapes_are_rejected(self) -> None:
        from engine.k4_letter_chain import linear_probe

        with self.assertRaises(ValueError):
            linear_probe(2, a=3, b=2)

    def test_fit_case_is_open_not_excluded(self) -> None:
        from engine.k4_letter_chain import linear_probe

        report = linear_probe(13, rec_sign=-1, apply_sign=1)
        self.assertEqual(report["answer"], "fits")
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])


class LetterChainSatTest(unittest.TestCase):
    def test_k4_unsat_at_sample_short_primers(self) -> None:
        from engine.k4_letter_chain import check

        for m in (2, 3):
            self.assertEqual(check(m), "unsat", m)
        self.assertEqual(check(10, rec_sign=-1), "unsat", "subtract-stream boundary")

    def test_planted_texts_are_satisfiable(self) -> None:
        from engine.k4_letter_chain import check, planted

        for m, seed in ((3, 9), (5, 10), (14, 92), (20, 93)):
            text = planted(m, seed=seed)
            self.assertEqual(check(m, ciphertext=text["ciphertext"]), "sat", m)

    def test_planted_subtract_and_generic_lag_shapes_are_satisfiable(self) -> None:
        """The rec sign applies to the b term only; planted controls pin that."""
        from engine.k4_letter_chain import check, planted

        for (m, a, b, rec, ap) in ((4, 2, 3, -1, 1), (6, 1, 4, -1, 1), (5, 1, 2, 1, -1)):
            text = planted(m, seed=500 + m, a=a, b=b, rec_sign=rec, apply_sign=ap)
            self.assertEqual(check(m, a, b, rec, ap, ciphertext=text["ciphertext"]), "sat", (m, a, b, rec, ap))

    def test_canonical_fit_matches_linear_algebra(self) -> None:
        from engine.k4_letter_chain import linear_probe

        for m, rec in ((11, 1), (13, -1)):
            report = linear_probe(m, rec_sign=rec)
            self.assertEqual(report["answer"], "fits", (m, rec))


if __name__ == "__main__":
    unittest.main()
