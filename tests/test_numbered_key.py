"""Literal ACA numbered homophones, preserved duplicates and strict code parser."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

from engine.solvers.numbered_key import (
    numbered_key_alphabet, numbered_key_decrypt, numbered_key_encrypt,
    solve_numbered_key,
)

KEY = "I like ciphers."
PLAIN = "THEROADTOSUCCESSISALWAYSUNDERCONSTRUCTION"
CIPHER = "04 19 20 21 02 23 25 04 02 22 05 16 16 15 22 22 11 22 23 12 07 23 09 22 05 01 25 20 21 16 02 01 22 04 21 05 16 04 17 02 01"


class NumberedKeyTest(unittest.TestCase):
    def test_literal_extended_rotated_alphabet_and_published_cipher(self):
        self.assertEqual(numbered_key_alphabet(KEY), "ILIKECIPHERSABDFGJMNOQTUVWXYZ")
        self.assertEqual(numbered_key_alphabet(KEY, start=18), "MNOQTUVWXYZILIKECIPHERSABDFGJ")
        self.assertEqual(numbered_key_decrypt(CIPHER + ".", KEY, start=18), PLAIN)
        self.assertEqual(solve_numbered_key(CIPHER, key=KEY, start=18).plaintext, PLAIN)
        # Replay the sheet's chosen homophones: E uses 20,15,20; I uses 11,17.
        choices = []
        table = "MNOQTUVWXYZILIKECIPHERSABDFGJ"
        for letter, code in zip(PLAIN, map(int, CIPHER.split())):
            choices.append([i for i, symbol in enumerate(table) if symbol == letter].index(code))
        self.assertEqual(numbered_key_encrypt(PLAIN, KEY, start=18, homophone_indices=choices), CIPHER)

    def test_repeated_letters_are_homophones_not_deduplicated(self):
        self.assertEqual(numbered_key_decrypt("11 13 17 15 20", KEY, start=18), "IIIEE")
        self.assertEqual(numbered_key_encrypt("III", KEY, start=18), "11 11 11")
        self.assertEqual(numbered_key_encrypt("III", KEY, start=18, homophone_indices=(0, 1, 2)), "11 13 17")

    def test_independent_index_mapping_for_every_letter_and_rotation(self):
        plain = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
        for key in ("AAA", "ZEBRA", "I like ciphers."):
            letters = "".join(ch for ch in key.upper() if "A" <= ch <= "Z")
            extended = letters + "".join(ch for ch in plain if ch not in letters)
            for start in range(len(extended)):
                table = extended[start:] + extended[:start]
                codes = " ".join(f"{table.index(ch):02d}" for ch in plain)
                self.assertEqual(numbered_key_encrypt(plain, key, start=start), codes)
                self.assertEqual(numbered_key_decrypt(codes, key, start=start), plain)

    def test_rejects_invalid_symbols_codes_keys_and_homophone_choices(self):
        for text in ("1", "-1", "100", "29", "１１", "04,19", "04 A9", ""):
            with self.assertRaises(ValueError):
                numbered_key_decrypt(text, KEY, start=18)
        for text in ((True,), (-1,), (29,), (1.0,), None):
            with self.assertRaises((ValueError, TypeError)):
                numbered_key_decrypt(text, KEY, start=18)
        for start in (-1, 29, True, "18"):
            with self.assertRaises((ValueError, TypeError)):
                numbered_key_alphabet(KEY, start=start)
        for key in ("", "123", "CAFÉ", "A" * 100, None):
            with self.assertRaises((ValueError, TypeError)):
                numbered_key_alphabet(key)
        for choices in ((3,), (True,), (), (0, 1)):
            with self.assertRaises((ValueError, TypeError)):
                numbered_key_encrypt("I", KEY, start=18, homophone_indices=choices)

    def test_certificate_hashes_literal_recovered_output(self):
        cert = json.loads((Path(__file__).parents[1] / "engine/data/numbered_key_certificate.json").read_text())
        recovered = numbered_key_decrypt(cert["ciphertext"], cert["keys"]["key"], start=cert["keys"]["start"])
        self.assertEqual(cert["ciphertext"], CIPHER)
        self.assertEqual(recovered, PLAIN)
        self.assertEqual(hashlib.sha256(recovered.encode("ascii")).hexdigest(), cert["plaintext_sha256"])


if __name__ == "__main__":
    unittest.main()
