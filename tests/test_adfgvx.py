"""ADFGVX known-key recovery pinned to the Wikipedia worked example.

Source (fetched 2026-10-02, America/New_York):
https://en.wikipedia.org/wiki/ADFGVX_cipher

The article's ADFGVX section (the 6×6 cipher, not the earlier 5×5 ADFGX
example) uses fractionation keyword ``nachtbommenwerper`` and transposition
keyword ``PRIVACY``. The message is ``attack at 1200am``. Ciphertext groups
are DGDD DAGD DGAF ADDF DADV DVFA ADVX. This test recovers that plaintext
letter-for-letter as the enciphered stream ``ATTACKAT1200AM`` (spaces are
not in the cipher alphabet). It is a known-cipher check, not a reading of
an unknown script.
"""

from __future__ import annotations

import unittest

from engine.solvers import SOLVERS
from engine.solvers.adfgvx import (
    WIKIPEDIA_CIPHERTEXT,
    WIKIPEDIA_FRACTIONATION_KEYWORD,
    WIKIPEDIA_MESSAGE,
    WIKIPEDIA_PLAINTEXT,
    WIKIPEDIA_SOURCE_URL,
    WIKIPEDIA_SQUARE,
    WIKIPEDIA_TRANSPOSITION_KEY,
    adfgvx_decrypt,
    adfgvx_encrypt,
    solve_adfgvx,
    square_from_fractionation_keyword,
)


class AdfgvxSquareTest(unittest.TestCase):
    def test_wikipedia_keyword_square(self) -> None:
        square = square_from_fractionation_keyword(WIKIPEDIA_FRACTIONATION_KEYWORD)
        self.assertEqual(square, WIKIPEDIA_SQUARE)
        self.assertEqual(len(square), 36)
        rows = [square[i : i + 6] for i in range(0, 36, 6)]
        self.assertEqual(
            rows,
            ["NA1C3H", "8TB2OM", "E5WRPD", "4F6G7I", "9J0KLQ", "SUVXYZ"],
        )


class AdfgvxWikipediaExampleTest(unittest.TestCase):
    def test_encrypt_published_message_to_wikipedia_ciphertext(self) -> None:
        cipher = adfgvx_encrypt(
            WIKIPEDIA_MESSAGE,
            WIKIPEDIA_TRANSPOSITION_KEY,
            fractionation_keyword=WIKIPEDIA_FRACTIONATION_KEYWORD,
        )
        self.assertEqual(cipher, WIKIPEDIA_CIPHERTEXT)
        groups = [cipher[i : i + 4] for i in range(0, len(cipher), 4)]
        self.assertEqual(
            groups,
            ["DGDD", "DAGD", "DGAF", "ADDF", "DADV", "DVFA", "ADVX"],
        )

    def test_decrypt_recovers_plaintext_exactly(self) -> None:
        plain = adfgvx_decrypt(
            WIKIPEDIA_CIPHERTEXT,
            WIKIPEDIA_TRANSPOSITION_KEY,
            fractionation_keyword=WIKIPEDIA_FRACTIONATION_KEYWORD,
        )
        self.assertEqual(plain, WIKIPEDIA_PLAINTEXT)
        self.assertEqual(plain, "ATTACKAT1200AM")

    def test_decrypt_with_explicit_square_recovers_plaintext_exactly(self) -> None:
        plain = adfgvx_decrypt(
            "DGDD DAGD DGAF ADDF DADV DVFA ADVX",
            WIKIPEDIA_TRANSPOSITION_KEY,
            square=WIKIPEDIA_SQUARE,
        )
        self.assertEqual(plain, WIKIPEDIA_PLAINTEXT)

    def test_solver_recovers_wikipedia_plaintext_exactly(self) -> None:
        result = solve_adfgvx(
            WIKIPEDIA_CIPHERTEXT,
            WIKIPEDIA_TRANSPOSITION_KEY,
            fractionation_keyword=WIKIPEDIA_FRACTIONATION_KEYWORD,
        )
        self.assertEqual(result.plaintext, WIKIPEDIA_PLAINTEXT)
        self.assertEqual(result.method, "adfgvx")
        self.assertEqual(result.key, "PRIVACY")
        self.assertEqual(result.details["square"], WIKIPEDIA_SQUARE)
        self.assertEqual(result.details["source_example"], WIKIPEDIA_SOURCE_URL)
        self.assertIn("unknown script", result.details["scope"])
        self.assertIn("known-key", result.details["scope"])

    def test_roundtrip_on_wikipedia_message(self) -> None:
        cipher = adfgvx_encrypt(
            WIKIPEDIA_MESSAGE,
            WIKIPEDIA_TRANSPOSITION_KEY,
            square=WIKIPEDIA_SQUARE,
        )
        self.assertEqual(
            adfgvx_decrypt(cipher, WIKIPEDIA_TRANSPOSITION_KEY, square=WIKIPEDIA_SQUARE),
            WIKIPEDIA_PLAINTEXT,
        )

    def test_short_last_row_roundtrip(self) -> None:
        # 5 symbols → 10 fractionated letters, key width 4, so the last row
        # fills only the first two columns. Not part of the Wikipedia fixture.
        message = "NIGHT"
        key = "CARGO"
        cipher = adfgvx_encrypt(message, key, square=WIKIPEDIA_SQUARE)
        self.assertEqual(
            adfgvx_decrypt(cipher, key, square=WIKIPEDIA_SQUARE),
            message,
        )

    def test_not_registered_as_a_blind_solver(self) -> None:
        self.assertNotIn("adfgvx", SOLVERS)

    def test_documents_known_cipher_scope(self) -> None:
        import engine.solvers.adfgvx as adfgvx_mod

        doc = adfgvx_mod.__doc__ or ""
        self.assertIn("known-cipher", doc)
        self.assertIn("does **not** read an unknown script", doc)
        self.assertIn(WIKIPEDIA_SOURCE_URL, doc)


if __name__ == "__main__":
    unittest.main()
