"""K4 in-place substitution on unknown alphabets, with planted-clue controls."""

from __future__ import annotations

import importlib.util
import unittest

_HAS_Z3 = importlib.util.find_spec("z3") is not None


@unittest.skipUnless(_HAS_Z3, "optional z3-solver not installed")
class K4AlphabetCspTest(unittest.TestCase):
    def test_k4_blocks_sample_periods_and_lags(self) -> None:
        from engine.k4_alphabet_csp import check

        for family, parameter in (("q3-vigenere", 8), ("q3-vigenere", 13), ("q3-beaufort", 8),
                                  ("q1", 8), ("q2", 13), ("q3-ct-autokey", 13), ("q3-pt-autokey", 42)):
            self.assertEqual(check(family, parameter), "unsat", (family, parameter))

    def test_planted_clues_are_never_blocked(self) -> None:
        from engine.k4_alphabet_csp import FAMILIES, check, planted

        for family in FAMILIES:
            for parameter in (3, 13):
                ciphertext = planted(family, parameter, seed=parameter + len(family))
                self.assertEqual(check(family, parameter, ciphertext), "sat", (family, parameter))

    def test_report_claims_nothing(self) -> None:
        from engine.k4_alphabet_csp import scan

        report = scan(families=("q2",), max_parameter=2)
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])


class K4HillRowsTest(unittest.TestCase):
    def test_every_size_alignment_and_numbering_is_excluded(self) -> None:
        from engine.k4_hill_rows import scan

        report = scan()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(len(report["rows"]), 36)
        self.assertEqual({row["status"] for row in report["rows"]}, {"unsat"})

    def test_planted_hill_keys_are_never_excluded(self) -> None:
        from engine.k4_hill_rows import NUMBERINGS, check, planted

        for numbering in NUMBERINGS:
            for n in (2, 3, 4):
                for alignment in range(n):
                    ciphertext = planted(n, alignment, seed=n * 10 + alignment, numbering=numbering)
                    self.assertEqual(check(n, alignment, numbering, ciphertext)["status"], "sat",
                                     (numbering, n, alignment))

    def test_three_by_three_fit_predicts_the_reserved_clue(self) -> None:
        from engine.k4_hill_rows import held_back, planted

        # Power: with a planted key, EASTNORTHEAST alone pins BERLINCLOCK.
        result = held_back(3, 1, "A-Z", planted(3, 1, seed=31))
        self.assertEqual((result["right"], result["wrong"]), (11, 0))


if __name__ == "__main__":
    unittest.main()
