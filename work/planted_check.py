"""Planted controls for the relaxed periodic-Gromark SAT, corrected. Not for the repo."""
import random

import work.scratch_periodic as sp
from engine.solvers.periodic_gromark import (
    periodic_gromark_alphabet,
    periodic_gromark_encrypt,
    periodic_gromark_primer,
    periodic_gromark_running_key,
)
from engine.solvers.gromark import gromark_keyword
from pysat.solvers import Solver

sp.SPEC = None  # disable default constant use in module-level constant checks


def planted_case(klen, rng):
    head = "".join(rng.sample("ABCDEFGHIJKLMNOPQRSTUVWXYZ", klen))
    plain = [rng.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(97)]
    plain[21:34] = list("EASTNORTHEAST")
    plain[63:74] = list("BERLINCLOCK")
    pt = "".join(plain)
    ct = periodic_gromark_encrypt(pt, keyword=head)
    kwm = gromark_keyword(head)
    A = periodic_gromark_alphabet(kwm)
    S_true = [A.index(ch) for ch in kwm]
    R_true = [int(c) for c in periodic_gromark_running_key(kwm, 97)]
    spec = [(start + o, ct[start + o], ch)
            for start, word in sp.CRIB_SPANS
            for o, ch in enumerate(word)]
    return ct, spec, S_true, R_true, head


def run_case(klen, rng):
    ct, spec, S_true, R_true, head = planted_case(klen, rng)
    f = sp.Cnf()
    # build with spec override
    sp_ct = sp.CT
    sp.SPEC = spec
    f, S, r, t, ton, toff, fitted, reserved = sp.build(klen, fits=(0, 1))
    sp.SPEC = None
    pins = [S[g][S_true[g]] for g in range(klen)] + [r[i][R_true[i]] for i in range(97)]
    with Solver(name="cadical153", bootstrap_with=f.cls) as s:
        ok_pin = s.solve(assumptions=pins)
        ok_free = s.solve()
    print(f"k={klen} head={head}: pinned {'SAT' if ok_pin else 'UNSAT'}, free {'SAT' if ok_free else 'UNSAT'}")


if __name__ == "__main__":
    rng = random.Random(11)
    for klen in range(2, 10):
        run_case(klen, rng)
