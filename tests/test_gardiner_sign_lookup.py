"""Gardiner-sign lookup: one known Unicode chart sign.

Tests A1 (U+13000, seated man) against the cited Unicode Egyptian Hieroglyphs
chart. No multi-sign phrase is verified here, only single-sign table lookup.
This is a known-sign dictionary check, not a decipherment claim.
"""

from __future__ import annotations

import unittest
import hashlib
import json
from pathlib import Path

from engine.gardiner_sign_lookup import (
    KNOWN_SIGN_LOOKUP_ONLY,
    NOT_A_NEW_DECIPHERMENT,
    UnknownGardinerSignError,
    lookup,
    source_url,
)

A1_GLYPH = "𓀀"


class GardinerSignLookupTest(unittest.TestCase):
    def test_honesty_flags(self) -> None:
        self.assertTrue(KNOWN_SIGN_LOOKUP_ONLY)
        self.assertTrue(NOT_A_NEW_DECIPHERMENT)

    def test_source_url_is_unicode_chart(self) -> None:
        url = source_url()
        self.assertTrue(url.startswith("https://"))
        self.assertIn("unicode.org", url)
        self.assertIn("U13000", url)

    def test_a1_seated_man_from_unicode_chart(self) -> None:
        # Unicode chart: U+13000 EGYPTIAN HIEROGLYPH A001, seated man.
        entry = lookup("A1")
        self.assertEqual(entry.code, "A1")
        self.assertEqual(entry.unicode_hex, "U+13000")
        self.assertEqual(entry.unicode, A1_GLYPH)
        self.assertEqual(ord(entry.unicode), 0x13000)
        self.assertIn("A001", entry.name)
        self.assertIn("seated man", entry.gloss.lower())

    def test_a1_unicode_char_agrees(self) -> None:
        by_code = lookup("A1")
        by_glyph = lookup(A1_GLYPH)
        self.assertEqual(by_code.unicode, by_glyph.unicode)
        self.assertEqual(by_code.code, by_glyph.code)

    def test_unknown_sign_raises(self) -> None:
        with self.assertRaises(UnknownGardinerSignError):
            lookup("ZZ99")



CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "gardiner_sign_certificate.json"


class GardinerCertificateTest(unittest.TestCase):
    """Certificate checks a cited known text/gloss, not an unknown script."""

    def test_certificate_matches_known_text_hash(self) -> None:
        cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(cert["tool_name"], "gardiner-sign-lookup")
        known = cert["known_text"]
        digest = hashlib.sha256(known.encode("utf-8")).hexdigest()
        self.assertEqual(digest, cert["known_text_sha256"])
        entry = lookup(cert["input"])
        self.assertEqual(entry.gloss, known)
        self.assertEqual(cert["source_url"], source_url())
        self.assertIn("not an unknown script", cert["note"].lower())


if __name__ == "__main__":
    unittest.main()
