"""Tests for unknown-script analysis helpers (not decipherment)."""

from __future__ import annotations

import unittest
from pathlib import Path

from engine.script_tools import (
    SYNTHETIC_BILINGUAL_PATH,
    SYNTHETIC_CORPUS_PATH,
    check_bilingual_crib,
    find_repeated_sequences,
    load_sign_corpus,
    load_synthetic_bilingual,
    sign_inventory,
    tokenize_signs,
)

ROOT = Path(__file__).resolve().parents[1]


class SignInventoryTest(unittest.TestCase):
    def test_fixture_corpus_inventory_and_frequencies(self) -> None:
        signs = load_sign_corpus(SYNTHETIC_CORPUS_PATH)
        inv = sign_inventory(signs)
        self.assertGreater(inv.total, 0)
        self.assertEqual(inv.total, len(signs))
        self.assertEqual(inv.unique, len(inv.counts))
        # SX02 and SX03 dominate the fixture (repeated bigram SX02 SX03).
        top_signs = [sign for sign, _ in inv.counts[:3]]
        self.assertIn("SX02", top_signs)
        self.assertIn("SX03", top_signs)
        self.assertAlmostEqual(sum(inv.frequency(s) for s, _ in inv.counts), 1.0, places=9)
        self.assertGreater(inv.frequency("SX02"), inv.frequency("SX12"))

    def test_tokenize_skips_comments_and_commas(self) -> None:
        text = "# ignore\nA01, A02 A01\n\nB03\n"
        self.assertEqual(tokenize_signs(text), ["A01", "A02", "A01", "B03"])


class RepeatedSequenceTest(unittest.TestCase):
    def test_finds_repeated_bigrams_in_fixture(self) -> None:
        signs = load_sign_corpus(SYNTHETIC_CORPUS_PATH)
        repeats = find_repeated_sequences(signs, min_length=2, max_length=3, min_count=2)
        texts = {item.text: item for item in repeats}
        self.assertIn("SX02 SX03", texts)
        self.assertGreaterEqual(texts["SX02 SX03"].count, 5)
        self.assertGreaterEqual(len(texts["SX02 SX03"].positions), 2)
        # Positions must be increasing and point at the same n-gram.
        for item in repeats:
            self.assertEqual(sorted(item.positions), list(item.positions))
            for pos in item.positions:
                self.assertEqual(tuple(signs[pos : pos + len(item.sequence)]), item.sequence)

    def test_rejects_singleton_grams(self) -> None:
        signs = ["A", "B", "C", "A", "B"]
        repeats = find_repeated_sequences(signs, min_length=2, max_length=2, min_count=2)
        self.assertEqual([r.text for r in repeats], ["A B"])
        none = find_repeated_sequences(["A", "B", "C"], min_length=2, max_length=2, min_count=2)
        self.assertEqual(none, [])


class BilingualCribTest(unittest.TestCase):
    def test_correct_map_matches_synthetic_lexicon(self) -> None:
        data = load_synthetic_bilingual(SYNTHETIC_BILINGUAL_PATH)
        report = check_bilingual_crib(
            data["inscriptions"],
            data["sign_to_sound"],
            data["known_words"],
        )
        self.assertEqual(report.match_count, len(data["inscriptions"]))
        self.assertEqual(report.mismatch_count, 0)
        self.assertTrue(report.all_matched)
        readings = {m.reading for m in report.matches}
        self.assertEqual(readings, set(data["known_words"]))

    def test_wrong_map_is_rejected(self) -> None:
        data = load_synthetic_bilingual(SYNTHETIC_BILINGUAL_PATH)
        report = check_bilingual_crib(
            data["inscriptions"],
            data["wrong_sign_to_sound"],
            data["known_words"],
        )
        self.assertGreater(report.mismatch_count, 0)
        self.assertFalse(report.all_matched)
        # Flipping SX01 from ka→zu breaks every word that begins with SX01.
        broken = [m for m in report.mismatches if m.signs[0] == "SX01"]
        self.assertTrue(broken)
        for item in broken:
            self.assertTrue(item.reading.startswith("zu"))
            self.assertEqual(item.reason, "not_in_lexicon")

    def test_unmapped_sign_is_skipped(self) -> None:
        report = check_bilingual_crib(
            [["SX01", "MISSING"]],
            {"SX01": "ka"},
            ["ka"],
        )
        self.assertEqual(report.match_count, 0)
        self.assertEqual(report.mismatch_count, 0)
        self.assertEqual(len(report.skipped), 1)
        self.assertEqual(report.skipped[0].reason, "unmapped_sign")

    def test_fixture_files_are_utf8_and_present(self) -> None:
        corpus = (ROOT / "engine/data/synthetic_sign_corpus.txt").read_bytes()
        bilingual = (ROOT / "engine/data/synthetic_bilingual.json").read_bytes()
        self.assertFalse(corpus.startswith(b"\xff\xfe") or corpus.startswith(b"\xfe\xff"))
        self.assertIn(b"SX02", corpus)
        self.assertIn(b"katiru", bilingual)
        # Ensure we did not touch the hero JPEG path as part of this work.
        hero = ROOT / "docs/assets/readme-hero.jpg"
        self.assertTrue(hero.is_file())
        self.assertEqual(hero.read_bytes()[:3], bytes.fromhex("ffd8ff"))


if __name__ == "__main__":
    unittest.main()
