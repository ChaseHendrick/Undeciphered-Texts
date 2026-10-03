"""Bazeries known-key recovery against a published worked example.

Source (fetched 2026-10-02):
https://www.cryptogram.org/downloads/aca.info/ciphers/Bazeries.pdf

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.bazeries import (
    ACA_CIPHER,
    ACA_KEY,
    ACA_PLAIN,
    ACA_URL,
    bazeries_decrypt,
    bazeries_encrypt,
    ciphertext_square,
    plaintext_square,
    solve_bazeries,
    spell_bazeries_number,
)


CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "bazeries_certificate.json"


class BazeriesScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.bazeries as bazeries_mod

        doc = (bazeries_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("cryptogram.org/downloads/aca.info/ciphers/bazeries.pdf", ACA_URL.lower())


class BazeriesPublishedExampleTest(unittest.TestCase):
    """ACA sheet: SIMPLESUBSTITUTIONPLUSTRANSPOSITION + 3752 → ACYYUX…"""

    def test_squares_match_the_published_sheet(self) -> None:
        self.assertEqual(
            plaintext_square(),
            ["AFLQV", "BGMRW", "CHNSX", "DIOTY", "EKPUZ"],
        )
        self.assertEqual(
            ciphertext_square(ACA_KEY),
            ["THREO", "USAND", "VFIYW", "BCGKL", "MPQXZ"],
        )
        # 3752 spelled out is the keyword that fills that ciphertext square.
        self.assertEqual(spell_bazeries_number(ACA_KEY), "THREETHOUSANDSEVENHUNDREDFIFTYTWO")

    def test_first_reversed_group_matches_the_published_walkthrough(self) -> None:
        # Sheet: groups of 3, 7, 5, 2. SIM reverses to MIS, which enciphers as ACY.
        self.assertEqual(bazeries_encrypt("SIM", ACA_KEY), "ACY")

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = bazeries_encrypt(ACA_PLAIN, ACA_KEY)
        self.assertEqual(cipher, ACA_CIPHER)
        self.assertEqual(cipher, "ACYYUXYMRQKXKCKGCRQIYITNKYXKCYGQGCI")

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_bazeries(ACA_CIPHER, key=ACA_KEY)
        self.assertEqual(result.plaintext, ACA_PLAIN)
        self.assertEqual(result.method, "bazeries")
        self.assertEqual(result.key, ACA_KEY)
        self.assertEqual(result.details["source_url"], ACA_URL)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_roundtrip(self) -> None:
        again = bazeries_decrypt(bazeries_encrypt(ACA_PLAIN, "3752"), 3752)
        self.assertEqual(again, ACA_PLAIN)


class BazeriesCertificateTest(unittest.TestCase):
    """Certificate checks the published ACA example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "bazeries")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["key"], key)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(bazeries_decrypt(ciphertext, key), plaintext)
        result = solve_bazeries(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], ACA_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown script", note)
        self.assertIn("nr. 86", note)


if __name__ == "__main__":
    unittest.main()
