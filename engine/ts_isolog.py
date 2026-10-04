"""Slide clerk formulae across a Truppenschlüssel pair grid.

A two-square cipher is a fixed substitution of letter pairs. Inside a window,
two plaintext pairs are equal exactly when the two ciphertext pairs are equal.
Phrases are a declared list, not a recovered message. A placement that
survives is unverified. solved stays false.
"""

from __future__ import annotations

from engine.ts_close_pairs import DSZPZ, IASRZ_129, IASRZ_130

# Even length, no J. Chosen as formulae a clerk might write, not as a reading.
PHRASES = (
    "KOMMANDANT",
    "KOMMANDO",
    "ARTILLERIE",
    "INFANTERIE",
    "STELLUNG",
    "VERLUSTE",
    "DURCHBRUCH",
    "FUNKSPRUCH",
    "UNTERKUNFT",
    "FLIEGERALARM",
    "TAGESMELDUNG",
    "FEUERUEBERFALL",
)

TEXTS = (
    ("IASRZ_129", IASRZ_129),
    ("IASRZ_130", IASRZ_130),
    ("DSZPZ", DSZPZ),
)


def pairs(text: str) -> tuple[str, ...]:
    if len(text) % 2:
        raise ValueError("pair grid needs an even length")
    return tuple(text[index : index + 2] for index in range(0, len(text), 2))


def repeats_a_pair(grams: tuple[str, ...]) -> bool:
    return len(set(grams)) < len(grams)


def placement_map(phrase: str, window: str) -> dict[str, str] | None:
    """Plaintext pair to ciphertext pair, or None when the repeats disagree."""
    plain = pairs(phrase)
    cipher = pairs(window)
    if len(plain) != len(cipher):
        raise ValueError("window length does not match the phrase")
    forward: dict[str, str] = {}
    backward: dict[str, str] = {}
    for plain_pair, cipher_pair in zip(plain, cipher):
        if forward.get(plain_pair, cipher_pair) != cipher_pair:
            return None
        if backward.get(cipher_pair, plain_pair) != plain_pair:
            return None
        forward[plain_pair] = cipher_pair
        backward[cipher_pair] = plain_pair
    return forward


def slide(phrase: str, text: str) -> tuple[dict, ...]:
    """Even offsets only. The pair grid starts on the first printed letter."""
    if len(phrase) % 2 or len(phrase) > len(text):
        return ()
    found = []
    for start in range(0, len(text) - len(phrase) + 1, 2):
        window = text[start : start + len(phrase)]
        mapping = placement_map(phrase, window)
        if mapping is None:
            continue
        plain = pairs(phrase)
        cipher = pairs(window)
        found.append({
            "start": start,
            "informative": repeats_a_pair(plain) or repeats_a_pair(cipher),
            "pairs": len(plain),
        })
    return tuple(found)


def maps_agree(left: dict[str, str], right: dict[str, str]) -> bool:
    for key, value in left.items():
        if key in right and right[key] != value:
            return False
    for key, value in right.items():
        if key in left and left[key] != value:
            return False
    return True


def joint_informative(phrase: str, left: str, right: str) -> int:
    """Placements, one on each text, whose pair maps do not contradict."""
    left_hits = []
    right_hits = []
    for text, store in ((left, left_hits), (right, right_hits)):
        for start in range(0, len(text) - len(phrase) + 1, 2):
            window = text[start : start + len(phrase)]
            mapping = placement_map(phrase, window)
            if mapping is None:
                continue
            if repeats_a_pair(pairs(phrase)) or repeats_a_pair(pairs(window)):
                store.append(mapping)
    agree = 0
    for one in left_hits:
        for other in right_hits:
            if maps_agree(one, other):
                agree += 1
    return agree


def search_ts_isolog() -> dict:
    """Count surviving placements. Do not assemble a plaintext."""
    odd = [phrase for phrase in PHRASES if len(phrase) % 2]
    if odd:
        raise ValueError("phrases must be even length: " + ", ".join(odd))
    per_text = []
    for name, text in TEXTS:
        if len(text) % 2:
            raise ValueError(f"{name} is not on an even pair grid")
        phrase_rows = []
        for phrase in PHRASES:
            hits = slide(phrase, text)
            phrase_rows.append({
                "phrase": phrase,
                "placements": len(hits),
                "informative": sum(1 for hit in hits if hit["informative"]),
            })
        per_text.append({
            "text": name,
            "length": len(text),
            "phrases": phrase_rows,
            "informative": sum(row["informative"] for row in phrase_rows),
        })
    iasrz_joint = tuple(
        {"phrase": phrase, "agreeing": joint_informative(phrase, IASRZ_129, IASRZ_130)}
        for phrase in PHRASES
    )
    return {
        "claimed_plaintext": None,
        "solved": False,
        "phrases": len(PHRASES),
        "texts": per_text,
        "iasrz_joint": iasrz_joint,
        "iasrz_joint_agreeing": sum(row["agreeing"] for row in iasrz_joint),
        "scope": "Repeat pattern only. A surviving placement is not a reading and not a square.",
    }
