"""Preference for candidate sentences that use color, dream, and melting.

Persona: hallucinogens. The word list is a preference among candidates.
These are preferences among candidates, not decipherments of Nr. 86, K4,
or an unknown script.

The separate investigate_hallucinogens API tests bounded reverse/rotation
and affine compositions. Creative policy changes the models tested, never
the evidence required or the candidate's unverified status.
"""

from __future__ import annotations

import re

from engine.language import get_model
from engine.persona_solver_common import validate_inputs, make_report
from engine.solvers.affine import affine_decrypt, affine_encrypt

# Word list for the hallucinogens preference: color, dream, melting.
WORD_LIST = ("color", "dream", "melting")

DISCLAIMER = (
    "These are preferences among candidates, not decipherments of "
    "Nr. 86, K4, or an unknown script."
)


def covers(text: str) -> bool:
    """True when every hallucinogens word appears as its own word."""
    lowered = text.lower()
    return all(re.search(rf"\b{re.escape(word)}\b", lowered) for word in WORD_LIST)


def choose(left: str, right: str) -> str:
    """Pick the candidate that matches the hallucinogens word list.

    Exactly one of the two sentences must contain color, dream, and melting.
    The other is a plain alternative. This does not decipher anything.
    """
    left_ok = covers(left)
    right_ok = covers(right)
    if left_ok == right_ok:
        raise ValueError("need exactly one candidate that matches the word list")
    return left if left_ok else right


_AFFINE_UNITS = (1, 3, 5, 7, 9, 11, 15, 17, 19, 21, 23, 25)
MAX_ROTATIONS = 64
MAX_COMPOSITION_WITNESSES = 4


def _transform(cipher: str, transform: dict) -> str:
    """Apply the hypothesis to ciphertext before affine decryption."""
    if transform["kind"] == "reverse":
        return cipher[::-1]
    offset = transform["offset"]
    return cipher[offset:] + cipher[:offset]


def _restore_cipher_order(mapped: str, transform: dict) -> str:
    """Invert the permutation after affine encryption to replay original CT."""
    if transform["kind"] == "reverse":
        return mapped[::-1]
    offset = transform["offset"]
    return mapped[-offset:] + mapped[:-offset] if offset else mapped


