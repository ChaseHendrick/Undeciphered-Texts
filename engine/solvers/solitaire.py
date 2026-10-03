"""Solitaire (Pontifex) known-deck keystream cipher.

Bruce Schneier, "The Solitaire Encryption Algorithm", version 1.2
(26 May 1999), fetched 2026-10-03:

  https://www.schneier.com/academic/solitaire/

Solitaire is an output-feedback stream cipher. A 54-card deck (52 cards
plus two distinct jokers) is the key. Each output step moves the A joker
down one card, moves the B joker down two cards, triple-cuts around the
jokers, then count-cuts on the bottom card. The top card selects the
output card. A joker output is skipped and the step repeats. Output
cards become keystream numbers 1 through 26. Encryption adds the
keystream to plaintext modulo 26 (A=1). Decryption subtracts it.

The unkeyed deck is bridge order: clubs, diamonds, hearts, spades, then
the A joker, then the B joker. A passphrase key uses Schneier's method 3:
the same steps, with a second count cut from each passphrase letter
instead of an output. The optional joker-placement step is not used.
That is the choice the published samples use.

This module is a **known classical-cipher** solver (a known-cipher
solver). It recovers a reading only when the deck or the passphrase is
supplied. It is **not** an unknown-script reading. It does **not** claim
Kryptos K4, the Zodiac ciphers, the Beale ciphers, the McCormick
cipher, the Voynich manuscript, or army message Nr. 86.
"""

from __future__ import annotations

from engine.result import SolveResult

SCHNEIER_SOLITAIRE_URL = "https://www.schneier.com/academic/solitaire/"

# Sample 1 on that page. Unkeyed deck. No passphrase.
SCHNEIER_SOLITAIRE_UNKEYED_PLAIN = "AAAAAAAAAA"
SCHNEIER_SOLITAIRE_UNKEYED_CIPHER = "EXKYI ZSGEH"
# Raw step-5 cards, including the skipped joker the page writes as (53).
SCHNEIER_SOLITAIRE_UNKEYED_RAW = (4, 49, 10, 53, 24, 8, 51, 44, 6, 4, 33)

# Sample 2. Key letters are FOO. The comma in the page's quotation is
# sentence punctuation, not a key character. Optional joker placement is off.
SCHNEIER_SOLITAIRE_FOO_KEY = "FOO"
SCHNEIER_SOLITAIRE_FOO_PLAIN = "AAAAAAAAAAAAAAA"
SCHNEIER_SOLITAIRE_FOO_CIPHER = "ITHZU JIWGR FARMW"
SCHNEIER_SOLITAIRE_FOO_RAW = (
    8, 19, 7, 25, 20, 53, 9, 8, 22, 32, 43, 5, 26, 17, 53, 38, 48,
)

# Sample 3. Message SOLITAIRE, last group filled with X, key CRYPTONOMICON.
SCHNEIER_SOLITAIRE_KEY = "CRYPTONOMICON"
SCHNEIER_SOLITAIRE_MESSAGE = "SOLITAIRE"
SCHNEIER_SOLITAIRE_PLAIN = "SOLITAIREX"
SCHNEIER_SOLITAIRE_CIPHER = "KIRAK SFJAN"

JOKER_A = 53
JOKER_B = 54
_GROUP = 5

_SCOPE = (
    "Known classical Solitaire (Pontifex) keystream solver only; "
    "not an unknown-script reading and not a claim about Kryptos K4, "
    "the Zodiac ciphers, the Beale ciphers, the McCormick cipher, "
    "the Voynich manuscript, or army message Nr. 86."
)


def _letters(text: str) -> str:
    """Uppercase A-Z letters, in order. Spaces and punctuation are dropped."""
    if not isinstance(text, str):
        raise ValueError("solitaire text must be a string")
    return "".join(ch.upper() for ch in text if ch.isascii() and ch.isalpha())


def normalize_passphrase(key: str) -> str:
    """Passphrase letters A-Z. An empty string is the unkeyed deck.

    Non-letters are ignored, matching a passphrase such as "SECRET KEY"
    on the Schneier page. A non-empty key that contains no letters is
    rejected so a typo is not silently treated as unkeyed.
    """
    if not isinstance(key, str):
        raise ValueError("solitaire passphrase must be a string")
    if key == "":
        return ""
    letters = _letters(key)
    if not letters:
        raise ValueError("solitaire passphrase must contain at least one letter")
    return letters


def unkeyed_deck() -> list[int]:
    """Bridge-order deck: 1..52, A joker (53), B joker (54)."""
    return list(range(1, 53)) + [JOKER_A, JOKER_B]


