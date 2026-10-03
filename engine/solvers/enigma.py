"""Known-key three-rotor Enigma (Enigma I) solver.

The worked example is the one on Wikipedia's Enigma rotor details page
(fetched 2026-10-02):

  https://en.wikipedia.org/wiki/Enigma_rotor_details

  Rotors I, II, III (left to right), wide B reflector, ring settings
  AAA, start position AAA, no plugboard pairs: typing AAAAA produces
  BDZGO. The same page's ring-B example produces EWTYX.

This is the historical three-rotor machine (Enigma I), the military
form of the commercial Enigma: three rotors, a fixed reflector, and an
optional plugboard. The entry wheel is the military identity wheel.
It is a **known-key historical machine**. The key (rotors, rings,
start positions, plugboard) is supplied. It is **not** a break of an
unsolved intercept and **not** a claim about army message Nr. 86 or
Kryptos K4.
"""

from __future__ import annotations

from engine.alphabet import letters_only, reinject
from engine.result import SolveResult

# Wikipedia, Enigma rotor details (fetched 2026-10-02).
# https://en.wikipedia.org/wiki/Enigma_rotor_details
WIKIPEDIA_ROTOR_DETAILS_URL = "https://en.wikipedia.org/wiki/Enigma_rotor_details"
WIKIPEDIA_ROTORS = ("I", "II", "III")
WIKIPEDIA_REFLECTOR = "B"
WIKIPEDIA_RINGS = "AAA"
WIKIPEDIA_POSITIONS = "AAA"
WIKIPEDIA_PLUGBOARD: tuple[tuple[str, str], ...] = ()
WIKIPEDIA_PLAIN = "AAAAA"
WIKIPEDIA_CIPHER = "BDZGO"
# Same page: all ring settings in the B-position, start AAA.
WIKIPEDIA_RING_B = "BBB"
WIKIPEDIA_RING_B_CIPHER = "EWTYX"

_SCOPE = (
    "Known-key historical three-rotor Enigma only; "
    "not a break of an unsolved intercept and not a claim about "
    "army message Nr. 86 or Kryptos K4."
)

# Wiring is the permutation of the right-hand contacts onto the left-hand
# contacts at ring A and window A. Notch letters are the window letters
# from which a step carries the rotor onto the next letter and advances
# the rotor on its left (Wikipedia: I steps Q to R, II E to F, III V to W).
_ROTOR_WIRING: dict[str, str] = {
    "I": "EKMFLGDQVZNTOWYHXUSPAIBRCJ",
    "II": "AJDKSIRUXBLHWTMCQGZNPYFVOE",
    "III": "BDFHJLCPRTXVZNYEIWGAKMUSQO",
    "IV": "ESOVPZJAYQUIRHXLNFTGKDCMWB",
    "V": "VZBRGITYUPSDNHLXAWMJQOFECK",
}
_ROTOR_NOTCHES: dict[str, str] = {
    "I": "Q",
    "II": "E",
    "III": "V",
    "IV": "J",
    "V": "Z",
}
_REFLECTORS: dict[str, str] = {
    "B": "YRUHQSLDPXNGOKMIEBFZCWVJAT",
    "C": "FVPJIAOYEDRZXWGCTKUQSBNMHL",
}


def _index(letter: str) -> int:
    return ord(letter) - 65


def _letter(index: int) -> str:
    return chr(65 + (index % 26))


def _inverse(wiring: str) -> list[int]:
    forward = [_index(ch) for ch in wiring]
    backward = [0] * 26
    for src, dst in enumerate(forward):
        backward[dst] = src
    return backward


def _parse_rotor_name(name: str) -> str:
    token = name.strip().upper()
    if token not in _ROTOR_WIRING:
        raise ValueError(
            "three-rotor Enigma I rotor must be one of I, II, III, IV, V"
        )
    return token


def _parse_abc(value: str, what: str) -> tuple[int, int, int]:
    letters = letters_only(value)
    if len(letters) != 3:
        raise ValueError(f"{what} must be three A-Z letters")
    return (_index(letters[0]), _index(letters[1]), _index(letters[2]))


