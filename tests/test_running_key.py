"""Running-key known-key recovery against a published worked example.

Source (fetched 2026-10-02):
http://practicalcryptography.com/ciphers/classical-era/running-key/

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.running_key import (
    PRACTICAL_CRYPTOGRAPHY_CIPHER,
    PRACTICAL_CRYPTOGRAPHY_KEY,
    PRACTICAL_CRYPTOGRAPHY_PLAIN,
    PRACTICAL_CRYPTOGRAPHY_URL,
    running_key_decrypt,
    running_key_encrypt,
    solve_running_key,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "running_key_certificate.json"
)


class RunningKeyScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.running_key as running_key_mod

        doc = (running_key_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn(
            "practicalcryptography.com/ciphers/classical-era/running-key",
            PRACTICAL_CRYPTOGRAPHY_URL,
        )


class RunningKeyPublishedExampleTest(unittest.TestCase):
    """Practical Cryptography: DEFENDTHEEAST... + HOWDOESTHEDUCK... -> KSBHBH..."""

    def test_first_lookup_matches_the_published_walkthrough(self) -> None:
        # Page: plaintext D with key letter H yields ciphertext K.
        self.assertEqual(running_key_encrypt("D", "H"), "K")

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = running_key_encrypt(
            PRACTICAL_CRYPTOGRAPHY_PLAIN, PRACTICAL_CRYPTOGRAPHY_KEY
        )
        self.assertEqual(cipher, PRACTICAL_CRYPTOGRAPHY_CIPHER)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_running_key(
            PRACTICAL_CRYPTOGRAPHY_CIPHER, key=PRACTICAL_CRYPTOGRAPHY_KEY
        )
        self.assertEqual(result.plaintext, PRACTICAL_CRYPTOGRAPHY_PLAIN)
        self.assertEqual(result.method, "running_key")
        self.assertEqual(result.key, PRACTICAL_CRYPTOGRAPHY_KEY)
        self.assertEqual(result.details["source_url"], PRACTICAL_CRYPTOGRAPHY_URL)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_roundtrip_does_not_repeat_a_short_keyword(self) -> None:
        again = running_key_decrypt(
            running_key_encrypt(
                PRACTICAL_CRYPTOGRAPHY_PLAIN, "how does the duck know that? said Victor"
            ),
            PRACTICAL_CRYPTOGRAPHY_KEY,
        )
        self.assertEqual(again, PRACTICAL_CRYPTOGRAPHY_PLAIN)

    def test_key_shorter_than_the_text_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            running_key_decrypt(PRACTICAL_CRYPTOGRAPHY_CIPHER, "HOW")


class RunningKeyCertificateTest(unittest.TestCase):
    """Certificate checks the published Practical Cryptography example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "running_key")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["key"], key)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(running_key_decrypt(ciphertext, key), plaintext)
        result = solve_running_key(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], PRACTICAL_CRYPTOGRAPHY_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown-script", note)
        self.assertIn("nr. 86", note)


if __name__ == "__main__":
    unittest.main()
