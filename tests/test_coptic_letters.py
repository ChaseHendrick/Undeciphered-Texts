"""Known-word check for the Coptic letter reader.

The word under test is Sahidic U+2CA3 U+2CB1 U+2C99 U+2C89, romanized r-macron-o (U+014D),
glossed "human, person" on the Wiktionary page for that spelling
(checked 2026-10-02). This does not claim a reading of an undeciphered script.
"""

from __future__ import annotations

import unittest
import hashlib
import json
from pathlib import Path

from engine.coptic_letters import ROME, ROME_CAPITAL, lookup, read_letters, read_word


class CopticLetterReaderTest(unittest.TestCase):
    def test_rome_letters_and_gloss(self) -> None:
        self.assertEqual([ord(ch) for ch in ROME], [0x2CA3, 0x2CB1, 0x2C99, 0x2C89])
        reading = read_word(ROME)
        self.assertTrue(reading.all_letters_known)
        self.assertEqual(
            [item.name for item in reading.letters],
            [
                "COPTIC SMALL LETTER RO",
                "COPTIC SMALL LETTER OOU",
                "COPTIC SMALL LETTER MI",
                "COPTIC SMALL LETTER EIE",
            ],
        )
        self.assertEqual(
            [item.codepoint for item in reading.letters],
            ["U+2CA3", "U+2CB1", "U+2C99", "U+2C89"],
        )
        self.assertIsNotNone(reading.lexeme)
        assert reading.lexeme is not None
        self.assertEqual(reading.lexeme.word, ROME)
        self.assertEqual(reading.lexeme.romanization, "r\u014dme")
        self.assertEqual(reading.lexeme.gloss, "human, person")
        self.assertEqual(reading.lexeme.pos, "noun")
        self.assertEqual(
            reading.lexeme.source_url,
            "https://en.wiktionary.org/wiki/" + ROME,
        )
        self.assertIn("pageID=294", reading.lexeme.bibliography)

    def test_capital_spelling_finds_same_entry(self) -> None:
        self.assertEqual(
            [ord(ch) for ch in ROME_CAPITAL], [0x2CA2, 0x2CB0, 0x2C98, 0x2C88]
        )
        hit = lookup(ROME_CAPITAL)
        self.assertIsNotNone(hit)
        assert hit is not None
        self.assertEqual(hit.word, ROME)
        self.assertEqual(hit.gloss, "human, person")

    def test_anok_and_snau(self) -> None:
        anok = lookup("\u2c81\u2c9b\u2c9f\u2c95")
        snau = lookup("\u2ca5\u2c9b\u2c81\u2ca9")
        self.assertIsNotNone(anok)
        self.assertIsNotNone(snau)
        assert anok is not None and snau is not None
        self.assertEqual(anok.romanization, "anok")
        self.assertEqual(anok.gloss, "I")
        self.assertTrue(anok.source_url.endswith("\u2c81\u2c9b\u2c9f\u2c95"))
        self.assertEqual(snau.romanization, "snau")
        self.assertEqual(snau.gloss, "two")
        self.assertTrue(snau.source_url.endswith("\u2ca5\u2c9b\u2c81\u2ca9"))

    def test_non_coptic_sign_is_unread(self) -> None:
        letters = read_letters(ROME[0] + "?")
        self.assertEqual(len(letters), 2)
        self.assertTrue(letters[0].known)
        self.assertEqual(letters[0].codepoint, "U+2CA3")
        self.assertFalse(letters[1].known)
        self.assertEqual(letters[1].reason, "not_coptic_letter")
        reading = read_word("?")
        self.assertIsNone(reading.lexeme)
        self.assertFalse(reading.all_letters_known)



CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "coptic_letters_certificate.json"


class CopticCertificateTest(unittest.TestCase):
    """Certificate checks a cited known text/gloss, not an unknown script."""

    def test_certificate_matches_known_text_hash(self) -> None:
        cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(cert["tool_name"], "coptic-letters")
        known = cert["known_text"]
        digest = hashlib.sha256(known.encode("utf-8")).hexdigest()
        self.assertEqual(digest, cert["known_text_sha256"])
        reading = read_word(cert["input"])
        assert reading.lexeme is not None
        self.assertEqual(reading.lexeme.gloss, known)
        self.assertEqual(reading.lexeme.source_url, cert["source_url"])
        self.assertIn("not an unknown script", cert["note"].lower())


if __name__ == "__main__":
    unittest.main()
