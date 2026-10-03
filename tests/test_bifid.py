"""Bifid known-key recovery against a published worked example.

Source (fetched): http://practicalcryptography.com/ciphers/bifid-cipher/

This is a known classical-cipher solver test. It does not claim an
ancient-script or unknown-language reading.
"""

from __future__ import annotations

import unittest

from engine.solvers.bifid import (
    PRACTICAL_CRYPTOGRAPHY_CIPHER,
    PRACTICAL_CRYPTOGRAPHY_PERIOD,
    PRACTICAL_CRYPTOGRAPHY_PLAIN,
    PRACTICAL_CRYPTOGRAPHY_SQUARE,
    PRACTICAL_CRYPTOGRAPHY_URL,
    bifid_decrypt,
    bifid_encrypt,
    bifid_letters,
    solve_bifid,
    square_from_keyword,
)


class BifidScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_ancient_script(self) -> None:
        import engine.solvers.bifid as bifid_mod

        doc = bifid_mod.__doc__ or ""
        self.assertIn("known classical-cipher", doc.lower().replace("\n", " "))
        # Accept either phrasing used in the module docstring.
        lowered = doc.lower()
        self.assertTrue(
            "ancient script" in lowered or "ancient-script" in lowered,
            msg="module docstring must say it does not read ancient scripts",
        )
        self.assertIn("practicalcryptography.com/ciphers/bifid-cipher", PRACTICAL_CRYPTOGRAPHY_URL)


class BifidPublishedExampleTest(unittest.TestCase):
    """Practical Cryptography: defend…castle → FFYHMK… with square + period 5."""

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = bifid_encrypt(
            PRACTICAL_CRYPTOGRAPHY_PLAIN,
            PRACTICAL_CRYPTOGRAPHY_SQUARE,
            PRACTICAL_CRYPTOGRAPHY_PERIOD,
        )
        self.assertEqual(cipher, PRACTICAL_CRYPTOGRAPHY_CIPHER)

    def test_decrypt_recovers_published_plaintext_exactly(self) -> None:
        plain = bifid_decrypt(
            PRACTICAL_CRYPTOGRAPHY_CIPHER,
            PRACTICAL_CRYPTOGRAPHY_SQUARE,
            PRACTICAL_CRYPTOGRAPHY_PERIOD,
        )
        self.assertEqual(plain, PRACTICAL_CRYPTOGRAPHY_PLAIN)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        # Solver is handed the published keysquare and period, not the plaintext.
        result = solve_bifid(
            PRACTICAL_CRYPTOGRAPHY_CIPHER,
            square=PRACTICAL_CRYPTOGRAPHY_SQUARE,
            period=PRACTICAL_CRYPTOGRAPHY_PERIOD,
        )
        self.assertEqual(result.plaintext, PRACTICAL_CRYPTOGRAPHY_PLAIN)
        self.assertEqual(result.method, "bifid")
        self.assertEqual(result.details["period"], 5)
        self.assertEqual(result.details["square"], PRACTICAL_CRYPTOGRAPHY_SQUARE.upper())
        self.assertIn("not an ancient-script", result.details["scope"].lower())
        self.assertEqual(result.details["source_url"], PRACTICAL_CRYPTOGRAPHY_URL)

    def test_spaced_plaintext_roundtrips_to_same_letters(self) -> None:
        spaced = "defend the east wall of the castle"
        cipher = bifid_encrypt(
            spaced,
            PRACTICAL_CRYPTOGRAPHY_SQUARE,
            PRACTICAL_CRYPTOGRAPHY_PERIOD,
        )
        self.assertEqual(cipher, PRACTICAL_CRYPTOGRAPHY_CIPHER)
        plain = bifid_decrypt(
            cipher,
            PRACTICAL_CRYPTOGRAPHY_SQUARE,
            PRACTICAL_CRYPTOGRAPHY_PERIOD,
        )
        self.assertEqual(plain, bifid_letters(spaced))
        self.assertEqual(plain, PRACTICAL_CRYPTOGRAPHY_PLAIN)


class BifidHelpersTest(unittest.TestCase):
    def test_keyword_square_puts_keyword_first(self) -> None:
        square = square_from_keyword("CIPHER")
        self.assertEqual(square[:6], "CIPHER")
        self.assertEqual(len(square), 25)
        self.assertNotIn("J", square)
        self.assertEqual(len(set(square)), 25)

    def test_j_folds_to_i(self) -> None:
        self.assertEqual(bifid_letters("Jazz"), "IAZZ")


if __name__ == "__main__":
    unittest.main()
