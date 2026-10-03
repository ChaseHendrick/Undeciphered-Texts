"""EM sign-to-letter recovery on a synthetic English substitution.

The corpus is ordinary English with each letter replaced by a random sign
label. The test does not read Linear A, the Indus script, or the Voynich
manuscript, and the aligner is not given the map it has to recover.
"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROSE_PATH = ROOT / "engine" / "data" / "english.txt"
DOC_PATH = ROOT / "docs" / "em-sign-aligner.md"
HERO_JPEG = ROOT / "docs" / "assets" / "readme-hero.jpg"


def _numpy():
    try:
        import numpy as np
    except ImportError:
        return None
    return np


class EmSignAlignerTest(unittest.TestCase):
    def test_scope_names_scripts_it_does_not_read(self) -> None:
        from engine.solvers import em_sign_aligner

        for name in ("Linear A", "Indus", "Voynich"):
            self.assertIn(name, em_sign_aligner.__doc__ or "")
            self.assertIn(name, em_sign_aligner.SCOPE)
        self.assertIn("does not read", em_sign_aligner.SCOPE)
        doc = DOC_PATH.read_text(encoding="utf-8")
        for name in ("Linear A", "Indus", "Voynich"):
            self.assertIn(name, doc)
        self.assertIn("does not read", doc.lower())
        # New files only: the hero JPEG stays a JPEG.
        self.assertEqual(HERO_JPEG.read_bytes()[:3], bytes.fromhex("ffd8ff"))

    def test_recovers_most_of_random_sign_map(self) -> None:
        if _numpy() is None:
            self.skipTest("numpy is required for the EM sign aligner")
        from engine.solvers.em_sign_aligner import (
            align_signs,
            character_accuracy,
            encode_letters,
            fit_bigram_channel,
            holdout_letters,
            map_accuracy,
            random_letter_to_sign,
        )

        prose = PROSE_PATH.read_text(encoding="utf-8")
        language_sample, hidden = holdout_letters(prose, split=0.45)
        self.assertGreater(len(hidden), 2000)
        self.assertNotIn(hidden[:60], language_sample)
        transition, initial = fit_bigram_channel(language_sample)
        letter_to_sign = random_letter_to_sign(20261002)
        self.assertEqual(len(set(letter_to_sign.values())), 26)
        signs = encode_letters(hidden, letter_to_sign)
        self.assertEqual(len(signs), len(hidden))
        self.assertTrue(all(sign.startswith("U+") for sign in signs))
        self.assertTrue(all(not sign.isalpha() for sign in signs))
        # Truth is scored after alignment. It is not passed into align_signs.
        truth = {sign: letter for letter, sign in letter_to_sign.items()}
        result = align_signs(signs, transition, initial, seed=20261002, restarts=2)
        self.assertGreaterEqual(result.iterations, 2)
        self.assertEqual(result.observed_signs, 26)
        self.assertEqual(len(result.plaintext), len(hidden))
        self.assertTrue(result.log_likelihood < 0.0)
        sign_acc = map_accuracy(result.sign_to_letter, truth, signs)
        char_acc = character_accuracy(result.plaintext, hidden)
        # Most of the 26-sign map, and nearly all of the letter stream.
        # Rare letters may still swap; that is not a reading of a real script.
        self.assertGreaterEqual(sign_acc, 0.80, msg=f"map accuracy {sign_acc:.4f}")
        self.assertGreaterEqual(char_acc, 0.95, msg=f"character accuracy {char_acc:.4f}")
        print(
            f"MAP_ACCURACY {sign_acc:.4f} CHAR_ACCURACY {char_acc:.4f} "
            f"SIGNS {result.observed_signs} ITERATIONS {result.iterations}",
            flush=True,
        )


if __name__ == "__main__":
    unittest.main()
