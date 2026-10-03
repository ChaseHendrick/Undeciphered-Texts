"""Beam search must beat a random substitution key on synthetic English.

The search does not decipher ancient scripts. See docs/beam-search.md.
"""

from __future__ import annotations

import random
import unittest
from pathlib import Path

from engine.ciphers import substitution_decrypt, substitution_encrypt
from engine.solvers.beam_search import (
    beam_search_decipher,
    get_beam_model,
    letter_accuracy,
)

_PLAIN = (
    "The quiet harbor kept every small boat safe while the morning tide lifted "
    "the wooden pier and the gulls cried over the gray water. A fisher mended "
    "nets beside a red shed and told his friend that the catch would improve "
    "once the wind shifted to the west. Children raced along the dock, counted "
    "the painted buoys, and begged for a story about a brave captain who guided "
    "a crowded ship through fog. Later the shops closed, lamps glowed in the "
    "windows, and the slow bell in the square marked the end of a long calm day."
)
_MODEL_PATH = Path(__file__).resolve().parent.parent / "engine" / "data" / "beam_english.txt"
_DOCS_PATH = Path(__file__).resolve().parent.parent / "docs" / "beam-search.md"


def _random_decrypt(cipher: str, seed: int) -> str:
    alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    random.Random(seed).shuffle(alphabet)
    return substitution_decrypt(cipher, "".join(alphabet))


class BeamSearchDecipherTest(unittest.TestCase):
    def test_beam_recovers_plaintext_better_than_a_random_key(self) -> None:
        rng = random.Random(20261002)
        alphabet = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
        rng.shuffle(alphabet)
        cipher = substitution_encrypt(_PLAIN, "".join(alphabet))
        result = beam_search_decipher(cipher, beam_width=40)
        beam_acc = letter_accuracy(result.plaintext, _PLAIN)
        random_acc = max(letter_accuracy(_random_decrypt(cipher, seed), _PLAIN) for seed in range(20))
        self.assertGreater(beam_acc, random_acc)
        self.assertGreater(beam_acc, 0.5)
        self.assertEqual(result.plaintext, _PLAIN)
        self.assertEqual(len(set(result.decrypt_key)), 26)
        self.assertEqual(len(result.decrypt_key), 26)

    def test_model_sample_is_not_the_plaintext(self) -> None:
        sample = _MODEL_PATH.read_text(encoding="utf-8")
        self.assertNotIn("quiet harbor", sample.lower())
        model = get_beam_model()
        self.assertEqual(len(model.log_unigram), 26)
        self.assertEqual(len(model.log_bigram), 26 * 26)
        self.assertGreater(model.train_letters, 1000)

    def test_documents_that_it_does_not_decipher_ancient_scripts(self) -> None:
        import engine.solvers.beam_search as beam_mod

        note = "does not decipher ancient scripts"
        self.assertIn(note, (beam_mod.__doc__ or "").lower())
        docs = _DOCS_PATH.read_text(encoding="utf-8")
        self.assertIn(note, docs.lower())
        self.assertIn("Linear A", docs)
        result = beam_search_decipher(substitution_encrypt(_PLAIN, "QWERTYUIOPASDFGHJKLZXCVBNM"), beam_width=20)
        self.assertIn(note, result.limitation.lower())

    def test_short_ciphertext_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            beam_search_decipher("Too short.")


if __name__ == "__main__":
    unittest.main()
