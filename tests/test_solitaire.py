"""Solitaire (Pontifex) known-deck recovery against published samples.

Source (fetched 2026-10-03):
https://www.schneier.com/academic/solitaire/

This is a known classical-cipher solver test. It does not claim Kryptos
K4, the Zodiac ciphers, the Beale ciphers, the McCormick cipher, the
Voynich manuscript, or army message Nr. 86.
"""

from __future__ import annotations

import hashlib
import json
import unittest
from pathlib import Path

from engine.solvers import SOLVERS
from engine.solvers import solitaire as solitaire_mod
from engine.solvers.solitaire import (
    SCHNEIER_SOLITAIRE_CIPHER,
    SCHNEIER_SOLITAIRE_FOO_CIPHER,
    SCHNEIER_SOLITAIRE_FOO_KEY,
    SCHNEIER_SOLITAIRE_FOO_PLAIN,
    SCHNEIER_SOLITAIRE_FOO_RAW,
    SCHNEIER_SOLITAIRE_KEY,
    SCHNEIER_SOLITAIRE_MESSAGE,
    SCHNEIER_SOLITAIRE_PLAIN,
    SCHNEIER_SOLITAIRE_UNKEYED_CIPHER,
    SCHNEIER_SOLITAIRE_UNKEYED_PLAIN,
    SCHNEIER_SOLITAIRE_UNKEYED_RAW,
    SCHNEIER_SOLITAIRE_URL,
    keystream_numbers,
    normalize_deck,
    normalize_passphrase,
    raw_output_cards,
    solitaire_decrypt,
    solitaire_encrypt,
    solve_solitaire,
    unkeyed_deck,
)


CERT_PATH = (
    Path(__file__).resolve().parents[1] / "engine" / "data" / "solitaire_certificate.json"
)


class SolitaireScopeTest(unittest.TestCase):
    def test_module_documents_known_cipher_not_unsolved_claims(self) -> None:
        source = Path(solitaire_mod.__file__).read_text(encoding="utf-8")
        doc = (solitaire_mod.__doc__ or "").lower()
        self.assertIn("known classical-cipher", doc)
        self.assertIn("known-cipher", doc)
        self.assertIn("not", doc)
        self.assertIn("unknown-script", doc)
        self.assertIn("kryptos k4", doc)
        self.assertIn("zodiac", doc)
        self.assertIn("beale", doc)
        self.assertIn("mccormick", doc)
        self.assertIn("voynich", doc)
        self.assertIn("nr. 86", doc)
        self.assertIn("solitaire/", SCHNEIER_SOLITAIRE_URL.lower())
        self.assertNotIn("solitaire", SOLVERS)
        self.assertNotIn("\u2014", source)
        self.assertNotIn("\u2013", source)
        self.assertNotIn("\u2014", doc)
        self.assertNotIn("\u2013", doc)


