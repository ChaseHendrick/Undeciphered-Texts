"""Tests for the declared held-out homophonic screen of family 5.

The artifact pins the frozen measurement; the reproducibility tests
recompute the real's held-out value and one band member's first draw
from the declared seeds; the machinery tests nail the declared exact
rule: the candidate evaluation is exact against brute force, the split
shares no positions between its halves and consumes no seed, the
planted anchor algebra carries the true configuration's score-half
identity, and the held-out assignment selection reads no score-half
data. Nothing here reads the manuscript beyond the frozen artifact.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path
from typing import NamedTuple

import numpy as np

import engine.voynich_homophonic as homo
from engine import voynich_substitution as sub

ARTIFACT = Path(
    "docs/research-notes/voynich-homophonic-heldout.json"
).resolve()
SCREEN = Path(
    "docs/research-notes/voynich-homophonic-screen.json"
).resolve()


class Band(NamedTuple):
    """One frozen band member of the held-out measurement."""

    file: str
    ebook: int
    plant_length: int
    anchor: float
    anchor_climb: float
    draws: list
    draws_climb: list
    draws_full: list
    selected: int
    best: float
    spread: float


class Cell(NamedTuple):
    """One frozen (file, language) cell of the held-out measurement."""

    real_held: float
    real_climb: float
    real_full: float
    counted: int
    climb_pairs: int
    score_pairs: int
    anchor: float
    anchor_climb: float
    plants_held: list
    plants_full: list
    excesses: list
    floors_held: list
    floors_full: list
    band_min: float
    band_max: float
    margin_to_band: float
    margin_to_floor: float
    verdict: str
    band: list


# The frozen measurement of 21 October 2026, filled from the artifact
# produced by the declared run: every verdict stayed
# consistent-with-substitution under the repaired exact rule and the
# held-out split, so the declared exclusion format excluded nothing and
# the family stays open exactly as the disclosure demands.
FROZEN = {
    ("ZL", "english"): Cell(
        -4.4252, -4.4313, -4.4437,
        218415, 109208, 109207,
        -5.143, -5.1415,
        [-4.6625, -4.7236, -4.7041, -4.7236, -4.7236],
        [-4.7411, -4.7256, -4.6595, -4.7256, -4.7256],
        [0.4805, 0.4194, 0.4389, 0.4194, 0.4194],
        [-5.2324, -5.2375, -5.2334, -5.2336, -5.2354],
        [-5.2291, -5.2276, -5.2309, -5.2264, -5.2307],
        -4.6997, -4.6712,
        0.2745, 0.8072,
        "consistent-with-substitution",
        [
            Band("substref_english2_pg84.txt", 84, 218663,
                 -5.1585, -5.1621,
                 [-4.738, -4.738, -4.738, -4.6992, -4.6992],
                 [-4.7379, -4.7379, -4.7379, -4.7003, -4.7003],
                 [-4.6997, -4.6997, -4.738, -4.738, -4.6997],
                 3, -4.6992, 0.0388),
            Band("substref_english3_pg2701.txt", 2701, 218663,
                 -5.1885, -5.1902,
                 [-4.6997, -4.6997, -4.6997, -4.6997, -4.6997],
                 [-4.7025, -4.7025, -4.7025, -4.7025, -4.7025],
                 [-4.7011, -4.7011, -4.7011, -4.7011, -4.7011],
                 0, -4.6997, 0.0),
            Band("substref_english4_pg1251.txt", 1251, 218663,
                 -5.0993, -5.1016,
                 [-4.6712, -4.6708, -4.6708, -4.6708, -4.6708],
                 [-4.668, -4.67, -4.67, -4.67, -4.67],
                 [-4.6699, -4.6699, -4.6699, -4.6699, -4.6699],
                 0, -4.6712, 0.0004),
        ],
    ),
    ("ZL", "latin"): Cell(
        -4.3743, -4.3826, -4.3784,
        218415, 109208, 109207,
        -5.0755, -5.0729,
        [-4.5771, -4.5771, -4.5771, -4.5775, -4.5771],
        [-4.5764, -4.5764, -4.5764, -4.5772, -4.5764],
        [0.4984, 0.4984, 0.4984, 0.498, 0.4984],
        [-5.1764, -5.171, -5.1741, -5.1744, -5.1707],
        [-5.1664, -5.167, -5.1682, -5.1673, -5.1667],
        -4.6081, -4.5788,
        0.2338, 0.7964,
        "consistent-with-substitution",
        [
            Band("substref_latin2_pg218.txt", 218, 143947,
                 -5.1338, -5.1351,
                 [-4.6063, -4.6081, -4.6081, -4.6081, -4.6081],
                 [-4.6074, -4.6066, -4.6066, -4.6066, -4.6066],
                 [-4.6068, -4.6068, -4.6074, -4.6068, -4.6068],
                 1, -4.6081, 0.0018),
            Band("substref_latin3_pg828.txt", 828, 77572,
                 -5.1465, -5.1453,
                 [-4.583, -4.583, -4.5816, -4.583, -4.583],
                 [-4.5905, -4.5905, -4.5832, -4.5905, -4.5905],
                 [-4.5867, -4.5867, -4.5867, -4.5867, -4.5867],
                 2, -4.5816, 0.0014),
            Band("substref_latin4_pg17859.txt", 17859, 218663,
                 -5.1684, -5.1686,
                 [-4.6068, -4.6068, -4.6068, -4.6068, -4.6068],
                 [-4.6036, -4.6036, -4.6036, -4.6036, -4.6036],
                 [-4.6052, -4.6052, -4.6052, -4.6052, -4.6052],
                 0, -4.6068, 0.0),
            Band("substref_latin5_pg27655.txt", 27655, 77529,
                 -5.2038, -5.2106,
                 [-4.5788, -4.5788, -4.5788, -4.5788, -4.5788],
                 [-4.5978, -4.5978, -4.5978, -4.5978, -4.5978],
                 [-4.5883, -4.5883, -4.5883, -4.5883, -4.5883],
                 0, -4.5788, 0.0),
        ],
    ),
    ("GC", "english"): Cell(
        -4.3534, -4.353, -4.3527,
        183199, 91600, 91599,
        -5.1444, -5.1415,
        [-4.7256, -4.6627, -4.6627, -4.6627, -4.6609],
        [-4.7271, -4.6592, -4.6592, -4.6592, -4.6592],
        [0.4188, 0.4817, 0.4817, 0.4817, 0.4835],
        [-5.2356, -5.2389, -5.2334, -5.2321, -5.2378],
        [-5.2251, -5.2302, -5.2242, -5.2253, -5.2275],
        -4.6989, -4.6362,
        0.3455, 0.8787,
        "consistent-with-substitution",
        [
            Band("substref_english2_pg84.txt", 84, 186708,
                 -5.1627, -5.1665,
                 [-4.7278, -4.7278, -4.6989, -4.6989, -4.6989],
                 [-4.731, -4.731, -4.7024, -4.7024, -4.7024],
                 [-4.7294, -4.7294, -4.7004, -4.7294, -4.7294],
                 2, -4.6989, 0.0289),
            Band("substref_english3_pg2701.txt", 2701, 186708,
                 -5.1878, -5.1896,
                 [-4.6362, -4.7556, -4.7, -4.6362, -4.7],
                 [-4.639, -4.7508, -4.7042, -4.639, -4.7042],
                 [-4.7521, -4.7021, -4.7021, -4.7521, -4.7021],
                 0, -4.6362, 0.1194),
            Band("substref_english4_pg1251.txt", 1251, 186708,
                 -5.1067, -5.1099,
                 [-4.6729, -4.6688, -4.6688, -4.6688, -4.6729],
                 [-4.6711, -4.6691, -4.6691, -4.6691, -4.6711],
                 [-4.6711, -4.6715, -4.6715, -4.6715, -4.6715],
                 1, -4.6688, 0.0041),
        ],
    ),
    ("GC", "latin"): Cell(
        -4.4318, -4.4276, -4.3896,
        183199, 91600, 91599,
        -5.076, -5.0726,
        [-4.5776, -4.5774, -4.5774, -4.5774, -4.5774],
        [-4.5761, -4.5761, -4.5761, -4.5761, -4.5761],
        [0.4984, 0.4986, 0.4986, 0.4986, 0.4986],
        [-5.1725, -5.1719, -5.1745, -5.1677, -5.1796],
        [-5.1599, -5.1632, -5.1608, -5.161, -5.1584],
        -4.6081, -4.5788,
        0.1763, 0.7359,
        "consistent-with-substitution",
        [
            Band("substref_latin2_pg218.txt", 218, 143947,
                 -5.1338, -5.1351,
                 [-4.6081, -4.6081, -4.6081, -4.6063, -4.6081],
                 [-4.6066, -4.6066, -4.6066, -4.6074, -4.6066],
                 [-4.6074, -4.6068, -4.6074, -4.6068, -4.6068],
                 0, -4.6081, 0.0018),
            Band("substref_latin3_pg828.txt", 828, 77572,
                 -5.1465, -5.1453,
                 [-4.583, -4.5816, -4.5816, -4.5816, -4.583],
                 [-4.5905, -4.5832, -4.5832, -4.5832, -4.5905],
                 [-4.5867, -4.5867, -4.5867, -4.5804, -4.5867],
                 1, -4.5816, 0.0014),
            Band("substref_latin4_pg17859.txt", 17859, 186708,
                 -5.1659, -5.167,
                 [-4.605, -4.605, -4.605, -4.605, -4.5974],
                 [-4.6037, -4.6037, -4.6037, -4.6037, -4.5968],
                 [-4.6044, -4.6044, -4.5971, -4.6044, -4.5971],
                 4, -4.5974, 0.0076),
            Band("substref_latin5_pg27655.txt", 27655, 77529,
                 -5.2038, -5.2106,
                 [-4.5788, -4.5788, -4.5788, -4.5788, -4.5788],
                 [-4.5978, -4.5978, -4.5978, -4.5978, -4.5978],
                 [-4.5883, -4.5883, -4.5883, -4.5883, -4.5883],
                 0, -4.5788, 0.0),
        ],
    ),
    ("IT", "english"): Cell(
        -4.3878, -4.3912, -4.3895,
        220531, 110266, 110265,
        -5.1431, -5.1414,
        [-4.7482, -4.7234, -4.7425, -4.7496, -4.7521],
        [-4.7477, -4.726, -4.7412, -4.7488, -4.7488],
        [0.3949, 0.4197, 0.4006, 0.3935, 0.391],
        [-5.2295, -5.2376, -5.2285, -5.2354, -5.229],
        [-5.2296, -5.2293, -5.2261, -5.2307, -5.2262],
        -4.6992, -4.6354,
        0.3114, 0.8407,
        "consistent-with-substitution",
        [
            Band("substref_english2_pg84.txt", 84, 220532,
                 -5.1588, -5.1618,
                 [-4.6992, -4.7378, -4.7378, -4.6992, -4.7378],
                 [-4.7002, -4.7376, -4.7376, -4.7002, -4.7376],
                 [-4.6997, -4.7377, -4.7377, -4.6997, -4.7377],
                 0, -4.6992, 0.0386),
            Band("substref_english3_pg2701.txt", 2701, 220532,
                 -5.1894, -5.1916,
                 [-4.6998, -4.6354, -4.6998, -4.6354, -4.6354],
                 [-4.7028, -4.6391, -4.7028, -4.6391, -4.6391],
                 [-4.6373, -4.6373, -4.7013, -4.6373, -4.7013],
                 1, -4.6354, 0.0644),
            Band("substref_english4_pg1251.txt", 1251, 220532,
                 -5.0985, -5.1012,
                 [-4.6713, -4.6713, -4.6713, -4.6713, -4.6713],
                 [-4.6678, -4.6678, -4.6678, -4.6678, -4.6678],
                 [-4.6691, -4.6691, -4.6691, -4.6691, -4.6691],
                 0, -4.6713, 0.0),
        ],
    ),
    ("IT", "latin"): Cell(
        -4.3707, -4.3756, -4.3732,
        220531, 110266, 110265,
        -5.0753, -5.0727,
        [-4.577, -4.577, -4.5986, -4.577, -4.577],
        [-4.5765, -4.5765, -4.5765, -4.5765, -4.5765],
        [0.4983, 0.4983, 0.4767, 0.4983, 0.4983],
        [-5.1749, -5.1703, -5.1808, -5.167, -5.1766],
        [-5.1642, -5.1667, -5.1668, -5.1643, -5.168],
        -4.6081, -4.5788,
        0.2374, 0.7963,
        "consistent-with-substitution",
        [
            Band("substref_latin2_pg218.txt", 218, 143947,
                 -5.1338, -5.1351,
                 [-4.6081, -4.6081, -4.6081, -4.6063, -4.6063],
                 [-4.6066, -4.6066, -4.6066, -4.6074, -4.6074],
                 [-4.6074, -4.6074, -4.6074, -4.6068, -4.6068],
                 0, -4.6081, 0.0018),
            Band("substref_latin3_pg828.txt", 828, 77572,
                 -5.1465, -5.1453,
                 [-4.5816, -4.5816, -4.5816, -4.5816, -4.5816],
                 [-4.5832, -4.5832, -4.5832, -4.5832, -4.5832],
                 [-4.5804, -4.5804, -4.5804, -4.5804, -4.5804],
                 0, -4.5816, 0.0),
            Band("substref_latin4_pg17859.txt", 17859, 220532,
                 -5.1682, -5.1688,
                 [-4.6064, -4.6064, -4.6064, -4.6064, -4.6064],
                 [-4.6038, -4.6038, -4.6038, -4.6038, -4.6038],
                 [-4.6051, -4.6051, -4.6051, -4.6051, -4.6051],
                 0, -4.6064, 0.0),
            Band("substref_latin5_pg27655.txt", 27655, 77529,
                 -5.2038, -5.2106,
                 [-4.5788, -4.5788, -4.5788, -4.5788, -4.5788],
                 [-4.5978, -4.5978, -4.5978, -4.5978, -4.5978],
                 [-4.5883, -4.5883, -4.5883, -4.5883, -4.5883],
                 0, -4.5788, 0.0),
        ],
    ),
}

MODELS = {
    "english": ("substref_english_pg1342.txt", 1342, -5.1311,
                -5.1314, -5.1309),
    "latin": ("substref_latin_pg33849.txt", 33849, -5.0999,
              -5.0979, -5.1019),
}

DEMO = ("ZL", "english")


def band_expected(band: list) -> list:
    """The frozen band members in the artifact's stored shape."""
    members = []
    for entry in band:
        members.append({
            "file": entry.file,
            "ebook": entry.ebook,
            "plant_length": entry.plant_length,
            "anchor": entry.anchor,
            "anchor_climb": entry.anchor_climb,
            "draws": entry.draws,
            "draws_climb": entry.draws_climb,
            "draws_full": entry.draws_full,
            "draw_sweep_budget_hits": [False] * 5,
            "draw_full_sweep_budget_hits": [False] * 5,
            "selected_draw_index": entry.selected,
            "recovered_best": entry.best,
            "spread": entry.spread,
        })
    return members


