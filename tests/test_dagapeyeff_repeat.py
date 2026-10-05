"""A second run of the same cell is not rare once a long run is required."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_repeat import repeat_report
from engine.solvers.dagapeyeff import consider_repeat


class DagapeyeffRepeatTest(unittest.TestCase):
    def test_the_second_run_needs_the_long_run(self) -> None:
        report = repeat_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["lines"], 1)
        self.assertEqual(report["hits"], [{
            "axis": "column",
            "index": 3,
            "cell": "82",
            "lengths": [2, 1, 3],
        }])
        self.assertEqual(report["draws"], 20000)
        self.assertEqual(report["as_high"], 956)
        self.assertLess(report["as_high"] / report["draws"], 0.05)
        self.assertEqual(report["vertical_runs"], 10855)
        self.assertEqual(report["vertical_and_feature"], 724)
        self.assertGreaterEqual(report["vertical_and_feature"] / report["vertical_runs"], 0.05)
        self.assertEqual(report["any_long"], 15871)
        self.assertEqual(report["any_and_feature"], 956)
        self.assertGreaterEqual(report["any_and_feature"] / report["any_long"], 0.05)
        self.assertIs(report["allowed"], False)
        claim = consider_repeat()
        self.assertIs(claim["repeat_allowed"], False)
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
