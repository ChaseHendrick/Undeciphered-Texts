"""Nihilist transposition known-key recovery against a published example.

Source (fetched 2026-10-03):
https://www.cryptogram.org/downloads/aca.info/ciphers/NihilistTransposition.pdf

This is a known classical-cipher solver test. It does not claim Kryptos
K4, the Zodiac ciphers, the Beale ciphers, the McCormick cipher, the
Voynich manuscript, or army message Nr. 86. It is not the Nihilist
substitution cipher already covered by tests/test_nihilist.py.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers import SOLVERS
from engine.solvers.nihilist_transposition import (
    ACA_NIHILIST_TRANSPOSITION_CIPHER,
    ACA_NIHILIST_TRANSPOSITION_CIPHER_ROWS,
    ACA_NIHILIST_TRANSPOSITION_KEY,
    ACA_NIHILIST_TRANSPOSITION_PLAIN,
    ACA_NIHILIST_TRANSPOSITION_SHEET_PLAIN,
    ACA_NIHILIST_TRANSPOSITION_URL,
    nihilist_transposition_decrypt,
    nihilist_transposition_encrypt,
    normalize_key,
    solve_nihilist_transposition,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "nihilist_transposition_certificate.json"
)


class NihilistTranspositionScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unsolved_claims(self) -> None:
        import engine.solvers.nihilist_transposition as mod

        source = Path(mod.__file__).read_text(encoding="utf-8")
        doc = (mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("known-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("kryptos k4", doc)
        self.assertIn("zodiac", doc)
        self.assertIn("beale", doc)
        self.assertIn("mccormick", doc)
        self.assertIn("voynich", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("nihilist substitution", doc)
        self.assertIn("nihilisttransposition.pdf", ACA_NIHILIST_TRANSPOSITION_URL.lower())
        self.assertNotIn("nihilist_transposition", SOLVERS)
        self.assertNotIn("\u2014", source)
        self.assertNotIn("\u2013", source)
        self.assertNotIn("\u2014", doc)
        self.assertNotIn("\u2013", doc)


class NihilistTranspositionPublishedExampleTest(unittest.TestCase):
    """ACA sheet: key 2134, plaintext square needed here."""

    def test_key_digits_match_the_sheet(self) -> None:
        self.assertEqual(normalize_key(ACA_NIHILIST_TRANSPOSITION_KEY), "2134")
        self.assertEqual(normalize_key("2 1 3 4"), "2134")
        self.assertEqual(ACA_NIHILIST_TRANSPOSITION_KEY, "2134")

    def test_encrypt_matches_published_column_ciphertext(self) -> None:
        cipher = nihilist_transposition_encrypt(
            ACA_NIHILIST_TRANSPOSITION_SHEET_PLAIN,
            ACA_NIHILIST_TRANSPOSITION_KEY,
        )
        self.assertEqual(cipher, ACA_NIHILIST_TRANSPOSITION_CIPHER)
        self.assertEqual(cipher, "EQDER SEHNU EREAD E")
        self.assertEqual(
            nihilist_transposition_encrypt(
                ACA_NIHILIST_TRANSPOSITION_PLAIN, "2134"
            ),
            ACA_NIHILIST_TRANSPOSITION_CIPHER,
        )

    def test_encrypt_matches_published_row_ciphertext(self) -> None:
        cipher = nihilist_transposition_encrypt(
            ACA_NIHILIST_TRANSPOSITION_SHEET_PLAIN,
            ACA_NIHILIST_TRANSPOSITION_KEY,
            takeoff="rows",
        )
        self.assertEqual(cipher, ACA_NIHILIST_TRANSPOSITION_CIPHER_ROWS)
        self.assertEqual(cipher, "ERNEQ SUADE EDEHR E")

    def test_decrypt_recovers_published_letters(self) -> None:
        plain = nihilist_transposition_decrypt(
            ACA_NIHILIST_TRANSPOSITION_CIPHER, ACA_NIHILIST_TRANSPOSITION_KEY
        )
        self.assertEqual(plain, ACA_NIHILIST_TRANSPOSITION_PLAIN)
        self.assertEqual(
            nihilist_transposition_decrypt(
                ACA_NIHILIST_TRANSPOSITION_CIPHER + ".",
                ACA_NIHILIST_TRANSPOSITION_KEY,
            ),
            ACA_NIHILIST_TRANSPOSITION_PLAIN,
        )
        self.assertEqual(
            nihilist_transposition_decrypt(
                ACA_NIHILIST_TRANSPOSITION_CIPHER_ROWS,
                ACA_NIHILIST_TRANSPOSITION_KEY,
                takeoff="rows",
            ),
            ACA_NIHILIST_TRANSPOSITION_PLAIN,
        )

    def test_sheet_plaintext_letters_match_the_stored_letters(self) -> None:
        letters = "".join(
            ch.upper()
            for ch in ACA_NIHILIST_TRANSPOSITION_SHEET_PLAIN
            if ch.isascii() and ch.isalpha()
        )
        self.assertEqual(letters, ACA_NIHILIST_TRANSPOSITION_PLAIN)
        self.assertEqual(len(ACA_NIHILIST_TRANSPOSITION_PLAIN), 16)
        self.assertEqual(ACA_NIHILIST_TRANSPOSITION_SHEET_PLAIN, "square needed here")

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_nihilist_transposition(
            ACA_NIHILIST_TRANSPOSITION_CIPHER,
            key=ACA_NIHILIST_TRANSPOSITION_KEY,
        )
        self.assertEqual(result.plaintext, ACA_NIHILIST_TRANSPOSITION_PLAIN)
        self.assertEqual(result.method, "nihilist_transposition")
        self.assertEqual(result.key, "2134")
        self.assertEqual(result.details["source_url"], ACA_NIHILIST_TRANSPOSITION_URL)
        self.assertEqual(result.details["numeric_key"], "2134")
        self.assertEqual(result.details["side"], 4)
        self.assertEqual(result.details["takeoff"], "columns")
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("kryptos k4", scope)
        self.assertIn("zodiac", scope)
        self.assertIn("beale", scope)
        self.assertIn("mccormick", scope)
        self.assertIn("voynich", scope)
        self.assertIn("nr. 86", scope)
        self.assertNotIn("\u2014", scope)
        self.assertNotIn("\u2013", scope)

    def test_roundtrip_on_another_taking_out_key(self) -> None:
        plain = "ABCDEFGHIJKLMNOP"
        cipher = nihilist_transposition_encrypt(plain, "3142")
        self.assertEqual(nihilist_transposition_decrypt(cipher, "3142"), plain)
        cipher_rows = nihilist_transposition_encrypt(plain, "3142", takeoff="rows")
        self.assertEqual(
            nihilist_transposition_decrypt(cipher_rows, "3142", takeoff="rows"),
            plain,
        )

    def test_empty_key_and_non_square_text_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            nihilist_transposition_encrypt(ACA_NIHILIST_TRANSPOSITION_PLAIN, "")
        with self.assertRaises(ValueError):
            nihilist_transposition_decrypt(ACA_NIHILIST_TRANSPOSITION_CIPHER, "...")
        with self.assertRaises(ValueError):
            nihilist_transposition_encrypt("ABC", "2134")
        with self.assertRaises(ValueError):
            solve_nihilist_transposition("", key="2134")
        with self.assertRaises(ValueError):
            normalize_key("1123")


class NihilistTranspositionCertificateTest(unittest.TestCase):
    """Certificate checks the published ACA example, not an unsolved text."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "nihilist_transposition")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["numeric_key"], "2134")
        self.assertEqual(self.cert["keys"]["takeoff"], "columns")
        self.assertEqual(key, "2134")
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(nihilist_transposition_decrypt(ciphertext, key), plaintext)
        self.assertEqual(nihilist_transposition_encrypt(plaintext, key), ciphertext)
        result = solve_nihilist_transposition(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], ACA_NIHILIST_TRANSPOSITION_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown-script", note)
        self.assertIn("nr. 86", note)
        self.assertIn("kryptos k4", note)
        self.assertIn("zodiac", note)
        self.assertIn("beale", note)
        self.assertIn("mccormick", note)
        self.assertIn("voynich", note)
        self.assertIn("linear a", note)
        self.assertIn("indus", note)
        self.assertIn("rongorongo", note)
        self.assertIn("nihilist substitution", note)
        raw = CERT_PATH.read_text(encoding="utf-8")
        self.assertNotIn("\u2014", raw)
        self.assertNotIn("\u2013", raw)
        self.assertNotIn("\u2014", note)
        self.assertNotIn("\u2013", note)


if __name__ == "__main__":
    unittest.main()
