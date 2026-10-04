"""Counted once, the seam score is the private symbols."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_outgoing import outgoing_report


class DagapeyeffOutgoingTest(unittest.TestCase):
    def test_each_pair_is_counted_once(self) -> None:
        report = outgoing_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["trials"], 140000)
        self.assertEqual(report["full_mi"], 0.5706)
        self.assertEqual(report["outgoing_sum"], 0.5706)
        self.assertEqual(
            report["outgoing"],
            (
                0.0272, 0.0258, 0.0311, 0.0476, 0.0397, 0.0096, 0.0438,
                0.0305, 0.0357, 0.0275, 0.0311, 0.0362, 0.0894, 0.0953,
            ),
        )
        self.assertEqual(report["highest_column"], 13)
        self.assertEqual(report["highest"], 0.0953)
        self.assertEqual(report["second_column"], 12)
        self.assertEqual(report["second"], 0.0894)
        self.assertEqual(report["private_from_12"], 0.077)
        self.assertEqual(report["private_from_13"], 0.0839)
        self.assertEqual(report["as_high"], 7)


if __name__ == "__main__":
    unittest.main()
