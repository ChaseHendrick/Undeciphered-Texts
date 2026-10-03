"""Egyptian Gardiner-sign reader: table lookup and one verified phrase.

Phrase check: M17 Y5 N35 → jmn (Amun), letter-for-letter against
https://en.wiktionary.org/wiki/jmn and https://en.wikipedia.org/wiki/Amun .
This is a known-script dictionary test, not a decipherment claim.
"""

from __future__ import annotations

import unittest
import hashlib
import json
from pathlib import Path

from engine.egyptian import (
    UnknownSignError,
    get_reader,
    read_hieroglyphs,
)


# Verified against Wiktionary lemma jmn (head i-mn:n) and Wikipedia Amun.
AMUN_GARDINER = ("M17", "Y5", "N35")
AMUN_UNICODE = "𓇋𓏠𓈖"
AMUN_TRANSLITERATION = "jmn"


class EgyptianSignTableTest(unittest.TestCase):
    def test_subset_loads_from_sourced_json(self) -> None:
        reader = get_reader()
        self.assertTrue(reader.source_url.startswith("https://"))
        self.assertIn("List_of_Egyptian_hieroglyphs", reader.source_url)
        self.assertGreaterEqual(len(reader.signs), 24)

    def test_uniliteral_n35_lookup(self) -> None:
        entry = get_reader().lookup_sign("N35")
        self.assertEqual(entry.code, "N35")
        self.assertEqual(entry.unicode, "𓈖")
        self.assertEqual(entry.transliteration, "n")
        self.assertIn("water", entry.meaning.lower())

    def test_biliteral_y5_lookup(self) -> None:
        entry = get_reader().lookup_sign("Y5")
        self.assertEqual(entry.transliteration, "mn")
        self.assertEqual(entry.unicode, "𓏠")

    def test_unicode_and_code_agree(self) -> None:
        reader = get_reader()
        by_code = reader.lookup_sign("S34")
        by_glyph = reader.lookup_sign("𓋹")
        self.assertEqual(by_code.transliteration, by_glyph.transliteration)
        self.assertEqual(by_code.transliteration, "ꜥnḫ")

    def test_unknown_sign_raises(self) -> None:
        with self.assertRaises(UnknownSignError):
            get_reader().lookup_sign("ZZ99")


class EgyptianVerifiedPhraseTest(unittest.TestCase):
    def test_amun_gardiner_codes_match_source_transliteration(self) -> None:
        reading = read_hieroglyphs(AMUN_GARDINER)
        # Table values are j + mn + n; the complement n is not read twice.
        self.assertEqual([s.transliteration for s in reading.signs], ["j", "mn", "n"])
        self.assertEqual(reading.transliteration, AMUN_TRANSLITERATION)
        # Letter-for-letter against Wiktionary/Wikipedia "jmn".
        self.assertEqual(list(reading.transliteration), list("jmn"))

    def test_amun_unicode_sequence_matches_same_source(self) -> None:
        reading = read_hieroglyphs(AMUN_UNICODE)
        self.assertEqual(reading.transliteration, AMUN_TRANSLITERATION)
        self.assertEqual([s.code for s in reading.signs], ["M17", "Y5", "N35"])

    def test_amun_spaced_codes_string(self) -> None:
        reading = read_hieroglyphs("M17 Y5 N35")
        self.assertEqual(reading.transliteration, "jmn")
        self.assertIn("M17:", reading.gloss)
        self.assertIn("Y5:", reading.gloss)
        self.assertIn("N35:", reading.gloss)



CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "egyptian_certificate.json"


class EgyptianCertificateTest(unittest.TestCase):
    """Certificate checks a cited known text/gloss, not an unknown script."""

    def test_certificate_matches_known_text_hash(self) -> None:
        cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(cert["tool_name"], "egyptian-hieroglyph-reader")
        known = cert["known_text"]
        digest = hashlib.sha256(known.encode("utf-8")).hexdigest()
        self.assertEqual(digest, cert["known_text_sha256"])
        reading = read_hieroglyphs(cert["input"])
        self.assertEqual(reading.transliteration, known)
        self.assertIn("not an unknown script", cert["note"].lower())


if __name__ == "__main__":
    unittest.main()
