"""One known OSL reading: sign AN publishes the value "an".

Fetched from osl.asl at commit dcee28e57d9387638c122e3435a98ceb6ea9e5e2
(@sign AN, @list U+1202D, @ucun, @v an). Not a tablet decipherment.
"""

from __future__ import annotations

import unittest
import hashlib
import json
from pathlib import Path

from engine.cuneiform_sign_lookup import PINNED_URL, lookup_sign, lookup_value, source

# Code point and glyph taken from the fetched @list U+1202D / @ucun line.
AN_CODEPOINT = 0x1202D
AN_GLYPH = "𒀭"


class CuneiformSignLookupTest(unittest.TestCase):
    def test_known_osl_value_an(self) -> None:
        sign = lookup_sign("AN")
        self.assertIsNotNone(sign)
        assert sign is not None
        self.assertEqual(sign["unicode"], "U+1202D")
        self.assertEqual(sign["uname"], "CUNEIFORM SIGN AN")
        self.assertEqual(sign["character"], AN_GLYPH)
        self.assertEqual(ord(sign["character"]), AN_CODEPOINT)
        self.assertIn("an", sign["values"])

        by_value = lookup_value("an")
        self.assertEqual([item["name"] for item in by_value], ["AN"])
        self.assertEqual(by_value[0]["character"], AN_GLYPH)

        cited = source()
        self.assertEqual(
            cited["url"],
            "https://github.com/oracc/osl/blob/master/00lib/osl.asl",
        )
        self.assertEqual(cited["pinned_url"], PINNED_URL)
        self.assertIn("dcee28e57d9387638c122e3435a98ceb6ea9e5e2", cited["pinned_url"])

        self.assertIsNone(lookup_sign("NOT-A-PUBLISHED-SIGN"))
        self.assertEqual(lookup_value("not-a-published-value"), [])



CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "cuneiform_sign_certificate.json"


class CuneiformCertificateTest(unittest.TestCase):
    """Certificate checks a cited known text/gloss, not an unknown script."""

    def test_certificate_matches_known_text_hash(self) -> None:
        cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(cert["tool_name"], "cuneiform-sign-lookup")
        known = cert["known_text"]
        digest = hashlib.sha256(known.encode("utf-8")).hexdigest()
        self.assertEqual(digest, cert["known_text_sha256"])
        sign = lookup_sign(cert["input"])
        self.assertIn(known, sign["values"])
        self.assertEqual(cert["source_url"], PINNED_URL)
        self.assertIn("not an unknown script", cert["note"].lower())


if __name__ == "__main__":
    unittest.main()
