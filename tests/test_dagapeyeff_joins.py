"""The last column's joins carry more of the order than a shuffle allows."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_joins import join_report


class DagapeyeffJoinsTest(unittest.TestCase):
    def test_the_last_column_and_its_neighbors_hold_the_score(self) -> None:
        report = join_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["trials"], 140000)
        self.assertEqual(report["full_mi"], 0.5706)
        self.assertEqual(
            report["shares"],
            (
                0.1226, 0.0531, 0.0569, 0.0787, 0.0873, 0.0493, 0.0534,
                0.0744, 0.0663, 0.0632, 0.0586, 0.0673, 0.1256, 0.1847,
            ),
        )
        self.assertEqual(report["highest_column"], 13)
        self.assertEqual(report["second_column"], 12)
        self.assertEqual(report["third_column"], 0)
        self.assertEqual(report["highest_share"], 0.1847)
        self.assertEqual(report["second_share"], 0.1256)
        self.assertEqual(report["third_share"], 0.1226)
        self.assertEqual(report["as_high"], 0)


if __name__ == "__main__":
    unittest.main()
