"""The broad-Enigma training share leaves the fixed comparisons unchanged at zero."""

from __future__ import annotations

import unittest

import numpy as np

from engine.neural_features import feature_tables
from engine.neural_grade import _english_unigram, letters_az, load_training_prose
from engine.neural_router_v2 import _samples, train_router


class BroadEnigmaShareTest(unittest.TestCase):
    def setUp(self) -> None:
        prose = letters_az(load_training_prose())
        self.letters = prose[:6000]
        english = _english_unigram(self.letters)
        self.tables = (english, feature_tables(self.letters, english))

    def test_zero_share_draws_the_same_rows(self) -> None:
        english, tables = self.tables
        families = ["caesar", "enigma", "m209"]
        plain_x, plain_y = _samples(self.letters, families, 2, 11, english, tables, version="cipher_statistics_v5")
        zero_x, zero_y = _samples(self.letters, families, 2, 11, english, tables, version="cipher_statistics_v5",
                                  broad_enigma=0.)
        self.assertTrue(np.array_equal(plain_x, zero_x))
        self.assertTrue(np.array_equal(plain_y, zero_y))

    def test_a_full_share_changes_only_the_enigma_rows_kind(self) -> None:
        english, tables = self.tables
        families = ["enigma"]
        plain_x, _ = _samples(self.letters, families, 2, 11, english, tables, version="cipher_statistics_v5")
        broad_x, _ = _samples(self.letters, families, 2, 11, english, tables, version="cipher_statistics_v5",
                              broad_enigma=1.)
        self.assertFalse(np.array_equal(plain_x, broad_x))

    def test_the_share_is_bounded(self) -> None:
        for bad in (-0.1, 1.5, True):
            with self.assertRaises(ValueError):
                train_router(write=False, broad_enigma=bad)


if __name__ == "__main__":
    unittest.main()
