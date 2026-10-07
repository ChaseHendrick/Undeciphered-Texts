"""The four-square and repeating-shift searches again, under a second seed. Not a reading.

The paper's quality record left one item open: these searches had been run
under one seed each. This pass calls the same report functions with a new
seed, so every planted text, key, shuffle and search start is drawn afresh,
and compares the result with the frozen first run. The programs, budgets and
thresholds are unchanged.

Each probe is run in turn and kept in the ignored work/reseed/ folder, so a
stopped run resumes at the next probe. The frozen file keeps a summary of
both seeds, not the second run in full. Only four-square and the English
shift at periods 2 to 14 are frozen so far; the shift at periods 6 and 8 to 13
and the Latin searches are listed in PENDING. No letter string is stored.
"""

from __future__ import annotations

import importlib
import json
from pathlib import Path

from engine.dagapeyeff_cache import _DIR, frozen

# Probe name in the cache, module and report function. Recovery thresholds are the modules' own.
PROBES = (
    ("foursquare", "engine.dagapeyeff_foursquare", "foursquare_report"),
    ("additive", "engine.dagapeyeff_additive", "additive_report"),
)
# Not yet rerun: the session ended first. Run each with _second(), then move it to PROBES.
PENDING = (
    ("shiftgap", "engine.dagapeyeff_shiftgap", "shiftgap_report"),
    ("latin14", "engine.dagapeyeff_latin14", "latin14_report"),
    ("latinw", "engine.dagapeyeff_latinw", "latinw_report"),
    ("latinmore", "engine.dagapeyeff_latinmore", "latinmore_report"),
    ("latinshift", "engine.dagapeyeff_latinmore", "latinshift_report"),
)
# Probes holding more than one family, each summarised on its own because their scores differ in scale.
_PARTS = {"latinmore": ("foursquare", "homophone"), "shiftgap": ("english", "latin")}
# Added to each module's own seed, so no second run shares a first run's draws.
_OFFSET = 7_000_001
_WORK = Path(__file__).resolve().parents[1] / "work" / "reseed"


def _walk(node, path=()):
    if isinstance(node, dict):
        yield path, node
        for key, value in node.items():
            yield from _walk(value, path + (str(key),))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from _walk(value, path + (str(index),))


def summarise(result: dict, threshold: float) -> dict:
    """Planted recovery, the weakest recovered planted text, the cells' best score and the shuffle tally.

    A planted row is any dict with a true score and a share right; a searched row is any dict with a
    per-letter score and its shuffles. The searched rows include the regrouping where the probe ran it.
    """
    planted = recovered = 0
    weakest = None
    best = None
    as_high = shuffles = 0
    for _, row in _walk(result):
        right = row.get("letters_right", row.get("cells_right"))
        if "true_per_letter" in row and right is not None:
            planted += 1
            if right >= threshold:
                recovered += 1
                found = row.get("found_per_letter", row["true_per_letter"])
                weakest = found if weakest is None else min(weakest, found)
        if "per_letter" in row and isinstance(row.get("shuffles"), list):
            score = row["per_letter"]
            best = score if best is None else max(best, score)
            as_high += sum(value >= score for value in row["shuffles"])
            shuffles += len(row["shuffles"])
    return {
        "planted": planted,
        "recovered": recovered,
        "weakest_recovered": None if weakest is None else round(weakest, 4),
        "searched_best": None if best is None else round(best, 4),
        "gap": None if weakest is None or best is None else round(weakest - best, 4),
        "shuffles": shuffles,
        "shuffles_as_high": as_high,
    }


def _second(name: str, module_name: str, function: str) -> tuple[int, dict]:
    module = importlib.import_module(module_name)
    seed = module._SEED + _OFFSET
    path = _WORK / f"{name}.json"
    if path.exists():
        stored = json.loads(path.read_text(encoding="utf-8"))
        if stored["seed"] == seed:
            return seed, stored["result"]
    first_seed = module._SEED
    module._SEED = seed
    try:
        result = getattr(module, function).compute()
    finally:
        module._SEED = first_seed
    if result.get("solved") is not False or result.get("claimed_plaintext") is not None:
        raise RuntimeError(f"{name}: a second-seed run claims a reading")
    _WORK.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps({"seed": seed, "result": result}, sort_keys=True) + "\n", encoding="utf-8")
    return seed, result


@frozen("dagapeyeff-reseed")
def reseed_report() -> dict:
    rows = []
    for name, module_name, function in PROBES:
        module = importlib.import_module(module_name)
        threshold = module._RECOVERED
        first = json.loads((_DIR / f"dagapeyeff-{name}.json").read_text(encoding="utf-8"))
        seed, second = _second(name, module_name, function)
        for part in _PARTS.get(name, (None,)):
            rows.append({
                "probe": name if part is None else f"{name} {part}",
                "threshold": threshold,
                "first_seed": module._SEED,
                "second_seed": seed,
                "first": summarise(first if part is None else first[part], threshold),
                "second": summarise(second if part is None else second[part], threshold),
            })
    return {
        "solved": False,
        "claimed_plaintext": None,
        "offset": _OFFSET,
        "rows": rows,
        "cells_below_weakest_both": all(
            row[run]["gap"] is None or row[run]["gap"] > 0 for row in rows for run in ("first", "second")),
    }
