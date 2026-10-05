"""The two runs of three start in the same printed column."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_triples import triples_report
from engine.solvers.dagapeyeff import consider_triples


class DagapeyeffTriplesTest(unittest.TestCase):
    def test_the_two_runs_share_a_starting_column(self) -> None:
        report = triples_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["runs"], 2)
        self.assertEqual(report["cells"], ["75", "63"])
        self.assertEqual(report["rows"], [2, 6])
        self.assertEqual(report["columns"], [10, 10])
        self.assertEqual(report["lengths"], [3, 3])
        self.assertEqual(report["shared_starts"], 2)
        self.assertEqual(report["as_aligned"], 430)
        self.assertEqual(report["draws"], 20000)
        self.assertLess(report["as_aligned"] / report["draws"], 0.05)
        claim = consider_triples()
        self.assertTrue(claim["triples_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
