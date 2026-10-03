"""Playfair known-key recovery pinned to the Wikipedia worked example.

Source (fetched 2026-10-02, America/New_York):
https://en.wikipedia.org/wiki/Playfair_cipher

The article's Example section uses keyword ``playfair example`` and message
``hide the gold in the tree stump``. Prepared digraphs insert X between the
repeated E's in TREE. Ciphertext groups are BM OD ZB XD NA BE KU DM UI XM MO
UV IF. This test recovers that prepared plaintext letter-for-letter. It is a
known-cipher check, not a reading of an unknown script.
"""

from __future__ import annotations

import unittest

from engine.solvers import SOLVERS
from engine.solvers.playfair import (
    WIKIPEDIA_CIPHERTEXT,
    WIKIPEDIA_KEYWORD,
    WIKIPEDIA_MESSAGE,
    WIKIPEDIA_PREPARED_PLAINTEXT,
    WIKIPEDIA_SOURCE_URL,
    playfair_decrypt,
    playfair_encrypt,
    playfair_square,
    prepare_playfair_plaintext,
    solve_playfair,
)


class PlayfairSquareTest(unittest.TestCase):
    def test_wikipedia_keyword_square(self) -> None:
        square = playfair_square(WIKIPEDIA_KEYWORD)
        self.assertEqual(square, "PLAYFIREXMBCDGHKNOQSTUVWZ")
        self.assertEqual(len(square), 25)
        self.assertNotIn("J", square)
        # Row-major layout printed in the article.
        rows = [square[i : i + 5] for i in range(0, 25, 5)]
        self.assertEqual(rows, ["PLAYF", "IREXM", "BCDGH", "KNOQS", "TUVWZ"])


class PlayfairWikipediaExampleTest(unittest.TestCase):
    def test_prepare_matches_wikipedia_pairs(self) -> None:
        prepared = prepare_playfair_plaintext(WIKIPEDIA_MESSAGE)
        self.assertEqual(prepared, WIKIPEDIA_PREPARED_PLAINTEXT)
        pairs = [prepared[i : i + 2] for i in range(0, len(prepared), 2)]
        self.assertEqual(
            pairs,
            ["HI", "DE", "TH", "EG", "OL", "DI", "NT", "HE", "TR", "EX", "ES", "TU", "MP"],
        )

    def test_encrypt_published_pairs_to_wikipedia_ciphertext(self) -> None:
        cipher = playfair_encrypt(WIKIPEDIA_MESSAGE, WIKIPEDIA_KEYWORD)
        self.assertEqual(cipher, WIKIPEDIA_CIPHERTEXT)

    def test_decrypt_recovers_prepared_plaintext_exactly(self) -> None:
        plain = playfair_decrypt(WIKIPEDIA_CIPHERTEXT, WIKIPEDIA_KEYWORD)
        self.assertEqual(plain, WIKIPEDIA_PREPARED_PLAINTEXT)

    def test_solver_recovers_wikipedia_plaintext_exactly(self) -> None:
        result = solve_playfair(WIKIPEDIA_CIPHERTEXT, WIKIPEDIA_KEYWORD)
        self.assertEqual(result.plaintext, WIKIPEDIA_PREPARED_PLAINTEXT)
        self.assertEqual(result.method, "playfair")
        self.assertEqual(result.key, "PLAYFAIREXAMPLE")
        self.assertEqual(result.details["square"], "PLAYFIREXMBCDGHKNOQSTUVWZ")
        self.assertEqual(result.details["source_example"], WIKIPEDIA_SOURCE_URL)
        self.assertIn("unknown script", result.details["scope"])
        # Spaced article message is the same letters once the TREE null X is
        # understood as a digraph pad, not part of the English words.
        self.assertTrue(result.plaintext.startswith("HIDETHEGOLDINTHE"))
        self.assertIn("TREXESTUMP", result.plaintext)

    def test_roundtrip_on_wikipedia_message(self) -> None:
        cipher = playfair_encrypt(WIKIPEDIA_MESSAGE, WIKIPEDIA_KEYWORD)
        self.assertEqual(playfair_decrypt(cipher, WIKIPEDIA_KEYWORD), WIKIPEDIA_PREPARED_PLAINTEXT)

    def test_not_registered_as_a_blind_solver(self) -> None:
        self.assertNotIn("playfair", SOLVERS)

    def test_documents_known_cipher_scope(self) -> None:
        import engine.solvers.playfair as playfair_mod

        doc = playfair_mod.__doc__ or ""
        self.assertIn("known-cipher", doc)
        self.assertIn("does **not** read an unknown script", doc)
        self.assertIn(WIKIPEDIA_SOURCE_URL, doc)


if __name__ == "__main__":
    unittest.main()