class DeclaredBookkeepingTest(unittest.TestCase):
    """The declared constants and rule strings, pinned against both
    the module and the artifact."""

    def test_declared_inherited_constants(self) -> None:
        self.assertEqual(36, homo.MAPPED_HOMO)
        self.assertEqual(16, homo.N_RESTARTS)
        self.assertEqual(200, homo.SWEEP_CAP)
        self.assertEqual(5, homo.N_PLANTS)
        self.assertEqual(5, homo.N_FLOORS)
        self.assertEqual(
            200, sub.SWEEP_CAP, "the sweep cap is inherited as declared"
        )
        self.assertEqual(
            16, sub.N_RESTARTS, "the restart count is inherited"
        )

    def test_no_new_seed_kinds_are_consumed(self) -> None:
        self.assertEqual(1, homo.KIND_ID["real"])
        self.assertEqual(24, homo.KIND_ID["homo_plant_enc"])
        self.assertEqual(25, homo.KIND_ID["homo_plant_mach"])
        self.assertEqual(26, homo.KIND_ID["homo_floor_perm"])
        self.assertEqual(27, homo.KIND_ID["homo_floor_mach"])
        self.assertEqual(28, homo.KIND_ID["homo_cross_enc"])
        self.assertEqual(29, homo.KIND_ID["homo_cross_mach"])
        self.assertEqual(
            {1, 24, 25, 26, 27, 28, 29}, set(homo.KIND_ID.values()),
            "the held-out measurement consumes the first screen's kinds "
            "and draws none of its own",
        )

    def test_declared_artifact_strings(self) -> None:
        declared = json.loads(ARTIFACT.read_text())["declared"]
        self.assertEqual(20261020, declared["base_seed"])
        self.assertEqual(36, declared["mapped"])
        self.assertEqual(16, declared["restarts"])
        self.assertEqual(200, declared["sweep_cap"])
        split = declared["split_rule"]
        self.assertIn("pair-index parity", split)
        self.assertIn("even indices form the climb half", split)
        self.assertIn("odd indices the score half", split)
        self.assertIn("share no counted pair", split)
        self.assertIn(
            "every interior position carries one climbed pair and one "
            "scored pair", split,
        )
        self.assertIn("not an independent sample of the stream", split)
        self.assertIn("consumes no seed", split)
        machinery = declared["machinery_rule"]
        self.assertIn("exact greedy reassignment climb", machinery)
        self.assertIn("self-pair correction", machinery)
        self.assertIn("1e-12", machinery)
        self.assertIn("climb half", machinery)
        self.assertIn("score half", machinery)
        self.assertIn("ties to the first restart", machinery)
        self.assertIn("no assignment is stored", machinery)
        self.assertIn("no new kinds", declared["seed_sharing"])
        self.assertIn("machinery-above-anchor", declared["plant_rule"])
        self.assertIn(
            "smallest member value sets the band threshold",
            declared["band_rule"],
        )
        self.assertIn("attribution", declared["side_instrument"])
        self.assertIn("no verdict is built on it",
                      declared["side_instrument"])
        verdict = declared["verdict_rule"]
        self.assertIn("consistent-with-substitution", verdict)
        self.assertIn("not-consistent", verdict)
        self.assertIn("below-held-band", verdict)
        self.assertIn("machinery-noise-unresolved", verdict)
        exclusion = declared["exclusion_rule"]
        self.assertIn("smallest member band value", exclusion)
        self.assertIn("plant parity", exclusion)
        self.assertIn("standing caveats", exclusion)

    def test_the_two_screens_share_their_declared_draws(self) -> None:
        """The held-out measurement declares the first screen's draws;
        both artifacts record the same base seed and budgets, and the
        plant encodings replay from the same kinds."""
        held = json.loads(ARTIFACT.read_text())["declared"]
        screen = json.loads(SCREEN.read_text())["declared"]
        self.assertEqual(held["base_seed"], screen["base_seed"])
        self.assertEqual(held["mapped"], screen["mapped"])
        self.assertEqual(held["restarts"], screen["restarts"])
        self.assertEqual(held["sweep_cap"], screen["sweep_cap"])
        self.assertEqual(
            held["seed_kinds"]["homo_plant"],
            screen["seed_kinds"]["homo_plant"],
        )