class SolitairePublishedExampleTest(unittest.TestCase):
    """Schneier samples: unkeyed deck, FOO, and CRYPTONOMICON."""

    def test_unkeyed_encrypt_matches_published_ciphertext(self) -> None:
        cipher = solitaire_encrypt(SCHNEIER_SOLITAIRE_UNKEYED_PLAIN)
        self.assertEqual(cipher, SCHNEIER_SOLITAIRE_UNKEYED_CIPHER)
        self.assertEqual(cipher, "EXKYI ZSGEH")
        self.assertEqual(solitaire_encrypt("AAAAA AAAAA"), "EXKYI ZSGEH")
        self.assertEqual(
            solitaire_encrypt("AAAAAAAAAA", deck=unkeyed_deck()),
            "EXKYI ZSGEH",
        )

    def test_unkeyed_raw_cards_include_the_skipped_joker(self) -> None:
        raw = tuple(raw_output_cards(len(SCHNEIER_SOLITAIRE_UNKEYED_RAW)))
        self.assertEqual(raw, SCHNEIER_SOLITAIRE_UNKEYED_RAW)
        self.assertEqual(
            keystream_numbers(10),
            [4, 23, 10, 24, 8, 25, 18, 6, 4, 7],
        )

    def test_unkeyed_decrypt_recovers_published_letters(self) -> None:
        self.assertEqual(
            solitaire_decrypt(SCHNEIER_SOLITAIRE_UNKEYED_CIPHER),
            SCHNEIER_SOLITAIRE_UNKEYED_PLAIN,
        )
        self.assertEqual(solitaire_decrypt("EXKYI ZSGEH"), "AAAAAAAAAA")

    def test_foo_passphrase_matches_published_ciphertext(self) -> None:
        self.assertEqual(normalize_passphrase("FOO"), "FOO")
        self.assertEqual(normalize_passphrase("foo"), "FOO")
        cipher = solitaire_encrypt(
            SCHNEIER_SOLITAIRE_FOO_PLAIN, SCHNEIER_SOLITAIRE_FOO_KEY
        )
        self.assertEqual(cipher, SCHNEIER_SOLITAIRE_FOO_CIPHER)
        self.assertEqual(cipher, "ITHZU JIWGR FARMW")
        self.assertEqual(
            tuple(raw_output_cards(len(SCHNEIER_SOLITAIRE_FOO_RAW), "FOO")),
            SCHNEIER_SOLITAIRE_FOO_RAW,
        )
        self.assertEqual(
            solitaire_decrypt(SCHNEIER_SOLITAIRE_FOO_CIPHER, "FOO"),
            SCHNEIER_SOLITAIRE_FOO_PLAIN,
        )

    def test_cryptonomicon_encrypts_solitaire_to_published_ciphertext(self) -> None:
        cipher = solitaire_encrypt(
            SCHNEIER_SOLITAIRE_MESSAGE, SCHNEIER_SOLITAIRE_KEY
        )
        self.assertEqual(cipher, SCHNEIER_SOLITAIRE_CIPHER)
        self.assertEqual(cipher, "KIRAK SFJAN")
        self.assertEqual(
            solitaire_encrypt("SOLITAIREX", "CRYPTONOMICON"),
            "KIRAK SFJAN",
        )
        self.assertEqual(
            solitaire_decrypt(SCHNEIER_SOLITAIRE_CIPHER, SCHNEIER_SOLITAIRE_KEY),
            SCHNEIER_SOLITAIRE_PLAIN,
        )
        self.assertEqual(SCHNEIER_SOLITAIRE_PLAIN, "SOLITAIREX")
        self.assertEqual(SCHNEIER_SOLITAIRE_MESSAGE, "SOLITAIRE")

    def test_solver_recovers_published_plaintext_exactly(self) -> None:
        result = solve_solitaire(
            SCHNEIER_SOLITAIRE_CIPHER, key=SCHNEIER_SOLITAIRE_KEY
        )
        self.assertEqual(result.plaintext, SCHNEIER_SOLITAIRE_PLAIN)
        self.assertEqual(result.method, "solitaire")
        self.assertEqual(result.key, "CRYPTONOMICON")
        self.assertEqual(result.details["source_url"], SCHNEIER_SOLITAIRE_URL)
        self.assertEqual(result.details["passphrase"], "CRYPTONOMICON")
        self.assertEqual(result.details["deck_keying"], "passphrase")
        self.assertEqual(result.details["variant"], "schneier_1_2")
        scope = result.details["scope"].lower()
        self.assertIn("known classical", scope)
        self.assertIn("not an unknown-script", scope)
        self.assertIn("kryptos k4", scope)
        self.assertIn("zodiac", scope)
        self.assertIn("beale", scope)
        self.assertIn("mccormick", scope)
        self.assertIn("voynich", scope)
        self.assertIn("nr. 86", scope)
        self.assertNotIn("\u2014", scope)
        self.assertNotIn("\u2013", scope)
        unkeyed = solve_solitaire(SCHNEIER_SOLITAIRE_UNKEYED_CIPHER, key="")
        self.assertEqual(unkeyed.plaintext, "AAAAAAAAAA")
        self.assertEqual(unkeyed.key, "unkeyed")
        self.assertEqual(unkeyed.details["deck_keying"], "unkeyed")

    def test_page_joker_moves_and_triple_cut(self) -> None:
        deck = [53, 7, 2, 54, 9, 4, 1]
        solitaire_mod._move_down(deck, 53, 1)
        solitaire_mod._move_down(deck, 54, 2)
        self.assertEqual(deck, [7, 53, 2, 9, 4, 54, 1])

        deck = [3, 53, 54, 8, 9, 6]
        solitaire_mod._move_down(deck, 53, 1)
        solitaire_mod._move_down(deck, 54, 2)
        self.assertEqual(deck, [3, 53, 8, 54, 9, 6])

        deck = [2, 4, 6, 54, 5, 8, 7, 1, 53, 3, 9]
        solitaire_mod._triple_cut(deck)
        self.assertEqual(deck, [3, 9, 54, 5, 8, 7, 1, 53, 2, 4, 6])

        deck = [54, 5, 8, 7, 1, 53, 3, 9]
        solitaire_mod._triple_cut(deck)
        self.assertEqual(deck, [3, 9, 54, 5, 8, 7, 1, 53])

        deck = [54, 5, 8, 7, 1, 53]
        solitaire_mod._triple_cut(deck)
        self.assertEqual(deck, [54, 5, 8, 7, 1, 53])

    def test_roundtrip_on_another_passphrase(self) -> None:
        plain = "DO NOT USE PC"
        cipher = solitaire_encrypt(plain, "SECRET KEY")
        self.assertEqual(solitaire_decrypt(cipher, "SECRETKEY"), "DONOTUSEPC")
        self.assertEqual(normalize_passphrase("SECRET KEY"), "SECRETKEY")

    def test_explicit_deck_roundtrip_and_rejects_bad_input(self) -> None:
        deck = unkeyed_deck()
        deck[0], deck[10] = deck[10], deck[0]
        cipher = solitaire_encrypt("HELLO", deck=deck)
        self.assertEqual(solitaire_decrypt(cipher, deck=deck), "HELLO")
        result = solve_solitaire(cipher, deck=deck)
        self.assertEqual(result.plaintext, "HELLO")
        self.assertEqual(result.details["deck_keying"], "explicit_deck")
        with self.assertRaises(ValueError):
            solitaire_encrypt("")
        with self.assertRaises(ValueError):
            solitaire_decrypt("...")
        with self.assertRaises(ValueError):
            normalize_passphrase("...")
        with self.assertRaises(ValueError):
            solitaire_encrypt("HELLO", "FOO", deck=unkeyed_deck())
        with self.assertRaises(ValueError):
            normalize_deck([1, 2, 3])
        with self.assertRaises(ValueError):
            solve_solitaire("", key="FOO")


