"""Baum–Welch recovers a synthetic two-state path better than chance.

This is not a decipherment test. No ancient script is an input.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from engine.hmm_baum_welch import (
    DOES_NOT_DECIPHER_ANCIENT_SCRIPTS,
    aligned_state_accuracy,
    constant_state_baseline,
    fit_baum_welch,
    generate_two_state_corpus,
)

ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "hmm-baum-welch.md"


class BaumWelchRecoveryTest(unittest.TestCase):
    def test_recovers_hidden_states_better_than_chance(self) -> None:
        corpus = generate_two_state_corpus(length=500, seed=0)
        # Unsupervised: only symbols are passed. Generating states stay out of fit.
        fit = fit_baum_welch(
            corpus.symbols,
            n_states=2,
            n_iter=30,
            restarts=4,
            seed=0,
            alphabet=corpus.alphabet,
        )
        accuracy = aligned_state_accuracy(corpus.states, fit.states)
        chance = constant_state_baseline(corpus.states)
        self.assertGreater(accuracy, 0.5)
        self.assertGreater(accuracy, chance)
        # Margin over the best constant labeling, which is chance on a balanced chain.
        self.assertGreaterEqual(accuracy, chance + 0.2)
        self.assertGreaterEqual(accuracy, 0.85)
        self.assertEqual(len(fit.states), len(corpus.symbols))
        self.assertTrue(math_is_finite(fit.log_likelihood))
        self.assertAlmostEqual(sum(fit.start), 1.0, places=6)
        for row in fit.transition:
            self.assertAlmostEqual(sum(row), 1.0, places=6)
        for row in fit.emission:
            self.assertAlmostEqual(sum(row), 1.0, places=6)
        # Fixed seed is deterministic.
        again = fit_baum_welch(
            corpus.symbols,
            n_states=2,
            n_iter=30,
            restarts=4,
            seed=0,
            alphabet=corpus.alphabet,
        )
        self.assertEqual(again.states, fit.states)
        self.assertAlmostEqual(again.log_likelihood, fit.log_likelihood, places=6)

    def test_module_documents_it_does_not_decipher_ancient_scripts(self) -> None:
        import engine.hmm_baum_welch as hmm

        self.assertIn("does not decipher ancient scripts", DOES_NOT_DECIPHER_ANCIENT_SCRIPTS)
        self.assertIn("does not decipher ancient scripts", hmm.__doc__ or "")
        self.assertIn("Linear A", DOES_NOT_DECIPHER_ANCIENT_SCRIPTS)
        text = DOC.read_text(encoding="utf-8")
        self.assertIn("does not decipher ancient scripts", text)
        self.assertIn("better than chance", text)
        self.assertNotIn("\ufeff", text)
        # The note is UTF-8 prose, not a JPEG and not base64-as-text.
        raw = DOC.read_bytes()
        self.assertFalse(raw.startswith(b"\xff\xd8\xff"))
        raw.decode("utf-8")


class BaumWelchGuardsTest(unittest.TestCase):
    def test_rejects_short_or_unknown_symbols(self) -> None:
        with self.assertRaises(ValueError):
            fit_baum_welch(["A"])
        with self.assertRaises(ValueError):
            fit_baum_welch(["A", "B"], alphabet=("A",))
        with self.assertRaises(ValueError):
            generate_two_state_corpus(length=1)
        with self.assertRaises(ValueError):
            aligned_state_accuracy([0, 1], [0])


def math_is_finite(value: float) -> bool:
    return value == value and value not in (float("inf"), float("-inf"))


if __name__ == "__main__":
    unittest.main()
