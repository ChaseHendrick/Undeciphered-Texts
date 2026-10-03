"""Known-word check for the Coptic letter reader.

The word under test is Sahidic ⲓⲱⲙⲉ, romanized rōme, glossed "human, person"
on https://en.wiktionary.org/wiki/ⲓⲱⲙⲉ (checked 2026-10-02). This does not
claim a reading of an undeciphered script.
"""

from __future__ import annotations

import unittest

from engine.coptic_letters import lookup, read_letters, read_word


class CopticLetterReaderTest(unittest.TestCase):
    def test_rome_letters_and_gloss(self) -> None:
        reading = read_word("ⲓⲱⲙⲉ")
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
        self.assertEqual(reading.lexeme.romanization, "rōme")
        self.assertEqual(reading.lexeme.gloss, "human, person")
        self.assertEqual(reading.lexeme.pos, "noun")
        self.assertEqual(
            reading.lexeme.source_url,
            "https://en.wiktionary.org/wiki/ⲓⲱⲙⲉ",
        )
        self.assertIn("pageID=294", reading.lexeme.bibliography)

    def test_capital_spelling_finds_same_entry(self) -> None:
        hit = lookup("ⲢⲰⲘⲈ")
        self.assertIsNotNone(hit)
        assert hit is not None
        self.assertEqual(hit.word, "ⲓⲱⲙⲉ")
        self.assertEqual(hit.gloss, "human, person")

    def test_anok_and_snau(self) -> None:
        anok = lookup("ⲁⲛⲟⲕ")
        snau = lookup("ⲥⲛⲁⲩ")
        self.assertIsNotNone(anok)
        self.assertIsNotNone(snau)
        assert anok is not None and snau is not None
        self.assertEqual(anok.romanization, "anok")
        self.assertEqual(anok.gloss, "I")
        self.assertEqual(anok.source_url, "https://en.wiktionary.org/wiki/ⲁⲛⲟⲕ")
        self.assertEqual(snau.romanization, "snau")
        self.assertEqual(snau.gloss, "two")
        self.assertEqual(snau.source_url, "https://en.wiktionary.org/wiki/ⲥⲛⲁⲩ")

    def test_non_coptic_sign_is_unread(self) -> None:
        letters = read_letters("ⲓ?")
        self.assertEqual(len(letters), 2)
        self.assertTrue(letters[0].known)
        self.assertFalse(letters[1].known)
        self.assertEqual(letters[1].reason, "not_coptic_letter")
        reading = read_word("?")
        self.assertIsNone(reading.lexeme)
        self.assertFalse(reading.all_letters_known)


if __name__ == "__main__":
    unittest.main()
