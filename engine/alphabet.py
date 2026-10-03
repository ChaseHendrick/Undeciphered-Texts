"""Letter-stream helpers shared by every solver.

Non-letters stay in the ciphertext skeleton so recovered plaintext keeps
spaces and punctuation. Scores and keys use the A-Z stream only.
"""

from __future__ import annotations

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
A_ORD = ord("A")


def letters_only(text: str) -> str:
    return "".join(ch.upper() for ch in text if ch.isalpha())


def to_ints(letters: str) -> list[int]:
    return [ord(ch) - A_ORD for ch in letters]


def from_ints(seq: list[int]) -> str:
    return "".join(chr(A_ORD + n) for n in seq)


def reinject(template: str, solved_letters: str) -> str:
    """Write solved uppercase letters back into the original skeleton."""
    stream = iter(solved_letters)
    out: list[str] = []
    for ch in template:
        if not ch.isalpha():
            out.append(ch)
            continue
        plain = next(stream)
        out.append(plain.lower() if ch.islower() else plain.upper())
    return "".join(out)


def shift_letter(index: int, shift: int) -> int:
    return (index + shift) % 26
