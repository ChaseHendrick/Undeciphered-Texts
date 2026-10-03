"""Certificate check for the lumen braid.

The plaintext was written for this test. Decrypting the certificate
ciphertext and matching its SHA-256 does not read an ancient script and
does not read army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.lumen_braid import (
    CIPHER_NAME,
    NOT_A_DECIPHERMENT,
    decrypt,
    encrypt,
)


CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "lumen_braid_certificate.json"


class LumenBraidCertificateTest(unittest.TestCase):
    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], CIPHER_NAME)
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(decrypt(ciphertext), plaintext)
        self.assertEqual(encrypt(plaintext), ciphertext)
        self.assertIn("Not a reading of an ancient script", NOT_A_DECIPHERMENT)
        self.assertIn("Nr. 86", NOT_A_DECIPHERMENT)

    def test_roundtrip_covers_short_tails(self) -> None:
        for text in ("", "A", "ab", "abc", "abcd", "Hello, world!", "a1b2c3"):
            self.assertEqual(decrypt(encrypt(text)), text)


if __name__ == "__main__":
    unittest.main()
