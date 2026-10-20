"""Tests for the declared substitution screen of Voynich family 4.

The artifact pins the frozen measurement; the reproducibility tests
recompute stored cells from the declared seeds; the machinery tests nail
down the mapping search on synthetic languages: a planted substitution
must reach parity with its own decoding, a destroyed-adjacency stream
must fall far below, and the search must be invariant to the glyph
labels it receives. Nothing here reads the manuscript.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import numpy as np

from engine import voynich_substitution as sub

ARTIFACT = Path("docs/research-notes/voynich-substitution-screen.json").resolve()
HEAD = 5

# The frozen measurement of 20 October 2026, after the declared stream
# design (boundary between every two adjacent words). Real best mean
# nats per counted pair, the plant band, the floor band, and the verdict
# the declared rule emitted, per (file, language).
FROZEN = {
    ("ZL", "english"): {
        "real": -5.2832,
        "plant": -5.1422,
        "floors": [-6.6139, -6.6068, -6.6075, -6.6105, -6.6072],
        "margin_floor": 1.3236,
        "margin_plant": -0.141,
        "verdict": "indeterminate",
    },
    ("ZL", "latin"): {
        "real": -5.3162,
        "plant": -5.0742,
        "floors": [-6.4987, -6.5001, -6.5028, -6.4986, -6.4983],
        "margin_floor": 1.1821,
        "margin_plant": -0.242,
        "verdict": "indeterminate",
    },
    ("GC", "english"): {
        "real": -5.3536,
        "plant": -5.143,
        "floors": [-6.5878, -6.5804, -6.5868, -6.5788, -6.5893],
        "margin_floor": 1.2252,
        "margin_plant": -0.2106,
        "verdict": "indeterminate",
    },
    ("GC", "latin"): {
        "real": -5.3883,
        "plant": -5.0743,
        "floors": [-6.5638, -6.5659, -6.5687, -6.5628, -6.5584],
        "margin_floor": 1.1701,
        "margin_plant": -0.314,
        "verdict": "indeterminate",
    },
    ("IT", "english"): {
        "real": -5.2541,
        "plant": -5.1422,
        "floors": [-6.5943, -6.5855, -6.5958, -6.5886, -6.5863],
        "margin_floor": 1.3314,
        "margin_plant": -0.1119,
        "verdict": "indeterminate",
    },
    ("IT", "latin"): {
        "real": -5.2933,
        "plant": -5.074,
        "floors": [-6.4789, -6.474, -6.4814, -6.4869, -6.4866],
        "margin_floor": 1.1807,
        "margin_plant": -0.2193,
        "verdict": "indeterminate",
    },
}

STREAM_FACTS = {
    "ZL": {"word_count": 34354, "total_events": 218663, "kept_events": 218473,
           "kept_share": 0.9991, "boundary_share": 0.1571},
    "GC": {"word_count": 36232, "total_events": 186708, "kept_events": 182887,
           "kept_share": 0.9795, "boundary_share": 0.1941},
    "IT": {"word_count": 36441, "total_events": 220532, "kept_events": 220532,
           "kept_share": 1.0, "boundary_share": 0.1652},
}

REFERENCE_FACTS = {
    "english": {
        "file": "substref_english_pg1342.txt",
        "ebook": 1342,
        "sha256": "3f6bb9d6f78e0293b56acd4714dd68cb7d6d1d293402031ce9d5a216bcaf9d75",
        "processed_symbols": 692537,
        "space_share": 0.1857,
    },
    "latin": {
        "file": "substref_latin_pg33849.txt",
        "ebook": 33849,
        "sha256": "30287aab673c861ae500f06fe55d4396f529a0c251b37178e7220b6c51317189",
        "processed_symbols": 858522,
        "space_share": 0.1581,
    },
}

ZL_MAPPED = (
    "oehyacdiklrstnqpmfg?'xbv" + chr(0x184) + chr(0x185) + sub.BOUNDARY
)


class ArtifactTest(unittest.TestCase):
    """The frozen measurement and its declared bookkeeping."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.artifact = json.loads(ARTIFACT.read_text())

    def test_declared_facts_are_frozen(self) -> None:
        declared = self.artifact["declared"]
        self.assertEqual(20261020, declared["base_seed"])
        self.assertEqual(26, declared["mapped_letters"])
        self.assertEqual(16, declared["restarts"])
        self.assertEqual(200, declared["sweep_cap"])
        self.assertEqual(5, declared["plants"])
        self.assertEqual(5, declared["floors"])
        self.assertTrue(declared["reserved_folios_excluded"])
        self.assertIn("consistent-with-substitution", declared["verdict_rule"])
        self.assertIn("not-consistent", declared["verdict_rule"])

    def test_reference_provenance_is_frozen(self) -> None:
        for language, facts in REFERENCE_FACTS.items():
            stored = self.artifact["declared"]["references"][language]
            self.assertEqual(facts["file"], stored["file"], language)
            self.assertEqual(facts["ebook"], stored["ebook"], language)
            self.assertEqual(facts["sha256"], stored["sha256"], language)
            self.assertEqual(facts["processed_symbols"],
                             stored["processed_symbols"], language)
            self.assertEqual(facts["space_share"], stored["space_share"],
                             language)

    def test_stream_facts_are_frozen(self) -> None:
        for code, facts in STREAM_FACTS.items():
            stream = self.artifact["files"][code]["stream"]
            self.assertEqual(facts["word_count"], stream["word_count"], code)
            self.assertEqual(facts["total_events"], stream["total_events"], code)
            self.assertEqual(facts["kept_events"], stream["kept_events"], code)
            self.assertEqual(facts["kept_share"], stream["kept_share"], code)
            self.assertEqual(facts["boundary_share"], stream["boundary_share"],
                             code)

    def test_all_six_cells_match_the_frozen_measurement(self) -> None:
        for (code, language), facts in sorted(FROZEN.items()):
            cell = self.artifact["files"][code][language]
            self.assertEqual(facts["real"], cell["real_best_mean_nats"],
                             f"{code}.{language}")
            self.assertEqual([facts["plant"]] * HEAD,
                             cell["plants_best_mean_nats"],
                             f"{code}.{language} plants")
            self.assertEqual(facts["floors"], cell["floors_best_mean_nats"],
                             f"{code}.{language} floors")
            self.assertAlmostEqual(
                facts["margin_floor"], cell["real_margin_to_floor_max"],
                places=9, msg=f"{code}.{language} floor margin",
            )
            self.assertAlmostEqual(
                facts["margin_plant"], cell["real_margin_to_plant_min"],
                places=9, msg=f"{code}.{language} plant margin",
            )
            self.assertEqual(facts["verdict"], cell["verdict"],
                             f"{code}.{language} verdict")
            # every plant converges to one value and floors stay below it
            self.assertEqual(
                len(set(cell["plants_best_mean_nats"])), 1,
                f"{code}.{language} plant convergence",
            )
            self.assertTrue(
                min(cell["plants_best_mean_nats"])
                > max(cell["floors_best_mean_nats"]),
                f"{code}.{language} band separation",
            )


