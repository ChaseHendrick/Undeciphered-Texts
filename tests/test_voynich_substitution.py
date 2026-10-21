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

# The frozen cross-text calibration of 20 October 2026: cross plants from
# the second reference proeses (Frankenstein, Caesar's De Bello Gallico
# I-IV), scored under the first language's table. Cross plants converge
# to one value each; floors recompute the first artifact's values.
CROSS_ARTIFACT = (
    Path("docs/research-notes/voynich-substitution-crossband.json").resolve()
)
CROSS_REFERENCE_FACTS = {
    "english": {
        "file": "substref_english2_pg84.txt",
        "ebook": 84,
        "sha256": "7810cd483cffcf2cc8a1d8f0d5807931e69d4f48cd14149b8c76f88af82fead3",
        "processed_symbols": 407795,
        "space_share": 0.1847,
    },
    "latin": {
        "file": "substref_latin2_pg218.txt",
        "ebook": 218,
        "sha256": "84ac8411841a4d8f5f4a49b6a2cd1f466917c6a5af72916d5e0b2b1ecb2f659c",
        "processed_symbols": 143947,
        "space_share": 0.1428,
    },
}
CROSS_CELLS = {
    ("ZL", "english"): {"plant": -5.1603, "real": -5.2832,
                        "margin_cross": -0.1229, "verdict": "below-cross-band"},
    ("ZL", "latin"): {"plant": -5.1345, "real": -5.3162,
                      "margin_cross": -0.1817, "verdict": "below-cross-band"},
    ("GC", "english"): {"plant": -5.1646, "real": -5.3536,
                        "margin_cross": -0.189, "verdict": "below-cross-band"},
    ("GC", "latin"): {"plant": -5.1345, "real": -5.3883,
                      "margin_cross": -0.2538, "verdict": "below-cross-band"},
    ("IT", "english"): {"plant": -5.1603, "real": -5.2541,
                        "margin_cross": -0.0938, "verdict": "below-cross-band"},
    ("IT", "latin"): {"plant": -5.1345, "real": -5.2933,
                      "margin_cross": -0.1588, "verdict": "below-cross-band"},
}
CROSS_PLANT_LENGTH = {
    "english": {"ZL": 218663, "GC": 186708, "IT": 220532},
    "latin": {"ZL": 143947, "GC": 143947, "IT": 143947},
}

