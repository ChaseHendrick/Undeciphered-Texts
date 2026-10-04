"""The frequency labeling is not English, and a shuffle usually scores better."""

from __future__ import annotations

import unittest

from engine.dagapeyeff_model import model_report
from engine.solvers.dagapeyeff import consider_language_model


class DagapeyeffModelTest(unittest.TestCase):
    def test_the_language_model_prefers_a_shuffle(self) -> None:
        report = model_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertEqual(report["length"], 196)
        self.assertEqual(report["english_quad"], -1.553)
        self.assertEqual(report["english_neural"], -2.495)
        self.assertEqual(report["printed_quad"], -3.6316)
        self.assertEqual(report["printed_neural"], -3.2313)
        self.assertEqual(report["regrouped_quad"], -3.6352)
        self.assertEqual(report["regrouped_neural"], -3.3504)
        self.assertFalse(report["regrouped_beats_printed_quad"])
        self.assertFalse(report["either_reaches_english"])
        self.assertEqual(report["printed_tail"]["draws"], 200000)
        self.assertEqual(report["printed_tail"]["quad_as_high"], 177295)
        self.assertEqual(report["printed_tail"]["neural_as_high"], 114857)
        self.assertEqual(report["printed_tail"]["best_shuffle_quad"], -3.107)
        self.assertEqual(report["regrouped_tail"]["quad_as_high"], 151728)
        self.assertEqual(report["regrouped_tail"]["neural_as_high"], 175130)
        self.assertEqual(report["regrouped_tail"]["best_shuffle_quad"], -3.1795)
        claim = consider_language_model()
        self.assertFalse(claim["language_model_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])


if __name__ == "__main__":
    unittest.main()