def investigate_hallucinogens(text, *, cribs=(), max_checks=5000,
                              max_candidates=20, max_rotations=8) -> dict:
    """Test finite creative compositions, preserving factual proof requirements.

    Each affine/permutation pair costs one shared check. Transformations are
    interleaved fairly for each affine key. Original normalized plaintext crib
    coordinates never move. Every retained candidate replays to the original
    normalized ciphertext; no letters are inserted, deleted or guessed.
    """
    cipher, normalized_cribs, known = validate_inputs(text, cribs, max_checks, max_candidates)
    if not isinstance(max_rotations, int) or isinstance(max_rotations, bool):
        raise TypeError("max_rotations must be an integer")
    if not 0 <= max_rotations <= MAX_ROTATIONS:
        raise ValueError(f"max_rotations must be in 0..{MAX_ROTATIONS}")
    offsets = list(range(1, min(max_rotations, len(cipher) - 1) + 1))
    transforms = [{"kind": "identity", "offset": 0}, {"kind": "reverse", "offset": 0}]
    transforms.extend({"kind": "rotate_left", "offset": offset} for offset in offsets)
    transformed = [_transform(cipher, transform) for transform in transforms]
    transform_counts = [0] * len(transforms)
    transform_rejections = [0] * len(transforms)
    transform_mismatches = [0] * len(transforms)
    total_checks = 312 * len(transforms)
    model = get_model() if max_checks else None
    checks, duplicates, crib_rejections, forward_mismatches = 0, 0, 0, 0
    seen_plaintexts: set[str] = set()
    retained: dict[str, dict] = {}
    rank = lambda candidate: (-candidate["score"], candidate["plaintext"])

    for a in _AFFINE_UNITS:
        for b in range(26):
            for index, transform in enumerate(transforms):
                if checks >= max_checks:
                    break
                checks += 1
                transform_counts[index] += 1
                plain = affine_decrypt(transformed[index], a, b)
                if len(plain) != len(cipher):
                    forward_mismatches += 1
                    transform_mismatches[index] += 1
                    continue
                if any(plain[position] != letter for position, letter in known.items()):
                    crib_rejections += 1
                    transform_rejections[index] += 1
                    continue
                replay = _restore_cipher_order(affine_encrypt(plain, a, b), transform)
                if replay != cipher:
                    forward_mismatches += 1
                    transform_mismatches[index] += 1
                    continue
                key = {"transform": dict(transform), "affine": {"a": a, "b": b}}
                if plain in seen_plaintexts:
                    duplicates += 1
                    candidate = retained.get(plain)
                    if candidate is not None:
                        candidate["equivalent_compositions_seen"] += 1
                        if len(candidate["equivalent_compositions"]) < MAX_COMPOSITION_WITNESSES:
                            candidate["equivalent_compositions"].append(key)
                    continue
                seen_plaintexts.add(plain)
                candidate = {
                    "plaintext": plain, "family": "composed_affine", "key": key,
                    "score": model.score([ord(letter) - 65 for letter in plain]),
                    "forward_consistent": True, "crib_match": True,
                    "status": "unverified_candidate",
                    "evidence": {
                        "transform": dict(transform),
                        "plan": "permute ciphertext, invert affine, then replay the exact inverse composition",
                        "forward_equation": "original ciphertext = inverse permutation(affine(plaintext))",
                        "known_plaintext_positions": len(known),
                        "cribs_are_supplied_constraints": True,
                        "independent_validation": False,
                    },
                    "equivalent_compositions": [key], "equivalent_compositions_seen": 1,
                }
                retained[plain] = candidate
                if len(retained) > max_candidates:
                    worst = max(retained.values(), key=rank)
                    del retained[worst["plaintext"]]
            if checks >= max_checks:
                break
        if checks >= max_checks:
            break

    search_complete = checks == total_checks
    contradictions = []
    if forward_mismatches:
        contradictions.append({"kind": "forward_mismatch", "count": forward_mismatches,
                               "result": "discarded candidates that could not restore the original ciphertext"})
    if search_complete and not seen_plaintexts:
        contradictions.append({"kind": "no_model_matches_constraints", "count": crib_rejections,
                               "result": "requested compositions did not match supplied constraints; other models remain untested"})
    actions = [{"stage": "composition", "transform": dict(transform), "checks": transform_counts[index],
                "crib_rejections": transform_rejections[index], "forward_mismatches": transform_mismatches[index]}
               for index, transform in enumerate(transforms)]
    report = make_report(
        "hallucinogens", "bounded_reverse_rotation_affine_composition",
        sorted(retained.values(), key=rank), checks, max_checks, search_complete,
        "complete" if search_complete else "check_limit", actions,
        ("Normalized A-Z text is an affine substitution composed with one requested permutation.",
         "English scoring orders hypotheses, not independent correctness or probability.",
         "Original plaintext crib coordinates are fixed; supplied cribs are not independent validation.",
         "Equivalent compositions are alternate witnesses for the same text, not independent agreement."),
        contradictions,
    )
    report.update({
        "ciphertext_length": len(cipher), "known_positions": len(known),
        "cribs": [{"offset": crib.offset, "plaintext": crib.plaintext} for crib in normalized_cribs],
        "bounds": {"max_checks": max_checks, "max_candidates": max_candidates,
                   "max_rotations": max_rotations, "effective_rotation_offsets": offsets,
                   "total_requested_checks": total_checks,
                   "max_equivalent_composition_witnesses": MAX_COMPOSITION_WITNESSES},
        "transform_checks": [{"transform": dict(transform), "checks": transform_counts[index]}
                             for index, transform in enumerate(transforms)],
        "accepted_unique_plaintexts": len(seen_plaintexts), "duplicate_candidates": duplicates,
        "crib_rejections": crib_rejections, "forward_mismatches": forward_mismatches,
        "candidates_truncated": len(seen_plaintexts) > len(retained),
        "unique_plaintext_established": False,
        "ranking": "existing English language score descending, then plaintext; not a probability",
    })
    return report