# The frozen widened band of 21 October 2026: the cross screen's own
# texts plus the declared second-wave members (Moby Dick and Le Morte
# D'Arthur under the English model; Vulgate Daniel, Colloquium
# heptaplomeres, and De Rariorum Animalium under the Latin model), five
# plants per text per cell, converged to one value each.
WIDENED_ARTIFACT = (
    Path("docs/research-notes/voynich-substitution-widened.json").resolve()
)
WIDENED_REFERENCE_FACTS = {
    "english": [
        {"file": "substref_english3_pg2701.txt", "ebook": 2701,
         "sha256": ("b5e88b71a1cda068e9ab1d94344c9d932338ba6da1a66"
                    "def97a1aecd9cfcc87d"),
         "processed_symbols": 1174300, "space_share": 0.1865},
        {"file": "substref_english4_pg1251.txt", "ebook": 1251,
         "sha256": ("5dae4564bb198fe0291956a681c556497ceed562de75f84a"
                    "82592032505c9fee"),
         "processed_symbols": 854142, "space_share": 0.1986},
    ],
    "latin": [
        {"file": "substref_latin3_pg828.txt", "ebook": 828,
         "sha256": ("7787b590956462f5d651b96f201e9caaaa8d4ea37034832c3"
                    "adc3119205aae1d"),
         "processed_symbols": 77572, "space_share": 0.1568},
        {"file": "substref_latin4_pg17859.txt", "ebook": 17859,
         "sha256": ("39b5e9363328e4e474f0a605cc6a7218a9a230121686edaa8"
                    "6cf3941e9eb7614"),
         "processed_symbols": 938855, "space_share": 0.1441},
        {"file": "substref_latin5_pg27655.txt", "ebook": 27655,
         "sha256": ("d4c7591a3985fa0162b3f4a3f856d72a94e18862b5cdaa0a4"
                    "0d9db8942d7bcda"),
         "processed_symbols": 77529, "space_share": 0.1512},
    ],
}
WIDENED_CELLS = {
    ("ZL", "english"): {
        "real": -5.2832,
        "plants": {"substref_english2_pg84.txt": -5.1603,
                   "substref_english3_pg2701.txt": -5.1893,
                   "substref_english4_pg1251.txt": -5.1004},
        "band_min": -5.1893,
        "floors": [-6.6139, -6.6068, -6.6075, -6.6105, -6.6072],
        "verdict": "below-widened-band",
    },
    ("ZL", "latin"): {
        "real": -5.3162,
        "plants": {"substref_latin2_pg218.txt": -5.1345,
                   "substref_latin3_pg828.txt": -5.1439,
                   "substref_latin4_pg17859.txt": -5.1682,
                   "substref_latin5_pg27655.txt": -5.2063},
        "band_min": -5.2063,
        "floors": [-6.4987, -6.5001, -6.5028, -6.4986, -6.4983],
        "verdict": "below-widened-band",
    },
    ("GC", "english"): {
        "real": -5.3536,
        "plants": {"substref_english2_pg84.txt": -5.1646,
                   "substref_english3_pg2701.txt": -5.1887,
                   "substref_english4_pg1251.txt": -5.1083},
        "band_min": -5.1887,
        "floors": [-6.5878, -6.5804, -6.5868, -6.5788, -6.5893],
        "verdict": "below-widened-band",
    },
    ("GC", "latin"): {
        "real": -5.3883,
        "plants": {"substref_latin2_pg218.txt": -5.1345,
                   "substref_latin3_pg828.txt": -5.1439,
                   "substref_latin4_pg17859.txt": -5.1662,
                   "substref_latin5_pg27655.txt": -5.2063},
        "band_min": -5.2063,
        "floors": [-6.5638, -6.5659, -6.5687, -6.5628, -6.5584],
        "verdict": "below-widened-band",
    },
    ("IT", "english"): {
        "real": -5.2541,
        "plants": {"substref_english2_pg84.txt": -5.1603,
                   "substref_english3_pg2701.txt": -5.1905,
                   "substref_english4_pg1251.txt": -5.0999},
        "band_min": -5.1905,
        "floors": [-6.5943, -6.5855, -6.5958, -6.5886, -6.5863],
        "verdict": "below-widened-band",
    },
    ("IT", "latin"): {
        "real": -5.2933,
        "plants": {"substref_latin2_pg218.txt": -5.1345,
                   "substref_latin3_pg828.txt": -5.1439,
                   "substref_latin4_pg17859.txt": -5.1683,
                   "substref_latin5_pg27655.txt": -5.2063},
        "band_min": -5.2063,
        "floors": [-6.4789, -6.474, -6.4814, -6.4869, -6.4866],
        "verdict": "below-widened-band",
    },
}
WIDENED_PLANT_LENGTHS = {
    "english": {"ZL": [218663, 218663, 218663],
                "GC": [186708, 186708, 186708],
                "IT": [220532, 220532, 220532]},
    "latin": {"ZL": [143947, 77572, 218663, 77529],
              "GC": [143947, 77572, 186708, 77529],
              "IT": [143947, 77572, 220532, 77529]},
}