class SplitRuleTest(unittest.TestCase):
    """The declared pair-index parity split."""

    def test_split_parity_and_pair_conservation(self) -> None:
        first = np.array([0, 1, 2, 3, 4, 5], dtype=np.int64)
        second = np.array([1, 2, 3, 4, 5, 6], dtype=np.int64)
        c_first, c_second, s_first, s_second = homo._split_pairs(
            first, second
        )
        # even pair indices 0, 2, 4 climb; odd pair indices 1, 3, 5 score
        self.assertEqual(c_first.tolist(), [0, 2, 4])
        self.assertEqual(c_second.tolist(), [1, 3, 5])
        self.assertEqual(s_first.tolist(), [1, 3, 5])
        self.assertEqual(s_second.tolist(), [2, 4, 6])
        # together the halves are the flat list, each pair exactly once
        np.testing.assert_array_equal(
            np.sort(np.concatenate([c_first, s_first])), np.sort(first),
        )
        np.testing.assert_array_equal(
            np.sort(np.concatenate([c_second, s_second])), np.sort(second),
        )
        # within each half, pairs two indices apart share no symbol
        climbed_positions = np.sort(
            np.stack([c_first, c_second], axis=1).reshape(-1)
        )
        self.assertTrue(np.all(np.diff(climbed_positions) > 0))
        scored_positions = np.sort(
            np.stack([s_first, s_second], axis=1).reshape(-1)
        )
        self.assertTrue(np.all(np.diff(scored_positions) > 0))

    def test_split_sizes_match_the_frozen_pair_counts(self) -> None:
        artifact = json.loads(ARTIFACT.read_text())
        for code in sub.FILES:
            stream = homo._homo_real_stream(code)
            first, second = homo._kept_pairs(
                stream["event_ids"], stream["kept_mask"]
            )
            c_first, _c2, s_first, _s2 = homo._split_pairs(first, second)
            cell = artifact["files"][code]["english"]
            label = code
            self.assertEqual(cell["counted_pairs"], len(first), label)
            self.assertEqual(cell["climb_pairs"], len(c_first), label)
            self.assertEqual(cell["score_pairs"], len(s_first), label)
            self.assertEqual(
                cell["climb_pairs"] + cell["score_pairs"],
                cell["counted_pairs"], label,
            )
            self.assertLessEqual(
                abs(cell["climb_pairs"] - cell["score_pairs"]), 1, label,
            )

    def test_reference_models_match_the_declared_halves(self) -> None:
        artifact = json.loads(ARTIFACT.read_text())
        models = artifact["declared"]["models"]
        for language, facts in MODELS.items():
            self.assertEqual(
                facts[0], models[language]["file"], language
            )
            self.assertEqual(
                facts[1], models[language]["ebook"], language
            )
            stream = sub._reference_stream(language)
            table, _counts = sub.table_from_stream(stream)
            matrix = homo._stream_matrix_27(stream)
            self.assertLess(
                abs(
                    round(float((matrix * table).sum()) / matrix.sum(), 4)
                    - facts[2]
                ), 1e-9, language,
            )
            held, climb, _cp, _sp = homo._identity_half_means(
                stream, table
            )
            self.assertLess(abs(round(climb, 4) - facts[3]), 1e-9, language)
            self.assertLess(abs(round(held, 4) - facts[4]), 1e-9, language)
            self.assertEqual(
                facts[3],
                models[language]["identity_climb_half_mean_nats_per_pair"],
                language,
            )
            self.assertEqual(
                facts[4],
                models[language]["identity_score_half_mean_nats_per_pair"],
                language,
            )


