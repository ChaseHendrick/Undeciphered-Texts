"""The fullest row with an empty cell. Not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_heavy import heavy_report
from engine.solvers.dagapeyeff import consider_heavy


class DagapeyeffHeavyTest(unittest.TestCase):
    def test_the_row_is_rare_and_the_column_is_not(self) -> None:
        report = heavy_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["row_full"], 56)
        self.assertEqual(report["row_open"], 80)
        self.assertEqual(report["column_full"], 46)
        self.assertEqual(report["control_row_full"], 26)
        self.assertEqual(
            (report["row_numerator"], report["row_denominator"]),
            (
                49457625028435544158345552750235855398188499,
                1830195262429003541521826002942669214789351708376,
            ),
        )
        self.assertEqual(
            (report["column_numerator"], report["column_denominator"]),
            (
                1328866302093932338657983518057960012398,
                1732713715827559446565946859854543934657,
            ),
        )
        row_rate = report["row_numerator"] / report["row_denominator"]
        column_rate = report["column_numerator"] / report["column_denominator"]
        control_rate = report["control_numerator"] / report["control_denominator"]
        self.assertLess(row_rate, 1 / 37005)
        self.assertLess(row_rate, 0.05)
        self.assertGreater(column_rate, 0.05)
        self.assertLess(control_rate, 0.01)
        claim = consider_heavy()
        self.assertFalse(claim["heavy_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
