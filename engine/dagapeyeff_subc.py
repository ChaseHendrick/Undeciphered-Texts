"""Loader for the periodic substitution kernel with null symbols. Not a reading.

`engine/dagapeyeff_subc.c` anneals one or more substitution alphabets, and may
drop up to a set number of symbols as nulls, under the default English model
with J folded into I. The callers are short attacks with planted texts and
shuffled controls. The best letters are returned so a caller may store them
as a candidate; a candidate is not a reading.
"""

from __future__ import annotations

import ctypes
import shutil
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path

from engine.dagapeyeff_foursquare import PLAIN, _model

_SOURCE = Path(__file__).resolve().parent / "dagapeyeff_subc.c"


@lru_cache(maxsize=1)
def _kernel():
    compiler = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if compiler is None:
        raise RuntimeError("a C compiler is needed to rerun the substitution search")
    built = Path(tempfile.mkdtemp(prefix="subc-")) / "kernel.so"
    subprocess.run([compiler, "-O3", "-shared", "-fPIC", "-o", str(built), str(_SOURCE), "-lm"], check=True)
    lib = ctypes.CDLL(str(built))
    lib.sub_anneal.restype = ctypes.c_double
    return lib


@lru_cache(maxsize=1)
def _tables():
    logp = (ctypes.c_double * 26 ** 4)(*_model().logp)
    plain = (ctypes.c_int * 25)(*[ord(ch) - 65 for ch in PLAIN])
    return logp, plain


def anneal(cells: list[int], seed: int, *, period: int = 1, max_nulls: int = 0,
           min_letters: int = 0, restarts: int = 8, steps: int = 200_000,
           temperature: float = 0.04) -> dict:
    """Best per-letter score, the letters behind it, and the null symbols."""
    lib = _kernel()
    logp, plain = _tables()
    n = len(cells)
    cipher = (ctypes.c_int * n)(*cells)
    key = (ctypes.c_int * (25 * period))()
    null = (ctypes.c_int * 25)()
    out = (ctypes.c_int * n)()
    length = ctypes.c_int(0)
    best = lib.sub_anneal(cipher, n, period, max_nulls, min_letters, logp, plain,
                          ctypes.c_ulonglong(seed), restarts, steps, ctypes.c_double(temperature),
                          key, null, out, ctypes.byref(length))
    letters = "".join(chr(65 + x) for x in out[:length.value])
    return {
        "per_letter": best,
        "letters": letters,
        "nulls": [s for s in range(25) if null[s]],
        "key": [PLAIN[k] for k in key],
    }
