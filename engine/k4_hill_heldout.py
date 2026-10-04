"""Bounded 2x2 Hill heldout on K4. Not a decipherment.

Fold A fits EASTNORTHEAST only and then looks for BERLINCLOCK at offset 63.
Fold B reverses that. The reserved crib is not passed to the fitter.
K4 has 97 letters. `infer_hill` requires complete two-letter blocks and does
not pad. That rejection is recorded. `solved` stays false and
`claimed_plaintext` stays None. A reserved match would be unverified.
"""

from __future__ import annotations

from engine.reverse_engineer import Crib
from engine.solvers.hill_inference import infer_hill
from engine.solvers.k4_attempt import CRIBS, K4_CIPHERTEXT

# Zero-based public cribs. EAST begins at 1-based 22; BERLIN at 1-based 64.
EASTNORTHEAST = Crib(21, "EASTNORTHEAST")
BERLINCLOCK = Crib(63, "BERLINCLOCK")

# infer_hill validates max_checks in 0..100000 and max_candidates in 1..100.
_MAX_CHECKS = 100000
_MAX_CANDIDATES = 20
_UNVERIFIED_CAP = 20


def _assert_public_alignment() -> None:
    """Fail closed if the joined cribs are not the published K4 spans."""
    by_word = {word: (start, cipher) for start, word, cipher in CRIBS}
    east_start, east_cipher = by_word["EAST"]
    north_start, north_cipher = by_word["NORTHEAST"]
    berlin_start, berlin_cipher = by_word["BERLIN"]
    clock_start, clock_cipher = by_word["CLOCK"]
    if east_start != 22 or north_start != east_start + len("EAST"):
        raise ValueError("EAST and NORTHEAST are not contiguous published cribs")
    if berlin_start != 64 or clock_start != berlin_start + len("BERLIN"):
        raise ValueError("BERLIN and CLOCK are not contiguous published cribs")
    if K4_CIPHERTEXT[21:34] != east_cipher + north_cipher:
        raise ValueError("EASTNORTHEAST span does not match the K4 ciphertext")
    if K4_CIPHERTEXT[63:74] != berlin_cipher + clock_cipher:
        raise ValueError("BERLINCLOCK span does not match the K4 ciphertext")


def _word(crib: Crib) -> str:
    return "".join(ch.upper() for ch in crib.plaintext if ch.isalpha())


def _reserved_hits(candidates: list[dict], reserved: Crib) -> list[dict]:
    word = _word(reserved)
    start = reserved.offset
    end = start + len(word)
    hits = []
    for candidate in candidates:
        plain = candidate.get("plaintext")
        if not isinstance(plain, str) or len(plain) < end:
            continue
        if plain[start:end] != word:
            continue
        hits.append(
            {
                "status": "unverified",
                "plaintext": plain,
                "reserved_crib": word,
                "reserved_offset": start,
                "key": candidate.get("key"),
                "matrix": candidate.get("matrix"),
            }
        )
    return hits


def _fold(
    name: str,
    fitted: Crib,
    reserved: Crib,
    *,
    max_checks: int,
    max_candidates: int,
) -> dict:
    """Fit one crib. Compare the other only to whatever infer_hill returns."""
    base = {
        "fold": name,
        "fitted": _word(fitted),
        "fitted_offset": fitted.offset,
        "reserved": _word(reserved),
        "reserved_offset": reserved.offset,
        "reserved_passed_to_fitter": False,
        "candidates_checked": 0,
        "reserved_matches": 0,
        "checks": 0,
        "search_ran": False,
        "limitation": None,
        "unverified": [],
    }
    try:
        # Only the fitted crib is supplied. The reserved crib stays out.
        report = infer_hill(
            K4_CIPHERTEXT,
            cribs=(fitted,),
            max_checks=max_checks,
            max_candidates=max_candidates,
        )
    except (ValueError, IndexError) as exc:
        base["limitation"] = str(exc)
        return base

    candidates = list(report.get("candidates") or [])
    hits = _reserved_hits(candidates, reserved)
    base.update(
        {
            "candidates_checked": len(candidates),
            "reserved_matches": len(hits),
            "checks": report.get("checks", 0),
            "search_ran": True,
            "limitation": None,
            "candidates_truncated": bool(report.get("candidates_truncated")),
            "search_complete": report.get("search_complete"),
            "stop_reason": report.get("stop_reason"),
            "unverified": hits,
        }
    )
    return base


