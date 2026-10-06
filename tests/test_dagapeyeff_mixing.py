"""Ciphers that mix letters never use as few symbols as the cells."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_mixing import bifid, mixing_report, running


class DagapeyeffMixingTest(unittest.TestCase):
    def test_bifid_and_running_key(self) -> None:
        self.assertEqual(bifid([0, 6], 2), [1, 1])
        self.assertEqual(running([0, 24], [6, 1]), [6, 20])

    def test_no_case_reaches_eighteen_symbols(self) -> None:
        report = mixing_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["cells_distinct"], 18)
        for name, row in report["cases"].items():
            self.assertEqual(row["reaching_cells"], 0, name)
            self.assertGreaterEqual(row["fewest_distinct"], 20, name)


if __name__ == "__main__":
    unittest.main()
