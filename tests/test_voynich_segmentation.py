"""Tests for the word-segmentation range of the Voynich corpus."""

from __future__ import annotations

import unittest

import engine.voynich_ivtff as ivtff
import engine.voynich_segmentation as seg
import engine.voynich_transcript_stats as base
from engine.voynich_compare import index_loci
from engine.voynich_ivtff import parse_ivtff_text
from engine.voynich_segmentation import locus_words, segmentation_range


class LockTest(unittest.TestCase):
    """The join policy must never drift from the frozen parser."""

    def test_join_policy_is_the_parser_on_every_locus_of_all_files(
        self,
    ) -> None:
        checked = 0
        for code in ("ZL", "GC", "IT"):
            index = index_loci(ivtff.load(code))
            for locus in index.values():
                self.assertEqual(locus.words, locus_words(locus.raw, "join"), locus.folio)
                checked += 1
        self.assertGreater(checked, 15000)

    def test_split_policy_partitions_exactly_at_uncertain_spaces(self) -> None:
        # Every comma becomes a boundary; everything else is untouched.
        self.assertEqual(("ab", "cd"), seg.split_words("ab,cd"))
        self.assertEqual(("ab", "cd", "ef"), seg.split_words("ab,cd.ef"))
        self.assertEqual(("ab", "cd"), seg.split_words("ab,.cd"))
        self.assertEqual(("ab",), seg.split_words("{ab}"))


