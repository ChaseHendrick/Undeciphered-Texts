"""Bob can search Caesar and Vigenere. He does not store the letters."""

from __future__ import annotations

import hashlib
import json
import unittest

from engine.alphabet import letters_only
from engine.bob_read import bob_read_report, try_read
from engine.ciphers import caesar_encrypt
from engine.neural_grade import letters_az, load_training_prose
from engine.solvers.dagapeyeff import consider_bob_read


class BobReadTest(unittest.TestCase):
    def test_a_training_caesar_returns_the_shift_and_not_the_letters(self) -> None:
        original = letters_az(load_training_prose())[:160]
        reading = try_read(caesar_encrypt(original, 3))
        self.assertEqual(reading["family"], "caesar")
        self.assertEqual(reading["key"], "3")
        self.assertTrue(reading["consistent"])
        self.assertFalse(reading["withheld"])
        self.assertIs(reading["solved"], False)
        self.assertIsNone(reading["claimed_plaintext"])
        self.assertEqual(reading["sha256"], hashlib.sha256(letters_only(original).encode("ascii")).hexdigest())
        self.assertNotIn(original[:24], json.dumps(reading))
        short = try_read("abc")
        self.assertTrue(short["withheld"])
        self.assertIs(short["solved"], False)

    def test_the_drill_is_not_a_reading(self) -> None:
        report = bob_read_report()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        self.assertFalse(report["weights_replaced"])
        self.assertFalse(report["promoted"])
        self.assertEqual(report["caesar_texts"], 8)
        self.assertEqual(report["caesar_routed"], 8)
        self.assertEqual(report["caesar_matched"], 8)
        self.assertEqual(report["vigenere_texts"], 6)
        self.assertEqual(report["vigenere_routed"], 6)
        self.assertEqual(report["vigenere_matched"], 6)
        self.assertEqual(report["substitution_withheld"], 4)
        self.assertEqual(report["substitution_false_match"], 0)
        self.assertEqual(report["beaufort_withheld"], 4)
        self.assertEqual(report["beaufort_false_match"], 0)
        self.assertTrue(report["short_withheld"])
        self.assertTrue(report["digit_withheld"])
        self.assertEqual(report["proverb_family"], "keyed-vigenere")
        self.assertTrue(report["proverb_withheld"])
        self.assertFalse(report["proverb_matched"])
        claim = consider_bob_read()
        self.assertFalse(claim["bob_read_allowed"])
        self.assertIs(claim["solved"], False)
        self.assertIsNone(claim["claimed_plaintext"])
        self.assertIn("Not a reading", claim["learned"])


if __name__ == "__main__":
    unittest.main()
