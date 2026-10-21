"""Tests for the declared homophonic screen of Voynich family 5.

The artifact pins the frozen measurement; the reproducibility tests
recompute stored real and band values from the declared seeds; the
machinery tests nail down the reassignment search: the partition rule
sums to its declared budget, the encoder is invertible under its true
key, a planted homophonic encoding reaches at least its anchor through
the declared climb, and the incremental candidate identity is exact.
Nothing here reads the manuscript.
"""

from __future__ import annotations

import json
import unittest
from pathlib import Path

import numpy as np

import engine.voynich_homophonic as homo
from engine import voynich_substitution as sub

ARTIFACT = Path("docs/research-notes/voynich-homophonic-screen.json").resolve()

# The frozen measurement of 21 October 2026. Real best mean nats per
# counted pair, the per-cell anchor, the five plant values with their
# cap-disclosure flags and machinery-above-anchor excesses, the floor
# values, the band members, and the verdicts the declared rule emitted:
# every cell came back consistent-with-substitution, the real scoring
# above the band under the wider alphabet, so the family stays open by
# the declared exclusion format.
FROZEN = {
    ("ZL", "english"): {
        "real": -4.4149,
        "real_hit": True,
        "counted": 218415,
        "anchor": -5.1422,
        "plants": [-4.7417, -4.7256, -4.7411, -4.7256, -4.7256],
        "excesses": [0.4005, 0.4166, 0.4011, 0.4166, 0.4166],
        "floors": [-5.2948, -5.2989, -5.2693, -5.2982, -5.2711],
        "band": [
            ("substref_english2_pg84.txt", 84, 218663, -5.1603,
             [-4.738, -4.6997, -4.6548, -4.7489, -4.6569]),
            ("substref_english3_pg2701.txt", 2701, 218663, -5.1893,
             [-4.7011] * 5),
            ("substref_english4_pg1251.txt", 1251, 218663, -5.1004,
             [-4.6712, -4.6696, -4.6766, -4.5774, -4.6712]),
        ],
        "band_min": -4.7011,
        "band_max": -4.5774,
        "verdict": "consistent-with-substitution",
    },
    ("ZL", "latin"): {
        "real": -4.5125,
        "real_hit": True,
        "counted": 218415,
        "anchor": -5.0742,
        "plants": [-4.5873, -4.5873, -4.5873, -4.5772, -4.5772],
        "excesses": [0.4869, 0.4869, 0.4869, 0.497, 0.497],
        "floors": [-5.2078, -5.2172, -5.2066, -5.2008, -5.2038],
        "band": [
            ("substref_latin2_pg218.txt", 218, 143947, -5.1345,
             [-4.6194] * 5),
            ("substref_latin3_pg828.txt", 828, 77572, -5.1459,
             [-4.5807, -4.5867, -4.5867, -4.5867, -4.5867]),
            ("substref_latin4_pg17859.txt", 17859, 218663, -5.1685,
             [-4.6152, -4.6152, -4.6152, -4.6152, -4.6063]),
            ("substref_latin5_pg27655.txt", 27655, 77529, -5.2072,
             [-4.5883] * 5),
        ],
        "band_min": -4.6194,
        "band_max": -4.5807,
        "verdict": "consistent-with-substitution",
    },
    ("GC", "english"): {
        "real": -4.3527,
        "real_hit": True,
        "counted": 183199,
        "anchor": -5.143,
        "plants": [-4.7271, -4.7271, -4.6594, -4.6599, -4.6592],
        "excesses": [0.4159, 0.4159, 0.4836, 0.4831, 0.4838],
        "floors": [-5.3489, -5.2966, -5.3567, -5.3471, -5.3598],
        "band": [
            ("substref_english2_pg84.txt", 84, 186708, -5.1646,
             [-4.7292, -4.7519, -4.7004, -4.7292, -4.7292]),
            ("substref_english3_pg2701.txt", 2701, 186708, -5.1887,
             [-4.7021, -4.7021, -4.7217, -4.7264, -4.7552]),
            ("substref_english4_pg1251.txt", 1251, 186708, -5.1083,
             [-4.6711, -4.6711, -4.5826, -4.6701, -4.6701]),
        ],
        "band_min": -4.7021,
        "band_max": -4.5826,
        "verdict": "consistent-with-substitution",
    },
    ("GC", "latin"): {
        "real": -4.3896,
        "real_hit": True,
        "counted": 183199,
        "anchor": -5.0743,
        "plants": [-4.5873] * 5,
        "excesses": [0.487] * 5,
        "floors": [-5.6689, -5.3818, -5.385, -5.6679, -5.6174],
        "band": [
            ("substref_latin2_pg218.txt", 218, 143947, -5.1345,
             [-4.6074, -4.6194, -4.6194, -4.6194, -4.6194]),
            ("substref_latin3_pg828.txt", 828, 77572, -5.1459,
             [-4.5867, -4.5807, -4.5867, -4.5807, -4.5807]),
            ("substref_latin4_pg17859.txt", 17859, 186708, -5.1665,
             [-4.6143, -4.6143, -4.6143, -4.6143, -4.6053]),
            ("substref_latin5_pg27655.txt", 27655, 77529, -5.2072,
             [-4.5883] * 5),
        ],
        "band_min": -4.6074,
        "band_max": -4.5807,
        "verdict": "consistent-with-substitution",
    },
    ("IT", "english"): {
        "real": -4.4136,
        "real_hit": True,
        "counted": 220531,
        "anchor": -5.1422,
        "plants": [-4.75, -4.726, -4.6599, -4.7492, -4.6914],
        "excesses": [0.3922, 0.4162, 0.4823, 0.393, 0.4508],
        "floors": [-5.3048, -5.2966, -5.2972, -5.2992, -5.3016],
        "band": [
            ("substref_english2_pg84.txt", 84, 220532, -5.1603,
             [-4.6997, -4.7557, -4.6568, -4.7557, -4.7306]),
            ("substref_english3_pg2701.txt", 2701, 220532, -5.1905,
             [-4.7013] * 5),
            ("substref_english4_pg1251.txt", 1251, 220532, -5.0999,
             [-4.6696, -4.6711, -4.6889, -4.6696, -4.7401]),
        ],
        "band_min": -4.7013,
        "band_max": -4.6568,
        "verdict": "consistent-with-substitution",
    },
    ("IT", "latin"): {
        "real": -4.5027,
        "real_hit": True,
        "counted": 220531,
        "anchor": -5.074,
        "plants": [-4.5773, -4.5874, -4.5874, -4.5874, -4.5773],
        "excesses": [0.4967, 0.4866, 0.4866, 0.4866, 0.4967],
        "floors": [-5.2134, -5.2177, -5.222, -5.2221, -5.2297],
        "band": [
            ("substref_latin2_pg218.txt", 218, 143947, -5.1345,
             [-4.6194, -4.6088, -4.6194, -4.6194, -4.6194]),
            ("substref_latin3_pg828.txt", 828, 77572, -5.1459,
             [-4.5807, -4.5807, -4.5807, -4.5867, -4.5807]),
            ("substref_latin4_pg17859.txt", 17859, 220532, -5.1685,
             [-4.6062, -4.615, -4.6051, -4.615, -4.615]),
            ("substref_latin5_pg27655.txt", 27655, 77529, -5.2072,
             [-4.5883, -4.5883, -4.6305, -4.5883, -4.5883]),
        ],
        "band_min": -4.6088,
        "band_max": -4.5807,
        "verdict": "consistent-with-substitution",
    },
}

