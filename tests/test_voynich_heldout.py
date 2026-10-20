"""Tests for the held-out family 3 measurement of the Voynich corpus."""

from __future__ import annotations

import json
import random
import unittest
from pathlib import Path

import numpy as np

import engine.voynich_heldout as heldout
import engine.voynich_transcript_stats as base
from engine.voynich_compare import index_loci
from engine.voynich_heldout import (
    HEAD,
    _pairs,
    _prepare,
    _shuffle_within_words,
    _token_model,
    _triples,
    heldout_report,
    glyph_null_nll,
    real_nlls,
    token_null_nll,
)
from engine.voynich_ivtff import parse_ivtff_text

RESERVED = [
    "f87r", "f96v", "f95r2", "f68v1", "f32v",
    "f106r", "f67r1", "f36r", "f82v", "f24r",
]
ARTIFACT = Path(
    "docs/research-notes/voynich-heldout-prediction.json"
).resolve()

_FROZEN_CELLS = {
    "ZL": {"train_loci": 5013, "reserved_loci": 201, "train_tokens": 34354,
           "reserved_tokens": 1410, "absent_shared_loci": 0},
    "GC": {"train_loci": 5012, "reserved_loci": 201, "train_tokens": 36232,
           "reserved_tokens": 1478, "absent_shared_loci": 1},
    "IT": {"train_loci": 5013, "reserved_loci": 201, "train_tokens": 36441,
           "reserved_tokens": 1477, "absent_shared_loci": 0},
}


class ArtifactTest(unittest.TestCase):
    """The committed artifact of the family 3 run, pinned."""

    artifact: dict

    @classmethod
    def setUpClass(cls) -> None:
        cls.artifact = json.loads(ARTIFACT.read_text())

    def test_the_artifact_uses_the_frozen_reservation(self) -> None:
        self.assertEqual(RESERVED, self.artifact["reserved_folios"])
        self.assertEqual(1000, self.artifact["n_perm"])
        self.assertEqual(set(("ZL", "GC", "IT")), set(self.artifact["cells"]))

    def test_each_cell_holds_its_frozen_counts(self) -> None:
        for code, facts in _FROZEN_CELLS.items():
            for name, value in facts.items():
                self.assertEqual(
                    value, self.artifact["cells"][code][name], f"{code}.{name}"
                )

    def test_every_cell_is_detected_at_the_smallest_declared_p(self) -> None:
        for code, cell in sorted(self.artifact["cells"].items()):
            for statistic in ("glyph", "token"):
                facts = cell[statistic]
                self.assertAlmostEqual(
                    1.0 / 1001.0, facts["p_value"], places=12,
                    msg=f"{code}.{statistic}",
                )
                self.assertEqual("detected", facts["verdict"], f"{code}.{statistic}")
                self.assertEqual(0, facts["nulls_at_or_below_real"],
                                 f"{code}.{statistic}")
                self.assertEqual(HEAD, len(facts["stored_null_head"]),
                                 f"{code}.{statistic}")

    def test_the_real_score_sits_below_the_null_minimum_everywhere(self) -> None:
        for code, cell in sorted(self.artifact["cells"].items()):
            for statistic in ("glyph", "token"):
                facts = cell[statistic]
                self.assertLess(
                    facts["real_nll"], facts["null_min"], f"{code}.{statistic}"
                )


class ReproducibilityTest(unittest.TestCase):
    """Declared seeds: stored null heads must recomput from the toolkit."""

    artifact: dict

    @classmethod
    def setUpClass(cls) -> None:
        cls.artifact = json.loads(ARTIFACT.read_text())
        heldout._PREPARED.clear()

    def test_stored_glyph_head_recomputes_from_its_seed(self) -> None:
        stored = self.artifact["cells"]["ZL"]["glyph"]["stored_null_head"]
        for index, value in enumerate(stored):
            self.assertAlmostEqual(
                value, glyph_null_nll("ZL", index), places=9, msg=f"ZL glyph {index}"
            )

    def test_stored_token_head_recomputes_from_its_seed(self) -> None:
        stored = self.artifact["cells"]["IT"]["token"]["stored_null_head"]
        for index, value in enumerate(stored):
            self.assertAlmostEqual(
                value, token_null_nll("IT", index), places=9, msg=f"IT token {index}"
            )

    def test_the_real_statistics_match_the_artifact(self) -> None:
        for code in ("ZL", "GC", "IT"):
            glyph_real, token_real = real_nlls(code)
            self.assertAlmostEqual(
                self.artifact["cells"][code]["glyph"]["real_nll"],
                glyph_real, places=9, msg=code,
            )
            self.assertAlmostEqual(
                self.artifact["cells"][code]["token"]["real_nll"],
                token_real, places=9, msg=code,
            )


