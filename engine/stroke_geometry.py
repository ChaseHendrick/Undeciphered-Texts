"""Stroke geometry and letter-shape comparison.

Measures ink the caller supplies: whether strokes are separated or joined,
which way those strokes lean, and whether two drawings share a letter shape.

This is pixel geometry on a picture. It is not a claim about a real person's
handwriting, not a forensic identification of a writer, and not a reading of
an ancient manuscript. Slant here is the lean of the ink, not handedness.
A horizontal flip, including the view through thin paper from the back of the
sheet, reverses that lean. The reversed picture is still not evidence that
someone is left-handed.
"""

from __future__ import annotations

from dataclasses import dataclass

DISCLAIMER = (
    "Stroke geometry only. Not a claim about a real person's handwriting, "
    "not a forensic identification of a writer, and not a reading of an "
    "ancient manuscript. Slant is ink lean, not handedness, and not evidence "
    "someone is left-handed. A horizontal flip, including thin paper seen "
    "from the back, reverses slant."
)

LETTER_DISCLAIMER = (
    "Letter-shape comparison of drawings. Not a forensic identification "
    "of a person, and not a claim about who wrote a manuscript."
)

# dx/dy below this absolute value is treated as upright.
_SLANT_SLOPE = 0.28
# Interior empty columns wider than this, inside the ink span, mean a pen lift.
_GAP_COLUMNS = 8
_MIN_COMPONENT_PIXELS = 12
_GRID = 16


@dataclass(frozen=True)
class StrokeReport:
    """Geometry of one ink picture.

    ``script`` is ``print`` when strokes are separated by gaps and ``cursive``
    when the ink is one joined run. ``slant`` is ``right`` (lean like /),
    ``left`` (lean like \\), or ``upright``. ``identifies_person`` is always
    false. ``left_handed`` is always false: lean is not a person.
    """

    script: str
    slant: str
    slope: float
    component_count: int
    interior_gap_columns: int
    identifies_person: bool
    left_handed: bool
    thin_paper_reverses_slant: bool
    disclaimer: str

    def as_dict(self) -> dict[str, object]:
        return {
            "script": self.script,
            "slant": self.slant,
            "slope": self.slope,
            "component_count": self.component_count,
            "interior_gap_columns": self.interior_gap_columns,
            "identifies_person": self.identifies_person,
            "left_handed": self.left_handed,
            "thin_paper_reverses_slant": self.thin_paper_reverses_slant,
            "disclaimer": self.disclaimer,
        }


@dataclass(frozen=True)
class LetterMatch:
    """Whether two drawings are the same letter shape.

    ``same_shape`` is a geometry decision. ``identifies_person`` is always
    false.
    """

    same_shape: bool
    distance: float
    identifies_person: bool
    disclaimer: str


def _gray_rows(image: object) -> list[list[int]]:
    """Accept a Pillow image or a sequence of gray rows (0 dark, 255 light)."""
    if hasattr(image, "convert") and hasattr(image, "size"):
        gray = image.convert("L")  # type: ignore[attr-defined]
        width, height = gray.size
        raw = list(gray.getdata())
        return [list(raw[y * width : (y + 1) * width]) for y in range(height)]
    rows = [list(row) for row in image]  # type: ignore[arg-type]
    if not rows or not rows[0]:
        raise ValueError("image has no pixels")
    width = len(rows[0])
    if any(len(row) != width for row in rows):
        raise ValueError("image rows have different widths")
    return rows


def ink_mask(image: object, threshold: int = 160) -> list[list[bool]]:
    """True where the pixel is darker than ``threshold``."""
    return [[value < threshold for value in row] for row in _gray_rows(image)]


def _components(mask: list[list[bool]]) -> list[list[tuple[int, int]]]:
    """8-connected ink components, smallest blobs dropped."""
    height = len(mask)
    width = len(mask[0]) if height else 0
    seen = [[False] * width for _ in range(height)]
    found: list[list[tuple[int, int]]] = []
    for y in range(height):
        for x in range(width):
            if not mask[y][x] or seen[y][x]:
                continue
            stack = [(x, y)]
            seen[y][x] = True
            pixels: list[tuple[int, int]] = []
            while stack:
                cx, cy = stack.pop()
                pixels.append((cx, cy))
                for dy in (-1, 0, 1):
                    ny = cy + dy
                    if ny < 0 or ny >= height:
                        continue
                    for dx in (-1, 0, 1):
                        if dx == 0 and dy == 0:
                            continue
                        nx = cx + dx
                        if nx < 0 or nx >= width or seen[ny][nx] or not mask[ny][nx]:
                            continue
                        seen[ny][nx] = True
                        stack.append((nx, ny))
            if len(pixels) >= _MIN_COMPONENT_PIXELS:
                found.append(pixels)
    return found


def _column_occupied(mask: list[list[bool]]) -> list[bool]:
    width = len(mask[0])
    height = len(mask)
    return [any(mask[y][x] for y in range(height)) for x in range(width)]


def _interior_gap_columns(occupied: list[bool]) -> int:
    ink_at = [i for i, flag in enumerate(occupied) if flag]
    if len(ink_at) < 2:
        return 0
    left, right = ink_at[0], ink_at[-1]
    gap = 0
    best = 0
    for x in range(left, right + 1):
        if not occupied[x]:
            gap += 1
            if gap > best:
                best = gap
        else:
            gap = 0
    return best


