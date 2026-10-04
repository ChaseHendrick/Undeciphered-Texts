"""Dictionary shapes do not prefer the printed order, or the regrouping."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_patterns import pattern_report
from engine.solvers.dagapeyeff import consider_patterns


class DagapeyeffPatternTest(unittest.TestCase):
    def test_shuffles_have_more_dictionary_shapes(self) -> None:
        report = pattern_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["shapes"], 4703)
        self.assertEqual(report["windows"], 940)
        self.assertEqual(report["printed_hits"], 423)
        self.assertEqual(report["down_hits"], 464)
        self.assertEqual(report["regrouped_hits"], 499)
        self.assertEqual(report["printed_null"], {"draws": 100000, "as_high": 92932, "below": 7068})
        self.assertEqual(report["down_null"], {"draws": 50000, "as_high": 32841, "below": 17159})
        self.assertEqual(report["regrouped_null"], {"draws": 50000, "as_high": 31687, "below": 18313})
        claim = consider_patterns()
        self.assertFalse(claim["pattern_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
