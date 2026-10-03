"""Ogham lookup matches one value taken from the fetched Unicode names list.

Not a decipherment test. The expected name and character are the row
printed for 1681 on the Unicode 18.0.0 Ogham names list.
"""

from __future__ import annotations

import unittest
import hashlib
import json
from pathlib import Path

from engine.ogham_lookup import SOURCE_URL, lookup


class OghamLookupTest(unittest.TestCase):
    def test_beith_matches_fetched_unicode_names_list(self) -> None:
        # Fetched from
        # https://unicode.org/Public/18.0.0/charts/nameslist/1680/
        # Traditional letters: 1681 ᚁ OGHAM LETTER BEITH
        entry = lookup("ᚁ")
        self.assertEqual(entry.codepoint, 0x1681)
        self.assertEqual(entry.code, "U+1681")
        self.assertEqual(entry.character, "ᚁ")
        self.assertEqual(entry.name, "OGHAM LETTER BEITH")
        self.assertEqual(entry.group, "traditional")
        self.assertEqual(lookup(0x1681), entry)
        self.assertEqual(lookup("U+1681"), entry)
        self.assertIn("unicode.org/Public/18.0.0/charts/nameslist/1680", SOURCE_URL)



CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "ogham_certificate.json"


class OghamCertificateTest(unittest.TestCase):
    """Certificate checks a cited known text/gloss, not an unknown script."""

    def test_certificate_matches_known_text_hash(self) -> None:
        cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(cert["tool_name"], "ogham-lookup")
        known = cert["known_text"]
        digest = hashlib.sha256(known.encode("utf-8")).hexdigest()
        self.assertEqual(digest, cert["known_text_sha256"])
        entry = lookup(cert["input"])
        self.assertEqual(entry.name, known)
        self.assertEqual(cert["source_url"], SOURCE_URL)
        self.assertIn("not an unknown script", cert["note"].lower())


if __name__ == "__main__":
    unittest.main()
