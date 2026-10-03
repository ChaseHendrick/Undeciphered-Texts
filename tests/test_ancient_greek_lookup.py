"""One published LSJ gloss, checked against the fetched Perseus entry.

Not a decipherment test. The expected lemma and gloss are sense A of
ἄνθρωπος on the Perseus LSJ page fetched 2026-10-02.
"""

from __future__ import annotations

import unittest
import hashlib
import json
from pathlib import Path

from engine.ancient_greek_lookup import (
    DOES_NOT_DECIPHER_LINEAR_B_OR_UNKNOWN_GREEK,
    WORD_SOURCE_URL,
    lookup_letter,
    lookup_word,
)


class AncientGreekLookupTest(unittest.TestCase):
    def test_anthropos_matches_fetched_lsj_gloss(self) -> None:
        # Fetched 2026-10-02 from
        # https://www.perseus.tufts.edu/hopper/text?doc=Perseus:text:1999.04.0057:entry=a)/nqrwpos
        # Sense A: "man, both as a generic term and of individuals"
        row = lookup_word("ἄνθρωπος")
        self.assertIsNotNone(row)
        assert row is not None
        self.assertEqual(row.lemma, "ἄνθρωπος")
        self.assertEqual(row.lemma, "\u1f04\u03bd\u03b8\u03c1\u03c9\u03c0\u03bf\u03c2")
        self.assertEqual(row.sense, "A")
        self.assertEqual(
            row.gloss,
            "man, both as a generic term and of individuals",
        )
        self.assertIn("man", row.gloss)
        self.assertEqual(row.source_url, WORD_SOURCE_URL)
        self.assertTrue(row.source_url.startswith("https://www.perseus.tufts.edu/"))
        self.assertTrue(DOES_NOT_DECIPHER_LINEAR_B_OR_UNKNOWN_GREEK)
        self.assertIsNone(lookup_word("da-mo Linear B"))
        self.assertIsNone(lookup_word("unknown Greek passage"))
        letter = lookup_letter("Α")
        self.assertIsNotNone(letter)
        assert letter is not None
        self.assertEqual(letter.unicode_name, "GREEK CAPITAL LETTER ALPHA")
        self.assertEqual(letter.codepoint, "U+0391")
        self.assertEqual(letter.character, "\u0391")



CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "ancient_greek_certificate.json"


class AncientGreekCertificateTest(unittest.TestCase):
    """Certificate checks a cited known text/gloss, not an unknown script."""

    def test_certificate_matches_known_text_hash(self) -> None:
        cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(cert["tool_name"], "ancient-greek-lookup")
        known = cert["known_text"]
        digest = hashlib.sha256(known.encode("utf-8")).hexdigest()
        self.assertEqual(digest, cert["known_text_sha256"])
        row = lookup_word(cert["input"])
        self.assertIsNotNone(row)
        assert row is not None
        self.assertEqual(row.gloss, known)
        self.assertEqual(cert["source_url"], WORD_SOURCE_URL)
        self.assertIn("not an unknown script", cert["note"].lower())


if __name__ == "__main__":
    unittest.main()
