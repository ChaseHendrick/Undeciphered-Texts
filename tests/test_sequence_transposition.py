"""Literal ACA sequence, column diagram, framed check digit and inverse oracle."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import unittest

from engine.solvers.sequence_transposition import (
    sequence_digits, sequence_key_ranks, sequence_transposition_decrypt,
    sequence_transposition_encrypt, solve_sequence_transposition,
)

PLAIN = "THEEARLYBIRDGETSTHEWORM"
CIPHER = "YHOMARTBDETHIGWLRESEERT"
FRAME = "69315 YHOMA RTBDE THIGW LRESE ERT 9."


class SequenceTranspositionTest(unittest.TestCase):
    def test_literal_published_sequence_and_rank_diagram(self):
        self.assertEqual(sequence_digits("69315", 23), "69315524607606736630929")
        self.assertEqual(sequence_key_ranks("GUMMYBEARS"), (4, 9, 5, 6, 0, 2, 3, 1, 7, 8))
        self.assertEqual(sequence_transposition_encrypt(PLAIN, "GUMMYBEARS", "69315"), CIPHER)
        self.assertEqual(sequence_transposition_decrypt(CIPHER, "GUMMYBEARS", "69315"), PLAIN)
        self.assertEqual(sequence_transposition_decrypt(FRAME, "GUMMYBEARS"), PLAIN)
        self.assertEqual(sequence_transposition_encrypt(PLAIN, "GUMMYBEARS", "69315", framed=True), FRAME[:-1])
        self.assertEqual(solve_sequence_transposition(FRAME, keyword="GUMMYBEARS").plaintext, PLAIN)

    def test_check_digit_is_verified_not_ignored(self):
        for frame in (FRAME.replace("9.", "8."), FRAME.replace("69315", "69314"),
                      "69315 YHOMA RTBDE THIGW LRESE ERT", "69315 YHO1A RTBDE THIGW LRESE ERT 9"):
            with self.assertRaises(ValueError):
                sequence_transposition_decrypt(frame, "GUMMYBEARS")
        with self.assertRaises(ValueError):
            sequence_transposition_decrypt(CIPHER, "GUMMYBEARS", "69315", check_digit="8")

    def test_independent_position_sort_oracle(self):
        plain = "ABCDEFGHIJKLMNOPQRSTUVWXYZABCD"
        for primer in ("00000", "12345", "98765"):
            digits = [int(x) for x in primer]
            for i in range(len(plain) - 5):
                digits.append((digits[i] + digits[i + 1]) % 10)
            for key in ("ABCDEFGHIJ", "JJJJJJJJJJ", "GUMMYBEARS"):
                ranks = [0] * 10
                for rank, col in enumerate(sorted(range(10), key=lambda i: (key[i], i)), 1):
                    ranks[col] = rank % 10
                positions = sorted(range(len(plain)), key=lambda i: (ranks.index(digits[i]), i))
                expected = "".join(plain[i] for i in positions)
                self.assertEqual(sequence_transposition_encrypt(plain, key, primer), expected)
                self.assertEqual(sequence_transposition_decrypt(expected, key, primer), plain)

    def test_lengths_leading_zero_and_strict_parameter_validation(self):
        for size in (1, 4, 5, 6, 31):
            plain = ("ABCD" * 8)[:size]
            cipher = sequence_transposition_encrypt(plain, "ABCDEFGHIJ", "01234")
            self.assertEqual(sequence_transposition_decrypt(cipher, "ABCDEFGHIJ", "01234"), plain)
        for key in ("SHORT", "ABCDEFGHIJK", "ABCDEFＧHIJ", None):
            with self.assertRaises((ValueError, TypeError)):
                sequence_key_ranks(key)
        for primer in ("1234", "123456", "１２３４５", "12a45", 12345, True):
            with self.assertRaises((ValueError, TypeError)):
                sequence_digits(primer, 10)
        for length in (0, -1, True, 4097):
            with self.assertRaises((ValueError, TypeError)):
                sequence_digits("01234", length)
        with self.assertRaises(ValueError):
            sequence_transposition_decrypt("123 ABC", "ABCDEFGHIJ", "12345")

    def test_certificate_hashes_recovered_literal_output(self):
        cert = json.loads((Path(__file__).parents[1] / "engine/data/sequence_transposition_certificate.json").read_text())
        recovered = sequence_transposition_decrypt(cert["ciphertext"], cert["keys"]["keyword"], cert["keys"]["primer"])
        self.assertEqual(cert["ciphertext"], CIPHER)
        self.assertEqual(recovered, PLAIN)
        self.assertEqual(hashlib.sha256(recovered.encode("ascii")).hexdigest(), cert["plaintext_sha256"])


if __name__ == "__main__":
    unittest.main()
