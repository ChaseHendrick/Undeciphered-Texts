"""Four-square known-key recovery pinned to the Wikipedia worked example.

Source (fetched 2026-10-02, America/New_York):
https://en.wikipedia.org/wiki/Four-square_cipher

The article uses keywords ``example`` and ``keyword`` (Q omitted; I and J
distinct). Plaintext digraphs are ``he lp me ob iw an ke no bi``. Ciphertext
groups are ``FY GM KY HO BX MF KK KI MD``. This test recovers that plaintext
letter-for-letter. It is a known-cipher check, not a reading of an unknown
script, and not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers import SOLVERS
from engine.solvers.four_square import (
    PLAIN_ALPHABET,
    WIKIPEDIA_CIPHERTEXT,
    WIKIPEDIA_LOWER_LEFT_KEYWORD,
    WIKIPEDIA_MESSAGE,
    WIKIPEDIA_PLAINTEXT,
    WIKIPEDIA_SOURCE_URL,
    WIKIPEDIA_UPPER_RIGHT_KEYWORD,
    four_square_decrypt,
    four_square_encrypt,
    solve_four_square,
    square_from_keyword,
)


class FourSquareSquareTest(unittest.TestCase):
    def test_wikipedia_keyword_squares(self) -> None:
        upper = square_from_keyword(WIKIPEDIA_UPPER_RIGHT_KEYWORD)
        lower = square_from_keyword(WIKIPEDIA_LOWER_LEFT_KEYWORD)
        self.assertEqual(upper, "EXAMPLBCDFGHIJKNORSTUVWYZ")
        self.assertEqual(lower, "KEYWORDABCFGHIJLMNPSTUVXZ")
        self.assertEqual(len(upper), 25)
        self.assertEqual(len(set(upper)), 25)
        self.assertNotIn("Q", upper)
        self.assertNotIn("Q", lower)
        self.assertNotIn("Q", PLAIN_ALPHABET)
        self.assertEqual(
            [upper[i : i + 5] for i in range(0, 25, 5)],
            ["EXAMP", "LBCDF", "GHIJK", "NORST", "UVWYZ"],
        )
        self.assertEqual(
            [lower[i : i + 5] for i in range(0, 25, 5)],
            ["KEYWO", "RDABC", "FGHIJ", "LMNPS", "TUVXZ"],
        )


class FourSquareWikipediaExampleTest(unittest.TestCase):
    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = four_square_encrypt(
            WIKIPEDIA_MESSAGE,
            WIKIPEDIA_UPPER_RIGHT_KEYWORD,
            WIKIPEDIA_LOWER_LEFT_KEYWORD,
        )
        self.assertEqual(cipher, WIKIPEDIA_CIPHERTEXT)
        self.assertEqual(cipher, "FYGMKYHOBXMFKKKIMD")

    def test_decrypt_recovers_published_plaintext_exactly(self) -> None:
        plain = four_square_decrypt(
            WIKIPEDIA_CIPHERTEXT,
            WIKIPEDIA_UPPER_RIGHT_KEYWORD,
            WIKIPEDIA_LOWER_LEFT_KEYWORD,
        )
        self.assertEqual(plain, WIKIPEDIA_PLAINTEXT)
        self.assertEqual(plain, "HELPMEOBIWANKENOBI")

    def test_solver_recovers_wikipedia_plaintext_exactly(self) -> None:
        result = solve_four_square(
            WIKIPEDIA_CIPHERTEXT,
            WIKIPEDIA_UPPER_RIGHT_KEYWORD,
            WIKIPEDIA_LOWER_LEFT_KEYWORD,
        )
        self.assertEqual(result.plaintext, WIKIPEDIA_PLAINTEXT)
        self.assertEqual(result.method, "four_square")
        self.assertEqual(result.key, "EXAMPLE/KEYWORD")
        self.assertEqual(result.details["upper_right_square"], "EXAMPLBCDFGHIJKNORSTUVWYZ")
        self.assertEqual(result.details["lower_left_square"], "KEYWORDABCFGHIJLMNPSTUVXZ")
        self.assertEqual(result.details["source_example"], WIKIPEDIA_SOURCE_URL)
        self.assertIn("unknown script", result.details["scope"])
        self.assertIn("Nr. 86", result.details["scope"])

    def test_not_registered_as_a_blind_solver(self) -> None:
        self.assertNotIn("four_square", SOLVERS)
        self.assertNotIn("four-square", SOLVERS)

    def test_documents_known_cipher_scope(self) -> None:
        import engine.solvers.four_square as mod

        doc = mod.__doc__ or ""
        self.assertIn("known-cipher", doc)
        self.assertIn("does **not** read an unknown script", doc)
        self.assertIn("Nr. 86", doc)
        self.assertIn(WIKIPEDIA_SOURCE_URL, doc)


CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "four_square_certificate.json"


class FourSquareCertificateTest(unittest.TestCase):
    """Certificate checks the published Wikipedia example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "four-square")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        keys = self.cert["keys"]
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(self.cert["source_url"], WIKIPEDIA_SOURCE_URL)
        recovered = four_square_decrypt(
            ciphertext,
            keys["upper_right_keyword"],
            keys["lower_left_keyword"],
        )
        self.assertEqual(recovered, plaintext)
        self.assertEqual(recovered, WIKIPEDIA_PLAINTEXT)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown script", note)
        self.assertIn("nr. 86", note)
        self.assertIn("known-cipher", note)


if __name__ == "__main__":
    unittest.main()
