"""Ogham lookup matches one value taken from the fetched Unicode names list.

Not a decipherment test. The expected name and character are the row
printed for 1681 on the Unicode 18.0.0 Ogham names list.
"""

from __future__ import annotations

import unittest

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


if __name__ == "__main__":
    unittest.main()