# The frozen trigram resolution pass of 21 October 2026, declared after
# the widened band's six below-widened-band verdicts and before its own
# run: identical streams, machinery and mapped set, re-scored under the
# declared add-one trigram model of the first reference prose. Self
# plants restated the truncated-stream anchor exactly (30 of 30); Latin
# cross plants converged (within 0.0001); the English band's Moby Dick
# draws disclose search noise (stuck draws near the floors' region),
# recorded as measured and read in the log. The real text stands below
# every best-recovered member in all six cells.
TRIGRAM_ARTIFACT = (
    Path("docs/research-notes/voynich-substitution-trigram.json").resolve()
)
TRIGRAM_MODELS = {"english": -1.7939, "latin": -1.9243}
TRIGRAM_CELLS = {
    ("ZL", "english"): {
        "real": -3.0925, "counted": 218127, "anchor": -1.8109,
        "floors": [-3.4901, -3.4883, -3.4881, -3.4891, -3.4883],
        "band": {
            "substref_english2_pg84.txt": [-1.9327] * 5,
            "substref_english3_pg2701.txt": [
                -2.0449, -2.0449, -3.4296, -2.0449, -2.0449],
            "substref_english4_pg1251.txt": [-1.9337] * 5,
        },
        "gap_to_weakest_recovered": -1.0476,
        "verdict": "consistent-with-substitution",
        "margins": {"to_band_min": 0.3371, "to_band_max": -1.1598,
                    "to_floor": 0.3956},
    },
    ("ZL", "latin"): {
        "real": -2.8468, "counted": 218127, "anchor": -1.9129,
        "floors": [-3.4135, -3.4134, -3.4145, -3.4146, -3.4132],
        "band": {
            "substref_latin2_pg218.txt": [-2.0592] * 5,
            "substref_latin3_pg828.txt": [-2.0809] * 5,
            "substref_latin4_pg17859.txt": [-2.0676] * 5,
            "substref_latin5_pg27655.txt": [
                -2.1587, -2.1587, -2.1588, -2.1587, -2.1587],
        },
        "gap_to_weakest_recovered": -0.6881,
        "verdict": "below-trigram-band",
        "margins": {"to_band_min": -0.688, "to_band_max": -0.7876,
                    "to_floor": 0.5664},
    },
    ("GC", "english"): {
        "real": -2.9878, "counted": 175543, "anchor": -1.8146,
        "floors": [-3.5194, -3.5202, -3.5196, -3.5194, -3.5191],
        "band": {
            "substref_english2_pg84.txt": [
                -1.9358, -1.9358, -1.9358, -1.9358, -3.4309],
            "substref_english3_pg2701.txt": [
                -2.0487, -2.0487, -2.0487, -3.4271, -3.4272],
            "substref_english4_pg1251.txt": [-1.9398] * 5,
        },
        "gap_to_weakest_recovered": -0.9391,
        "verdict": "consistent-with-substitution",
        "margins": {"to_band_min": 0.4431, "to_band_max": -1.052,
                    "to_floor": 0.5313},
    },
    ("GC", "latin"): {
        "real": -2.9182, "counted": 175543, "anchor": -1.9138,
        "floors": [-3.4389, -3.4387, -3.4392, -3.4395, -3.4396],
        "band": {
            "substref_latin2_pg218.txt": [-2.0592] * 5,
            "substref_latin3_pg828.txt": [-2.0809] * 5,
            "substref_latin4_pg17859.txt": [-2.0687] * 5,
            "substref_latin5_pg27655.txt": [
                -2.1588, -2.1587, -2.1588, -2.1588, -2.1588],
        },
        "gap_to_weakest_recovered": -0.7595,
        "verdict": "below-trigram-band",
        "margins": {"to_band_min": -0.7594, "to_band_max": -0.859,
                    "to_floor": 0.5205},
    },
    ("IT", "english"): {
        "real": -3.121, "counted": 220530, "anchor": -1.8107,
        "floors": [-3.4849, -3.4855, -3.4843, -3.4853, -3.4851],
        "band": {
            "substref_english2_pg84.txt": [
                -3.4397, -1.9327, -1.9327, -1.9327, -1.9327],
            "substref_english3_pg2701.txt": [
                -2.0447, -3.4392, -2.0447, -2.0447, -3.4451],
            "substref_english4_pg1251.txt": [-1.9331] * 5,
        },
        "gap_to_weakest_recovered": -1.0763,
        "verdict": "consistent-with-substitution",
        "margins": {"to_band_min": 0.3241, "to_band_max": -1.1883,
                    "to_floor": 0.3633},
    },
    ("IT", "latin"): {
        "real": -2.6908, "counted": 220530, "anchor": -1.9127,
        "floors": [-3.4107, -3.4109, -3.4104, -3.4107, -3.4111],
        "band": {
            "substref_latin2_pg218.txt": [-2.0592] * 5,
            "substref_latin3_pg828.txt": [-2.0809] * 5,
            "substref_latin4_pg17859.txt": [-2.0677] * 5,
            "substref_latin5_pg27655.txt": [
                -2.1588, -2.1587, -2.1587, -2.1587, -2.1587],
        },
        "gap_to_weakest_recovered": -0.5321,
        "verdict": "below-trigram-band",
        "margins": {"to_band_min": -0.532, "to_band_max": -0.6316,
                    "to_floor": 0.7196},
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


class CrossBandTest(unittest.TestCase):
    """The declared cross-text calibration and its frozen measurement."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.first = json.loads(ARTIFACT.read_text())
        cls.artifact = json.loads(CROSS_ARTIFACT.read_text())

    def test_declared_cross_bookkeeping(self) -> None:
        declared = self.artifact["declared"]
        self.assertEqual(5, declared["cross_plants"])
        self.assertEqual(5, declared["cross_floors"])
        for language, facts in CROSS_REFERENCE_FACTS.items():
            stored = declared["cross_references"][language]
            self.assertEqual(facts["file"], stored["file"], language)
            self.assertEqual(facts["ebook"], stored["ebook"], language)
            self.assertEqual(facts["sha256"], stored["sha256"], language)
            self.assertEqual(facts["processed_symbols"],
                             stored["processed_symbols"], language)
            self.assertEqual(facts["space_share"], stored["space_share"],
                             language)

    def test_all_six_cells_below_the_cross_band(self) -> None:
        for (code, language), facts in sorted(CROSS_CELLS.items()):
            cell = self.artifact["files"][code][language]
            self.assertEqual(facts["real"], cell["real_best_mean_nats"],
                             f"{code}.{language} real")
            self.assertEqual(
                [facts["plant"]] * HEAD,
                cell["cross_plants_best_mean_nats"],
                f"{code}.{language} cross plant convergence",
            )
            # floors recompute the first artifact's values exactly
            self.assertEqual(
                self.first["files"][code][language]["floors_best_mean_nats"],
                cell["floors_best_mean_nats"],
                f"{code}.{language} floors reproduce the first artifact",
            )
            self.assertEqual(len(set(cell["plant_lengths"])), 1,
                             f"{code}.{language} plant length")
            self.assertEqual(
                CROSS_PLANT_LENGTH[language][code], cell["plant_lengths"][0],
                f"{code}.{language} plant length rule",
            )
            self.assertEqual(
                facts["verdict"], cell["verdict"], f"{code}.{language}"
            )
            self.assertAlmostEqual(
                facts["margin_cross"], cell["real_margin_to_cross_min"],
                places=9, msg=f"{code}.{language} cross margin",
            )
            self.assertLess(
                facts["real"], facts["plant"], f"{code}.{language} below band"
            )

    def test_cross_plant_cell_recomputes_from_the_declared_seed(self) -> None:
        sub._REAL_STREAMS.clear()
        try:
            stream = sub._real_stream("ZL")
            table, counts, _text = sub._reference("english")
            cross_stream = sub._reference_stream("english", cross=True)
            length = min(stream.total_events, len(cross_stream))
            self.assertEqual(length, CROSS_PLANT_LENGTH["english"]["ZL"])
            rng_perm = np.random.default_rng(
                sub._seed(sub.CELL_ID["ZL"], sub.KIND_ID["cross_perm"], 0, 0)
            )
            permutation = list(rng_perm.permutation(27))
            plant = np.array(
                [permutation[value] for value in cross_stream[:length]],
                dtype=np.int64,
            )
            matrix = sub._full_matrix(plant)
            rng_mach = np.random.default_rng(
                sub._seed(sub.CELL_ID["ZL"], sub.KIND_ID["cross_mach"], 0, 0)
            )
            value = round(
                sub.machinery_best(matrix, table, counts, rng_mach), 4
            )
            self.assertEqual(
                value, CROSS_CELLS[("ZL", "english")]["plant"],
                "ZL.english cross plant, seed holder 6 and 7",
            )
        finally:
            sub._REAL_STREAMS.clear()


class WidenedTest(unittest.TestCase):
    """The declared widened band and its frozen measurement."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.first = json.loads(ARTIFACT.read_text())
        cls.cross = json.loads(CROSS_ARTIFACT.read_text())
        cls.artifact = json.loads(WIDENED_ARTIFACT.read_text())

    def test_declared_widened_bookkeeping(self) -> None:
        declared = self.artifact["declared"]
        self.assertEqual(20261020, declared["base_seed"])
        self.assertEqual(5, declared["plants_per_text"])
        self.assertEqual(5, declared["floors"])
        self.assertEqual({"cross_screen": [6, 7], "widened": [10, 11]},
                         declared["seed_kinds"])
        self.assertEqual((sub.WIDENED_SEED_KINDS[0],
                          sub.WIDENED_SEED_KINDS[1]), (10, 11))
        for key in ("legacy_rule", "widened_scheme", "verdict_rule"):
            self.assertTrue(declared[key], key)
        self.assertIn("consistent-with-substitution", declared["verdict_rule"])
        self.assertIn("not-consistent", declared["verdict_rule"])
        self.assertIn("below-widened-band", declared["verdict_rule"])
        self.assertIn("below-widened-band", self.artifact["what"])

    def test_widened_reference_provenance(self) -> None:
        for language, additions in WIDENED_REFERENCE_FACTS.items():
            stored = self.artifact["declared"]["references"][language]
            # entry 0 is the cross screen's own text, sha-pinned already
            self.assertEqual(CROSS_REFERENCE_FACTS[language]["file"],
                             stored[0]["file"], language)
            self.assertEqual(len(additions) + 1, len(stored), language)
            for position, facts in enumerate(additions, start=1):
                entry = stored[position]
                self.assertEqual(facts["file"], entry["file"], language)
                self.assertEqual(facts["ebook"], entry["ebook"], language)
                self.assertEqual(facts["sha256"], entry["sha256"], language)
                self.assertEqual(facts["processed_symbols"],
                                 entry["processed_symbols"], language)
                self.assertEqual(facts["space_share"], entry["space_share"],
                                 language)
                self.assertTrue(entry["url"].endswith(
                    f"/pg{facts['ebook']}.txt"), language)

    def test_all_six_cells_stay_below_the_widened_band(self) -> None:
        for (code, language), facts in sorted(WIDENED_CELLS.items()):
            cell = self.artifact["files"][code][language]
            # the real and the floors reproduce the first artifact exactly
            self.assertEqual(
                self.first["files"][code][language]["real_best_mean_nats"],
                cell["real_best_mean_nats"],
                f"{code}.{language} real reproduces the first artifact",
            )
            self.assertEqual(
                self.first["files"][code][language]["floors_best_mean_nats"],
                cell["floors_best_mean_nats"],
                f"{code}.{language} floors reproduce the first artifact",
            )
            self.assertEqual(
                facts["floors"], cell["floors_best_mean_nats"],
                f"{code}.{language} floors frozen",
            )
            # band composition in declared order
            expected_files = ([CROSS_REFERENCE_FACTS[language]["file"]]
                              + [facts["file"] for facts
                                 in WIDENED_REFERENCE_FACTS[language]])
            self.assertEqual(
                expected_files, [entry["file"] for entry in cell["band"]],
                f"{code}.{language} band order",
            )
            converged = []
            for entry in cell["band"]:
                expected = facts["plants"][entry["file"]]
                self.assertEqual([expected] * HEAD, entry["plants"],
                                 f"{code}.{language} {entry['file']}")
                converged.append(expected)
            self.assertEqual(
                facts["band_min"], cell["band_min"],
                f"{code}.{language} band min stored",
            )
            self.assertEqual(
                facts["band_min"], min(converged),
                f"{code}.{language} band min is the weakest member",
            )
            # verdict recomputed from the declared rule
            real = cell["real_best_mean_nats"]
            floor_max = max(cell["floors_best_mean_nats"])
            if real >= cell["band_min"]:
                rule_verdict = "consistent-with-substitution"
            elif real <= floor_max:
                rule_verdict = "not-consistent"
            else:
                rule_verdict = "below-widened-band"
            self.assertEqual(rule_verdict, cell["verdict"],
                             f"{code}.{language} rule applied")
            self.assertEqual(facts["verdict"], cell["verdict"],
                             f"{code}.{language} frozen verdict")
            self.assertLess(real, facts["band_min"],
                            f"{code}.{language} real below the band")
            self.assertGreater(real, floor_max,
                               f"{code}.{language} real above the floors")
        # the verdict wording is the declared exact string everywhere
        for cell in self.artifact["files"].values():
            for language_cell in cell.values():
                self.assertEqual(
                    "below-widened-band", language_cell["verdict"],
                    f"{language_cell['real_best_mean_nats']} stayed "
                    "below-widened-band",
                )

    def test_plant_lengths_follow_the_declared_rule(self) -> None:
        for (code, language), facts in sorted(WIDENED_CELLS.items()):
            lengths = [
                entry["plant_length"]
                for entry in self.artifact["files"][code][language]["band"]
            ]
            self.assertEqual(
                WIDENED_PLANT_LENGTHS[language][code], lengths,
                f"{code}.{language} lengths frozen",
            )
        # the rule re-reads: length = min(the file's stream, the text)
        sub._REAL_STREAMS.clear()
        try:
            it_total = sub._real_stream("IT").total_events
            daniel = len(sub._reference_stream(
                "latin", file="substref_latin3_pg828.txt"))
            self.assertEqual(min(it_total, daniel),
                             WIDENED_PLANT_LENGTHS["latin"]["IT"][1],
                             "IT.latin Daniel length rule")
            gc_total = sub._real_stream("GC").total_events
            rariorum = len(sub._reference_stream(
                "latin", file="substref_latin5_pg27655.txt"))
            self.assertEqual(min(gc_total, rariorum),
                             WIDENED_PLANT_LENGTHS["latin"]["GC"][3],
                             "GC.latin Rariorum length rule")
        finally:
            sub._REAL_STREAMS.clear()

    def test_legacy_plants_reproduce_the_cross_artifact(self) -> None:
        for code, cell in self.artifact["files"].items():
            for language in ("english", "latin"):
                widened_entry = self.artifact["files"][code][language]["band"][0]
                cross_cell = self.cross["files"][code][language]
                self.assertEqual(
                    cross_cell["cross_plants_best_mean_nats"],
                    widened_entry["plants"],
                    f"{code}.{language} legacy plants replay",
                )
                self.assertEqual(
                    cross_cell["plant_lengths"][0],
                    widened_entry["plant_length"],
                    f"{code}.{language} legacy length replay",
                )

    def test_one_widened_cell_recomputes_from_the_declared_seeds(self) -> None:
        sub._REAL_STREAMS.clear()
        try:
            zl_total = sub._real_stream("ZL").total_events
            text_stream = sub._reference_stream(
                "latin", file="substref_latin4_pg17859.txt"
            )
            length = min(zl_total, len(text_stream))
            self.assertEqual(length, WIDENED_PLANT_LENGTHS["latin"]["ZL"][2])
            table, counts, _primary = sub._reference("latin")
            rng_perm = np.random.default_rng(
                sub._seed(sub.CELL_ID["ZL"], sub.WIDENED_SEED_KINDS[0],
                          sub.LANG_ID["latin"], 1)
            )
            rng_mach = np.random.default_rng(
                sub._seed(sub.CELL_ID["ZL"], sub.WIDENED_SEED_KINDS[1],
                          sub.LANG_ID["latin"], 1)
            )
            values = []
            for _index in range(5):
                permutation = list(rng_perm.permutation(27))
                plant = np.array(
                    [permutation[value] for value in text_stream[:length]],
                    dtype=np.int64,
                )
                matrix = sub._full_matrix(plant)
                values.append(
                    round(sub.machinery_best(matrix, table, counts, rng_mach),
                          4)
                )
            facts = WIDENED_CELLS[("ZL", "latin")]["plants"][
                "substref_latin4_pg17859.txt"
            ]
            self.assertEqual([facts] * 5, values,
                             "ZL.latin heptaplomeres, seed holders 10 and 11")
        finally:
            sub._REAL_STREAMS.clear()


class TrigramTest(unittest.TestCase):
    """The declared trigram resolution pass and its frozen measurement."""

    @classmethod
    def setUpClass(cls) -> None:
        cls.artifact = json.loads(TRIGRAM_ARTIFACT.read_text())

    def test_declared_trigram_bookkeeping(self) -> None:
        declared = self.artifact["declared"]
        self.assertEqual(20261020, declared["base_seed"])
        self.assertEqual(5, declared["plants_per_text"])
        self.assertEqual(5, declared["floors"])
        self.assertEqual(
            {"tri_plant": [12, 13], "tri_floor": [14, 15],
             "tri_cross": [16, 17]},
            declared["seed_kinds"],
        )
        for language, clean in TRIGRAM_MODELS.items():
            model = declared["models"][language]
            self.assertEqual(clean, model["clean_identity_mean_nats_per_trigram"],
                             language)
            self.assertEqual(model["ebook"],
                             REFERENCE_FACTS[language]["ebook"], language)
        self.assertIn("(n(first, second, third) + 1)",
                      declared["smoothing_rule"])
        self.assertIn("in plant order", declared["cross_scheme"])
        for phrase in ("consistent-with-substitution", "not-consistent",
                       "below-trigram-band"):
            self.assertIn(phrase, declared["verdict_rule"])
        self.assertIn("below-trigram-band", self.artifact["what"])

    def test_all_six_cells_match_the_frozen_trigram_measurement(self) -> None:
        for (code, language), facts in sorted(TRIGRAM_CELLS.items()):
            cell = self.artifact["files"][code][language]
            self.assertEqual(facts["real"], cell["real_best_mean_nats"],
                             f"{code}.{language} real")
            self.assertEqual(facts["counted"], cell["counted_trigrams"],
                             f"{code}.{language} counted trigrams")
            self.assertEqual(facts["anchor"],
                             cell["plant_parity_anchor_mean_nats"],
                             f"{code}.{language} anchor")
            self.assertEqual(facts["floors"], cell["floors_best_mean_nats"],
                             f"{code}.{language} floors")
            for key, key_name in (("to_band_min", "real_margin_to_band_min"),
                                  ("to_band_max", "real_margin_to_band_max"),
                                  ("to_floor", "real_margin_to_floor_max")):
                self.assertEqual(
                    facts["margins"][key], cell[key_name],
                    f"{code}.{language} margin {key}",
                )
            # the verdict recomputes per the declared rule
            real = cell["real_best_mean_nats"]
            plant_min = cell["band_min"]
            floor_max = max(cell["floors_best_mean_nats"])
            if real >= plant_min:
                rule_verdict = "consistent-with-substitution"
            elif real <= floor_max:
                rule_verdict = "not-consistent"
            else:
                rule_verdict = "below-trigram-band"
            self.assertEqual(rule_verdict, cell["verdict"],
                             f"{code}.{language} rule applied")
            self.assertEqual(facts["verdict"], cell["verdict"],
                             f"{code}.{language} frozen verdict")

    def test_self_plants_reach_the_declared_anchor_everywhere(self) -> None:
        for (code, language), facts in sorted(TRIGRAM_CELLS.items()):
            cell = self.artifact["files"][code][language]
            plants = cell["self_plants_best_mean_nats"]
            self.assertEqual([facts["anchor"]] * 5, plants,
                             f"{code}.{language} plant parity")
            self.assertEqual(facts["anchor"],
                             cell["plant_parity_anchor_mean_nats"],
                             f"{code}.{language} anchor")

    def test_band_members_match_their_frozen_draws(self) -> None:
        for (code, language), facts in sorted(TRIGRAM_CELLS.items()):
            stored = self.artifact["files"][code][language]["band"]
            self.assertEqual(facts["band"].keys(), {b["file"] for b in stored},
                             f"{code}.{language} band files")
            for entry in stored:
                self.assertEqual(facts["band"][entry["file"]], entry["plants"],
                                 f"{code}.{language} {entry['file']}")
                if language == "latin":
                    self.assertLessEqual(
                        max(entry["plants"]) - min(entry["plants"]), 0.0001,
                        f"{code}.{language} latin draws converge",
                    )
            # the central finding: below every best-recovered member
            recovered_min = min(max(entry["plants"]) for entry in stored)
            self.assertEqual(
                facts["gap_to_weakest_recovered"],
                round(real_of(self.artifact, code, language) - recovered_min,
                      4),
                f"{code}.{language} gap to the weakest recovered member",
            )
            self.assertLess(
                real_of(self.artifact, code, language), recovered_min,
                f"{code}.{language} real below every recovered member",
            )
            # and above the floors with the search noise disclosed
            self.assertGreater(
                real_of(self.artifact, code, language),
                max(self.artifact["files"][code][language]["floors_best_mean_nats"]),
                f"{code}.{language} real above the floors",
            )

    def test_one_trigram_real_cell_recomputes_from_the_declared_seed(self) -> None:
        sub._REAL_STREAMS.clear()
        try:
            stream = sub._real_stream("ZL")
            total = int(stream.total_events)
            scoped = np.full(total, -1, dtype=np.int64)
            scoped[stream.kept_mask] = stream.kept_ids
            codes, weights, _total = sub._tri_observed_masked(
                scoped, stream.kept_mask
            )
            logp, _clean, letter_counts = sub._reference_tri("english")
            rng = np.random.default_rng(
                sub._seed(sub.CELL_ID["ZL"], sub.KIND_ID["real"], 0, 0)
            )
            value = round(
                sub.machinery_best_tri(
                    codes, weights, logp, letter_counts, rng
                ),
                4,
            )
            self.assertEqual(
                TRIGRAM_CELLS[("ZL", "english")]["real"], value,
                "ZL.english trigram real, seed kind 1",
            )
        finally:
            sub._REAL_STREAMS.clear()

    def test_one_trigram_band_entry_recomputes_from_the_declared_seeds(self) -> None:
        sub._REAL_STREAMS.clear()
        try:
            total = int(sub._real_stream("ZL").total_events)
            text_stream = sub._reference_stream(
                "english", file="substref_english3_pg2701.txt"
            )
            length = min(total, len(text_stream))
            logp, _clean, letter_counts = sub._reference_tri("english")
            rng_perm = np.random.default_rng(
                sub._seed(sub.CELL_ID["ZL"], sub.KIND_ID["tri_cross_perm"],
                          sub.LANG_ID["english"], 1)
            )
            rng_mach = np.random.default_rng(
                sub._seed(sub.CELL_ID["ZL"], sub.KIND_ID["tri_cross_mach"],
                          sub.LANG_ID["english"], 1)
            )
            values = []
            for _index in range(5):
                permutation = list(rng_perm.permutation(27))
                plant = np.array(
                    [permutation[value] for value in text_stream[:length]],
                    dtype=np.int64,
                )
                codes, weights, _total = sub._tri_observed_full(plant)
                values.append(round(sub.machinery_best_tri(
                    codes, weights, logp, letter_counts, rng_mach
                ), 4))
            facts = TRIGRAM_CELLS[("ZL", "english")]["band"][
                "substref_english3_pg2701.txt"
            ]
            self.assertEqual(facts, values,
                             "ZL.english Moby Dick, seed holders 16 and 17")
        finally:
            sub._REAL_STREAMS.clear()


def real_of(artifact, code, language) -> float:
    """The stored real statistic of one cell."""
    return artifact["files"][code][language]["real_best_mean_nats"]


if __name__ == "__main__":
    unittest.main()
