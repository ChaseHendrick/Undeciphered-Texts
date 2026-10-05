"""The paper notes cite frozen scores and do not claim a reading."""

from __future__ import annotations

import unittest

from engine.paper_notes import paper_notes, search_notes


class PaperNotesTest(unittest.TestCase):
    def test_the_notes_are_searchable_and_unsolved(self) -> None:
        notes = paper_notes()
        self.assertEqual(notes["schema"], "paper-notes-1")
        self.assertIs(notes["solved"], False)
        self.assertIsNone(notes["claimed_plaintext"])
        self.assertEqual(len(notes["notes"]), 46)
        self.assertTrue(all(note["claimed_plaintext"] is None for note in notes["notes"] if "claimed_plaintext" in note))
        shared = search_notes("72")
        self.assertEqual(
            [note["id"] for note in shared],
            ["repairs-share-one-loss", "pair-72-window"],
        )
        branch = search_notes("residual")
        self.assertEqual([note["id"] for note in branch], ["residual-branch-is-alive"])
        self.assertEqual(search_notes(""), [])
        self.assertTrue(all("not a reading" in note["do_not_claim"].lower() or "not a reading" in note["do_not_claim"] or "not identified" in note["do_not_claim"] or "not a plaintext" in note["do_not_claim"] or "does not" in note["do_not_claim"] for note in notes["notes"]))


if __name__ == "__main__":
    unittest.main()
