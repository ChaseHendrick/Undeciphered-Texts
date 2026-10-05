"""The skill runs the solvers on a ciphertext someone brings."""

from __future__ import annotations

import unittest
from pathlib import Path

_SKILL = Path(__file__).resolve().parents[1] / ".claude" / "skills" / "unsolved-attack" / "SKILL.md"


class UnsolvedSkillTest(unittest.TestCase):
    def test_the_skill_solves_a_cipher_the_user_brings(self) -> None:
        text = _SKILL.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: unsolved-attack\n"))
        self.assertIn("Solve a ciphertext someone brings", text)
        self.assertIn("python3 -m engine solve caesar", text)
        self.assertIn("python3 -m engine solve vigenere", text)
        self.assertIn("python3 -m engine solve substitution", text)
        self.assertIn("Do not invent a plaintext the solvers did not return", text)
        self.assertIn("catalogued unread cipher", text)
        self.assertNotIn("\u2014", text)
        self.assertNotIn("\u2013", text)


if __name__ == "__main__":
    unittest.main()
