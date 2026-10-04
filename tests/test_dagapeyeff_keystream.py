"""A printed column is not the key for the rest of its row."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_keystream import keystream_report
from engine.solvers.dagapeyeff import consider_keystream


class DagapeyeffKeystreamTest(unittest.TestCase):
    def test_the_repetitive_column_is_not_a_key(self) -> None:
        report = keystream_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["columns"], 14)
        self.assertEqual(report["kept"], 182)
        self.assertEqual(report["best_column"], 9)
        self.assertEqual(report["best_rule"], "add")
        self.assertEqual(report["best_quadgram"], -3.645)
        self.assertEqual(report["fourth_column"], 3)
        self.assertEqual(report["fourth_quadgram"], -3.6947)
        self.assertEqual(report["prose_quadgram"], -2.5185)
        self.assertFalse(report["reaches_prose"])
        self.assertEqual(report["draws"], 80)
        self.assertEqual(report["best_shuffles_as_high"], 71)
        self.assertEqual(report["fourth_shuffles_as_high"], 21)
        claim = consider_keystream()
        self.assertFalse(claim["keystream_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
