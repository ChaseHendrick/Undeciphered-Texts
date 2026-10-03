"""Portax known-key recovery against the ACA sheet worked example.

Source (fetched 2026-10-03):
https://www.cryptogram.org/downloads/aca.info/ciphers/Portax.pdf

Keyword EASY. Printed plaintext "the early bird gets the worm" with a
final x pad. Printed ciphertext NIJAM PBGQC WKHQJ EUIKY MPAT.

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
from engine.solvers.portax import (
    ACA_CIPHER,
    ACA_KEY,
    ACA_MESSAGE,
    ACA_PLAIN,
    ACA_PRINTED_CIPHER,
    ACA_URL,
    portax_decrypt,
    portax_encrypt,
    portax_pair,
    solve_portax,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1] / "engine" / "data" / "portax_certificate.json"
)


class PortaxScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.portax as portax_mod

        doc = (portax_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("kryptos k4", doc)
        self.assertIn("voynich", doc)
        self.assertIn("zodiac", doc)
        self.assertIn("beale", doc)
        self.assertIn("mccormick", doc)
        self.assertIn("ciphers/Portax.pdf", ACA_URL)
        self.assertNotIn("portax", SOLVERS)


class PortaxPublishedExampleTest(unittest.TestCase):
    """ACA sheet: EASY, the early bird gets the worm, plus the x pad."""

    def test_sheet_pairs_match_the_published_walkthrough(self) -> None:
        # Key E: plain ta becomes NM; bg, same column, becomes QH.
        self.assertEqual(portax_pair("T", "A", "E"), "NM")
        self.assertEqual(portax_pair("B", "G", "E"), "QH")
        # Key U or V: in becomes JL, no becomes UA, na becomes DB.
        self.assertEqual(portax_pair("I", "N", "U"), "JL")
        self.assertEqual(portax_pair("N", "O", "V"), "UA")
        self.assertEqual(portax_pair("N", "A", "U"), "DB")
        self.assertEqual(portax_pair("I", "N", "V"), "JL")

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = portax_encrypt(ACA_MESSAGE, ACA_KEY)
        self.assertEqual(cipher, ACA_CIPHER)
        self.assertEqual(portax_encrypt(ACA_PLAIN, "easy"), ACA_CIPHER)
        self.assertEqual(ACA_CIPHER, ACA_PRINTED_CIPHER.replace(" ", ""))

    def test_decrypt_recovers_published_plaintext_exactly(self) -> None:
        plain = portax_decrypt(ACA_PRINTED_CIPHER, ACA_KEY)
        self.assertEqual(plain, ACA_PLAIN)
        self.assertEqual(portax_decrypt(ACA_CIPHER, ACA_KEY), ACA_PLAIN)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_portax(ACA_CIPHER, key=ACA_KEY)
        self.assertEqual(result.plaintext, ACA_PLAIN)
        self.assertEqual(result.method, "portax")
        self.assertEqual(result.key, ACA_KEY)
        self.assertEqual(result.details["source_url"], ACA_URL)
        self.assertEqual(result.details["period"], 4)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)
        self.assertIn("kryptos k4", scope)
        self.assertIn("voynich", scope)
        self.assertIn("zodiac", scope)
        self.assertIn("beale", scope)
        self.assertIn("mccormick", scope)

    def test_reciprocal_map_roundtrips(self) -> None:
        again = portax_decrypt(portax_encrypt(ACA_MESSAGE, ACA_KEY), "easy")
        self.assertEqual(again, ACA_PLAIN)
        self.assertEqual(portax_encrypt(ACA_PLAIN, ACA_KEY), ACA_CIPHER)
        self.assertEqual(portax_decrypt(ACA_CIPHER, ACA_KEY), ACA_PLAIN)


class PortaxCertificateTest(unittest.TestCase):
    """Certificate checks the published ACA example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "portax")
        self.assertEqual(self.cert["name"], "portax")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(plaintext, ACA_PLAIN)
        self.assertEqual(ciphertext, ACA_CIPHER)
        self.assertEqual(self.cert["keys"]["key"], key)
        self.assertEqual(self.cert["message"], ACA_MESSAGE)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(portax_decrypt(ciphertext, key), plaintext)
        self.assertEqual(portax_encrypt(ACA_MESSAGE, key), ciphertext)
        self.assertEqual(portax_encrypt(plaintext, key), ciphertext)
        result = solve_portax(ciphertext, key=key)
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
        self.assertNotIn("\u2014", self.cert["note"])
        self.assertNotIn("\u2013", self.cert["note"])
        self.assertNotIn("\u2014", plaintext)
        self.assertNotIn("\u2013", plaintext)


if __name__ == "__main__":
    unittest.main()
