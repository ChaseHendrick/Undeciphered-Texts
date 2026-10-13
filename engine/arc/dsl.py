# SPDX-License-Identifier: MIT-0
"""Finite grid DSL and its deterministic length-first enumeration.

Programs are data, never eval/exec strings. Undefined or oversized intermediate
results reject a program on that input. Votes count syntax in this grammar,
not probabilities. The grammar is deliberately small and not a general solver.
"""
from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
from collections.abc import Sequence

from .grid import Grid, MAX_SIDE, components, crop_cells, mode_color, shape


@dataclass(frozen=True)
class Atom:
    name: str
    args: tuple = ()

    def __post_init__(self):
        if not isinstance(self.args, tuple):
            raise ValueError('operation arguments must be an immutable tuple')
        a = self.args
        color = lambda x: type(x) is int and 0 <= x <= 9
        bg = lambda x: color(x) or x == 'mode'
        valid = ((self.name in D4 and not a)
                 or (self.name in ('replace', 'swap') and len(a) == 2 and all(color(x) for x in a))
                 or (self.name == 'color_map' and len(a) == 10 and all(color(x) for x in a))
                 or (self.name == 'crop_background' and len(a) == 1 and bg(a[0]))
                 or (self.name == 'crop_color' and len(a) == 1 and color(a[0]))
                 or (self.name == 'component' and len(a) == 3 and bg(a[0])
                     and type(a[1]) is bool and a[2] in ('largest', 'smallest'))
                 or (self.name in ('scale', 'tile', 'repeat_rows', 'repeat_cols')
                     and len(a) == 1 and type(a[0]) is int and a[0] in (2, 3))
                 or (self.name == 'compress' and len(a) == 1 and a[0] in ('rows', 'cols', 'both')))
        if not valid:
            raise ValueError(f'invalid operation or arguments: {self.name!r}, {a!r}')

    def to_dict(self):
        return {'op': self.name, 'args': list(self.args)}


@dataclass(frozen=True)
class Program:
    steps: tuple[Atom, ...]

    def __post_init__(self):
        if not isinstance(self.steps, tuple) or not self.steps or any(not isinstance(a, Atom) for a in self.steps):
            raise ValueError('a program needs one or more Atom steps')

    @property
    def cost(self):
        return len(self.steps)

    def to_dict(self):
        return [step.to_dict() for step in self.steps]

    @property
    def key(self):
        return json.dumps(self.to_dict(), separators=(',', ':'), sort_keys=True)


def apply_atom(atom: Atom, grid: Grid) -> Grid | None:
    name, args = atom.name, atom.args
    h, w = shape(grid)
    if name == 'identity':
        return grid
    if name == 'rot90':
        return tuple(tuple(grid[h - 1 - c][r] for c in range(h)) for r in range(w))
    if name == 'rot180':
        return tuple(tuple(reversed(row)) for row in reversed(grid))
    if name == 'rot270':
        return tuple(tuple(grid[c][w - 1 - r] for c in range(h)) for r in range(w))
    if name == 'flip_rows':
        return tuple(reversed(grid))
    if name == 'flip_cols':
        return tuple(tuple(reversed(row)) for row in grid)
    if name == 'transpose':
        return tuple(zip(*grid))
    if name == 'anti_transpose':
        return tuple(tuple(grid[h - 1 - c][w - 1 - r] for c in range(h)) for r in range(w))
    if name == 'replace':
        old, new = args
        return tuple(tuple(new if x == old else x for x in row) for row in grid)
    if name == 'swap':
        a, b = args
        return tuple(tuple(b if x == a else a if x == b else x for x in row) for row in grid)
    if name == 'color_map':
        return tuple(tuple(args[x] for x in row) for row in grid)
    if name in ('crop_background', 'crop_color'):
        value = mode_color(grid) if args[0] == 'mode' else args[0]
        cells = ((r, c) for r in range(h) for c in range(w)
                 if (grid[r][c] != value if name == 'crop_background' else grid[r][c] == value))
        return crop_cells(grid, cells)
    if name == 'component':
        background, monochrome, which = args
        background = mode_color(grid) if background == 'mode' else background
        groups = components(grid, background, monochrome)
        if not groups:
            return None
        ordered = sorted(groups, key=lambda cells: ((-1 if which == 'largest' else 1) * len(cells), cells))
        return crop_cells(grid, ordered[0], mask=True, background=background)
    if name in ('repeat_rows', 'repeat_cols'):
        factor = args[0]
        if (h if name == 'repeat_rows' else w) * factor > MAX_SIDE:
            return None
        if name == 'repeat_rows':
            return tuple(row for row in grid for _ in range(factor))
        return tuple(tuple(x for x in row for _ in range(factor)) for row in grid)
    if name in ('scale', 'tile'):
        factor = args[0]
        if h * factor > MAX_SIDE or w * factor > MAX_SIDE:
            return None
        if name == 'scale':
            return tuple(tuple(x for x in row for _ in range(factor)) for row in grid for _ in range(factor))
        return tuple(row * factor for _ in range(factor) for row in grid)
    if name == 'compress':
        axis = args[0]
        result = grid
        if axis in ('rows', 'both'):
            result = tuple(row for r, row in enumerate(result) if r == 0 or row != result[r - 1])
        if axis in ('cols', 'both'):
            cols = tuple(zip(*result))
            cols = tuple(col for c, col in enumerate(cols) if c == 0 or col != cols[c - 1])
            result = tuple(zip(*cols))
        return result
    raise ValueError(f'unknown operation: {name}')