def normalize_deck(deck: list[int]) -> list[int]:
    """Return a copy of a 54-card deck.

    Cards 1..52 are clubs, diamonds, hearts, spades in bridge order
    (ace through king in each suit). 53 is the A joker. 54 is the B joker.
    """
    if not isinstance(deck, list) or len(deck) != 54:
        raise ValueError("solitaire deck must be a list of 54 cards")
    if sorted(deck) != list(range(1, 55)):
        raise ValueError("solitaire deck must be a permutation of 1..54")
    return list(deck)


def _count_value(card: int) -> int:
    """1..52 stay themselves. Either joker counts as 53."""
    if card >= JOKER_A:
        return 53
    return card


def _letter_value(card: int) -> int | None:
    """Keystream number 1..26, or None when the output card is a joker.

    Clubs and hearts are 1..13. Diamonds and spades are 14..26.
    """
    if card >= JOKER_A:
        return None
    if card <= 26:
        return card
    return card - 26


def _move_down(deck: list[int], card: int, steps: int) -> None:
    """Move one card down `steps` places.

    A card on the bottom is reinserted just below the top card, not as
    the new top. That is Schneier's wrap rule. Repeating a one-card move
    covers the B joker sitting one up from the bottom.
    """
    for _ in range(steps):
        pos = deck.index(card)
        if pos == len(deck) - 1:
            deck.pop()
            deck.insert(1, card)
        else:
            deck[pos], deck[pos + 1] = deck[pos + 1], deck[pos]


def _triple_cut(deck: list[int]) -> None:
    """Swap the cards above the first joker with the cards below the second.

    The jokers and the cards between them stay in place. "First" and
    "second" ignore the A and B labels. An empty side stays empty.
    """
    first = min(deck.index(JOKER_A), deck.index(JOKER_B))
    second = max(deck.index(JOKER_A), deck.index(JOKER_B))
    deck[:] = deck[second + 1 :] + deck[first : second + 1] + deck[:first]


def _count_cut(deck: list[int], count: int | None = None) -> None:
    """Cut `count` cards from the top to just above the bottom card.

    The bottom card does not move. With no count, the bottom card's own
    value is used. A count of 53 (a joker) leaves the deck unchanged.
    """
    if count is None:
        count = _count_value(deck[-1])
    if count == 53:
        return
    if count < 1 or count > 52:
        raise ValueError("solitaire count cut must be from 1 to 53")
    deck[:] = deck[count:-1] + deck[:count] + deck[-1:]


def _output_card(deck: list[int]) -> int:
    """Run one Solitaire step and return the output card (53 means a joker).

    The top card is number 1. The card after the counted card is the
    output. This does not remove that card. Caller skips jokers and
    repeats from the joker moves.
    """
    _move_down(deck, JOKER_A, 1)
    _move_down(deck, JOKER_B, 2)
    _triple_cut(deck)
    _count_cut(deck)
    count = _count_value(deck[0])
    card = deck[count]
    if card >= JOKER_A:
        return 53
    return card


def _apply_passphrase(deck: list[int], passphrase: str) -> None:
    """Keying method 3. Optional final joker placement is not applied."""
    for ch in passphrase:
        value = ord(ch) - 64
        _move_down(deck, JOKER_A, 1)
        _move_down(deck, JOKER_B, 2)
        _triple_cut(deck)
        _count_cut(deck)
        _count_cut(deck, value)


def keyed_deck(key: str = "", deck: list[int] | None = None) -> list[int]:
    """Copy a starting deck and, when `key` is set, run passphrase keying.

    Pass a deck or a passphrase, not both. An empty key and no deck is
    the unkeyed bridge-order deck.
    """
    if deck is not None and key != "":
        raise ValueError("pass a solitaire passphrase or a deck, not both")
    cards = unkeyed_deck() if deck is None else normalize_deck(deck)
    passphrase = normalize_passphrase(key)
    if passphrase:
        _apply_passphrase(cards, passphrase)
    return cards


def raw_output_cards(
    count: int,
    key: str = "",
    *,
    deck: list[int] | None = None,
) -> list[int]:
    """Return `count` step-5 cards. A skipped joker is recorded as 53.

    Card values 1..52 are the bridge-order ranks. 53 is a joker output
    and is not a keystream letter.
    """
    if not isinstance(count, int) or count < 1:
        raise ValueError("solitaire output count must be a positive integer")
    cards = keyed_deck(key, deck)
    return [_output_card(cards) for _ in range(count)]


