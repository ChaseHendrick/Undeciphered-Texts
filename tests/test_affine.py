"""Affine known-key recovery against a published worked example.

Source (fetched 2026-10-02): https://en.wikipedia.org/wiki/Affine_cipher

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.affine import (
    WIKIPEDIA_A,
    WIKIPEDIA_B,
    WIKIPEDIA_CIPHER,
    WIKIPEDIA_PLAIN,
    WIKIPEDIA_URL,
    affine_decrypt,
    affine_encrypt,
    solve_affine,
)


CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "affine_certificate.json"


class AffineScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.affine as affine_mod

        doc = (affine_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertEqual(WIKIPEDIA_URL, "https://en.wikipedia.org/wiki/Affine_cipher")


class AffinePublishedExampleTest(unittest.TestCase):
    """Wikipedia: AFFINE CIPHER, a=5, b=8 → IHHWVCSWFRCP."""

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = affine_encrypt(WIKIPEDIA_PLAIN, WIKIPEDIA_A, WIKIPEDIA_B)
        self.assertEqual(cipher, WIKIPEDIA_CIPHER)
        # The page's encryption table starts A, F, F, I → I, H, H, W.
        self.assertEqual(cipher[:4], "IHHW")

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_affine(WIKIPEDIA_CIPHER, a=WIKIPEDIA_A, b=WIKIPEDIA_B)
        self.assertEqual(result.plaintext, WIKIPEDIA_PLAIN)
        self.assertEqual(result.method, "affine")
        self.assertEqual(result.key, "a=5,b=8")
        self.assertEqual(result.details["a"], 5)
        self.assertEqual(result.details["b"], 8)
        self.assertEqual(result.details["a_inverse"], 21)
        self.assertEqual(result.details["source_url"], WIKIPEDIA_URL)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_roundtrip_returns_plaintext(self) -> None:
        again = affine_decrypt(affine_encrypt(WIKIPEDIA_PLAIN, 5, 8), 5, 8)
        self.assertEqual(again, WIKIPEDIA_PLAIN)


class AffineCertificateTest(unittest.TestCase):
    """Certificate checks the published Wikipedia example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "affine")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(key, "a=5,b=8")
        self.assertEqual(self.cert["keys"]["a"], 5)
        self.assertEqual(self.cert["keys"]["b"], 8)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(
            affine_decrypt(ciphertext, self.cert["keys"]["a"], self.cert["keys"]["b"]),
            plaintext,
        )
        result = solve_affine(ciphertext, a=self.cert["keys"]["a"], b=self.cert["keys"]["b"])
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], WIKIPEDIA_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown script", note)
        self.assertIn("nr. 86", note)


if __name__ == "__main__":
    unittest.main()
