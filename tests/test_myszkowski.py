"""Myszkowski known-key recovery against a published worked example.

Source (fetched 2026-10-03):
https://www.cryptogram.org/downloads/aca.info/ciphers/Myszkowski.pdf

This is a known classical-cipher solver test. It does not claim Kryptos
K4, the Zodiac ciphers, the Beale ciphers, the McCormick cipher, the
Voynich manuscript, or army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers import SOLVERS
from engine.solvers.myszkowski import (
    ACA_MYSZKOWSKI_CIPHER,
    ACA_MYSZKOWSKI_KEYWORD,
    ACA_MYSZKOWSKI_NUMERIC,
    ACA_MYSZKOWSKI_PLAIN,
    ACA_MYSZKOWSKI_SHEET_PLAIN,
    ACA_MYSZKOWSKI_URL,
    myszkowski_decrypt,
    myszkowski_encrypt,
    myszkowski_numbers,
    numeric_key,
    solve_myszkowski,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "myszkowski_certificate.json"
)


class MyszkowskiScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unsolved_claims(self) -> None:
        import engine.solvers.myszkowski as myszkowski_mod

        source = Path(myszkowski_mod.__file__).read_text(encoding="utf-8")
        doc = (myszkowski_mod.__doc__ or "").lower()
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
        self.assertIn("myszkowski.pdf", ACA_MYSZKOWSKI_URL.lower())
        self.assertNotIn("myszkowski", SOLVERS)
        self.assertNotIn("\u2014", source)
        self.assertNotIn("\u2013", source)
        self.assertNotIn("\u2014", doc)
        self.assertNotIn("\u2013", doc)


class MyszkowskiPublishedExampleTest(unittest.TestCase):
    """ACA sheet: keyword BANANA, plaintext beginning Incomplete columnar."""

    def test_keyword_numbers_match_the_sheet(self) -> None:
        self.assertEqual(myszkowski_numbers(ACA_MYSZKOWSKI_KEYWORD), [2, 1, 3, 1, 3, 1])
        self.assertEqual(numeric_key("banana"), ACA_MYSZKOWSKI_NUMERIC)
        self.assertEqual(ACA_MYSZKOWSKI_KEYWORD, "BANANA")

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = myszkowski_encrypt(ACA_MYSZKOWSKI_SHEET_PLAIN, ACA_MYSZKOWSKI_KEYWORD)
        self.assertEqual(cipher, ACA_MYSZKOWSKI_CIPHER)
        self.assertEqual(
            cipher,
            "NOPEE OUNRI HATRW RKYNL TESNE SMNME TKNFB RWRMO TBTOI LLWTO ATDER "
            "OOTOC MTCMA TPEND EDERU RAUBA EFYFO POTM",
        )
        self.assertEqual(
            myszkowski_encrypt(ACA_MYSZKOWSKI_PLAIN, "banana"),
            ACA_MYSZKOWSKI_CIPHER,
        )

    def test_decrypt_recovers_published_letters(self) -> None:
        plain = myszkowski_decrypt(ACA_MYSZKOWSKI_CIPHER, ACA_MYSZKOWSKI_KEYWORD)
        self.assertEqual(plain, ACA_MYSZKOWSKI_PLAIN)
        self.assertTrue(plain.startswith("INCOMPLETECOLUMNARWITHPATTERNWORDKEY"))
        # The printed line ends with a period. That period is not a letter.
        self.assertEqual(
            myszkowski_decrypt(ACA_MYSZKOWSKI_CIPHER + ".", ACA_MYSZKOWSKI_KEYWORD),
            ACA_MYSZKOWSKI_PLAIN,
        )

    def test_sheet_plaintext_letters_match_the_stored_letters(self) -> None:
        letters = "".join(
            ch.upper()
            for ch in ACA_MYSZKOWSKI_SHEET_PLAIN
            if ch.isascii() and ch.isalpha()
        )
        self.assertEqual(letters, ACA_MYSZKOWSKI_PLAIN)
        self.assertEqual(len(ACA_MYSZKOWSKI_PLAIN), 89)
        self.assertTrue(
            ACA_MYSZKOWSKI_SHEET_PLAIN.startswith(
                "Incomplete columnar with pattern word key"
            )
        )

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_myszkowski(
            ACA_MYSZKOWSKI_CIPHER, keyword=ACA_MYSZKOWSKI_KEYWORD
        )
        self.assertEqual(result.plaintext, ACA_MYSZKOWSKI_PLAIN)
        self.assertEqual(result.method, "myszkowski")
        self.assertEqual(result.key, "BANANA")
        self.assertEqual(result.details["source_url"], ACA_MYSZKOWSKI_URL)
        self.assertEqual(result.details["numeric_key"], "2-1-3-1-3-1")
        self.assertEqual(result.details["width"], 6)
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

    def test_roundtrip_on_an_incomplete_rectangle(self) -> None:
        # BANANA columns 1, 3, and 5 share number 1 and are read by rows.
        # 11 letters leave the last cell of the last row empty.
        cipher = myszkowski_encrypt("ABCDEFGHIJK", "BANANA")
        self.assertEqual(cipher, "BDFHJ AGCEI K")
        self.assertEqual(myszkowski_decrypt(cipher, "BANANA"), "ABCDEFGHIJK")

    def test_empty_keyword_and_empty_text_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            myszkowski_encrypt(ACA_MYSZKOWSKI_PLAIN, "")
        with self.assertRaises(ValueError):
            myszkowski_decrypt(ACA_MYSZKOWSKI_CIPHER, "...")
        with self.assertRaises(ValueError):
            myszkowski_encrypt("...", ACA_MYSZKOWSKI_KEYWORD)
        with self.assertRaises(ValueError):
            solve_myszkowski("", keyword="BANANA")


class MyszkowskiCertificateTest(unittest.TestCase):
    """Certificate checks the published ACA example, not an unsolved text."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "myszkowski")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["keyword"], "BANANA")
        self.assertEqual(self.cert["keys"]["numeric_key"], "2-1-3-1-3-1")
        self.assertEqual(key, "BANANA")
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(myszkowski_decrypt(ciphertext, key), plaintext)
        self.assertEqual(myszkowski_encrypt(plaintext, key), ciphertext)
        result = solve_myszkowski(ciphertext, keyword=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], ACA_MYSZKOWSKI_URL)
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
        raw = CERT_PATH.read_text(encoding="utf-8")
        self.assertNotIn("\u2014", raw)
        self.assertNotIn("\u2013", raw)
        self.assertNotIn("\u2014", note)
        self.assertNotIn("\u2013", note)


if __name__ == "__main__":
    unittest.main()
