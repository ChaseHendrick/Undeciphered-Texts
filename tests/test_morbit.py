"""Supplied-key Morbit against the independently printed ACA example."""

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.morbit import morbit_decrypt, morbit_encrypt, morbit_key, solve_morbit

PLAIN = "ONCE UPON A TIME"
CIPHER = "27435 88151 28274 65679 378."
COMPACT = "27435881512827465679378"
CERT = Path(__file__).parents[1] / "engine/data/morbit_certificate.json"


class MorbitTest(unittest.TestCase):
    def test_keyword_ranking_breaks_duplicate_letters_left_to_right(self):
        self.assertEqual(morbit_key("WISECRACK"), "958427136")
        self.assertEqual(morbit_key("wisecrack"), "958427136")
        self.assertEqual(morbit_key("958427136"), "958427136")

    def test_published_encryption_and_decryption_literals(self):
        self.assertEqual(morbit_encrypt(PLAIN, "WISECRACK"), COMPACT)
        self.assertEqual(morbit_decrypt(CIPHER, "WISECRACK", terminal_period=True), PLAIN)
        self.assertEqual(morbit_decrypt(COMPACT, "958427136"), PLAIN)

    def test_solve_result_requires_key_and_records_framing(self):
        result = solve_morbit(CIPHER, key="WISECRACK", terminal_period=True)
        self.assertEqual(result.plaintext, PLAIN)
        self.assertEqual(result.method, "morbit")
        self.assertEqual(result.key, "958427136")
        self.assertEqual(result.details["mode"], "known_key")
        self.assertTrue(result.details["terminal_period_is_framing"])
        with self.assertRaises(TypeError):
            solve_morbit(COMPACT)

    def test_certificate_hashes_the_recovered_word_spaces(self):
        certificate = json.loads(CERT.read_text())
        recovered = morbit_decrypt(certificate["ciphertext"], certificate["keys"]["key"], terminal_period=True)
        self.assertEqual(recovered, PLAIN)
        self.assertEqual(certificate["plaintext"], PLAIN)
        self.assertEqual(certificate["plaintext_sha256"], hashlib.sha256(recovered.encode("ascii")).hexdigest())

    def test_general_morse_letters_numbers_and_encoded_punctuation(self):
        for text in ("E", "SOS! 2026?", "a.b, c:d", "Q @ HOME", "X - Y"):
            with self.subTest(text=text):
                encrypted = morbit_encrypt(text, "123456789")
                self.assertEqual(morbit_decrypt(encrypted, "123456789"), text.upper())
        self.assertEqual(morbit_decrypt("3", "123456789"), "E")

    def test_ciphertext_period_requires_explicit_framing(self):
        with self.assertRaises(ValueError):
            morbit_decrypt(CIPHER, "WISECRACK")
        for text in ("27.43", "27..", ".", "0", "12,34", "\u0661"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                morbit_decrypt(text, "WISECRACK", terminal_period=True)

    def test_invalid_morse_gaps_and_tokens_are_rejected(self):
        for text in ("7", "99", "59", "1151"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                morbit_decrypt(text, "123456789")

    def test_types_keys_and_finite_input_bounds(self):
        for key in ("", "SHORT", "123456788", "ABCDEFGHIJ", "ABCDE1234", "\u00e9ABCDEFGH"):
            with self.subTest(key=key), self.assertRaises(ValueError):
                morbit_key(key)
        with self.assertRaises(TypeError):
            morbit_key(None)
        for text in ("", "  ", "\u00df", "\u017f", "\u0131", "A" * 10001):
            with self.assertRaises(ValueError):
                morbit_encrypt(text, "WISECRACK")
        with self.assertRaises(ValueError):
            morbit_decrypt("1" * 100001, "WISECRACK")
        with self.assertRaises(TypeError):
            morbit_decrypt("1", "WISECRACK", terminal_period=1)


if __name__ == "__main__":
    unittest.main()
