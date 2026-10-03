"""Polybius-plus-Gronsfeld search: a constructed cipher, then the 1939 challenge.

The constructed fixture is encrypted in this file. The solver is not given the
keyword, the numeric key, or the null period. The D'Agapeyeff checks lock the
published digit string and the failure of that same search. They do not claim
a decipherment.
"""

from __future__ import annotations

import unittest
from collections import Counter

from engine.ciphers import square_from_keyword
from engine.language import get_model
from engine.solvers.polybius_gronsfeld import (
    BOOK_POLYBIUS_CIPHER,
    DAGAPEYEFF_SOURCE,
    apply_gronsfeld,
    coords_to_text,
    dagapeyeff_digits,
    decrypt_book_polybius,
    insert_nulls,
    legal_keys,
    polybius_digits,
    solve_polybius_gronsfeld,
    undo_gronsfeld,
)

CONSTRUCTED_PLAIN = "MEET AT THE HARBOR AFTER THE BELL RINGS AT DAWN"
CONSTRUCTED_KEYWORD = "alphabet"
CONSTRUCTED_KEY = (2, 7, 1, 8)
CONSTRUCTED_NULL_PERIOD = 5
CONSTRUCTED_NULL_PHASE = 4
CONSTRUCTED_DUMMY = 9

# Faithful reading of the 178-letter example and the square printed on
# https://en.wikipedia.org/wiki/D%27Agapeyeff_cipher (fetched 2026-10-02).
# The page's prose gloss is longer; this is what the printed pairs decode to.
BOOK_FAITHFUL = (
    "THENEWPLANOFATTACKINCLUDESOPERATIONSBYTHREEBOMBRSQUDRONS"
    "OVERFACTORYARYASOUTHWESTOTHERIVER"
)
BOOK_GLOSS = (
    "THENEWPLANOFATTACKINCLUDESOPERATIONSBYTHREEBOMBERSQUADRONS"
    "OVERFACTORYARYASOUTHWESTOFTHERIVER"
)


def _constructed_ciphertext() -> str:
    square = square_from_keyword(CONSTRUCTED_KEYWORD)
    coords = polybius_digits(CONSTRUCTED_PLAIN, square)
    enciphered = apply_gronsfeld(coords, CONSTRUCTED_KEY)
    with_nulls = insert_nulls(
        enciphered,
        CONSTRUCTED_NULL_PERIOD,
        CONSTRUCTED_NULL_PHASE,
        CONSTRUCTED_DUMMY,
    )
    return "".join(str(digit) for digit in with_nulls)


def _pair_ic_times_26(digit_string: str) -> float:
    pairs = [digit_string[i : i + 2] for i in range(0, len(digit_string), 2)]
    counts = Counter(pairs)
    total = len(pairs)
    ic = sum(count * (count - 1) for count in counts.values()) / (total * (total - 1))
    return 26 * ic


class ConstructedPolybiusGronsfeldTest(unittest.TestCase):
    def test_search_recovers_constructed_plaintext(self) -> None:
        ciphertext = _constructed_ciphertext()
        self.assertNotIn(CONSTRUCTED_KEYWORD, ciphertext)
        self.assertNotIn("2718", ciphertext)
        result = solve_polybius_gronsfeld(ciphertext)
        self.assertEqual(result.plaintext, "MEETATTHEHARBORAFTERTHEBELLRINGSATDAWN")
        self.assertEqual(result.key, "2718")
        self.assertEqual(result.details["keyword"], CONSTRUCTED_KEYWORD)
        self.assertEqual(result.details["null_period"], 5)
        self.assertEqual(result.details["null_phase"], 4)
        self.assertFalse(result.details["solved_historical"])
        self.assertGreater(result.score / (len(result.plaintext) - 3), -2.3)

    def test_book_polybius_example_matches_printed_square(self) -> None:
        reading = decrypt_book_polybius(BOOK_POLYBIUS_CIPHER)
        self.assertEqual(len("".join(ch for ch in BOOK_POLYBIUS_CIPHER if ch.isalpha())), 178)
        self.assertEqual(reading, BOOK_FAITHFUL)
        self.assertTrue(reading.startswith("THENEWPLANOFATTACKINCLUDESOPERATIONSBYTHREE"))
        self.assertIn("ARYA", reading)
        self.assertNotIn("AREA", reading)
        self.assertNotEqual(reading, BOOK_GLOSS)
        self.assertEqual(len(BOOK_GLOSS) - len(reading), 3)


class DagapeyeffSearchTest(unittest.TestCase):
    def test_published_digits_and_pair_index(self) -> None:
        digits = dagapeyeff_digits()
        self.assertEqual(DAGAPEYEFF_SOURCE, "https://en.wikipedia.org/wiki/D%27Agapeyeff_cipher")
        self.assertEqual(len(digits), 395)
        self.assertTrue(digits.startswith("7562828591"))
        self.assertTrue(digits.endswith("92000"))
        # Wikipedia: IC 1.812 on horizontal pairs, and a 196-character message.
        # Dropping the final 000 leaves 196 pairs. 26 * Friedman IC matches 1.812.
        self.assertEqual(len(digits) - 3, 392)
        self.assertAlmostEqual(_pair_ic_times_26(digits[:-3]), 1.812, places=3)

    def test_same_search_does_not_recover_english(self) -> None:
        digits = dagapeyeff_digits()
        model = get_model()
        control = solve_polybius_gronsfeld(_constructed_ciphertext())
        control_mean = control.score / (len(control.plaintext) - 3)
        self.assertLess(control_mean, -1.5)
        self.assertGreater(control_mean, -2.3)

        for reading in (digits, digits[:-3]):
            result = solve_polybius_gronsfeld(reading)
            self.assertFalse(result.details["solved_historical"])
            self.assertGreaterEqual(len(result.plaintext), 100)
            mean = result.score / (len(result.plaintext) - 3)
            self.assertLess(mean, -3.2)
            self.assertLess(mean, control_mean - 1.0)
            self.assertNotIn("THENEWPLAN", result.plaintext)
            self.assertNotIn("ATTACK", result.plaintext)

        # 196 pairs. Even digits are {0,6,7,8,9} and odd digits are {1,2,3,4,5},
        # so subtracting 5,0,5,0,... lands in 1..5 for every digit. That is a
        # partition of the digits, not a recovered message.
        pairs = [int(ch) for ch in digits[:-3]]
        evens = {pairs[i] for i in range(0, len(pairs), 2)}
        odds = {pairs[i] for i in range(1, len(pairs), 2)}
        self.assertEqual(evens, {0, 6, 7, 8, 9})
        self.assertEqual(odds, {1, 2, 3, 4, 5})
        self.assertEqual(legal_keys(pairs, 4), [(5, 0), (4, 0, 5, 0), (5, 0, 5, 0)])
        straight = coords_to_text(undo_gronsfeld(pairs, (5, 0)), square_from_keyword(""))
        straight_mean = model.score([ord(ch) - 65 for ch in straight]) / (len(straight) - 3)
        self.assertEqual(len(straight), 196)
        self.assertLess(straight_mean, -3.5)
        self.assertNotIn("ATTACK", straight)
        self.assertTrue(straight.startswith("KBMPQ"))


if __name__ == "__main__":
    unittest.main()
