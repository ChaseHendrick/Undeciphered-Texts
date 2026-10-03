"""Known-key keyed Vigenère, pinned to the published Kryptos K1 reading.

The expected plaintext is the letter-by-letter decrypt in the NSA FOIA paper
(DOCID 4051151), which Wikipedia's "Solution of passage 1" also prints with
spaces. The prose line in that memo that says ILLUSION is a respacing, not
the letter groups. This test fails if those groups are "corrected".

K4 is out of scope. Nothing here is a K4 claim.
"""

from __future__ import annotations

import unittest

from engine.alphabet import letters_only
from engine.ciphers import vigenere_decrypt, vigenere_encrypt
from engine.solvers import SOLVERS
from engine.solvers.keyed_vigenere import (
    cipher_alphabet,
    keyed_vigenere_decrypt,
    keyed_vigenere_encrypt,
    keyword_mixed_alphabet,
    solve_keyed_vigenere,
)

# Sculpture K1, first two lines, as printed by Wikipedia and the NSA cipher sheet.
PUBLISHED_K1_CIPHERTEXT = (
    "EMUFPHZLRFAXYUSDJKZLDKRNSHGNFIVJYQTQUXQBQVYUVLLTREVJYQTMKYRDMFD"
)
# NSA letter groups: BETWE ENSUB TLESH ADING ANDTH ABSCE NCEOF LIGHT /
# LIEST HENUA NCEOF IQLUS ION. Wikipedia spaces the same letters.
PUBLISHED_K1_PLAINTEXT = (
    "BETWEENSUBTLESHADINGANDTHEABSENCEOFLIGHTLIESTHENUANCEOFIQLUSION"
)
PUBLISHED_K1_SPACED = (
    "BETWEEN SUBTLE SHADING AND THE ABSENCE OF LIGHT LIES THE NUANCE OF IQLUSION"
)
PUBLISHED_ALPHABET = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
# Cipher rows for PALIMPSEST under index letter K, from the same NSA tableau.
PUBLISHED_ROWS = {
    "P": "PTOSABCDEFGHIJLMNQUVWXZKRY",
    "A": "ABCDEFGHIJLMNQUVWXZKRYPTOS",
    "L": "LMNQUVWXZKRYPTOSABCDEFGHIJ",
    "I": "IJLMNQUVWXZKRYPTOSABCDEFGH",
    "M": "MNQUVWXZKRYPTOSABCDEFGHIJL",
    "S": "SABCDEFGHIJLMNQUVWXZKRYPTO",
    "E": "EFGHIJLMNQUVWXZKRYPTOSABCD",
    "T": "TOSABCDEFGHIJLMNQUVWXZKRYP",
}


class KeyedAlphabetTest(unittest.TestCase):
    def test_kryptos_alphabet_is_keyword_then_remaining_letters(self) -> None:
        mixed = keyword_mixed_alphabet("KRYPTOS")
        self.assertEqual(mixed, PUBLISHED_ALPHABET)
        self.assertEqual(len(mixed), 26)
        self.assertIn("C", mixed)
        self.assertEqual(keyword_mixed_alphabet("kryptos kryptos"), mixed)

    def test_published_tableau_rows(self) -> None:
        alphabet = keyword_mixed_alphabet("KRYPTOS")
        for key_letter, row in PUBLISHED_ROWS.items():
            self.assertEqual(cipher_alphabet(alphabet, key_letter, "K"), row)


class KryptosK1Test(unittest.TestCase):
    def test_recovers_published_k1_plaintext_exactly(self) -> None:
        result = solve_keyed_vigenere(
            PUBLISHED_K1_CIPHERTEXT,
            key="PALIMPSEST",
            alphabet_keyword="KRYPTOS",
            index_letter="K",
        )
        self.assertEqual(result.plaintext, PUBLISHED_K1_PLAINTEXT)
        self.assertEqual(letters_only(result.plaintext), letters_only(PUBLISHED_K1_SPACED))
        self.assertIn("IQLUSION", result.plaintext)
        self.assertNotIn("ILLUSION", result.plaintext)
        self.assertEqual(result.key, "PALIMPSEST")
        self.assertEqual(result.details["alphabet"], PUBLISHED_ALPHABET)
        self.assertEqual(result.details["index_letter"], "K")
        self.assertEqual(result.details["period"], 10)
        self.assertNotIn("k4 plaintext", result.details["scope"].lower())

    def test_encrypt_published_plaintext_reproduces_ciphertext(self) -> None:
        cipher = keyed_vigenere_encrypt(
            PUBLISHED_K1_PLAINTEXT,
            key="PALIMPSEST",
            alphabet_keyword="KRYPTOS",
            index_letter="K",
        )
        self.assertEqual(cipher, PUBLISHED_K1_CIPHERTEXT)
        again = keyed_vigenere_decrypt(
            cipher,
            key="palimpsest",
            alphabet_keyword="Kryptos",
            index_letter="k",
        )
        self.assertEqual(again, PUBLISHED_K1_PLAINTEXT)

    def test_not_registered_as_a_blind_solver(self) -> None:
        self.assertNotIn("keyed-vigenere", SOLVERS)


class KeyedVigenereGeneralTest(unittest.TestCase):
    def test_plain_alphabet_matches_standard_vigenere(self) -> None:
        plain = "The harbor bell rang at dusk."
        key = "SECRET"
        cipher = vigenere_encrypt(plain, key)
        self.assertEqual(
            keyed_vigenere_decrypt(cipher, key, alphabet_keyword="", index_letter="A"),
            vigenere_decrypt(cipher, key),
        )
        self.assertEqual(keyword_mixed_alphabet(""), "ABCDEFGHIJKLMNOPQRSTUVWXYZ")

    def test_punctuation_does_not_advance_the_key(self) -> None:
        plain = "AB, CD."
        cipher = keyed_vigenere_encrypt(plain, "K", "KRYPTOS", "K")
        self.assertEqual(cipher[2], ",")
        self.assertEqual(cipher[-1], ".")
        self.assertEqual(keyed_vigenere_decrypt(cipher, "K", "KRYPTOS", "K"), plain)


if __name__ == "__main__":
    unittest.main()
