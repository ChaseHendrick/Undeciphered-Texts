"""Boneh / Hastad low-exponent RSA broadcast known-answer recovery.

Attack survey:
https://crypto.stanford.edu/~dabo/papers/RSA-survey.pdf

Dan Boneh, Twenty Years of Attacks on the RSA Cryptosystem,
Notices of the AMS 46(2), 1999 (low public exponent / Hastad).

The worked instance is synthetic. The moduli, e=3, ciphertexts, and
plaintext are printed in engine/data/rsa_broadcast_certificate.json.

This is a known-answer textbook-weak test. It does not attack a real
key, a live server, TLS, or a padding oracle. It does not claim an
unknown-script reading and it is not a claim about Kryptos K4, Zodiac,
Beale, McCormick, Voynich, or army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers import SOLVERS
from engine.solvers.rsa_broadcast import (
    ATTACK_NAME,
    BONEH_URL,
    SYNTHETIC_CIPHERTEXT,
    SYNTHETIC_E,
    SYNTHETIC_N,
    SYNTHETIC_PLAINTEXT,
    SYNTHETIC_PLAINTEXT_INTEGER,
    chinese_remainder,
    integer_nth_root,
    integer_to_plaintext,
    plaintext_to_integer,
    recover_broadcast_plaintext,
    rsa_encrypt_integer,
    solve_rsa_broadcast,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "rsa_broadcast_certificate.json"
)


class RsaBroadcastScopeTest(unittest.TestCase):
    def test_module_documents_known_answer_not_real_key_or_k4(self) -> None:
        import engine.solvers.rsa_broadcast as mod

        doc = (mod.__doc__ or "").lower()
        self.assertIn("known-answer", doc)
        self.assertIn("synthetic", doc)
        self.assertIn("not attack a", doc)
        self.assertIn("real key", doc)
        self.assertIn("tls", doc)
        self.assertIn("padding oracle", doc)
        self.assertIn("kryptos k4", doc)
        self.assertIn("voynich", doc)
        self.assertIn("zodiac", doc)
        self.assertIn("beale", doc)
        self.assertIn("mccormick", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("crypto.stanford.edu/~dabo/papers/RSA-survey.pdf", BONEH_URL)
        self.assertNotIn("rsa_broadcast", SOLVERS)
        self.assertNotIn("\u2014", mod.__doc__ or "")
        self.assertNotIn("\u2013", mod.__doc__ or "")


class RsaBroadcastSyntheticExampleTest(unittest.TestCase):
    """Synthetic e=3 broadcast: CRT plus cube root recovers ATTACK AT DAWN."""

    def test_plaintext_integer_encoding_matches_certificate_value(self) -> None:
        self.assertEqual(
            plaintext_to_integer(SYNTHETIC_PLAINTEXT), SYNTHETIC_PLAINTEXT_INTEGER
        )
        self.assertEqual(
            integer_to_plaintext(SYNTHETIC_PLAINTEXT_INTEGER), SYNTHETIC_PLAINTEXT
        )

    def test_encrypt_matches_printed_ciphertexts(self) -> None:
        for cipher, modulus in zip(SYNTHETIC_CIPHERTEXT, SYNTHETIC_N):
            self.assertEqual(
                rsa_encrypt_integer(
                    SYNTHETIC_PLAINTEXT_INTEGER, SYNTHETIC_E, modulus
                ),
                cipher,
            )

    def test_crt_and_cube_root_recover_plaintext_integer(self) -> None:
        combined = chinese_remainder(list(SYNTHETIC_CIPHERTEXT), list(SYNTHETIC_N))
        self.assertEqual(combined, SYNTHETIC_PLAINTEXT_INTEGER**SYNTHETIC_E)
        root = integer_nth_root(combined, SYNTHETIC_E)
        self.assertEqual(root**SYNTHETIC_E, combined)
        self.assertEqual(root, SYNTHETIC_PLAINTEXT_INTEGER)

    def test_recover_broadcast_plaintext_exact(self) -> None:
        message = recover_broadcast_plaintext(
            SYNTHETIC_CIPHERTEXT, SYNTHETIC_N, exponent=SYNTHETIC_E
        )
        self.assertEqual(message, SYNTHETIC_PLAINTEXT_INTEGER)
        self.assertEqual(integer_to_plaintext(message), SYNTHETIC_PLAINTEXT)

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_rsa_broadcast()
        self.assertEqual(result.plaintext, SYNTHETIC_PLAINTEXT)
        self.assertEqual(result.method, "rsa_broadcast")
        self.assertEqual(result.details["attack"], ATTACK_NAME)
        self.assertEqual(result.details["e"], 3)
        self.assertEqual(result.details["source_url"], BONEH_URL)
        self.assertEqual(result.details["instance"], "synthetic")
        scope = result.details["scope"].lower()
        self.assertIn("known-answer", scope)
        self.assertIn("synthetic", scope)
        self.assertIn("real key", scope)
        self.assertIn("tls", scope)
        self.assertIn("padding oracle", scope)
        self.assertIn("kryptos k4", scope)
        self.assertIn("voynich", scope)
        self.assertIn("zodiac", scope)
        self.assertIn("beale", scope)
        self.assertIn("mccormick", scope)
        self.assertIn("nr. 86", scope)

    def test_solver_accepts_explicit_certificate_numbers(self) -> None:
        result = solve_rsa_broadcast(
            list(SYNTHETIC_CIPHERTEXT),
            moduli=list(SYNTHETIC_N),
            exponent=SYNTHETIC_E,
        )
        self.assertEqual(result.plaintext, SYNTHETIC_PLAINTEXT)


class RsaBroadcastCertificateTest(unittest.TestCase):
    """Certificate checks the synthetic textbook-weak instance only."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_recovers_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "rsa_broadcast")
        self.assertEqual(self.cert["name"], "rsa_broadcast")
        self.assertEqual(self.cert["attack"], ATTACK_NAME)
        plaintext = self.cert["plaintext"]
        ciphertexts = [int(c) for c in self.cert["ciphertext"]]
        moduli = [int(n) for n in self.cert["n"]]
        exponent = int(self.cert["e"])
        self.assertEqual(plaintext, SYNTHETIC_PLAINTEXT)
        self.assertEqual(ciphertexts, list(SYNTHETIC_CIPHERTEXT))
        self.assertEqual(moduli, list(SYNTHETIC_N))
        self.assertEqual(exponent, SYNTHETIC_E)
        self.assertEqual(self.cert["instance"], "synthetic")
        self.assertEqual(self.cert["keys"]["e"], exponent)
        self.assertEqual(self.cert["keys"]["n"], self.cert["n"])
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        message = recover_broadcast_plaintext(
            ciphertexts, moduli, exponent=exponent
        )
        self.assertEqual(str(message), self.cert["plaintext_integer"])
        self.assertEqual(integer_to_plaintext(message), plaintext)
        result = solve_rsa_broadcast(
            ciphertexts, moduli=moduli, exponent=exponent
        )
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], BONEH_URL)
        note = self.cert["note"].lower()
        self.assertIn("synthetic", note)
        self.assertIn("known-answer", note)
        self.assertIn("real key", note)
        self.assertIn("tls", note)
        self.assertIn("padding oracle", note)
        self.assertIn("nr. 86", note)
        self.assertIn("kryptos k4", note)
        self.assertIn("voynich", note)
        self.assertIn("zodiac", note)
        self.assertIn("beale", note)
        self.assertIn("mccormick", note)
        self.assertNotIn("\u2014", self.cert["note"])
        self.assertNotIn("\u2013", self.cert["note"])
        self.assertNotIn("\u2014", plaintext)
        self.assertNotIn("\u2013", plaintext)


if __name__ == "__main__":
    unittest.main()
