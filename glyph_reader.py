"""Segment ink marks and match repeats to a small synthetic sign inventory.

The marks are drawn by this module. Matching a repeat to an inventory label
is template comparison of those marks. It is not a decipherment.

This module does not decipher Linear A, the Indus script, or the signs painted
at Teotihuacan. Those scripts are not in the inventory, and a low template
distance is not a reading of them.
"""

from __future__ import annotations

import argparse
import sys
from collections.abc import Callable, Sequence
from dataclasses import dataclass

CELL = 48
GAP = 20
MARGIN = 16
INK_THRESHOLD = 128
MIN_INK = 12
GRID = 16

DISCLAIMER = (
    "Does not decipher Linear A, the Indus script, or Teotihuacan signs. "
    "Segments ink on a raster and matches repeats only to the synthetic "
    "inventory defined in this module."
)

Drawer = Callable[["ImageDraw.ImageDraw", int, int, int], None]


def _require_pillow():
    try:
        from PIL import Image, ImageDraw
    except ImportError as exc:
        raise RuntimeError(
            "Pillow is not installed. The glyph sheet is drawn with Pillow; "
            "this module does not invent a reading without a raster."
        ) from exc
    return Image, ImageDraw


def _hbar(draw, x: int, y: int, size: int) -> None:
    inset = 8
    mid = y + size // 2
    draw.rectangle([x + inset, mid - 4, x + size - inset - 1, mid + 3], fill=0)


def _stem(draw, x: int, y: int, size: int) -> None:
    inset = 8
    mid = x + size // 2
    draw.rectangle([mid - 4, y + inset, mid + 3, y + size - inset - 1], fill=0)


def _corner(draw, x: int, y: int, size: int) -> None:
    inset = 8
    draw.rectangle([x + inset, y + inset, x + inset + 7, y + size - inset - 1], fill=0)
    draw.rectangle([x + inset, y + size - inset - 8, x + size - inset - 1, y + size - inset - 1], fill=0)


def _cross(draw, x: int, y: int, size: int) -> None:
    _hbar(draw, x, y, size)
    _stem(draw, x, y, size)


def _ring(draw, x: int, y: int, size: int) -> None:
    inset = 8
    draw.ellipse(
        [x + inset, y + inset, x + size - inset - 1, y + size - inset - 1],
        outline=0,
        width=6,
    )


def _peak(draw, x: int, y: int, size: int) -> None:
    inset = 8
    top = y + inset
    bot = y + size - inset - 1
    left = x + inset
    right = x + size - inset - 1
    mid = x + size // 2
    draw.polygon([(left, top), (left + 8, top), (mid + 2, bot), (mid - 6, bot)], fill=0)
    draw.polygon([(right - 8, top), (right, top), (mid + 6, bot), (mid - 2, bot)], fill=0)


# Stable order. Labels are inventory ids, not readings of any ancient sign list.
SIGN_DRAWERS: dict[str, Drawer] = {
    "bar": _hbar,
    "stem": _stem,
    "corner": _corner,
    "cross": _cross,
    "ring": _ring,
    "peak": _peak,
}


@dataclass(frozen=True)
class Glyph:
    """One connected ink component, in reading order."""

    bbox: tuple[int, int, int, int]
    ink_pixels: int
    label: str
    distance: float


@dataclass(frozen=True)
class GlyphSheetReport:
    width: int
    height: int
    glyphs: tuple[Glyph, ...]
    disclaimer: str


def inventory_labels() -> tuple[str, ...]:
    return tuple(SIGN_DRAWERS)


def render_synthetic_sheet(labels: Sequence[str], columns: int = 5):
    """Draw `labels` left to right, wrapping every `columns` cells.

    Repeats are the same drawer called again. Cells are separated so ink
    does not bridge two signs.
    """
    if columns < 1:
        raise ValueError("columns must be >= 1")
    if not labels:
        raise ValueError("labels must be non-empty")
    unknown = [name for name in labels if name not in SIGN_DRAWERS]
    if unknown:
        raise KeyError(f"not in the synthetic inventory: {unknown}")

    Image, ImageDraw = _require_pillow()
    rows = (len(labels) + columns - 1) // columns
    width = MARGIN * 2 + columns * CELL + (columns - 1) * GAP
    height = MARGIN * 2 + rows * CELL + (rows - 1) * GAP
    image = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(image)
    for index, name in enumerate(labels):
        col = index % columns
        row = index // columns
        origin_x = MARGIN + col * (CELL + GAP)
        origin_y = MARGIN + row * (CELL + GAP)
        SIGN_DRAWERS[name](draw, origin_x, origin_y, CELL)
    return image


def _luminance(image) -> tuple[int, int, list[int]]:
    """Accept a Pillow image. Dark pixels are ink."""
    if not hasattr(image, "convert") or not hasattr(image, "size"):
        raise TypeError("expected a Pillow image")
    gray = image.convert("L")
    width, height = gray.size
    return width, height, list(gray.getdata())


