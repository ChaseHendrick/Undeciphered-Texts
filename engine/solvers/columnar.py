"""Columnar transposition solvers, including published Kryptos K3 recovery.

Kryptos passage 3 is a transposition cipher. Wikipedia's "Solution of passage 3"
prints the plaintext (including the intentional misspelling DESPARATLY) and
labels the method Transposition. The NSA FOIA technical paper (DOCID 4051151 /
4050988) diagnoses the same passage as a keyed columnar transposition on an
incompletely filled 4 x 86 matrix with specific key KRYPTOS and route bottom
to top.

This module does not read or claim Kryptos K4.
"""

from __future__ import annotations

from engine.alphabet import letters_only
from engine.language import get_model
from engine.result import SolveResult

# Sculpture K3 letters only (Wikipedia left-side transcript of passage 3,
# excluding the terminal ? that begins the unsolved K4 block).
KRYPTOS_K3_CIPHERTEXT = (
    "ENDYAHROHNLSRHEOCPTEOIBIDYSHNAIA"
    "CHTNREYULDSLLSLLNOHSNOSMRWXMNE"
    "TPRNGATIHNRARPESLNNELEBLPIIACAE"
    "WMTWNDITEENRAHCTENEUDRETNHAEOE"
    "TFOLSEDTIWENHAEIOYTEYQHEENCTAYCR"
    "EIFTBRSPAMHHEWENATAMATEGYEERLB"
    "TEEFOASFIOTUETUAEOTOARMAEERTNRTI"
    "BSEDDNIAAHTTMSTEWPIEROAGRIEWFEB"
    "AECTDDHILCEIHSITEGOEAOSDDRYDLORIT"
    "RKLMLEHAGTDHARDPNEOHMGFMFEUHE"
    "ECDMRIPFEIMEHNLSSTTRTVDOHW"
)

# Wikipedia "Solution of passage 3" and NSA FOIA plaintext, letters only.
# DESPARATLY is the published misspelling (not DESPERATELY).
KRYPTOS_K3_PLAINTEXT = (
    "SLOWLYDESPARATLYSLOWLYTHEREMAINSOFPASSAGEDEBRIS"
    "THATENCUMBEREDTHELOWERPARTOFTHEDOORWAYWASREMOVED"
    "WITHTREMBLINGHANDSIMADEATINYBREACHINTHEUPPERLEFT"
    "HANDCORNERANDTHENWIDENINGTHEHOLEALITTLEIINSERTED"
    "THECANDLEANDPEEREDINTHEHOTAIRESCAPINGFROMTHECHAMBER"
    "CAUSEDTHEFLAMETOFLICKERBUTPRESENTLYDETAILSOFTHEROOM"
    "WITHINEMERGEDFROMTHEMISTXCANYOUSEEANYTHINGQ"
)

KRYPTOS_K3_SPACED = (
    "SLOWLY DESPARATLY SLOWLY THE REMAINS OF PASSAGE DEBRIS THAT ENCUMBERED "
    "THE LOWER PART OF THE DOORWAY WAS REMOVED WITH TREMBLING HANDS I MADE A "
    "TINY BREACH IN THE UPPER LEFT HAND CORNER AND THEN WIDENING THE HOLE A "
    "LITTLE I INSERTED THE CANDLE AND PEERED IN THE HOT AIR ESCAPING FROM THE "
    "CHAMBER CAUSED THE FLAME TO FLICKER BUT PRESENTLY DETAILS OF THE ROOM "
    "WITHIN EMERGED FROM THE MIST X CAN YOU SEE ANYTHING Q"
)

# Double columnar widths published for K3 (complete rectangles on 336 letters).
K3_WIDTHS = (21, 28)


def numerical_key(keyword: str) -> list[int]:
    """1-based columnar ranks: alphabetical order, left-to-right for ties."""
    keyed = letters_only(keyword)
    if not keyed:
        raise ValueError("keyword must contain at least one letter")
    order = sorted(range(len(keyed)), key=lambda i: (keyed[i], i))
    ranks = [0] * len(keyed)
    for rank, index in enumerate(order, start=1):
        ranks[index] = rank
    return ranks


def columnar_decrypt_right_to_left(text: str, width: int) -> str:
    """Undo write-in-rows / read-down-columns-from-the-right on a full rectangle.

    The ciphertext must divide evenly by width. Columns were read from right
    to left; restore by writing ciphertext down those columns in the same
    order, then reading rows left to right.
    """
    letters = letters_only(text)
    if width < 2:
        raise ValueError("width must be at least 2")
    if len(letters) % width != 0:
        raise ValueError(
            f"length {len(letters)} is not divisible by columnar width {width}"
        )
    rows = len(letters) // width
    grid = [[""] * width for _ in range(rows)]
    pos = 0
    for col in range(width - 1, -1, -1):
        for row in range(rows):
            grid[row][col] = letters[pos]
            pos += 1
    return "".join("".join(row) for row in grid)


