"""Exact, bounded letter-model compositions for conditional crib experiments.

This is a repository-specific model tester, not a claimed K4 mechanism.
The key is unknown. The alphabet, model family and layout are explicit
assumptions. Unknown key slots and plaintext letters remain unknown.
Repeating and Beaufort definitions:
https://www.cryptogram.org/downloads/aca.info/ciphers/Vigenere.pdf
https://www.cryptogram.org/downloads/aca.info/ciphers/Beaufort.pdf
Plaintext-autokey definition:
https://www.cryptogram.org/downloads/aca.info/ciphers/Autokey.pdf
"""
from __future__ import annotations

from collections.abc import Sequence
import hashlib
import time

from engine.reverse_engineer import Crib

AZ = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
KRYPTOS_MIXED = "KRYPTOSABCDEFGHIJLMNQUVWXZ"
FAMILIES = ("repeating", "plaintext-autokey", "ciphertext-autokey", "beaufort")
ORDERS = ("substitute-then-transpose", "transpose-then-substitute")


def _integer(value, name, low, high):
    if isinstance(value, bool) or not isinstance(value, int):
        raise TypeError(f"{name} must be an integer")
    if not low <= value <= high:
        raise ValueError(f"{name} must be in {low}..{high}")


def _letters(text, name, minimum=1):
    if not isinstance(text, str):
        raise TypeError(f"{name} must be a string")
    if len(text) > 4096 or any(ch not in AZ + AZ.lower() and not ch.isspace() for ch in text):
        raise ValueError(f"{name} accepts ASCII letters and whitespace, no gaps or punctuation")
    result = "".join(ch.upper() for ch in text if not ch.isspace())
    if not minimum <= len(result) <= 512:
        raise ValueError(f"{name} requires {minimum}..512 letters")
    return result


def _choices(values, name, allowed, maximum):
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise TypeError(f"{name} must be a finite sequence")
    if not 1 <= len(values) <= maximum or any(not isinstance(v, str) for v in values):
        raise ValueError(f"{name} has invalid length or entries")
    if len(set(values)) != len(values) or any(v not in allowed for v in values):
        raise ValueError(f"{name} must contain distinct supported entries")
    return tuple(values)


def _alphabets(values):
    if isinstance(values, (str, bytes)) or not isinstance(values, Sequence):
        raise TypeError("alphabets must be a finite sequence")
    if not 1 <= len(values) <= 8 or any(not isinstance(v, str) or len(v) != 26 or set(v) != set(AZ) for v in values):
        raise ValueError("each alphabet must be an uppercase A-Z permutation")
    if len(set(values)) != len(values):
        raise ValueError("duplicate alphabets are not allowed")
    return tuple(values)


def _known(cribs, length):
    if isinstance(cribs, (str, bytes)) or not isinstance(cribs, Sequence):
        raise TypeError("cribs must be a finite sequence of Crib objects")
    if not 1 <= len(cribs) <= 32:
        raise ValueError("at least one crib and at most 32 are required")
    known = {}
    for crib in cribs:
        if not isinstance(crib, Crib):
            raise TypeError("cribs must contain Crib objects")
        _integer(crib.offset, "crib offset", 0, length - 1)
        text = _letters(crib.plaintext, "crib plaintext")
        if crib.offset + len(text) > length:
            raise ValueError("crib extends beyond ciphertext")
        for i, letter in enumerate(text, crib.offset):
            if i in known and known[i] != letter:
                raise ValueError("overlapping cribs disagree")
            known[i] = letter
    return known


def _permutation(layout, length):
    if not isinstance(layout, dict):
        raise TypeError("layout must be a dictionary")
    kind = layout.get("kind")
    if kind in ("identity", "reverse") and set(layout) == {"kind"}:
        return tuple(range(length)) if kind == "identity" else tuple(range(length - 1, -1, -1))
    if kind != "ragged-columnar" or set(layout) != {"kind", "width", "direction"}:
        raise ValueError("unsupported layout")
    _integer(layout["width"], "layout width", 2, min(32, length))
    if layout["direction"] not in ("left-to-right", "right-to-left"):
        raise ValueError("unsupported column direction")
    width = layout["width"]
    columns = range(width) if layout["direction"] == "left-to-right" else range(width - 1, -1, -1)
    return tuple(i for column in columns for i in range(column, length, width))


def _layouts(length, max_width):
    result = []
    seen = set()
    candidates = [{"kind": "identity"}, {"kind": "reverse"}]
    candidates += [{"kind": "ragged-columnar", "width": width, "direction": direction}
                   for width in range(2, min(length, max_width) + 1)
                   for direction in ("left-to-right", "right-to-left")]
    for layout in candidates:
        perm = _permutation(layout, length)
        if perm not in seen:
            result.append((layout, perm))
            seen.add(perm)
    return result


