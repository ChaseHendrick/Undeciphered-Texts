"""Elder Futhark lookup: one sourced known value (not a decipherment)."""

from __future__ import annotations

import unittest
import hashlib
import json
from pathlib import Path

from engine.elder_futhark import SOURCE_URL, load_inventory, lookup, transliterate


class ElderFutharkLookupTest(unittest.TestCase):
    def test_source_url_is_real_wikipedia_page(self) -> None:
        self.assertEqual(SOURCE_URL, "https://en.wikipedia.org/wiki/Elder_Futhark")
        inventory = load_inventory()
        self.assertEqual(inventory["source_url"], SOURCE_URL)
        self.assertTrue(inventory["not_a_decipherment"])

    def test_fehu_matches_fetched_wikipedia_value(self) -> None:
        # Fetched 2026-10-02 from https://en.wikipedia.org/wiki/Elder_Futhark
        # Rune names table: ᚠ / f / *fehu / "cattle", "wealth"
        entry = lookup("ᚠ")
        self.assertIsNotNone(entry)
        assert entry is not None
        self.assertEqual(entry["rune"], "ᚠ")
        self.assertEqual(entry["unicode"], "U+16A0")
        self.assertEqual(entry["transliteration"], "f")
        self.assertEqual(entry["name"], "*fehu")
        self.assertIn("cattle", entry["meaning"])
        self.assertIn("wealth", entry["meaning"])

    def test_unknown_glyph_is_not_invented(self) -> None:
        self.assertIsNone(lookup("A"))
        self.assertEqual(transliterate("ᚠXᚢ"), "fXu")



CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "elder_futhark_certificate.json"


class ElderFutharkCertificateTest(unittest.TestCase):
    """Certificate checks a cited known text/gloss, not an unknown script."""

    def test_certificate_matches_known_text_hash(self) -> None:
        cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(cert["tool_name"], "elder-futhark")
        known = cert["known_text"]
        digest = hashlib.sha256(known.encode("utf-8")).hexdigest()
        self.assertEqual(digest, cert["known_text_sha256"])
        entry = lookup(cert["input"])
        self.assertEqual(entry["name"], known)
        self.assertEqual(cert["source_url"], SOURCE_URL)
        self.assertIn("not an unknown script", cert["note"].lower())


if __name__ == "__main__":
    unittest.main()