class ReproducibilityTest(unittest.TestCase):
    """Stored cells recompute exactly from the declared seeds."""

    @classmethod
    def setUpClass(cls) -> None:
        sub._REAL_STREAMS.clear()

    @classmethod
    def tearDownClass(cls) -> None:
        sub._REAL_STREAMS.clear()

    def test_streams_recompute_the_declared_facts(self) -> None:
        for code, facts in STREAM_FACTS.items():
            stream = sub._real_stream(code)
            self.assertEqual(facts["word_count"], stream.word_count, code)
            self.assertEqual(facts["total_events"], stream.total_events, code)
            self.assertEqual(facts["kept_events"], int(stream.kept_ids.size),
                             code)
        self.assertEqual(
            tuple(ZL_MAPPED), sub._real_stream("ZL").mapped_chars,
            "ZL mapped glyphs, most frequent first, then the boundary mark",
        )

    def _recompute(self, code: str, language: str) -> float:
        stream = sub._real_stream(code)
        table, counts, _text = sub._reference(language)
        scoped = np.full(stream.total_events, -1, dtype=np.int64)
        scoped[stream.kept_mask] = stream.kept_ids
        matrix = sub._count_matrix(scoped, stream.kept_mask)
        rng = np.random.default_rng(
            sub._seed(sub.CELL_ID[code], sub.KIND_ID["real"],
                      sub.LANG_ID[language], 0)
        )
        return sub.machinery_best(matrix, table, counts, rng)

    def test_stored_real_cells_recompute_exactly(self) -> None:
        for code, language in (("ZL", "english"), ("IT", "latin")):
            facts = FROZEN[(code, language)]
            value = round(self._recompute(code, language), 4)
            self.assertEqual(value, facts["real"], f"{code}.{language}")

    def test_stored_bests_survive_more_restarts(self) -> None:
        """Adequacy control: more restarts must not beat the frozen best."""
        for code, language in (("ZL", "english"), ("GC", "latin")):
            stream = sub._real_stream(code)
            table, counts, _text = sub._reference(language)
            scoped = np.full(stream.total_events, -1, dtype=np.int64)
            scoped[stream.kept_mask] = stream.kept_ids
            matrix = sub._count_matrix(scoped, stream.kept_mask)
            rng = np.random.default_rng(
                sub._seed(sub.CELL_ID[code], sub.KIND_ID["real"],
                          sub.LANG_ID[language], 0)
            )
            wider = sub.machinery_best(matrix, table, counts, rng, restarts=48)
            stored = FROZEN[(code, language)]["real"]
            self.assertLessEqual(
                wider, stored + 1e-4, f"{code}.{language} adequacy",
            )


