"""Seriated Playfair known-key recovery against the ACA sheet example.

Source (fetched 2026-10-03, America/New_York):
https://www.cryptogram.org/downloads/aca.info/ciphers/SeriatedPlayfair.pdf

PDF SHA-256:
8cce8115f416d4a6b8d133190cd26e0ca4aea3332ae432f0a366b66db08da94d

Period 6. Keyword LOGARITHM. Sentence "Come quickly we need help
immediately. tom." The sheet inserts a null X where a vertical pair
would otherwise be a double letter. Printed ciphertext:
NLBCS PCDFG XZQQC DCMGC GQTBH CFTRH FGWHG B.

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about Kryptos K4, Zodiac,
Beale, McCormick, Voynich, or army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers import SOLVERS
from engine.solvers.seriated_playfair import (
    ACA_CIPHER,
    ACA_KEYWORD,
    ACA_PDF_SHA256,
    ACA_PERIOD,
    ACA_PLAIN,
    ACA_PRINTED_CIPHER,
    ACA_SENTENCE,
    ACA_SQUARE,
    ACA_URL,
    prepare_seriated_playfair,
    seriated_playfair_decrypt,
    seriated_playfair_encrypt,
    solve_seriated_playfair,
)
from engine.solvers.playfair import playfair_square


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "seriated_playfair_certificate.json"
)


class SeriatedPlayfairScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.seriated_playfair as seriated_mod

        doc = (seriated_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("kryptos k4", doc)
        self.assertIn("voynich", doc)
        self.assertIn("zodiac", doc)
        self.assertIn("beale", doc)
        self.assertIn("mccormick", doc)
        self.assertIn("ciphers/SeriatedPlayfair.pdf", ACA_URL)
        self.assertEqual(ACA_PDF_SHA256, "8cce8115f416d4a6b8d133190cd26e0ca4aea3332ae432f0a366b66db08da94d")
        self.assertNotIn("seriated_playfair", SOLVERS)
        self.assertNotIn("\u2014", seriated_mod.__doc__ or "")
        self.assertNotIn("\u2013", seriated_mod.__doc__ or "")


class SeriatedPlayfairPublishedExampleTest(unittest.TestCase):
    """ACA sheet: LOGARITHM, period 6, Come quickly..."""

    def test_keyword_square_matches_the_sheet(self) -> None:
        square = playfair_square(ACA_KEYWORD)
        self.assertEqual(square, ACA_SQUARE)
        rows = [square[i : i + 5] for i in range(0, 25, 5)]
        self.assertEqual(rows, ["LOGAR", "ITHMB", "CDEFK", "NPQSU", "VWXYZ"])

    def test_prepare_inserts_the_sheet_null_and_keeps_the_groups(self) -> None:
        prepared = prepare_seriated_playfair(ACA_SENTENCE, ACA_PERIOD)
        self.assertEqual(prepared, ACA_PLAIN)
        self.assertEqual(len(prepared), 36)
        groups = [prepared[i : i + 12] for i in range(0, 36, 12)]
        self.assertEqual(
            groups,
            ["COMEQUICKLYW", "ENEEDHXELPIM", "MEDIATELYTOM"],
        )
        # The only added letter is the vertical null. The sentence has 35 letters.
        self.assertEqual(prepared.replace("X", "", 1), "COMEQUICKLYWENEEDHELPIMMEDIATELYTOM")

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = seriated_playfair_encrypt(ACA_SENTENCE, ACA_KEYWORD, ACA_PERIOD)
        self.assertEqual(cipher, ACA_CIPHER)
        self.assertEqual(
            seriated_playfair_encrypt(ACA_PLAIN, ACA_KEYWORD.lower(), ACA_PERIOD),
            ACA_CIPHER,
        )
        self.assertEqual(ACA_CIPHER, ACA_PRINTED_CIPHER.replace(" ", ""))
        self.assertEqual(cipher[:12], "NLBCSPCDFGXZ")
        self.assertEqual(cipher[12:24], "QQCDCMGCGQTB")
        self.assertEqual(cipher[24:], "HCFTRHFGWHGB")

    def test_decrypt_recovers_published_plaintext_exactly(self) -> None:
        plain = seriated_playfair_decrypt(ACA_PRINTED_CIPHER, ACA_KEYWORD, ACA_PERIOD)
        self.assertEqual(plain, ACA_PLAIN)
        self.assertEqual(
            seriated_playfair_decrypt(ACA_CIPHER, "logarithm", ACA_PERIOD),
            ACA_PLAIN,
        )

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_seriated_playfair(
            ACA_CIPHER, keyword=ACA_KEYWORD, period=ACA_PERIOD
        )
        self.assertEqual(result.plaintext, ACA_PLAIN)
        self.assertEqual(result.method, "seriated_playfair")
        self.assertEqual(result.key, ACA_KEYWORD)
        self.assertEqual(result.details["period"], 6)
        self.assertEqual(result.details["square"], ACA_SQUARE)
        self.assertEqual(result.details["source_url"], ACA_URL)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)
        self.assertIn("kryptos k4", scope)
        self.assertIn("voynich", scope)
        self.assertIn("zodiac", scope)
        self.assertIn("beale", scope)
        self.assertIn("mccormick", scope)

    def test_roundtrip_keeps_an_inserted_null(self) -> None:
        again = seriated_playfair_decrypt(
            seriated_playfair_encrypt(ACA_SENTENCE, ACA_KEYWORD, ACA_PERIOD),
            ACA_KEYWORD,
            ACA_PERIOD,
        )
        self.assertEqual(again, ACA_PLAIN)

    def test_empty_key_bad_period_and_short_ciphertext_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            seriated_playfair_decrypt(ACA_CIPHER, "---", ACA_PERIOD)
        with self.assertRaises(ValueError):
            seriated_playfair_encrypt("...", ACA_KEYWORD, ACA_PERIOD)
        with self.assertRaises(ValueError):
            seriated_playfair_decrypt(ACA_CIPHER, ACA_KEYWORD, 0)
        with self.assertRaises(ValueError):
            seriated_playfair_decrypt(ACA_CIPHER, ACA_KEYWORD, 5)
        with self.assertRaises(ValueError):
            seriated_playfair_encrypt(ACA_SENTENCE, ACA_KEYWORD, True)  # type: ignore[arg-type]


class SeriatedPlayfairCertificateTest(unittest.TestCase):
    """Certificate checks the published ACA example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "seriated_playfair")
        self.assertEqual(self.cert["name"], "seriated_playfair")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        keyword = self.cert["key"]
        self.assertEqual(plaintext, ACA_PLAIN)
        self.assertEqual(ciphertext, ACA_CIPHER)
        self.assertEqual(self.cert["keys"]["keyword"], keyword)
        self.assertEqual(self.cert["keys"]["period"], ACA_PERIOD)
        self.assertEqual(self.cert["message"], ACA_SENTENCE)
        self.assertEqual(self.cert["source_pdf_sha256"], ACA_PDF_SHA256)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(
            seriated_playfair_decrypt(ciphertext, keyword, self.cert["keys"]["period"]),
            plaintext,
        )
        self.assertEqual(
            seriated_playfair_encrypt(self.cert["message"], keyword, ACA_PERIOD),
            ciphertext,
        )
        self.assertEqual(
            seriated_playfair_encrypt(plaintext, keyword, ACA_PERIOD),
            ciphertext,
        )
        result = solve_seriated_playfair(ciphertext, keyword=keyword, period=ACA_PERIOD)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], ACA_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown script", note)
        self.assertIn("nr. 86", note)
        self.assertIn("kryptos k4", note)
        self.assertIn("voynich", note)
        self.assertIn("zodiac", note)
        self.assertIn("beale", note)
        self.assertIn("mccormick", note)
        blob = CERT_PATH.read_text(encoding="utf-8")
        self.assertNotIn("\u2014", blob)
        self.assertNotIn("\u2013", blob)
        self.assertNotIn("\u2014", plaintext)
        self.assertNotIn("\u2013", plaintext)


if __name__ == "__main__":
    unittest.main()
