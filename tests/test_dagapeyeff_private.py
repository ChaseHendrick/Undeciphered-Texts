"""Five symbols never leave the last column. That is not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_private import private_report


class DagapeyeffPrivateTest(unittest.TestCase):
    def test_five_symbols_live_only_in_the_last_column(self) -> None:
        report = private_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["trials"], 20000)
        self.assertEqual(
            report["private"],
            (("92", 13, 3), ("93", 13, 2), ("04", 13, 1), ("71", 13, 1), ("94", 13, 1)),
        )
        self.assertEqual(report["private_mass"], 8)
        self.assertEqual(report["mass_by_column"][13], 8)
        self.assertEqual(sum(report["mass_by_column"][:13]), 0)
        self.assertEqual(report["as_high"], 0)
        self.assertIs(report["all_in_column_13"], True)
        self.assertIs(report["all_mod_14_is_13"], True)
        self.assertIs(report["all_mod_7_is_6"], True)


if __name__ == "__main__":
    unittest.main()
