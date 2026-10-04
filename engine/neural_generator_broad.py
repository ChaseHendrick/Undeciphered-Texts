"""Broadened Enigma and M-209 sampler for a frozen incumbent probe.

engine.neural_grade.encrypt_family still trains on four Enigma rotor orders
with an empty plugboard, and on M-209 messages that keep the published
Bouchaudy pins and lugs. This module does not replace that generator, does
not train, and does not write engine/data/neural_router_v2_weights.json.

Scores from evaluate_incumbent are family labels on synthetic machine
settings. They are not a decipherment and they do not recover plaintext.
"""

from __future__ import annotations

import hashlib
import itertools
import json
import random
import time
from pathlib import Path

from engine.solvers.enigma import enigma_decrypt, enigma_encrypt, parse_plugboard
from engine.solvers.m209 import (
    BOUCHAUDY_LUGS,
    BOUCHAUDY_PINS,
    WHEEL_ALPHABETS,
    WHEEL_SIZES,
    lugs_from_specs,
    m209_decrypt,
    m209_encrypt,
)

_WEIGHTS_PATH = Path(__file__).resolve().parent / "data" / "neural_router_v2_weights.json"
_WINDOW = 180
_LUG_RESAMPLE_BOUND = 8
_PIN_RESAMPLE_BOUND = 8
_N_BARS = len(BOUCHAUDY_LUGS)
_BASIC_ROTORS = frozenset({"I", "II", "III"})
_ROTOR_NAMES = ("I", "II", "III", "IV", "V")
# Every ordered triple, no repeated rotor. itertools order is stable.
_ALL_ROTOR_ORDERS = tuple(itertools.permutations(_ROTOR_NAMES, 3))
# The four orders encrypt_family actually draws, in that same sequence.
_OLD_ROTOR_ORDERS = (
    ("I", "II", "III"),
    ("II", "I", "III"),
    ("III", "II", "I"),
    ("I", "III", "II"),
)
_REFLECTORS = ("B", "C")
# 0 is an empty lug. A nonzero wheel may not be used on both lugs of one bar.
_LEGAL_LUG_SPECS = tuple(
    f"{left}-{right}"
    for left in range(7)
    for right in range(7)
    if left == 0 or left != right
)


def _require_letters(plaintext: str) -> str:
    if not isinstance(plaintext, str) or not plaintext:
        raise ValueError("plaintext must be normalized A-Z letters")
    if any(not ("A" <= char <= "Z") for char in plaintext):
        raise ValueError("plaintext must be normalized A-Z letters")
    return plaintext


def _three_letters(rng: random.Random) -> str:
    """Match neural_grade._random_word(rng, 3, 3), including the length draw."""
    length = rng.randint(3, 3)
    return "".join(chr(65 + rng.randrange(26)) for _ in range(length))


def _sample_plugboard(rng: random.Random) -> list[str]:
    """0 to 6 disjoint pairs. Each pair is two different unused letters."""
    count = rng.randint(0, 6)
    pool = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    rng.shuffle(pool)
    pairs = [
        "".join(sorted((pool[2 * index], pool[2 * index + 1])))
        for index in range(count)
    ]
    pairs.sort()
    parse_plugboard(pairs)
    return pairs


def _external_key(rng: random.Random) -> str:
    """One letter from each wheel alphabet, same draws as encrypt_family."""
    return "".join(rng.choice(alphabet) for alphabet in WHEEL_ALPHABETS)


def _sample_pin_patterns(rng: random.Random) -> tuple[str, ...]:
    """One pattern per wheel. Lengths come from WHEEL_SIZES, not a guess.

    Each wheel is drawn as a 0/1 string of that length. m209_encrypt stores
    an active pin as the wheel's own letter and an inactive pin as '_', so
    the returned patterns use that form. An all-zero wheel is rejected by
    turning one pin on. The published Bouchaudy patterns are not copied.
    """
    for _attempt in range(_PIN_RESAMPLE_BOUND):
        patterns: list[str] = []
        for alphabet, size in zip(WHEEL_ALPHABETS, WHEEL_SIZES):
            if len(alphabet) != size:
                raise RuntimeError("M-209 wheel alphabet and WHEEL_SIZES disagree")
            bits = [rng.randrange(2) for _ in range(size)]
            if not any(bits):
                bits[rng.randrange(size)] = 1
            patterns.append(
                "".join(
                    alphabet[index] if bits[index] else "_" for index in range(size)
                )
            )
        found = tuple(patterns)
        if found != tuple(BOUCHAUDY_PINS):
            return found
    raise RuntimeError("pin sampler stayed on the Bouchaudy patterns")


