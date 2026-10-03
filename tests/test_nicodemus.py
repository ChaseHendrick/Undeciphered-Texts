"""Nicodemus known-key recovery against a published worked example.

Source (fetched 2026-10-02):
https://www.cryptogram.org/downloads/aca.info/ciphers/Nicodemus.pdf

A second published walk-through is also checked:
https://sites.google.com/site/cryptocrackprogram/user-guide/cipher-types/substitution/nicodemus

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.nicodemus import (
    ACA_NICODEMUS_CIPHER,
    ACA_NICODEMUS_CIPHER_GROUPED,
    ACA_NICODEMUS_KEY,
    ACA_NICODEMUS_PLAIN,
    ACA_NICODEMUS_URL,
    CRYPTOCRACK_NICODEMUS_CIPHER,
    CRYPTOCRACK_NICODEMUS_KEY,
    CRYPTOCRACK_NICODEMUS_PLAIN,
    CRYPTOCRACK_NICODEMUS_URL,
    column_order,
    nicodemus_decrypt,
    nicodemus_encrypt,
    solve_nicodemus,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "nicodemus_certificate.json"
)


class NicodemusScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.nicodemus as nicodemus_mod

        doc = (nicodemus_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("Nicodemus.pdf", ACA_NICODEMUS_URL)


class NicodemusPublishedExampleTest(unittest.TestCase):
    """ACA sheet: CAT, the early bird gets the worm."""

    def test_column_order_matches_the_published_ranks(self) -> None:
        # C=2, A=1, T=3, so columns are read A, C, T (indexes 1, 0, 2).
        self.assertEqual(column_order(ACA_NICODEMUS_KEY), (1, 0, 2))

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = nicodemus_encrypt(
            "the early bird gets the worm",
            ACA_NICODEMUS_KEY,
        )
        self.assertEqual(cipher, ACA_NICODEMUS_CIPHER)
        self.assertEqual(cipher, "HAYREVGNKIXKUWMTWMUGTAH")

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_nicodemus(ACA_NICODEMUS_CIPHER, key=ACA_NICODEMUS_KEY)
        self.assertEqual(result.plaintext, ACA_NICODEMUS_PLAIN)
        self.assertEqual(result.plaintext, "THEEARLYBIRDGETSTHEWORM")
        self.assertEqual(result.method, "nicodemus")
        self.assertEqual(result.key, ACA_NICODEMUS_KEY)
        self.assertEqual(result.details["source_url"], ACA_NICODEMUS_URL)
        self.assertEqual(result.details["reordered_key"], "ACT")
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_grouped_ciphertext_decrypts_to_the_same_letters(self) -> None:
        # The sheet prints the ciphertext in groups of five, with a final period.
        self.assertEqual(
            nicodemus_decrypt(ACA_NICODEMUS_CIPHER_GROUPED, ACA_NICODEMUS_KEY),
            ACA_NICODEMUS_PLAIN,
        )

    def test_cryptocrack_published_example_recovers_plaintext(self) -> None:
        cipher = nicodemus_encrypt(
            "Money can't buy happiness. But it sure makes misery easier to live with.",
            CRYPTOCRACK_NICODEMUS_KEY,
        )
        self.assertEqual(cipher, CRYPTOCRACK_NICODEMUS_CIPHER)
        result = solve_nicodemus(cipher, key=CRYPTOCRACK_NICODEMUS_KEY)
        self.assertEqual(result.plaintext, CRYPTOCRACK_NICODEMUS_PLAIN)
        self.assertIn("nicodemus", CRYPTOCRACK_NICODEMUS_URL)

    def test_repeated_keyword_letters_roundtrip(self) -> None:
        # Local check only. Not a published example.
        sentence = "the early bird gets the worm"
        key = "LETTER"
        again = nicodemus_decrypt(nicodemus_encrypt(sentence, key), key)
        self.assertEqual(again, ACA_NICODEMUS_PLAIN)
        self.assertEqual(column_order(key), (1, 4, 0, 5, 2, 3))

    def test_empty_keyword_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            nicodemus_decrypt(ACA_NICODEMUS_CIPHER, "...")


class NicodemusCertificateTest(unittest.TestCase):
    """Certificate checks the published ACA example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "nicodemus")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["key"], key)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(nicodemus_decrypt(ciphertext, key), plaintext)
        result = solve_nicodemus(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], ACA_NICODEMUS_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown-script", note)
        self.assertIn("nr. 86", note)


if __name__ == "__main__":
    unittest.main()
