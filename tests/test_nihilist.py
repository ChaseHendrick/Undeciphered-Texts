"""Nihilist known-key recovery against a published worked example.

Source (fetched 2026-10-02):
https://en.wikipedia.org/wiki/Nihilist_cipher

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.nihilist import (
    WIKIPEDIA_CIPHER,
    WIKIPEDIA_KEY,
    WIKIPEDIA_PLAIN,
    WIKIPEDIA_URL,
    nihilist_decrypt,
    nihilist_encrypt,
    solve_nihilist,
    square_from_keyword,
)


CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "nihilist_certificate.json"


class NihilistScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.nihilist as nihilist_mod

        doc = (nihilist_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("en.wikipedia.org/wiki/Nihilist_cipher", WIKIPEDIA_URL)


class NihilistPublishedExampleTest(unittest.TestCase):
    """Wikipedia: DYNAMITE WINTER PALACE with square ZEBRAS and key RUSSIAN."""

    def test_square_matches_the_published_grid(self) -> None:
        # Row-major reading of the Wikipedia ZEBRAS square (J omitted).
        self.assertEqual(square_from_keyword("ZEBRAS"), "ZEBRASCDFGHIKLMNOPQTUVWXY")

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = nihilist_encrypt("DYNAMITE WINTER PALACE", WIKIPEDIA_KEY)
        self.assertEqual(cipher, WIKIPEDIA_CIPHER)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_nihilist(WIKIPEDIA_CIPHER, key=WIKIPEDIA_KEY)
        self.assertEqual(result.plaintext, WIKIPEDIA_PLAIN)
        self.assertEqual(result.method, "nihilist")
        self.assertEqual(result.key, WIKIPEDIA_KEY)
        self.assertEqual(result.details["source_url"], WIKIPEDIA_URL)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_roundtrip_uses_the_published_keywords(self) -> None:
        again = nihilist_decrypt(
            nihilist_encrypt(WIKIPEDIA_PLAIN, "ZEBRAS/RUSSIAN"),
            "ZEBRAS RUSSIAN",
        )
        self.assertEqual(again, WIKIPEDIA_PLAIN)


class NihilistCertificateTest(unittest.TestCase):
    """Certificate checks the published Wikipedia example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "nihilist")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["key"], key)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(nihilist_decrypt(ciphertext, key), plaintext)
        result = solve_nihilist(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], WIKIPEDIA_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown-script", note)
        self.assertIn("nr. 86", note)


if __name__ == "__main__":
    unittest.main()
