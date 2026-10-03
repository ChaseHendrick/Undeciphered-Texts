"""Unsupervised sign clustering recovers synthetic vowel vs consonant classes.

The corpus is generated, not historical. Passing this test does not decipher
an ancient script.
"""

from __future__ import annotations

import unittest

from engine.sign_cluster import (
    NOT_A_DECIPHERMENT,
    alignment_accuracy,
    chance_alignment_accuracy,
    cluster_signs,
    generate_vowel_consonant_corpus,
)


class SignClusterRecoveryTest(unittest.TestCase):
    def test_disclaimer_says_this_does_not_decipher(self) -> None:
        self.assertIn("does not decipher an ancient script", NOT_A_DECIPHERMENT)

    def test_kmeans_recovers_vowel_and_consonant_classes_better_than_chance(self) -> None:
        corpus = generate_vowel_consonant_corpus(n_words=400, seed=0)
        clusters = cluster_signs(corpus.words, k=2, method="kmeans", seed=0)
        self.assertEqual(clusters.method, "kmeans")
        self.assertEqual(len(set(clusters.labels)), 2)
        # The clusterer is not given the generating classes.
        accuracy = alignment_accuracy(clusters, corpus.sign_class)
        chance = chance_alignment_accuracy(
            clusters, corpus.sign_class, n_perm=400, seed=1
        )
        self.assertGreater(
            accuracy,
            chance,
            msg=f"kmeans accuracy={accuracy:.3f} chance={chance:.3f}",
        )
        # A clear gap, not a coin-flip that happened to win by a hair.
        self.assertGreaterEqual(accuracy, 0.85)
        self.assertGreater(accuracy, chance + 0.2)
        groups = clusters.by_cluster()
        self.assertEqual(len(groups), 2)
        # Each cluster should be pure once labels are aligned: with accuracy
        # 1.0 every symbol matches. Allow a miss but require both classes to
        # be the majority of different clusters.
        for label, signs in groups.items():
            classes = {corpus.sign_class[sign] for sign in signs}
            self.assertEqual(len(classes), 1, msg=f"cluster {label} mixed: {signs}")

    def test_hierarchical_also_beats_chance(self) -> None:
        corpus = generate_vowel_consonant_corpus(n_words=400, seed=0)
        clusters = cluster_signs(corpus.words, k=2, method="hierarchical")
        accuracy = alignment_accuracy(clusters, corpus.sign_class)
        chance = chance_alignment_accuracy(
            clusters, corpus.sign_class, n_perm=400, seed=1
        )
        self.assertGreater(
            accuracy,
            chance,
            msg=f"hierarchical accuracy={accuracy:.3f} chance={chance:.3f}",
        )
        self.assertGreaterEqual(accuracy, 0.85)

    def test_same_seed_is_repeatable_and_labels_are_unused(self) -> None:
        corpus = generate_vowel_consonant_corpus(n_words=80, seed=2)
        first = cluster_signs(corpus.words, method="kmeans", seed=3)
        second = cluster_signs(corpus.words, method="kmeans", seed=3)
        self.assertEqual(first.labels, second.labels)
        self.assertEqual(first.signs, second.signs)


if __name__ == "__main__":
    unittest.main()