class ExactRuleTest(unittest.TestCase):
    """The declared exact greedy reassignment climb."""

    SMALL = None

    @classmethod
    def setUpClass(cls) -> None:
        rng = np.random.default_rng([20261020, 555])
        cls.SMALL = np.zeros((37, 37))
        np.add.at(
            cls.SMALL,
            (rng.integers(0, 37, 500), rng.integers(0, 37, 500)), 1.0,
        )

    def candidate_rule(self, matrix, table, f, symbol):
        """The declared candidate evaluation, written from its rule."""
        arr = np.asarray(f, dtype=np.int64)
        best = homo._score(arr, matrix, table)
        outbound = table[:, arr] @ matrix[symbol]
        inbound = matrix[:, symbol] @ table[arr, :]
        c = arr[symbol]
        n = matrix[symbol, symbol]
        hold = outbound[c] + inbound[c] - n * table[c, c]
        candidates = (
            best + outbound + inbound - hold
            - n * table[:, c] - n * table[c, :] + n * np.diag(table)
        )
        candidates[c] = best
        return candidates, best, hold

    def test_candidates_are_the_exact_new_totals(self) -> None:
        table, _counts = sub.table_from_stream(
            sub._reference_stream("english")
        )
        matrix = self.SMALL
        f = list(np.arange(37) % 27)
        symbol = 5
        arr = np.array(f)
        candidates, best, _hold = self.candidate_rule(
            matrix, table, f, symbol
        )
        brute = np.empty(27)
        for lab in range(27):
            g = arr.copy()
            g[symbol] = lab
            brute[lab] = best + (homo._score(g, matrix, table) - best)
        self.assertLess(float(np.abs(candidates - brute).max()), 1e-9)

    def test_held_climb_returns_the_exact_reevaluation(self) -> None:
        table, counts = sub.table_from_stream(
            sub._reference_stream("english")
        )
        total, sweeps, f_best = homo._held_climb(
            self.SMALL, table, homo._rank_init(self.SMALL, counts)
        )
        self.assertLess(
            abs(total - homo._score(f_best, self.SMALL, table)), 1e-9,
            "the climb's returned total is the exact score of its "
            "tracked assignment, so no drift reaches a stored number",
        )
        self.assertGreaterEqual(sweeps, 1)

    def test_machinery_is_deterministic_for_a_fresh_seed(self) -> None:
        truncated = homo._truncated_reference("ZL", "english")
        groups = homo._partition_groups(truncated, homo.MAPPED_HOMO)
        encoded = homo._encode(
            truncated, groups, np.random.default_rng([20261020, 90]),
            homo.MAPPED_HOMO,
        )
        first_ids, second_ids = homo._full_pairs(encoded)
        c1, c2, s1, s2 = homo._split_pairs(first_ids, second_ids)
        climb = homo._matrix_from_pairs(c1, c2)
        score = homo._matrix_from_pairs(s1, s2)
        table, counts = sub.table_from_stream(
            sub._reference_stream("english")
        )
        first = homo.machinery_best_held(
            climb, score, table, counts,
            np.random.default_rng([20261020, 91]),
            restarts=homo.N_RESTARTS,
        )
        second = homo.machinery_best_held(
            climb, score, table, counts,
            np.random.default_rng([20261020, 91]),
            restarts=homo.N_RESTARTS,
        )
        self.assertEqual(first, second)