def columnar_encrypt_right_to_left(text: str, width: int) -> str:
    """Write letters in rows of width, read down columns from right to left."""
    letters = letters_only(text)
    if width < 2:
        raise ValueError("width must be at least 2")
    if len(letters) % width != 0:
        raise ValueError(
            f"length {len(letters)} is not divisible by columnar width {width}"
        )
    rows = [letters[i : i + width] for i in range(0, len(letters), width)]
    out: list[str] = []
    for col in range(width - 1, -1, -1):
        for row in rows:
            out.append(row[col])
    return "".join(out)


def double_columnar_decrypt(text: str, width1: int, width2: int) -> str:
    """Apply two successive right-to-left columnar decryptions."""
    return columnar_decrypt_right_to_left(
        columnar_decrypt_right_to_left(text, width1), width2
    )


def double_columnar_encrypt(text: str, width1: int, width2: int) -> str:
    """Inverse of double_columnar_decrypt (encrypt with width2, then width1)."""
    return columnar_encrypt_right_to_left(
        columnar_encrypt_right_to_left(text, width2), width1
    )


def _rotate90_ccw(rows: list[list[str]]) -> list[list[str]]:
    height = len(rows)
    width = len(rows[0])
    return [[rows[r][width - 1 - c] for r in range(height)] for c in range(width)]


def _rotate90_cw(rows: list[list[str]]) -> list[list[str]]:
    height = len(rows)
    width = len(rows[0])
    return [[rows[height - 1 - r][c] for r in range(height)] for c in range(width)]


def kryptos_k3_sanborn_decrypt(ciphertext: str) -> str:
    """Recover K3 via Sanborn's published two-rotation matrix method.

    Coding charts (NYT, 2010): write an 8 x 42 plaintext matrix, rotate 90
    degrees clockwise, reshape to 24 x 14, rotate 90 degrees clockwise again,
    and read by rows. Decryption reverses those steps. The letter stream matches
    Wikipedia / NSA K3 plaintext exactly.
    """
    letters = letters_only(ciphertext)
    if len(letters) != 336:
        raise ValueError(f"K3 ciphertext must be 336 letters, got {len(letters)}")
    grid = [[letters[r * 24 + c] for c in range(24)] for r in range(14)]
    grid = _rotate90_ccw(grid)
    flat = "".join("".join(row) for row in grid)
    grid = [[flat[r * 8 + c] for c in range(8)] for r in range(42)]
    grid = _rotate90_ccw(grid)
    return "".join("".join(row) for row in grid)


def kryptos_k3_sanborn_encrypt(plaintext: str) -> str:
    """Forward Sanborn K3 encoding (inverse of kryptos_k3_sanborn_decrypt)."""
    letters = letters_only(plaintext)
    if len(letters) != 336:
        raise ValueError(f"K3 plaintext must be 336 letters, got {len(letters)}")
    grid = [[letters[r * 42 + c] for c in range(42)] for r in range(8)]
    grid = _rotate90_cw(grid)
    flat = "".join("".join(row) for row in grid)
    grid = [[flat[r * 14 + c] for c in range(14)] for r in range(24)]
    grid = _rotate90_cw(grid)
    return "".join("".join(row) for row in grid)


def solve_columnar(
    text: str,
    width1: int = K3_WIDTHS[0],
    width2: int = K3_WIDTHS[1],
) -> SolveResult:
    """Decrypt with a double right-to-left columnar transposition.

    Default widths (21, 28) are the published complete-rectangle pair that
    recovers Kryptos K3 from its 336-letter ciphertext. Supplying other widths
    runs the same general transform only.
    """
    plaintext = double_columnar_decrypt(text, width1, width2)
    az = [ord(ch) - 65 for ch in plaintext]
    return SolveResult(
        method="columnar-transposition",
        plaintext=plaintext,
        key=f"{width1}x{width2}",
        score=get_model().score(az) if az else 0.0,
        details={
            "widths": (width1, width2),
            "letters": len(az),
            "route": "columns right-to-left, then rows left-to-right",
            "scope": "double columnar transposition; not a K4 solution",
        },
    )


def solve_kryptos_k3(ciphertext: str | None = None) -> SolveResult:
    """Recover the published Kryptos K3 plaintext from its ciphertext.

    Uses the double columnar (21 then 28) reading that restores the Wikipedia
    / NSA letter stream. Cross-checks the Sanborn two-rotation form so both
    published transposition presentations agree. Does not touch K4.
    """
    source = KRYPTOS_K3_CIPHERTEXT if ciphertext is None else ciphertext
    letters = letters_only(source)
    if len(letters) != 336:
        raise ValueError(f"K3 ciphertext must be 336 letters, got {len(letters)}")
    result = solve_columnar(letters, K3_WIDTHS[0], K3_WIDTHS[1])
    sanborn = kryptos_k3_sanborn_decrypt(letters)
    if sanborn != result.plaintext:
        raise ValueError(
            "double columnar and Sanborn rotation decrypts disagree on K3"
        )
    result.details["sanborn_rotations"] = "8x42 then 24x14, each rotated 90 CW on encrypt"
    result.details["nsa"] = (
        "FOIA DOCID 4051151/4050988: keyed columnar, incomplete 4x86, "
        "key KRYPTOS, route bottom-to-top"
    )
    result.details["scope"] = "Kryptos K3 published plaintext only; not a K4 solution"
    return result
