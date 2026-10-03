"""The error writer appends only when called. It does not invent failures."""

from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from engine import errors


class ErrorLogTest(unittest.TestCase):
    def test_append_writes_the_four_fields(self) -> None:
        with TemporaryDirectory() as tmp:
            path = Path(tmp) / "errors.md"
            with patch.object(errors, "LOG", path):
                errors.append_error("python -m engine demo", "caesar mismatch", "no")
            text = path.read_text(encoding="utf-8")
            self.assertIn("**command:** python -m engine demo", text)
            self.assertIn("**failure:** caesar mismatch", text)
            self.assertIn("**retried:** no", text)
            self.assertIn("**date:**", text)


if __name__ == "__main__":
    unittest.main()
