"""One known OSL reading: sign AN publishes the value "an".

Fetched from osl.asl at commit dcee28e57d9387638c122e3435a98ceb6ea9e5e2
(@sign AN, @list U+1202D, @ucun, @v an). Not a tablet decipherment.
"""

from __future__ import annotations

import unittest

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


if __name__ == "__main__":
    unittest.main()