def parse_plugboard(pairs: object) -> tuple[tuple[str, str], ...]:
    """Disjoint letter pairs. An empty plugboard is the identity."""
    if pairs is None:
        return ()
    if isinstance(pairs, str):
        raw = pairs.replace(",", " ").replace("-", " ").split()
    else:
        raw = list(pairs)  # type: ignore[arg-type]
    used: set[str] = set()
    cleaned: list[tuple[str, str]] = []
    for item in raw:
        if isinstance(item, str):
            letters = letters_only(item)
        else:
            letters = "".join(letters_only(str(part)) for part in item)
        if len(letters) != 2:
            raise ValueError("each plugboard pair must be two letters")
        a, b = letters[0], letters[1]
        if a == b or a in used or b in used:
            raise ValueError("plugboard pairs must be disjoint and non-trivial")
        used.add(a)
        used.add(b)
        cleaned.append(tuple(sorted((a, b))))
    cleaned.sort()
    return tuple(cleaned)


def format_key(
    rotors: tuple[str, str, str],
    reflector: str,
    rings: str,
    positions: str,
    plugboard: tuple[tuple[str, str], ...],
) -> str:
    """Readable known-key settings. Empty plugboard is written as (none)."""
    plugs = " ".join(a + b for a, b in plugboard) if plugboard else "(none)"
    rotor_text = " ".join(rotors)
    return (
        f"reflector {reflector}; rotors {rotor_text} left-to-right; "
        f"rings {rings}; positions {positions}; plugboard {plugs}"
    )


class EnigmaMachine:
    """Three-rotor Enigma I. Steps before each letter, including double-step."""

    def __init__(
        self,
        rotors: tuple[str, str, str],
        reflector: str,
        rings: str,
        positions: str,
        plugboard: tuple[tuple[str, str], ...] = (),
    ) -> None:
        names = tuple(_parse_rotor_name(name) for name in rotors)
        if len(names) != 3:
            raise ValueError("this solver takes exactly three rotors")
        if len(set(names)) != 3:
            raise ValueError("the three rotors must be distinct")
        ukw = reflector.strip().upper()
        if ukw not in _REFLECTORS:
            raise ValueError("reflector must be B or C")
        self.names = names
        self.reflector_name = ukw
        self.forward = [tuple(_index(ch) for ch in _ROTOR_WIRING[name]) for name in names]
        self.backward = [_inverse(_ROTOR_WIRING[name]) for name in names]
        self.notches = [frozenset(_index(ch) for ch in _ROTOR_NOTCHES[name]) for name in names]
        self.reflector = tuple(_index(ch) for ch in _REFLECTORS[ukw])
        self.rings = _parse_abc(rings, "ring settings")
        self.positions = list(_parse_abc(positions, "start positions"))
        self.plug_map = list(range(26))
        for a, b in plugboard:
            ia, ib = _index(a), _index(b)
            self.plug_map[ia] = ib
            self.plug_map[ib] = ia

    def windows(self) -> str:
        return "".join(_letter(pos) for pos in self.positions)

    def step(self) -> None:
        """Pawl step. Middle rotor double-steps when it is sitting on its notch."""
        left, middle, right = 0, 1, 2
        middle_on_notch = self.positions[middle] in self.notches[middle]
        right_on_notch = self.positions[right] in self.notches[right]
        if middle_on_notch:
            self.positions[left] = (self.positions[left] + 1) % 26
            self.positions[middle] = (self.positions[middle] + 1) % 26
        elif right_on_notch:
            self.positions[middle] = (self.positions[middle] + 1) % 26
        self.positions[right] = (self.positions[right] + 1) % 26

    def _through_rotor(self, index: int, contact: int, *, inverse: bool) -> int:
        shift = (self.positions[index] - self.rings[index]) % 26
        table = self.backward[index] if inverse else self.forward[index]
        entered = (contact + shift) % 26
        left = table[entered]
        return (left - shift) % 26

    def encrypt_letter(self, letter: str) -> str:
        self.step()
        contact = self.plug_map[_index(letter)]
        for index in (2, 1, 0):
            contact = self._through_rotor(index, contact, inverse=False)
        contact = self.reflector[contact]
        for index in (0, 1, 2):
            contact = self._through_rotor(index, contact, inverse=True)
        return _letter(self.plug_map[contact])

    def process(self, text: str) -> str:
        stream = letters_only(text)
        if not stream:
            raise ValueError("text has no letters")
        return "".join(self.encrypt_letter(ch) for ch in stream)


def _machine(
    rotors: tuple[str, str, str] | list[str],
    reflector: str,
    rings: str,
    positions: str,
    plugboard: object,
) -> tuple[EnigmaMachine, tuple[str, str, str], str, str, str, tuple[tuple[str, str], ...]]:
    names = tuple(_parse_rotor_name(name) for name in rotors)
    if len(names) != 3:
        raise ValueError("this solver takes exactly three rotors")
    plugs = parse_plugboard(plugboard)
    ring_letters = letters_only(rings)
    position_letters = letters_only(positions)
    machine = EnigmaMachine(names, reflector, ring_letters, position_letters, plugs)
    return machine, names, reflector.strip().upper(), ring_letters, position_letters, plugs


