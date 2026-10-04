"""No bifid period reaches English, and the best one is ordinary."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_bifid import bifid_report
from engine.solvers.dagapeyeff import consider_bifid


class DagapeyeffBifidTest(unittest.TestCase):
    def test_the_best_period_is_ordinary(self) -> None:
        report = bifid_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["periods"], 196)
        self.assertEqual(report["draws"], 2000)
        self.assertEqual(report["period_scores"], 392000)
        self.assertEqual(report["identity_quad"], -3.6316)
        self.assertEqual(report["best_quad"], -3.4727)
        self.assertEqual(report["best_period"], 174)
        self.assertEqual(report["english_quad"], -1.553)
        self.assertFalse(report["reaches_english"])
        self.assertEqual(report["shuffles_as_high"], 1109)
        claim = consider_bifid()
        self.assertFalse(claim["bifid_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