MODELS = {
    "english": ("substref_english_pg1342.txt", 1342, -5.1311),
    "latin": ("substref_latin_pg33849.txt", 33849, -5.0999),
}

DEMO = ("ZL", "english")


def band_expected(frozen: dict) -> list[dict]:
    """The frozen band members in the artifact's stored shape."""
    members = []
    for name, ebook, length, anchor, draws in frozen["band"]:
        members.append({
            "file": name,
            "ebook": ebook,
            "plant_length": length,
            "anchor": anchor,
            "draws": draws,
            "draw_cap_hits": [True] * 5,
            "recovered_best": max(draws),
            "spread": round(max(draws) - min(draws), 4),
        })
    return members


class DeclaredBookkeepingTest(unittest.TestCase):
    """The declared constants and rule strings, pinned before the run."""

    def test_declared_constants(self) -> None:
        self.assertEqual(36, homo.MAPPED_HOMO)
        self.assertEqual(16, homo.N_RESTARTS)
        self.assertEqual(200, homo.SWEEP_CAP)
        self.assertEqual(5, homo.N_PLANTS)
        self.assertEqual(5, homo.N_FLOORS)
        self.assertEqual(
            200, sub.SWEEP_CAP, "the sweep cap is inherited as declared"
        )
        self.assertEqual(
            16, sub.N_RESTARTS, "the restart count is inherited as declared"
        )

    def test_declared_seed_kinds(self) -> None:
        self.assertEqual(1, homo.KIND_ID["real"])
        self.assertEqual(24, homo.KIND_ID["homo_plant_enc"])
        self.assertEqual(25, homo.KIND_ID["homo_plant_mach"])
        self.assertEqual(26, homo.KIND_ID["homo_floor_perm"])
        self.assertEqual(27, homo.KIND_ID["homo_floor_mach"])
        self.assertEqual(28, homo.KIND_ID["homo_cross_enc"])
        self.assertEqual(29, homo.KIND_ID["homo_cross_mach"])
        shared = set(homo.KIND_ID.values()) & set(sub.KIND_ID.values())
        self.assertEqual(
            {1}, shared,
            "only the real's kind 1 is shared across the two artefacts",
        )

    def test_declared_artifact_strings(self) -> None:
        artifact = json.loads(ARTIFACT.read_text())
        declared = artifact["declared"]
        self.assertEqual(20261020, declared["base_seed"])
        self.assertEqual(36, declared["mapped"])
        self.assertEqual(16, declared["restarts"])
        self.assertEqual(200, declared["sweep_cap"])
        rule = declared["band_membership_rule"]
        self.assertIn("unconditional", rule)
        self.assertIn("smallest member value sets the band threshold", rule)
        verdict = declared["verdict_rule"]
        self.assertIn("consistent-with-substitution", verdict)
        self.assertIn("not-consistent", verdict)
        self.assertIn("below-homophonic-band", verdict)
        self.assertIn("machinery-noise-unresolved", verdict)
        self.assertIn("memberless band", verdict)
        exclusion = declared["exclusion_rule"]
        self.assertIn("smallest member value", exclusion)
        self.assertIn("plant parity", exclusion)
        self.assertIn("standing caveats", exclusion)

    def test_reference_models_are_frozen(self) -> None:
        artifact = json.loads(ARTIFACT.read_text())
        models = artifact["declared"]["models"]
        for language, (name, ebook, anchor) in MODELS.items():
            self.assertEqual(name, models[language]["file"])
            self.assertEqual(ebook, models[language]["ebook"])
            self.assertEqual(
                anchor, models[language]["clean_identity_mean_nats_per_pair"]
            )