class MachineryTest(unittest.TestCase):
    def test_word_gauge_masks_stay_inside_words(self) -> None:
        flat = np.array([1, 2, 3, 9, 9, 4, 5], dtype=np.int64)
        lens = np.array([3, 1, 3], dtype=np.int64)
        # word one is 1,2,3; word two is the lone 9; word three is 9,4,5.
        a, b = _pairs(flat, lens)
        np.testing.assert_array_equal(np.array([1, 2, 9, 4]), a)
        np.testing.assert_array_equal(np.array([2, 3, 4, 5]), b)
        tri_a, tri_b, tri_c = _triples(flat, lens)
        np.testing.assert_array_equal(np.array([1, 9]), tri_a)
        np.testing.assert_array_equal(np.array([2, 4]), tri_b)
        np.testing.assert_array_equal(np.array([3, 5]), tri_c)

    def test_the_word_glyph_shuffle_preserves_lengths_and_multiset(self) -> None:
        words = ["qokedy", "daiin", "or"]
        alphabet = sorted({c for w in words for c in w})
        code = {c: i for i, c in enumerate(alphabet)}
        flat = np.array([code[c] for w in words for c in w], dtype=np.int64)
        lens = np.array([len(w) for w in words], dtype=np.int64)
        token_ids = np.repeat(np.arange(lens.size), lens)
        rng = np.random.default_rng([20261020, 0, 0, 0])
        shuffled = _shuffle_within_words(flat, token_ids, rng)
        self.assertEqual(sorted(flat.tolist()), sorted(shuffled.tolist()))
        self.assertEqual(
            [tuple(sorted(v.tolist())) for v in np.split(flat, np.cumsum(lens)[:-1])],
            [tuple(sorted(v.tolist())) for v in np.split(shuffled, np.cumsum(lens)[:-1])],
        )

    def test_the_token_shuffle_preserves_the_word_multiset(self) -> None:
        rng = np.random.default_rng([20261020, 1, 1, 3])
        ids = np.arange(40) % 7
        shuffled = ids[rng.permutation(ids.size)]
        self.assertEqual(sorted(ids.tolist()), sorted(shuffled.tolist()))

    def test_token_model_scoring_is_symmetric_in_the_union_alphabet(self) -> None:
        # add-one means an unseen pair scores 1/(unigram + v), which keeps
        # real and null models evaluated on the same vocabulary size.
        ids = np.array([0, 1, 0, 1, 2], dtype=np.int64)
        lens = np.array([5], dtype=np.int64)
        a, b = heldout._pairs(ids, lens)
        model = _token_model(ids, a, b, 5)
        value = heldout._token_nll(model, a, b, 5)
        self.assertGreater(value, 0.0)


class PowerTest(unittest.TestCase):
    """Synthetic planted controls: detection and no-false-detection."""

    folios = ["f1r", "f2r", "f3r", "f4r", "f5r"]
    N = 25  # replication budget for the synthetic instruments

    def setUp(self) -> None:
        heldout._PREPARED.clear()
        self._originals = (
            heldout.load, heldout.index_loci, heldout.FILES,
            base.load, base.index_loci, base.RESERVED_COUNT,
        )

    def tearDown(self) -> None:
        heldout._PREPARED.clear()
        (heldout.load, heldout.index_loci, heldout.FILES,
         base.load, base.index_loci, base.RESERVED_COUNT) = self._originals

    def _install(self, word_of_locus) -> None:
        lines = ["#=IVTFF Eva- 2.0 M 1"]
        for folio in self.folios:
            lines.append(f"<{folio}>      <! $L=A>")
            for i, words in enumerate(word_of_locus(), start=1):
                marker = "@P0" if i == 1 else "+P0"
                lines.append(f"<{folio}.{i},{marker}>       {words}")
        text = "\n".join(lines) + "\n"
        parsed = {code: parse_ivtff_text(text) for code in ("ZL", "IT")}

        def fake_load(code: str):
            return parsed[code]

        shared_index = index_loci(parsed["ZL"])

        def fake_index(_file):
            return shared_index

        heldout.load = fake_load
        heldout.index_loci = fake_index
        heldout.FILES = ("ZL", "IT")
        base.load = fake_load
        base.index_loci = fake_index
        base.RESERVED_COUNT = 1

    def test_template_structure_is_detected_in_words(self) -> None:
        random.seed(7)
        middles = "oear"
        bodies = "kchr"

        def loci():
            return [".".join(
                f"q{random.choice(middles)}{random.choice(bodies)}dy"
                for _ in range(6)
            ) for _ in range(4)]

        self._install(loci)
        report = heldout_report(n_perm=self.N)
        facts = report["cells"]["ZL"]["glyph"]
        self.assertEqual(0, facts["nulls_at_or_below_real"], "planted rule")
        self.assertAlmostEqual(
            1.0 / (self.N + 1.0), facts["p_value"], places=12,
        )

    def test_template_structure_is_detected_in_word_adjacency(self) -> None:
        # The rule needs a third type: after 'or' always 'sheey', never
        # 'daiin', so a global token shuffle cannot reproduce the rates.
        def loci():
            return [".".join(["daiin", "or", "sheey"] * 4) for _ in range(4)]

        self._install(loci)
        report = heldout_report(n_perm=self.N)
        facts = report["cells"]["ZL"]["token"]
        self.assertEqual(0, facts["nulls_at_or_below_real"], "planted adjacency")
        self.assertAlmostEqual(
            1.0 / (self.N + 1.0), facts["p_value"], places=12,
        )

    def test_shuffled_only_glyphs_are_not_detected(self) -> None:
        # An i.i.d. glyph bag carries no order structure beyond its glyph
        # multiset: the real score must not fall below every null.
        random.seed(11)
        letters = "ohikrdy"

        def loci():
            return [".".join(
                "".join(random.choice(letters) for _ in range(4))
                for _ in range(6)
            ) for _ in range(4)]

        self._install(loci)
        report = heldout_report(n_perm=self.N)
        facts = report["cells"]["ZL"]["glyph"]
        self.assertGreaterEqual(facts["nulls_at_or_below_real"], 1)
        self.assertGreaterEqual(facts["p_value"], 0.05)

    def test_shuffled_only_tokens_are_not_detected(self) -> None:
        random.seed(13)
        vocabulary = ["daiin", "or", "sheey", "okal"]

        def loci():
            return [".".join(
                random.choice(vocabulary) for _ in range(8)
            ) for _ in range(4)]

        self._install(loci)
        report = heldout_report(n_perm=self.N)
        facts = report["cells"]["ZL"]["token"]
        self.assertGreaterEqual(facts["nulls_at_or_below_real"], 1)
        self.assertGreaterEqual(facts["p_value"], 0.05)


if __name__ == "__main__":
    unittest.main()
