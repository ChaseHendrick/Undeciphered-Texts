"""Real 196-letter prose windows against the cells' letter counts."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_corpus import corpus_report
from engine.solvers.dagapeyeff import consider_corpus


class DagapeyeffCorpusTest(unittest.TestCase):
    def test_no_real_window_has_all_three_properties(self) -> None:
        report = corpus_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["windows"], 479051)
        self.assertEqual(report["cell_chi_square"], 34.23)
        self.assertEqual(report["windows_as_flat"], 94)
        self.assertEqual(report["windows_as_narrow"], 192)
        self.assertEqual(report["windows_all_three"], 0)
        self.assertEqual(report["closest_sorted_distance"], 16)
        claim = consider_corpus()
        self.assertFalse(claim["corpus_allowed"])


if __name__ == "__main__":
    unittest.main()
