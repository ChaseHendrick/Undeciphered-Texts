"""The broad-generator manifest records labels and does not replace Bob."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

from engine.alphabet import letters_only
from engine.neural import load_training_prose
from engine.neural_generator_broad import _weights_sha256, probe_manifest

_MANIFEST = Path("engine/data/bob_probe_manifest_2026-10-04.json")


class BobProbeManifestTest(unittest.TestCase):
    def test_committed_manifest_matches_the_shipped_weights(self) -> None:
        saved = json.loads(_MANIFEST.read_text(encoding="utf-8"))
        self.assertFalse(saved["incumbent_replaced"])
        self.assertTrue(saved["weights_unchanged"])
        self.assertEqual(saved["weights_sha256"], _weights_sha256())
        self.assertEqual(saved["format_version"], 10)
        self.assertEqual(saved["seed"], 20261005)
        self.assertEqual(saved["per_family"], 32)
        self.assertEqual(len(saved["rows"]), 128)
        self.assertEqual(saved["restricted_top1"], 63)
        self.assertEqual(saved["broad_top1"], 30)
        self.assertTrue(all(len(row["ciphertext_sha256"]) == 64 for row in saved["rows"]))

    def test_a_fresh_one_key_manifest_does_not_write_weights(self) -> None:
        before = _weights_sha256()
        letters = "".join(
            char for char in letters_only(load_training_prose()) if "A" <= char <= "Z"
        )
        report = probe_manifest(letters[:180], seed=3, per_family=1)
        self.assertEqual(_weights_sha256(), before)
        self.assertFalse(report["incumbent_replaced"])
        self.assertEqual(len(report["rows"]), 4)


if __name__ == "__main__":
    unittest.main()
