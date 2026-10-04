"""Keyword panel on Kryptos K4 must not emit a claimed plaintext.

The keywords are the published K1 and K2 keys plus the KRYPTOS alphabet
keyword. A crib match is not a K4 decipherment.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from engine.k4_keyword_panel import KEYWORDS, keyword_panel
from engine.solvers.k4_attempt import cribs_in_place


ROOT = Path(__file__).resolve().parents[1]


class K4KeywordPanelTest(unittest.TestCase):
    def test_panel_stays_unsolved_and_counts_keywords(self) -> None:
        keyed = (ROOT / "tests" / "test_keyed_vigenere.py").read_text(encoding="utf-8")
        attempt = (ROOT / "engine" / "solvers" / "k4_attempt.py").read_text(encoding="utf-8")
        self.assertIn('key="PALIMPSEST"', keyed)
        self.assertIn('key="ABSCISSA"', keyed)
        self.assertIn('KEYED_ALPHABET_KEYWORD = "KRYPTOS"', attempt)
        self.assertEqual(KEYWORDS, ("PALIMPSEST", "ABSCISSA", "KRYPTOS"))

        report = keyword_panel()
        self.assertIs(report.solved, False)
        self.assertIsNone(report.claimed_plaintext)
        self.assertFalse(hasattr(report, "plaintext"))
        self.assertEqual(
            tuple(tally.method for tally in report.tallies),
            ("playfair", "porta", "gromark", "two-square"),
        )
        expected = {
            "playfair": len(KEYWORDS),
            "porta": len(KEYWORDS),
            "gromark": len(KEYWORDS),
            "two-square": len(KEYWORDS) * (len(KEYWORDS) - 1),
        }
        self.assertEqual(expected["two-square"], 6)
        for tally in report.tallies:
            self.assertEqual(tally.tried + tally.rejected, expected[tally.method])
        self.assertLessEqual(len(report.unverified), 20)
        for item in report.unverified:
            self.assertEqual(item.status, "unverified")
            self.assertTrue(cribs_in_place(item.candidate))
            self.assertNotEqual(report.claimed_plaintext, item.candidate)


if __name__ == "__main__":
    unittest.main()