class FrozenDivisionTest(unittest.TestCase):
    """The frozen corpus measurement, computed once and pinned."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.report = segmentation_range()

    def test_the_uncertain_spaces_live_only_in_zl_and_gc(self) -> None:
        joins = {
            code: self.report["files"][code]["join"]["uncertain_joins"]
            for code in ("ZL", "GC", "IT")
        }
        self.assertEqual(2603, joins["ZL"])
        self.assertEqual(2321, joins["GC"])
        self.assertEqual(0, joins["IT"])

    def test_sign_frequencies_are_invariant_under_both_policies(self) -> None:
        for code in ("ZL", "GC", "IT"):
            self.assertEqual(
                0,
                self.report["word_statistic_movement"][code][
                    "sign_frequency_delta"
                ],
                code,
            )

    def test_token_delta_equals_the_join_count_exactly(self) -> None:
        for code in ("ZL", "GC", "IT"):
            facts = self.report["files"][code]
            movement = self.report["word_statistic_movement"][code]
            self.assertEqual(
                facts["join"]["uncertain_joins"], movement["token_delta"], code
            )
        self.assertEqual(34354, self.report["files"]["ZL"]["join"]["tokens"])
        self.assertEqual(36957, self.report["files"]["ZL"]["split"]["tokens"])
        self.assertEqual(38553, self.report["files"]["GC"]["split"]["tokens"])
        self.assertEqual(36441, self.report["files"]["IT"]["split"]["tokens"])

    def test_it_is_the_zero_join_control(self) -> None:
        it = self.report["files"]["IT"]
        movement = self.report["word_statistic_movement"]["IT"]
        self.assertEqual(1.0, movement["word_frequency_rho_join_vs_split"])
        self.assertEqual(it["join"], it["split"])

    def test_word_statistics_move_without_collapsing(self) -> None:
        zl = self.report["word_statistic_movement"]["ZL"][
            "word_frequency_rho_join_vs_split"
        ]
        gc = self.report["word_statistic_movement"]["GC"][
            "word_frequency_rho_join_vs_split"
        ]
        self.assertGreaterEqual(zl, 0.93, "ZL")
        self.assertLessEqual(zl, 0.95, "ZL")
        self.assertGreaterEqual(gc, 0.93, "GC")
        self.assertLessEqual(gc, 0.96, "GC")
        # More tokens, fewer types: the long-word convention was inflating
        # the vocabulary with rare joined forms.
        self.assertLess(
            self.report["files"]["ZL"]["split"]["types"],
            self.report["files"]["ZL"]["join"]["types"],
        )
        self.assertEqual(7959, self.report["files"]["ZL"]["split"]["types"])
        self.assertEqual(9438, self.report["files"]["GC"]["split"]["types"])

    def test_cross_file_agreement_is_stable_across_policies(self) -> None:
        cross = self.report["cross_file_agreement"]
        frozen_family_one = {
            "char1": 0.999,
            "ngram2": 0.9647,
            "ngram3": 0.9365,
            "ngram4": 0.9146,
            "word1": 0.9015,
        }
        for name, value in frozen_family_one.items():
            self.assertAlmostEqual(
                value, cross["join"][name], places=4, msg=name
            )
        for name, floor in frozen_family_one.items():
            self.assertGreaterEqual(cross["split"][name], floor, msg=name)
        # Cutting at unsure spaces did not hide agreement anywhere:
        for name in frozen_family_one:
            self.assertGreaterEqual(
                cross["split"][name], cross["join"][name] - 0.011, name
            )


class SyntheticDivisionTest(unittest.TestCase):
    """Planted control: known commas must yield known movements.

    Locus compositions differ per folio (the first 4-j word lines, so type
    counts are unequal and the rank metric is defined), each comma is
    interior, and lines 2 and 4 carry no commas at all.
    """

    folios = ["f1r", "f2r", "f3r", "f4r"]
    words = [
        "fachys,ykal.ar,ataiin",
        "sory.ckhar.or.daiin",
        "sheey,cthos.daiin,okaiin",
        "qokal.dy.otedy.qokain",
    ]

    def setUp(self) -> None:
        lines = ["#=IVTFF Eva- 2.0 M 1"]
        for index, folio in enumerate(self.folios):
            lines.append(f"<{folio}>      <! $L=A>")
            for i, words in enumerate(self.words[: 4 - index], start=1):
                marker = "@P0" if i == 1 else "+P0"
                lines.append(f"<{folio}.{i},{marker}>       {words}")
        text = "\n".join(lines) + "\n"
        self._originals = (
            base.load, base.index_loci, base.RESERVED_COUNT,
            seg.load, seg.index_loci, seg._FILES,
        )
        parsed = {code: parse_ivtff_text(text) for code in ("ZL", "IT")}
        shared_index = index_loci(parsed["ZL"])

        def fake_load(code: str):
            return parsed[code]

        def fake_index(_file):
            return shared_index

        base.load, base.index_loci = fake_load, fake_index
        seg.load, seg.index_loci = fake_load, fake_index
        base.RESERVED_COUNT = 1
        seg._FILES = ("ZL", "IT")

    def tearDown(self) -> None:
        (base.load, base.index_loci, base.RESERVED_COUNT,
         seg.load, seg.index_loci, seg._FILES) = self._originals

    def test_planted_commas_produce_exactly_their_own_movements(self) -> None:
        report = segmentation_range()
        self.assertEqual(7, report["used_loci"])
        movement = report["word_statistic_movement"]["ZL"]
        joins = report["files"]["ZL"]["join"]["uncertain_joins"]
        self.assertGreater(joins, 0)
        # Every interior join is exactly one new token.
        self.assertEqual(joins, movement["token_delta"])
        self.assertEqual(0, movement["sign_frequency_delta"])
        # The type inventory and the mean length move with the segmentation.
        self.assertNotEqual(
            report["files"]["ZL"]["join"]["types"],
            report["files"]["ZL"]["split"]["types"],
        )
        self.assertLess(
            report["files"]["ZL"]["split"]["mean_length"],
            report["files"]["ZL"]["join"]["mean_length"],
        )
        # Identical files must agree at 1.0 under either policy.
        for policy in ("join", "split"):
            self.assertAlmostEqual(
                1.0, report["cross_file_agreement"][policy]["word1"], places=12
            )
        self.assertEqual(
            report["word_statistic_movement"]["ZL"]["token_delta"],
            report["word_statistic_movement"]["IT"]["token_delta"],
        )


if __name__ == "__main__":
    unittest.main()
