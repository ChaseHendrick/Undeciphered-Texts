"""Four cells share a count and do not pile into one line."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_quartet import quartet_report
from engine.solvers.dagapeyeff import consider_quartet


class DagapeyeffQuartetTest(unittest.TestCase):
    def test_the_shared_count_is_spread_across_the_rows(self) -> None:
        report = quartet_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["cells"], ["62", "75", "82", "85"])
        self.assertEqual(report["count"], 17)
        self.assertEqual(report["copies"], 68)
        self.assertEqual(report["row_most"], 6)
        self.assertEqual(report["column_most"], 8)
        self.assertEqual(report["cap"], 6)
        self.assertEqual(report["draws"], 100000)
        self.assertEqual(report["as_even"], 4643)
        self.assertLess(report["as_even"] / report["draws"], 0.05)
        self.assertEqual(report["mode_cell"], ["81"])
        self.assertEqual(report["mode_as_even"], 76792)
        self.assertGreaterEqual(report["mode_as_even"] / report["draws"], 0.05)
        self.assertEqual(report["next_cells"], ["64", "74", "81", "83"])
        self.assertEqual(report["next_as_even"], 96962)
        self.assertGreaterEqual(report["next_as_even"] / report["draws"], 0.05)
        self.assertIs(report["allowed"], True)
        claim = consider_quartet()
        self.assertIs(claim["quartet_allowed"], True)
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