def _sample_lugs(rng: random.Random) -> tuple[str, ...]:
    """27 legal lug specs. At least one lug is active. Not BOUCHAUDY_LUGS."""
    if _N_BARS != 27:
        raise RuntimeError("M-209 lug list is no longer 27 bars")
    for _attempt in range(_LUG_RESAMPLE_BOUND):
        specs = tuple(rng.choice(_LEGAL_LUG_SPECS) for _ in range(_N_BARS))
        if specs == tuple(BOUCHAUDY_LUGS):
            continue
        if any(spec != "0-0" for spec in specs):
            lugs_from_specs(specs)
            return specs
    raise RuntimeError("lug sampler exceeded its resample bound")


def sample_enigma(rng: random.Random, plaintext: str) -> tuple[dict[str, object], str]:
    """Draw a legal three-rotor key and return ``(settings, ciphertext)``.

    Rotors are an ordered triple from I, II, III, IV, V with no repeats.
    The reflector is B or C. Rings and positions are three A-Z letters.
    The plugboard has 0 to 6 disjoint pairs, as a list of two-letter
    strings (empty list when there are none). ``settings`` is the keyword
    map ``enigma_encrypt`` and ``enigma_decrypt`` already accept.
    """
    text = _require_letters(plaintext)
    rotors = rng.choice(_ALL_ROTOR_ORDERS)
    reflector = rng.choice(_REFLECTORS)
    settings: dict[str, object] = {
        "rotors": rotors,
        "reflector": reflector,
        "rings": _three_letters(rng),
        "positions": _three_letters(rng),
        "plugboard": _sample_plugboard(rng),
    }
    ciphertext = enigma_encrypt(text, **settings)
    return settings, ciphertext


def sample_restricted_enigma(
    rng: random.Random, plaintext: str
) -> tuple[dict[str, object], str]:
    """Reproduce the training Enigma draw: four orders, reflector B, no plugs.

    Random calls match ``encrypt_family``: ``choice`` of the four orders,
    then rings and positions via the same ``randint(3, 3)`` plus three
    ``randrange(26)`` draws each. The plugboard is an empty list.
    """
    text = _require_letters(plaintext)
    settings: dict[str, object] = {
        "rotors": rng.choice(_OLD_ROTOR_ORDERS),
        "reflector": "B",
        "rings": _three_letters(rng),
        "positions": _three_letters(rng),
        "plugboard": [],
    }
    ciphertext = enigma_encrypt(
        text,
        rotors=settings["rotors"],
        reflector="B",
        rings=settings["rings"],
        positions=settings["positions"],
        plugboard=[],
    )
    return settings, ciphertext


def sample_m209(rng: random.Random, plaintext: str) -> tuple[dict[str, object], str]:
    """Draw a legal M-209 key and return ``(settings, ciphertext)``.

    ``settings`` uses the ``m209_encrypt`` parameter names ``external_key``,
    ``pin_patterns`` and ``lug_specs``.
    """
    text = _require_letters(plaintext)
    external = _external_key(rng)
    pins = _sample_pin_patterns(rng)
    lugs = _sample_lugs(rng)
    ciphertext = m209_encrypt(text, external, pins, lugs)
    settings: dict[str, object] = {
        "external_key": external,
        "pin_patterns": pins,
        "lug_specs": lugs,
    }
    return settings, ciphertext


def sample_restricted_m209(
    rng: random.Random, plaintext: str
) -> tuple[dict[str, object], str]:
    """Reproduce the training M-209 draw: random external key, fixed pins and lugs."""
    text = _require_letters(plaintext)
    external = _external_key(rng)
    ciphertext = m209_encrypt(text, external, BOUCHAUDY_PINS, BOUCHAUDY_LUGS)
    settings: dict[str, object] = {
        "external_key": external,
        "pin_patterns": BOUCHAUDY_PINS,
        "lug_specs": BOUCHAUDY_LUGS,
    }
    return settings, ciphertext


def _require_roundtrip(
    family: str, settings: dict[str, object], ciphertext: str, plaintext: str
) -> None:
    if family == "enigma":
        recovered = enigma_decrypt(ciphertext, **settings)
    elif family == "m209":
        recovered = m209_decrypt(ciphertext, **settings)
    else:
        raise ValueError(f"unknown family {family}")
    if recovered != plaintext:
        raise RuntimeError("sample did not roundtrip to the plaintext letters")


def _sample_plaintext(letters: str, index: int) -> str:
    """Use a short excerpt whole. Longer text is cut into 180-letter windows."""
    if len(letters) <= _WINDOW:
        return letters
    start = (index * 37) % (len(letters) - _WINDOW + 1)
    return letters[start : start + _WINDOW]


