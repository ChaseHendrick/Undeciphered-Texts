"""Public-key recovery against Wiener's original Section V example."""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.rsa_wiener import recover_wiener_key, solve_rsa_wiener


class WienerRecoveryTest(unittest.TestCase):
    def test_original_paper_lambda_example_requires_generalized_probe(self):
        result = recover_wiener_key(8927, 2621)
        self.assertEqual((result.p, result.q, result.private_exponent), (79, 113, 5))
        self.assertEqual((result.k, result.g), (3, 2))
        self.assertEqual(result.status, "recovered")
        self.assertEqual(result.steps, 3)
        self.assertTrue(result.search_complete)

    def test_synthetic_phi_inverse_example_and_nonunits(self):
        n, e = 239 * 379, 17993
        key = recover_wiener_key(n, e)
        self.assertEqual((key.p, key.q, key.private_exponent), (239, 379, 5))
        for message in (0, 1, 239, 379, 12345, n - 1):
            result = solve_rsa_wiener(pow(message, e, n), modulus=n, exponent=e)
            self.assertEqual(result.details["plaintext_integer"], message)
            self.assertEqual(int.from_bytes(bytes.fromhex(result.plaintext), "big"), message)
            self.assertTrue(result.details["reencryption_matches"])

    def test_paper_key_decrypts_a_separately_labeled_synthetic_message(self):
        result = solve_rsa_wiener(1511, modulus=8927, exponent=2621, plaintext_length=2)
        self.assertEqual(result.plaintext, "0041")
        self.assertEqual(result.details["private_exponent"], 5)
        self.assertEqual(result.details["plaintext_sha256"], hashlib.sha256(b"\x00A").hexdigest())

    def test_budget_has_exact_no_guess_semantics(self):
        for budget in (0, 1, 2):
            key = recover_wiener_key(8927, 2621, max_steps=budget)
            self.assertEqual(key.status, "incomplete")
            self.assertEqual(key.steps, budget)
            self.assertFalse(key.search_complete)
            self.assertIsNone(key.private_exponent)
            result = solve_rsa_wiener(7255, modulus=8927, exponent=2621, max_steps=budget)
            self.assertEqual(result.plaintext, "")
            self.assertIsNone(result.details["claimed_plaintext"])
        self.assertEqual(recover_wiener_key(8927, 2621, max_steps=3).status, "recovered")

    def test_complete_negative_result_only_covers_this_attack(self):
        result = recover_wiener_key(101 * 113, 3)
        self.assertEqual(result.status, "not-found")
        self.assertTrue(result.search_complete)
        self.assertIsNone(result.p)
        report = solve_rsa_wiener(42, modulus=101 * 113, exponent=3)
        self.assertEqual(report.plaintext, "")
        self.assertEqual(report.details["status"], "not-found")
        self.assertIsNone(report.details["claimed_plaintext"])

    def test_validation_rejects_invalid_types_sizes_and_parameters(self):
        for n, e in ((True, 3), (8927, True), (8927.0, 2621)):
            with self.assertRaises(TypeError):
                recover_wiener_key(n, e)
        for n, e in ((14, 3), (81, 5), (113, 3), (8927, 1), (8927, 8927), (1 << 4096 | 1, 3)):
            with self.assertRaises(ValueError):
                recover_wiener_key(n, e)
        for budget in (-1, 10001):
            with self.assertRaises(ValueError):
                recover_wiener_key(8927, 2621, max_steps=budget)
        with self.assertRaises(TypeError):
            recover_wiener_key(8927, 2621, max_steps=True)
        for c in (-1, 8927):
            with self.assertRaises(ValueError):
                solve_rsa_wiener(c, modulus=8927, exponent=2621)
        for length in (0, 4097):
            with self.assertRaises(ValueError):
                solve_rsa_wiener(7255, modulus=8927, exponent=2621, plaintext_length=length)

    def test_certificate_hashes_raw_recovered_bytes(self):
        path = Path(__file__).resolve().parents[1] / "engine/data/rsa_wiener_certificate.json"
        cert = json.loads(path.read_text())
        self.assertEqual(cert["vector_kind"], "published_key_with_synthetic_message")
        result = solve_rsa_wiener(cert["ciphertext_integer"], modulus=cert["modulus"],
                                  exponent=cert["exponent"], plaintext_length=cert["plaintext_length"])
        self.assertEqual(result.plaintext, cert["plaintext_hex"])
        self.assertEqual(hashlib.sha256(bytes.fromhex(result.plaintext)).hexdigest(), cert["plaintext_sha256"])


if __name__ == "__main__":
    unittest.main()
