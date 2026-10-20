"""Tests for the locus alignment of the frozen Voynich transliterations."""

from __future__ import annotations

import unittest

import engine.voynich_compare as compare
from engine.voynich_compare import disagreement_report, headline, pair_alignment
from engine.voynich_ivtff import parse_ivtff_text

_FILE_A = """#=IVTFF Eva- 2.0 M 1
<f1r>      <! $L=A>
<f1r.1,@P0>       fachys.ykal.ar.ataiin
<f1r.2,+P0>       sory.ckhar.or.c
<fRos.2,@Cc>      oto.tosaes.adar.otar
"""

_FILE_B = """#=IVTFF Eva- 2.0 M 1
<f1r>      <! $L=A>
<f1r.1,@P0>       fachys.ykal.ar.ataiin
<f1r.2,+P0>       sory.ckhar.or.daiin
<f1r.3,@L0>       chedy.okin
"""


class SyntheticAlignmentTest(unittest.TestCase):
    """A planted control: the comparator must report exact agreement and,
    on a changed word, must land the locus in a lower agreement band."""

    def setUp(self) -> None:
        self._original_load = compare.load
        # ZL and IT share two loci; the first is identical, one word of the
        # second differs; each has one locus alone.
        files = {"ZL": parse_ivtff_text(_FILE_A), "GC": parse_ivtff_text(_FILE_A),
                 "IT": parse_ivtff_text(_FILE_B)}

        def fake_load(code: str):
            return files[code]

        compare.load = fake_load

    def tearDown(self) -> None:
        compare.load = self._original_load

    def test_shared_only_counts_and_bands_for_the_control(self) -> None:
        report = pair_alignment("ZL", "IT")
        self.assertEqual(2, report["shared_loci"])
        self.assertEqual(1, report["only_a"])
        self.assertEqual(1, report["only_b"])
        self.assertEqual(0.5, report["loci_word_identical_share"])
        self.assertEqual({0.875}, {report["words_matched_share"]})
        self.assertEqual(
            {"identical": 1, "two-thirds-to-one": 1},
            report["agreement_band_counts"],
        )

    def test_the_cross_alphabet_pair_reports_structure_only(self) -> None:
        report = pair_alignment("ZL", "GC")
        self.assertFalse(report["same_alphabet"])
        self.assertTrue(report["loci_word_identical_share"] is None)
        self.assertEqual(1.0, report["shared_word_count_equal_share"])
        self.assertIn("note", report)


class FrozenAlignmentTest(unittest.TestCase):
    """The frozen files, parsed fresh from disk, are the ground truth."""

    def test_the_real_pairs_align_with_the_frozen_files(self) -> None:
        report = pair_alignment("ZL", "IT")
        self.assertEqual(5385, report["loci_a"])
        self.assertEqual(5215, report["loci_b"])
        self.assertEqual(5214, report["shared_loci"])
        self.assertEqual(1, report["only_b"])
        self.assertTrue(report["same_alphabet"])
        self.assertGreater(report["words_matched_share"], 0.7)
        self.assertLess(report["words_matched_share"], 0.9)

    def test_the_cross_alphabet_pair_comes_with_an_honest_note(self) -> None:
        report = pair_alignment("ZL", "GC")
        self.assertFalse(report["same_alphabet"])
        self.assertIn("note", report)
        self.assertEqual(5366, report["shared_loci"])
        self.assertEqual(1, report["only_b"])

    def test_headline_names_all_three_pairs(self) -> None:
        text = headline(disagreement_report())
        for marker in ("ZL vs IT", "ZL vs GC", "GC vs IT"):
            self.assertIn(marker, text)
        self.assertIn("5214", text)


if __name__ == "__main__":
    unittest.main()