def _family_counts() -> dict[str, int]:
    return {"top1_correct": 0, "top3_correct": 0, "total": 0}


def _score_rows(rows: list[tuple[str, dict[str, object], str]]) -> dict[str, object]:
    from engine.neural_router_v2 import route_probabilities

    per_family = {"enigma": _family_counts(), "m209": _family_counts()}
    for family, _settings, ciphertext in rows:
        ranked = [
            item["family"]
            for item in route_probabilities(ciphertext, weights_path=_WEIGHTS_PATH)[
                "candidates"
            ]
        ]
        bucket = per_family[family]
        bucket["total"] += 1
        if ranked and ranked[0] == family:
            bucket["top1_correct"] += 1
        if family in ranked[:3]:
            bucket["top3_correct"] += 1
    return {
        "top1_correct": sum(item["top1_correct"] for item in per_family.values()),
        "top3_correct": sum(item["top3_correct"] for item in per_family.values()),
        "total": sum(item["total"] for item in per_family.values()),
        "per_family": per_family,
    }


def _broad_diagnostics(rows: list[tuple[str, dict[str, object], str]]) -> dict[str, int]:
    nonempty_plugboard = 0
    outer_rotor = 0
    both = 0
    pins_differ = 0
    for family, settings, _ciphertext in rows:
        if family == "enigma":
            rotors = settings["rotors"]
            has_outer = any(name not in _BASIC_ROTORS for name in rotors)
            has_plugs = bool(settings["plugboard"])
            nonempty_plugboard += int(has_plugs)
            outer_rotor += int(has_outer)
            both += int(has_plugs and has_outer)
        elif family == "m209":
            pins_differ += int(
                tuple(settings["pin_patterns"]) != tuple(BOUCHAUDY_PINS)
            )
    return {
        "enigma_nonempty_plugboard": nonempty_plugboard,
        "enigma_rotor_outside_i_ii_iii": outer_rotor,
        "enigma_nonempty_plugboard_and_outer_rotor": both,
        "m209_pins_differ_from_bouchaudy": pins_differ,
    }


def _weights_sha256() -> str:
    return hashlib.sha256(_WEIGHTS_PATH.read_bytes()).hexdigest()


def evaluate_incumbent(
    plaintext: str, *, seed: int, per_family: int
) -> dict[str, object]:
    """Score the shipped router on restricted and broad Enigma and M-209 draws.

    ``plaintext`` is already normalized A-Z. One ``random.Random(seed)``
    draws restricted Enigma, restricted M-209, broad Enigma, then broad
    M-209, ``per_family`` times each. Texts of 16 to 180 letters are reused
    for every sample. Longer texts use 180-letter windows.

    The returned counts are top-1 and top-3 family hits. Nothing is written.
    ``route_probabilities`` is read-only. This is not training and not a
    decipherment.
    """
    letters = _require_letters(plaintext)
    if len(letters) < 16:
        raise ValueError("plaintext needs at least 16 letters")
    if isinstance(seed, bool) or not isinstance(seed, int) or seed < 0:
        raise ValueError("seed must be a nonnegative integer")
    if isinstance(per_family, bool) or not isinstance(per_family, int) or per_family < 1:
        raise ValueError("per_family must be a positive integer")
    before = _weights_sha256()
    format_version = json.loads(_WEIGHTS_PATH.read_text(encoding="utf-8"))[
        "format_version"
    ]
    rng = random.Random(seed)
    texts = [_sample_plaintext(letters, index) for index in range(per_family)]
    restricted: list[tuple[str, dict[str, object], str]] = []
    broad: list[tuple[str, dict[str, object], str]] = []
    for text in texts:
        settings, ciphertext = sample_restricted_enigma(rng, text)
        if settings["plugboard"] != [] or settings["rotors"] not in _OLD_ROTOR_ORDERS:
            raise RuntimeError("restricted Enigma draw left the old generator")
        if settings["reflector"] != "B":
            raise RuntimeError("restricted Enigma reflector is not B")
        _require_roundtrip("enigma", settings, ciphertext, text)
        restricted.append(("enigma", settings, ciphertext))
    for text in texts:
        settings, ciphertext = sample_restricted_m209(rng, text)
        if tuple(settings["pin_patterns"]) != tuple(BOUCHAUDY_PINS):
            raise RuntimeError("restricted M-209 pins are not the Bouchaudy pins")
        if tuple(settings["lug_specs"]) != tuple(BOUCHAUDY_LUGS):
            raise RuntimeError("restricted M-209 lugs are not the Bouchaudy lugs")
        _require_roundtrip("m209", settings, ciphertext, text)
        restricted.append(("m209", settings, ciphertext))
    for text in texts:
        settings, ciphertext = sample_enigma(rng, text)
        _require_roundtrip("enigma", settings, ciphertext, text)
        broad.append(("enigma", settings, ciphertext))
    for text in texts:
        settings, ciphertext = sample_m209(rng, text)
        _require_roundtrip("m209", settings, ciphertext, text)
        broad.append(("m209", settings, ciphertext))
    started = time.perf_counter()
    restricted_counts = _score_rows(restricted)
    broad_counts = _score_rows(broad)
    broad_counts.update(_broad_diagnostics(broad))
    elapsed = time.perf_counter() - started
    after = _weights_sha256()
    if before != after:
        raise RuntimeError("incumbent weights changed during evaluation")
    return {
        "kind": "broad_generator_family_probe",
        "seed": seed,
        "per_family": per_family,
        "plaintext_letters": len(letters),
        "plaintext_sha256": hashlib.sha256(letters.encode("utf-8")).hexdigest(),
        "window": min(_WINDOW, len(letters)),
        "format_version": format_version,
        "weights_path": "engine/data/neural_router_v2_weights.json",
        "weights_sha256": before,
        "weights_unchanged": True,
        "incumbent_replaced": False,
        "elapsed_seconds": elapsed,
        "restricted": restricted_counts,
        "broad": broad_counts,
        "scope": (
            "Family recognition on synthetic machine settings. "
            "The incumbent was not replaced. This is not a decipherment."
        ),
    }