class FrozenCellsTest(unittest.TestCase):
    """The artifact's stored cells match the frozen measurement."""

    def setUp(self) -> None:
        self.artifact = json.loads(ARTIFACT.read_text())

    def test_all_six_cells_match_the_frozen_measurement(self) -> None:
        for (code, language), facts in FROZEN.items():
            cell = self.artifact["files"][code][language]
            label = f"{code}.{language}"
            self.assertEqual(facts["real"], cell["real_best_mean_nats"], label)
            self.assertEqual(
                facts["counted"], cell["counted_pairs"], label
            )
            self.assertEqual(
                facts["anchor"],
                cell["plant_parity_anchor_mean_nats"],
                label,
            )
            self.assertEqual(
                facts["real_hit"], cell["real_sweep_budget_hit"], label
            )
            self.assertEqual(
                facts["plants"],
                cell["self_plants_best_mean_nats"], label,
            )
            self.assertEqual(
                facts["excesses"],
                cell["machinery_above_anchor_excesses"], label,
            )
            self.assertEqual(
                facts["floors"], cell["floors_best_mean_nats"], label
            )
            self.assertEqual(facts["band_min"], cell["band_min"], label)
            self.assertEqual(facts["band_max"], cell["band_max"], label)
            self.assertEqual(facts["verdict"], cell["verdict"], label)

    def test_all_band_members_match_their_frozen_draws(self) -> None:
        for (code, language), facts in FROZEN.items():
            cell = self.artifact["files"][code][language]
            self.assertEqual(
                band_expected(facts), cell["band"], f"{code}.{language}"
            )
            for member in cell["band"]:
                self.assertTrue(all(member["draw_cap_hits"]))

    def test_the_declared_plant_rule_holds_everywhere(self) -> None:
        """Every plant at or above its anchor minus 0.0001; flags and
        excesses recorded per the declared rule."""
        for (code, language), facts in FROZEN.items():
            cell = self.artifact["files"][code][language]
            anchor = cell["plant_parity_anchor_mean_nats"]
            values = cell["self_plants_best_mean_nats"]
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
            self.assertTrue(
                all(cell["self_plants_sweep_budget_hits"]), label
            )

    def test_every_floor_stays_below_the_real(self) -> None:
        for (code, language), facts in FROZEN.items():
            self.assertTrue(
                all(value < facts["real"] for value in facts["floors"]),
                f"{code}.{language}",
            )

    def test_the_real_is_above_the_band_in_all_six_cells(self) -> None:
        """The frozen outcome that keeps the family open: the real's
        machinery best reaches or passes the smallest member value in
        every cell."""
        for (code, language), facts in FROZEN.items():
            cell = self.artifact["files"][code][language]
            self.assertGreaterEqual(
                cell["real_best_mean_nats"], cell["band_min"],
                f"{code}.{language}",
            )
            self.assertEqual(
                "consistent-with-substitution", cell["verdict"],
                f"{code}.{language}",
            )
            self.assertIsNotNone(cell["band_min"])