def apply_program(program: Program, grid: Grid) -> Grid | None:
    for atom in program.steps:
        grid = apply_atom(atom, grid)
        if grid is None:
            return None
    return grid


D4 = ('identity', 'rot90', 'rot180', 'rot270', 'flip_rows', 'flip_cols', 'transpose', 'anti_transpose')


def primitives(training: Sequence[tuple[Grid, Grid]]) -> tuple[Atom, ...]:
    """Instantiate the fixed grammar using demonstration pairs only.

    Color maps fitted after each D4 transform use all demonstrations. Unseen
    colors remain unchanged, an explicit modeling assumption rather than a
    forced inference. No test input or answer enters parameter fitting.
    """
    atoms = [Atom(name) for name in D4]
    learned = []
    for transform in D4:
        mapping = {}
        valid = True
        for source, target in training:
            source = apply_atom(Atom(transform), source)
            if shape(source) != shape(target):
                valid = False
                break
            for row, out in zip(source, target):
                for color, dest in zip(row, out):
                    if color in mapping and mapping[color] != dest:
                        valid = False
                    mapping[color] = dest
        if valid:
            params = tuple(mapping.get(color, color) for color in range(10))
            if params != tuple(range(10)) and params not in learned:
                learned.append(params)
    atoms.extend(Atom('color_map', mapping) for mapping in sorted(learned))
    atoms.extend(Atom('crop_background', (bg,)) for bg in (0, 'mode'))
    atoms.extend(Atom('component', (bg, mono, which)) for bg in (0, 'mode')
                 for mono in (True, False) for which in ('largest', 'smallest'))
    atoms.extend(Atom('compress', (axis,)) for axis in ('rows', 'cols', 'both'))
    atoms.extend(Atom(op, (factor,)) for op in ('scale', 'tile', 'repeat_rows', 'repeat_cols') for factor in (2, 3))
    atoms.extend(Atom('crop_color', (color,)) for color in range(10))
    atoms.extend(Atom('replace', (old, new)) for old in range(10) for new in range(10) if old != new)
    atoms.extend(Atom('swap', (a, b)) for a in range(10) for b in range(a + 1, 10))
    assert len(atoms) == len(set(atoms))
    return tuple(atoms)


def programs(atoms: Sequence[Atom]):
    """All single atoms, then two nonidentity atoms in diagonal index order.

    Diagonal order shares the budget across both composition positions. It is
    fixed before evaluation. Repeated literal programs never get extra votes;
    semantically equivalent but syntactically distinct programs may still vote.
    """
    for atom in atoms:
        yield Program((atom,))
    inner = tuple(atom for atom in atoms if atom.name != 'identity')
    n = len(inner)
    for diagonal in range(2 * n - 1):
        for left in range(max(0, diagonal - n + 1), min(n - 1, diagonal) + 1):
            yield Program((inner[left], inner[diagonal - left]))


def grammar_size(atoms):
    return len(atoms) + sum(a.name != 'identity' for a in atoms) ** 2


def grammar_sha256(atoms):
    payload = {'version': 'arc-dsl-v1', 'order': 'single-then-composition-diagonal',
               'maximum_depth': 2, 'atoms': [a.to_dict() for a in atoms]}
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
