"""Width 14 under a new seed does not beat shuffled cells."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_columnar14 import columnar14_report
from engine.solvers.dagapeyeff import consider_columnar14


class DagapeyeffColumnar14Test(unittest.TestCase):
    def test_most_shuffles_reach_the_cells(self) -> None:
        report = columnar14_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["draws"], 20)
        self.assertEqual(report["cells_per_letter"], -3.6146)
        self.assertEqual(report["plain_shuffles_as_high"], 13)
        self.assertEqual(report["kept_column_shuffles_as_high"], 10)
        claim = consider_columnar14()
        self.assertFalse(claim["columnar14_allowed"])


if __name__ == "__main__":
    unittest.main()
