"""Elder Futhark rune lookup (known inventory; not a decipherment).

Source: https://en.wikipedia.org/wiki/Elder_Futhark (retrieved 2026-10-02).

This module maps Unicode Elder Futhark glyphs to their conventional
transliteration, reconstructed Proto-Germanic name, and short gloss as
published for the 24-rune alphabet. It is a lookup of an already-known
script inventory. It does not decipher unknown inscriptions, assign
readings to undeciphered texts, or claim new readings of unreadable
artifacts.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

SOURCE_URL = "https://en.wikipedia.org/wiki/Elder_Futhark"
_DATA_PATH = Path(__file__).resolve().parent / "data" / "elder_futhark.json"


@lru_cache(maxsize=1)
def load_inventory() -> dict[str, Any]:
    """Load the sourced Elder Futhark inventory (UTF-8 JSON)."""
    with _DATA_PATH.open(encoding="utf-8") as fh:
        return json.load(fh)


def lookup(rune: str) -> dict[str, str] | None:
    """Return the sourced entry for one Elder Futhark rune, or None.

    Parameters
    ----------
    rune:
        A single Unicode character from the Elder Futhark inventory
        (for example ``ᚠ``).

    Returns
    -------
    dict or None
        Keys include ``rune``, ``unicode``, ``transliteration``,
        ``ipa``, ``name``, and ``meaning`` when the glyph is in the
        published inventory; ``None`` otherwise.
    """
    if len(rune) != 1:
        return None
    for entry in load_inventory()["runes"]:
        if entry["rune"] == rune:
            return dict(entry)
    return None


def transliterate(text: str) -> str:
    """Map known Elder Futhark runes to transliteration; leave others.

    Unknown characters (spaces, Latin letters, Younger Futhark, etc.)
    are passed through unchanged. This is string substitution against a
    known alphabet, not a decipherment of an undeciphered inscription.
    """
    out: list[str] = []
    for ch in text:
        entry = lookup(ch)
        out.append(entry["transliteration"] if entry else ch)
    return "".join(out)
