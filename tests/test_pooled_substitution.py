"""Pooled substitution roundtrips a permutation and does not read the residue."""

from __future__ import annotations

import random
import unittest
from pathlib import Path

from engine.alphabet import letters_only, to_ints
from engine.language import ENGLISH_ORDER
from engine.pooled_substitution import (
    character_accuracy,
    encrypt_permutation,
    polish,
    pooled_key,
    search_pooled_swarm,
)


class PooledSubstitutionTest(unittest.TestCase):
    def test_permutation_roundtrips_and_unread_texts_stay_unread(self) -> None:
        letters = letters_only(Path("engine/data/english.txt").read_text(encoding="utf-8"))[:240]
        rng = random.Random(7)
        perm = list(range(26))
        rng.shuffle(perm)
        plain = to_ints(letters)
        cipher_seq = [perm[index] for index in plain]
        cipher = "".join(chr(65 + index) for index in cipher_seq)
        key, _score = polish(
            cipher_seq,
            pooled_key(cipher_seq, ENGLISH_ORDER, bijective=True),
            "english",
            bijective=True,
            seed=1,
        )
        self.assertEqual(len(set(key)), 26)
        decrypted = "".join(chr(65 + key[index]) for index in cipher_seq)
        self.assertEqual(encrypt_permutation(decrypted, key), cipher)
        self.assertGreater(character_accuracy(plain, [key[index] for index in cipher_seq]), 0.25)
        colliding, _score = polish(
            cipher_seq,
            pooled_key(cipher_seq, ENGLISH_ORDER, bijective=False),
            "english",
            bijective=False,
            seed=1,
        )
        self.assertLess(len(set(colliding)), 26)
        report = search_pooled_swarm()
        self.assertIs(report["solved"], False)
        self.assertIsNone(report["claimed_plaintext"])
        expected = {
            ("IASRZ_129", "english"): (-279.57, False),
            ("IASRZ_129", "german"): (-274.61, False),
            ("K4", "english"): (-309.35, False),
            ("K4", "german"): (-313.26, True),
        }
        # The last boolean is whether the control beat the bijective key.
        for row in report["rows"]:
            score, control_wins = expected[(row["text"], row["language"])]
            self.assertEqual(round(row["bijective_score"], 2), score)
            self.assertIs(row["beats_colliding"], False)
            self.assertIs(row["beats_control"], not control_wins)


if __name__ == "__main__":
    unittest.main()
