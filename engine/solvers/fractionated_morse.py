"""Known-key fractionated Morse cipher solver.

Plaintext is written as Morse (dot ".", dash "-", letter gap "x", word
gap "xx"), then read in groups of three. Each of the 26 groups other
than "xxx" is replaced by one letter of a mixed alphabet. The key is
that alphabet, or a keyword that is written first and followed by the
unused letters of A-Z.

The worked example used here is Practical Cryptography, Fractionated
Morse cipher (fetched 2026-10-02):

  http://practicalcryptography.com/ciphers/fractionated-morse-cipher/

  key ROUNDTABLECFGHIJKMPQSVWXYZ
  plaintext "defend the east"
  morse -..x.x..-.x.x-.x-..xx-x....x.xx.x.-x...x-x
  ciphertext ESOAVVLJRSSTRX

The page prints the plaintext in lowercase. Morse has no case, so this
solver returns A-Z letters and keeps the word spaces the page says are
recovered: DEFEND THE EAST. The morse line on the page already includes
one padding "x" so the stream length is a multiple of 3. The first
group "-.." is E and the next group "x.x" is S.

This module is a **known classical-cipher** solver. It recovers plaintext
only when the key is supplied. It is **not** an unknown-script reading
and **not** a claim about army message Nr. 86.
"""

from __future__ import annotations

from engine.alphabet import ALPHABET, letters_only
from engine.result import SolveResult

# Practical Cryptography worked example (fetched 2026-10-02).
# http://practicalcryptography.com/ciphers/fractionated-morse-cipher/
PRACTICAL_CRYPTOGRAPHY_URL = (
    "http://practicalcryptography.com/ciphers/fractionated-morse-cipher/"
)
PRACTICAL_CRYPTOGRAPHY_KEY = "ROUNDTABLECFGHIJKMPQSVWXYZ"
PRACTICAL_CRYPTOGRAPHY_PLAIN = "DEFEND THE EAST"
PRACTICAL_CRYPTOGRAPHY_CIPHER = "ESOAVVLJRSSTRX"
PRACTICAL_CRYPTOGRAPHY_MORSE = "-..x.x..-.x.x-.x-..xx-x....x.xx.x.-x...x-x"