class ReproducibilityTest(unittest.TestCase):
    """Stored cells recompute exactly from the declared seeds."""

    def test_one_real_cell_recomputes_from_the_declared_seed(self) -> None:
        code, language = DEMO
        facts = FROZEN[(code, language)]
        table, counts = sub.table_from_stream(sub._reference_stream(language))
        stream = homo._homo_real_stream(code)
        matrix = homo._count_matrix_37(
            stream["event_ids"], stream["kept_mask"]
        )
        rng = np.random.default_rng(
            sub._seed(sub.CELL_ID[code], homo.KIND_ID["real"],
                      sub.LANG_ID[language], 0)
        )
        value, hit = homo.machinery_best(
            matrix, table, counts, rng, restarts=homo.N_RESTARTS
        )
        self.assertEqual(facts["real"], round(value, 4))
        self.assertEqual(facts["real_hit"], hit)

    def test_one_band_first_draw_recomputes_from_the_declared_seeds(
        self,
    ) -> None:
        code, language = DEMO
        facts = FROZEN[(code, language)]
        table, counts = sub.table_from_stream(sub._reference_stream(language))
        truncated = homo._truncated_reference(
            code, language, file=facts["band"][0][0]
        )
        groups = homo._partition_groups(truncated, homo.MAPPED_HOMO)
        rng_enc = np.random.default_rng(
            sub._seed(sub.CELL_ID[code], homo.KIND_ID["homo_cross_enc"],
                      sub.LANG_ID[language], 0)
        )
        encoded = homo._encode(truncated, groups, rng_enc, homo.MAPPED_HOMO)
        matrix = homo._full_matrix_37(encoded)
        rng_mach = np.random.default_rng(
            sub._seed(sub.CELL_ID[code], homo.KIND_ID["homo_cross_mach"],
                      sub.LANG_ID[language], 0)
        )
        value, hit = homo.machinery_best(
            matrix, table, counts, rng_mach, restarts=homo.N_RESTARTS
        )
        self.assertEqual(facts["band"][0][4][0], round(value, 4))
        self.assertTrue(hit)

    def test_plant_lengths_follow_the_declared_rule(self) -> None:
        for (code, language), facts in FROZEN.items():
            total = homo._homo_real_stream(code)["total_events"]
            for name, _ebook, length, _anchor, _draws in facts["band"]:
                reference = sub._reference_stream(language, file=name)
                self.assertEqual(
                    min(total, len(reference)), length, f"{code} {name}"
                )