class MachineryTest(unittest.TestCase):
    """The mapping search, pinned on synthetic languages."""

    RESTARTS = 12

    @classmethod
    def setUpClass(cls) -> None:
        rng = np.random.default_rng(20261020)
        vocabulary = [
            "the", "king", "queen", "gave", "bread", "told", "them", "under",
            "the", "old", "wall", "and", "went", "over", "it", "with", "bags",
            "of", "grain", "till", "the", "sun", "fell", "then", "ate", "the",
            "bread", "in", "the", "rain", "and", "they", "came", "at", "the",
            "hour", "when", "the", "land", "was", "still", "so", "the", "men",
            "stood", "in", "the", "field", "till", "the", "light", "grew",
        ]
        cls.reference_ids: list[int] = []
        while len(cls.reference_ids) < 24000:
            for _word in range(6):
                word = vocabulary[rng.integers(len(vocabulary))]
                for char in word:
                    cls.reference_ids.append(ord(char) - 97)
                cls.reference_ids.append(26)
        cls.table, cls.counts = sub.table_from_stream(cls.reference_ids)

    def _plant(self, seed: int) -> tuple[np.ndarray, float]:
        rng = np.random.default_rng([20261020, seed])
        permutation = rng.permutation(27)
        plant = np.array(
            [permutation[value] for value in self.reference_ids],
            dtype=np.int64,
        )
        true_decode = np.argsort(permutation)
        matrix = sub._full_matrix(plant)
        true_score = sub._score(matrix, self.table, true_decode) / matrix.sum()
        return matrix, true_score

    def test_planted_substitution_reaches_parity(self) -> None:
        for seed in (0, 1):
            matrix, true_score = self._plant(seed)
            rng = np.random.default_rng([20261020, 100 + seed])
            best = sub.machinery_best(
                matrix, self.table, self.counts, rng,
                restarts=self.RESTARTS,
            )
            self.assertGreaterEqual(best, true_score - 1e-9, f"seed {seed}")
            self.assertLessEqual(
                best, true_score + 0.05, f"seed {seed} overrecover",
            )

    def test_destroyed_adjacency_falls_far_below_parity(self) -> None:
        stream = self.reference_ids
        rng_perm = np.random.default_rng([20261020, 202])
        permutation = rng_perm.permutation(27)
        plant = np.array(
            [permutation[value] for value in stream], dtype=np.int64,
        )
        matrix = sub._full_matrix(plant)
        true_decode = np.argsort(permutation)
        true_score = sub._score(matrix, self.table, true_decode) / matrix.sum()
        rng_mach = np.random.default_rng([20261020, 102])
        best = sub.machinery_best(
            matrix, self.table, self.counts, rng_mach, restarts=self.RESTARTS,
        )
        shuffled = plant.copy()
        np.random.default_rng([20261020, 302]).shuffle(shuffled)
        floor_matrix = sub._full_matrix(shuffled)
        floor = sub.machinery_best(
            floor_matrix, self.table, self.counts,
            np.random.default_rng([20261020, 402]),
            restarts=self.RESTARTS,
        )
        self.assertGreaterEqual(best, true_score - 1e-9, "parity plant")
        self.assertGreaterEqual(
            best - floor, 1.0, "plant must sit far above its destroyed floor",
        )

    def test_machinery_is_invariant_to_glyph_labels(self) -> None:
        matrix, _true_score = self._plant(3)
        rng = np.random.default_rng([20261020, 103])
        best = sub.machinery_best(
            matrix, self.table, self.counts, rng, restarts=self.RESTARTS,
        )
        relabel = np.random.default_rng([20261020, 203]).permutation(27)
        relabeled = matrix[np.ix_(relabel, relabel)]
        again = sub.machinery_best(
            relabeled, self.table, self.counts,
            np.random.default_rng([20261020, 103]),
            restarts=self.RESTARTS,
        )
        self.assertAlmostEqual(best, again, places=6)


if __name__ == "__main__":
    unittest.main()
