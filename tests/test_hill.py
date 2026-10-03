"""2x2 Hill known-key recovery against a published worked example.

Source (fetched 2026-10-02):
https://www.math.auckland.ac.nz/~slinko/Talks/AfC.pdf

Arkadii Slinko, Algebra for Cryptology (University of Auckland,
6 April 2013), "Hill's cryptosystem. Example 2": key
[[3, 3], [2, 5]] sends HELP to HIAT. Example 3 decrypts HIAT
back to HELP.

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.hill import (
    SLINKO_CIPHER,
    SLINKO_KEY,
    SLINKO_PLAIN,
    SLINKO_URL,
    hill_decrypt,
    hill_encrypt,
    hill_inverse,
    solve_hill,
)


CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "hill_certificate.json"


class HillScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.hill as hill_mod

        doc = (hill_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("math.auckland.ac.nz/~slinko/Talks/AfC.pdf", SLINKO_URL)


class HillPublishedExampleTest(unittest.TestCase):
    """Slinko: HELP with K = [[3, 3], [2, 5]] encrypts to HIAT."""

    def test_first_pair_matches_the_published_walkthrough(self) -> None:
        # Page: HE = (7, 4) maps to (7, 8) = HI.
        self.assertEqual(hill_encrypt("HE", SLINKO_KEY), "HI")

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = hill_encrypt(SLINKO_PLAIN, SLINKO_KEY)
        self.assertEqual(cipher, SLINKO_CIPHER)

    def test_published_inverse_matrix(self) -> None:
        # Page states K^{-1} = [[15, 17], [20, 9]].
        self.assertEqual(hill_inverse(SLINKO_KEY), (15, 17, 20, 9))

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_hill(SLINKO_CIPHER, key=SLINKO_KEY)
        self.assertEqual(result.plaintext, SLINKO_PLAIN)
        self.assertEqual(result.method, "hill")
        self.assertEqual(result.key, SLINKO_KEY)
        self.assertEqual(result.details["source_url"], SLINKO_URL)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_roundtrip_recovers_published_plaintext(self) -> None:
        again = hill_decrypt(hill_encrypt(SLINKO_PLAIN, SLINKO_KEY), "3, 3; 2, 5")
        self.assertEqual(again, SLINKO_PLAIN)


class HillCertificateTest(unittest.TestCase):
    """Certificate checks the published Auckland example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "hill")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["key"], key)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(hill_decrypt(ciphertext, key), plaintext)
        result = solve_hill(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], SLINKO_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown-script", note)
        self.assertIn("nr. 86", note)


if __name__ == "__main__":
    unittest.main()