def _component_slope(pixels: list[tuple[int, int]]) -> float | None:
    """Least-squares dx/dy. Negative is a right lean (/). None if too flat."""
    n = len(pixels)
    if n < _MIN_COMPONENT_PIXELS:
        return None
    xs = [p[0] for p in pixels]
    ys = [p[1] for p in pixels]
    height = max(ys) - min(ys)
    if height < 8:
        return None
    mean_x = sum(xs) / n
    mean_y = sum(ys) / n
    var_y = sum((y - mean_y) ** 2 for y in ys)
    if var_y <= 0:
        return None
    cov = sum((x - mean_x) * (y - mean_y) for x, y in pixels)
    return cov / var_y


def _mean_slope(components: list[list[tuple[int, int]]]) -> float:
    slopes: list[float] = []
    weights: list[int] = []
    for pixels in components:
        slope = _component_slope(pixels)
        if slope is None:
            continue
        slopes.append(slope)
        weights.append(len(pixels))
    if not slopes:
        return 0.0
    total = sum(weights)
    return sum(s * w for s, w in zip(slopes, weights)) / total


def _slant_label(slope: float) -> str:
    # Image y grows downward. A stroke like / has smaller x at larger y,
    # so dx/dy is negative: right lean. A stroke like \ has positive dx/dy.
    if slope <= -_SLANT_SLOPE:
        return "right"
    if slope >= _SLANT_SLOPE:
        return "left"
    return "upright"


def classify_strokes(image: object) -> StrokeReport:
    """Classify separated versus joined strokes, and the lean of the ink.

    Does not identify a person. ``left_handed`` is always false.
    """
    mask = ink_mask(image)
    if not mask or not any(any(row) for row in mask):
        raise ValueError("no ink pixels")
    components = _components(mask)
    if not components:
        raise ValueError("no ink pixels")
    occupied = _column_occupied(mask)
    gap = _interior_gap_columns(occupied)
    # Joined ink is one component and has no wide pen-lift inside the span.
    # Separated strokes leave a wide empty run between components.
    script = "print" if gap >= _GAP_COLUMNS or len(components) >= 3 else "cursive"
    if len(components) == 1 and gap < _GAP_COLUMNS:
        script = "cursive"
    slope = _mean_slope(components)
    return StrokeReport(
        script=script,
        slant=_slant_label(slope),
        slope=slope,
        component_count=len(components),
        interior_gap_columns=gap,
        identifies_person=False,
        left_handed=False,
        thin_paper_reverses_slant=True,
        disclaimer=DISCLAIMER,
    )


def flip_horizontal(image: object):
    """Mirror a Pillow image left-to-right. Slant reverses. Person does not."""
    if not hasattr(image, "transpose"):
        raise TypeError("flip_horizontal expects a Pillow image")
    from PIL import Image

    return image.transpose(Image.Transpose.FLIP_LEFT_RIGHT)


def thin_paper_reverse(image: object):
    """Ink as seen from the back of a thin sheet: a horizontal mirror.

    The lean reverses. That is not a left-handed writer and not a second person.
    """
    return flip_horizontal(image)


def _crop_mask(mask: list[list[bool]]) -> list[list[bool]]:
    ys = [y for y, row in enumerate(mask) if any(row)]
    xs = [x for row in mask for x, flag in enumerate(row) if flag]
    if not ys:
        raise ValueError("no ink pixels")
    top, bottom = min(ys), max(ys)
    left, right = min(xs), max(xs)
    return [row[left : right + 1] for row in mask[top : bottom + 1]]


def _dilate(mask: list[list[bool]], radius: int = 2) -> list[list[bool]]:
    height = len(mask)
    width = len(mask[0])
    out = [[False] * width for _ in range(height)]
    ink = [(x, y) for y in range(height) for x in range(width) if mask[y][x]]
    for x, y in ink:
        for dy in range(-radius, radius + 1):
            ny = y + dy
            if ny < 0 or ny >= height:
                continue
            for dx in range(-radius, radius + 1):
                nx = x + dx
                if 0 <= nx < width:
                    out[ny][nx] = True
    return out


def _resample(mask: list[list[bool]], size: int = _GRID) -> list[float]:
    height = len(mask)
    width = len(mask[0])
    values: list[float] = []
    for gy in range(size):
        y0 = gy * height // size
        y1 = max(y0 + 1, (gy + 1) * height // size)
        for gx in range(size):
            x0 = gx * width // size
            x1 = max(x0 + 1, (gx + 1) * width // size)
            ink = 0
            total = 0
            for y in range(y0, min(y1, height)):
                for x in range(x0, min(x1, width)):
                    total += 1
                    if mask[y][x]:
                        ink += 1
            values.append(ink / total if total else 0.0)
    return values


def letter_descriptor(image: object) -> tuple[float, ...]:
    """Scale-free ink occupancy of one drawing, after a small dilation."""
    mask = _dilate(_crop_mask(ink_mask(image)))
    return tuple(_resample(mask))


def letter_distance(image_a: object, image_b: object) -> float:
    """L1 distance between letter descriptors, in ``[0, 1]``-ish occupancy units."""
    left = letter_descriptor(image_a)
    right = letter_descriptor(image_b)
    return sum(abs(a - b) for a, b in zip(left, right)) / len(left)


def letters_same_shape(image_a: object, image_b: object, max_distance: float = 0.20) -> LetterMatch:
    """True when two drawings share a letter shape.

    Not a forensic identification of a person. Two copies of one synthetic
    letter match; two different letters do not.
    """
    distance = letter_distance(image_a, image_b)
    return LetterMatch(
        same_shape=distance <= max_distance,
        distance=distance,
        identifies_person=False,
        disclaimer=LETTER_DISCLAIMER,
    )
