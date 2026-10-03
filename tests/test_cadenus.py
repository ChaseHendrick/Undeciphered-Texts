"""Cadenus known-key recovery against a published worked example.

Source (fetched): https://www.cryptogram.org/downloads/aca.info/ciphers/Cadenus.pdf

This is a known classical-cipher solver test. It does not claim an
ancient-script or unknown-language reading.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.cadenus import (
    ACA_CIPHER,
    ACA_KEYWORD,
    ACA_NUMERIC_KEY,
    ACA_PLAIN,
    ACA_PRINTED,
    ACA_URL,
    cadenus_decrypt,
    cadenus_encrypt,
    cadenus_letters,
    numeric_key,
    row_shift,
    solve_cadenus,
)


class CadenusScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_ancient_script(self) -> None:
        import engine.solvers.cadenus as cadenus_mod

        doc = cadenus_mod.__doc__ or ""
        self.assertIn("known classical-cipher", doc.lower().replace("\n", " "))
        lowered = doc.lower()
        self.assertTrue(
            "ancient script" in lowered or "ancient-script" in lowered,
            msg="module docstring must say it does not read ancient scripts",
        )
        self.assertIn("cryptogram.org/downloads/aca.info/ciphers/Cadenus.pdf", ACA_URL)
        from engine.solvers import SOLVERS

        self.assertNotIn("cadenus", SOLVERS)


class CadenusPublishedExampleTest(unittest.TestCase):
    """ACA sheet: keyword EASY, numeric key 2-1-3-4, 100 plaintext letters."""

    def test_numeric_key_matches_the_sheet(self) -> None:
        self.assertEqual(numeric_key(ACA_KEYWORD), ACA_NUMERIC_KEY)
        self.assertEqual(numeric_key("easy"), "2-1-3-4")
        # E is the 22nd row label (index 21). That row of column 1 is Y.
        self.assertEqual(row_shift("E"), 21)
        column = ACA_PLAIN[0::4]
        self.assertEqual(len(column), 25)
        self.assertEqual(column[21], "Y")
        # A is the top row, so that column is not cycled.
        self.assertEqual(row_shift("A"), 0)

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = cadenus_encrypt(ACA_PLAIN, ACA_KEYWORD)
        self.assertEqual(cipher, ACA_CIPHER)
        self.assertEqual(len(cipher), 100)
        self.assertEqual(
            cipher,
            "SYSTRETOMTATTLUSOATLEEESFIYHEASDFNMSCHBHNEUVSNPMTOFARENUSEIE"
            "EIELTARLMENTIEETOGEVESITFAISLTNGEEUVOWUL",
        )

    def test_decrypt_recovers_published_plaintext_exactly(self) -> None:
        plain = cadenus_decrypt(ACA_CIPHER, ACA_KEYWORD)
        self.assertEqual(plain, ACA_PLAIN)
        self.assertEqual(len(plain), 100)
        self.assertNotIn(" ", plain)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_cadenus(ACA_CIPHER, keyword=ACA_KEYWORD)
        self.assertEqual(result.plaintext, ACA_PLAIN)
        self.assertEqual(result.method, "cadenus")
        self.assertEqual(result.key, "EASY")
        self.assertEqual(result.details["numeric_key"], "2-1-3-4")
        self.assertEqual(result.details["keyword"], "EASY")
        self.assertEqual(result.details["width"], 4)
        self.assertIn("not an ancient-script", result.details["scope"].lower())
        self.assertEqual(result.details["source_url"], ACA_URL)

    def test_grouped_ciphertext_and_spaced_plaintext_roundtrip(self) -> None:
        grouped = (
            "SYSTR ETOMT ATTLU SOATL EEESF IYHEA SDFNM SCHBH NEUVS NPMTO "
            "FAREN USEIE EIELT ARLME NTIEE TOGEV ESITF AISLT NGEEU VOWUL."
        )
        plain = cadenus_decrypt(grouped, "EASY")
        self.assertEqual(plain, ACA_PLAIN)
        cipher = cadenus_encrypt(ACA_PRINTED, ACA_KEYWORD)
        self.assertEqual(cipher, ACA_CIPHER)
        self.assertEqual(cadenus_letters(ACA_PRINTED), ACA_PLAIN)
        self.assertNotIn(" ", plain)
        self.assertNotIn("-", plain)


class CadenusHelpersTest(unittest.TestCase):
    def test_v_and_w_share_a_row_and_roundtrip(self) -> None:
        # Synthetic roundtrip. Not a published ciphertext.
        self.assertEqual(row_shift("V"), row_shift("W"))
        self.assertEqual(row_shift("V"), 4)
        self.assertEqual(numeric_key("WAVE"), "4-1-3-2")
        plain = ("THEQUICKBROWNFOXJUMPED" * 8)[: 25 * 4]
        cipher = cadenus_encrypt(plain, "WAVE")
        self.assertEqual(cadenus_decrypt(cipher, "wave"), plain)
        self.assertNotEqual(cipher, plain)

    def test_repeated_keyword_letter_keeps_left_to_right_order(self) -> None:
        # Synthetic roundtrip. Not a published ciphertext.
        self.assertEqual(numeric_key("SEES"), "3-1-2-4")
        plain = "A" * 24 + "B" + ("C" * 25 * 3)
        self.assertEqual(len(plain), 100)
        cipher = cadenus_encrypt(plain, "SEES")
        self.assertEqual(cadenus_decrypt(cipher, "SEES"), plain)

    def test_length_not_multiple_of_the_block_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            cadenus_encrypt("ABC", ACA_KEYWORD)
        with self.assertRaises(ValueError):
            cadenus_decrypt(ACA_CIPHER[:-1], ACA_KEYWORD)
        with self.assertRaises(ValueError):
            cadenus_encrypt(ACA_PLAIN, "...")
        with self.assertRaises(ValueError):
            numeric_key("")


CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "cadenus_certificate.json"


class CadenusCertificateTest(unittest.TestCase):
    """Certificate checks the ACA sheet example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "cadenus")
        self.assertEqual(self.cert["name"], "cadenus")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(plaintext, ACA_PLAIN)
        self.assertEqual(ciphertext, ACA_CIPHER)
        self.assertEqual(key, ACA_KEYWORD)
        self.assertEqual(self.cert["keys"]["keyword"], "EASY")
        self.assertEqual(self.cert["keys"]["numeric_key"], "2-1-3-4")
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(digest, "581abe3a18d62e63c60a17ce6c2bc708a5d3012123307d1990342b83b83a7c11")
        self.assertNotIn(" ", plaintext)
        self.assertEqual(cadenus_decrypt(ciphertext, key), plaintext)
        result = solve_cadenus(ciphertext, keyword=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], ACA_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown script", note)
        self.assertIn("no spaces", note)
        self.assertIn("nr. 86", note)
        self.assertIn("kryptos k4", note)
        self.assertIn("voynich", note)
        self.assertIn("linear a", note)
        self.assertIn("indus", note)
        self.assertIn("rongorongo", note)


if __name__ == "__main__":
    unittest.main()
