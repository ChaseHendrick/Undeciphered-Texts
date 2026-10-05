"""A palindrome fills the span of a spaced triple."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_span import span_report
from engine.solvers.dagapeyeff import consider_span


class DagapeyeffSpanTest(unittest.TestCase):
    def test_a_palindrome_fills_the_span(self) -> None:
        report = span_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["span_count"], 1)
        span = report["spans"][0]
        self.assertEqual(span["cell"], "62")
        self.assertEqual(span["axis"], "row")
        self.assertEqual(span["index"], 11)
        self.assertEqual(span["seats"], [6, 8, 10])
        self.assertEqual(span["span"], [6, 10])
        self.assertEqual(span["echo"], 0)
        self.assertEqual(span["window"], ["91", "64", "81", "64", "91"])
        self.assertEqual(report["draws"], 20000)
        self.assertEqual(report["as_many"], 782)
        self.assertLess(report["as_many"] / report["draws"], 0.05)
        self.assertIs(report["allowed"], True)
        claim = consider_span()
        self.assertIs(claim["span_allowed"], True)
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
