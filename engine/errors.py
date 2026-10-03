"""Append a real solver failure to docs/logs/errors.md.

Success paths must not call this. Do not invent a failure in order to
exercise the writer.
"""

from __future__ import annotations

from datetime import datetime
from pathlib import Path

LOG = Path(__file__).resolve().parent.parent / "docs" / "logs" / "errors.md"


def append_error(command: str, failure: str, retried: str) -> Path:
    """Append one entry. `retried` is "no" or a short description of the retry."""
    stamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    block = (
        f"\n### {stamp} ET — solver failure\n\n"
        f"- **date:** {stamp} (ET)\n"
        f"- **command:** {command}\n"
        f"- **failure:** {failure}\n"
        f"- **retried:** {retried}\n"
    )
    if not LOG.exists():
        LOG.parent.mkdir(parents=True, exist_ok=True)
        LOG.write_text(
            "# Error log\n\n"
            "Append-only. One entry per real failure. "
            "The engine writes here only when a known-plaintext recovery fails.\n",
            encoding="utf-8",
        )
    with LOG.open("a", encoding="utf-8") as handle:
        handle.write(block)
    return LOG
