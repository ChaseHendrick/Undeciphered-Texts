"""Vigenère autokey known-key recovery against a published worked example.

Source (fetched 2026-10-02): http://practicalcryptography.com/ciphers/autokey-cipher/

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.autokey import (
    PRACTICAL_CRYPTOGRAPHY_CIPHER,
    PRACTICAL_CRYPTOGRAPHY_KEY,
    PRACTICAL_CRYPTOGRAPHY_PLAIN,
    PRACTICAL_CRYPTOGRAPHY_URL,
    autokey_decrypt,
    autokey_encrypt,
    solve_autokey,
)


CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "autokey_certificate.json"


class AutokeyScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.autokey as autokey_mod

        doc = (autokey_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("practicalcryptography.com/ciphers/autokey-cipher", PRACTICAL_CRYPTOGRAPHY_URL)


class AutokeyPublishedExampleTest(unittest.TestCase):
    """Practical Cryptography: DEFENDTHEEASTWALLOFTHECASTLE + FORTIFICATION → ISWXVI…"""

    def test_first_lookup_matches_the_published_walkthrough(self) -> None:
        # Page: plaintext D with key letter F yields ciphertext I.
        self.assertEqual(autokey_encrypt("D", "F"), "I")

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = autokey_encrypt(PRACTICAL_CRYPTOGRAPHY_PLAIN, PRACTICAL_CRYPTOGRAPHY_KEY)
        self.assertEqual(cipher, PRACTICAL_CRYPTOGRAPHY_CIPHER)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_autokey(PRACTICAL_CRYPTOGRAPHY_CIPHER, key=PRACTICAL_CRYPTOGRAPHY_KEY)
        self.assertEqual(result.plaintext, PRACTICAL_CRYPTOGRAPHY_PLAIN)
        self.assertEqual(result.method, "autokey")
        self.assertEqual(result.key, PRACTICAL_CRYPTOGRAPHY_KEY)
        self.assertEqual(result.details["source_url"], PRACTICAL_CRYPTOGRAPHY_URL)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_roundtrip_uses_primer_then_plaintext(self) -> None:
        again = autokey_decrypt(
            autokey_encrypt(PRACTICAL_CRYPTOGRAPHY_PLAIN, PRACTICAL_CRYPTOGRAPHY_KEY),
            "fortification",
        )
        self.assertEqual(again, PRACTICAL_CRYPTOGRAPHY_PLAIN)

    def test_second_published_example_on_the_same_page(self) -> None:
        # pycipher snippet on the same page: primer HELLO.
        cipher = autokey_encrypt("defend the east wall of the castle", "HELLO")
        self.assertEqual(cipher, "KIQPBGXMIRDLAAELDHBTSPQFLAPG")
        self.assertEqual(autokey_decrypt(cipher, "HELLO"), "DEFENDTHEEASTWALLOFTHECASTLE")


class AutokeyCertificateTest(unittest.TestCase):
    """Certificate checks the published Practical Cryptography example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "autokey")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["key"], key)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(autokey_decrypt(ciphertext, key), plaintext)
        result = solve_autokey(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], PRACTICAL_CRYPTOGRAPHY_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown-script", note)
        self.assertIn("nr. 86", note)


if __name__ == "__main__":
    unittest.main()
