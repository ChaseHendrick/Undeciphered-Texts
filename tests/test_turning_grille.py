"""Turning grille known-stencil recovery against a published worked example.

Source (fetched 2026-10-03):
https://www.cryptogram.org/downloads/aca.info/ciphers/Grille.pdf

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers import SOLVERS
from engine.solvers.turning_grille import (
    ACA_GRILLE_CIPHER,
    ACA_GRILLE_PLAIN,
    ACA_GRILLE_SHEET_PLAIN,
    ACA_GRILLE_STENCIL,
    ACA_GRILLE_URL,
    parse_stencil,
    solve_turning_grille,
    turning_grille_decrypt,
    turning_grille_encrypt,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "turning_grille_certificate.json"
)


class TurningGrilleScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.turning_grille as grille_mod

        doc = (grille_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("known-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("grille.pdf", ACA_GRILLE_URL.lower())
        self.assertNotIn("turning_grille", SOLVERS)
        self.assertNotIn("grille", SOLVERS)


class TurningGrillePublishedExampleTest(unittest.TestCase):
    """ACA sheet: stencil 1 8 10 12, plaintext the turning grille."""

    def test_stencil_is_the_published_openings(self) -> None:
        side, numbers = parse_stencil(ACA_GRILLE_STENCIL)
        self.assertEqual(side, 4)
        self.assertEqual(numbers, (1, 8, 10, 12))
        self.assertEqual(ACA_GRILLE_STENCIL, "1 8 10 12")

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = turning_grille_encrypt(ACA_GRILLE_SHEET_PLAIN, ACA_GRILLE_STENCIL)
        self.assertEqual(cipher, ACA_GRILLE_CIPHER)
        self.assertEqual(cipher, "TILUN RGHGE LTENI R")
        self.assertEqual(
            turning_grille_encrypt(ACA_GRILLE_PLAIN, "12 10 8 1"),
            ACA_GRILLE_CIPHER,
        )

    def test_decrypt_recovers_published_letters(self) -> None:
        plain = turning_grille_decrypt(ACA_GRILLE_CIPHER, ACA_GRILLE_STENCIL)
        self.assertEqual(plain, ACA_GRILLE_PLAIN)
        self.assertEqual(plain, "THETURNINGGRILLE")
        # The printed line ends with a period. That period is not a cell.
        self.assertEqual(
            turning_grille_decrypt("TILUN RGHGE LTENI R.", ACA_GRILLE_STENCIL),
            ACA_GRILLE_PLAIN,
        )

    def test_sheet_plaintext_letters_match_the_stored_letters(self) -> None:
        letters = "".join(
            ch.upper() for ch in ACA_GRILLE_SHEET_PLAIN if ch.isascii() and ch.isalpha()
        )
        self.assertEqual(letters, ACA_GRILLE_PLAIN)
        self.assertEqual(ACA_GRILLE_SHEET_PLAIN, "the turning grille")

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_turning_grille(ACA_GRILLE_CIPHER, key=ACA_GRILLE_STENCIL)
        self.assertEqual(result.plaintext, ACA_GRILLE_PLAIN)
        self.assertEqual(result.plaintext, "THETURNINGGRILLE")
        self.assertEqual(result.method, "turning_grille")
        self.assertEqual(result.key, ACA_GRILLE_STENCIL)
        self.assertEqual(result.details["source_url"], ACA_GRILLE_URL)
        self.assertEqual(result.details["stencil"], "1 8 10 12")
        self.assertEqual(result.details["side"], 4)
        self.assertEqual(result.details["direction"], "clockwise")
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_roundtrip_on_a_two_by_two_stencil(self) -> None:
        # One opening at cell 1 covers a 2 by 2 square under four turns.
        cipher = turning_grille_encrypt("ABCD", "1")
        self.assertEqual(cipher, "ABDC")
        self.assertEqual(turning_grille_decrypt(cipher, "1"), "ABCD")

    def test_overlapping_stencil_and_bad_length_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            turning_grille_encrypt(ACA_GRILLE_PLAIN, "1 2 3 4")
        with self.assertRaises(ValueError):
            turning_grille_decrypt(ACA_GRILLE_CIPHER, "")
        with self.assertRaises(ValueError):
            turning_grille_encrypt("SHORT", ACA_GRILLE_STENCIL)
        with self.assertRaises(ValueError):
            turning_grille_decrypt("...", ACA_GRILLE_STENCIL)


class TurningGrilleCertificateTest(unittest.TestCase):
    """Certificate checks the published ACA example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "turning_grille")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["stencil"], "1 8 10 12")
        self.assertEqual(self.cert["keys"]["side"], 4)
        self.assertEqual(key, "1 8 10 12")
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(turning_grille_decrypt(ciphertext, key), plaintext)
        self.assertEqual(turning_grille_encrypt(plaintext, key), ciphertext)
        result = solve_turning_grille(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], ACA_GRILLE_URL)
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
