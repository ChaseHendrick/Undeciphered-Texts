"""Tests for the IVTFF parser of the frozen Voynich MS transliterations."""

from __future__ import annotations

import unittest
from pathlib import Path

from engine import voynich_ivtff
from engine.voynich_ivtff import (
    IVTFFFile,
    Page,
    load,
    parse_ivtff_text,
    statistics,
)

_MINIMAL = """#=IVTFF Eva- 2.0 M 1
# A synthetic file with every grammar case the frozen files use.

<f1r>      <! $Q=A $P=A $F=a $B=1 $I=T $L=A $H=1 $C=1 $X=V>
<f1r.1,@P0>       <%>fachys.ykal[sh:do]or<!a free note>.and<->head
<f1r.2,+P0>       sory.ckhar,or.dan
<f1r.3,@L0>       @253;.{ee}???
<f1r.4,=Pt>       otol.daiiin<$>
# a comment line
<f1r.5,@Lc;G>     <!25:30>plant
"""


class ParserGrammarTest(unittest.TestCase):
    def test_the_synthetic_file_parses_structure_and_words(self) -> None:
        file = parse_ivtff_text(_MINIMAL)
        self.assertEqual(1, len(file.pages))
        self.assertEqual(5, len(file.pages[0].loci))
        self.assertEqual("A", file.pages[0].vars["Q"])
        self.assertEqual("1", file.pages[0].vars["H"])
        self.assertEqual([], list(file.warnings))

    def test_definite_and_drawing_separators_split_and_comments_are_stripped(self) -> None:
        file = parse_ivtff_text(_MINIMAL)
        locus = file.loci[0]
        self.assertEqual(("fachys", "ykalshor", "and", "head"), locus.words)
        self.assertEqual(1, locus.drawing_gaps)
        self.assertEqual(1, locus.paragraph_start)
        self.assertFalse(locus.paragraph_end)

    def test_uncertain_readings_resolve_to_the_first_option(self) -> None:
        file = parse_ivtff_text(_MINIMAL)
        locus = file.loci[0]
        self.assertEqual(1, locus.alt_readings)

    def test_uncertain_spaces_join_words_under_the_frozen_convention(self) -> None:
        file = parse_ivtff_text(_MINIMAL)
        locus = file.loci[1]
        self.assertEqual(("sory", "ckharor", "dan"), locus.words)
        self.assertEqual(1, locus.uncertain_joins)

    def test_high_ascii_ligatures_and_unreadable_glyps(self) -> None:
        file = parse_ivtff_text(_MINIMAL)
        locus = file.loci[2]
        self.assertEqual(("@253;", "ee???"), locus.words)
        self.assertEqual(("???",), locus.unreadable)
        self.assertEqual(0, locus.paragraph_start)

    def test_titles_and_paragraph_end_and_source_id(self) -> None:
        file = parse_ivtff_text(_MINIMAL)
        title = file.loci[3]
        self.assertEqual("Pt", title.locus_type)
        self.assertEqual("=", title.locator)
        self.assertTrue(title.paragraph_end)
        self.assertEqual(("otol", "daiiin"), title.words)
        labelled = file.loci[4]
        self.assertEqual("G", labelled.source_id)
        self.assertEqual(("plant",), labelled.words)


class FrozenCorpusTest(unittest.TestCase):
    """The frozen files are the ground truth the parser must reproduce."""

    def test_loci_paragraphs_and_long_words_match_the_published_counts(self) -> None:
        expected = {
            "ZL": {"locus_count": 5385, "paragraph_count": 740, "long_word_count": 36278},
            "GC": {"locus_count": 5367, "paragraph_count": 775, "long_word_count": 38242},
            "IT": {"locus_count": 5215, "paragraph_count": 772, "long_word_count": 37919},
        }
        for code in ("ZL", "GC", "IT"):
            file = load(code)
            for key, value in expected[code].items():
                self.assertEqual(value, getattr(file, key), key)

    def test_headers_identify_the_three_files(self) -> None:
        self.assertEqual("Eva-", load("ZL").alphabet_code)
        self.assertEqual("v101", load("GC").alphabet_code)
        self.assertEqual("EvaT", load("IT").alphabet_code)
        for code in ("ZL", "GC", "IT"):
            self.assertEqual("2.0", load(code).format_version)

    def test_gc_and_it_carry_one_invalid_locus_each_and_zl_zero(self) -> None:
        self.assertEqual(0, len(load("ZL").invalid_loci))
        for code in ("GC", "IT"):
            invalid = load(code).invalid_loci
            self.assertEqual(1, len(invalid), code)
            self.assertEqual("f89v2", invalid[0].folio, code)
            self.assertEqual(26, invalid[0].num, code)

    def test_fros_is_covered_by_zl_and_gc_only(self) -> None:
        self.assertIn("fRos", [page.name for page in load("ZL").pages])
        self.assertIn("fRos", [page.name for page in load("GC").pages])
        self.assertNotIn("fRos", [page.name for page in load("IT").pages])

    def test_the_parse_is_silent_with_no_warnings(self) -> None:
        for code in ("ZL", "GC", "IT"):
            self.assertEqual([], list(load(code).warnings), code)

    def test_statistics_reports_what_the_log_records(self) -> None:
        stats = statistics(load("ZL"))
        self.assertEqual(5385, stats["loci"])
        self.assertEqual(740, stats["paragraphs"])
        self.assertEqual(36278, stats["long_words"])
        self.assertEqual(227, stats["pages"])
        self.assertEqual("Eva-", stats["alphabet_code"])


if __name__ == "__main__":
    unittest.main()
