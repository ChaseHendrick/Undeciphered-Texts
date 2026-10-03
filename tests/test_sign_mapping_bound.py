"""Unicity-distance checks. A pass is not a decipherment of any script."""

from __future__ import annotations

import math
import unittest

from engine.sign_mapping_bound import (
    SHANNON_UNICITY_URL,
    estimate_sign_mapping,
    unicity_distance_symbols,
)

# Stated language-model entropy, in bits per symbol. Not fit to a corpus.
# It sits well below both log2(20) and log2(26), so redundancy is positive.
# Shannon's 1949 English illustration used a higher entropy (redundancy
# near 0.7 decimal digits per letter) and still put simple-substitution
# unicity near 30 letters. One bit per symbol is the rate used below.
STATED_ENTROPY_BITS = 1.0

# Long English-length text: tens of thousands of letters, the scale of a
# long essay or a short book, far past a 30-letter unicity distance.
ENGLISH_LENGTH = 50_000


class SignMappingBoundTest(unittest.TestCase):
    def test_five_signs_over_twenty_is_underdetermined(self) -> None:
        bound = estimate_sign_mapping(20, 5, STATED_ENTROPY_BITS)
        self.assertEqual(bound.verdict, "underdetermined")
        self.assertTrue(bound.underdetermined)
        self.assertGreater(bound.lower_bound_symbols, 5)
        self.assertEqual(bound.alphabet_size, 20)
        self.assertEqual(bound.text_length, 5)
        self.assertEqual(bound.entropy_bits_per_symbol, STATED_ENTROPY_BITS)
        self.assertEqual(bound.source_url, SHANNON_UNICITY_URL)

    def test_long_english_length_text_is_not_underdetermined(self) -> None:
        bound = estimate_sign_mapping(26, ENGLISH_LENGTH, STATED_ENTROPY_BITS)
        self.assertEqual(bound.verdict, "possibly determined")
        self.assertFalse(bound.underdetermined)
        self.assertLess(bound.lower_bound_symbols, ENGLISH_LENGTH)
        self.assertGreater(bound.lower_bound_symbols, 0)
        # Same stated rate: a few dozen letters would still be short, so
        # the pass is the length, not a claim that English is solved.
        short = estimate_sign_mapping(26, 5, STATED_ENTROPY_BITS)
        self.assertEqual(short.verdict, "underdetermined")
        self.assertGreater(short.lower_bound_symbols, 5)

    def test_zero_redundancy_stays_underdetermined(self) -> None:
        # Entropy equal to the alphabet capacity: Shannon's ideal case.
        # No finite corpus crosses the bound.
        capacity = math.log2(20)
        bound = estimate_sign_mapping(20, 10**6, capacity)
        self.assertEqual(bound.verdict, "underdetermined")
        self.assertTrue(math.isinf(bound.lower_bound_symbols))
        self.assertEqual(unicity_distance_symbols(20, capacity), math.inf)

    def test_module_states_it_is_not_a_decipherment(self) -> None:
        import engine.sign_mapping_bound as mod

        doc = mod.__doc__ or ""
        self.assertIn("not a decipherment", doc)
        self.assertIn("Linear A", doc)
        self.assertIn("Indus", doc)
        self.assertIn(SHANNON_UNICITY_URL, doc)
        self.assertIn("unicity", doc.lower())


if __name__ == "__main__":
    unittest.main()
