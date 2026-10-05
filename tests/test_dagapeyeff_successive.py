"""The three cells that appear once sit in successive rows."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_successive import successive_report
from engine.solvers.dagapeyeff import consider_successive


class DagapeyeffSuccessiveTest(unittest.TestCase):
    def test_singleton_rows_are_successive(self) -> None:
        report = successive_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["rows"], [6, 7, 8])
        self.assertEqual(
            [(item["cell"], item["column"]) for item in report["cells"]],
            [("04", 13), ("94", 13), ("71", 13)],
        )
        self.assertIs(report["successive"], True)
        self.assertEqual(report["choices"], 364)
        self.assertEqual(report["successive_choices"], 12)
        self.assertLess(report["successive_choices"] / report["choices"], 0.05)
        self.assertIs(report["allowed"], True)
        claim = consider_successive()
        self.assertIs(claim["successive_allowed"], True)
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
