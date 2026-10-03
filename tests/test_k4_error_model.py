"""Ciphertext-error search on Kryptos K4 must not emit a claimed plaintext.

The bounds live in engine/solvers/k4_error_model.py and docs/k4-error-model.md.
This test locks the negative result. It does not treat a candidate as a solve.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from engine.solvers.k4_attempt import ENGLISH_CONTROL, K4_CIPHERTEXT
from engine.solvers.k4_error_model import (
    _shifted_spans,
    formulas_match_certified,
    search_k4_errors,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "k4-error-model.md"


class K4ErrorModelTest(unittest.TestCase):
    def test_search_does_not_emit_a_claimed_plaintext(self) -> None:
        report = search_k4_errors()
        self.assertEqual(report.result, "not solved")
        self.assertFalse(report.solved)
        self.assertIsNone(report.claimed_plaintext)
        self.assertFalse(hasattr(report, "plaintext"))
        self.assertEqual(report.unverified, ())
        for tally in report.tallies:
            self.assertEqual(tally.key_consistent, 0)
            self.assertEqual(tally.crib_consistent, 0)
            self.assertEqual(tally.bar_pass, 0)
        again = search_k4_errors()
        self.assertEqual(again.lines(), report.lines())
        self.assertIsNone(again.claimed_plaintext)
        self.assertEqual(again.unverified, ())

    def test_doc_states_the_negative_result_and_the_counts(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        self.assertNotIn("\u2014", text)
        self.assertNotIn("\u2013", text)
        self.assertIn("not solved", text)
        self.assertIn("No plaintext claimed.", text)
        self.assertIn("eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab", text)
        report = search_k4_errors()
        for line in report.lines():
            self.assertIn(line, text)
        self.assertEqual(
            report.ciphertext_sha256,
            "eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab",
        )
        self.assertNotIn("claimed plaintext:", text.lower())

    def test_bounds_and_certified_maps(self) -> None:
        self.assertTrue(formulas_match_certified())
        self.assertEqual(len(K4_CIPHERTEXT), 97)
        self.assertEqual(len(ENGLISH_CONTROL), 97)
        # A deletion inside EAST (1-based 22) breaks that crib word.
        self.assertIsNone(_shifted_spans("del", 21))
        # A deletion before EAST shifts the tail and keeps the words.
        shifted = _shifted_spans("del", 0)
        self.assertIsNotNone(shifted)
        assert shifted is not None
        self.assertEqual(shifted[0][0], 20)
        self.assertEqual(shifted[0][2], "EAST")
        self.assertEqual(shifted[3][2], "CLOCK")


if __name__ == "__main__":
    unittest.main()
