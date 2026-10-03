"""One published Maya sign reading, checked against the fetched CMGG entry."""

from __future__ import annotations

import unittest

from engine.maya_glyph_lookup import (
    DOES_NOT_DECIPHER_UNDECIPHERED_MAYA_PASSAGES,
    lookup,
)


class MayaGlyphLookupTest(unittest.TestCase):
    def test_t544_kin_matches_fetched_cmgg_entry(self) -> None:
        # Fetched 2026-10-02 from
        # https://mayaglyphs.org/CMGGgrid.html (label K&#x27;IN, code T544)
        # and https://mayaglyphs.org/CWLhtml/K%27INlogo.html
        # Translation line: day; sun; calendar unit k’in (U+2019), ...
        row = lookup("T544")
        self.assertIsNotNone(row)
        assert row is not None
        self.assertEqual(row.reading, "K'IN")
        self.assertEqual(row.reading, "K\u0027IN")
        self.assertEqual(
            row.gloss,
            "day; sun; calendar unit k\u2019in, 1st (lowest) position in the LC = 1 day",
        )
        self.assertIn("day", row.gloss)
        self.assertIn("sun", row.gloss)
        self.assertEqual(row.part_of_speech, "Noun")
        self.assertEqual(
            row.source_url,
            "https://mayaglyphs.org/CWLhtml/K%27INlogo.html",
        )
        self.assertTrue(DOES_NOT_DECIPHER_UNDECIPHERED_MAYA_PASSAGES)
        self.assertIsNone(lookup("T544 T544 undeciphered passage"))


if __name__ == "__main__":
    unittest.main()
