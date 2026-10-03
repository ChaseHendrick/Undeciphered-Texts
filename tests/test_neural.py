"""The learned letter model must prefer English over random letters.

The probe sentence is not the training excerpt and not a solver fixture.
A higher score is only an English-letter fitness, not a claim about
Linear A, Voynich, or the Vesuvius scrolls.
"""

from __future__ import annotations

import random
import unittest

from engine.alphabet import letters_only, to_ints
from engine.neural import get_neural_model


ENGLISH_PROBE = (
    "The baker counted the loaves and set them on the wooden rack "
    "before the shop opened for the morning trade."
)


class NeuralLetterModelTest(unittest.TestCase):
    def test_prefers_real_english_over_random_letters(self) -> None:
        model = get_neural_model()
        self.assertGreater(model.train_events, 1000)
        self.assertLess(model.final_loss, model.initial_loss)
        self.assertIn(model.backend, {"numpy", "python"})

        letters = "".join(ch for ch in letters_only(ENGLISH_PROBE) if "A" <= ch <= "Z")
        self.assertNotIn(letters, model.training_letters)
        seq = to_ints(letters)
        draw = random.Random(1)
        random_seq = [draw.randrange(26) for _ in seq]
        self.assertEqual(len(seq), len(random_seq))
        self.assertGreater(len(set(random_seq)), 10)
        self.assertGreater(model.score(seq), model.score(random_seq))

    def test_training_prose_is_not_the_solver_fixture(self) -> None:
        from engine.fixtures import CAESAR_PLAIN, SUBSTITUTION_PLAIN, VIGENERE_PLAIN

        model = get_neural_model()
        for plain in (CAESAR_PLAIN, VIGENERE_PLAIN, SUBSTITUTION_PLAIN):
            folded = "".join(ch for ch in letters_only(plain) if "A" <= ch <= "Z")
            self.assertNotIn(folded, model.training_letters)

    def test_substitution_records_neural_second_opinion(self) -> None:
        from engine.ciphers import substitution_encrypt
        from engine.fixtures import SUBSTITUTION_KEY, SUBSTITUTION_PLAIN
        from engine.solvers.substitution import solve_substitution

        cipher = substitution_encrypt(SUBSTITUTION_PLAIN, SUBSTITUTION_KEY)
        result = solve_substitution(cipher, restarts=1, steps=1, seed=20261002)
        self.assertEqual(result.details["fitness"], "quadgram")
        self.assertEqual(result.details["second_opinion"], "neural_trigram")
        self.assertIsInstance(result.details["neural_score"], float)
        folded = "".join(ch for ch in letters_only(result.plaintext) if "A" <= ch <= "Z")
        self.assertAlmostEqual(
            result.details["neural_score"],
            get_neural_model().score(to_ints(folded)),
            places=5,
        )


if __name__ == "__main__":
    unittest.main()