def probe_manifest(plaintext: str, *, seed: int, per_family: int) -> dict[str, object]:
    """Hash each draw and record the frozen router's top family.

    One ``random.Random(seed)`` draws in the same order as
    ``evaluate_incumbent``. The plaintext and the keys are not stored.
    The weight file is only read. This is not a training run.
    """
    letters = _require_letters(plaintext)
    if len(letters) < 16:
        raise ValueError("plaintext needs at least 16 letters")
    before = _weights_sha256()
    format_version = json.loads(_WEIGHTS_PATH.read_text(encoding="utf-8"))["format_version"]
    rng = random.Random(seed)
    texts = [_sample_plaintext(letters, index) for index in range(per_family)]
    draws: list[tuple[str, str, str]] = []
    for text in texts:
        settings, ciphertext = sample_restricted_enigma(rng, text)
        _require_roundtrip("enigma", settings, ciphertext, text)
        draws.append(("restricted", "enigma", ciphertext))
    for text in texts:
        settings, ciphertext = sample_restricted_m209(rng, text)
        _require_roundtrip("m209", settings, ciphertext, text)
        draws.append(("restricted", "m209", ciphertext))
    for text in texts:
        settings, ciphertext = sample_enigma(rng, text)
        _require_roundtrip("enigma", settings, ciphertext, text)
        draws.append(("broad", "enigma", ciphertext))
    for text in texts:
        settings, ciphertext = sample_m209(rng, text)
        _require_roundtrip("m209", settings, ciphertext, text)
        draws.append(("broad", "m209", ciphertext))
    from engine.neural_router_v2 import route_probabilities

    rows = []
    for generator, family, ciphertext in draws:
        ranked = [
            item["family"]
            for item in route_probabilities(ciphertext, weights_path=_WEIGHTS_PATH)["candidates"]
        ]
        rows.append({
            "generator": generator,
            "family": family,
            "ciphertext_sha256": hashlib.sha256(ciphertext.encode("utf-8")).hexdigest(),
            "top1": ranked[0] if ranked else "",
            "in_top3": family in ranked[:3],
        })
    after = _weights_sha256()
    if before != after:
        raise RuntimeError("incumbent weights changed during the manifest")

    def _hits(generator: str) -> int:
        return sum(
            row["top1"] == row["family"]
            for row in rows
            if row["generator"] == generator
        )

    return {
        "kind": "bob_probe_manifest",
        "seed": seed,
        "per_family": per_family,
        "format_version": format_version,
        "weights_sha256": before,
        "weights_unchanged": True,
        "incumbent_replaced": False,
        "plaintext_sha256": hashlib.sha256(letters.encode("utf-8")).hexdigest(),
        "rows": rows,
        "restricted_top1": _hits("restricted"),
        "broad_top1": _hits("broad"),
        "scope": "Hashes and family labels for one frozen incumbent. Not a weight update.",
    }


__all__ = [
    "evaluate_incumbent",
    "probe_manifest",
    "sample_enigma",
    "sample_m209",
    "sample_restricted_enigma",
    "sample_restricted_m209",
]
