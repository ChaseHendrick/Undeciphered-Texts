"""Two cells in one line are each equally spaced."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_twospace import twospace_report
from engine.solvers.dagapeyeff import consider_twospace


class DagapeyeffTwospaceTest(unittest.TestCase):
    def test_one_line_holds_two_spaced_triples(self) -> None:
        report = twospace_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["line_count"], 1)
        line = report["lines"][0]
        self.assertEqual(line["axis"], "column")
        self.assertEqual(line["index"], 2)
        self.assertEqual(line["cells"][0]["cell"], "82")
        self.assertEqual(line["cells"][0]["seats"], [0, 6, 12])
        self.assertEqual(line["cells"][0]["step"], 6)
        self.assertEqual(line["cells"][1]["cell"], "85")
        self.assertEqual(line["cells"][1]["seats"], [5, 8, 11])
        self.assertEqual(line["cells"][1]["step"], 3)
        self.assertEqual(report["draws"], 20000)
        self.assertEqual(report["as_many"], 740)
        self.assertLess(report["as_many"] / report["draws"], 0.05)
        self.assertIs(report["allowed"], True)
        claim = consider_twospace()
        self.assertIs(claim["twospace_allowed"], True)
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
