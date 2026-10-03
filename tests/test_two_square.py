"""Two-square recovery: synthetic plaintext from two 5×5 squares."""

from __future__ import annotations

import unittest

from engine.alphabet import letters_only
from engine.ciphers import (
    square_from_keyword,
    two_square_decrypt,
    two_square_encrypt,
    two_square_letters,
)
from engine.fixtures import VIGENERE_PLAIN
from engine.german import TRUPPENSCHLUESSEL_NR86, get_german_model
from engine.solvers.two_square import (
    DEFAULT_KEYWORDS,
    climb_two_square,
    solve_two_square,
    trigram_count_score,
)

# Synthetic English (no J). Enciphered under keyword squares HARBOR / CANAL.
TWO_SQUARE_PLAIN = two_square_letters(VIGENERE_PLAIN)
TWO_SQUARE_LEFT_KW = "HARBOR"
TWO_SQUARE_RIGHT_KW = "CANAL"
TWO_SQUARE_LEFT = square_from_keyword(TWO_SQUARE_LEFT_KW)
TWO_SQUARE_RIGHT = square_from_keyword(TWO_SQUARE_RIGHT_KW)


class TwoSquareRoundTripTest(unittest.TestCase):
    def test_keyword_squares_are_25_without_j(self) -> None:
        self.assertEqual(len(TWO_SQUARE_LEFT), 25)
        self.assertEqual(len(set(TWO_SQUARE_LEFT)), 25)
        self.assertNotIn("J", TWO_SQUARE_LEFT)
        self.assertNotIn("J", TWO_SQUARE_RIGHT)

    def test_encrypt_decrypt_roundtrip(self) -> None:
        cipher = two_square_encrypt(TWO_SQUARE_PLAIN, TWO_SQUARE_LEFT, TWO_SQUARE_RIGHT)
        self.assertEqual(len(cipher) % 2, 0)
        self.assertNotEqual(cipher, TWO_SQUARE_PLAIN)
        plain = two_square_decrypt(cipher, TWO_SQUARE_LEFT, TWO_SQUARE_RIGHT)
        # Odd length may have gained a pad X; compare even prefix of source.
        expect = TWO_SQUARE_PLAIN if len(TWO_SQUARE_PLAIN) % 2 == 0 else TWO_SQUARE_PLAIN + "X"
        self.assertEqual(plain, expect)

    def test_paper_rectangle_example_kr_to_in(self) -> None:
        # Ostwald & Weierud Fig. 6 squares; compromise pair kr→IN (mcts.pdf).
        left = "WKIZBOGPSFENHQRDATLMVCXUY"
        right = "IGVBXDPQFSREYNCZOLMHATUKW"
        self.assertEqual(two_square_encrypt("KR", left, right), "IN")
        self.assertEqual(two_square_decrypt("IN", left, right), "KR")
        self.assertEqual(two_square_encrypt("NI", left, right), "RK")
        self.assertEqual(two_square_encrypt("QT", left, right), "EU")
        self.assertEqual(two_square_encrypt("UE", left, right), "TQ")


class TwoSquareRecoveryTest(unittest.TestCase):
    def test_keyword_solver_recovers_synthetic_plaintext(self) -> None:
        expect = TWO_SQUARE_PLAIN if len(TWO_SQUARE_PLAIN) % 2 == 0 else TWO_SQUARE_PLAIN + "X"
        cipher = two_square_encrypt(expect, TWO_SQUARE_LEFT, TWO_SQUARE_RIGHT)
        # Solver is not handed the squares—only a word list that contains them.
        result = solve_two_square(cipher, keywords=DEFAULT_KEYWORDS)
        self.assertEqual(result.details["left_keyword"], TWO_SQUARE_LEFT_KW)
        self.assertEqual(result.details["right_keyword"], TWO_SQUARE_RIGHT_KW)
        self.assertEqual(letters_only(result.plaintext), expect)
        self.assertEqual(result.details["left_square"], TWO_SQUARE_LEFT)
        self.assertEqual(result.details["right_square"], TWO_SQUARE_RIGHT)

    def test_known_squares_decrypt_path(self) -> None:
        expect = TWO_SQUARE_PLAIN if len(TWO_SQUARE_PLAIN) % 2 == 0 else TWO_SQUARE_PLAIN + "X"
        cipher = two_square_encrypt(expect, TWO_SQUARE_LEFT, TWO_SQUARE_RIGHT)
        result = solve_two_square(cipher, left=TWO_SQUARE_LEFT, right=TWO_SQUARE_RIGHT)
        self.assertEqual(result.plaintext, expect)
        self.assertEqual(result.details["mode"], "known_squares")

    def test_wrong_keywords_score_worse_than_true(self) -> None:
        expect = TWO_SQUARE_PLAIN if len(TWO_SQUARE_PLAIN) % 2 == 0 else TWO_SQUARE_PLAIN + "X"
        cipher = two_square_encrypt(expect, TWO_SQUARE_LEFT, TWO_SQUARE_RIGHT)
        true_plain = two_square_decrypt(cipher, TWO_SQUARE_LEFT, TWO_SQUARE_RIGHT)
        wrong_plain = two_square_decrypt(
            cipher,
            square_from_keyword("STONE"),
            square_from_keyword("RIVER"),
        )
        self.assertGreater(trigram_count_score(true_plain), trigram_count_score(wrong_plain))


class TwoSquareNr86ExperimentTest(unittest.TestCase):
    """Nr. 86 is an experiment only. Do not treat climb output as a reading."""

    def test_climb_on_nr86_does_not_match_any_sourced_plaintext(self) -> None:
        # No public sourced plaintext for Funkspruch Nr. 86 (FBOIQ). A climb
        # may emit letters; that is not a match to a sourced reading.
        cipher = TRUPPENSCHLUESSEL_NR86
        self.assertEqual(len(cipher), 46)
        result = climb_two_square(cipher, restarts=2, kicks=4, seed=86)
        model = get_german_model()
        probe = model.mean_quadgram(
            [ord(ch) - 65 for ch in "DERWOLFUNDDIESIEBENJUNGENGEISZLEINWARENALLEHUNGRIG"]
        )
        got = model.mean_quadgram([ord(ch) - 65 for ch in result.plaintext])
        # Climber output stays well below held-out German prose; not a reading.
        self.assertLess(got, probe - 0.5)
        # Sourced booklet example from the paper is 54 letters; this message is 46.
        booklet = "FEINDLIQERANGRIFFAUFSTRASZEADORFSTRIQBEHAUSENABGEWEHRT"
        self.assertNotEqual(result.plaintext, booklet)
        self.assertNotEqual(len(result.plaintext), len(booklet))


if __name__ == "__main__":
    unittest.main()