def reencrypt_k4_model(plaintext, *, family, key_shift_indices, alphabet=AZ,
                      layout=None, order="substitute-then-transpose"):
    """Forward replay with supplied complete modular shifts, not key recovery.

    With indices in the declared alphabet, repeating uses C=P+K, Beaufort
    uses C=K-P. Autokey uses primer indices, then earlier plaintext or earlier
    intermediate ciphertext at lag equal to primer length. No nulls/padding.
    """
    plain = _letters(plaintext, "plaintext")
    _choices((family,), "family", FAMILIES, 1)
    _choices((order,), "order", ORDERS, 1)
    _alphabets((alphabet,))
    if isinstance(key_shift_indices, (str, bytes)) or not isinstance(key_shift_indices, Sequence):
        raise TypeError("key_shift_indices must be a finite sequence")
    _integer(len(key_shift_indices), "key length", 1, min(32, len(plain)))
    for value in key_shift_indices:
        _integer(value, "key shift", 0, 25)
    perm = _permutation({"kind": "identity"} if layout is None else layout, len(plain))
    work = plain if order == ORDERS[0] else "".join(plain[i] for i in perm)
    values = [alphabet.index(ch) for ch in work]
    cipher = []
    period = len(key_shift_indices)
    for i, value in enumerate(values):
        if family in ("repeating", "beaufort") or i < period:
            shift = key_shift_indices[i % period]
        elif family == "plaintext-autokey":
            shift = values[i - period]
        else:
            shift = cipher[i - period]
        cipher.append((shift - value if family == "beaufort" else value + shift) % 26)
    rendered = "".join(alphabet[v] for v in cipher)
    return "".join(rendered[i] for i in perm) if order == ORDERS[0] else rendered


def _fit(ciphertext, known, family, alphabet, period, layout, perm, order):
    length = len(ciphertext)
    if order == ORDERS[0]:
        restored = [""] * length
        for output, original in enumerate(perm):
            restored[original] = ciphertext[output]
        work = "".join(restored)
        fitted = {i: alphabet.index(ch) for i, ch in known.items()}
    else:
        work = ciphertext
        fitted = {i: alphabet.index(known[original]) for i, original in enumerate(perm) if original in known}
    cipher = [alphabet.index(ch) for ch in work]
    # Each residue has one free first-plaintext seed. Later letters are
    # signed copies plus a known constant, or fixed in ciphertext-autokey.
    coefficients, constants = [], []
    for i in range(length):
        residue = i % period
        if family == "repeating":
            coefficient, constant = 1, (cipher[i] - cipher[residue]) % 26
        elif family == "beaufort":
            coefficient, constant = 1, (cipher[residue] - cipher[i]) % 26
        elif i < period:
            coefficient, constant = 1, 0
        elif family == "plaintext-autokey":
            coefficient = -coefficients[i - period]
            constant = (cipher[i] - constants[i - period]) % 26
        else:
            coefficient, constant = 0, (cipher[i] - cipher[i - period]) % 26
        coefficients.append(coefficient)
        constants.append(constant)
    seeds = [None] * period
    for i, value in fitted.items():
        coefficient, constant = coefficients[i], constants[i]
        if coefficient == 0:
            if value != constant:
                return None
            continue
        seed = ((value - constant) * coefficient) % 26
        residue = i % period
        if seeds[residue] is not None and seeds[residue] != seed:
            return None
        seeds[residue] = seed
    values = [constants[i] if coefficients[i] == 0 else
              (constants[i] + coefficients[i] * seeds[i % period]) % 26
              if seeds[i % period] is not None else None for i in range(length)]
    shifts = [(cipher[i] + seeds[i] if family == "beaufort" else cipher[i] - seeds[i]) % 26
              if seeds[i] is not None else None for i in range(period)]
    verified = 0
    for i, value in enumerate(values):
        if value is None:
            continue
        if family in ("repeating", "beaufort") or i < period:
            shift = shifts[i % period]
        elif family == "plaintext-autokey":
            shift = values[i - period]
        else:
            shift = cipher[i - period]
        if shift is None:
            continue
        expected = (shift - value if family == "beaufort" else value + shift) % 26
        if cipher[i] != expected:
            raise RuntimeError("forced model equation failed verification")
        verified += 1
    mask = "".join(alphabet[value] if value is not None else "?" for value in values)
    if order == ORDERS[1]:
        restored = ["?"] * length
        for output, original in enumerate(perm):
            restored[original] = mask[output]
        mask = "".join(restored)
    if any(mask[i] != letter for i, letter in known.items()):
        raise RuntimeError("model lost original plaintext crib coordinates")
    complete = all(value is not None for value in shifts)
    replay = None
    if complete:
        replay = reencrypt_k4_model(mask, family=family, key_shift_indices=shifts,
                                   alphabet=alphabet, layout=layout, order=order) == ciphertext
        if not replay:
            raise RuntimeError("complete model failed forward replay")
    return {"family": family, "alphabet": alphabet, "period": period,
            "layout": dict(layout), "order": order, "key_shift_indices": shifts,
            "key_complete": complete, "unresolved_key_slots": shifts.count(None),
            "compatible_key_completions": 26 ** shifts.count(None),
            "predicted_plaintext": mask, "predicted_positions": length - mask.count("?"),
            "unknown_plaintext_positions": mask.count("?"),
            "forced_equations_verified": True, "forced_equations_checked": verified,
            "re_encryption_matches": replay, "claimed_plaintext": None}


