"""The cells' order passes a no-message test that catches a keyed square and done columnar transposition."""

from __future__ import annotations

import unittest

import numpy as np

from engine.dagapeyeff_nomessage import dealings, nomessage_report, statistic_names, statistics
from engine.solvers.dagapeyeff import consider_nomessage


class DagapeyeffNoMessageTest(unittest.TestCase):
    def test_dealings_keep_fixed_places_and_counts(self) -> None:
        symbols = list(range(10)) * 3
        out = dealings(symbols, {0, 5}, 50, np.random.default_rng(1))
        self.assertTrue((out[:, 0] == 0).all() and (out[:, 5] == 5).all())
        self.assertTrue(all(sorted(row) == sorted(symbols) for row in out.tolist()))
        self.assertEqual(statistics(np.asarray([symbols])).shape, (1, len(statistic_names())))
        self.assertEqual(len(statistic_names()), 30)

    def test_the_cells_pass_where_the_test_has_power(self) -> None:
        report = nomessage_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(len(report["fixed_places"]), 8)
        self.assertGreater(report["cells"]["family_p"], 0.05)
        power = report["power"]
        self.assertGreaterEqual(power["keyed square"]["flagged"], 18)
        self.assertGreaterEqual(power["columnar 14 done"]["flagged"], 18)
        self.assertLessEqual(power["random transposition"]["flagged"], 3)
        self.assertFalse(consider_nomessage()["nomessage_allowed"])


if __name__ == "__main__":
    unittest.main()
