"""Synthetic stroke geometry. Not a person, and not a manuscript."""

from __future__ import annotations

import unittest

from PIL import Image, ImageDraw

from engine.stroke_geometry import (
    DISCLAIMER,
    LETTER_DISCLAIMER,
    classify_strokes,
    flip_horizontal,
    letters_same_shape,
    thin_paper_reverse,
)


def _canvas() -> tuple[Image.Image, ImageDraw.ImageDraw]:
    image = Image.new("L", (420, 160), 255)
    return image, ImageDraw.Draw(image)


def separated_strokes(slant: str) -> Image.Image:
    """Print-like strokes with a pen lift between them.

    ``slant`` is ``upright``, ``right`` (/), or ``left`` (\\).
    """
    image, draw = _canvas()
    for index in range(5):
        x = 30 + index * 75
        if slant == "upright":
            draw.line([(x, 30), (x, 130)], fill=0, width=6)
        elif slant == "right":
            draw.line([(x, 130), (x + 36, 30)], fill=0, width=6)
        elif slant == "left":
            draw.line([(x + 36, 130), (x, 30)], fill=0, width=6)
        else:
            raise ValueError(slant)
    return image


def connected_strokes(slant: str = "upright") -> Image.Image:
    """Cursive-like strokes joined by a continuous pen path."""
    image, draw = _canvas()
    points: list[tuple[int, int]] = []
    for index in range(9):
        x = 24 + index * 46
        y = 48 if index % 2 == 0 else 118
        if slant == "right":
            y_shift = int((118 - y) * 0.0)
            x = x + (130 - y) // 3
            y = y + y_shift
        elif slant == "left":
            x = x - (130 - y) // 3
        points.append((x, y))
    draw.line(points, fill=0, width=6)
    return image


def draw_letter(kind: str, *, stroke: int, shift: tuple[int, int]) -> Image.Image:
    """One synthetic letter. ``shift`` and ``stroke`` vary the drawing, not the shape."""
    image = Image.new("L", (180, 180), 255)
    draw = ImageDraw.Draw(image)
    dx, dy = shift
    if kind == "A":
        draw.line([(40 + dx, 150 + dy), (90 + dx, 24 + dy)], fill=0, width=stroke)
        draw.line([(90 + dx, 24 + dy), (140 + dx, 150 + dy)], fill=0, width=stroke)
        draw.line([(62 + dx, 100 + dy), (118 + dx, 100 + dy)], fill=0, width=stroke)
    elif kind == "O":
        draw.ellipse(
            (36 + dx, 28 + dy, 146 + dx, 152 + dy),
            outline=0,
            width=stroke,
        )
    elif kind == "L":
        draw.line([(48 + dx, 22 + dy), (48 + dx, 150 + dy)], fill=0, width=stroke)
        draw.line([(48 + dx, 150 + dy), (142 + dx, 150 + dy)], fill=0, width=stroke)
    else:
        raise ValueError(kind)
    return image


class StrokeGeometryTest(unittest.TestCase):
    def test_print_separated_strokes(self) -> None:
        report = classify_strokes(separated_strokes("upright"))
        self.assertEqual(report.script, "print")
        self.assertEqual(report.slant, "upright")
        self.assertGreaterEqual(report.component_count, 3)
        self.assertFalse(report.identifies_person)
        self.assertFalse(report.left_handed)
        self.assertIn("not a forensic identification", report.disclaimer)
        self.assertIn("ancient manuscript", report.disclaimer)
        self.assertEqual(report.disclaimer, DISCLAIMER)

    def test_cursive_connected_strokes(self) -> None:
        report = classify_strokes(connected_strokes())
        self.assertEqual(report.script, "cursive")
        self.assertEqual(report.component_count, 1)
        self.assertLess(report.interior_gap_columns, 8)
        self.assertFalse(report.identifies_person)

    def test_right_slant(self) -> None:
        report = classify_strokes(separated_strokes("right"))
        self.assertEqual(report.slant, "right")
        self.assertEqual(report.script, "print")
        self.assertLess(report.slope, 0)
        self.assertFalse(report.left_handed)

    def test_left_slant(self) -> None:
        report = classify_strokes(separated_strokes("left"))
        self.assertEqual(report.slant, "left")
        self.assertEqual(report.script, "print")
        self.assertGreater(report.slope, 0)
        self.assertFalse(report.left_handed)
        self.assertIn("not handedness", report.disclaimer)

    def test_flip_reverses_slant(self) -> None:
        right = separated_strokes("right")
        flipped = flip_horizontal(right)
        self.assertEqual(classify_strokes(right).slant, "right")
        flipped_report = classify_strokes(flipped)
        self.assertEqual(flipped_report.slant, "left")
        self.assertFalse(flipped_report.left_handed)
        self.assertTrue(flipped_report.thin_paper_reverses_slant)

    def test_thin_paper_reverse_is_not_left_handed(self) -> None:
        front = separated_strokes("right")
        back = thin_paper_reverse(front)
        front_report = classify_strokes(front)
        back_report = classify_strokes(back)
        self.assertEqual(front_report.slant, "right")
        self.assertEqual(back_report.slant, "left")
        self.assertFalse(back_report.left_handed)
        self.assertFalse(back_report.identifies_person)
        self.assertIn("thin paper", back_report.disclaimer)
        self.assertIn("left-handed", back_report.disclaimer)

    def test_same_letter_drawings_match(self) -> None:
        first = draw_letter("A", stroke=4, shift=(0, 0))
        second = draw_letter("A", stroke=10, shift=(12, -8))
        match = letters_same_shape(first, second)
        self.assertTrue(match.same_shape)
        self.assertLessEqual(match.distance, 0.20)
        self.assertFalse(match.identifies_person)
        self.assertEqual(match.disclaimer, LETTER_DISCLAIMER)
        self.assertIn("Not a forensic identification of a person", match.disclaimer)

    def test_different_letters_do_not_match(self) -> None:
        aye = draw_letter("A", stroke=6, shift=(0, 0))
        oh = draw_letter("O", stroke=6, shift=(4, 4))
        ell = draw_letter("L", stroke=5, shift=(-6, 3))
        self.assertFalse(letters_same_shape(aye, oh).same_shape)
        self.assertFalse(letters_same_shape(aye, ell).same_shape)
        self.assertFalse(letters_same_shape(oh, ell).same_shape)
        self.assertFalse(letters_same_shape(aye, oh).identifies_person)

    def test_same_shape_holds_for_o_and_l(self) -> None:
        self.assertTrue(
            letters_same_shape(
                draw_letter("O", stroke=3, shift=(0, 0)),
                draw_letter("O", stroke=9, shift=(8, 6)),
            ).same_shape
        )
        self.assertTrue(
            letters_same_shape(
                draw_letter("L", stroke=4, shift=(0, 0)),
                draw_letter("L", stroke=11, shift=(-10, 5)),
            ).same_shape
        )


if __name__ == "__main__":
    unittest.main()
