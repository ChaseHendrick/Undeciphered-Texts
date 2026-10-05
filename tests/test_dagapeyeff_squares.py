"""One cell that shares the count 17 prefers one color of the board."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_squares import squares_report
from engine.solvers.dagapeyeff import consider_squares


class DagapeyeffSquaresTest(unittest.TestCase):
    def test_one_tied_cell_prefers_one_color(self) -> None:
        report = squares_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["cells"], ["62", "75", "82", "85"])
        self.assertEqual(report["cell"], "62")
        self.assertEqual(report["even"], 3)
        self.assertEqual(report["odd"], 14)
        self.assertEqual(report["gap"], 11)
        self.assertEqual(report["detail"]["75"]["gap"], 1)
        self.assertEqual(report["detail"]["82"]["gap"], 3)
        self.assertEqual(report["detail"]["85"]["gap"], 1)
        self.assertEqual(report["draws"], 20000)
        self.assertEqual(report["as_split"], 723)
        self.assertLess(report["as_split"] / report["draws"], 0.05)
        self.assertIs(report["allowed"], True)
        claim = consider_squares()
        self.assertIs(claim["squares_allowed"], True)
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
