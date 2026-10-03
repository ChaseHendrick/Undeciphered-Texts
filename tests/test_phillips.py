"""Phillips known-key recovery against a published worked example.

Source (fetched 2026-10-02):
https://www.cwu.edu/academics/math/_documents/kryptos-challenges/cwu-kryptos-challenge-phillips-cipher.pdf

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.phillips import (
    CWU_PHILLIPS_CIPHER,
    CWU_PHILLIPS_KEY,
    CWU_PHILLIPS_PLAIN,
    CWU_PHILLIPS_URL,
    phillips_decrypt,
    phillips_encrypt,
    phillips_square,
    solve_phillips,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "phillips_certificate.json"
)


class PhillipsScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.phillips as phillips_mod

        doc = (phillips_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn(
            "cwu-kryptos-challenge-phillips-cipher.pdf",
            CWU_PHILLIPS_URL,
        )


class PhillipsPublishedExampleTest(unittest.TestCase):
    """CWU sheet: COMPETE, squares one and five... -> letter-row ciphertext."""

    def test_square_matches_the_published_keyword_square(self) -> None:
        self.assertEqual(
            phillips_square(CWU_PHILLIPS_KEY),
            ("COMPE", "TABDF", "GHIKL", "NQRSU", "VWXYZ"),
        )

    def test_first_lookup_matches_the_published_walkthrough(self) -> None:
        # Sheet: plaintext S on grid 1 is replaced by Z.
        self.assertEqual(phillips_encrypt("S", CWU_PHILLIPS_KEY), "Z")

    def test_encrypt_matches_published_letter_rows(self) -> None:
        cipher = phillips_encrypt(CWU_PHILLIPS_PLAIN, CWU_PHILLIPS_KEY)
        self.assertEqual(cipher, CWU_PHILLIPS_CIPHER)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_phillips(CWU_PHILLIPS_CIPHER, key=CWU_PHILLIPS_KEY)
        self.assertEqual(result.plaintext, CWU_PHILLIPS_PLAIN)
        self.assertEqual(result.method, "phillips")
        self.assertEqual(result.key, CWU_PHILLIPS_KEY)
        self.assertEqual(result.details["source_url"], CWU_PHILLIPS_URL)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_roundtrip_with_spaced_plaintext(self) -> None:
        sentence = "squares one and five are the same and so are two and eight"
        again = phillips_decrypt(
            phillips_encrypt(sentence, "compete"),
            CWU_PHILLIPS_KEY,
        )
        self.assertEqual(again, CWU_PHILLIPS_PLAIN)

    def test_empty_keyword_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            phillips_decrypt(CWU_PHILLIPS_CIPHER, "...")


class PhillipsCertificateTest(unittest.TestCase):
    """Certificate checks the published CWU example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "phillips")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["key"], key)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(phillips_decrypt(ciphertext, key), plaintext)
        result = solve_phillips(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], CWU_PHILLIPS_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown-script", note)
        self.assertIn("nr. 86", note)


if __name__ == "__main__":
    unittest.main()
