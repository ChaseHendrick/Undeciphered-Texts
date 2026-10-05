"""Published readings of the 1939 challenge, checked against the cells. Not a reading.

Each entry quotes a reading someone else published, as they published it,
with where and when. The quotes are their claims, not this repository's.
The checks use arithmetic the cells force on any reading:

* If every cell is a letter, a one-to-one key and any transposition keep the
  cells' sorted counts: 20, 17, 17, 17, 17, 16, 15, 14, 12, 12, 11, 11, 9,
  3, 2, 1, 1, 1. A full-length reading must have exactly those counts.
* A reading that drops some cells as dummies can still use at most 18
  distinct letters, and its k-th most common letter can be no more common
  than the cells' k-th most common symbol.
* The book's own dummy rule, a dummy every third, fourth or fifth letter,
  keeps between 131 and 157 of the 196 cells.

A reading that passes these checks is not thereby right. One that fails
them cannot come from the cells by the method its author describes.
"""

from __future__ import annotations

from collections import Counter

from engine.dagapeyeff_cache import frozen
from engine.dagapeyeff_swarm import challenge_pairs

CLAIMS = (
    {
        "id": "triggernick",
        "source": "https://triggernick.com/dagapeyeff/ (unreachable on 5 October 2026; text from a search summary)",
        "date": "undated",
        "method": "cells read as letters, dummies removed, homophonic solver (ZKDecrypto)",
        "text": "ON ITS RED HAIR IS NO HOOT SINGER NOR HAT AS SEEN ALAS ON A SHINE A PRATT DIED",
    },
    {
        "id": "tony-2014",
        "source": "https://ciphermysteries.com/2013/12/23/dagapeyeff-cipher, comment by Tony",
        "date": "2014-04-25",
        "method": "not stated",
        "text": (
            "TOWARDS THE END OF THE FOURTEENTH CENTURY EUROPE WAS REORGANIZING ITSELF THE NATIONS STARTED "
            "TO ASSUME SOME OF THE FORMS WE KNOW TODAY THERE WERE WARS AND EXCURSIONS AND A GREAT DEAL OF "
            "DIPLOMATIC ACTIVITY AS CIVILIZATION AND LEARNING"
        ),
    },
    {
        "id": "darensbourg-2019",
        "source": "https://ciphermysteries.com/2013/12/23/dagapeyeff-cipher, comment by Catherine Mary Darensbourg",
        "date": "2019-11-01",
        "method": "column digits paired with each other as a second Polybius message; partial",
        "text": "MAIL LLT YR I KEY GO DUTCH C",
    },
    {
        "id": "officialchaos-2026",
        "source": "https://ciphermysteries.com/2017/03/05/new-clue-dagapeyeff-challenge-cipher, comment by OfficialChaos",
        "date": "2026-02-27",
        "method": "single digits as a straddling checkerboard 8=E 1=T 5=R 7=S 2=I 3=C 4=H 6=P 9=U, 14 by 28 columnar, one digit deleted",
        "text": (
            "SPEECH IN DEPTH REQUIRES A SHEET IT IS HARD TO DETECT BECAUSE CIPHERS USE SCHEMES THAT SHIFT "
            "THE HEIGHT OF SECURITY IS HARD TO TEST EXCEPT BY SHIFTING THE SHEET REPORT ENDS"
        ),
        "key_letters": "ETRSICHPU",
    },
    {
        "id": "vento-2026",
        "source": "https://ciphermysteries.com/2013/12/23/dagapeyeff-cipher, comment by Vento",
        "date": "2026-07-28",
        "method": "each pair of five-digit groups read as two coordinates",
        "text": "FATHER CHRISTMAS FILL OUR STOCKINGS WE HAVE BEEN GOOD AND WE WOULD LIKE TOYS SWEETS CHOCOLATE",
        "same_coordinates": {"(1,4) (2,3)": ["GO", "AN", "SW", "TS"]},
    },
    {
        "id": "uygun-2026",
        "source": "https://doi.org/10.5281/zenodo.18639390",
        "date": "2026-02-14",
        "method": "two 14 by 7 blocks split at 04, shared 14-column key, ASSESSED and ATTACK imposed as cribs",
        "text": "ASSESSED TSQ ESR KTDTDS JJJ AREAS RSDTES JQ TRAT SURDRE TAG RTT SE EKUASCUT ATTACK",
        "cribs_imposed": ["ASSESSED", "ATTACK"],
        "note": "excerpt of the printed raw text; the paper's ellipses and bracketed corrections are left out",
    },
    {
        "id": "caillahua-2026",
        "source": "https://doi.org/10.5281/zenodo.20652502",
        "date": "2026-06-12",
        "method": "keyword square MANCHESTR, inverse rail fence of 5 rails, every fourth symbol a null; partial",
        "text": "NOW OUT TOO YOU",
        "stated_length": "196 decimal digits grouped into 98 digrams",
    },
    {
        "id": "leggett-2025",
        "source": "https://doi.org/10.5281/zenodo.17993736",
        "date": "2025-12-19",
        "method": "digits read as two 14 by 14 matrices of anti-aircraft telemetry, with a shift chosen so impossible values vanish",
        "text": "",
    },
)


def _profile(text: str) -> list[int]:
    letters = "".join(ch for ch in text.upper() if "A" <= ch <= "Z").replace("J", "I")
    return sorted(Counter(letters).values(), reverse=True)


@frozen("dagapeyeff-claims")
def claims_report() -> dict:
    cells = challenge_pairs()
    cell_profile = sorted(Counter(cells).values(), reverse=True)
    rows = []
    for claim in CLAIMS:
        profile = _profile(claim["text"])
        letters = sum(profile)
        row = {
            "id": claim["id"],
            "date": claim["date"],
            "source": claim["source"],
            "method": claim["method"],
            "quoted": claim["text"],
            "letters": letters,
            "distinct_letters": len(profile),
        }
        if letters:
            row["exact_full_profile"] = letters == len(cells) and profile == cell_profile
            row["fits_inside_cells"] = len(profile) <= len(cell_profile) and all(
                a <= b for a, b in zip(profile, cell_profile)
            )
            row["inside_book_dummy_rule"] = 131 <= letters <= 157
        if "key_letters" in claim:
            letters_used = {ch for ch in claim["text"] if "A" <= ch <= "Z"}
            row["letters_outside_own_key"] = sorted(letters_used - set(claim["key_letters"]))
        if "same_coordinates" in claim:
            row["one_coordinate_many_letters"] = claim["same_coordinates"]
        if "cribs_imposed" in claim:
            row["cribs_imposed"] = claim["cribs_imposed"]
        if "note" in claim:
            row["note"] = claim["note"]
        if "stated_length" in claim:
            row["stated_length"] = claim["stated_length"]
            row["printed_length"] = "392 digits in 196 pairs, then 000"
        rows.append(row)
    return {
        "solved": False,
        "claimed_plaintext": None,
        "cells": len(cells),
        "cell_profile": cell_profile,
        "claims": rows,
        "full_length_claims_with_cell_profile": sum(1 for row in rows if row.get("exact_full_profile")),
        "scope": (
            "Other people's published readings, quoted as they gave them, checked against counts the cells "
            "force on any reading. Passing a check is not a reading. No reading is claimed here."
        ),
    }
