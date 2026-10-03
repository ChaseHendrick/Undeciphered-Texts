"""Bounded Kryptos K4 search must not emit a claimed plaintext.

The acceptance rule and the bounds live in engine/solvers/k4_attempt.py
and docs/k4-attempt.md. This test locks the negative result.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from engine.solvers.columnar import KRYPTOS_K3_PLAINTEXT
from engine.solvers.k4_attempt import (
    CRIBS,
    ENGLISH_CONTROL,
    K4_CIPHERTEXT,
    cribs_in_place,
    english_pass,
    search_k4,
)


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "k4-attempt.md"


class K4AttemptTest(unittest.TestCase):
    def test_search_does_not_emit_a_claimed_plaintext(self) -> None:
        report = search_k4()
        self.assertEqual(report.result, "not solved")
        self.assertFalse(report.solved)
        self.assertIsNone(report.claimed_plaintext)
        self.assertFalse(hasattr(report, "plaintext"))
        for tally in report.tallies:
            self.assertEqual(tally.crib_consistent, 0)
            self.assertEqual(tally.english_pass, 0)
        again = search_k4()
        self.assertEqual(again.lines(), report.lines())
        self.assertIsNone(again.claimed_plaintext)

    def test_doc_states_the_negative_result_and_the_counts(self) -> None:
        text = DOC.read_text(encoding="utf-8")
        self.assertNotIn("\u2014", text)
        self.assertNotIn("\u2013", text)
        self.assertIn("not solved", text)
        self.assertIn("No plaintext claimed.", text)
        self.assertIn("eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab", text)
        report = search_k4()
        for line in report.lines():
            self.assertIn(line, text)
        self.assertEqual(
            report.ciphertext_sha256,
            "eea813570c7f1fd3b34674e47b5c3da8948026f5cefee612a0b38ffaa515ceab",
        )

    def test_ciphertext_and_english_floor_are_the_predeclared_ones(self) -> None:
        self.assertEqual(len(K4_CIPHERTEXT), 97)
        self.assertTrue(K4_CIPHERTEXT.startswith("OBKR"))
        self.assertEqual(
            [(start, word, cipher) for start, word, cipher in CRIBS],
            [
                (22, "EAST", "FLRV"),
                (26, "NORTHEAST", "QQPRNGKSS"),
                (64, "BERLIN", "NYPVTT"),
                (70, "CLOCK", "MZFPK"),
            ],
        )
        self.assertEqual(ENGLISH_CONTROL, KRYPTOS_K3_PLAINTEXT[:97])
        self.assertEqual(len(ENGLISH_CONTROL), 97)
        self.assertTrue(english_pass(ENGLISH_CONTROL))
        self.assertFalse(cribs_in_place(K4_CIPHERTEXT))
        self.assertFalse(english_pass("A" * 97))


if __name__ == "__main__":
    unittest.main()