def enigma_encrypt(
    text: str,
    *,
    rotors: tuple[str, str, str] | list[str] = WIKIPEDIA_ROTORS,
    reflector: str = WIKIPEDIA_REFLECTOR,
    rings: str = WIKIPEDIA_RINGS,
    positions: str = WIKIPEDIA_POSITIONS,
    plugboard: object = WIKIPEDIA_PLUGBOARD,
) -> str:
    """Encrypt with a known three-rotor Enigma key. Non-letters are dropped."""
    machine, *_rest = _machine(rotors, reflector, rings, positions, plugboard)
    return machine.process(text)


def enigma_decrypt(
    text: str,
    *,
    rotors: tuple[str, str, str] | list[str] = WIKIPEDIA_ROTORS,
    reflector: str = WIKIPEDIA_REFLECTOR,
    rings: str = WIKIPEDIA_RINGS,
    positions: str = WIKIPEDIA_POSITIONS,
    plugboard: object = WIKIPEDIA_PLUGBOARD,
) -> str:
    """Decrypt with a known key. The machine is reciprocal, so this re-enciphers."""
    return enigma_encrypt(
        text,
        rotors=rotors,
        reflector=reflector,
        rings=rings,
        positions=positions,
        plugboard=plugboard,
    )


def windows_after_steps(
    steps: int,
    *,
    rotors: tuple[str, str, str] | list[str] = WIKIPEDIA_ROTORS,
    reflector: str = WIKIPEDIA_REFLECTOR,
    rings: str = WIKIPEDIA_RINGS,
    positions: str = WIKIPEDIA_POSITIONS,
    plugboard: object = WIKIPEDIA_PLUGBOARD,
) -> list[str]:
    """Window letters after each key-press step, before the lamp is read."""
    machine, *_rest = _machine(rotors, reflector, rings, positions, plugboard)
    seen: list[str] = []
    for _ in range(steps):
        machine.step()
        seen.append(machine.windows())
    return seen


def solve_enigma(
    text: str,
    *,
    rotors: tuple[str, str, str] | list[str] = WIKIPEDIA_ROTORS,
    reflector: str = WIKIPEDIA_REFLECTOR,
    rings: str = WIKIPEDIA_RINGS,
    positions: str = WIKIPEDIA_POSITIONS,
    plugboard: object = WIKIPEDIA_PLUGBOARD,
) -> SolveResult:
    """Recover plaintext when the three-rotor key is already known.

    Known-key historical machine only. Not a break of an unsolved intercept
    and not a claim about army message Nr. 86 or Kryptos K4.
    """
    machine, names, ukw, ring_letters, position_letters, plugs = _machine(
        rotors, reflector, rings, positions, plugboard
    )
    plain_letters = machine.process(text)
    rendered = reinject(text, plain_letters) if any(not ch.isalpha() for ch in text) else plain_letters
    key = format_key(names, ukw, ring_letters, position_letters, plugs)
    return SolveResult(
        method="enigma",
        plaintext=rendered,
        key=key,
        score=float(len(plain_letters)),
        details={
            "rotors": list(names),
            "reflector": ukw,
            "rings": ring_letters,
            "positions": position_letters,
            "plugboard": [a + b for a, b in plugs],
            "letters": len(letters_only(text)),
            "mode": "known_key",
            "scope": _SCOPE,
            "source_url": WIKIPEDIA_ROTOR_DETAILS_URL,
        },
    )


__all__ = [
    "WIKIPEDIA_CIPHER",
    "WIKIPEDIA_PLAIN",
    "WIKIPEDIA_PLUGBOARD",
    "WIKIPEDIA_POSITIONS",
    "WIKIPEDIA_REFLECTOR",
    "WIKIPEDIA_RING_B",
    "WIKIPEDIA_RING_B_CIPHER",
    "WIKIPEDIA_RINGS",
    "WIKIPEDIA_ROTORS",
    "WIKIPEDIA_ROTOR_DETAILS_URL",
    "EnigmaMachine",
    "enigma_decrypt",
    "enigma_encrypt",
    "format_key",
    "parse_plugboard",
    "solve_enigma",
    "windows_after_steps",
]
