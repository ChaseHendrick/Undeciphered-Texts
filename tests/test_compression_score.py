"""Zlib language score: real prose must outrank a shuffle of itself.

Passing this file does not mean an ancient script was deciphered.
"""

from __future__ import annotations

import unittest
from collections import Counter
from pathlib import Path

from engine.compression_score import (
    DOES_NOT_DECIPHER,
    HONESTY_DE,
    ShuffleComparison,
    compare_to_shuffle,
    compressed_size,
    cross_entropy_bits_per_byte,
    language_score,
    shuffle_characters,
)
import engine.compression_score as compression_score

ROOT = Path(__file__).resolve().parents[1]
ENGLISH_PATH = ROOT / "engine" / "data" / "english.txt"
GERMAN_PATH = ROOT / "engine" / "data" / "german_excerpt.txt"


def _prose(path: Path) -> str:
    """Drop leading comment lines (the German fixture cites its source)."""
    kept: list[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.startswith("#"):
            continue
        kept.append(line)
    text = "\n".join(kept).strip()
    if len(text) < 200:
        raise AssertionError(f"fixture prose unexpectedly short: {path}")
    return text


class CompressionScoreTest(unittest.TestCase):
    def test_english_and_german_rank_above_a_shuffle(self) -> None:
        english = _prose(ENGLISH_PATH)
        german = _prose(GERMAN_PATH)
        self.assertIn("harbor", english.lower())
        # Umlauts from the Grimm excerpt must survive as UTF-8 text.
        self.assertTrue(any(ch in german for ch in "äöüßÄÖÜ"))

        for label, text in (("english", english), ("german", german)):
            for seed in (0, 1, 7):
                with self.subTest(language=label, seed=seed):
                    compared = compare_to_shuffle(text, seed=seed)
                    self.assertIsInstance(compared, ShuffleComparison)
                    self.assertGreater(compared.original_score, compared.shuffled_score)
                    self.assertTrue(compared.original_ranks_above)
                    self.assertLess(
                        compared.original_cross_entropy,
                        compared.shuffled_cross_entropy,
                    )
                    shuffled = shuffle_characters(text, seed=seed)
                    self.assertEqual(Counter(text), Counter(shuffled))
                    self.assertNotEqual(text, shuffled)
                    self.assertGreater(language_score(text), language_score(shuffled))
                    self.assertLess(
                        cross_entropy_bits_per_byte(text),
                        cross_entropy_bits_per_byte(shuffled),
                    )

    def test_score_matches_raw_over_compressed_size(self) -> None:
        text = _prose(ENGLISH_PATH)[:800]
        raw = text.encode("utf-8")
        self.assertEqual(language_score(text), len(raw) / compressed_size(text))
        self.assertAlmostEqual(
            cross_entropy_bits_per_byte(text),
            8.0 * compressed_size(text) / len(raw),
        )

    def test_empty_and_non_str_are_rejected(self) -> None:
        with self.assertRaises(ValueError):
            language_score("")
        with self.assertRaises(ValueError):
            cross_entropy_bits_per_byte("")
        with self.assertRaises(TypeError):
            language_score(b"not a str")  # type: ignore[arg-type]
        with self.assertRaises(ValueError):
            compressed_size("abc", level=10)

    def test_documents_that_it_does_not_decipher_ancient_scripts(self) -> None:
        blob = compression_score.__doc__ or ""
        self.assertIn("does not decipher ancient scripts", blob)
        self.assertIn("does not decipher ancient scripts", DOES_NOT_DECIPHER)
        self.assertIn("Voynich", DOES_NOT_DECIPHER)
        self.assertIn("Linear A", DOES_NOT_DECIPHER)
        self.assertIn("entziffert keine antiken Schriften", HONESTY_DE)
        self.assertIn(HONESTY_DE, blob)
        # The source file itself is UTF-8, not a mis-decoded byte string.
        source = Path(compression_score.__file__).read_text(encoding="utf-8")
        self.assertIn("entziffert keine antiken Schriften", source)
        self.assertIn("Schriften, nur ein Kompressionsmaß", source)


if __name__ == "__main__":
    unittest.main()