class AnchorAlgebraTest(unittest.TestCase):
    """The true configuration's score-half identity is the anchor."""

    def test_true_assignment_scores_the_held_anchor(self) -> None:
        truncated = homo._truncated_reference("ZL", "english")[:3000]
        groups = homo._partition_groups(truncated, homo.MAPPED_HOMO)
        rng = np.random.default_rng([20261020, 80])
        encoded = homo._encode(truncated, groups, rng, homo.MAPPED_HOMO)
        f_true = np.zeros(homo.MAPPED_HOMO + 1, dtype=np.int64)
        for letter in range(26):
            for glyph in groups[letter]:
                f_true[glyph] = letter
        f_true[homo.MAPPED_HOMO] = 26
        enc_first, enc_second = homo._full_pairs(encoded)
        _, _, s1, s2 = homo._split_pairs(enc_first, enc_second)
        table, _counts = sub.table_from_stream(
            sub._reference_stream("english")
        )
        held_via_true = float(table[f_true[s1], f_true[s2]].sum()) / len(s1)
        anchor_held, _climb, _cp, _sp = homo._identity_half_means(
            truncated, table
        )
        self.assertLess(abs(held_via_true - anchor_held), 1e-9)


class FrozenCellsTest(unittest.TestCase):
    """The artifact's stored cells match the frozen measurement."""

    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())

    def test_all_six_cells_match_the_frozen_measurement(self) -> None:
        for (code, language), facts in FROZEN.items():
            cell = self.artifact["files"][code][language]
            label = f"{code}.{language}"
            self.assertEqual(
                facts.real_held, cell["real_held_mean_nats"], label
            )
            self.assertEqual(
                facts.real_climb, cell["real_climb_mean_nats"], label
            )
            self.assertEqual(
                facts.real_full,
                cell["real_full_exact_mean_nats"], label,
            )
            self.assertEqual(
                facts.counted, cell["counted_pairs"], label
            )
            self.assertEqual(
                facts.climb_pairs, cell["climb_pairs"], label
            )
            self.assertEqual(
                facts.score_pairs, cell["score_pairs"], label
            )
            self.assertEqual(
                facts.anchor,
                cell["plant_parity_anchor_mean_nats"], label,
            )
            self.assertEqual(
                facts.anchor_climb,
                cell["plant_climb_identity_mean_nats"], label,
            )
            self.assertEqual(
                facts.plants_held,
                cell["self_plants_held_mean_nats"], label,
            )
            self.assertEqual(
                facts.plants_full,
                cell["self_plants_full_exact_mean_nats"], label,
            )
            self.assertEqual(
                facts.excesses,
                cell["machinery_above_anchor_excesses"], label,
            )
            self.assertEqual(
                facts.floors_held,
                cell["floors_held_mean_nats"], label,
            )
            self.assertEqual(
                facts.floors_full,
                cell["floors_full_exact_mean_nats"], label,
            )
            self.assertEqual(facts.band_min, cell["band_min"], label)
            self.assertEqual(facts.band_max, cell["band_max"], label)
            self.assertEqual(facts.verdict, cell["verdict"], label)

    def test_all_band_members_match_their_frozen_draws(self) -> None:
        for (code, language), facts in FROZEN.items():
            cell = self.artifact["files"][code][language]
            self.assertEqual(
                band_expected(facts.band), cell["band"],
                f"{code}.{language}",
            )

    def test_the_declared_plant_rule_holds_everywhere(self) -> None:
        """Every plant at or above its held-out anchor minus 0.0001;
        flags and excesses recorded per the declared rule."""
        for (code, language), facts in FROZEN.items():
            cell = self.artifact["files"][code][language]
            anchor = cell["plant_parity_anchor_mean_nats"]
            values = cell["self_plants_held_mean_nats"]
            label = f"{code}.{language}"
            parity = [value >= anchor - 0.0001 for value in values]
            self.assertEqual(parity, cell["self_plants_at_parity"], label)
            self.assertTrue(all(parity), label)
            excesses = [
                round(value - anchor, 4)
                for value in values
                if value > anchor + 0.0001
            ]
            self.assertEqual(
                excesses, cell["machinery_above_anchor_excesses"], label
            )
            self.assertFalse(
                any(cell["self_plants_sweep_budget_hits"]), label
            )
            self.assertFalse(
                any(cell["self_plants_full_sweep_budget_hits"]), label
            )

    def test_every_floor_held_value_stays_below_the_real(self) -> None:
        for (code, language), facts in FROZEN.items():
            self.assertTrue(
                all(value < facts.real_held for value in facts.floors_held),
                f"{code}.{language}",
            )
            self.assertTrue(
                all(value < facts.real_full for value in facts.floors_full),
                f"{code}.{language}",
            )

    def test_the_real_stays_above_the_band_in_all_six_cells(self) -> None:
        """The frozen outcome that keeps the family open: under the
        repaired exact rule and the held-out split the real's held-out
        value still reaches past the smallest member value in every
        cell, so the declared exclusion format excludes nothing."""
        for (code, language), facts in FROZEN.items():
            cell = self.artifact["files"][code][language]
            margin = round(
                cell["real_held_mean_nats"] - cell["band_min"], 4
            )
            self.assertEqual(facts.margin_to_band, margin,
                             f"{code}.{language}")
            floor_margin = round(
                cell["real_held_mean_nats"]
                - max(cell["floors_held_mean_nats"]), 4
            )
            self.assertEqual(facts.margin_to_floor, floor_margin,
                             f"{code}.{language}")
            self.assertEqual(
                "consistent-with-substitution", cell["verdict"],
                f"{code}.{language}",
            )

    def test_no_machinery_call_hits_the_cap(self) -> None:
        """The declared exact rule converges: every recorded cap flag
        of the frozen run is false."""
        for code, cell in self.artifact["files"].items():
            for language, facts in cell.items():
                label = f"{code}.{language}"
                self.assertFalse(facts["real_sweep_budget_hit"], label)
                self.assertFalse(facts["real_full_sweep_budget_hit"], label)
                self.assertFalse(
                    any(facts["self_plants_sweep_budget_hits"]), label
                )
                self.assertFalse(
                    any(facts["self_plants_full_sweep_budget_hits"]), label
                )
                self.assertFalse(
                    any(facts["floors_sweep_budget_hits"]), label
                )
                self.assertFalse(
                    any(facts["floors_full_sweep_budget_hits"]), label
                )
                for member in facts["band"]:
                    self.assertFalse(
                        any(member["draw_sweep_budget_hits"]), label
                    )
                    self.assertFalse(
                        any(member["draw_full_sweep_budget_hits"]), label
                    )

    def test_the_selected_draw_rule_holds_everywhere(self) -> None:
        """Each member's band value is the held-out value of the draw
        whose climb-half total is best, ties to the first draw."""
        for code, cell in self.artifact["files"].items():
            for language, facts in cell.items():
                for member in facts["band"]:
                    label = f"{code}.{language} {member['file']}"
                    climbs = member["draws_climb"]
                    selected = 0
                    best = climbs[0]
                    for position, value in enumerate(climbs):
                        if value > best:
                            best = value
                            selected = position
                    self.assertEqual(
                        member["selected_draw_index"], selected, label
                    )
                    self.assertEqual(
                        member["recovered_best"],
                        member["draws"][selected], label,
                    )


