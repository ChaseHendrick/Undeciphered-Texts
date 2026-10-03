"""German letter fitness must prefer German prose over random letters.

The probe is not the training excerpt and not a reading of any ciphertext.
Scoring the logged Truppenschlüssel Nr. 86 failures only measures resemblance
to the Grimm sample. It does not produce a plaintext.
"""

from __future__ import annotations

import random
import unittest

from engine.alphabet import to_ints
from engine.german import (
    FAILED_NR86_APPROACHES,
    TRUPPENSCHLUESSEL_NR86,
    german_letters,
    get_german_model,
    score_failed_nr86,
)

# Held out: Grimm, "Der Wolf und die sieben jungen Geißlein," same Gutenberg
# edition as the training file, but that tale is not in the excerpt.
GERMAN_PROBE = (
    "Es war einmal eine alte Geiß, die hatte sieben junge Geißlein, "
    "und hatte sie lieb, wie eine Mutter ihre Kinder lieb hat. "
    "Eines Tages wollte sie in den Wald gehen und Futter holen."
)


class GermanLetterModelTest(unittest.TestCase):
    def test_german_prose_scores_higher_than_random_letters(self) -> None:
        model = get_german_model()
        self.assertGreater(model.sample_letters, 400)
        letters = german_letters(GERMAN_PROBE)
        self.assertNotIn(letters, model.training_letters)
        # ß in "Geißlein" must fold to SS; the probe is not left as a raw umlaut.
        self.assertIn("GEISS", letters)
        self.assertNotIn("ß", letters)
        seq = to_ints(letters)
        draw = random.Random(86)
        random_seq = [draw.randrange(26) for _ in seq]
        self.assertEqual(len(seq), len(random_seq))
        self.assertGreater(len(set(random_seq)), 10)
        self.assertGreater(model.quadgram_score(seq), model.quadgram_score(random_seq))
        self.assertGreater(model.unigram_score(seq), model.unigram_score(random_seq))
        self.assertLess(model.chi_square(seq), model.chi_square(random_seq))

    def test_training_excerpt_is_not_the_unsolved_ciphertext(self) -> None:
        model = get_german_model()
        cipher = german_letters(TRUPPENSCHLUESSEL_NR86)
        self.assertEqual(len(cipher), 46)
        self.assertNotIn(cipher, model.training_letters)
        for _name, text in FAILED_NR86_APPROACHES:
            folded = german_letters(text)
            self.assertEqual(len(folded), 46)
            self.assertNotIn(folded, model.training_letters)

    def test_logged_nr86_failures_score_below_german_prose(self) -> None:
        """The logged Caesar, Vigenère, and substitution dumps are not German."""
        model = get_german_model()
        probe = to_ints(german_letters(GERMAN_PROBE))
        probe_mean = model.mean_quadgram(probe)
        rows = {row["name"]: row for row in score_failed_nr86(model)}
        self.assertEqual(set(rows), {"ciphertext", "caesar", "vigenere", "substitution"})
        for name, _text in FAILED_NR86_APPROACHES:
            row = rows[name]
            self.assertEqual(row["letters"], 46)
            self.assertLess(row["mean_quadgram"], probe_mean)
            self.assertIsInstance(row["quadgram"], float)
            self.assertIsInstance(row["chi_square"], float)


if __name__ == "__main__":
    unittest.main()
