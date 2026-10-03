"""Crib drag must recover a known Vigenère without being given the key."""

from __future__ import annotations

import unittest

from engine.alphabet import letters_only
from engine.ciphers import vigenere_encrypt
from engine.fixtures import VIGENERE_KEY, VIGENERE_PLAIN
from engine.solvers.crib import search_vigenere_crib


CRIB = "presses running after dark"


class VigenereCribTest(unittest.TestCase):
    def test_known_crib_recovers_key_and_plaintext(self) -> None:
        cipher = vigenere_encrypt(VIGENERE_PLAIN, VIGENERE_KEY)
        self.assertIn(letters_only(CRIB), letters_only(VIGENERE_PLAIN))
        hits = search_vigenere_crib(cipher, CRIB, max_period=12)
        self.assertTrue(hits)
        best = hits[0]
        self.assertEqual(best.key, VIGENERE_KEY)
        self.assertEqual(best.period, len(VIGENERE_KEY))
        self.assertGreater(best.checks, 0)
        self.assertEqual(letters_only(best.plaintext), letters_only(VIGENERE_PLAIN))
        # A repeated keyword is the same cipher. It must not outrank the short key.
        repeated = [hit for hit in hits if hit.key == VIGENERE_KEY * 2]
        if repeated:
            self.assertLess(best.period, repeated[0].period)
            self.assertGreaterEqual(best.score, repeated[0].score)

    def test_wrong_crib_does_not_return_the_fixture_plaintext(self) -> None:
        cipher = vigenere_encrypt(VIGENERE_PLAIN, VIGENERE_KEY)
        hits = search_vigenere_crib(cipher, "quartz samples from the ridge", max_period=12)
        for hit in hits:
            self.assertNotEqual(letters_only(hit.plaintext), letters_only(VIGENERE_PLAIN))
            self.assertNotEqual(hit.key, VIGENERE_KEY)


if __name__ == "__main__":
    unittest.main()
