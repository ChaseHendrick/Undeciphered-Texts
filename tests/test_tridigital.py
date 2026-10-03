"""Tridigital known-key recovery against a published worked example.

Source (fetched 2026-10-02):
https://www.cryptogram.org/downloads/aca.info/ciphers/Tridigital.pdf

A second published walk-through is checked for encryption:
https://sites.google.com/site/cryptocrackprogram/user-guide/cipher-types/other/tridigital

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.tridigital import (
    ACA_TRIDIGITAL_CIPHER,
    ACA_TRIDIGITAL_CIPHER_GROUPED,
    ACA_TRIDIGITAL_DIGIT_KEY,
    ACA_TRIDIGITAL_KEY,
    ACA_TRIDIGITAL_PLAIN,
    ACA_TRIDIGITAL_URL,
    CRYPTOCRACK_TRIDIGITAL_CIPHER,
    CRYPTOCRACK_TRIDIGITAL_KEY,
    CRYPTOCRACK_TRIDIGITAL_PLAIN,
    CRYPTOCRACK_TRIDIGITAL_URL,
    column_letters,
    digit_key_from_keyword,
    solve_tridigital,
    tridigital_decrypt,
    tridigital_encrypt,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "tridigital_certificate.json"
)


class TridigitalScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.tridigital as tridigital_mod

        doc = (tridigital_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("known-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("Tridigital.pdf", ACA_TRIDIGITAL_URL)


class TridigitalPublishedExampleTest(unittest.TestCase):
    """ACA sheet: NOVELCRAFT, DRAGONFLY, the ides of march."""

    def test_digit_key_matches_the_published_numbering(self) -> None:
        # A=1, C=2, E=3, F=4, L=5, N=6, O=7, R=8, T=9, V=0.
        self.assertEqual(
            digit_key_from_keyword("NOVELCRAFT"),
            ACA_TRIDIGITAL_DIGIT_KEY,
        )
        self.assertEqual(ACA_TRIDIGITAL_DIGIT_KEY, "6703528149")

    def test_square_matches_the_published_columns(self) -> None:
        digits, columns, separator = column_letters("NOVELCRAFT", "DRAGONFLY")
        self.assertEqual(digits, "6703528149")
        self.assertEqual(separator, "9")
        self.assertEqual(columns["6"], "DBQ")
        self.assertEqual(columns["0"], "AET")
        self.assertEqual(columns["4"], "YP")

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = tridigital_encrypt("the ides of march", ACA_TRIDIGITAL_KEY)
        self.assertEqual(cipher, ACA_TRIDIGITAL_CIPHER)
        self.assertEqual(cipher, "03095607958910773")

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_tridigital(ACA_TRIDIGITAL_CIPHER, key=ACA_TRIDIGITAL_KEY)
        self.assertEqual(result.plaintext, ACA_TRIDIGITAL_PLAIN)
        self.assertEqual(result.plaintext, "THE IDES OF MARCH")
        self.assertEqual(result.method, "tridigital")
        self.assertEqual(result.key, ACA_TRIDIGITAL_KEY)
        self.assertEqual(result.details["source_url"], ACA_TRIDIGITAL_URL)
        self.assertEqual(result.details["digit_key"], "6703528149")
        self.assertEqual(result.details["separator"], "9")
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_grouped_ciphertext_decrypts_to_the_same_sentence(self) -> None:
        # The sheet prints the ciphertext in groups of five, with a final period.
        self.assertEqual(
            tridigital_decrypt(ACA_TRIDIGITAL_CIPHER_GROUPED, ACA_TRIDIGITAL_KEY),
            ACA_TRIDIGITAL_PLAIN,
        )

    def test_cryptocrack_published_example_encrypts(self) -> None:
        # Encryption check only. "GO" shares its columns with the more
        # frequent word "UP", so the ranked reading is not that sentence.
        cipher = tridigital_encrypt(
            "Some cause happiness wherever they go others whenever they go.",
            CRYPTOCRACK_TRIDIGITAL_KEY,
        )
        self.assertEqual(cipher, CRYPTOCRACK_TRIDIGITAL_CIPHER)
        self.assertIn("tridigital", CRYPTOCRACK_TRIDIGITAL_URL)
        self.assertIn("GO", CRYPTOCRACK_TRIDIGITAL_PLAIN)

    def test_bad_key_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            tridigital_decrypt(ACA_TRIDIGITAL_CIPHER, "CAT")
        with self.assertRaises(ValueError):
            tridigital_decrypt(ACA_TRIDIGITAL_CIPHER, "NOVELCRAFT")


class TridigitalCertificateTest(unittest.TestCase):
    """Certificate checks the published ACA example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "tridigital")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["digit_keyword"], "NOVELCRAFT")
        self.assertEqual(self.cert["keys"]["alphabet_keyword"], "DRAGONFLY")
        self.assertEqual(key, "NOVELCRAFT|DRAGONFLY")
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(tridigital_decrypt(ciphertext, key), plaintext)
        result = solve_tridigital(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], ACA_TRIDIGITAL_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown-script", note)
        self.assertIn("nr. 86", note)


if __name__ == "__main__":
    unittest.main()
