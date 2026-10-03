"""Bounded Fermat RSA recovery, including HAC Example 8.4.

Printed RSA vector: https://cacr.uwaterloo.ca/hac/about/chap8.pdf
Fermat method: https://eprint.iacr.org/2023/026.pdf
Only the public modulus, public exponent, and ciphertext enter recovery.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.rsa_fermat import (
    FERMAT_URL,
    HAC_URL,
    factor_fermat,
    solve_rsa_fermat,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1] / "engine" / "data" / "rsa_fermat_certificate.json"
)


class RsaFermatPublishedExampleTest(unittest.TestCase):
    def test_recovers_published_factors_in_exactly_two_square_checks(self) -> None:
        result = factor_fermat(6012707, max_steps=2)
        self.assertTrue(result.found)
        self.assertFalse(result.exhausted)
        self.assertEqual((result.p, result.q), (2357, 2551))
        self.assertEqual(result.checks, 2)
        self.assertEqual(result.start_a, 2453)
        self.assertEqual(result.last_a, 2454)
        self.assertEqual(result.prime_validation, "deterministic_below_2_64")

    def test_recovers_published_plaintext_from_only_public_parameters(self) -> None:
        result = solve_rsa_fermat(
            3650502, modulus=6012707, exponent=3674911, max_steps=2
        )
        self.assertEqual(result.method, "rsa-fermat")
        self.assertEqual(result.plaintext, "4fdff1")
        self.assertEqual(result.details["plaintext_integer"], 5234673)
        self.assertEqual(result.details["private_exponent"], 422191)
        self.assertEqual(result.details["factors"], [2357, 2551])
        self.assertEqual(result.details["status"], "recovered")
        self.assertEqual(result.details["mode"], "bounded_public_parameter_attack")
        self.assertEqual(result.details["encoding"], "hex")
        self.assertEqual(result.details["plaintext_bytes"], 3)
        self.assertEqual(result.details["checks"], 2)
        self.assertEqual(result.details["source_url"], HAC_URL)
        self.assertEqual(result.details["attack_source_url"], FERMAT_URL)
        self.assertEqual(
            result.details["plaintext_sha256"],
            hashlib.sha256(bytes.fromhex("4fdff1")).hexdigest(),
        )

    def test_one_check_is_exhausted_without_plaintext_or_factors(self) -> None:
        factors = factor_fermat(6012707, max_steps=1)
        self.assertFalse(factors.found)
        self.assertTrue(factors.exhausted)
        self.assertEqual(factors.checks, 1)
        self.assertEqual(factors.last_a, 2453)
        self.assertIsNone(factors.p)
        self.assertIsNone(factors.q)
        result = solve_rsa_fermat(
            3650502, modulus=6012707, exponent=3674911, max_steps=1
        )
        self.assertEqual(result.plaintext, "")
        self.assertEqual(result.details["status"], "exhausted")
        self.assertEqual(result.details["checks"], 1)
        self.assertIsNone(result.details["claimed_plaintext"])
        self.assertNotIn("plaintext_integer", result.details)

    def test_zero_budget_makes_no_square_checks(self) -> None:
        factors = factor_fermat(6012707, max_steps=0)
        self.assertTrue(factors.exhausted)
        self.assertEqual(factors.checks, 0)
        self.assertIsNone(factors.last_a)


class RsaFermatGeneralRecoveryTest(unittest.TestCase):
    def test_larger_close_primes_recover_without_passing_either_factor(self) -> None:
        # These constructed fixtures are distinct from the published certificate.
        for p, q, message in (
            (1000000007, 1000000009, 123456789012345),
            (32416187567, 32416190071, 987654321012345678),
            (
                1208925819614629174706189,
                1208925819614629174706261,
                123456789012345678901234567890,
            ),
        ):
            with self.subTest(p=p, q=q):
                n = p * q
                ciphertext = pow(message, 65537, n)
                result = solve_rsa_fermat(
                    ciphertext, modulus=n, exponent=65537, max_steps=10
                )
                self.assertEqual(result.details["plaintext_integer"], message)
                self.assertEqual(result.details["factors"], [p, q])
                self.assertEqual(result.details["status"], "recovered")
                self.assertEqual(result.details["checks"], 1)
                self.assertEqual(
                    result.details["prime_validation"],
                    "deterministic_below_2_64"
                    if q < 2**64
                    else "fixed_base_probable_prime_screen",
                )

    def test_general_public_exponent_and_non_coprime_messages(self) -> None:
        # RSA also decrypts residues divisible by a prime factor.
        n, e = 101 * 113, 3
        for message in (0, 1, 101, 113, n - 1):
            with self.subTest(message=message):
                result = solve_rsa_fermat(
                    pow(message, e, n), modulus=n, exponent=e, max_steps=2
                )
                self.assertEqual(result.details["plaintext_integer"], message)
                recovered = bytes.fromhex(result.plaintext)
                self.assertEqual(int.from_bytes(recovered, "big"), message)
                self.assertGreaterEqual(len(recovered), 1)

    def test_explicit_byte_length_preserves_requested_leading_zeros(self) -> None:
        result = solve_rsa_fermat(
            3650502,
            modulus=6012707,
            exponent=3674911,
            max_steps=2,
            plaintext_length=5,
        )
        self.assertEqual(result.plaintext, "00004fdff1")
        self.assertEqual(result.details["plaintext_bytes"], 5)
        self.assertEqual(
            result.details["plaintext_sha256"],
            hashlib.sha256(bytes.fromhex("00004fdff1")).hexdigest(),
        )

    def test_wide_prime_gap_reports_exhaustion_at_the_exact_bound(self) -> None:
        n = 101 * 1000000007
        factors = factor_fermat(n, max_steps=7)
        self.assertTrue(factors.exhausted)
        self.assertEqual(factors.checks, 7)
        self.assertEqual(factors.last_a, factors.start_a + 6)


class RsaFermatInvalidInputTest(unittest.TestCase):
    def test_rejects_prime_square_even_and_non_semiprime_moduli(self) -> None:
        for modulus in (0, 1, -15, 2, 14, 101, 101 * 101, 3 * 5 * 7):
            with self.subTest(modulus=modulus):
                with self.assertRaises(ValueError):
                    factor_fermat(modulus, max_steps=100)

    def test_rejects_invalid_exponents_ciphertexts_and_budget(self) -> None:
        for exponent in (0, 1, -3, 6012707):
            with self.subTest(exponent=exponent):
                with self.assertRaises(ValueError):
                    solve_rsa_fermat(3650502, modulus=6012707, exponent=exponent)
        # The public exponent is not invertible modulo (p-1)(q-1).
        with self.assertRaises(ValueError):
            solve_rsa_fermat(5, modulus=101 * 113, exponent=7, max_steps=2)
        for ciphertext in (-1, 6012707):
            with self.subTest(ciphertext=ciphertext):
                with self.assertRaises(ValueError):
                    solve_rsa_fermat(ciphertext, modulus=6012707, exponent=3674911)
        with self.assertRaises(ValueError):
            factor_fermat(6012707, max_steps=-1)

    def test_rejects_non_integer_and_boolean_parameters(self) -> None:
        for value in (True, 6012707.0, "6012707", None):
            with self.subTest(value=value):
                with self.assertRaises(TypeError):
                    factor_fermat(value)
                with self.assertRaises(TypeError):
                    factor_fermat(6012707, max_steps=value)
                with self.assertRaises(TypeError):
                    solve_rsa_fermat(value, modulus=6012707, exponent=3674911)
                with self.assertRaises(TypeError):
                    solve_rsa_fermat(3650502, modulus=6012707, exponent=value)

    def test_rejects_invalid_plaintext_length(self) -> None:
        for length in (0, -1, 2):
            with self.subTest(length=length):
                with self.assertRaises(ValueError):
                    solve_rsa_fermat(
                        3650502,
                        modulus=6012707,
                        exponent=3674911,
                        max_steps=2,
                        plaintext_length=length,
                    )
        with self.assertRaises(TypeError):
            solve_rsa_fermat(
                3650502, modulus=6012707, exponent=3674911, plaintext_length=True
            )


class RsaFermatCertificateTest(unittest.TestCase):
    def test_certificate_recovers_published_plaintext_and_raw_byte_hash(self) -> None:
        cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))
        self.assertEqual(cert["cipher_name"], "rsa-fermat")
        self.assertEqual(cert["encoding"], "hex")
        self.assertEqual(cert["hash_encoding"], "raw_big_endian_bytes")
        self.assertNotIn("plaintext", cert)
        self.assertNotIn("ciphertext", cert)
        result = solve_rsa_fermat(
            cert["ciphertext_integer"],
            modulus=cert["modulus"],
            exponent=cert["exponent"],
            max_steps=cert["max_steps"],
            plaintext_length=cert["plaintext_length"],
        )
        self.assertEqual(result.details["plaintext_integer"], 5234673)
        self.assertEqual(result.details["plaintext_integer"], cert["plaintext_integer"])
        self.assertEqual(result.plaintext, cert["plaintext_hex"])
        self.assertEqual(result.details["checks"], cert["checks"])
        self.assertEqual(
            hashlib.sha256(bytes.fromhex(result.plaintext)).hexdigest(),
            cert["plaintext_sha256"],
        )
        self.assertEqual(cert["source_url"], HAC_URL)
        self.assertEqual(cert["attack_source_url"], FERMAT_URL)


if __name__ == "__main__":
    unittest.main()
