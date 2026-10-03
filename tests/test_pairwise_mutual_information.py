"""Planted-pair test for adjacent-sign mutual information.

The corpus is synthetic. A passing rank is not a reading of any ancient script.
"""

from __future__ import annotations

import random
import unittest

from engine.pairwise_mutual_information import (
    mutual_information_bits,
    pairwise_mutual_information,
    pairwise_mutual_information_grouped,
)


PLANTED = ("QX", "ZY")


def _planted_corpus(seed: int = 20261002) -> list[str]:
    """Independent background, then one ordered pair planted far above chance.

    Background signs are drawn from A-H only. QX is always followed by ZY, and
    ZY does not occur otherwise, so the pair's count is several times the
    independence expectation N * P(QX) * P(ZY). Labels are invented. They are
    not a historical sign list.
    """
    rng = random.Random(seed)
    background = ["A", "B", "C", "D", "E", "F", "G", "H"]
    signs: list[str] = [rng.choice(background) for _ in range(800)]
    for _ in range(200):
        signs.append("QX")
        signs.append("ZY")
        signs.append(rng.choice(background))
    return signs


class PairwiseMutualInformationTest(unittest.TestCase):
    def test_planted_pair_ranks_first(self) -> None:
        signs = _planted_corpus()
        ranked = pairwise_mutual_information(signs)
        self.assertGreaterEqual(len(ranked), 2)
        top = ranked[0]
        self.assertEqual(top.pair, PLANTED)
        self.assertGreater(top.pmi_bits, ranked[1].pmi_bits)
        # Far more often than the independence baseline for this stream.
        self.assertGreater(top.count, 5 * top.expected_count)
        self.assertGreater(top.pmi_bits, 1.0)
        self.assertEqual(top.text, "QX ZY")

    def test_planted_pair_is_stable_across_seeds(self) -> None:
        for seed in range(20):
            ranked = pairwise_mutual_information(_planted_corpus(seed))
            self.assertEqual(ranked[0].pair, PLANTED, msg=f"seed {seed}")
            self.assertGreater(ranked[0].pmi_bits, ranked[1].pmi_bits)

    def test_short_stream_is_empty(self) -> None:
        self.assertEqual(pairwise_mutual_information([]), [])
        self.assertEqual(pairwise_mutual_information(["ONLY"]), [])
        self.assertEqual(mutual_information_bits([]), 0.0)

    def test_independent_pair_has_zero_pmi(self) -> None:
        # One repeated sign: the only adjacent pair is independent of itself.
        ranked = pairwise_mutual_information(["S", "S", "S", "S"])
        self.assertEqual(len(ranked), 1)
        self.assertEqual(ranked[0].pair, ("S", "S"))
        self.assertAlmostEqual(ranked[0].pmi_bits, 0.0, places=9)
        self.assertAlmostEqual(ranked[0].count, ranked[0].expected_count, places=9)
        self.assertAlmostEqual(mutual_information_bits(ranked), 0.0, places=9)

    def test_grouped_spans_do_not_cross_boundaries(self) -> None:
        # Within lines the planted pair repeats. Across lines, ZY would meet QX
        # if the spans were concatenated. Grouping must not count that join.
        spans = [["QX", "ZY"], ["QX", "ZY"], ["QX", "ZY"]]
        ranked = pairwise_mutual_information_grouped(spans)
        self.assertEqual([row.pair for row in ranked], [("QX", "ZY")])
        self.assertEqual(ranked[0].count, 3)
        crossed = pairwise_mutual_information([sign for span in spans for sign in span])
        crossed_pairs = {row.pair for row in crossed}
        self.assertIn(("ZY", "QX"), crossed_pairs)
        self.assertNotIn(("ZY", "QX"), {row.pair for row in ranked})

    def test_module_states_it_does_not_decipher(self) -> None:
        import engine.pairwise_mutual_information as mod

        doc = mod.__doc__ or ""
        self.assertIn("does not decipher", doc)
        self.assertIn("Voynich", doc)
        self.assertIn("Linear A", doc)


if __name__ == "__main__":
    unittest.main()
