"""Straddling checkerboard known-key recovery against a published worked example.

Source (fetched 2026-10-02):
https://en.wikipedia.org/wiki/Straddling_checkerboard

The article converts "ATTACK AT DAWN" with the printed board into
3113212731223655. Spaces are not encoded, so the recovered text is
ATTACKATDAWN.

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.straddling_checkerboard import (
    WIKIPEDIA_CHECKERBOARD_CIPHER,
    WIKIPEDIA_CHECKERBOARD_KEY,
    WIKIPEDIA_CHECKERBOARD_PLAIN,
    WIKIPEDIA_CHECKERBOARD_SOURCE_TEXT,
    WIKIPEDIA_CHECKERBOARD_URL,
    parse_checkerboard_key,
    solve_straddling_checkerboard,
    straddling_checkerboard_decrypt,
    straddling_checkerboard_encrypt,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "straddling_checkerboard_certificate.json"
)


class StraddlingCheckerboardScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.straddling_checkerboard as checkerboard_mod

        doc = (checkerboard_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("known-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("Straddling_checkerboard", WIKIPEDIA_CHECKERBOARD_URL)


class StraddlingCheckerboardPublishedExampleTest(unittest.TestCase):
    """Wikipedia board: rows 2 and 6, header ETAONRIS, ATTACK AT DAWN."""

    def test_board_matches_the_published_codes(self) -> None:
        board = parse_checkerboard_key(WIKIPEDIA_CHECKERBOARD_KEY)
        self.assertEqual(board.row_digits, ("2", "6"))
        self.assertEqual(board.header, "ETAONRIS")
        self.assertEqual(board.encode["A"], "3")
        self.assertEqual(board.encode["T"], "1")
        self.assertEqual(board.encode["C"], "21")
        self.assertEqual(board.encode["K"], "27")
        self.assertEqual(board.encode["D"], "22")
        self.assertEqual(board.encode["W"], "65")
        self.assertEqual(board.encode["N"], "5")
        self.assertEqual(board.encode["E"], "0")
        self.assertEqual(board.encode["/"], "62")
        self.assertEqual(board.encode["."], "69")

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = straddling_checkerboard_encrypt(
            WIKIPEDIA_CHECKERBOARD_SOURCE_TEXT,
            WIKIPEDIA_CHECKERBOARD_KEY,
        )
        self.assertEqual(cipher, WIKIPEDIA_CHECKERBOARD_CIPHER)
        self.assertEqual(cipher, "3113212731223655")
        self.assertEqual(WIKIPEDIA_CHECKERBOARD_SOURCE_TEXT, "ATTACK AT DAWN")

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_straddling_checkerboard(
            WIKIPEDIA_CHECKERBOARD_CIPHER,
            key=WIKIPEDIA_CHECKERBOARD_KEY,
        )
        self.assertEqual(result.plaintext, WIKIPEDIA_CHECKERBOARD_PLAIN)
        self.assertEqual(result.plaintext, "ATTACKATDAWN")
        self.assertEqual(result.method, "straddling_checkerboard")
        self.assertEqual(result.key, WIKIPEDIA_CHECKERBOARD_KEY)
        self.assertEqual(result.details["source_url"], WIKIPEDIA_CHECKERBOARD_URL)
        self.assertEqual(result.details["row_digits"], "2,6")
        self.assertEqual(result.details["header"], "ETAONRIS")
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_grouped_ciphertext_decrypts_to_the_same_letters(self) -> None:
        grouped = "31132 12731 22365 5"
        self.assertEqual(
            straddling_checkerboard_decrypt(grouped, WIKIPEDIA_CHECKERBOARD_KEY),
            WIKIPEDIA_CHECKERBOARD_PLAIN,
        )

    def test_bad_key_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            straddling_checkerboard_decrypt(WIKIPEDIA_CHECKERBOARD_CIPHER, "CAT")
        with self.assertRaises(ValueError):
            straddling_checkerboard_decrypt(WIKIPEDIA_CHECKERBOARD_CIPHER, "2,2|ETAONRIS|BCDFGHJKLMPQ/UVWXYZ.")


class StraddlingCheckerboardCertificateTest(unittest.TestCase):
    """Certificate checks the published Wikipedia example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "straddling checkerboard")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(plaintext, "ATTACKATDAWN")
        self.assertEqual(ciphertext, "3113212731223655")
        self.assertEqual(key, WIKIPEDIA_CHECKERBOARD_KEY)
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(straddling_checkerboard_decrypt(ciphertext, key), plaintext)
        result = solve_straddling_checkerboard(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], WIKIPEDIA_CHECKERBOARD_URL)
        note = self.cert["note"].lower()
        self.assertIn("known-cipher", note)
        self.assertIn("not an unknown-script", note)
        self.assertIn("nr. 86", note)


if __name__ == "__main__":
    unittest.main()
