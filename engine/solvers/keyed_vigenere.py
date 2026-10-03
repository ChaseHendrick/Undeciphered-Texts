"""Keyed Vigenère: keyword-mixed alphabet, repeating key, index letter.

This is the periodic polyalphabetic substitution used for Kryptos passage 1,
as printed in the NSA FOIA technical paper (DOCID 4051151): plain and cipher
components are the same keyword-mixed sequence, and each cipher alphabet is
that sequence rotated so the current key letter sits under the index letter.

It recovers a ciphertext only when the key and alphabet keyword are supplied.
It does not search for an unknown key, and it does not read Kryptos K4.
"""

from __future__ import annotations

from engine.alphabet import ALPHABET, letters_only
from engine.language import get_model
from engine.result import SolveResult


def keyword_mixed_alphabet(keyword: str, base: str = ALPHABET) -> str:
    """Keyword letters, first occurrence only, then the unused base letters in order.

    KRYPTOS on A-Z is KRYPTOSABCDEFGHIJLMNQUVWXZ: C stays, and K, R, Y, P, T,
    O, S are not written again.
    """
    if len(base) < 2 or len(set(base)) != len(base):
        raise ValueError("base alphabet must be at least two distinct letters")
    if any(not ch.isalpha() or ch != ch.upper() for ch in base):
        raise ValueError("base alphabet must be uppercase letters")
    seen: set[str] = set()
    out: list[str] = []
    for ch in letters_only(keyword) + base:
        if ch not in base:
            raise ValueError(f"keyword letter {ch} is not in the base alphabet")
        if ch not in seen:
            seen.add(ch)
            out.append(ch)
    if len(out) != len(base):
        raise ValueError("keyword-mixed alphabet must be a permutation of the base alphabet")
    return "".join(out)


def cipher_alphabet(alphabet: str, key_letter: str, index_letter: str) -> str:
    """Mixed alphabet rotated so key_letter sits in the index letter's column."""
    if key_letter not in alphabet or index_letter not in alphabet:
        raise ValueError("key letter and index letter must be in the alphabet")
    n = len(alphabet)
    shift = (alphabet.index(key_letter) - alphabet.index(index_letter)) % n
    return "".join(alphabet[(shift + i) % n] for i in range(n))


def _convert(text: str, key: str, alphabet: str, index_letter: str, *, decrypt: bool) -> str:
    if len(set(alphabet)) != len(alphabet) or len(alphabet) < 2:
        raise ValueError("alphabet must be distinct letters")
    if index_letter not in alphabet:
        raise ValueError("index letter is not in the alphabet")
    keyword = letters_only(key)
    if not keyword:
        raise ValueError("key must contain at least one letter")
    missing = [ch for ch in keyword if ch not in alphabet]
    if missing:
        raise ValueError(f"key letter {missing[0]} is not in the alphabet")
    n = len(alphabet)
    index = alphabet.index(index_letter)
    out: list[str] = []
    j = 0
    for ch in text:
        upper = ch.upper()
        if upper not in alphabet:
            if upper in ALPHABET:
                raise ValueError(f"letter {upper} is outside the keyed alphabet")
            out.append(ch)
            continue
        key_index = alphabet.index(keyword[j % len(keyword)])
        src = alphabet.index(upper)
        if decrypt:
            dest = (src - key_index + index) % n
        else:
            dest = (src + key_index - index) % n
        mapped = alphabet[dest]
        out.append(mapped.lower() if ch.islower() else mapped)
        j += 1
    return "".join(out)


def keyed_vigenere_encrypt(
    text: str,
    key: str,
    alphabet_keyword: str,
    index_letter: str | None = None,
    base: str = ALPHABET,
) -> str:
    alphabet = keyword_mixed_alphabet(alphabet_keyword, base)
    index = alphabet[0] if index_letter is None else letters_only(index_letter)
    if len(index) != 1:
        raise ValueError("index letter must be a single letter")
    return _convert(text, key, alphabet, index, decrypt=False)


def keyed_vigenere_decrypt(
    text: str,
    key: str,
    alphabet_keyword: str,
    index_letter: str | None = None,
    base: str = ALPHABET,
) -> str:
    alphabet = keyword_mixed_alphabet(alphabet_keyword, base)
    index = alphabet[0] if index_letter is None else letters_only(index_letter)
    if len(index) != 1:
        raise ValueError("index letter must be a single letter")
    return _convert(text, key, alphabet, index, decrypt=True)


def solve_keyed_vigenere(
    text: str,
    key: str,
    alphabet_keyword: str,
    index_letter: str | None = None,
    base: str = ALPHABET,
) -> SolveResult:
    """Decrypt with a known repeating key on a keyword-mixed alphabet.

    For Kryptos K1 the published arguments are key PALIMPSEST, alphabet
    keyword KRYPTOS, and index letter K (the first letter of that alphabet).
    """
    alphabet = keyword_mixed_alphabet(alphabet_keyword, base)
    index = alphabet[0] if index_letter is None else letters_only(index_letter)
    if len(index) != 1:
        raise ValueError("index letter must be a single letter")
    plaintext = _convert(text, key, alphabet, index, decrypt=True)
    keyword = letters_only(key)
    letters = letters_only(plaintext)
    az = [ord(ch) - 65 for ch in letters]
    return SolveResult(
        method="keyed-vigenere",
        plaintext=plaintext,
        key=keyword,
        score=get_model().score(az) if az else 0.0,
        details={
            "alphabet_keyword": letters_only(alphabet_keyword),
            "alphabet": alphabet,
            "index_letter": index,
            "period": len(keyword),
            "letters": len(az),
            "scope": "known-key keyed Vigenère; not a K4 solution",
        },
    )
