"""Chaocipher known-alphabet encrypt and decrypt.

Programming Praxis, 6 July 2010, gives the worked example of the algorithm
Moshe Rubin published from John F. Byrne's papers:

  https://programmingpraxis.com/2010/07/06/chaocipher/

Two 26-letter disks start in a known order. The left disk is the ciphertext
alphabet. The right disk is the plaintext alphabet. To encrypt, find the
plaintext letter on the right disk and take the left-disk letter in the same
position. To decrypt, find the ciphertext letter on the left disk and take
the right-disk letter in the same position.

After each letter both disks are permuted. Zenith is position 1 and nadir
is position 14.

Left disk (ciphertext letter just used):
1. Rotate left until that ciphertext letter is at position 1.
2. Cycle positions 2 through 14 one place to the left. The letter that was
   in position 2 moves to position 14.

Right disk (plaintext letter just used):
1. Rotate left until that plaintext letter is at position 1.
2. Move position 1 to the end.
3. Cycle positions 3 through 14 one place to the left. The letter that was
   in position 3 moves to position 14.

The page's illustration: left HXUCZVAMDSLKPEFJRIGTWOBNYQ with ciphertext
letter P becomes PFJRIGTWOBNYQEHXUCZVAMDSLK. Right
PTLNBQDEOYSFAVZKGJRIHWXUMC with plaintext letter A becomes
VZGJRIHWXUMCPKTLNBQDEOYSFA.

The same starting disks encrypt WELLDONEISBETTERTHANWELLSAID to
OAHQHCNYNXTSZJRRHJBYHQKSOUJY.

This module is a **known classical-cipher** solver (a known-cipher
solver). It recovers a reading only when both starting alphabets are
supplied. It checks the revealed algorithm's published test vector. It
is **not** a claim that Byrne's challenge exhibits are solved. It is
**not** an unknown-script reading and **not** a claim about Kryptos K4,
Zodiac, Beale, McCormick, Voynich, or army message Nr. 86.
"""

from __future__ import annotations

from engine.alphabet import letters_only
from engine.language import get_model
from engine.result import SolveResult

PRAXIS_URL = "https://programmingpraxis.com/2010/07/06/chaocipher/"
PRAXIS_LEFT = "HXUCZVAMDSLKPEFJRIGTWOBNYQ"
PRAXIS_RIGHT = "PTLNBQDEOYSFAVZKGJRIHWXUMC"
PRAXIS_PLAIN = "WELLDONEISBETTERTHANWELLSAID"
PRAXIS_CIPHER = "OAHQHCNYNXTSZJRRHJBYHQKSOUJY"
# Standalone permutation steps printed on the same page.
PRAXIS_LEFT_AFTER_P = "PFJRIGTWOBNYQEHXUCZVAMDSLK"
PRAXIS_RIGHT_AFTER_A = "VZGJRIHWXUMCPKTLNBQDEOYSFA"

_SCOPE = (
    "Known classical Chaocipher solver only; "
    "the Programming Praxis vector is the revealed algorithm's test vector, "
    "not a claim that Byrne's challenge exhibits are solved; "
    "not an unknown-script reading and not a claim about Kryptos K4, "
    "Zodiac, Beale, McCormick, Voynich, or army message Nr. 86."
)


def _alphabet(alphabet: str, name: str) -> str:
    cleaned = letters_only(alphabet)
    if len(cleaned) != 26 or len(set(cleaned)) != 26:
        raise ValueError(f"Chaocipher {name} alphabet must be 26 distinct letters")
    return cleaned


def permute_left(disk: str, cipher_letter: str) -> str:
    """Permute the ciphertext disk after one letter. See the module note."""
    if len(disk) != 26:
        raise ValueError("Chaocipher disk must be 26 letters")
    index = disk.find(cipher_letter)
    if index < 0:
        raise ValueError("ciphertext letter is not on the left disk")
    rotated = disk[index:] + disk[:index]
    return rotated[0] + rotated[2:14] + rotated[1] + rotated[14:]


def permute_right(disk: str, plain_letter: str) -> str:
    """Permute the plaintext disk after one letter. See the module note."""
    if len(disk) != 26:
        raise ValueError("Chaocipher disk must be 26 letters")
    index = disk.find(plain_letter)
    if index < 0:
        raise ValueError("plaintext letter is not on the right disk")
    rotated = disk[index:] + disk[:index]
    shifted = rotated[1:] + rotated[0]
    return shifted[:2] + shifted[3:14] + shifted[2] + shifted[14:]


def chaocipher_encrypt(text: str, left: str, right: str) -> str:
    """Encrypt with known starting left and right alphabets.

    Non-letters are dropped. The returned string is uppercase A-Z.
    """
    cipher_disk = _alphabet(left, "left")
    plain_disk = _alphabet(right, "right")
    letters = letters_only(text)
    if not letters:
        raise ValueError("text has no letters")
    out: list[str] = []
    for plain in letters:
        index = plain_disk.find(plain)
        if index < 0:
            raise ValueError("plaintext letter is not on the right disk")
        cipher = cipher_disk[index]
        out.append(cipher)
        cipher_disk = permute_left(cipher_disk, cipher)
        plain_disk = permute_right(plain_disk, plain)
    return "".join(out)


def chaocipher_decrypt(text: str, left: str, right: str) -> str:
    """Decrypt with known starting left and right alphabets.

    Non-letters are dropped. The returned string is uppercase A-Z.
    The disks must be the starting alphabets, not the alphabets left
    behind by a previous encrypt or decrypt.
    """
    cipher_disk = _alphabet(left, "left")
    plain_disk = _alphabet(right, "right")
    letters = letters_only(text)
    if not letters:
        raise ValueError("text has no letters")
    out: list[str] = []
    for cipher in letters:
        index = cipher_disk.find(cipher)
        if index < 0:
            raise ValueError("ciphertext letter is not on the left disk")
        plain = plain_disk[index]
        out.append(plain)
        cipher_disk = permute_left(cipher_disk, cipher)
        plain_disk = permute_right(plain_disk, plain)
    return "".join(out)


def solve_chaocipher(text: str, *, left: str, right: str) -> SolveResult:
    """Recover Chaocipher plaintext when both starting alphabets are known.

    Known-cipher decrypt only. The Programming Praxis vector is the
    revealed algorithm's test vector, not a claim that Byrne's challenge
    exhibits are solved. Not an unknown-script reading and not a claim
    about Kryptos K4, Zodiac, Beale, McCormick, Voynich, or army message
    Nr. 86.
    """
    cipher_disk = _alphabet(left, "left")
    plain_disk = _alphabet(right, "right")
    plain_letters = chaocipher_decrypt(text, cipher_disk, plain_disk)
    az = [ord(ch) - 65 for ch in plain_letters]
    return SolveResult(
        method="chaocipher",
        plaintext=plain_letters,
        key=f"{cipher_disk}|{plain_disk}",
        score=get_model().score(az) if az else 0.0,
        details={
            "left": cipher_disk,
            "right": plain_disk,
            "letters": len(letters_only(text)),
            "mode": "known_alphabets",
            "scope": _SCOPE,
            "source_url": PRAXIS_URL,
        },
    )


__all__ = [
    "PRAXIS_CIPHER",
    "PRAXIS_LEFT",
    "PRAXIS_LEFT_AFTER_P",
    "PRAXIS_PLAIN",
    "PRAXIS_RIGHT",
    "PRAXIS_RIGHT_AFTER_A",
    "PRAXIS_URL",
    "chaocipher_decrypt",
    "chaocipher_encrypt",
    "permute_left",
    "permute_right",
    "solve_chaocipher",
]
