"""Independent ACA Monome-Dinome box and variable-length parsing."""

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.monome_dinome import keyed_alphabet, monome_dinome_decrypt, monome_dinome_encrypt, solve_monome_dinome

KEY = "NOTARIES"
DIGITS = "6318927054"
ALPHABET = "NOTARIESBCDFGHKLMPQUVWXY"
PLAIN = "HIGHFREQUENCYKEYSSHORTENCIPHERTEXT"
CIPHER = "60067 60627 53932 51683 46553 44460 87951 68038 60579 5359."
COMPACT = "6006760627539325168346553444608795168038605795359"
CERT = Path(__file__).parents[1] / "engine/data/monome_dinome_certificate.json"


class MonomeDinomeTest(unittest.TestCase):
    def test_printed_box_and_literal_ciphertext(self):
        self.assertEqual(keyed_alphabet(KEY), ALPHABET)
        self.assertEqual(monome_dinome_encrypt(PLAIN, KEY, digit_order=DIGITS), COMPACT)
        self.assertEqual(monome_dinome_decrypt(CIPHER, KEY, digit_order=DIGITS, terminal_period=True), PLAIN)

    def test_single_digits_row_prefixes_and_declared_merges(self):
        self.assertEqual(monome_dinome_encrypt("IJ YZ", KEY, digit_order=DIGITS), "003434")
        self.assertEqual(monome_dinome_decrypt("003434", KEY, digit_order=DIGITS), "IIYY")
        for plain, cipher in (("N", "1"), ("B", "61"), ("P", "38"), ("Y", "34")):
            self.assertEqual(monome_dinome_encrypt(plain, KEY, digit_order=DIGITS), cipher)
            self.assertEqual(monome_dinome_decrypt(cipher, KEY, digit_order=DIGITS), plain)

    def test_alternative_merge_and_digit_orders(self):
        text = "JAZZ QUILT"
        cipher = monome_dinome_encrypt(text, "KEYWORD", digit_order="9876543210", merge=("Q", "Z"))
        self.assertEqual(monome_dinome_decrypt(cipher, "KEYWORD", digit_order="9876543210", merge=("Q", "Z")), "IAQQQUILT")
        self.assertEqual(len(keyed_alphabet("KEYWORD", merge=("Q", "Z"))), 24)

    def test_certificate_hash_and_lossy_result_metadata(self):
        certificate = json.loads(CERT.read_text())
        result = solve_monome_dinome(certificate["ciphertext"], key=certificate["keys"]["key"], digit_order=DIGITS, terminal_period=True)
        self.assertEqual(result.plaintext, PLAIN)
        self.assertEqual(result.details["mode"], "known_key")
        self.assertEqual(result.details["letter_merges"], {"J": "I", "Z": "Y"})
        self.assertTrue(result.details["lossy"])
        self.assertEqual(certificate["plaintext_sha256"], hashlib.sha256(result.plaintext.encode("ascii")).hexdigest())

    def test_prefix_without_column_and_prefix_as_column_fail(self):
        for cipher in ("6", "3", "66", "33", "63", "36", "1236"):
            with self.subTest(cipher=cipher), self.assertRaises(ValueError):
                monome_dinome_decrypt(cipher, KEY, digit_order=DIGITS)

    def test_period_and_punctuation_are_explicit_framing(self):
        with self.assertRaises(ValueError):
            monome_dinome_decrypt(CIPHER, KEY, digit_order=DIGITS)
        for cipher in ("60.0", "600..", "\u0661", "A12", "1,2"):
            with self.assertRaises(ValueError):
                monome_dinome_decrypt(cipher, KEY, digit_order=DIGITS, terminal_period=True)
        with self.assertRaises(ValueError):
            monome_dinome_encrypt("HIGH!", KEY)

    def test_keys_parameters_types_and_finite_bounds(self):
        for key in ("", "   ", "\u00e9", "KEY!", "A" * 1001):
            with self.assertRaises(ValueError):
                keyed_alphabet(key)
        for digits in ("012345678", "0012345678", "ABCDEFGHIJ"):
            with self.assertRaises(ValueError):
                monome_dinome_encrypt("ABC", KEY, digit_order=digits)
        for merge in (("I", "Z"), ("Q", "Q"), ("Q", "J"), ("q", "Z"), ("A",)):
            with self.assertRaises((ValueError, TypeError)):
                keyed_alphabet(KEY, merge=merge)
        with self.assertRaises(TypeError):
            keyed_alphabet(None)
        with self.assertRaises(TypeError):
            solve_monome_dinome("1")
        with self.assertRaises(ValueError):
            monome_dinome_encrypt("A" * 10001, KEY)
        with self.assertRaises(ValueError):
            monome_dinome_decrypt("1" * 100001, KEY)
        with self.assertRaises(TypeError):
            monome_dinome_decrypt("1", KEY, terminal_period=1)


if __name__ == "__main__":
    unittest.main()
