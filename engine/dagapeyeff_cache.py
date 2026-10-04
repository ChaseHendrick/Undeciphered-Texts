"""Frozen swarm results, so a later hash does not repeat the search.

The file is the measurement. A hash of it is a recomputation of the hash,
not of the search, and not a reading. No letter string is stored.
"""

from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

_DIR = Path(__file__).resolve().parent / "data" / "swarm_cache"


def remember(name: str, compute):
    """Return the stored result for this name, or compute it and store it."""
    path = _DIR / f"{name}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    value = compute()
    _DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return value


def frozen(name: str):
    """Store a report on disk. Later calls read it instead of searching again."""

    def decorate(fn):
        @lru_cache(maxsize=1)
        def wrapper():
            return remember(name, fn)

        return wrapper

    return decorate

