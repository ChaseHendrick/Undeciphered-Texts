"""FBI one-letter shift known-key recovery against a published example.

Source (fetched 2026-10-03):
https://web.archive.org/web/20110405112022/http://www.fbi.gov/news/stories/2011/march/cryptanalysis_032911

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
It does not read the unsolved notes in that FBI article.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.fbi_letter_shift import (
    FBI_LETTER_SHIFT_CIPHER,
    FBI_LETTER_SHIFT_PLAIN,
    FBI_LETTER_SHIFT_RIGHT,
    FBI_LETTER_SHIFT_URL,
    fbi_letter_shift_decrypt,
    fbi_letter_shift_encrypt,
    solve_fbi_letter_shift,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "fbi_letter_shift_certificate.json"
)


class FbiLetterShiftScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.fbi_letter_shift as mod

        doc = (mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("known-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("kryptos k4", doc)
        self.assertIn("unsolved notes", doc)
        self.assertIn("cryptanalysis_032911", FBI_LETTER_SHIFT_URL)


class FbiLetterShiftPublishedExampleTest(unittest.TestCase):
    """FBI page: shift one letter right, Meet me at the park at noon."""

    def test_encrypt_matches_published_ciphertext(self) -> None:
        self.assertEqual(
            fbi_letter_shift_encrypt(FBI_LETTER_SHIFT_PLAIN, FBI_LETTER_SHIFT_RIGHT),
            FBI_LETTER_SHIFT_CIPHER,
        )

    def test_decrypt_matches_published_plaintext(self) -> None:
        self.assertEqual(
            fbi_letter_shift_decrypt(FBI_LETTER_SHIFT_CIPHER, FBI_LETTER_SHIFT_RIGHT),
            FBI_LETTER_SHIFT_PLAIN,
        )

    def test_spaces_and_case_follow_the_printed_cipher(self) -> None:
        self.assertEqual(FBI_LETTER_SHIFT_CIPHER[0], "N")
        self.assertTrue(FBI_LETTER_SHIFT_CIPHER[1:].islower())
        self.assertEqual(FBI_LETTER_SHIFT_PLAIN, "Meet me at the park at noon")
        self.assertNotIn(".", FBI_LETTER_SHIFT_CIPHER)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_fbi_letter_shift(
            FBI_LETTER_SHIFT_CIPHER, shift_right=FBI_LETTER_SHIFT_RIGHT
        )
        self.assertEqual(result.plaintext, FBI_LETTER_SHIFT_PLAIN)
        self.assertEqual(result.method, "fbi-letter-shift")
        self.assertEqual(result.key, "1")
        self.assertEqual(result.details["shift_right"], 1)
        self.assertEqual(result.details["source_url"], FBI_LETTER_SHIFT_URL)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)
        self.assertIn("kryptos k4", scope)
        self.assertIn("unsolved notes", scope)

    def test_empty_text_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            fbi_letter_shift_decrypt("...")


class FbiLetterShiftCertificateTest(unittest.TestCase):
    """Certificate checks the published FBI example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "fbi-letter-shift")
        self.assertEqual(self.cert["name"], "fbi-letter-shift")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        self.assertEqual(plaintext, FBI_LETTER_SHIFT_PLAIN)
        self.assertEqual(ciphertext, FBI_LETTER_SHIFT_CIPHER)
        self.assertEqual(self.cert["keys"]["shift_right"], 1)
        self.assertEqual(self.cert["key"], "1")
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(
            fbi_letter_shift_decrypt(ciphertext, self.cert["keys"]["shift_right"]),
            plaintext,
        )
        result = solve_fbi_letter_shift(
            ciphertext, shift_right=self.cert["keys"]["shift_right"]
        )
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], FBI_LETTER_SHIFT_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown-script", note)
        self.assertIn("nr. 86", note)
        self.assertIn("kryptos k4", note)
        self.assertIn("voynich", note)
        self.assertIn("linear a", note)
        self.assertIn("indus", note)
        self.assertIn("rongorongo", note)
        self.assertIn("unsolved notes", note)
        self.assertNotIn("\u2014", note)
        self.assertNotIn("\u2013", note)


if __name__ == "__main__":
    unittest.main()
