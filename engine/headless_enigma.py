"""Headless army Enigma. No keyboard, no invented daily key.

The machine is the repo's three-rotor Enigma I. A daily key is rotors,
rings, reflector, and plugboard. Each message adds a Grundstellung and
the enciphered message setting. A dash is a letter the clerk did not
read: the wheels step, and the output keeps a hole. solved stays false.
"""

from __future__ import annotations

from engine.german import get_german_model, german_letters
from engine.lxaca_neighborhood import (
    DEROP_CONTROL_TEXT,
    DEROP_GROUND,
    DEROP_PREFIX,
    DEROP_SECOND,
    DEROP_START,
    LXACA_BODY,
    LXACA_GROUND,
    LXACA_SECOND,
    PUBLISHED_KEYS,
)
from engine.solvers.enigma import EnigmaMachine, parse_plugboard

_ROMAN = {"1": "I", "2": "II", "3": "III", "4": "IV", "5": "V"}

# July message page, fetched 4 October 2026. The first group is the Kenngruppe.
# KLJBO's dashes are unread letters, not guesses.
KLJBO_GROUND = "RGN"
KLJBO_SECOND = "KUI"
KLJBO_BODY = "YNGZOWCIRESGVEVKFGCNXDTLIKINLBOYL-NTNYBD-NWK-A-UVV"
JBIYH_GROUND = "BSB"
JBIYH_SECOND = "NTK"
JBIYH_BODY = "NVYMIVLOGGKTDKKOYXWRDLBHRRZYPILVVXOGBEFXAXCWBNGILRWARXO"

OPEN_MESSAGES = (
    {"name": "KLJBO", "number": 87, "date": "1941-07-03", "ground": KLJBO_GROUND,
     "second": KLJBO_SECOND, "body": KLJBO_BODY, "daily_key_published": False},
    {"name": "LXACA", "number": 100, "date": "1941-07-05", "ground": LXACA_GROUND,
     "second": LXACA_SECOND, "body": LXACA_BODY, "daily_key_published": True},
    {"name": "JBIYH", "number": 242, "date": "1941-07-20", "ground": JBIYH_GROUND,
     "second": JBIYH_SECOND, "body": JBIYH_BODY, "daily_key_published": False},
)


class HeadlessEnigma:
    """One day's machine. It enciphers. It does not decide that the text is German."""

    def __init__(self, rotors: tuple[str, str, str], rings: str, plugboard: object, reflector: str = "B") -> None:
        if len(rotors) != 3:
            raise ValueError("army Enigma I takes three rotors")
        self.rotors = tuple(rotors)
        self.rings = rings
        self.plugboard = parse_plugboard(plugboard)
        self.reflector = reflector

    @classmethod
    def from_walzenlage(cls, walzenlage: str, rings: str, stecker: str, reflector: str = "B") -> "HeadlessEnigma":
        """Walzenlage is three digits, left to right, as on the key sheet."""
        if len(walzenlage) != 3 or any(ch not in _ROMAN for ch in walzenlage):
            raise ValueError("walzenlage must be three digits from 1 to 5")
        rotors = tuple(_ROMAN[ch] for ch in walzenlage)
        return cls(rotors, rings, stecker, reflector)

    def _machine(self, start: str) -> EnigmaMachine:
        return EnigmaMachine(self.rotors, self.reflector, self.rings, start, self.plugboard)

    def feed(self, start: str, text: str) -> str:
        """Encipher or decipher. A dash steps once and stays a hole. Spaces are ignored."""
        if len(start) != 3 or not start.isalpha():
            raise ValueError("window setting must be three letters")
        machine = self._machine(start)
        out: list[str] = []
        for char in text:
            if char == "-":
                machine.step()
                out.append("?")
            elif char.isalpha():
                out.append(machine.encrypt_letter(char))
        if not out:
            raise ValueError("text has no letters")
        return "".join(out)

    def message_setting(self, ground: str, enciphered: str) -> str:
        """Recover the three-letter start from the Grundstellung and the second group."""
        if len(enciphered) != 3 or not enciphered.isalpha():
            raise ValueError("enciphered message setting must be three letters")
        return self.feed(ground, enciphered)

    def open_spruch(self, ground: str, enciphered: str, body: str) -> dict:
        """Return the start and the letters. This is not a claim that they are German."""
        start = self.message_setting(ground, enciphered)
        return {
            "start": start,
            "text": self.feed(start, body),
            "claimed_plaintext": None,
        }


def _mean_score(text: str) -> float | None:
    """Score only a complete letter string. Holes are not German letters."""
    if "?" in text:
        return None
    model = get_german_model()
    seq = [ord(char) - 65 for char in german_letters(text)]
    if len(seq) < 4:
        return None
    return model.mean_quadgram(seq)


def _day_machine(day: dict) -> HeadlessEnigma:
    return HeadlessEnigma.from_walzenlage(day["walzenlage"], day["rings"], day["stecker"])


def search_open_messages() -> dict:
    """Run published July keys. Do not invent a missing day's walzenlage."""
    if len(KLJBO_BODY) != 50 or KLJBO_BODY.count("-") != 4:
        raise ValueError("KLJBO body must be 50 slots with 4 holes")
    if len(JBIYH_BODY) != 55 or "-" in JBIYH_BODY:
        raise ValueError("JBIYH body must be 55 known letters")
    control_day = _day_machine(next(day for day in PUBLISHED_KEYS if day["date"] == "1941-07-05"))
    derop = control_day.open_spruch(DEROP_GROUND, DEROP_SECOND, DEROP_PREFIX)
    if derop["start"] != DEROP_START or derop["text"] != DEROP_CONTROL_TEXT:
        raise RuntimeError("5 July control did not reproduce the known DEROP prefix")
    control_score = _mean_score(derop["text"])
    rows = []
    for message in OPEN_MESSAGES:
        for day in PUBLISHED_KEYS:
            opened = _day_machine(day).open_spruch(message["ground"], message["second"], message["body"])
            score = _mean_score(opened["text"])
            rows.append({
                "message": message["name"],
                "key_date": day["date"],
                "start": opened["start"],
                "holes": opened["text"].count("?"),
                "mean_score": None if score is None else round(score, 4),
                "beats_control": score is not None and control_score is not None and score > control_score,
            })
    return {
        "claimed_plaintext": None,
        "solved": False,
        "control_start": derop["start"],
        "control_text": derop["text"],
        "control_mean_score": None if control_score is None else round(control_score, 4),
        "published_keys": len(PUBLISHED_KEYS),
        "rows": rows,
        "rows_beating_control": sum(1 for row in rows if row["beats_control"]),
        "scope": (
            "Published 1 July and 5-9 July keys only. "
            "3 July and 20 July keys are not on the key page and are not searched. "
            "A higher score is not a reading."
        ),
    }
