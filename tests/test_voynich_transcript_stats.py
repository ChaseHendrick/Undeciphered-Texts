"""Tests for the transcription-robustness statistics of the Voynich corpus."""

from __future__ import annotations

import unittest

import numpy as np

import engine.voynich_transcript_stats as stats
from engine.voynich_transcript_stats import (
    _spearman,
    _spearman_from_values,
    reserved_folios,
    transcript_stats,
    used_keys,
)
from engine.voynich_ivtff import parse_ivtff_text
from engine import voynich_compare

RESERVED = [
    "f87r", "f96v", "f95r2", "f68v1", "f32v",
    "f106r", "f67r1", "f36r", "f82v", "f24r",
]
USED_LOCI = 5013
_REAL = {"char1": 0.998, "ngram2": 0.96, "ngram3": 0.93, "ngram4": 0.90,
         "word1": 0.89}
_PLANT_MARGIN = {"char1": 0.02, "ngram2": 0.30, "ngram3": 0.50, "ngram4": 0.50,
                 "word1": 0.30}
_BASELINE_MARGIN = {"word1": 0.10, "ngram4": 0.0}  # only the clean gaps assert
_AB = "#=IVTFF Eva- 2.0 M 1\n"


class MetricTest(unittest.TestCase):
    def test_the_rank_metric_is_monotone_and_tie_safe(self) -> None:
        self.assertAlmostEqual(
            1.0, _spearman_from_values(np.array([1.0, 2.0, 3.0]),
                                       np.array([1.0, 2.0, 4.0])), places=12
        )
        self.assertAlmostEqual(
            -1.0, _spearman_from_values(np.array([1.0, 2.0, 3.0]),
                                        np.array([3.0, 2.0, 1.0])), places=12
        )
        value, shared = _spearman(
            {"a": 5, "b": 3}, {"a": 7, "b": 4, "c": 1}
        )
        self.assertEqual(2, shared)
        self.assertAlmostEqual(1.0, value, places=12)

    def test_glyph_normalisation_collapses_codes_and_question_runs(self) -> None:
        self.assertEqual(chr(0x100 + 254), stats._word_glyphs("@254;"))
        self.assertEqual("o?", stats._word_glyphs("o???"))
        self.assertEqual(chr(0x100 + 253) + "or", stats._word_glyphs("@253;or"))


class FrozenStatsTest(unittest.TestCase):
    """The frozen corpus measurement, computed once and pinned."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.report = transcript_stats()

    def test_the_reserved_folios_match_the_frozen_list(self) -> None:
        self.assertEqual(RESERVED, self.report["reserved_folios"])
        self.assertEqual(RESERVED, reserved_folios())

    def test_the_reservation_applies_to_the_used_loci(self) -> None:
        self.assertEqual(USED_LOCI, self.report["used_loci"])
        reserved = set(RESERVED)
        self.assertEqual(
            0, len({folio for folio, _ in used_keys()} & reserved)
        )

    def test_every_declared_statistic_agrees_at_its_frozen_level(self) -> None:
        for name, floor in _REAL.items():
            value = self.report["spearman"][name]
            self.assertGreaterEqual(value, floor, name)
            self.assertLessEqual(value, 1.0, name)

    def test_the_planted_relabelling_is_detected_at_every_statistic(self) -> None:
        planted = self.report["controls"]["planted_relabel_of_it"]["spearman"]
        for name, margin in _PLANT_MARGIN.items():
            self.assertGreaterEqual(
                self.report["spearman"][name] - planted[name], margin, name
            )

    def test_the_resampling_baseline_stays_below_the_word_agreement(self) -> None:
        baseline = self.report["controls"]["within_file_half_split_baseline"]
        real = self.report["spearman"]["word1"]
        for code in ("ZL", "IT"):
            self.assertLessEqual(
                baseline[code]["word1"], real - _BASELINE_MARGIN["word1"], code
            )

    def test_the_two_files_hold_the_same_glyphs_on_the_same_loci(self) -> None:
        glyphs = {code: self.report["files"][code]["glyphs"] for code in ("ZL", "IT")}
        self.assertLessEqual(abs(glyphs["ZL"] - glyphs["IT"]), 500)
        self.assertEqual(
            34354, self.report["files"]["ZL"]["tokens"], "ZL tokens"
        )
        self.assertEqual(
            36441, self.report["files"]["IT"]["tokens"], "IT tokens"
        )
        self.assertAlmostEqual(
            5.365, self.report["files"]["ZL"]["lengths"]["mean_length"], places=2
        )
        self.assertAlmostEqual(
            5.052, self.report["files"]["IT"]["lengths"]["mean_length"], places=2
        )


class SyntheticStatsTest(unittest.TestCase):
    """Planted control: identical synthetic files must fully agree."""

    folios = ["f1r", "f2r", "f3r", "f4r"]
    words = [
        "fachys.ykal.ar.ataiin",
        "sory.ckhar.or.daiin",
        "sheey.cthos.daiin.okaiin",
        "@253;or.?shealdy",
    ]

    def setUp(self) -> None:
        lines = ["#=IVTFF Eva- 2.0 M 1"]
        for folio in self.folios:
            lines.append(f"<{folio}>      <! $L=A>")
            for i, words in enumerate(self.words, start=1):
                marker = "@P0" if i == 1 else "+P0"
                lines.append(f"<{folio}.{i},{marker}>       {words}")
        text = "\n".join(lines) + "\n"
        self._originals = (
            stats.load, stats.index_loci, stats.RESERVED_COUNT, voynich_compare.load,
        )
        parsed = {code: parse_ivtff_text(text) for code in ("ZL", "IT")}
        shared_index = stats.index_loci(parsed["ZL"])

        def fake_load(code: str):
            return parsed[code]

        def fake_index(_file):  # identical content, one shared locus index
            return shared_index

        stats.load, stats.index_loci = fake_load, fake_index
        voynich_compare.load = fake_load
        stats.RESERVED_COUNT = 1

    def tearDown(self) -> None:
        (stats.load, stats.index_loci, stats.RESERVED_COUNT,
         voynich_compare.load) = self._originals

    def test_identical_synthetic_files_agree_on_every_statistic(self) -> None:
        report = transcript_stats()
        for name, value in report["spearman"].items():
            self.assertAlmostEqual(1.0, value, places=12, msg=name)
        self.assertEqual(12, report["used_loci"])
        self.assertEqual(1, len(report["reserved_folios"]))

    def test_one_relabeled_glyph_alone_is_detected(self) -> None:
        # Plant the smallest possible transcription noise and require the
        # bigram and word metrics to fall: a NaN means the shared type set
        # collapsed, which is itself detection.
        report = transcript_stats()
        planted = report["controls"]["planted_relabel_of_it"]["spearman"]
        for name in ("ngram2", "word1"):
            value = planted[name]
            detected = value != value or value < report["spearman"][name] - 0.05
            self.assertTrue(detected, name)


if __name__ == "__main__":
    unittest.main()