class ReproducibilityTest(unittest.TestCase):
    """Stored values recompute exactly from the declared seeds."""

    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())

    def test_one_real_cell_recomputes_from_the_declared_seed(self) -> None:
        code, language = DEMO
        facts = FROZEN[(code, language)]
        table, counts = sub.table_from_stream(
            sub._reference_stream(language)
        )
        stream = homo._homo_real_stream(code)
        first, second = homo._kept_pairs(
            stream["event_ids"], stream["kept_mask"]
        )
        c1, c2, s1, s2 = homo._split_pairs(first, second)
        climb = homo._matrix_from_pairs(c1, c2)
        score = homo._matrix_from_pairs(s1, s2)
        full = homo._count_matrix_37(
            stream["event_ids"], stream["kept_mask"]
        )
        rng = np.random.default_rng(
            sub._seed(sub.CELL_ID[code], homo.KIND_ID["real"],
                      sub.LANG_ID[language], 0)
        )
        held, climb_view, hit = homo.machinery_best_held(
            climb, score, table, counts, rng, restarts=homo.N_RESTARTS
        )
        self.assertEqual(facts.real_held, round(held, 4))
        self.assertEqual(facts.real_climb, round(climb_view, 4))
        self.assertFalse(hit)
        rng_full = np.random.default_rng(
            sub._seed(sub.CELL_ID[code], homo.KIND_ID["real"],
                      sub.LANG_ID[language], 0)
        )
        full_value, full_hit = homo.machinery_exact_full(
            full, table, counts, rng_full, restarts=homo.N_RESTARTS
        )
        self.assertEqual(facts.real_full, round(full_value, 4))
        self.assertFalse(full_hit)

    def test_one_band_first_draw_recomputes_from_the_declared_seeds(
        self,
    ) -> None:
        code, language = DEMO
        facts = FROZEN[(code, language)]
        member = facts.band[0]
        table, counts = sub.table_from_stream(
            sub._reference_stream(language)
        )
        truncated = homo._truncated_reference(
            code, language, file=member.file
        )
        groups = homo._partition_groups(truncated, homo.MAPPED_HOMO)
        rng_enc = np.random.default_rng(
            sub._seed(sub.CELL_ID[code], homo.KIND_ID["homo_cross_enc"],
                      sub.LANG_ID[language], 0)
        )
        encoded = homo._encode(truncated, groups, rng_enc, homo.MAPPED_HOMO)
        e_first, e_second = homo._full_pairs(encoded)
        c1, c2, s1, s2 = homo._split_pairs(e_first, e_second)
        climb = homo._matrix_from_pairs(c1, c2)
        score = homo._matrix_from_pairs(s1, s2)
        full = homo._full_matrix_37(encoded)
        rng_mach = np.random.default_rng(
            sub._seed(sub.CELL_ID[code], homo.KIND_ID["homo_cross_mach"],
                      sub.LANG_ID[language], 0)
        )
        held, climb_view, hit = homo.machinery_best_held(
            climb, score, table, counts, rng_mach, restarts=homo.N_RESTARTS
        )
        self.assertEqual(member.draws[0], round(held, 4))
        self.assertEqual(member.draws_climb[0], round(climb_view, 4))
        self.assertFalse(hit)
        rng_full = np.random.default_rng(
            sub._seed(sub.CELL_ID[code], homo.KIND_ID["homo_cross_mach"],
                      sub.LANG_ID[language], 0)
        )
        full_value, full_hit = homo.machinery_exact_full(
            full, table, counts, rng_full, restarts=homo.N_RESTARTS
        )
        self.assertEqual(member.draws_full[0], round(full_value, 4))
        self.assertFalse(full_hit)

    def test_band_lengths_follow_the_declared_rule(self) -> None:
        for (code, language), facts in FROZEN.items():
            total = homo._homo_real_stream(code)["total_events"]
            for member in facts.band:
                reference = sub._reference_stream(language, file=member.file)
                self.assertEqual(
                    min(total, len(reference)), member.plant_length,
                    f"{code} {member.file}",
                )


if __name__ == "__main__":
    unittest.main()
