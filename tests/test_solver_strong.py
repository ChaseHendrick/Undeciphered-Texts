"""The larger English model recovers fresh windows the legacy model does not."""

from __future__ import annotations

import unittest

from engine.language import get_legacy_model, get_model
from engine.solver_strong import solver_strong_report


class SolverStrongTest(unittest.TestCase):
    def test_the_larger_model_is_promoted_on_the_drill(self) -> None:
        report = solver_strong_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["legacy_letters"], 8689)
        self.assertEqual(report["default_letters"], 1916398)
        rows = {row["width"]: row for row in report["rows"]}
        self.assertEqual((rows[200]["legacy_exact"], rows[200]["default_exact"]), (1, 7))
        self.assertEqual((rows[150]["legacy_exact"], rows[150]["default_exact"]), (0, 6))
        self.assertEqual((rows[100]["legacy_exact"], rows[100]["default_exact"]), (0, 0))
        self.assertLess(rows[100]["default_wrong_letters"], rows[100]["legacy_wrong_letters"])
        self.assertTrue(report["certificate_legacy_exact"])
        self.assertTrue(report["certificate_default_exact"])
        self.assertTrue(report["promoted"])

    def test_the_default_is_the_larger_model(self) -> None:
        self.assertEqual(get_model().sample_letters, 1916398)
        self.assertEqual(get_legacy_model().sample_letters, 8689)

    def test_an_unseen_context_backs_off_instead_of_going_flat(self) -> None:
        model = get_model()
        q = ord("Q") - 65
        x = ord("X") - 65
        z = ord("Z") - 65
        e = ord("E") - 65
        base = ((q * 26 + x) * 26 + z) * 26
        row = model.logp[base:base + 26]
        self.assertNotAlmostEqual(min(row), max(row), places=3)
        self.assertGreater(row[e], row[z])


if __name__ == "__main__":
    unittest.main()
