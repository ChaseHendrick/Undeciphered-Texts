"""Recovery tests: solvers must reproduce plaintext they were not given."""

from __future__ import annotations

import random
import unittest
import hashlib
import json
from pathlib import Path

from engine.alphabet import letters_only
from engine.ciphers import (
    caesar_decrypt,
    caesar_encrypt,
    substitution_decrypt,
    substitution_encrypt,
    vigenere_decrypt,
    vigenere_encrypt,
)
from engine.fixtures import (
    CAESAR_PLAIN,
    CAESAR_SHIFT,
    DEMO_SEED,
    SUBSTITUTION_KEY,
    SUBSTITUTION_PLAIN,
    VIGENERE_KEY,
    VIGENERE_PLAIN,
)
from engine.language import get_model
from engine.solvers.caesar import solve_caesar
from engine.solvers.substitution import solve_substitution
from engine.solvers.vigenere import solve_vigenere
from engine.stats import column_mean_ic, index_of_coincidence, kasiski_factors, ngram_counts


def _same(a: str, b: str) -> bool:
    return letters_only(a) == letters_only(b)


class CipherRoundTripTest(unittest.TestCase):
    def test_caesar_roundtrip(self) -> None:
        cipher = caesar_encrypt(CAESAR_PLAIN, CAESAR_SHIFT)
        self.assertNotEqual(letters_only(cipher), letters_only(CAESAR_PLAIN))
        self.assertTrue(_same(caesar_decrypt(cipher, CAESAR_SHIFT), CAESAR_PLAIN))

    def test_vigenere_roundtrip_keeps_punctuation(self) -> None:
        cipher = vigenere_encrypt(VIGENERE_PLAIN, VIGENERE_KEY)
        plain = vigenere_decrypt(cipher, VIGENERE_KEY)
        self.assertEqual(plain, VIGENERE_PLAIN)

    def test_substitution_roundtrip(self) -> None:
        cipher = substitution_encrypt(SUBSTITUTION_PLAIN, SUBSTITUTION_KEY)
        self.assertEqual(substitution_decrypt(cipher, SUBSTITUTION_KEY), SUBSTITUTION_PLAIN)
        self.assertEqual(len(set(SUBSTITUTION_KEY)), 26)


class RecoveryTest(unittest.TestCase):
    def test_caesar_recovers_shift_and_text(self) -> None:
        cipher = caesar_encrypt(CAESAR_PLAIN, CAESAR_SHIFT)
        result = solve_caesar(cipher)
        self.assertEqual(result.details["shift"], CAESAR_SHIFT)
        self.assertTrue(_same(result.plaintext, CAESAR_PLAIN))
        self.assertIn(",", result.plaintext)

    def test_vigenere_kasiski_and_recovery(self) -> None:
        cipher = vigenere_encrypt(VIGENERE_PLAIN, VIGENERE_KEY)
        letters = letters_only(cipher)
        votes = dict(kasiski_factors(letters, max_period=12))
        self.assertIn(len(VIGENERE_KEY), votes)
        self.assertGreater(column_mean_ic(letters, len(VIGENERE_KEY)), index_of_coincidence(letters))
        result = solve_vigenere(cipher)
        self.assertEqual(result.key, VIGENERE_KEY)
        self.assertEqual(result.details["period"], len(VIGENERE_KEY))
        self.assertTrue(_same(result.plaintext, VIGENERE_PLAIN))

    def test_substitution_recovers_plaintext_and_key(self) -> None:
        cipher = substitution_encrypt(SUBSTITUTION_PLAIN, SUBSTITUTION_KEY)
        result = solve_substitution(cipher, seed=DEMO_SEED)
        self.assertTrue(_same(result.plaintext, SUBSTITUTION_PLAIN))
        self.assertEqual(result.key, SUBSTITUTION_KEY)

    def test_ngrams_and_model_prefer_english(self) -> None:
        letters = letters_only(VIGENERE_PLAIN)
        top = ngram_counts(letters, 3, limit=5)
        self.assertTrue(top)
        self.assertGreater(top[0][1], 1)
        model = get_model()
        seq = [ord(ch) - 65 for ch in letters]
        shuffled = seq[:]
        random.Random(0).shuffle(shuffled)
        self.assertGreater(model.score(seq), model.score(shuffled))
        self.assertGreater(index_of_coincidence(letters), 0.06)



CAESAR_CERT = Path(__file__).resolve().parents[1] / "engine" / "data" / "caesar_certificate.json"
VIGENERE_CERT = Path(__file__).resolve().parents[1] / "engine" / "data" / "vigenere_certificate.json"
SUBSTITUTION_CERT = Path(__file__).resolve().parents[1] / "engine" / "data" / "substitution_certificate.json"


class ClassicalFixtureCertificateTest(unittest.TestCase):
    """Certificates check fixture plaintexts recovered by solvers, not unknown scripts."""

    def _check(self, path: Path, cipher_name: str, decrypt_fn) -> None:
        cert = json.loads(path.read_text(encoding="utf-8"))
        self.assertEqual(cert["cipher_name"], cipher_name)
        plaintext = cert["plaintext"]
        ciphertext = cert["ciphertext"]
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, cert["plaintext_sha256"])
        self.assertEqual(decrypt_fn(cert), plaintext)
        self.assertIn("not an unknown script", cert["note"].lower())

    def test_caesar_certificate(self) -> None:
        def dec(cert):
            return caesar_decrypt(cert["ciphertext"], cert["keys"]["shift"])
        self._check(CAESAR_CERT, "caesar", dec)
        cert = json.loads(CAESAR_CERT.read_text(encoding="utf-8"))
        result = solve_caesar(cert["ciphertext"])
        self.assertTrue(_same(result.plaintext, cert["plaintext"]))

    def test_vigenere_certificate(self) -> None:
        def dec(cert):
            return vigenere_decrypt(cert["ciphertext"], cert["keys"]["key"])
        self._check(VIGENERE_CERT, "vigenere", dec)

    def test_substitution_certificate(self) -> None:
        def dec(cert):
            return substitution_decrypt(cert["ciphertext"], cert["keys"]["key"])
        self._check(SUBSTITUTION_CERT, "substitution", dec)


if __name__ == "__main__":
    unittest.main()
