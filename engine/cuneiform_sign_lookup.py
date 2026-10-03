"""Lookup of published Sumero-Akkadian sign values.

This is a sign-list lookup, not a decipherment. It returns readings already
published in a small excerpt of the Oracc Sign List (OSL). It does not assign
values to undeciphered tablets, unknown scripts, or signs that are absent
from that excerpt.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any

_DATA = Path(__file__).resolve().parent / "data" / "cuneiform_osl_excerpt.json"

# Machine-readable OSL file cited by Unicode Technical Report #56.
SOURCE_URL = "https://github.com/oracc/osl/blob/master/00lib/osl.asl"
PINNED_URL = (
    "https://github.com/oracc/osl/blob/"
    "dcee28e57d9387638c122e3435a98ceb6ea9e5e2/00lib/osl.asl"
)


@lru_cache(maxsize=1)
def load_sign_list() -> dict[str, Any]:
    """Load the pinned OSL excerpt. Values are copied, not inferred."""
    with _DATA.open(encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict) or "signs" not in data:
        raise ValueError(f"excerpt is not an OSL sign list: {_DATA}")
    return data


def source() -> dict[str, Any]:
    """Citation for the excerpt, including the real sign-list URL."""
    data = load_sign_list()
    cited = dict(data["source"])
    cited["url"] = SOURCE_URL
    cited["pinned_url"] = PINNED_URL
    return cited


def lookup_sign(name: str) -> dict[str, Any] | None:
    """Return one known sign by its OSL name, or None if it is not in the excerpt.

    A missing sign is not a proposal. Callers must not treat None as a reading.
    """
    key = name.strip()
    for sign in load_sign_list()["signs"]:
        if sign["name"] == key:
            return dict(sign)
    return None


def lookup_value(value: str) -> list[dict[str, Any]]:
    """Return known signs that publish this reading, or an empty list.

    Matching is exact against the OSL ``@v`` field, including index digits
    and uncertainty marks. An empty list means the excerpt has no such value.
    It does not mean the value was deciphered or ruled out for a tablet.
    """
    key = value.strip()
    found: list[dict[str, Any]] = []
    for sign in load_sign_list()["signs"]:
        if key in sign["values"]:
            found.append(dict(sign))
    return found
