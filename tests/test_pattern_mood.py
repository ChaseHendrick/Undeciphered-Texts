"""Pattern-and-mood labels on synthetic sheets.

A tight repeating lattice is dense/rhythmic. A sparse asymmetric sheet is open.
The report describes pattern only and must not carry linguistic plaintext.
"""

from __future__ import annotations

import json
import unittest
from dataclasses import asdict

from engine.pattern_mood import (
    DISCLAIMER,
    MoodReport,
    analyze_sheet,
    analyze_sign_stream,
    make_sparse_asymmetric_sheet,
    make_tight_repeating_sheet,
    mood_from_measures,
    report_to_dict,
)


class PatternMoodTest(unittest.TestCase):
    def test_tight_repeating_sheet_is_dense_rhythmic(self) -> None:
        sheet = make_tight_repeating_sheet()
        report = analyze_sheet(sheet)

        self.assertEqual(report.mood, "dense/rhythmic")
        self.assertGreaterEqual(report.repeat_rhythm, 0.75)
        self.assertLessEqual(report.spacing, 2.5)
        self.assertGreater(report.mark_count, 20)
        self.assertEqual(report.disclaimer, DISCLAIMER)

    def test_sparse_asymmetric_sheet_is_open(self) -> None:
        sheet = make_sparse_asymmetric_sheet()
        report = analyze_sheet(sheet)

        self.assertEqual(report.mood, "open")
        self.assertGreaterEqual(report.spacing, 8.0)
        self.assertLessEqual(report.symmetry, 0.25)
        self.assertLess(report.repeat_rhythm, 0.5)
        self.assertEqual(report.mark_count, 4)
        self.assertEqual(report.disclaimer, DISCLAIMER)

    def test_mood_uses_only_measurements(self) -> None:
        self.assertEqual(mood_from_measures(0.9, 0.0, 2.0), "dense/rhythmic")
        self.assertEqual(mood_from_measures(0.1, 0.0, 20.0), "open")
        self.assertEqual(mood_from_measures(0.2, 0.9, 4.0), "mixed")

    def test_sign_stream_repeat_and_no_plaintext(self) -> None:
        report = analyze_sign_stream(list("ABABABABABAB"))
        self.assertIsInstance(report, MoodReport)
        self.assertEqual(report.mood, "dense/rhythmic")
        self.assertGreaterEqual(report.repeat_rhythm, 0.75)

        payload = report_to_dict(report)
        self.assertNotIn("plaintext", payload)
        self.assertNotIn("reading", payload)
        self.assertNotIn("transcription", payload)
        encoded = json.dumps(payload)
        self.assertNotIn("ABAB", encoded)
        self.assertNotIn("plaintext", asdict(report))

    def test_disclaimer_refuses_unsolved_texts(self) -> None:
        text = analyze_sheet(make_tight_repeating_sheet()).disclaimer.lower()
        self.assertIn("voynich", text)
        self.assertIn("rongorongo", text)
        self.assertIn("unsolved", text)
        self.assertIn("plaintext", text)
        self.assertIn("not a decipherment", text)


if __name__ == "__main__":
    unittest.main()
