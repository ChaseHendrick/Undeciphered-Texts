"""Gronsfeld known-key recovery against a published worked example.

Source (fetched 2026-10-02):
https://caesarcipher.org/learn/gronsfeld-cipher-numeric-key-vigenere-variant-guide

The page encrypts "ATTACK AT DAWN" with key 3 1 4 1 5. Spaces are removed
before the shifts, so the plaintext letter stream is ATTACKATDAWN and the
ciphertext letter stream is DUXBHNBXEFZO.

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.gronsfeld import (
    CAESARCIPHER_ORG_CIPHER,
    CAESARCIPHER_ORG_KEY,
    CAESARCIPHER_ORG_PLAIN,
    CAESARCIPHER_ORG_URL,
    gronsfeld_decrypt,
    gronsfeld_encrypt,
    gronsfeld_substitute,
    solve_gronsfeld,
)


CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "gronsfeld_certificate.json"


class GronsfeldScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.gronsfeld as gronsfeld_mod

        doc = (gronsfeld_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("caesarcipher.org/learn/gronsfeld-cipher", CAESARCIPHER_ORG_URL)


class GronsfeldPublishedExampleTest(unittest.TestCase):
    """CaesarCipher.org: ATTACKATDAWN + 31415 → DUXBHNBXEFZO."""

    def test_first_lookup_matches_the_published_walkthrough(self) -> None:
        # Page table: plaintext A with key digit 3 yields ciphertext D.
        self.assertEqual(gronsfeld_substitute("A", 3), "D")

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = gronsfeld_encrypt(CAESARCIPHER_ORG_PLAIN, CAESARCIPHER_ORG_KEY)
        self.assertEqual(cipher, CAESARCIPHER_ORG_CIPHER)
        spaced = gronsfeld_encrypt("ATTACK AT DAWN", "3 1 4 1 5")
        self.assertEqual(spaced, CAESARCIPHER_ORG_CIPHER)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_gronsfeld(CAESARCIPHER_ORG_CIPHER, key=CAESARCIPHER_ORG_KEY)
        self.assertEqual(result.plaintext, CAESARCIPHER_ORG_PLAIN)
        self.assertEqual(result.plaintext, "ATTACKATDAWN")
        self.assertEqual(result.method, "gronsfeld")
        self.assertEqual(result.key, CAESARCIPHER_ORG_KEY)
        self.assertEqual(result.details["source_url"], CAESARCIPHER_ORG_URL)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_decrypt_undoes_encrypt(self) -> None:
        again = gronsfeld_decrypt(
            gronsfeld_encrypt(CAESARCIPHER_ORG_PLAIN, CAESARCIPHER_ORG_KEY),
            "3 1 4 1 5",
        )
        self.assertEqual(again, CAESARCIPHER_ORG_PLAIN)


class GronsfeldCertificateTest(unittest.TestCase):
    """Certificate checks the published CaesarCipher.org example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "gronsfeld")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["key"], key)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(gronsfeld_decrypt(ciphertext, key), plaintext)
        result = solve_gronsfeld(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], CAESARCIPHER_ORG_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown script", note)
        self.assertIn("nr. 86", note)


if __name__ == "__main__":
    unittest.main()
