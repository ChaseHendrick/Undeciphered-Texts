"""Public-parameter common-modulus RSA recovery on a synthetic fixture.

Sources:
https://cacr.uwaterloo.ca/hac/about/chap8.pdf, section 8.2.2(vi).
https://www.acsu.buffalo.edu/~mblanton/cse664/lecture14.pdf, slide 12.
Ciphertexts below were frozen with built-in pow before adding the attacker.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers.rsa_common_modulus import (
    common_modulus_coefficients,
    recover_common_modulus_plaintext,
    solve_rsa_common_modulus,
)


_N = 340282366920938460843936948965011886881
_E1, _E2 = 17, 65537
_C1 = 124926563412530274107408452482445848228
_C2 = 214229972888188659887672188139473134959
_M = 1365204392090841280759282713515347
_PLAIN = bytes.fromhex("0000434f4d4d4f4e204d4f44554c5553")
_CERT_PATH = Path(__file__).resolve().parents[1] / "engine/data/rsa_common_modulus_certificate.json"


class RsaCommonModulusRecoveryTest(unittest.TestCase):
    def test_literal_synthetic_ciphertexts_recover_without_private_key(self) -> None:
        self.assertEqual(pow(_M, _E1, _N), _C1)
        self.assertEqual(pow(_M, _E2, _N), _C2)
        self.assertEqual(recover_common_modulus_plaintext(_C1, _C2, e1=_E1, e2=_E2, n=_N), _M)

    def test_both_negative_exponent_positions_and_swapped_input_order(self) -> None:
        a, b = common_modulus_coefficients(_E1, _E2)
        self.assertEqual(a * _E1 + b * _E2, 1)
        self.assertLess(b, 0)
        swapped_a, swapped_b = common_modulus_coefficients(_E2, _E1)
        self.assertEqual(swapped_a * _E2 + swapped_b * _E1, 1)
        self.assertLess(swapped_a, 0)
        self.assertEqual(recover_common_modulus_plaintext(_C2, _C1, e1=_E2, e2=_E1, n=_N), _M)

    def test_wrapper_preserves_supplied_byte_length_and_reports_hex(self) -> None:
        result = solve_rsa_common_modulus(_C1, _C2, e1=_E1, e2=_E2, n=_N, byte_length=16)
        self.assertEqual(result.method, "rsa_common_modulus")
        self.assertEqual(result.plaintext, _PLAIN.hex())
        self.assertEqual(result.details["plaintext_encoding"], "hex")
        self.assertEqual(result.details["mode"], "public_parameter_attack")
        self.assertEqual(result.details["plaintext_integer"], str(_M))
        self.assertEqual(result.details["bytes"], 16)
        self.assertEqual(result.details["byte_length_mode"], "supplied")
        self.assertTrue(result.details["reencryption_matches"])
        minimal = solve_rsa_common_modulus(_C1, _C2, e1=_E1, e2=_E2, n=_N)
        self.assertEqual(bytes.fromhex(minimal.plaintext), _PLAIN[2:])
        self.assertEqual(minimal.details["byte_length_mode"], "minimal")

    def test_zero_message_is_handled_without_modular_inversion(self) -> None:
        self.assertEqual(recover_common_modulus_plaintext(0, 0, e1=_E1, e2=_E2, n=_N), 0)
        result = solve_rsa_common_modulus(0, 0, e1=_E1, e2=_E2, n=_N, byte_length=3)
        self.assertEqual(result.plaintext, "000000")


class RsaCommonModulusValidationTest(unittest.TestCase):
    def test_noncoprime_exponents_are_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "coprime"):
            recover_common_modulus_plaintext(_C1, _C2, e1=3, e2=9, n=_N)

    def test_noninvertible_ciphertext_and_single_zero_are_rejected(self) -> None:
        # Constructed from a message sharing a prime factor with n.
        with self.assertRaisesRegex(ValueError, "invertible"):
            recover_common_modulus_plaintext(
                286121518389562679943364288652535331696,
                252822722844161321348659765274711383486,
                e1=_E1,
                e2=_E2,
                n=_N,
            )
        with self.assertRaisesRegex(ValueError, "inconsistent"):
            recover_common_modulus_plaintext(0, 1, e1=_E1, e2=_E2, n=_N)

    def test_different_plaintexts_are_rejected_by_reencryption(self) -> None:
        # The second ciphertext encrypts m+1, not m.
        with self.assertRaisesRegex(ValueError, "inconsistent"):
            recover_common_modulus_plaintext(
                _C1, 92285374192574804154231923742234497113, e1=_E1, e2=_E2, n=_N
            )

    def test_modulus_ciphertext_and_exponent_ranges(self) -> None:
        for n in (-1, 0, 1, 3, 4, _N + 1):
            with self.subTest(n=n):
                with self.assertRaises(ValueError):
                    recover_common_modulus_plaintext(1, 1, e1=_E1, e2=_E2, n=n)
        for c1, c2 in ((-1, _C2), (_N, _C2), (_C1, -1), (_C1, _N)):
            with self.subTest(c1=c1, c2=c2):
                with self.assertRaises(ValueError):
                    recover_common_modulus_plaintext(c1, c2, e1=_E1, e2=_E2, n=_N)
        for e1, e2 in ((0, _E2), (1, _E2), (_E1, -1)):
            with self.subTest(e1=e1, e2=e2):
                with self.assertRaises(ValueError):
                    recover_common_modulus_plaintext(_C1, _C2, e1=e1, e2=e2, n=_N)

    def test_integer_inputs_are_required_without_silent_coercion(self) -> None:
        args = {"c1": _C1, "c2": _C2, "e1": _E1, "e2": _E2, "n": _N}
        for name in args:
            for invalid in (True, 1.5, "17", None):
                with self.subTest(name=name, invalid=invalid):
                    with self.assertRaises(TypeError):
                        recover_common_modulus_plaintext(**{**args, name: invalid})

    def test_byte_length_validation(self) -> None:
        args = {"e1": _E1, "e2": _E2, "n": _N}
        for length in (0, -1, 13):
            with self.subTest(length=length):
                with self.assertRaises(ValueError):
                    solve_rsa_common_modulus(_C1, _C2, **args, byte_length=length)
        for length in (True, "16", 16.0):
            with self.subTest(length=length):
                with self.assertRaises(TypeError):
                    solve_rsa_common_modulus(_C1, _C2, **args, byte_length=length)


class RsaCommonModulusCertificateTest(unittest.TestCase):
    def test_certificate_recovers_and_hashes_raw_plaintext_bytes(self) -> None:
        cert = json.loads(_CERT_PATH.read_text(encoding="utf-8"))
        c1, c2 = cert["ciphertext_integers"]
        e1, e2 = cert["public_exponents"]
        result = solve_rsa_common_modulus(c1, c2, e1=e1, e2=e2, n=cert["modulus"], byte_length=cert["byte_length"])
        plain = bytes.fromhex(result.plaintext)
        self.assertEqual(plain, _PLAIN)
        self.assertEqual(result.plaintext, cert["plaintext_hex"])
        self.assertEqual(hashlib.sha256(plain).hexdigest(), cert["plaintext_sha256"])
        self.assertEqual(cert["instance"], "synthetic")
        self.assertEqual(cert["hash_encoding"], "raw_bytes")
        self.assertEqual(cert["cipher_name"], "rsa_common_modulus")
        self.assertEqual(cert["source_url"], "https://cacr.uwaterloo.ca/hac/about/chap8.pdf")
        self.assertNotIn("plaintext", cert)
        self.assertNotIn("ciphertext", cert)
        self.assertNotIn("private_key", cert)


if __name__ == "__main__":
    unittest.main()