class SolitaireCertificateTest(unittest.TestCase):
    """Certificate checks the published Schneier example, not an unsolved text."""

    def setUp(self) -> None:
        self.cert = json.loads(CERT_PATH.read_text(encoding="utf-8"))

    def test_certificate_decrypts_and_matches_plaintext_hash(self) -> None:
        self.assertEqual(self.cert["cipher_name"], "solitaire")
        plaintext = self.cert["plaintext"]
        ciphertext = self.cert["ciphertext"]
        key = self.cert["key"]
        self.assertEqual(self.cert["keys"]["passphrase"], "CRYPTONOMICON")
        self.assertEqual(self.cert["keys"]["message"], "SOLITAIRE")
        self.assertEqual(self.cert["keys"]["filler"], "X")
        self.assertEqual(key, "CRYPTONOMICON")
        self.assertEqual(plaintext, "SOLITAIREX")
        self.assertEqual(ciphertext, "KIRAK SFJAN")
        digest = hashlib.sha256(plaintext.encode("utf-8")).hexdigest()
        self.assertEqual(digest, self.cert["plaintext_sha256"])
        self.assertEqual(solitaire_decrypt(ciphertext, key), plaintext)
        self.assertEqual(solitaire_encrypt(plaintext, key), ciphertext)
        self.assertEqual(solitaire_encrypt("SOLITAIRE", key), ciphertext)
        result = solve_solitaire(ciphertext, key=key)
        self.assertEqual(result.plaintext, plaintext)
        self.assertEqual(self.cert["source_url"], SCHNEIER_SOLITAIRE_URL)
        note = self.cert["note"].lower()
        self.assertIn("not an unknown-script", note)
        self.assertIn("nr. 86", note)
        self.assertIn("kryptos k4", note)
        self.assertIn("zodiac", note)
        self.assertIn("beale", note)
        self.assertIn("mccormick", note)
        self.assertIn("voynich", note)
        self.assertIn("linear a", note)
        self.assertIn("indus", note)
        self.assertIn("rongorongo", note)
        self.assertIn("exkyi zsgeh", note)
        self.assertIn("cryptonomicon", note)
        raw = CERT_PATH.read_text(encoding="utf-8")
        self.assertNotIn("\u2014", raw)
        self.assertNotIn("\u2013", raw)
        self.assertNotIn("\u2014", note)
        self.assertNotIn("\u2013", note)


if __name__ == "__main__":
    unittest.main()
