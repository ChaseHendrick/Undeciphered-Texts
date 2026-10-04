"""The digits' own split, with no language assumed."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_frames import frame_report


class DagapeyeffFramesTest(unittest.TestCase):
    def test_one_digit_breaks_an_otherwise_strict_split(self) -> None:
        report = frame_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["digits"], 395)
        self.assertEqual(report["even_alphabet"], "06789")
        self.assertEqual(report["odd_alphabet_without_overlap"], "12345")
        self.assertEqual(report["overlap"], "0")
        self.assertEqual(report["bad_indexes"], (393,))
        self.assertEqual(report["zero_indexes"], (194, 392, 393, 394))
        self.assertEqual(report["legal_pairs"], 196)
        self.assertEqual(report["trials"], 40000)
        self.assertEqual(report["shuffles_as_clean"], 0)
        self.assertEqual(report["mutual_information"], 0.5706)
        self.assertEqual(report["shuffles_as_predictable"], 16611)


if __name__ == "__main__":
    unittest.main()
