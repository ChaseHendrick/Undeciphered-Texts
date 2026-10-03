"""The glyph reader must recover labels planted on a synthetic sheet.

The sheet is drawn in the test. Recovering those labels is template matching
against glyph_reader's inventory. It is not a decipherment of Linear A, the
Indus script, or Teotihuacan signs.
"""

from __future__ import annotations

import unittest

from glyph_reader import (
    DISCLAIMER,
    SIGN_DRAWERS,
    analyze_glyphs,
    inventory_labels,
    render_synthetic_sheet,
    template_descriptors,
)

# Distinct marks, with repeats of bar, peak, ring, and stem.
PLANTED = (
    "bar",
    "peak",
    "bar",
    "cross",
    "ring",
    "corner",
    "peak",
    "stem",
    "ring",
    "stem",
)


class SyntheticGlyphReaderTest(unittest.TestCase):
    def test_recovers_planted_inventory_labels(self) -> None:
        image = render_synthetic_sheet(PLANTED, columns=5)
        report = analyze_glyphs(image)

        self.assertEqual([glyph.label for glyph in report.glyphs], list(PLANTED))
        self.assertEqual(len(report.glyphs), len(PLANTED))
        self.assertIn("Linear A", report.disclaimer)
        self.assertIn("Indus", report.disclaimer)
        self.assertIn("Teotihuacan", report.disclaimer)
        self.assertEqual(report.disclaimer, DISCLAIMER)
        self.assertIn("does not decipher", report.disclaimer.lower())

        for glyph in report.glyphs:
            x, y, width, height = glyph.bbox
            self.assertGreaterEqual(x, 0)
            self.assertGreaterEqual(y, 0)
            self.assertGreater(width, 0)
            self.assertGreater(height, 0)
            self.assertGreaterEqual(glyph.ink_pixels, 12)
            self.assertEqual(glyph.distance, 0.0)
            self.assertIn(glyph.label, SIGN_DRAWERS)

        labels = [glyph.label for glyph in report.glyphs]
        self.assertGreater(labels.count("bar"), 1)
        self.assertGreater(labels.count("peak"), 1)
        self.assertGreater(labels.count("ring"), 1)
        self.assertGreater(labels.count("stem"), 1)

        bars = [glyph for glyph in report.glyphs if glyph.label == "bar"]
        stems = [glyph for glyph in report.glyphs if glyph.label == "stem"]
        self.assertEqual(bars[0].ink_pixels, bars[1].ink_pixels)
        self.assertNotEqual(bars[0].bbox, bars[1].bbox)
        bar_w, bar_h = bars[0].bbox[2], bars[0].bbox[3]
        stem_w, stem_h = stems[0].bbox[2], stems[0].bbox[3]
        self.assertGreater(bar_w, bar_h)
        self.assertGreater(stem_h, stem_w)

    def test_inventory_templates_are_distinct(self) -> None:
        templates = template_descriptors()
        self.assertEqual(set(templates), set(inventory_labels()))
        values = list(templates.values())
        self.assertEqual(len(values), len(set(values)))


if __name__ == "__main__":
    unittest.main()