def _connected_components(width: int, height: int, pixels: list[int]) -> list[list[tuple[int, int]]]:
    ink = [value < INK_THRESHOLD for value in pixels]
    seen = bytearray(width * height)
    components: list[list[tuple[int, int]]] = []
    for start in range(width * height):
        if not ink[start] or seen[start]:
            continue
        seen[start] = 1
        stack = [start]
        component: list[tuple[int, int]] = []
        while stack:
            cursor = stack.pop()
            x = cursor % width
            y = cursor // width
            component.append((x, y))
            for dy in (-1, 0, 1):
                ny = y + dy
                if ny < 0 or ny >= height:
                    continue
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    nx = x + dx
                    if nx < 0 or nx >= width:
                        continue
                    neighbor = ny * width + nx
                    if ink[neighbor] and not seen[neighbor]:
                        seen[neighbor] = 1
                        stack.append(neighbor)
        if len(component) >= MIN_INK:
            components.append(component)
    return components


def _descriptor(component: list[tuple[int, int]], bbox: tuple[int, int, int, int]) -> tuple[int, ...]:
    x0, y0, bw, bh = bbox
    grid = [0] * (GRID * GRID)
    for x, y in component:
        gx = min(GRID - 1, (x - x0) * GRID // bw)
        gy = min(GRID - 1, (y - y0) * GRID // bh)
        grid[gy * GRID + gx] = 1
    return tuple(grid)


def _bbox(component: list[tuple[int, int]]) -> tuple[int, int, int, int]:
    xs = [x for x, _ in component]
    ys = [y for _, y in component]
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    return (min_x, min_y, max_x - min_x + 1, max_y - min_y + 1)


def _reading_order(items: list[tuple[tuple[int, int, int, int], list[tuple[int, int]]]]) -> list:
    """Group into rows by vertical center, then sort each row left to right."""
    decorated = []
    for bbox, component in items:
        x, y, width, height = bbox
        decorated.append((y + height / 2, x, bbox, component))
    decorated.sort(key=lambda item: item[0])
    rows: list[list] = []
    for item in decorated:
        if not rows or item[0] - rows[-1][0][0] > CELL * 0.6:
            rows.append([item])
        else:
            rows[-1].append(item)
    ordered = []
    for row in rows:
        row.sort(key=lambda item: item[1])
        ordered.extend(row)
    return ordered


def _hamming(left: Sequence[int], right: Sequence[int]) -> float:
    if len(left) != len(right) or not left:
        raise ValueError("descriptors must be the same non-empty length")
    mismatches = sum(a != b for a, b in zip(left, right))
    return mismatches / len(left)


def template_descriptors() -> dict[str, tuple[int, ...]]:
    """One isolated drawing of each inventory sign, same cell size as the sheet."""
    templates: dict[str, tuple[int, ...]] = {}
    for name in SIGN_DRAWERS:
        image = render_synthetic_sheet([name], columns=1)
        width, height, pixels = _luminance(image)
        components = _connected_components(width, height, pixels)
        if len(components) != 1:
            raise RuntimeError(
                f"inventory sign {name!r} produced {len(components)} components; "
                "each sign must be one connected mark"
            )
        bbox = _bbox(components[0])
        templates[name] = _descriptor(components[0], bbox)
    return templates


def analyze_glyphs(image, templates: dict[str, tuple[int, ...]] | None = None) -> GlyphSheetReport:
    """Segment ink, describe each mark, and label it from the inventory.

    `label` is the nearest synthetic sign. `distance` is the fraction of
    descriptor cells that disagree. A label is not a translation.
    """
    if templates is None:
        templates = template_descriptors()
    if not templates:
        raise ValueError("inventory is empty")
    width, height, pixels = _luminance(image)
    raw = []
    for component in _connected_components(width, height, pixels):
        raw.append((_bbox(component), component))
    glyphs: list[Glyph] = []
    for _cy, _x, bbox, component in _reading_order(raw):
        descriptor = _descriptor(component, bbox)
        ranked = sorted(
            ((name, _hamming(descriptor, template)) for name, template in templates.items()),
            key=lambda item: (item[1], item[0]),
        )
        label, distance = ranked[0]
        if len(ranked) > 1 and ranked[1][1] == distance and ranked[1][0] != label:
            raise RuntimeError(f"ambiguous inventory match at bbox {bbox}")
        glyphs.append(
            Glyph(
                bbox=bbox,
                ink_pixels=len(component),
                label=label,
                distance=distance,
            )
        )
    return GlyphSheetReport(
        width=width,
        height=height,
        glyphs=tuple(glyphs),
        disclaimer=DISCLAIMER,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m glyph_reader",
        description=(
            "Draw a synthetic glyph sheet and print bbox, ink, and inventory "
            "labels. Does not decipher Linear A, Indus, or Teotihuacan."
        ),
    )
    parser.add_argument(
        "--labels",
        default="bar,peak,bar,cross,ring,corner,peak,stem,ring,stem",
        help="comma-separated inventory ids to plant on the sheet",
    )
    parser.add_argument("--columns", type=int, default=5)
    parser.add_argument("--save", help="optional PNG path for the generated sheet")
    args = parser.parse_args(argv)
    labels = [part.strip() for part in args.labels.split(",") if part.strip()]
    image = render_synthetic_sheet(labels, columns=args.columns)
    if args.save:
        image.save(args.save, format="PNG")
        print(f"wrote {args.save}", file=sys.stderr)
    report = analyze_glyphs(image)
    print(report.disclaimer)
    for glyph in report.glyphs:
        x, y, w, h = glyph.bbox
        print(
            f"{glyph.label}\tbbox={x},{y},{w},{h}\tink={glyph.ink_pixels}\t"
            f"distance={glyph.distance:.4f}"
        )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
