"""Frozen swarm results, so a later hash does not repeat the search.

The file is the measurement. A hash of it is a recomputation of the hash,
not of the search, and not a reading. No letter string is stored.

The unit tests read these files and do not rerun the search. Run
`python3 tools/verify_cache.py` to rerun each search and compare it with
its file.
"""

from __future__ import annotations

import importlib
import json
import pkgutil
from functools import lru_cache
from pathlib import Path

_DIR = Path(__file__).resolve().parent / "data" / "swarm_cache"
_ENGINE = Path(__file__).resolve().parent

# name -> (module, function name). Filled as modules that use @frozen import.
_REGISTRY: dict[str, tuple[str, str]] = {}


def remember(name: str, compute):
    """Return the stored result for this name, or compute it and store it."""
    path = _DIR / f"{name}.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    text = json.dumps(compute(), indent=2, sort_keys=True) + "\n"
    _DIR.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    # The first call returns what later calls will read, not the raw tuples and keys.
    return json.loads(text)


def frozen(name: str):
    """Store a report on disk. Later calls read it instead of searching again."""

    def decorate(fn):
        where = (fn.__module__, fn.__name__)
        if _REGISTRY.setdefault(name, where) != where:
            raise ValueError(f"frozen name {name!r} is already used by {_REGISTRY[name][0]}")

        @lru_cache(maxsize=1)
        def wrapper():
            return remember(name, fn)

        wrapper.cache_name = name
        wrapper.compute = fn
        return wrapper

    return decorate


def stored_names() -> list[str]:
    """Names of the frozen files on disk."""
    return sorted(path.stem for path in _DIR.glob("*.json"))


def frozen_registry() -> dict[str, tuple[str, str]]:
    """Import every engine module that uses @frozen and return name -> (module, function)."""
    for info in pkgutil.iter_modules([str(_ENGINE)]):
        source = _ENGINE / f"{info.name}.py"
        if source.exists() and "@frozen(" in source.read_text(encoding="utf-8"):
            importlib.import_module(f"engine.{info.name}")
    return dict(sorted(_REGISTRY.items()))
