"""The aligned runs sit next to rare cells, beyond the alignment itself."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_contact import contact_report
from engine.solvers.dagapeyeff import consider_contact


class DagapeyeffContactTest(unittest.TestCase):
    def test_the_contact_is_not_the_alignment(self) -> None:
        report = contact_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["cells"], ["75", "63"])
        self.assertEqual(report["following"], ["93", "04"])
        self.assertEqual(report["shared"], 2)
        self.assertEqual(report["touched"], 2)
        self.assertEqual(report["draws"], 40000)
        self.assertEqual(report["aligned"], 866)
        self.assertEqual(report["contact"], 11)
        self.assertLess(report["contact"] / report["aligned"], 0.05)
        claim = consider_contact()
        self.assertTrue(claim["contact_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
