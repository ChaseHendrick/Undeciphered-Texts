"""Explicit Baconian binary decoding and specified textual carrier extraction.

ACA source: https://www.cryptogram.org/downloads/aca.info/ciphers/Baconian.pdf
Its 24-letter alphabet merges I/J and U/V. Both printed carrier examples
are independently tested. A separate explicit 26-letter implementation
variant maps A..Z to integers 0..25; it is not the ACA printed alphabet.
No font, image, stylistic channel, or hidden extraction rule is inferred.
"""

from __future__ import annotations

from engine.result import SolveResult

ACA_URL = "https://www.cryptogram.org/downloads/aca.info/ciphers/Baconian.pdf"
ACA_CARRIER_INITIALS = (
    "Now is a good time to attend college. School work is a good teacher "
    "and a good builder of character. Every man should be a student and "
    "learn all that there is about a subject."
)
ACA_CARRIER_LETTERS = "BOWED ASTER PINED JOKED THEIR BLACK HASTE ARRAY INSET CHEST SLING."
MAX_CARRIER_CHARACTERS = 100_000
MAX_UNITS = 10_000
_ALPHABETS = {"24": "ABCDEFGHIKLMNOPQRSTUWXYZ", "26": "ABCDEFGHIJKLMNOPQRSTUVWXYZ"}
_ASCII = frozenset("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz")


def _alphabet(variant: str) -> str:
    if not isinstance(variant, str):
        raise TypeError("variant must be the explicit string '24' or '26'")
    if variant not in _ALPHABETS:
        raise ValueError("variant must be '24' or '26'")
    return _ALPHABETS[variant]


def _text(text: str) -> str:
    if not isinstance(text, str):
        raise TypeError("Baconian input must be text")
    if not text or len(text) > MAX_CARRIER_CHARACTERS:
        raise ValueError(f"input must contain 1..{MAX_CARRIER_CHARACTERS} characters")
    if any(ch.isalpha() and ch not in _ASCII for ch in text):
        raise ValueError("textual extraction accepts A-Z letters only")
    return text


def _direct_units(text: str) -> str:
    _text(text)
    if any(ch not in "abAB" and not ch.isspace() for ch in text):
        raise ValueError("direct codes accept only a/b and whitespace")
    tokens = text.split()
    if len(tokens) > 1 and any(len(token) != 5 for token in tokens):
        raise ValueError("whitespace-separated direct codes must each contain five units")
    units = "".join(tokens).lower()
    if not units or len(units) > MAX_UNITS or len(units) % 5:
        raise ValueError(f"direct code length must be a positive multiple of five, at most {MAX_UNITS} units")
    return units


def baconian_extract(text: str, *, extraction: str) -> str:
    """Extract a/b using an explicit direct, word_initials, or every_letter rule.

    Word initials use whitespace-separated tokens, retaining apostrophes
    and hyphens inside a token. Tokens without an ASCII letter are ignored;
    the first ASCII letter of each remaining token supplies its class.
    Both textual carrier rules map A-M to a and N-Z to b.
    """
    if not isinstance(extraction, str) or extraction not in ("direct", "word_initials", "every_letter"):
        raise ValueError("extraction must be direct, word_initials, or every_letter")
    if extraction == "direct":
        return _direct_units(text)
    _text(text)
    if extraction == "every_letter":
        letters = [ch.upper() for ch in text if ch in _ASCII]
    else:
        letters = [letter for token in text.split()
                   if (letter := next((ch.upper() for ch in token if ch in _ASCII), None)) is not None]
    if not 1 <= len(letters) <= MAX_UNITS:
        raise ValueError(f"carrier must yield 1..{MAX_UNITS} units")
    return "".join("a" if letter <= "M" else "b" for letter in letters)


def baconian_decode(units: str, *, variant: str) -> str:
    """Decode complete five-unit groups; reject unused binary codes."""
    alphabet = _alphabet(variant)
    normalized = _direct_units(units)
    output = []
    for offset in range(0, len(normalized), 5):
        group = normalized[offset:offset + 5]
        value = int(group.translate(str.maketrans("ab", "01")), 2)
        if value >= len(alphabet):
            raise ValueError(f"unused {variant}-letter code {group} at unit offset {offset}")
        output.append(alphabet[value])
    return "".join(output)


def baconian_encode(text: str, *, variant: str) -> str:
    """Encode uppercase A-Z, omitting spacing; 24 merges J->I and V->U."""
    alphabet = _alphabet(variant)
    _text(text)
    letters = "".join(ch.upper() for ch in text if ch in _ASCII)
    if not letters or len(letters) * 5 > MAX_UNITS:
        raise ValueError(f"plaintext must contain 1..{MAX_UNITS // 5} A-Z letters")
    if variant == "24":
        letters = letters.replace("J", "I").replace("V", "U")
    return "".join(format(alphabet.index(letter), "05b").translate(str.maketrans("01", "ab")) for letter in letters)


def solve_baconian(text: str, *, extraction: str, variant: str) -> SolveResult:
    """Decode only the caller's specified extraction and alphabet convention."""
    alphabet = _alphabet(variant)
    units = baconian_extract(text, extraction=extraction)
    plaintext = baconian_decode(units, variant=variant)
    choices = []
    if variant == "24":
        choices = [{"offset": index, "choices": [letter, "J" if letter == "I" else "V"]}
                   for index, letter in enumerate(plaintext) if letter in "IU"]
    return SolveResult("baconian", plaintext, f"extraction={extraction} variant={variant}", float(len(plaintext)), {
        "mode": "specified_extraction", "extraction": extraction, "variant": variant,
        "alphabet": alphabet, "units": units, "unit_count": len(units), "group_width": 5,
        "carrier_partition": None if extraction == "direct" else "A-M=a, N-Z=b",
        "word_tokenization": "whitespace tokens, first ASCII letter" if extraction == "word_initials" else None,
        "plaintext_spacing_lost": True, "merged_letter_choices": choices,
        "source_url": ACA_URL,
        "scope": "Specified textual Baconian decoding. No extraction detection, visual font interpretation, or historical decipherment is claimed.",
    })
