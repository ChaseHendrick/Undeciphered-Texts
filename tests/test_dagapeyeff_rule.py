"""The book's dummy rule is a prediction about the residue, not a deletion to try."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_rule import book_residues, search_rule, worker_report


class DagapeyeffRuleTest(unittest.TestCase):
    def test_no_residue_is_a_filler(self) -> None:
        self.assertEqual(len(book_residues()), 12)
        reports = [worker_report(index) for index in range(12)]
        self.assertTrue(all(report["looks_like_filler"] is False for report in reports))
        self.assertTrue(all(report["claimed_plaintext"] is None for report in reports))
        self.assertEqual(reports[0]["distinct"], 15)

    def test_rival_stands(self) -> None:
        report = search_rule()
        self.assertIs(report["solved"], False)
        self.assertIs(report["confirms_hypothesis"], False)
        self.assertIs(report["rival_stands"], True)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["narrow_distinct"], 12)
        self.assertEqual(report["narrow_period"], 4)
        self.assertEqual(report["shuffle_as_narrow"], 214)
        self.assertEqual(report["peak_share"], 0.2041)
        self.assertEqual(report["shuffle_as_peaked"], 116)
        self.assertEqual(report["control_narrow_distinct"], 8)
        self.assertIs(report["any_filler"], False)


if __name__ == "__main__":
    unittest.main()
