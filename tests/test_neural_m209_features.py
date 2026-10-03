"""Exact unknown-phase marginalization and training-only pair-score controls."""
from __future__ import annotations

import itertools
import math
import unittest

from engine.neural_m209_features import (
    LAGS, _joint_keystream_pairs, _cipher_pair_distribution,
    m209_pair_tables, m209_pair_features,
)


class M209PairFeatureTest(unittest.TestCase):
    def test_unknown_phase_joint_matches_exhaustive_tiny_machine(self):
        pins = ((1, 0), (1, 1, 0))
        bars = ((1, 0), (2, 0), (1, 2))
        for lag in (0, 1, 2, 3, 5):
            actual = _joint_keystream_pairs(pins, bars, lag)
            expected = [[0.] * 26 for _ in range(26)]
            for phases in itertools.product(range(2), range(3)):
                active = [[pins[wheel][(phase + step) % len(pins[wheel])]
                           for wheel, phase in enumerate(phases)] for step in (0, lag)]
                kicks = [sum(bool((left and row[left - 1]) or (right and row[right - 1]))
                             for left, right in bars) for row in active]
                expected[kicks[0]][kicks[1]] += 1 / 6
            for row, wanted in zip(actual, expected):
                for value, correct in zip(row, wanted):
                    self.assertAlmostEqual(value, correct, places=14)

    def test_beaufort_cipher_pair_formula_uses_slide25_and_two_plain_letters(self):
        english = tuple((index + 1) / 351 for index in range(26))
        keypair = [[0.] * 26 for _ in range(26)]
        keypair[2][4] = 1.
        actual = _cipher_pair_distribution(keypair, english)
        for first in range(26):
            for second in range(26):
                c1, c2 = (25 + 2 - first) % 26, (25 + 4 - second) % 26
                self.assertAlmostEqual(actual[c1][c2], english[first] * english[second], places=15)

    def test_uniform_training_distribution_makes_all_scores_neutral(self):
        for text in ("A" * 120, "ABCDEFGHIJKLMNOPQRSTUVWXYZ" * 8):
            actual = m209_pair_features(text, {"english": [1 / 26] * 26})
            self.assertEqual(len(actual), 6)
            self.assertEqual(LAGS, (17, 19, 21, 23, 25, 26))
            for score in actual:
                self.assertAlmostEqual(score, 0., places=12)

    def test_missing_lag_pairs_return_neutral_evidence(self):
        self.assertEqual(m209_pair_features("ABCDEFGHIJKLMNOP", {"english": [1 / 26] * 26}), [0.] * 6)

    def test_biased_training_tables_form_proper_pair_models_with_positive_expected_fit(self):
        english = tuple((index + 1) / 351 for index in range(26))
        tables = m209_pair_tables(english)
        self.assertEqual(m209_pair_tables(list(english)), tables)
        for logpair in tables:
            probability = [[math.exp(value) for value in row] for row in logpair]
            self.assertAlmostEqual(sum(map(sum, probability)), 1., places=12)
            own_fit = sum(p * (math.log(p) + 2 * math.log(26)) for row in probability for p in row)
            uniform_fit = sum(value + 2 * math.log(26) for row in logpair for value in row) / 676
            self.assertGreater(own_fit, 0.)
            self.assertLess(uniform_fit, 0.)

    def test_input_table_types_probabilities_and_bounds_are_validated(self):
        valid = {"english": [1 / 26] * 26}
        for text, tables in [(None, valid), ("ABC", valid), ("A" * 8193, valid),
                             ("A" * 16 + "\u017f", valid), ("A" * 16, {}),
                             ("A" * 16, {"english": [1.] * 26}),
                             ("A" * 16, {"english": [True] * 26}),
                             ("A" * 16, {"english": [0.] * 26}),
                             ("A" * 16, {"english": [10**1000] * 26}),
                             ("A" * 16, {"english": [float("nan")] * 26})]:
            with self.assertRaises((TypeError, ValueError)):
                m209_pair_features(text, tables)


if __name__ == "__main__":
    unittest.main()
