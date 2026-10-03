"""Route cipher known-key solver: grid fill, then a named read-off route.

The plaintext is written into a rectangle. The key gives the width, whether
letters fill by rows or by columns, and the route used to read the ciphertext
off that rectangle. Decryption writes the ciphertext back along the same
route and reads the grid in the fill order.

The worked example used here is Crypto-IT, "Route Cipher" (page dated
2020-03-09, fetched 2026-10-02):

  http://www.crypto-it.net/eng/simple/route-cipher.html

  "Brighton and Hove", width 3, row by row, clockwise inward spiral from
  the top right -> ITAHEVONOGBRHND.

This module is a **known classical-cipher** solver. It recovers plaintext
only when the width, fill, and route are supplied. It is **not** an
unknown-script reading and **not** a claim about army message Nr. 86.
"""

from __future__ import annotations

from engine.alphabet import letters_only, reinject
from engine.result import SolveResult

# Crypto-IT worked example (page dated 2020-03-09, fetched 2026-10-02).
# http://www.crypto-it.net/eng/simple/route-cipher.html
CRYPTO_IT_URL = "http://www.crypto-it.net/eng/simple/route-cipher.html"
CRYPTO_IT_KEY = "width=3;fill=rows;route=spiral-cw-top-right"
CRYPTO_IT_PLAIN = "BRIGHTONANDHOVE"
CRYPTO_IT_CIPHER = "ITAHEVONOGBRHND"

# Wikipedia, Transposition cipher, section "Route cipher" (fetched 2026-10-02).
# The 3 by 9 grid is the sentence plus the nulls J and X shown on the page.
WIKIPEDIA_URL = "https://en.wikipedia.org/wiki/Transposition_cipher#Route_cipher"
WIKIPEDIA_KEY = "width=9;fill=cols;route=spiral-cw-top-right"
WIKIPEDIA_PLAIN = "WEAREDISCOVEREDFLEEATONCEJX"
WIKIPEDIA_CIPHER = "EJXCTEDECDAEWRIORFEONALEVSE"

_SCOPE = (
    "Known classical route cipher solver only; "
    "not an unknown-script reading and not a claim about army message Nr. 86."
)

_ROUTE = "spiral-cw-top-right"
_FILLS = ("rows", "cols")


def route_key(key: str) -> dict[str, object]:
    """Parse ``width=3;fill=rows;route=spiral-cw-top-right``.

    ``height`` may be given instead of ``width``, or both. ``fill`` is
    ``rows`` (left to right, top to bottom) or ``cols`` (top to bottom,
    left to right). The only route name is ``spiral-cw-top-right``:
    clockwise, inward, starting at the top right, first step down.
    """
    text = str(key).strip()
    if not text:
        raise ValueError("route key is empty")
    fields: dict[str, str] = {}
    for part in text.split(";"):
        piece = part.strip()
        if not piece:
            continue
        if "=" not in piece:
            raise ValueError(
                "route key fields must look like width=3;fill=rows;route=spiral-cw-top-right"
            )
        name, value = piece.split("=", 1)
        fields[name.strip().lower()] = value.strip().lower()
    unknown = set(fields) - {"width", "height", "fill", "route"}
    if unknown:
        raise ValueError("unknown route key field: " + ",".join(sorted(unknown)))
    if "width" not in fields and "height" not in fields:
        raise ValueError("route key needs width or height")
    fill = fields.get("fill", "")
    if fill not in _FILLS:
        raise ValueError("route fill must be rows or cols")
    route = fields.get("route", "")
    if route != _ROUTE:
        raise ValueError("route must be spiral-cw-top-right")
    width = _positive(fields["width"]) if "width" in fields else None
    height = _positive(fields["height"]) if "height" in fields else None
    return {"width": width, "height": height, "fill": fill, "route": route}


def _positive(value: str) -> int:
    if not value.isdigit() or int(value) < 1:
        raise ValueError("route width and height must be positive integers")
    return int(value)


def _dimensions(count: int, spec: dict[str, object]) -> tuple[int, int]:
    """Return (rows, cols) for a letter count that fills the rectangle."""
    width = spec["width"]
    height = spec["height"]
    if width is None:
        assert isinstance(height, int)
        if count % height != 0:
            raise ValueError("letter count is not divisible by the route height")
        width = count // height
    if height is None:
        assert isinstance(width, int)
        if count % width != 0:
            raise ValueError("letter count is not divisible by the route width")
        height = count // width
    assert isinstance(width, int) and isinstance(height, int)
    if width * height != count:
        raise ValueError("route width times height must equal the letter count")
    if width < 1 or height < 1:
        raise ValueError("route grid is empty")
    return height, width