def search_k4_hill_heldout(
    *,
    max_checks: int = _MAX_CHECKS,
    max_candidates: int = _MAX_CANDIDATES,
) -> dict:
    """Run both heldout folds. Odd-length rejection is a limitation, not a crash.

    `max_checks` must stay in 0..100000, the range `infer_hill` accepts.
    """
    if isinstance(max_checks, bool) or not isinstance(max_checks, int):
        raise TypeError("max_checks must be an integer")
    if not 0 <= max_checks <= 100000:
        raise ValueError("max_checks must be in 0..100000")
    if isinstance(max_candidates, bool) or not isinstance(max_candidates, int):
        raise TypeError("max_candidates must be an integer")
    if not 1 <= max_candidates <= 100:
        raise ValueError("max_candidates must be in 1..100")

    _assert_public_alignment()
    folds = [
        _fold(
            "A",
            EASTNORTHEAST,
            BERLINCLOCK,
            max_checks=max_checks,
            max_candidates=max_candidates,
        ),
        _fold(
            "B",
            BERLINCLOCK,
            EASTNORTHEAST,
            max_checks=max_checks,
            max_candidates=max_candidates,
        ),
    ]
    unverified: list[dict] = []
    for fold in folds:
        for hit in fold["unverified"]:
            if len(unverified) >= _UNVERIFIED_CAP:
                break
            unverified.append(hit)
    limitations = [fold["limitation"] for fold in folds if fold["limitation"]]
    if not limitations:
        limitation = None
    elif all(item == limitations[0] for item in limitations):
        limitation = limitations[0]
    else:
        limitation = " | ".join(limitations)

    return {
        "claimed_plaintext": None,
        "solved": False,
        "candidates_checked": sum(fold["candidates_checked"] for fold in folds),
        "reserved_matches": sum(fold["reserved_matches"] for fold in folds),
        "checks": sum(fold["checks"] for fold in folds),
        "folds": folds,
        "unverified": unverified,
        "unverified_cap": _UNVERIFIED_CAP,
        "limitation": limitation,
        "max_checks": max_checks,
        "max_candidates": max_candidates,
        "ciphertext_letters": len(K4_CIPHERTEXT),
    }


def search_k4_hill_endpoints(
    *,
    max_checks: int = _MAX_CHECKS,
    max_candidates: int = _MAX_CANDIDATES,
) -> dict:
    """Fit 2x2 Hill after dropping one endpoint letter. No padding is added.

    `drop_last` uses the first 96 letters and the original crib offsets.
    `drop_first` uses the last 96 letters and shifts both crib offsets by -1.
    Both public cribs sit inside either window. The reserved crib is still
    withheld from the fitter. `solved` stays false.
    """
    if isinstance(max_checks, bool) or not isinstance(max_checks, int):
        raise TypeError("max_checks must be an integer")
    if not 0 <= max_checks <= 100000:
        raise ValueError("max_checks must be in 0..100000")
    if isinstance(max_candidates, bool) or not isinstance(max_candidates, int):
        raise TypeError("max_candidates must be an integer")
    if not 1 <= max_candidates <= 100:
        raise ValueError("max_candidates must be in 1..100")

    _assert_public_alignment()
    windows = (
        ("drop_last", K4_CIPHERTEXT[:96], EASTNORTHEAST, BERLINCLOCK, 0),
        (
            "drop_first",
            K4_CIPHERTEXT[1:],
            Crib(EASTNORTHEAST.offset - 1, EASTNORTHEAST.plaintext),
            Crib(BERLINCLOCK.offset - 1, BERLINCLOCK.plaintext),
            -1,
        ),
    )
    folds = []
    unverified: list[dict] = []
    for window, text, east, berlin, shift in windows:
        for name, fitted, reserved in (("A", east, berlin), ("B", berlin, east)):
            report = infer_hill(
                text,
                cribs=(fitted,),
                max_checks=max_checks,
                max_candidates=max_candidates,
            )
            hits = _reserved_hits(list(report.get("candidates") or []), reserved)
            for hit in hits:
                hit["window"] = window
                hit["offset_shift"] = shift
            fold = {
                "window": window,
                "fold": name,
                "letters": len(text),
                "excluded": "final letter" if window == "drop_last" else "first letter",
                "fitted": _word(fitted),
                "fitted_offset": fitted.offset,
                "reserved": _word(reserved),
                "reserved_offset": reserved.offset,
                "reserved_passed_to_fitter": False,
                "candidates_checked": len(report.get("candidates") or []),
                "reserved_matches": len(hits),
                "checks": report.get("checks", 0),
                "compatible_keys_seen": report.get("compatible_keys_seen"),
                "search_complete": report.get("search_complete"),
                "stop_reason": report.get("stop_reason"),
                "unverified": hits,
            }
            folds.append(fold)
            for hit in hits:
                if len(unverified) < _UNVERIFIED_CAP:
                    unverified.append(hit)
    return {
        "claimed_plaintext": None,
        "solved": False,
        "window_letters": 96,
        "padding": False,
        "candidates_checked": sum(fold["candidates_checked"] for fold in folds),
        "reserved_matches": sum(fold["reserved_matches"] for fold in folds),
        "checks": sum(fold["checks"] for fold in folds),
        "folds": folds,
        "unverified": unverified,
        "scope": "One endpoint letter excluded so the remainder has even length. Not a padded 97-letter Hill model, and not a historical plaintext.",
    }


__all__ = [
    "search_k4_hill_heldout",
    "search_k4_hill_endpoints",
    "EASTNORTHEAST",
    "BERLINCLOCK",
]
