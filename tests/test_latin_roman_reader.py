"""Latin is a known language: normalization and cited-lexicon glosses.

The published line is Caesar, De bello Gallico 1.1, as printed by T. Rice Holmes
(Oxford, 1914) on Perseus. Fetched 2026-10-02 from
https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.02.0002:book=1:chapter=1

Opening clause, before the comma: "Gallia est omnis divisa in partes tres".

This test does not claim an unknown script was read.
"""

from __future__ import annotations

import unittest

from engine.latin_reader import NOT_A_DECIPHERMENT, read_latin
from engine.roman_text import to_classical, to_epigraphic

# Holmes 1914 on Perseus, book 1 chapter 1, clause before the comma.
CAESAR_BG_1_1 = "Gallia est omnis divisa in partes tres"
CAESAR_BG_1_1_URL = (
    "https://www.perseus.tufts.edu/hopper/text?doc="
    "Perseus:text:1999.02.0002:book=1:chapter=1"
)
# Same clause with an interpunct between words, as in a diplomatic transcription.
CAESAR_INSCRIPTION = "GALLIA\u00b7EST\u00b7OMNIS\u00b7DIVISA\u00b7IN\u00b7PARTES\u00b7TRES"

DCC_CORE = "https://dcc.dickinson.edu/latin-core-list1"
DCC_CAESAR = "https://dcc.dickinson.edu/caesar/book-1/chapter-1-1"


class RomanNormalizationTest(unittest.TestCase):
    def test_interpunct_vu_and_j(self) -> None:
        self.assertEqual(to_epigraphic("Iulius"), "IVLIVS")
        self.assertEqual(to_classical("IVLIVS"), "IULIUS")
        self.assertEqual(to_classical("JULIUS"), "IULIUS")
        self.assertEqual(to_classical("VENI"), "VENI")
        self.assertEqual(to_classical("SENATVS\u00b7POPVLVS"), "SENATUS POPULUS")
        self.assertEqual(to_epigraphic("d\u012bv\u012bsa"), "DIVISA")
        self.assertEqual(to_classical("M.AGRIPPA"), "MAGRIPPA")

    def test_consonant_before_vowel_stays_v(self) -> None:
        # Documented limit: post-consonantal V before a vowel is not rewritten.
        self.assertEqual(to_classical("SERVARE"), "SERVARE")


class LatinReaderTest(unittest.TestCase):
    def test_published_caesar_line(self) -> None:
        reading = read_latin(CAESAR_INSCRIPTION)
        self.assertEqual(reading.classical, "GALLIA EST OMNIS DIVISA IN PARTES TRES")
        self.assertEqual(reading.epigraphic, reading.classical)
        self.assertEqual(reading.classical, to_classical(CAESAR_BG_1_1))
        self.assertEqual(reading.note, NOT_A_DECIPHERMENT)
        self.assertIn("not a decipherment", reading.note.lower())

        by_form = {item.form: item for item in reading.glosses}
        self.assertEqual(
            [item.form for item in reading.glosses],
            ["GALLIA", "EST", "OMNIS", "DIVISA", "IN", "PARTES", "TRES"],
        )
        self.assertTrue(all(item.known for item in reading.glosses))
        self.assertEqual(by_form["GALLIA"].gloss, "Gaul, roughly equivalent to modern France")
        self.assertEqual(by_form["GALLIA"].source_url, DCC_CAESAR)
        self.assertEqual(by_form["EST"].lemma, "sum")
        self.assertEqual(by_form["OMNIS"].gloss, "all, every, as a whole")
        self.assertEqual(by_form["DIVISA"].lemma, "divido")
        self.assertEqual(by_form["DIVISA"].gloss, "divide, separate")
        self.assertEqual(by_form["IN"].gloss, "in, on (+ abl.); into, onto (+ acc)")
        self.assertEqual(by_form["PARTES"].lemma, "pars")
        self.assertEqual(by_form["TRES"].gloss, "three")
        for form in ("EST", "OMNIS", "DIVISA", "IN", "PARTES", "TRES"):
            self.assertEqual(by_form[form].source_url, DCC_CORE)
        self.assertTrue(CAESAR_BG_1_1_URL.startswith("https://www.perseus.tufts.edu/"))

    def test_que_clitic_and_unknown_token(self) -> None:
        reading = read_latin("SENATVS\u00b7POPVLVSQVE")
        self.assertEqual(reading.classical, "SENATUS POPULUSQUE")
        self.assertEqual(
            [(item.form, item.lemma, item.gloss) for item in reading.glosses],
            [
                ("SENATUS", "senatus", "senate"),
                ("POPULUS", "populus", "people"),
                ("QUE", "que", "and (postpositive enclitic)"),
            ],
        )
        unknown = read_latin("RONGORONGO")
        self.assertEqual(unknown.glosses[0].known, False)
        self.assertIsNone(unknown.glosses[0].gloss)
        self.assertIn("not a decipherment", unknown.note)


if __name__ == "__main__":
    unittest.main()
