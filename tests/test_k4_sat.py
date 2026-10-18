"""K4 SAT encoding: agrees with the Z3 module, and MaxSAT counts planted errors."""

from __future__ import annotations

import importlib.util
import unittest

_HAS_SAT = importlib.util.find_spec("pysat") is not None
_HAS_Z3 = importlib.util.find_spec("z3") is not None

# Joint results of engine.k4_alphabet_csp on K4, periods and lags 1 to 32.
_Z3_SAT = {
    "q3-vigenere": {27, 28, 29, 30},
    "q1": {13, 16, 19, 23, 24, 26, 27, 28, 29, 30, 31, 32},
    "q4": {8, 13, 16, 19, 20, 23, 24, 26, 27, 28, 29, 30, 31, 32},
    "q3-ct-autokey": {8, 24},
}


@unittest.skipUnless(_HAS_SAT, "optional python-sat not installed")
class K4SatTest(unittest.TestCase):
    def test_matches_the_z3_scan(self) -> None:
        from engine.k4_sat import check

        for family, sat in _Z3_SAT.items():
            for period in range(1, 33):
                expected = "sat" if period in sat else "unsat"
                self.assertEqual(check(family, period), expected, (family, period))

    @unittest.skipUnless(_HAS_Z3, "planted texts come from the Z3 module")
    def test_planted_texts_fit_and_one_error_costs_one_drop(self) -> None:
        from engine.k4_alphabet_csp import planted
        from engine.k4_sat import FAMILIES, check, min_drops

        for family in FAMILIES:
            text = planted(family, 7, seed=7 + len(family))
            self.assertEqual(check(family, 7, text), "sat", family)
            self.assertEqual(min_drops(family, 7, text)["drops"], 0, family)
            # A wrong ciphertext letter at a clue position is one dropped letter at most.
            broken = text[:66] + ("A" if text[66] != "A" else "B") + text[67:]
            self.assertLessEqual(min_drops(family, 7, broken)["drops"], 1, family)

    def test_k4_needs_letters_dropped_at_period_seven(self) -> None:
        from engine.k4_sat import drop_scan, min_drops

        self.assertEqual(min_drops("q3-vigenere", 7)["drops"], 4)
        report = drop_scan(families=("q2",), periods=(3,), controls=1)
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
