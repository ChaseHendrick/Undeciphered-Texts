"""Normal Human Man: an ordinary baseline with a plain explanatory voice.

This fictional persona tries a small finite set of obvious classical keys.
Its voice and name supply no evidence or special human capabilities.
"""
from engine.language import get_model
from engine.persona_solver_common import make_report,validate_inputs
from engine.solvers.affine import affine_encrypt,affine_decrypt
from engine.solvers.rail_fence import rail_fence_encrypt,rail_fence_decrypt


def investigate_normal_man(text, *, cribs=(), max_checks=5000, max_candidates=20):
    """Try all Caesar shifts and rails 2..7 as a transparent small baseline."""
    cipher,cribs,known=validate_inputs(text,cribs,max_checks,max_candidates)
    tasks=[('caesar',{'shift':shift}) for shift in range(26)]
    tasks.extend(('rail-fence',{'rails':rails}) for rails in range(2,8))
    checks,candidates=0,{}
    for family,key in tasks:
        if checks >= max_checks:
            break
        checks+=1
        if family=='caesar':
            plain=affine_decrypt(cipher,1,key['shift'])
            replay=affine_encrypt(plain,1,key['shift'])
        else:
            plain=rail_fence_decrypt(cipher,key['rails'])
            replay=rail_fence_encrypt(plain,key['rails'])
        if replay!=cipher:
            raise RuntimeError('Normal Human Man trial failed its forward transform')
        if any(plain[position]!=letter for position,letter in known.items()):
            continue
        score=get_model().score([ord(ch)-65 for ch in plain])
        candidate=dict(plaintext=plain,family=family,key=key,score=score,
            forward_consistent=True,crib_match=True,
            evidence={'known_positions':len(known),'independent_correctness':False,
                      'check':'exact forward transform and caller cribs'})
        candidates.setdefault(plain,candidate)
    complete=checks==len(tasks)
    selected=sorted(candidates.values(),key=lambda row:(-row['score'],row['plaintext']))[:max_candidates]
    report=make_report('normal-man','plain small Caesar and rail-fence baseline',selected,
        checks,max_checks,complete,'complete' if complete else 'check_limit',
        [{'stage':'try obvious finite classical keys','checks':checks,'requested_checks':len(tasks)}],
        ['Only 26 Caesar shifts and six ordinary fence heights are tested.',
         'A high English score is a useful suggestion, not independent verification.'])
    report.update(display_name='Normal Human Man',narration='I tried the straightforward keys. These are the candidates that passed the checks.',
                  neural_advice={'status':'not_used','candidates':[]},
                  bounds={'total_declared_checks':len(tasks),'max_checks':max_checks},
                  next_actions=['Compare promising candidates with independent evidence; consider broader models if these fail.'])
    return report


__all__=['investigate_normal_man']
