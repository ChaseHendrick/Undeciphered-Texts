"""The common cells are as even as a fair die, and English is not."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_core import cliff, core, core_report
from engine.solvers.dagapeyeff import consider_core


class DagapeyeffCoreTest(unittest.TestCase):
    def test_the_cliff_is_the_largest_drop(self) -> None:
        self.assertEqual(cliff([20, 17, 9, 3, 2, 1]), 3)
        self.assertEqual(cliff([5, 5, 5]), 3)
        found = core(["A"] * 10 + ["B"] * 10 + ["C"])
        self.assertEqual((found["distinct"], found["cliff"], found["mass"]), (3, 2, 20))
        self.assertEqual(found["chi"], 0.0)

    def test_the_core_is_flat_and_no_english_family_makes_it(self) -> None:
        report = core_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual((report["cells"], report["distinct"], report["cliff"], report["core_mass"]), (196, 18, 13, 188))
        self.assertAlmostEqual(report["core_chi"], 8.6596, places=4)
        self.assertEqual(report["die_as_flat"], 5442)
        self.assertEqual(report["english"]["both"], 0)
        self.assertEqual(report["english"]["draws"], 20000)
        self.assertEqual(report["exercise_cliff"], 19)
        self.assertGreater(report["exercise_core_chi"], report["core_chi"])
        by_family = {row["family"]: row["flat_full_core"] for row in report["families"]}
        self.assertEqual(len(by_family), 21)
        self.assertEqual(by_family["any transposition of a Polybius"], 0)
        self.assertEqual(by_family["playfair"], 0)
        self.assertEqual(by_family["running key"], 13)
        self.assertEqual(by_family["13 equal cells and a rare tail, no language"], 485)
        self.assertEqual(report["language_families_reaching_5_percent"], ["two cells per letter from 13, then a period-7 key"])
        period = report["core_period"]
        self.assertEqual((period["core_letters"], period["best_period"]), (188, 40))
        self.assertEqual((period["shuffles_as_high"], period["draws"]), (831, 2000))
        claim = consider_core()
        self.assertFalse(claim["core_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])
        self.assertIn("Refuse it", claim["learned"])


if __name__ == "__main__":
    unittest.main()
