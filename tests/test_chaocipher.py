"""Chaocipher known-alphabet recovery against the Programming Praxis vector.

Source (fetched 2026-10-03, America/New_York):
https://programmingpraxis.com/2010/07/06/chaocipher/

Left (ciphertext) HXUCZVAMDSLKPEFJRIGTWOBNYQ.
Right (plaintext) PTLNBQDEOYSFAVZKGJRIHWXUMC.
Plaintext WELLDONEISBETTERTHANWELLSAID.
Ciphertext OAHQHCNYNXTSZJRRHJBYHQKSOUJY.

This is the revealed algorithm's published test vector. It does not claim
that Byrne's challenge exhibits are solved. It does not claim an
unknown-script reading and it is not a claim about Kryptos K4, Zodiac,
Beale, McCormick, Voynich, or army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers import SOLVERS
from engine.solvers.chaocipher import (
    PRAXIS_CIPHER,
    PRAXIS_LEFT,
    PRAXIS_LEFT_AFTER_P,
    PRAXIS_PLAIN,
    PRAXIS_RIGHT,
    PRAXIS_RIGHT_AFTER_A,
    PRAXIS_URL,
    chaocipher_decrypt,
    chaocipher_encrypt,
    permute_left,
    permute_right,
    solve_chaocipher,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "chaocipher_certificate.json"
)


class ChaocipherScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_byrne_exhibits_or_k4(self) -> None:
        import engine.solvers.chaocipher as chao_mod

        doc = (chao_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("byrne", doc)
        self.assertIn("exhibits", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("kryptos k4", doc)
        self.assertIn("voynich", doc)
        self.assertIn("zodiac", doc)
        self.assertIn("beale", doc)
        self.assertIn("mccormick", doc)
        self.assertIn("2010/07/06/chaocipher", PRAXIS_URL)
        self.assertNotIn("chaocipher", SOLVERS)
        self.assertNotIn("\u2014", chao_mod.__doc__ or "")
        self.assertNotIn("\u2013", chao_mod.__doc__ or "")


class ChaocipherPublishedExampleTest(unittest.TestCase):
    """Programming Praxis: the two printed alphabets and WELL DONE..."""

    def test_page_permutation_steps(self) -> None:
        self.assertEqual(permute_left(PRAXIS_LEFT, "P"), PRAXIS_LEFT_AFTER_P)
        self.assertEqual(permute_right(PRAXIS_RIGHT, "A"), PRAXIS_RIGHT_AFTER_A)
        self.assertEqual(len(PRAXIS_LEFT_AFTER_P), 26)
        self.assertEqual(len(PRAXIS_RIGHT_AFTER_A), 26)
        self.assertEqual(set(PRAXIS_LEFT_AFTER_P), set(PRAXIS_LEFT))
        self.assertEqual(set(PRAXIS_RIGHT_AFTER_A), set(PRAXIS_RIGHT))

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = chaocipher_encrypt(PRAXIS_PLAIN, PRAXIS_LEFT, PRAXIS_RIGHT)
        self.assertEqual(cipher, PRAXIS_CIPHER)
        self.assertEqual(
            chaocipher_encrypt(PRAXIS_PLAIN.lower(), PRAXIS_LEFT.lower(), PRAXIS_RIGHT.lower()),
            PRAXIS_CIPHER,
        )
        self.assertEqual(len(cipher), len(PRAXIS_PLAIN))

    def test_decrypt_recovers_published_plaintext_exactly(self) -> None:
        plain = chaocipher_decrypt(PRAXIS_CIPHER, PRAXIS_LEFT, PRAXIS_RIGHT)
        self.assertEqual(plain, PRAXIS_PLAIN)
        spaced = " ".join(PRAXIS_CIPHER[i : i + 5] for i in range(0, len(PRAXIS_CIPHER), 5))
        self.assertEqual(chaocipher_decrypt(spaced, PRAXIS_LEFT, PRAXIS_RIGHT), PRAXIS_PLAIN)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_chaocipher(PRAXIS_CIPHER, left=PRAXIS_LEFT, right=PRAXIS_RIGHT)
        self.assertEqual(result.plaintext, PRAXIS_PLAIN)
        self.assertEqual(result.method, "chaocipher")
        self.assertEqual(result.key, f"{PRAXIS_LEFT}|{PRAXIS_RIGHT}")
        self.assertEqual(result.details["left"], PRAXIS_LEFT)
        self.assertEqual(result.details["right"], PRAXIS_RIGHT)
        self.assertEqual(result.details["source_url"], PRAXIS_URL)
        self.assertEqual(result.details["mode"], "known_alphabets")
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not a claim that byrne", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)
        self.assertIn("kryptos k4", scope)
        self.assertIn("voynich", scope)
        self.assertIn("zodiac", scope)
        self.assertIn("beale", scope)
        self.assertIn("mccormick", scope)

    def test_roundtrip_uses_the_starting_alphabets(self) -> None:
        again = chaocipher_decrypt(
            chaocipher_encrypt(PRAXIS_PLAIN, PRAXIS_LEFT, PRAXIS_RIGHT),
            PRAXIS_LEFT,
            PRAXIS_RIGHT,
        )
        self.assertEqual(again, PRAXIS_PLAIN)

    def test_bad_alphabet_and_empty_text_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            chaocipher_encrypt(PRAXIS_PLAIN, "ABC", PRAXIS_RIGHT)
        with self.assertRaises(ValueError):
            chaocipher_decrypt(PRAXIS_CIPHER, PRAXIS_LEFT, "A" * 26)
        with self.assertRaises(ValueError):
            chaocipher_encrypt("...", PRAXIS_LEFT, PRAXIS_RIGHT)
        with self.assertRaises(ValueError):
            chaocipher_decrypt("", PRAXIS_LEFT, PRAXIS_RIGHT)
        with self.assertRaises(ValueError):
            solve_chaocipher(PRAXIS_CIPHER, left=PRAXIS_LEFT, right="---")


class ChaocipherCertificateTest(unittest.TestCase):
    """Certificate checks the published Programming Praxis vector, not Byrne's exhibits."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "chaocipher")
        self.assertEqual(self.cert["name"], "chaocipher")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        left = self.cert["keys"]["left"]
        right = self.cert["keys"]["right"]
        self.assertEqual(plaintext, PRAXIS_PLAIN)
        self.assertEqual(ciphertext, PRAXIS_CIPHER)
        self.assertEqual(self.cert["key"], f"{left}|{right}")
        self.assertEqual(left, PRAXIS_LEFT)
        self.assertEqual(right, PRAXIS_RIGHT)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(chaocipher_decrypt(ciphertext, left, right), plaintext)
        self.assertEqual(chaocipher_encrypt(plaintext, left, right), ciphertext)
        result = solve_chaocipher(ciphertext, left=left, right=right)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], PRAXIS_URL)
        note = self.cert["note"].lower()
        self.assertIn("not a claim that byrne", note)
        self.assertIn("exhibits", note)
        self.assertIn("not an unknown script", note)
        self.assertIn("nr. 86", note)
        self.assertIn("kryptos k4", note)
        self.assertIn("voynich", note)
        self.assertIn("zodiac", note)
        self.assertIn("beale", note)
        self.assertIn("mccormick", note)
        blob = CERT_PATH.read_text(encoding="utf-8")
        self.assertNotIn("\u2014", blob)
        self.assertNotIn("\u2013", blob)
        self.assertNotIn("\u2014", plaintext)
        self.assertNotIn("\u2013", plaintext)


if __name__ == "__main__":
    unittest.main()
