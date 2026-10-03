"""Grandpre known-key recovery against a published worked example.

Source (fetched 2026-10-02):
https://www.cryptogram.org/downloads/aca.info/ciphers/Grandpre.pdf

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.grandpre import (
    ACA_GRANDPRE_CIPHER,
    ACA_GRANDPRE_CIPHER_GROUPED,
    ACA_GRANDPRE_KEY,
    ACA_GRANDPRE_KEYWORD,
    ACA_GRANDPRE_PHRASE,
    ACA_GRANDPRE_PLAIN,
    ACA_GRANDPRE_URL,
    grandpre_decrypt,
    grandpre_encrypt,
    parse_grandpre_key,
    solve_grandpre,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "grandpre_certificate.json"
)


class GrandpreScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.grandpre as grandpre_mod

        doc = (grandpre_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("known-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("Grandpre.pdf", ACA_GRANDPRE_URL)


class GrandprePublishedExampleTest(unittest.TestCase):
    """ACA sheet: LACQUERS square, "The first column is the keyword." """

    def test_square_and_first_column_match_the_sheet(self) -> None:
        words = parse_grandpre_key(ACA_GRANDPRE_KEY)
        self.assertEqual(len(words), 8)
        self.assertEqual(words[0], "LADYBUGS")
        self.assertEqual(words[7], "SEXTUPLY")
        self.assertEqual("".join(word[0] for word in words), ACA_GRANDPRE_KEYWORD)
        self.assertEqual(ACA_GRANDPRE_KEYWORD, "LACQUERS")

    def test_published_pairs_are_the_sheet_letters(self) -> None:
        # Spot checks from the printed square, row then column, labels 1-8.
        self.assertEqual(grandpre_decrypt("84", ACA_GRANDPRE_KEY), "T")
        self.assertEqual(grandpre_decrypt("27", ACA_GRANDPRE_KEY), "H")
        self.assertEqual(grandpre_decrypt("82", ACA_GRANDPRE_KEY), "E")
        self.assertEqual(grandpre_decrypt("13", ACA_GRANDPRE_KEY), "D")
        self.assertEqual(grandpre_decrypt("53", ACA_GRANDPRE_KEY), "J")

    def test_decrypt_matches_published_plaintext(self) -> None:
        self.assertEqual(
            grandpre_decrypt(ACA_GRANDPRE_CIPHER, ACA_GRANDPRE_KEY),
            ACA_GRANDPRE_PLAIN,
        )
        self.assertEqual(
            grandpre_decrypt(ACA_GRANDPRE_CIPHER_GROUPED, ACA_GRANDPRE_KEY),
            "THEFIRSTCOLUMNISTHEKEYWORD",
        )

    def test_encrypt_roundtrip_uses_the_first_cell(self) -> None:
        # J is only at row 5, column 3. T's first cell is row 2, column 6,
        # not the 84 chosen on the sheet.
        self.assertEqual(grandpre_encrypt("J", ACA_GRANDPRE_KEY), "53")
        self.assertEqual(grandpre_encrypt("T", ACA_GRANDPRE_KEY), "26")
        cipher = grandpre_encrypt(ACA_GRANDPRE_PHRASE, ACA_GRANDPRE_KEY)
        self.assertEqual(grandpre_decrypt(cipher, ACA_GRANDPRE_KEY), ACA_GRANDPRE_PLAIN)
        self.assertNotEqual(cipher, ACA_GRANDPRE_CIPHER)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_grandpre(ACA_GRANDPRE_CIPHER_GROUPED, key=ACA_GRANDPRE_KEY)
        self.assertEqual(result.plaintext, ACA_GRANDPRE_PLAIN)
        self.assertEqual(result.method, "grandpre")
        self.assertEqual(result.key, ACA_GRANDPRE_KEY)
        self.assertEqual(result.details["keyword"], "LACQUERS")
        self.assertEqual(result.details["size"], 8)
        self.assertEqual(result.details["source_url"], ACA_GRANDPRE_URL)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_bad_key_and_odd_digit_count_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            grandpre_decrypt(ACA_GRANDPRE_CIPHER, "CAT")
        with self.assertRaises(ValueError):
            grandpre_decrypt("842", ACA_GRANDPRE_KEY)


class GrandpreCertificateTest(unittest.TestCase):
    """Certificate checks the published ACA example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "grandpre")
        self.assertEqual(self.cert["name"], "grandpre")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(plaintext, ACA_GRANDPRE_PLAIN)
        self.assertEqual(ciphertext, ACA_GRANDPRE_CIPHER)
        self.assertEqual(key, ACA_GRANDPRE_KEY)
        self.assertEqual(self.cert["keys"]["keyword"], "LACQUERS")
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(grandpre_decrypt(ciphertext, key), plaintext)
        result = solve_grandpre(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], ACA_GRANDPRE_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown-script", note)
        self.assertIn("nr. 86", note)
        self.assertIn("kryptos k4", note)
        self.assertIn("voynich", note)
        self.assertIn("linear a", note)
        self.assertIn("indus", note)
        self.assertIn("rongorongo", note)


if __name__ == "__main__":
    unittest.main()
