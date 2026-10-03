"""Ragbaby known-key recovery against a published worked example.

Source (fetched 2026-10-02):
https://www.cryptogram.org/downloads/aca.info/ciphers/Ragbaby.pdf

This is a known classical-cipher solver test. It does not claim an
unknown-script reading and it is not a claim about army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers import SOLVERS
from engine.solvers.ragbaby import (
    ACA_RAGBABY_ALPHABET,
    ACA_RAGBABY_CIPHER,
    ACA_RAGBABY_KEYWORD,
    ACA_RAGBABY_PLAIN,
    ACA_RAGBABY_URL,
    keyed_alphabet,
    ragbaby_decrypt,
    ragbaby_encrypt,
    solve_ragbaby,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1]
    / "engine"
    / "data"
    / "ragbaby_certificate.json"
)


class RagbabyScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unknown_script_or_nr86(self) -> None:
        import engine.solvers.ragbaby as ragbaby_mod

        doc = (ragbaby_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("known-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("ragbaby.pdf", ACA_RAGBABY_URL.lower())
        self.assertNotIn("ragbaby", SOLVERS)


class RagbabyPublishedExampleTest(unittest.TestCase):
    """ACA sheet: GROSBEAK, Word divisions are kept."""

    def test_keyed_alphabet_matches_the_published_block(self) -> None:
        self.assertEqual(keyed_alphabet("GROSBEAK"), ACA_RAGBABY_ALPHABET)
        self.assertEqual(ACA_RAGBABY_ALPHABET, "GROSBEAKCDFHILMNPQTUVWYZ")
        self.assertEqual(len(ACA_RAGBABY_ALPHABET), 24)
        self.assertNotIn("J", ACA_RAGBABY_ALPHABET)
        self.assertNotIn("X", ACA_RAGBABY_ALPHABET)

    def test_encrypt_matches_published_ciphertext(self) -> None:
        cipher = ragbaby_encrypt("Word divisions are kept.", ACA_RAGBABY_KEYWORD)
        self.assertEqual(cipher, ACA_RAGBABY_CIPHER)
        self.assertEqual(cipher, "YBBL HNGQDUFGL DEF HFYR.")

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_ragbaby(ACA_RAGBABY_CIPHER, key=ACA_RAGBABY_KEYWORD)
        self.assertEqual(result.plaintext, ACA_RAGBABY_PLAIN)
        self.assertEqual(result.plaintext, "WORD DIVISIONS ARE KEPT.")
        self.assertEqual(result.method, "ragbaby")
        self.assertEqual(result.key, ACA_RAGBABY_KEYWORD)
        self.assertEqual(result.details["source_url"], ACA_RAGBABY_URL)
        self.assertEqual(result.details["keyed_alphabet"], ACA_RAGBABY_ALPHABET)
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("nr. 86", scope)

    def test_roundtrip_accepts_a_lowercase_keyword(self) -> None:
        again = ragbaby_decrypt(
            ragbaby_encrypt(ACA_RAGBABY_PLAIN, "grosbeak"),
            ACA_RAGBABY_KEYWORD,
        )
        self.assertEqual(again, ACA_RAGBABY_PLAIN)

    def test_j_and_x_are_paired_before_the_shift(self) -> None:
        # J is I and X is W. Shifts 1, 2, 3 in GROSBEAKCDFHILMNPQTUVWYZ.
        self.assertEqual(ragbaby_encrypt("JAX", "GROSBEAK"), "LCG")

    def test_apostrophe_and_hyphen_do_not_split_a_word(self) -> None:
        # One word: shifts 1, 2, 3. A split would number S as a new word.
        self.assertEqual(ragbaby_encrypt("IT'S", "GROSBEAK"), "LV'A")
        one_word = ragbaby_encrypt("TWO-SQUARE", "GROSBEAK")
        two_words = ragbaby_encrypt("TWO SQUARE", "GROSBEAK")
        self.assertNotEqual(one_word.replace("-", ""), two_words.replace(" ", ""))

    def test_the_count_repeats_after_24(self) -> None:
        # 24 places is a full cycle, so the 24th A stays A. The 25th uses 1 again.
        cipher = ragbaby_encrypt("A" * 25, "GROSBEAK")
        self.assertEqual(len(cipher), 25)
        self.assertEqual(cipher[23], "A")
        self.assertEqual(cipher[0], cipher[24])

    def test_empty_keyword_and_empty_text_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            ragbaby_decrypt(ACA_RAGBABY_CIPHER, "---")
        with self.assertRaises(ValueError):
            ragbaby_encrypt("...", "GROSBEAK")


class RagbabyCertificateTest(unittest.TestCase):
    """Certificate checks the published ACA example, not an unknown script."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "ragbaby")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["keyword"], "GROSBEAK")
        self.assertEqual(
            self.cert["keys"]["keyed_alphabet"],
            "GROSBEAKCDFHILMNPQTUVWYZ",
        )
        self.assertEqual(key, "GROSBEAK")
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(ragbaby_decrypt(ciphertext, key), plaintext)
        result = solve_ragbaby(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], ACA_RAGBABY_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown-script", note)
        self.assertIn("nr. 86", note)
        self.assertIn("kryptos k4", note)
        self.assertIn("voynich", note)
        self.assertIn("linear a", note)
        self.assertIn("indus", note)
        self.assertIn("rongorongo", note)


if __name__ == "__main__":
    unittest.main()