def _spiral_cw_top_right(rows: int, cols: int) -> list[tuple[int, int]]:
    """Clockwise inward spiral from the top-right cell, first step down."""
    dirs = ((1, 0), (0, -1), (-1, 0), (0, 1))
    seen = [[False] * cols for _ in range(rows)]
    row, col = 0, cols - 1
    turn = 0
    path: list[tuple[int, int]] = []
    for _ in range(rows * cols):
        path.append((row, col))
        seen[row][col] = True
        dr, dc = dirs[turn]
        nr, nc = row + dr, col + dc
        if not (0 <= nr < rows and 0 <= nc < cols) or seen[nr][nc]:
            turn = (turn + 1) % 4
            dr, dc = dirs[turn]
            nr, nc = row + dr, col + dc
        row, col = nr, nc
    return path


def _fill_index(index: int, rows: int, cols: int, fill: str) -> tuple[int, int]:
    if fill == "rows":
        return index // cols, index % cols
    return index % rows, index // rows


def route_encrypt(text: str, key: str) -> str:
    """Encrypt with a known width, fill, and route. Non-letters are dropped.

    The letter count must fill the rectangle. This solver does not invent nulls.
    """
    spec = route_key(key)
    plain = letters_only(text)
    if not plain:
        raise ValueError("text has no letters")
    rows, cols = _dimensions(len(plain), spec)
    grid = [[""] * cols for _ in range(rows)]
    fill = str(spec["fill"])
    for index, letter in enumerate(plain):
        r, c = _fill_index(index, rows, cols, fill)
        grid[r][c] = letter
    return "".join(grid[r][c] for r, c in _spiral_cw_top_right(rows, cols))


def route_decrypt(text: str, key: str) -> str:
    """Decrypt with a known width, fill, and route.

    Ciphertext letters are written along the spiral. Plaintext is read back
    in the fill order.
    """
    spec = route_key(key)
    cipher = letters_only(text)
    if not cipher:
        raise ValueError("text has no letters")
    rows, cols = _dimensions(len(cipher), spec)
    grid = [[""] * cols for _ in range(rows)]
    for (r, c), letter in zip(_spiral_cw_top_right(rows, cols), cipher):
        grid[r][c] = letter
    fill = str(spec["fill"])
    plain: list[str] = []
    for index in range(rows * cols):
        r, c = _fill_index(index, rows, cols, fill)
        if not grid[r][c]:
            raise ValueError("route left a grid cell empty")
        plain.append(grid[r][c])
    return "".join(plain)


def solve_route(text: str, *, key: str) -> SolveResult:
    """Recover route-cipher plaintext when the grid and route are known.

    Known-cipher decrypt only. Not an unknown-script reading and not a
    claim about army message Nr. 86.
    """
    spec = route_key(key)
    plain_letters = route_decrypt(text, key)
    rows, cols = _dimensions(len(letters_only(text)), spec)
    rendered = reinject(text, plain_letters) if any(not ch.isalpha() for ch in text) else plain_letters
    canonical = (
        f"width={cols};fill={spec['fill']};route={spec['route']}"
    )
    return SolveResult(
        method="route",
        plaintext=rendered,
        key=canonical,
        score=float(len(plain_letters)),
        details={
            "key": canonical,
            "width": cols,
            "height": rows,
            "fill": spec["fill"],
            "route": spec["route"],
            "letters": len(letters_only(text)),
            "mode": "known_route",
            "scope": _SCOPE,
            "source_url": CRYPTO_IT_URL,
        },
    )


__all__ = [
    "CRYPTO_IT_CIPHER",
    "CRYPTO_IT_KEY",
    "CRYPTO_IT_PLAIN",
    "CRYPTO_IT_URL",
    "WIKIPEDIA_CIPHER",
    "WIKIPEDIA_KEY",
    "WIKIPEDIA_PLAIN",
    "WIKIPEDIA_URL",
    "route_decrypt",
    "route_encrypt",
    "route_key",
    "solve_route",
]
