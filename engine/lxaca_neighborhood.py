"""Supplied-key neighborhood for Enigma message LXACA, 5 July 1941.

The publisher says this 20-letter message does not break on the 5 July key
and is probably 4 July traffic. The 4 July key is not on the key page.
This module checks the published keys for 1 July and 5 through 9 July, then
every one-letter edit of the printed 5 July indicator. A known break on the
same 5 July key is the control. Nothing here is a new historical reading.
"""

from __future__ import annotations

from engine.german import get_german_model, german_letters
from engine.solvers.enigma import enigma_decrypt

# Frode Weierud, Enigma keys for July 1941, page updated 28 September 2026.
# https://cryptocellar.org/bgac/e-keys-july-1941.html
# W/O is left to right. 1 July rings are printed "(AAV)".
SOURCE_KEYS = "https://cryptocellar.org/bgac/e-keys-july-1941.html"
SOURCE_MESSAGE = "https://cryptocellar.org/bgac/g-army-july-1941.html"
_ROMAN = {"1": "I", "2": "II", "3": "III", "4": "IV", "5": "V"}

PUBLISHED_KEYS = (
    {"date": "1941-07-01", "walzenlage": "423", "rings": "AAV",
     "stecker": "CT EM FI GJ HK NQ OR SW UY VX"},
    {"date": "1941-07-05", "walzenlage": "354", "rings": "WHJ",
     "stecker": "BI CW EQ FX HZ JN KY MT OV PR"},
    {"date": "1941-07-06", "walzenlage": "513", "rings": "IRD",
     "stecker": "AN BM DH EI KQ LS OT PV RU YZ"},
    {"date": "1941-07-07", "walzenlage": "245", "rings": "BUL",
     "stecker": "AV BS CG DL FU HZ IN KM OW RX"},
    {"date": "1941-07-08", "walzenlage": "432", "rings": "PKF",
     "stecker": "CY EL FH GS IJ KQ MW PV RZ TU"},
    {"date": "1941-07-09", "walzenlage": "315", "rings": "NAV",
     "stecker": "AC BN FM GI JL KO PU QX RZ TV"},
)

# Message page, Nr. 100. The first group is the Kenngruppe, not ciphertext.
LXACA_BODY = "ZIXAGNQRKOHBPNKXRLFU"
LXACA_GROUND = "OGD"
LXACA_SECOND = "PKN"

# Same 5 July key, message Nr. 101. The key table prints start WER.
DEROP_GROUND = "AIK"
DEROP_SECOND = "SUD"
DEROP_START = "WER"
DEROP_PREFIX = "AQDEGMQTRRJYMHBITNRQ"
DEROP_CONTROL_TEXT = "BETRIEBSSPRUQXKUPPLU"

# 9 July, corrected indicator from master-list footnote 44. Printed group is YKI.
WEUWY_GROUND = "NUG"
WEUWY_CORRECTED = "YKS"
WEUWY_PRINTED = "YKI"


def _machine(day: dict) -> dict:
    rotors = tuple(_ROMAN[ch] for ch in day["walzenlage"])
    return {
        "rotors": rotors,
        "rings": day["rings"],
        "plugboard": tuple(day["stecker"].split()),
        "reflector": "B",
    }


def _by_date(date: str) -> dict:
    for day in PUBLISHED_KEYS:
        if day["date"] == date:
            return _machine(day)
    raise KeyError(date)


def indicator_start(date: str, ground: str, second: str) -> str:
    """Decipher the second indicator group at the Grundstellung."""
    machine = _by_date(date)
    return enigma_decrypt(second, positions=ground, **machine)


def decrypt_body(date: str, start: str, text: str) -> str:
    machine = _by_date(date)
    return enigma_decrypt(text, positions=start, **machine)


def _score(text: str) -> float:
    model = get_german_model()
    seq = [ord(ch) - 65 for ch in german_letters(text)]
    return model.quadgram_score(seq)


def _indicator_edits() -> tuple[tuple[str, str, str], ...]:
    """Printed indicator, the swapped groups, and each one-letter edit."""
    rows = [("as printed", LXACA_GROUND, LXACA_SECOND),
            ("groups swapped", LXACA_SECOND, LXACA_GROUND)]
    alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for index, letter in enumerate(LXACA_GROUND):
        for replacement in alphabet:
            if replacement == letter:
                continue
            ground = LXACA_GROUND[:index] + replacement + LXACA_GROUND[index + 1:]
            rows.append((f"ground {ground}", ground, LXACA_SECOND))
    for index, letter in enumerate(LXACA_SECOND):
        for replacement in alphabet:
            if replacement == letter:
                continue
            second = LXACA_SECOND[:index] + replacement + LXACA_SECOND[index + 1:]
            rows.append((f"second {second}", LXACA_GROUND, second))
    return tuple(rows)


def search_lxaca_neighborhood() -> dict:
    """Run the controls and the published-key neighborhood. No reading is claimed."""
    if len(LXACA_BODY) != 20 or len(DEROP_PREFIX) != 20:
        raise ValueError("LXACA and the DEROP control prefix must both be 20 letters")
    derop_start = indicator_start("1941-07-05", DEROP_GROUND, DEROP_SECOND)
    derop_text = decrypt_body("1941-07-05", DEROP_START, DEROP_PREFIX)
    control_score = _score(derop_text)
    days = []
    for day in PUBLISHED_KEYS:
        start = indicator_start(day["date"], LXACA_GROUND, LXACA_SECOND)
        output = decrypt_body(day["date"], start, LXACA_BODY)
        days.append({
            "date": day["date"],
            "walzenlage": day["walzenlage"],
            "start": start,
            "machine_output": output,
            "german_quadgram_score": _score(output),
            "status": "machine output, not a reading",
        })
    edits = []
    for label, ground, second in _indicator_edits():
        start = indicator_start("1941-07-05", ground, second)
        output = decrypt_body("1941-07-05", start, LXACA_BODY)
        edits.append({
            "edit": label,
            "ground": ground,
            "second": second,
            "start": start,
            "machine_output": output,
            "german_quadgram_score": _score(output),
            "beats_control": _score(output) >= control_score,
        })
    edits.sort(key=lambda row: row["german_quadgram_score"], reverse=True)
    return {
        "claimed_plaintext": None,
        "solved": False,
        "source_keys": SOURCE_KEYS,
        "source_message": SOURCE_MESSAGE,
        "body_letters": len(LXACA_BODY),
        "missing_key": "4 July 1941 is not on the July key page",
        "controls": {
            "derop_start": derop_start,
            "derop_start_matches_table": derop_start == DEROP_START,
            "derop_prefix": derop_text,
            "derop_prefix_matches_control": derop_text == DEROP_CONTROL_TEXT,
            "derop_score": control_score,
            "weuwy_corrected_start": indicator_start("1941-07-09", WEUWY_GROUND, WEUWY_CORRECTED),
            "weuwy_printed_start": indicator_start("1941-07-09", WEUWY_GROUND, WEUWY_PRINTED),
        },
        "published_days": days,
        "july5_indicator_edits": len(edits),
        "edits_beating_control": sum(1 for row in edits if row["beats_control"]),
        "best_edit": edits[0],
        "scope": "Published daily keys and one-letter indicator edits only. A 20-letter score is not a reading. The 4 July key was not searched because it is not published.",
    }
