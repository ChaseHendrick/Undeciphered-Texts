"""Every short repeating shift on the square. Not a reading."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_add import add_report


class DagapeyeffAddTest(unittest.TestCase):
    def test_the_friendliest_shift_matches_a_shuffled_cipher(self) -> None:
        report = add_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["trials"], 666450)
        self.assertEqual(report["period2_keys"], 625)
        self.assertEqual(report["period3_keys"], 15625)
        self.assertEqual(report["period2_chi"], 6.43)
        self.assertEqual(report["period2_null_as_low"], 11)
        self.assertEqual(report["period3_chi"], 2.8)
        self.assertEqual(report["period3_null_as_low"], 1)
        self.assertEqual(report["period3_quadgram"], -3.5039)
        self.assertEqual(report["quadgram_null_as_high"], 5)
        self.assertEqual(report["unigram_quadgram_median"], -3.5864)
        self.assertEqual(report["prose_quadgram"], -2.5185)


if __name__ == "__main__":
    unittest.main()