def keystream_numbers(
    count: int,
    key: str = "",
    *,
    deck: list[int] | None = None,
) -> list[int]:
    """Return `count` keystream numbers in 1..26, skipping joker outputs."""
    if not isinstance(count, int) or count < 1:
        raise ValueError("solitaire keystream count must be a positive integer")
    cards = keyed_deck(key, deck)
    numbers: list[int] = []
    while len(numbers) < count:
        card = _output_card(cards)
        value = None if card == 53 else _letter_value(card)
        if value is not None:
            numbers.append(value)
    return numbers


def _group(letters: str) -> str:
    """Groups of five. A short final group is kept."""
    return " ".join(
        letters[index : index + _GROUP] for index in range(0, len(letters), _GROUP)
    )


def _pad(letters: str) -> str:
    """Fill the last five-character group with X, as the page specifies."""
    if not letters:
        raise ValueError("solitaire text must contain at least one letter")
    extra = (-len(letters)) % _GROUP
    return letters + ("X" * extra)


def solitaire_encrypt(
    text: str,
    key: str = "",
    *,
    deck: list[int] | None = None,
) -> str:
    """Encrypt with a known deck or a known passphrase.

    Letters only. The last group is filled with X when the letter count
    is not a multiple of five. Ciphertext is grouped in fives. A=1.
    Addition is modulo 26, with a sum of 27 written as 1.
    """
    plain = _pad(_letters(text))
    stream = keystream_numbers(len(plain), key, deck=deck)
    out = []
    for letter, shift in zip(plain, stream):
        number = (ord(letter) - 64 + shift - 1) % 26 + 1
        out.append(chr(number + 64))
    return _group("".join(out))


def solitaire_decrypt(
    text: str,
    key: str = "",
    *,
    deck: list[int] | None = None,
) -> str:
    """Decrypt with the same deck or passphrase used to encrypt.

    Group spaces are ignored. A filler X that encryption added is
    returned as a letter; this function does not strip it. Subtraction
    is modulo 26 (A=1). When the ciphertext number is less than or equal
    to the keystream number, 26 is added before subtracting.
    """
    letters = _letters(text)
    if not letters:
        raise ValueError("solitaire ciphertext must contain at least one letter")
    stream = keystream_numbers(len(letters), key, deck=deck)
    out = []
    for letter, shift in zip(letters, stream):
        number = (ord(letter) - 64 - shift - 1) % 26 + 1
        out.append(chr(number + 64))
    return "".join(out)


def solve_solitaire(
    text: str,
    *,
    key: str = "",
    deck: list[int] | None = None,
) -> SolveResult:
    """Recover Solitaire plaintext when the deck or passphrase is known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about Kryptos K4, Zodiac, Beale, McCormick, Voynich, or Nr. 86.
    """
    if deck is not None and key != "":
        raise ValueError("pass a solitaire passphrase or a deck, not both")
    passphrase = "" if deck is not None else normalize_passphrase(key)
    plain = solitaire_decrypt(text, passphrase, deck=deck)
    shown_key = passphrase if passphrase else "unkeyed"
    if deck is not None:
        shown_key = "deck"
    return SolveResult(
        method="solitaire",
        plaintext=plain,
        key=shown_key,
        score=float(len(plain)),
        details={
            "key": shown_key,
            "passphrase": passphrase,
            "deck_keying": "explicit_deck" if deck is not None else (
                "passphrase" if passphrase else "unkeyed"
            ),
            "letters": len(plain),
            "mode": "known_solitaire_keystream",
            "variant": "schneier_1_2",
            "scope": _SCOPE,
            "source_url": SCHNEIER_SOLITAIRE_URL,
        },
    )


__all__ = [
    "JOKER_A",
    "JOKER_B",
    "SCHNEIER_SOLITAIRE_CIPHER",
    "SCHNEIER_SOLITAIRE_FOO_CIPHER",
    "SCHNEIER_SOLITAIRE_FOO_KEY",
    "SCHNEIER_SOLITAIRE_FOO_PLAIN",
    "SCHNEIER_SOLITAIRE_FOO_RAW",
    "SCHNEIER_SOLITAIRE_KEY",
    "SCHNEIER_SOLITAIRE_MESSAGE",
    "SCHNEIER_SOLITAIRE_PLAIN",
    "SCHNEIER_SOLITAIRE_UNKEYED_CIPHER",
    "SCHNEIER_SOLITAIRE_UNKEYED_PLAIN",
    "SCHNEIER_SOLITAIRE_UNKEYED_RAW",
    "SCHNEIER_SOLITAIRE_URL",
    "keyed_deck",
    "keystream_numbers",
    "normalize_deck",
    "normalize_passphrase",
    "raw_output_cards",
    "solitaire_decrypt",
    "solitaire_encrypt",
    "solve_solitaire",
    "unkeyed_deck",
]
