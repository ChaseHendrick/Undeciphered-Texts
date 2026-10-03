"""Rail-fence known-key recovery against a published worked example.

Source (fetched 2026-10-02):
http://practicalcryptography.com/ciphers/classical-era/rail-fence/

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.rail_fence import (
    PRACTICAL_CRYPTOGRAPHY_CIPHER,
    PRACTICAL_CRYPTOGRAPHY_KEY,
    PRACTICAL_CRYPTOGRAPHY_PLAIN,
    PRACTICAL_CRYPTOGRAPHY_URL,
    rail_fence_decrypt,
    rail_fence_encrypt,
    solve_rail_fence,
)


CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "rail_fence_certificate.json"


class RailFenceScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.rail_fence as rail_fence_mod

        doc = (rail_fence_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn(
            "practicalcryptography.com/ciphers/classical-era/rail-fence",
            PRACTICAL_CRYPTOGRAPHY_URL,
        )


class RailFencePublishedExampleTest(unittest.TestCase):
    """Practical Cryptography: DEFENDTHEEASTWALLOFTHECASTLE with 3 rails."""

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = rail_fence_encrypt(PRACTICAL_CRYPTOGRAPHY_PLAIN, PRACTICAL_CRYPTOGRAPHY_KEY)
        self.assertEqual(cipher, PRACTICAL_CRYPTOGRAPHY_CIPHER)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_rail_fence(
            PRACTICAL_CRYPTOGRAPHY_CIPHER,
            key=PRACTICAL_CRYPTOGRAPHY_KEY,
        )
        self.assertEqual(result.plaintext, PRACTICAL_CRYPTOGRAPHY_PLAIN)
        self.assertEqual(result.method, "rail_fence")
        self.assertEqual(result.key, PRACTICAL_CRYPTOGRAPHY_KEY)
        self.assertEqual(result.details["source_url"], PRACTICAL_CRYPTOGRAPHY_URL)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_roundtrip_uses_the_published_rail_count(self) -> None:
        again = rail_fence_decrypt(
            rail_fence_encrypt(PRACTICAL_CRYPTOGRAPHY_PLAIN, 3),
            "3",
        )
        self.assertEqual(again, PRACTICAL_CRYPTOGRAPHY_PLAIN)

    def test_second_published_example_on_the_same_page(self) -> None:
        # Same page, key of 4: ciphertext read off along the four rows.
        cipher = rail_fence_encrypt("defend the east wall of the castle", 4)
        self.assertEqual(cipher, "DTTFSEDHSWOTATFNEAALHCLEELEE")
        self.assertEqual(rail_fence_decrypt(cipher, 4), "DEFENDTHEEASTWALLOFTHECASTLE")


class RailFenceCertificateTest(unittest.TestCase):
    """Certificate checks the published Practical Cryptography example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "rail_fence")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["key"], key)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(rail_fence_decrypt(ciphertext, key), plaintext)
        result = solve_rail_fence(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], PRACTICAL_CRYPTOGRAPHY_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown-script", note)
        self.assertIn("nr. 86", note)


if __name__ == "__main__":
    unittest.main()
