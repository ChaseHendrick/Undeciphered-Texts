# Pacifist preference (Caesar candidates)

`engine/solvers/pacifist.py` is given two or more candidate plaintexts for
**one known Caesar ciphertext**. It picks the peaceful sentence over a
violent one using a small word list:

- Peace words: `peace`, `calm`, `garden`
- Violence words: `attack`, `war`, `kill`

The score is peace hits minus violence hits. The higher score wins. Ties
keep the earlier candidate.

This is a **preference among candidates**. It is **not** a decipherment of
army message Nr. 86, Kryptos K4, or an unknown script.

## Fixture

| Field | Value |
| --- | --- |
| Peaceful plaintext | The calm garden keeps peace under soft light. |
| Violent candidate | The attack will kill foes in a brutal war! |
| Caesar shift | 7 |
| Ciphertext | `Aol jhst nhyklu rllwz wlhjl bukly zvma spnoa.` |

The peaceful sentence encrypts to that ciphertext under shift 7. The
solver does not search shifts. It ranks the supplied candidates only.

## Verification certificate

`engine/data/pacifist_certificate.json` records the method, cipher name,
plaintext, ciphertext, candidates, chosen sentence, and the SHA-256 of
the peaceful plaintext. `PacifistCertificateTest` recomputes that hash
and asserts the pacifist choice matches. See
[verification-certificates.md](verification-certificates.md).

## Commands

```bash
python3 -m unittest tests.test_pacifist -v
```

## What it does not do

- Decipher army message Nr. 86.
- Read Kryptos K4.
- Read an unknown script or an undeciphered manuscript.
- Claim that word preference is classical cryptanalysis.

Checked 2026-10-02 (ET).
