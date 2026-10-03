"""Synthetic mural / painting analyzer: colors, regions, motif repeat.

This module measures flat RGB structure on images you generate or supply.
It does not read Teotihuacan glyphs, Mesoamerican murals, or any ancient
painting. It does not OCR, decipher, or claim a glyph reading.

Connected-region labeling follows the same one-pass union-find idea used in
classical site percolation (Hoshen-Kopelman), reimplemented here for RGB
labels. That technique appears in ChaseHendrick/GENChase's percolation plate;
no studio JavaScript is copied.

Stdlib only for analysis. Pillow is optional for load/save of PNG files.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Sequence

RGB = tuple[int, int, int]
PixelGrid = list[list[RGB]]

# Flat synthetic palette (not a historical reconstruction).
BACKGROUND: RGB = (240, 230, 210)
BLOCK_A: RGB = (60, 110, 180)
BLOCK_B: RGB = (40, 140, 90)
BLOCK_C: RGB = (180, 120, 50)
MOTIF: RGB = (200, 40, 40)


@dataclass(frozen=True)
class ColorCount:
    rgb: RGB
    pixels: int
    fraction: float


@dataclass(frozen=True)
class Region:
    label: int
    color: RGB
    size: int
    bbox: tuple[int, int, int, int]  # min_y, min_x, max_y, max_x
    shape_key: tuple[int, int, int]  # height, width, size


@dataclass(frozen=True)
class MuralReport:
    width: int
    height: int
    dominant_colors: list[ColorCount]
    region_count: int
    regions: list[Region]
    motif_repeats: bool
    motif_repeat_count: int
    disclaimer: str


DISCLAIMER = (
    "Does not read Teotihuacan glyphs or any ancient painting. "
    "Reports only flat RGB structure on synthetic or modern raster input."
)


def quantize_rgb(rgb: RGB, step: int = 32) -> RGB:
    """Bucket each channel. Same spirit as discrete color fields in GENChase plates."""
    if step < 1:
        raise ValueError("step must be >= 1")
    r, g, b = rgb

    def q(c: int) -> int:
        return min(255, (c // step) * step)

    return (q(r), q(g), q(b))


def make_synthetic_mural(width: int = 96, height: int = 64) -> PixelGrid:
    """Colored blocks plus a repeated plus-shaped motif (synthetic only)."""
    if width < 48 or height < 40:
        raise ValueError("synthetic mural needs at least 48x40")
    grid: PixelGrid = [[BACKGROUND for _ in range(width)] for _ in range(height)]

    def fill_rect(y0: int, x0: int, y1: int, x1: int, color: RGB) -> None:
        for y in range(y0, y1):
            for x in range(x0, x1):
                grid[y][x] = color

    fill_rect(4, 4, height // 2 - 2, width // 3 - 2, BLOCK_A)
    fill_rect(4, width // 3 + 2, height // 2 - 2, 2 * width // 3 - 2, BLOCK_B)
    fill_rect(height // 2 + 2, 4, height - 4, width // 2 - 2, BLOCK_C)

    def stamp_plus(cy: int, cx: int, arm: int = 4) -> None:
        for dy in range(-arm, arm + 1):
            y = cy + dy
            if 0 <= y < height:
                grid[y][cx] = MOTIF
        for dx in range(-arm, arm + 1):
            x = cx + dx
            if 0 <= x < width:
                grid[cy][x] = MOTIF

    stamp_plus(height // 4, width // 6)
    stamp_plus(height // 4, width // 2)
    stamp_plus(3 * height // 4, 3 * width // 4)
    return grid


def load_pixels(path: Path) -> PixelGrid:
    """Load RGB pixels. Requires Pillow when reading a file."""
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError(
            "Pillow is not installed. Analysis of in-memory grids works without it; "
            "install Pillow (or python3-pil) to load image files."
        ) from exc
    image = Image.open(path).convert("RGB")
    width, height = image.size
    data = list(image.getdata())
    return [
        [data[y * width + x] for x in range(width)]  # type: ignore[misc]
        for y in range(height)
    ]


def save_pixels(grid: PixelGrid, path: Path) -> Path:
    """Write a PNG when Pillow is available."""
    try:
        from PIL import Image
    except ImportError as exc:
        raise RuntimeError(
            "Pillow is not installed, so this helper cannot write a PNG."
        ) from exc
    height = len(grid)
    width = len(grid[0]) if height else 0
    image = Image.new("RGB", (width, height))
    flat: list[RGB] = [px for row in grid for px in row]
    image.putdata(flat)
    path.parent.mkdir(parents=True, exist_ok=True)
    image.save(path, format="PNG")
    return path


def dominant_colors(
    grid: PixelGrid, *, top_n: int = 5, step: int = 32
) -> list[ColorCount]:
    """Return the most common quantized colors by pixel count."""
    if not grid or not grid[0]:
        return []
    counts: Counter[RGB] = Counter()
    for row in grid:
        for px in row:
            counts[quantize_rgb(px, step)] += 1
    total = sum(counts.values()) or 1
    ranked = counts.most_common(top_n)
    return [
        ColorCount(rgb=color, pixels=n, fraction=n / total) for color, n in ranked
    ]


class _UnionFind:
    """Tiny union-find for Hoshen-Kopelman-style labeling."""

    def __init__(self) -> None:
        self.parent: dict[int, int] = {}

    def add(self, x: int) -> None:
        if x not in self.parent:
            self.parent[x] = x

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> int:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[rb] = ra
        return ra


def connected_regions(
    grid: PixelGrid, *, step: int = 32, min_size: int = 1
) -> list[Region]:
    """Label 4-connected same-color regions (Hoshen-Kopelman style)."""
    if not grid or not grid[0]:
        return []
    height = len(grid)
    width = len(grid[0])
    labels = [[0 for _ in range(width)] for _ in range(height)]
    uf = _UnionFind()
    next_label = 1
    colors: dict[int, RGB] = {}

    for y in range(height):
        for x in range(width):
            color = quantize_rgb(grid[y][x], step)
            left = labels[y][x - 1] if x > 0 else 0
            up = labels[y - 1][x] if y > 0 else 0
            left_ok = bool(left) and quantize_rgb(grid[y][x - 1], step) == color
            up_ok = bool(up) and quantize_rgb(grid[y - 1][x], step) == color
            if left_ok and up_ok:
                root = uf.union(left, up)
                labels[y][x] = root
            elif left_ok:
                labels[y][x] = uf.find(left)
            elif up_ok:
                labels[y][x] = uf.find(up)
            else:
                uf.add(next_label)
                colors[next_label] = color
                labels[y][x] = next_label
                next_label += 1

    sizes: Counter[int] = Counter()
    bbox: dict[int, list[int]] = {}
    root_color: dict[int, RGB] = {}
    for y in range(height):
        for x in range(width):
            root = uf.find(labels[y][x])
            labels[y][x] = root
            sizes[root] += 1
            if root not in root_color:
                root_color[root] = colors.get(root, quantize_rgb(grid[y][x], step))
            if root not in bbox:
                bbox[root] = [y, x, y, x]
            else:
                box = bbox[root]
                box[0] = min(box[0], y)
                box[1] = min(box[1], x)
                box[2] = max(box[2], y)
                box[3] = max(box[3], x)

    regions: list[Region] = []
    for root, size in sizes.items():
        if size < min_size:
            continue
        y0, x0, y1, x1 = bbox[root]
        h = y1 - y0 + 1
        w = x1 - x0 + 1
        regions.append(
            Region(
                label=root,
                color=root_color[root],
                size=size,
                bbox=(y0, x0, y1, x1),
                shape_key=(h, w, size),
            )
        )
    regions.sort(key=lambda r: (-r.size, r.label))
    return regions


def motif_repeat_info(
    regions: Sequence[Region], *, motif_color: RGB = MOTIF, step: int = 32
) -> tuple[bool, int]:
    """A motif repeats when two+ same-color regions share a shape signature."""
    q_motif = quantize_rgb(motif_color, step)
    by_shape: dict[tuple[int, int, int], int] = defaultdict(int)
    for region in regions:
        if quantize_rgb(region.color, step) != q_motif:
            continue
        by_shape[region.shape_key] += 1
    if not by_shape:
        return False, 0
    best = max(by_shape.values())
    return best >= 2, best


def analyze_mural(
    grid: PixelGrid,
    *,
    top_n: int = 5,
    step: int = 32,
    motif_color: RGB = MOTIF,
) -> MuralReport:
    """Dominant colors, connected regions, and whether a motif repeats."""
    height = len(grid)
    width = len(grid[0]) if height else 0
    colors = dominant_colors(grid, top_n=top_n, step=step)
    regions = connected_regions(grid, step=step)
    repeats, repeat_count = motif_repeat_info(
        regions, motif_color=motif_color, step=step
    )
    return MuralReport(
        width=width,
        height=height,
        dominant_colors=colors,
        region_count=len(regions),
        regions=regions,
        motif_repeats=repeats,
        motif_repeat_count=repeat_count,
        disclaimer=DISCLAIMER,
    )


def report_to_dict(report: MuralReport) -> dict:
    return asdict(report)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="python -m engine.mural_analyzer",
        description=(
            "Analyze a synthetic mural's colors and regions. "
            "Does not read Teotihuacan glyphs or any ancient painting."
        ),
    )
    parser.add_argument(
        "--synthetic",
        action="store_true",
        help="generate the built-in colored-block mural with a repeated motif",
    )
    parser.add_argument("--image", type=Path, help="optional PNG/JPEG path (needs Pillow)")
    parser.add_argument(
        "--write-synthetic",
        type=Path,
        metavar="PATH",
        help="write the synthetic mural PNG (needs Pillow); does not touch readme-hero.jpg",
    )
    args = parser.parse_args(argv)

    if args.synthetic or args.write_synthetic:
        grid = make_synthetic_mural()
        if args.write_synthetic:
            save_pixels(grid, args.write_synthetic)
            print(f"wrote {args.write_synthetic.resolve()}")
    elif args.image:
        grid = load_pixels(args.image)
    else:
        parser.error("pass --synthetic and/or --image PATH")

    report = analyze_mural(grid)
    print(json.dumps(report_to_dict(report), indent=2))
    print(report.disclaimer)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
