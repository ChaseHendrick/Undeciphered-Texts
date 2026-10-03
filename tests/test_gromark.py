"""Gromark known-key recovery against a published worked example.

Source (fetched 2026-10-02):
https://www.cryptogram.org/downloads/aca.info/ciphers/Gromark.pdf

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.gromark import (
    ACA_GROMARK_ALPHABET,
    ACA_GROMARK_CIPHER,
    ACA_GROMARK_KEY,
    ACA_GROMARK_PLAIN,
    ACA_GROMARK_RUNNING_KEY,
    ACA_GROMARK_URL,
    gromark_cipher_alphabet,
    gromark_decrypt,
    gromark_encrypt,
    gromark_running_key,
    solve_gromark,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "gromark_certificate.json"
)


class GromarkScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.gromark as gromark_mod

        doc = (gromark_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn(
            "cryptogram.org/downloads/aca.info/ciphers/gromark.pdf",
            ACA_GROMARK_URL.lower(),
        )


class GromarkPublishedExampleTest(unittest.TestCase):
    """ACA sheet: ENIGMA, primer 23452, THEREARE... -> NFYCK..."""

    def test_cipher_alphabet_matches_the_published_block(self) -> None:
        self.assertEqual(gromark_cipher_alphabet("ENIGMA"), ACA_GROMARK_ALPHABET)

    def test_running_key_matches_the_published_digits(self) -> None:
        self.assertEqual(
            gromark_running_key("23452", len(ACA_GROMARK_PLAIN)),
            ACA_GROMARK_RUNNING_KEY,
        )

    def test_first_lookup_matches_the_published_walkthrough(self) -> None:
        # Plaintext T, first primer digit 2, cipher alphabet under V is N.
        self.assertEqual(gromark_encrypt("T", ACA_GROMARK_KEY), "N")

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = gromark_encrypt(ACA_GROMARK_PLAIN, ACA_GROMARK_KEY)
        self.assertEqual(cipher, ACA_GROMARK_CIPHER)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_gromark(ACA_GROMARK_CIPHER, key=ACA_GROMARK_KEY)
        self.assertEqual(result.plaintext, ACA_GROMARK_PLAIN)
        self.assertEqual(result.method, "gromark")
        self.assertEqual(result.key, ACA_GROMARK_KEY)
        self.assertEqual(result.details["source_url"], ACA_GROMARK_URL)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_roundtrip_accepts_a_lowercase_keyword(self) -> None:
        again = gromark_decrypt(
            gromark_encrypt(ACA_GROMARK_PLAIN, "enigma 23452"),
            ACA_GROMARK_KEY,
        )
        self.assertEqual(again, ACA_GROMARK_PLAIN)

    def test_primer_that_is_not_five_digits_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            gromark_decrypt(ACA_GROMARK_CIPHER, "ENIGMA 234")


class GromarkCertificateTest(unittest.TestCase):
    """Certificate checks the published ACA example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "gromark")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["key"], key)
        self.assertEqual(self.cert["keys"]["keyword"], "ENIGMA")
        self.assertEqual(self.cert["keys"]["primer"], "23452")
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(gromark_decrypt(ciphertext, key), plaintext)
        result = solve_gromark(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], ACA_GROMARK_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown-script", note)
        self.assertIn("nr. 86", note)


if __name__ == "__main__":
    unittest.main()
