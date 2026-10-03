"""Synthetic mural analyzer must report colors, regions, and a repeated motif.

Not a Teotihuacan or ancient-painting test. The fixture is generated in memory.
"""

from __future__ import annotations

import unittest

from engine.mural_analyzer import (
    BLOCK_A,
    BLOCK_B,
    BLOCK_C,
    DISCLAIMER,
    MOTIF,
    analyze_mural,
    make_synthetic_mural,
    quantize_rgb,
)


class SyntheticMuralAnalyzerTest(unittest.TestCase):
    def test_synthetic_mural_report(self) -> None:
        grid = make_synthetic_mural(96, 64)
        report = analyze_mural(grid)

        self.assertEqual(report.width, 96)
        self.assertEqual(report.height, 64)
        self.assertIn("Teotihuacan", report.disclaimer)
        self.assertIn("does not read", report.disclaimer.lower())
        self.assertEqual(report.disclaimer, DISCLAIMER)

        dominant = {c.rgb for c in report.dominant_colors}
        self.assertIn(quantize_rgb(BLOCK_A), dominant)
        self.assertIn(quantize_rgb(BLOCK_B), dominant)
        self.assertIn(quantize_rgb(BLOCK_C), dominant)
        self.assertIn(quantize_rgb(MOTIF), dominant)

        # Colored blocks plus three motif copies plus background => several regions.
        self.assertGreaterEqual(report.region_count, 5)

        self.assertTrue(
            report.motif_repeats,
            "the synthetic plus motif is stamped three times and must count as a repeat",
        )
        self.assertGreaterEqual(report.motif_repeat_count, 3)

        motif_regions = [
            r for r in report.regions if quantize_rgb(r.color) == quantize_rgb(MOTIF)
        ]
        self.assertGreaterEqual(len(motif_regions), 3)
        shapes = {r.shape_key for r in motif_regions}
        self.assertEqual(len(shapes), 1, "repeated motif copies should share one shape key")


if __name__ == "__main__":
    unittest.main()