_SCOPE = (
    "Known classical fractionated Morse cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)

# International Morse as printed on the Practical Cryptography page.
# Dot is "." and dash is "-". "x" is not a Morse symbol; it is the gap.
_MORSE: dict[str, str] = {
    "A": ".-",
    "B": "-...",
    "C": "-.-.",
    "D": "-..",
    "E": ".",
    "F": "..-.",
    "G": "--.",
    "H": "....",
    "I": "..",
    "J": ".---",
    "K": "-.-",
    "L": ".-..",
    "M": "--",
    "N": "-.",
    "O": "---",
    "P": ".--.",
    "Q": "--.-",
    "R": ".-.",
    "S": "...",
    "T": "-",
    "U": "..-",
    "V": "...-",
    "W": ".--",
    "X": "-..-",
    "Y": "-.--",
    "Z": "--..",
    "0": "-----",
    "1": ".----",
    "2": "..---",
    "3": "...--",
    "4": "....-",
    "5": ".....",
    "6": "-....",
    "7": "--...",
    "8": "---..",
    "9": "----.",
    ".": ".-.-.-",
    ",": "--..--",
    ":": "---...",
    '"': ".-..-.",
    "'": ".----.",
    "!": "-.-.--",
    "?": "..--..",
    "@": ".--.-.",
    "-": "-....-",
    ";": "-.-.-.",
    "(": "-.--.",
    ")": "-.--.-",
    "=": "-...-",
}
_MORSE_TO_CHAR = {code: char for char, code in _MORSE.items()}

_TRIPLES: tuple[str, ...] = tuple(
    a + b + c
    for a in ".-x"
    for b in ".-x"
    for c in ".-x"
    if a + b + c != "xxx"
)


def fractionated_morse_key(key: str) -> str:
    """Mixed 26-letter alphabet: keyword letters first, then the rest of A-Z.

    A key that is already 26 distinct letters is used as written. Duplicate
    letters in a keyword are skipped. The result is the column order over
    the 26 Morse triples (everything except "xxx").
    """
    seen: list[str] = []
    for ch in key.upper():
        if not ch.isalpha() or ch in seen:
            continue
        seen.append(ch)
    for ch in ALPHABET:
        if ch not in seen:
            seen.append(ch)
    if len(seen) != 26:
        raise ValueError("fractionated Morse key must yield 26 letters")
    return "".join(seen)


def _encode_morse(text: str) -> str:
    """Morse stream with x between symbols and xx between words.

    A trailing x is added only when the length is not a multiple of 3,
    matching the padding x on the published "defend the east" line.
    Whitespace separates words and is not itself a Morse symbol.
    """
    words: list[str] = []
    for raw in text.split():
        pieces: list[str] = []
        for ch in raw:
            lookup = ch.upper() if ch.isalpha() else ch
            code = _MORSE.get(lookup)
            if code is None:
                raise ValueError(f"unsupported fractionated Morse character: {ch!r}")
            pieces.append(code)
        if pieces:
            words.append("x".join(pieces))
    if not words:
        raise ValueError("text has no encodable characters")
    morse = "xx".join(words)
    extra = len(morse) % 3
    if extra:
        morse += "x" * (3 - extra)
    return morse


def _decode_morse(morse: str) -> str:
    """Inverse of _encode_morse, after padding x characters are stripped."""
    body = morse.rstrip("x")
    if not body:
        raise ValueError("fractionated Morse stream is empty")
    words: list[str] = []
    for word in body.split("xx"):
        letters: list[str] = []
        for piece in word.split("x"):
            if not piece:
                continue
            char = _MORSE_TO_CHAR.get(piece)
            if char is None:
                raise ValueError(f"not a Morse symbol in the fractionated stream: {piece}")
            letters.append(char)
        if letters:
            words.append("".join(letters))
    if not words:
        raise ValueError("fractionated Morse stream has no letters")
    return " ".join(words)


def fractionated_morse_encrypt(text: str, key: str) -> str:
    """Encrypt with a known fractionated Morse key. Returns A-Z ciphertext."""
    alphabet = fractionated_morse_key(key)
    table = {triple: alphabet[index] for index, triple in enumerate(_TRIPLES)}
    morse = _encode_morse(text)
    return "".join(table[morse[index : index + 3]] for index in range(0, len(morse), 3))


def fractionated_morse_decrypt(text: str, key: str) -> str:
    """Decrypt with a known fractionated Morse key.

    Non-letters in the ciphertext are ignored (they are grouping, not
    word spaces). Word spaces come back from the Morse "xx" gaps.
    Letters are uppercase.
    """
    alphabet = fractionated_morse_key(key)
    inverse = {letter: _TRIPLES[index] for index, letter in enumerate(alphabet)}
    cipher = letters_only(text)
    if not cipher:
        raise ValueError("text has no letters")
    unknown = sorted({ch for ch in cipher if ch not in inverse})
    if unknown:
        raise ValueError("ciphertext letter is not in the fractionated Morse key")
    morse = "".join(inverse[ch] for ch in cipher)
    return _decode_morse(morse)


def solve_fractionated_morse(text: str, *, key: str) -> SolveResult:
    """Recover fractionated Morse plaintext when the key is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    alphabet = fractionated_morse_key(key)
    plain = fractionated_morse_decrypt(text, alphabet)
    return SolveResult(
        method="fractionated_morse",
        plaintext=plain,
        key=alphabet,
        score=float(len(letters_only(plain))),
        details={
            "key": alphabet,
            "letters": len(letters_only(text)),
            "mode": "known_key",
            "scope": _SCOPE,
            "source_url": PRACTICAL_CRYPTOGRAPHY_URL,
        },
    )


__all__ = [
    "PRACTICAL_CRYPTOGRAPHY_CIPHER",
    "PRACTICAL_CRYPTOGRAPHY_KEY",
    "PRACTICAL_CRYPTOGRAPHY_MORSE",
    "PRACTICAL_CRYPTOGRAPHY_PLAIN",
    "PRACTICAL_CRYPTOGRAPHY_URL",
    "fractionated_morse_decrypt",
    "fractionated_morse_encrypt",
    "fractionated_morse_key",
    "solve_fractionated_morse",
]
