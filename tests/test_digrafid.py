"""Digrafid known-key recovery against a published worked example.

Source (fetched): https://www.cryptogram.org/downloads/aca.info/ciphers/Digrafid.pdf

This is a known classical-cipher solver test. It does not claim an
ancient-script or unknown-language reading.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.digrafid import (
    ACA_CIPHER,
    ACA_CIPHER_PERIOD_4,
    ACA_HORIZONTAL,
    ACA_PERIOD,
    ACA_PERIOD_4,
    ACA_PLAIN,
    ACA_URL,
    ACA_VERTICAL,
    alphabet_from_keyword,
    digrafid_decrypt,
    digrafid_encrypt,
    digrafid_symbols,
    solve_digrafid,
)


class DigrafidScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_ancient_script(self) -> None:
        import engine.solvers.digrafid as digrafid_mod

        doc = digrafid_mod.__doc__ or ""
        self.assertIn("known classical-cipher", doc.lower().replace("\n", " "))
        lowered = doc.lower()
        self.assertTrue(
            "ancient script" in lowered or "ancient-script" in lowered,
            msg="module docstring must say it does not read ancient scripts",
        )
        self.assertIn("cryptogram.org/downloads/aca.info/ciphers/Digrafid.pdf", ACA_URL)


class DigrafidPublishedExampleTest(unittest.TestCase):
    """ACA sheet: THISISTHEFORESTPRI with KEYWORD / VERTICAL, period 3 and 4."""

    def test_keywords_rebuild_the_printed_alphabets(self) -> None:
        self.assertEqual(alphabet_from_keyword("KEYWORD"), ACA_HORIZONTAL)
        self.assertEqual(alphabet_from_keyword("VERTICAL"), ACA_VERTICAL)
        self.assertEqual(len(ACA_HORIZONTAL), 27)
        self.assertEqual(len(ACA_VERTICAL), 27)
        self.assertIn("#", ACA_HORIZONTAL)
        self.assertIn("J", ACA_HORIZONTAL)

    def test_encrypt_matches_published_ciphertext_period_3(self) -> None:
        cipher = digrafid_encrypt(ACA_PLAIN, ACA_HORIZONTAL, ACA_VERTICAL, ACA_PERIOD)
        self.assertEqual(cipher, ACA_CIPHER)
        self.assertEqual(cipher, "HJMXWSWJADWGFCSPYI")

    def test_encrypt_matches_published_ciphertext_period_4(self) -> None:
        cipher = digrafid_encrypt(
            ACA_PLAIN, ACA_HORIZONTAL, ACA_VERTICAL, ACA_PERIOD_4
        )
        self.assertEqual(cipher, ACA_CIPHER_PERIOD_4)
        self.assertEqual(cipher, "HJTKVHYUFFWDSQYPRI")

    def test_decrypt_recovers_published_plaintext_exactly(self) -> None:
        plain = digrafid_decrypt(ACA_CIPHER, ACA_HORIZONTAL, ACA_VERTICAL, ACA_PERIOD)
        self.assertEqual(plain, ACA_PLAIN)
        self.assertEqual(plain, "THISISTHEFORESTPRI")

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_digrafid(
            ACA_CIPHER,
            horizontal=ACA_HORIZONTAL,
            vertical=ACA_VERTICAL,
            period=ACA_PERIOD,
        )
        self.assertEqual(result.plaintext, ACA_PLAIN)
        self.assertEqual(result.method, "digrafid")
        self.assertEqual(result.details["period"], 3)
        self.assertEqual(result.details["horizontal"], ACA_HORIZONTAL)
        self.assertEqual(result.details["vertical"], ACA_VERTICAL)
        self.assertIn("not an ancient-script", result.details["scope"].lower())
        self.assertEqual(result.details["source_url"], ACA_URL)

    def test_spaced_plaintext_roundtrips_to_same_letters(self) -> None:
        spaced = "This is the forest pri"
        cipher = digrafid_encrypt(spaced, ACA_HORIZONTAL, ACA_VERTICAL, ACA_PERIOD)
        self.assertEqual(cipher, ACA_CIPHER)
        plain = digrafid_decrypt(cipher, ACA_HORIZONTAL, ACA_VERTICAL, ACA_PERIOD)
        self.assertEqual(plain, digrafid_symbols(spaced))
        self.assertEqual(plain, ACA_PLAIN)
        self.assertNotIn(" ", plain)


class DigrafidCryptoCrackExampleTest(unittest.TestCase):
    """Second published example. CryptoCrack calls the block size Period 6 letters.

    That is 3 digraphs, the same period unit as the ACA fractionation.
    Source: https://sites.google.com/site/cryptocrackprogram/user-guide/cipher-types/other/digrafid
    The page adds a null X because 'Golf: A good walk ruined.' has an odd letter count.
    """

    def test_encrypt_matches_cryptocrack_ciphertext(self) -> None:
        horizontal = alphabet_from_keyword("GOLF")
        vertical = alphabet_from_keyword("CLUB")
        self.assertEqual(horizontal, "GOLFABCDEHIJKMNPQRSTUVWXYZ#")
        self.assertEqual(vertical, "CLUBADEFGHIJKMNOPQRSTVWXYZ#")
        # Letter stream of the quote plus the page's null X. Spaces are not included.
        plain = "GOLFAGOODWALKRUINEDX"
        cipher = digrafid_encrypt(plain, horizontal, vertical, 3)
        self.assertEqual(cipher, "GWOCYQTMORPIFXXKGODX")
        self.assertEqual(digrafid_decrypt(cipher, horizontal, vertical, 3), plain)


class DigrafidHelpersTest(unittest.TestCase):
    def test_odd_length_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            digrafid_encrypt("ABC", ACA_HORIZONTAL, ACA_VERTICAL, 3)

    def test_roundtrip_keeps_j_and_hash_symbol(self) -> None:
        plain = "JAZZ#Q"
        cipher = digrafid_encrypt(plain, ACA_HORIZONTAL, ACA_VERTICAL, 2)
        self.assertEqual(
            digrafid_decrypt(cipher, ACA_HORIZONTAL, ACA_VERTICAL, 2),
            plain,
        )


CERT_PATH = Path(__file__).resolve().parents[1] / "engine" / "data" / "digrafid_certificate.json"


class DigrafidCertificateTest(unittest.TestCase):
    """Certificate checks the ACA sheet example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "digrafid")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        keys = self.cert["keys"]
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertNotIn(" ", plaintext)
        self.assertEqual(plaintext, "THISISTHEFORESTPRI")
        self.assertEqual(
            digrafid_decrypt(
                ciphertext, keys["horizontal"], keys["vertical"], keys["period"]
            ),
            plaintext,
        )
        self.assertEqual(self.cert["source_url"], ACA_URL)
        self.assertIn("not an unknown script", self.cert["note"].lower())
        self.assertIn("no spaces", self.cert["note"].lower())


if __name__ == "__main__":
    unittest.main()
