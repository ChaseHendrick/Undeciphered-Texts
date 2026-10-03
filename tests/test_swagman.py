"""Swagman known-key recovery against a published worked example.

Source (fetched 2026-10-02):
https://www.cryptogram.org/downloads/aca.info/ciphers/Swagman.pdf

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.swagman import (
    ACA_SWAGMAN_CIPHER,
    ACA_SWAGMAN_KEY,
    ACA_SWAGMAN_PLAIN,
    ACA_SWAGMAN_URL,
    parse_swagman_key,
    solve_swagman,
    swagman_decrypt,
    swagman_encrypt,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "swagman_certificate.json"
)


class SwagmanScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.swagman as swagman_mod

        doc = swagman_mod.__doc__ or ""
        lowered = doc.lower()
        self.assertIn("known-cipher solver", lowered)
        self.assertIn("known classical cipher", lowered)
        self.assertIn("not an unknown-script reading", lowered)
        self.assertIn("nr. 86", lowered)
        self.assertIn("Swagman.pdf", ACA_SWAGMAN_URL)


class SwagmanPublishedExampleTest(unittest.TestCase):
    """ACA sheet: 5x5 key, leap quote, column-read ciphertext."""

    def test_key_square_matches_the_published_square(self) -> None:
        self.assertEqual(
            parse_swagman_key(ACA_SWAGMAN_KEY),
            (
                (3, 2, 1, 4, 5),
                (1, 5, 3, 2, 4),
                (2, 4, 5, 3, 1),
                (5, 3, 4, 1, 2),
                (4, 1, 2, 5, 3),
            ),
        )

    def test_first_column_matches_the_published_walkthrough(self) -> None:
        # Column 0 letters D,E,N,C,S under key 3,1,2,5,4 become ENDSC.
        self.assertEqual(
            swagman_encrypt(ACA_SWAGMAN_PLAIN, ACA_SWAGMAN_KEY)[:5],
            "ENDSC",
        )

    def test_encrypt_matches_published_groups(self) -> None:
        cipher = swagman_encrypt(ACA_SWAGMAN_PLAIN, ACA_SWAGMAN_KEY)
        self.assertEqual(cipher, ACA_SWAGMAN_CIPHER)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        grouped = (
            "ENDSC MORDA NIBOI SICTN ASTGB LTEWA OAREE FSAID VPYRM "
            "OEAIA FUILR LDOCO TJNRA AENOU NCMIT SOAPH SKATI."
        )
        result = solve_swagman(grouped, key=ACA_SWAGMAN_KEY)
        self.assertEqual(result.plaintext, ACA_SWAGMAN_PLAIN)
        self.assertEqual(result.method, "swagman")
        self.assertEqual(result.key, ACA_SWAGMAN_KEY)
        self.assertEqual(result.details["source_url"], ACA_SWAGMAN_URL)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_roundtrip_with_spaced_plaintext(self) -> None:
        sentence = (
            "Don't be afraid to take a big leap if one is indicated. "
            "You cannot cross a river or a chasm in two small jumps."
        )
        again = swagman_decrypt(
            swagman_encrypt(sentence, ACA_SWAGMAN_KEY),
            ACA_SWAGMAN_KEY,
        )
        self.assertEqual(again, ACA_SWAGMAN_PLAIN)

    def test_empty_key_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            swagman_decrypt(ACA_SWAGMAN_CIPHER, "...")


class SwagmanCertificateTest(unittest.TestCase):
    """Certificate checks the published ACA example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "swagman")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["key"], key)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(swagman_decrypt(ciphertext, key), plaintext)
        result = solve_swagman(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], ACA_SWAGMAN_URL)
        note = self.cert["note"].lower()
        self.assertIn("known-cipher solver", note)
        self.assertIn("not an unknown-script", note)
        self.assertIn("nr. 86", note)


if __name__ == "__main__":
    unittest.main()
