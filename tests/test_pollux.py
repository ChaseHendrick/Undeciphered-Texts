"""Strict supplied-map Pollux and the literal ACA printed ciphertext."""

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.pollux import pollux_decrypt, pollux_encrypt, pollux_key, solve_pollux

KEY = ".x-..x.--x"
PLAIN = "LUCK HELPS"
CIPHER = "08639 34257 02417 68596 30414 56234 90874 5360."
COMPACT = "086393425702417685963041456234908745360"
CERT = Path(__file__).parents[1] / "engine/data/pollux_certificate.json"


class PolluxTest(unittest.TestCase):
    def test_published_literal_decrypts_with_digit_order_zero_through_nine(self):
        self.assertEqual(pollux_decrypt(CIPHER, KEY, terminal_period=True), PLAIN)
        self.assertEqual(pollux_decrypt(COMPACT, KEY), PLAIN)

    def test_complete_mapping_and_string_keys_are_equivalent(self):
        mapping = {str(index): symbol for index, symbol in enumerate(KEY)}
        self.assertEqual(pollux_key(mapping), KEY)
        self.assertEqual(pollux_decrypt(COMPACT, mapping), PLAIN)

    def test_published_encryption_with_explicit_homophone_choices(self):
        self.assertEqual(pollux_encrypt(PLAIN, KEY, choices=COMPACT), COMPACT)
        with self.assertRaises(ValueError):
            pollux_encrypt(PLAIN, KEY, choices="1" * len(COMPACT))
        with self.assertRaises(ValueError):
            pollux_encrypt(PLAIN, KEY, choices=COMPACT[:-1])

    def test_deterministic_default_homophones_and_general_morse(self):
        for text in ("E", "SOS! 2026?", "A.B", "Q @ HOME"):
            cipher = pollux_encrypt(text, KEY)
            self.assertEqual(cipher, pollux_encrypt(text, KEY))
            self.assertEqual(pollux_decrypt(cipher, KEY), text.upper())

    def test_solve_metadata_and_certificate_hash(self):
        result = solve_pollux(CIPHER, key=KEY, terminal_period=True)
        self.assertEqual(result.plaintext, PLAIN)
        self.assertEqual(result.details["mode"], "known_key")
        self.assertEqual(result.key, KEY)
        certificate = json.loads(CERT.read_text())
        recovered = pollux_decrypt(certificate["ciphertext"], certificate["keys"]["key"], terminal_period=True)
        self.assertEqual(recovered, PLAIN)
        self.assertEqual(certificate["plaintext_sha256"], hashlib.sha256(recovered.encode("ascii")).hexdigest())

    def test_missing_maps_ambiguous_symbols_and_types_fail(self):
        for key in (".........x", ".x-..x.--", ".x-..x.--?", {"0": "."}, {str(i): ".-" for i in range(10)}):
            with self.subTest(key=key), self.assertRaises(ValueError):
                pollux_key(key)
        for key in (None, 123, []):
            with self.assertRaises(TypeError):
                pollux_key(key)
        with self.assertRaises(TypeError):
            solve_pollux(COMPACT)

    def test_strict_morse_rejects_leading_trailing_or_excess_dividers(self):
        for text in ("111", "6666666", "31", "12", "31113"):
            with self.subTest(text=text), self.assertRaises(ValueError):
                pollux_decrypt(text, KEY)
        with self.assertRaises(ValueError):
            pollux_decrypt(CIPHER, KEY)
        with self.assertRaises(ValueError):
            pollux_decrypt("0.0", KEY, terminal_period=True)

    def test_finite_bounds_and_plaintext_validation(self):
        for text in ("", "   ", "\u00e9", "\u017f", "\u0131", "A" * 10001):
            with self.assertRaises(ValueError):
                pollux_encrypt(text, KEY)
        with self.assertRaises(ValueError):
            pollux_decrypt("0" * 100001, KEY)
        with self.assertRaises(TypeError):
            pollux_decrypt("0", KEY, terminal_period=1)


if __name__ == "__main__":
    unittest.main()