class MachineryTest(unittest.TestCase):
    """The declared search on synthetic and planted data."""

    def test_partition_sums_to_the_declared_budget(self) -> None:
        for language in ("english", "latin"):
            truncated = homo._truncated_reference("ZL", language)
            groups = homo._partition_groups(truncated, homo.MAPPED_HOMO)
            sizes = [len(groups[letter]) for letter in range(27)]
            self.assertEqual(homo.MAPPED_HOMO, sum(sizes))
            self.assertEqual([], groups[26])
            present = {value for value in truncated if value != 26}
            for letter in present:
                self.assertGreaterEqual(sizes[letter], 1)
            used = [glyph for letter in present for glyph in groups[letter]]
            self.assertEqual(len(set(used)), len(used))

    def test_encoder_is_invertible_under_the_true_key(self) -> None:
        truncated = homo._truncated_reference("ZL", "english")[:3000]
        groups = homo._partition_groups(truncated, homo.MAPPED_HOMO)
        rng = np.random.default_rng([20261020, 70])
        encoded = homo._encode(truncated, groups, rng, homo.MAPPED_HOMO)
        f_true = np.zeros(homo.MAPPED_HOMO + 1, dtype=np.int64)
        for letter in range(26):
            for glyph in groups[letter]:
                f_true[glyph] = letter
        f_true[homo.MAPPED_HOMO] = 26
        decoded = np.array(
            [26 if s == homo.MAPPED_HOMO else int(f_true[s]) for s in encoded]
        )
        self.assertTrue(np.array_equal(decoded, np.array(truncated)))
        table, _counts = sub.table_from_stream(
            sub._reference_stream("english")
        )
        scored = homo._score(
            f_true, homo._full_matrix_37(encoded), table
        )
        identity = float((homo._stream_matrix_27(truncated) * table).sum())
        self.assertLess(abs(scored - identity), 1e-6)

    def test_planted_encoding_reaches_the_declared_pass_rule(self) -> None:
        """The machinery never falls below a planted configuration's own
        score by more than the declared tie."""
        truncated = homo._truncated_reference("ZL", "english")
        groups = homo._partition_groups(truncated, homo.MAPPED_HOMO)
        rng = np.random.default_rng([20261020, 71])
        encoded = homo._encode(truncated, groups, rng, homo.MAPPED_HOMO)
        matrix = homo._full_matrix_37(encoded)
        table, counts = sub.table_from_stream(
            sub._reference_stream("english")
        )
        anchor_matrix = homo._stream_matrix_27(truncated)
        anchor = float((anchor_matrix * table).sum()) / anchor_matrix.sum()
        mach_rng = np.random.default_rng([20261020, 172])
        value, _hit = homo.machinery_best(
            matrix, table, counts, mach_rng, restarts=homo.N_RESTARTS
        )
        self.assertGreaterEqual(value, anchor - 0.0001)

    def test_candidate_identity_at_the_current_label(self) -> None:
        """The incremental candidate equals the running score exactly at
        the current label."""
        rng = np.random.default_rng([20261020, 73])
        matrix = rng.random((37, 37)) * 10
        table, _counts = sub.table_from_stream(
            sub._reference_stream("english")
        )
        f = np.arange(37) % 27
        best = homo._score(f, matrix, table)
        outbound = table[:, f] @ matrix[0]
        inbound = matrix[:, 0] @ table[f, :]
        current = f[0]
        hold = (
            outbound[current] + inbound[current]
            - matrix[0, 0] * table[current, current]
        )
        candidates = (
            best + outbound + inbound
            - matrix[0, 0] * np.diag(table) - hold
        )
        self.assertLess(abs(candidates[current] - best), 1e-9)
        self.assertFalse(np.any(np.diag(table) > 0))

    def test_machinery_is_deterministic_for_a_fresh_seed(self) -> None:
        truncated = homo._truncated_reference("ZL", "english")
        groups = homo._partition_groups(truncated, homo.MAPPED_HOMO)
        encoded = homo._encode(
            truncated, groups, np.random.default_rng([20261020, 74]),
            homo.MAPPED_HOMO,
        )
        matrix = homo._full_matrix_37(encoded)
        table, counts = sub.table_from_stream(
            sub._reference_stream("english")
        )
        first = homo.machinery_best(
            matrix, table, counts,
            np.random.default_rng([20261020, 175]),
            restarts=homo.N_RESTARTS,
        )
        second = homo.machinery_best(
            matrix, table, counts,
            np.random.default_rng([20261020, 175]),
            restarts=homo.N_RESTARTS,
        )
        self.assertEqual(first, second)

    def test_rank_init_wraps_the_surplus_symbols(self) -> None:
        """Reconstructing the declared rule reproduces the module's
        start: the k-th most frequent symbol at the k-th most frequent
        letter, k modulo 27."""
        table, counts = sub.table_from_stream(
            sub._reference_stream("english")
        )
        string = homo._truncated_reference("ZL", "english")
        rng = np.random.default_rng([20261020, 76])
        encoded = homo._encode(
            string,
            homo._partition_groups(string, homo.MAPPED_HOMO),
            rng,
            homo.MAPPED_HOMO,
        )
        matrix = homo._full_matrix_37(encoded)
        f = homo._rank_init(matrix, counts)
        self.assertEqual(37, len(f))
        self.assertTrue(all(0 <= label <= 26 for label in f))
        totals = matrix.sum(axis=1) + matrix.sum(axis=0)
        symbol_rank = np.argsort(-totals, kind="stable")
        letter_rank = np.argsort(-counts, kind="stable")
        self.assertEqual(
            [int(letter_rank[k % 27]) for k in range(37)],
            [f[int(symbol)] for symbol in symbol_rank],
        )


if __name__ == "__main__":
    unittest.main()
