"""Cartographer explores bounded layout hypotheses in the existing engine.

This is a search policy over established transpositions, not a new cipher,
personality-biased plaintext reading or independently verified decipherment.
"""
from engine.persona_solver_common import make_report, validate_inputs
from engine.transposition_ensemble import search_transposition_ensemble


def investigate_cartographer(text, *, cribs=(), max_checks=5000,
                            max_candidates=20, max_width=32, max_rails=5):
    """Test deeper rectangle widths, rail paths and row orderings fairly."""
    letters, cribs, _ = validate_inputs(text,cribs,max_checks,max_candidates)
    result=search_transposition_ensemble(letters,cribs=cribs,max_checks=max_checks,
        max_candidates=max_candidates,max_width=max_width,max_rails=max_rails)
    candidates=[]
    for witness in result.candidates:
        candidates.append(dict(plaintext=witness.plaintext,family=witness.family,
            key=witness.key,score=witness.score,forward_consistent=witness.re_encryption_matches,
            crib_match=True,evidence=dict(layout=witness.key,
                equivalent_keys=list(witness.equivalent_keys),
                equivalent_keys_seen=witness.equivalent_keys_seen,
                supplied_cribs=len(cribs),independent_correctness=False)))
    report=make_report('cartographer','finite layout and transposition mapping',candidates,
        result.checks,max_checks,result.search_complete,result.stop_reason,
        [dict(family=family,checks=checks) for family,checks in result.family_checks.items()],
        ['Only requested rectangle widths, rail paths and bounded row permutations are tested.',
         'English scores and equivalent layouts do not establish the historical family.'])
    report.update(bounds=dict(max_width=max_width,max_rails=max_rails,max_checks=max_checks),
                  ledger=result.to_dict(),neural_advice={'status':'not_used','candidates':[]})
    return report


__all__=['investigate_cartographer']
