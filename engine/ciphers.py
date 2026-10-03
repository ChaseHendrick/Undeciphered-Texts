"""Encrypt and decrypt the classical ciphers this package solves.

These are the forward maps used to build known tests. Solvers do not call
them with the secret; tests and the demo do, then throw the key away.
"""

from __future__ import annotations

from engine.alphabet import ALPHABET, letters_only


def _is_key_alpha(key: str) -> str:
    cleaned = letters_only(key)
    if not cleaned:
        raise ValueError("key must contain at least one letter")
    return cleaned


def caesar_encrypt(text: str, shift: int) -> str:
    shift %= 26
    out: list[str] = []
    for ch in text:
        if not ch.isalpha():
            out.append(ch)
            continue
        base = ord("A") if ch.isupper() else ord("a")
        out.append(chr(base + (ord(ch) - base + shift) % 26))
    return "".join(out)


def caesar_decrypt(text: str, shift: int) -> str:
    return caesar_encrypt(text, -shift)


def vigenere_encrypt(text: str, key: str) -> str:
    keyword = _is_key_alpha(key)
    out: list[str] = []
    j = 0
    for ch in text:
        if not ch.isalpha():
            out.append(ch)
            continue
        shift = ord(keyword[j % len(keyword)]) - 65
        base = ord("A") if ch.isupper() else ord("a")
        out.append(chr(base + (ord(ch) - base + shift) % 26))
        j += 1
    return "".join(out)


def vigenere_decrypt(text: str, key: str) -> str:
    keyword = _is_key_alpha(key)
    # Decrypt is encrypt under the complementary shifts.
    complement = "".join(chr(65 + (26 - (ord(ch) - 65)) % 26) for ch in keyword)
    return vigenere_encrypt(text, complement)


def substitution_encrypt(text: str, key: str) -> str:
    """key[i] is the ciphertext letter that replaces plaintext letter i (A=0)."""
    cipher_alpha = _is_key_alpha(key)
    if len(cipher_alpha) != 26 or len(set(cipher_alpha)) != 26:
        raise ValueError("substitution key must be a permutation of A-Z")
    table = {ALPHABET[i]: cipher_alpha[i] for i in range(26)}
    out: list[str] = []
    for ch in text:
        if not ch.isalpha():
            out.append(ch)
            continue
        mapped = table[ch.upper()]
        out.append(mapped.lower() if ch.islower() else mapped)
    return "".join(out)


def substitution_decrypt(text: str, key: str) -> str:
    cipher_alpha = _is_key_alpha(key)
    if len(cipher_alpha) != 26 or len(set(cipher_alpha)) != 26:
        raise ValueError("substitution key must be a permutation of A-Z")
    inverse = ["?"] * 26
    for plain_i, cipher_ch in enumerate(cipher_alpha):
        inverse[ord(cipher_ch) - 65] = ALPHABET[plain_i]
    return substitution_encrypt(text, "".join(inverse))


# --- Two-square / Truppenschlüssel (double Playfair, single stage) ---
# Alphabet omits J. Plaintext J is written as II before encipherment.
# First plaintext letter is found in the left square, second in the right.
# Different rows: take the other corners of the rectangle, reading the
# ciphertext letter from the right square first, then from the left.
# Same row: take the right-hand neighbour in each square (wrap), again
# right-square letter first. See Ostwald & Weierud, Cryptologia / mcts.pdf.

TWO_SQUARE_ALPHABET = "ABCDEFGHIKLMNOPQRSTUVWXYZ"


def two_square_letters(text: str) -> str:
    """A-Z stream for two-square: J folded to I, non-letters dropped."""
    out: list[str] = []
    for ch in text:
        if not ch.isalpha():
            continue
        up = ch.upper()
        out.append("I" if up == "J" else up)
    return "".join(out)


def square_from_keyword(keyword: str) -> str:
    """Build one 5×5 square string (25 letters, no J) from a keyword."""
    cleaned = two_square_letters(keyword)
    seen: set[str] = set()
    cells: list[str] = []
    for ch in cleaned:
        if ch not in seen:
            seen.add(ch)
            cells.append(ch)
    for ch in TWO_SQUARE_ALPHABET:
        if ch not in seen:
            cells.append(ch)
    if len(cells) != 25:
        raise ValueError("two-square square must contain 25 distinct letters")
    return "".join(cells)


def _parse_square(square: str) -> list[str]:
    cells = two_square_letters(square)
    if len(cells) != 25 or len(set(cells)) != 25:
        raise ValueError("two-square square must be a permutation of A-Z without J")
    if "J" in cells:
        raise ValueError("two-square square must omit J")
    return list(cells)


def _square_positions(cells: list[str]) -> dict[str, int]:
    return {ch: i for i, ch in enumerate(cells)}


def two_square_encrypt(text: str, left: str, right: str) -> str:
    """Encrypt with two 5×5 squares (Truppenschlüssel single-stage rule)."""
    left_cells = _parse_square(left)
    right_cells = _parse_square(right)
    left_pos = _square_positions(left_cells)
    right_pos = _square_positions(right_cells)
    stream = two_square_letters(text)
    if len(stream) % 2 == 1:
        stream += "X"
    out: list[str] = []
    for i in range(0, len(stream), 2):
        p1, p2 = stream[i], stream[i + 1]
        r1, c1 = divmod(left_pos[p1], 5)
        r2, c2 = divmod(right_pos[p2], 5)
        if r1 != r2:
            out.append(right_cells[r1 * 5 + c2])
            out.append(left_cells[r2 * 5 + c1])
        else:
            out.append(right_cells[r1 * 5 + (c2 + 1) % 5])
            out.append(left_cells[r1 * 5 + (c1 + 1) % 5])
    return "".join(out)


def two_square_decrypt(text: str, left: str, right: str) -> str:
    """Decrypt with two 5×5 squares (inverse of two_square_encrypt)."""
    left_cells = _parse_square(left)
    right_cells = _parse_square(right)
    left_pos = _square_positions(left_cells)
    right_pos = _square_positions(right_cells)
    stream = two_square_letters(text)
    if len(stream) % 2 == 1:
        raise ValueError("two-square ciphertext length must be even")
    out: list[str] = []
    for i in range(0, len(stream), 2):
        c1, c2 = stream[i], stream[i + 1]
        r1, c1p = divmod(right_pos[c1], 5)
        r2, c2p = divmod(left_pos[c2], 5)
        if r1 != r2:
            out.append(left_cells[r1 * 5 + c2p])
            out.append(right_cells[r2 * 5 + c1p])
        else:
            out.append(left_cells[r1 * 5 + (c2p - 1) % 5])
            out.append(right_cells[r1 * 5 + (c1p - 1) % 5])
    return "".join(out)
