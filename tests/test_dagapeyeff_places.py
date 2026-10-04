"""One digit place from each group does not beat prose, or a shuffle."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_places import place_report
from engine.solvers.dagapeyeff import consider_places


class DagapeyeffPlaceTest(unittest.TestCase):
    def test_one_digit_place_is_ordinary(self) -> None:
        report = place_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["groups"], 78)
        self.assertEqual(report["places"], 5)
        self.assertEqual(report["places_on_square"], 5)
        self.assertEqual(report["best_place"], 4)
        self.assertEqual(report["best_quadgram"], -3.1598)
        self.assertEqual(report["prose_quadgram"], -2.5185)
        self.assertFalse(report["reaches_prose"])
        self.assertEqual(report["null_texts"], 80)
        self.assertEqual(report["shuffles_as_high"], 24)
        claim = consider_places()
        self.assertFalse(claim["places_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
