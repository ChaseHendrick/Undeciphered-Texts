"""Gardiner-sign lookup over a tiny Unicode Egyptian Hieroglyphs subset.

Egyptian is a known (deciphered) script. This module only returns rows from a
cited Unicode chart subset. It is a known-sign dictionary lookup, not a new
decipherment, and it does not read damaged or unknown inscriptions.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

_DATA_PATH = Path(__file__).resolve().parent / "data" / "gardiner_sign_subset.json"

# Explicit so callers/tests see the honesty bar without reading prose.
KNOWN_SIGN_LOOKUP_ONLY = True
NOT_A_NEW_DECIPHERMENT = True


@dataclass(frozen=True)
class GardinerSign:
    """One Gardiner code from the sourced Unicode subset."""

    code: str
    unicode: str
    unicode_hex: str
    name: str
    gloss: str


class UnknownGardinerSignError(KeyError):
    """Raised when a token is not in the loaded subset."""


@lru_cache(maxsize=1)
def _table() -> tuple[dict[str, GardinerSign], dict[str, GardinerSign], str]:
    payload = json.loads(_DATA_PATH.read_text(encoding="utf-8"))
    by_code: dict[str, GardinerSign] = {}
    by_unicode: dict[str, GardinerSign] = {}
    for row in payload["signs"]:
        entry = GardinerSign(
            code=row["code"],
            unicode=row["unicode"],
            unicode_hex=row["unicode_hex"],
            name=row["name"],
            gloss=row["gloss"],
        )
        by_code[entry.code.upper()] = entry
        by_unicode[entry.unicode] = entry
    return by_code, by_unicode, payload.get("source_url", "")


def source_url() -> str:
    """Return the cited Unicode chart URL for the subset table."""
    return _table()[2]


def lookup(sign: str) -> GardinerSign:
    """Return the subset row for one Gardiner code or Unicode hieroglyph.

    Accepts codes like ``A1`` / ``a1`` or a single Egyptian hieroglyph character.
    Does not segment phrases or invent readings outside the table.
    """
    if not isinstance(sign, str):
        raise TypeError("sign must be a string")
    raw = sign.strip()
    if not raw:
        raise UnknownGardinerSignError("empty sign token")
    by_code, by_unicode, _ = _table()
    if raw in by_unicode:
        return by_unicode[raw]
    if len(raw) == 1 and 0x13000 <= ord(raw) <= 0x1342F:
        raise UnknownGardinerSignError(f"Unicode hieroglyph not in subset: {raw!r}")
    key = raw.upper()
    if key in by_code:
        return by_code[key]
    raise UnknownGardinerSignError(f"Gardiner code not in subset: {raw!r}")
