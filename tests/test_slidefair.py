"""Slidefair known-key recovery against a published worked example.

Source (fetched 2026-10-03):
https://www.cryptogram.org/downloads/aca.info/ciphers/Slidefair.pdf

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers import SOLVERS
from engine.solvers.slidefair import (
    ACA_SLIDEFAIR_CIPHER,
    ACA_SLIDEFAIR_KEYWORD,
    ACA_SLIDEFAIR_PLAIN,
    ACA_SLIDEFAIR_SENTENCE,
    ACA_SLIDEFAIR_URL,
    CRYPTOCRACK_SLIDEFAIR_CIPHER,
    CRYPTOCRACK_SLIDEFAIR_KEYWORD,
    CRYPTOCRACK_SLIDEFAIR_PLAIN,
    CRYPTOCRACK_SLIDEFAIR_SENTENCE,
    slidefair_decrypt,
    slidefair_encrypt,
    solve_slidefair,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "slidefair_certificate.json"
)


class SlidefairScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.slidefair as slidefair_mod

        doc = (slidefair_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("known-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("slidefair.pdf", ACA_SLIDEFAIR_URL.lower())
        self.assertNotIn("slidefair", SOLVERS)


class SlidefairPublishedExampleTest(unittest.TestCase):
    """ACA sheet: keyword DIGRAPH, Vigenere table."""

    def test_sheet_key_letter_b_matches_all_three_tables(self) -> None:
        self.assertEqual(slidefair_encrypt("ca", "B", table="vigenere"), "ZD")
        self.assertEqual(slidefair_encrypt("de", "B", table="vigenere"), "EF")
        self.assertEqual(slidefair_encrypt("ca", "B", table="variant"), "BB")
        self.assertEqual(slidefair_encrypt("de", "B", table="variant"), "FC")
        self.assertEqual(slidefair_encrypt("ca", "B", table="beaufort"), "BZ")
        self.assertEqual(slidefair_encrypt("de", "B", table="beaufort"), "XY")
        self.assertEqual(slidefair_decrypt("ZD", "B"), "CA")
        self.assertEqual(slidefair_decrypt("EF", "B"), "DE")

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = slidefair_encrypt(ACA_SLIDEFAIR_SENTENCE, ACA_SLIDEFAIR_KEYWORD)
        self.assertEqual(cipher, ACA_SLIDEFAIR_CIPHER)
        self.assertEqual(len(cipher.split()), 25)

    def test_decrypt_recovers_published_plaintext_exactly(self) -> None:
        packed = ACA_SLIDEFAIR_CIPHER.replace(" ", "")
        self.assertEqual(
            slidefair_decrypt(packed, ACA_SLIDEFAIR_KEYWORD.lower()),
            ACA_SLIDEFAIR_PLAIN,
        )

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_slidefair(ACA_SLIDEFAIR_CIPHER, key=ACA_SLIDEFAIR_KEYWORD)
        self.assertEqual(result.plaintext, ACA_SLIDEFAIR_PLAIN)
        self.assertEqual(
            result.plaintext,
            "THESLIDEFAIRCANBEUSEDWITHVIGENEREVARIANTORBEAUFORT",
        )
        self.assertEqual(result.method, "slidefair")
        self.assertEqual(result.key, "DIGRAPH")
        self.assertEqual(result.details["table"], "vigenere")
        self.assertEqual(result.details["period"], 7)
        self.assertEqual(result.details["source_url"], ACA_SLIDEFAIR_URL)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_cryptocrack_quote_pads_the_odd_letter_with_x(self) -> None:
        cipher = slidefair_encrypt(
            CRYPTOCRACK_SLIDEFAIR_SENTENCE,
            CRYPTOCRACK_SLIDEFAIR_KEYWORD,
        )
        self.assertEqual(cipher, CRYPTOCRACK_SLIDEFAIR_CIPHER)
        self.assertEqual(
            slidefair_decrypt(cipher, "slidefair"),
            CRYPTOCRACK_SLIDEFAIR_PLAIN,
        )

    def test_empty_key_odd_ciphertext_and_unknown_table_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            slidefair_decrypt(ACA_SLIDEFAIR_CIPHER, "---")
        with self.assertRaises(ValueError):
            slidefair_encrypt("...", "DIGRAPH")
        with self.assertRaises(ValueError):
            slidefair_decrypt("EWK", "DIGRAPH")
        with self.assertRaises(ValueError):
            slidefair_encrypt("CA", "DIGRAPH", table="playfair")


class SlidefairCertificateTest(unittest.TestCase):
    """Certificate checks the published ACA example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "slidefair")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["keyword"], "DIGRAPH")
        self.assertEqual(self.cert["keys"]["table"], "vigenere")
        self.assertEqual(self.cert["keys"]["period"], 7)
        self.assertEqual(key, ACA_SLIDEFAIR_KEYWORD)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(slidefair_decrypt(ciphertext, key), plaintext)
        result = solve_slidefair(ciphertext, key=key, table=self.cert["keys"]["table"])
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], ACA_SLIDEFAIR_URL)
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
