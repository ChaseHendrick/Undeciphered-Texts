"""The extra training file is public prose, not the held-out pages."""

from __future__ import annotations

import unittest
from pathlib import Path

from engine.neural_grade import (
    HELD_EN_PATH, TRAIN_PATH, assert_certificate_plaintexts_excluded, assert_split,
    letters_az, load_training_prose,
)

_DATA = Path(__file__).resolve().parents[1] / "engine" / "data"


class PublicProseTest(unittest.TestCase):
    def test_the_extra_file_does_not_contain_held_out_windows(self) -> None:
        extra = letters_az((_DATA / "neural_train_public.txt").read_text(encoding="utf-8"))
        full = letters_az(load_training_prose(TRAIN_PATH)) + extra
        held = letters_az(load_training_prose(HELD_EN_PATH))
        wells = letters_az((_DATA / "neural_audit_wells.txt").read_text(encoding="utf-8"))
        grimm = letters_az((_DATA / "neural_heldout_grimm_wolf.txt").read_text(encoding="utf-8"))
        self.assertGreater(len(extra), 1_000_000)
        assert_split(full, held)
        assert_split(full, wells)
        assert_split(full, grimm)
        assert_certificate_plaintexts_excluded(full)


if __name__ == "__main__":
    unittest.main()
