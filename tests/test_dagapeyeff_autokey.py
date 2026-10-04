"""An autokey on the square does not beat prose, or a shuffle."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_autokey import autokey_report
from engine.solvers.dagapeyeff import consider_autokey


class DagapeyeffAutokeyTest(unittest.TestCase):
    def test_the_autokey_is_worse_than_a_shuffle(self) -> None:
        report = autokey_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["rules"], 4)
        self.assertEqual(report["seeds"], 25)
        self.assertEqual(report["best_rule"], "plain-sub")
        self.assertEqual(report["best_quadgram"], -3.7495)
        self.assertEqual(report["prose_quadgram"], -2.5185)
        self.assertFalse(report["reaches_prose"])
        self.assertEqual(report["null_texts"], 40)
        self.assertEqual(report["shuffles_as_high"], 37)
        claim = consider_autokey()
        self.assertFalse(claim["autokey_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
