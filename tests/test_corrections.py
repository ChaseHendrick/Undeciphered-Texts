"""Retracted claims are searchable and none of them is a reading."""

from __future__ import annotations

import unittest

from engine.corrections import load_corrections, search_corrections


class CorrectionsTest(unittest.TestCase):
    def test_each_correction_is_findable_and_unsolved(self) -> None:
        data = load_corrections()
        self.assertEqual(data["schema"], "corrections-1")
        self.assertTrue(data["append_only"])
        ids = [record["id"] for record in data["records"]]
        self.assertEqual(
            ids,
            [
                "sorting-is-not-progress",
                "ioc-cutoff-too-low",
                "private-symbols-are-not-filler",
                "period-7-is-the-last-column",
                "seam-was-double-counted",
                "score-692-has-no-formula",
                "repair-04-to-75-is-worse",
                "not-the-lead-on-a-solution",
            ],
        )
        for record in data["records"]:
            self.assertIs(record["solved"], False)
            self.assertIsNone(record["claimed_plaintext"])
            self.assertTrue(search_corrections(record["id"]))
        self.assertEqual(search_corrections("filler")[0]["id"], "private-symbols-are-not-filler")
        self.assertEqual(search_corrections("-692.13")[0]["id"], "score-692-has-no-formula")
        self.assertEqual(search_corrections("49.23")[0]["id"], "not-the-lead-on-a-solution")
        self.assertEqual(search_corrections(""), [])


if __name__ == "__main__":
    unittest.main()
