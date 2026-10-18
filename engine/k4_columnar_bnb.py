"""K4 columnar transposition with substitution by branch and bound, to wider widths.

`engine.k4_transposition_sub` checks every column order to width 10 one at a
time. Here the order is built one read column at a time: placing a column
fixes where its clue letters land, so a contradiction in the key drops every
order that starts that way. The counts are of complete surviving orders, the
same unit as the full enumeration, and `tests/test_k4_columnar_bnb.py` checks
they agree with it width by width before any wider width is trusted.

Only the clue letters are used, so a result holds whatever language K4 is in.

This is not a K4 decipherment. solved stays false. claimed_plaintext stays None.
"""

from __future__ import annotations

import ctypes
import shutil
import subprocess
import tempfile
from functools import lru_cache
from pathlib import Path

from engine.k4_transposition_sub import _ranks, setup

_SOURCE = Path(__file__).with_name("k4_columnar_bnb.c")
VARIANTS = ("vigenere-AZ", "beaufort-AZ", "vigenere-KRYPTOS", "beaufort-KRYPTOS", "any-alphabet")
CAP = 64


@lru_cache(maxsize=1)
def _kernel():
    compiler = shutil.which("cc") or shutil.which("gcc") or shutil.which("clang")
    if compiler is None:
        raise RuntimeError("a C compiler is needed for engine.k4_columnar_bnb")
    built = Path(tempfile.mkdtemp(prefix="k4-columnar-bnb-")) / "kernel.so"
    subprocess.run([compiler, "-O3", "-shared", "-fPIC", "-o", str(built), str(_SOURCE)], check=True)
    lib = ctypes.CDLL(str(built))
    lib.bnb.restype = None
    lib.bnb_dir1.restype = None
    return lib


def search(s: dict, w: int, direction: int, comp: int, p: int, variant: int, node_limit: int = 0,
           cap: int = CAP) -> dict:
    """One width, direction, composition order, period and variant; keeps up to cap complete-key orders."""
    lib = _kernel()
    ncl = len(s["cpos"])
    ct = (ctypes.c_int * s["n"])(*s["ct"])
    cpos = (ctypes.c_int * ncl)(*s["cpos"])
    cpl = (ctypes.c_int * ncl)(*s["cpl"])
    rank = (ctypes.c_int * 52)(*(_ranks()[0] + _ranks()[1]))
    found = (ctypes.c_int * (cap * w))()
    out = (ctypes.c_longlong * 4)()
    lib.bnb(s["n"], ct, ncl, cpos, cpl, rank, w, direction, comp, p, variant,
            ctypes.c_longlong(node_limit), found, cap, out)
    kept = min(out[1], cap)
    orders = [tuple(found[i * w : (i + 1) * w]) for i in range(kept)]
    return {"leaves": out[0], "complete": out[1], "nodes": out[2], "stopped": bool(out[3]), "orders": orders}


def count_dir1(s: dict, w: int, comp: int, p: int, variant: int, node_limit: int = 0) -> dict:
    """Direction 1 surviving-order counts by slot patterns (no orders listed)."""
    lib = _kernel()
    ncl = len(s["cpos"])
    ct = (ctypes.c_int * s["n"])(*s["ct"])
    cpos = (ctypes.c_int * ncl)(*s["cpos"])
    cpl = (ctypes.c_int * ncl)(*s["cpl"])
    rank = (ctypes.c_int * 52)(*(_ranks()[0] + _ranks()[1]))
    out_d = (ctypes.c_double * 2)()
    out = (ctypes.c_longlong * 2)()
    lib.bnb_dir1(s["n"], ct, ncl, cpos, cpl, rank, w, comp, p, variant, ctypes.c_longlong(node_limit), out_d, out)
    return {"leaves": int(round(out_d[0])), "complete": int(round(out_d[1])), "nodes": out[0], "stopped": bool(out[1])}


def _job(args):
    n, w, direction, comp, p, variant, node_limit = args
    return args, search(setup(n), w, direction, comp, p, variant, node_limit)


def scan(widths, periods=range(1, 21), variants=(0, 1, 2, 3), lengths=(97, 98), workers: int = 1,
         node_limit: int = 0) -> dict:
    """Surviving orders per (length, width, composition, period), summed over directions.

    A hypothesis survives a variant when one shift per column places every
    clue letter. `any_strong` counts (order, direction) pairs surviving at
    least one variant is not tracked here; counts are per variant.
    """
    jobs = [(n, w, d, comp, p, v, node_limit) for n in lengths for w in widths for d in (0, 1)
            for comp in (0, 1) for p in periods for v in variants]
    if workers > 1:
        from concurrent.futures import ProcessPoolExecutor

        with ProcessPoolExecutor(workers) as pool:
            results = list(pool.map(_job, jobs, chunksize=2))
    else:
        results = [_job(job) for job in jobs]
    rows = []
    for (n, w, d, comp, p, v, _limit), r in results:
        rows.append({"n": n, "w": w, "dir": d, "comp": comp, "p": p, "variant": VARIANTS[v],
                     "survivors": r["leaves"], "complete": r["complete"], "nodes": r["nodes"],
                     "stopped": r["stopped"], "orders": [list(o) for o in r["orders"]]})
    return {"model": "columnar by branch and bound, clues only", "rows": rows,
            "solved": False, "claimed_plaintext": None}


if __name__ == "__main__":
    import json
    import sys

    low, high = int(sys.argv[1]), int(sys.argv[2])
    workers = int(sys.argv[3]) if len(sys.argv) > 3 else 1
    top = int(sys.argv[4]) if len(sys.argv) > 4 else 20
    print(json.dumps(scan(range(low, high + 1), periods=range(1, top + 1), workers=workers)))