def _stream(layouts, period_bound, order_index):
    # Diagonal enumeration exposes every period and layout early without
    # consuming the entire budget on the first width. Each pair occurs once.
    for phase in range(period_bound):
        for index, (layout, perm) in enumerate(layouts):
            if order_index and layout["kind"] == "identity":
                continue
            yield layout, perm, (index + phase) % period_bound + 1


def search_k4_models(text, *, cribs, max_checks=10000, max_period=32,
                     max_width=32, max_candidates=20,
                     alphabets=(AZ, KRYPTOS_MIXED), families=FAMILIES, orders=ORDERS):
    """Return forced predictions under a finite portfolio with an unknown key.

    One check fits one layout/family/alphabet/order/period hypothesis.
    Round robin across family/alphabet/order streams, diagonal within each
    stream. Seed domains are solved algebraically, not key-enumerated or
    language-filled. Storage limits never stop model enumeration. Callers
    must evaluate withheld clues after this function returns, with sufficient
    candidate storage if they need counts over every compatible hypothesis.
    """
    started = time.perf_counter()
    _integer(max_checks, "max_checks", 0, 10000)
    _integer(max_period, "max_period", 1, 32)
    _integer(max_width, "max_width", 2, 32)
    _integer(max_candidates, "max_candidates", 1, 10000)
    cipher = _letters(text, "ciphertext", minimum=4)
    known = _known(cribs, len(cipher))
    families = _choices(families, "families", FAMILIES, 4)
    orders = _choices(orders, "orders", ORDERS, 2)
    alphabets = _alphabets(alphabets)
    layouts = _layouts(len(cipher), max_width)
    period_bound = min(max_period, len(cipher))
    groups = []
    for family in families:
        for alphabet in alphabets:
            for index, order in enumerate(orders):
                groups.append({"family": family, "alphabet": alphabet, "order": order,
                               "iterator": iter(_stream(layouts, period_bound, index)),
                               "checks": 0, "compatible_models": 0, "rejected_models": 0,
                               "period_counts": {}, "layout_counts": {}})
    model_space = period_bound * len(families) * len(alphabets) * (len(layouts) * len(orders) - (len(orders) - 1))
    checks, candidates = 0, []
    active = list(groups)
    while active and checks < max_checks:
        remaining = []
        for group in active:
            if checks >= max_checks:
                break
            try:
                layout, perm, period = next(group["iterator"])
            except StopIteration:
                continue
            remaining.append(group)
            checks += 1
            group["checks"] += 1
            group["period_counts"][str(period)] = group["period_counts"].get(str(period), 0) + 1
            label = layout["kind"] if "width" not in layout else f"width={layout['width']};direction={layout['direction']}"
            group["layout_counts"][label] = group["layout_counts"].get(label, 0) + 1
            candidate = _fit(cipher, known, group["family"], group["alphabet"], period,
                             layout, perm, group["order"])
            if candidate is None:
                group["rejected_models"] += 1
            else:
                group["compatible_models"] += 1
                candidates.append(candidate)
        active = remaining
    # Holding at most max_checks intermediate records is bounded. Retention
    # depends only on forced-position counts and deterministic model labels.
    candidates.sort(key=lambda c: (-c["predicted_positions"], c["family"], c["alphabet"],
                                  c["period"], c["order"], str(c["layout"])))
    coverage = [{key: value for key, value in group.items() if key != "iterator"} for group in groups]
    complete = checks == model_space
    return {"ciphertext_length": len(cipher), "ciphertext_sha256": hashlib.sha256(cipher.encode("ascii")).hexdigest(),
            "known_positions": len(known), "checks": checks, "requested_models": model_space,
            "compatible_models": len(candidates), "rejected_models": checks - len(candidates),
            "candidates": candidates[:max_candidates], "candidates_truncated": len(candidates) > max_candidates,
            "search_complete": complete, "stop_reason": "complete" if complete else "check_limit",
            "coverage": coverage, "elapsed_seconds": time.perf_counter() - started,
            "bounds": {"max_checks": max_checks, "max_period": max_period, "max_width": max_width,
                       "max_candidates": max_candidates, "max_letters": 512,
                       "layouts": [layout for layout, _ in layouts], "families": list(families),
                       "alphabets": list(alphabets), "orders": list(orders)},
            "schedule": "round robin family/alphabet/order; diagonal layout/period; identity order duplicated only once",
            "key_convention": "indices 0..25 in stated alphabet, zero origin; not claimed artist keywords or indicator letters",
            "ranking": "forced positions then stable labels; no language, clue holdout or neural score",
            "key_completions_enumerated": False, "claimed_plaintext": None,
            "scope": "Conditional models only. Search completion is bounded model coverage, not unique key or historical plaintext. No nulls, padding, errors or letters invented."}

