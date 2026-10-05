"""Scratch paper keeps short notes and refuses a letter string."""

from __future__ import annotations

import unittest

from engine.bob_scratch import open_pad, pad_digest, write_note


class BobScratchTest(unittest.TestCase):
    def test_a_letter_string_and_a_plaintext_field_are_refused(self) -> None:
        pad = open_pad()
        write_note(pad, step="route", family="caesar", key="5", score=1.5)
        with self.assertRaises(ValueError):
            write_note(pad, step="bad", note="A" * 20)
        with self.assertRaises(ValueError):
            write_note(pad, step="bad", plaintext="NO")
        self.assertEqual(len(pad), 1)
        self.assertEqual(pad_digest(pad), pad_digest([dict(pad[0])]))
        self.assertNotEqual(pad_digest(pad), pad_digest([]))


if __name__ == "__main__":
    unittest.main()
