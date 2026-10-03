# Chaotic random search

`engine/solvers/chaos_search.py` randomly mutates a Caesar shift or a short
substitution on a known ciphertext. A short substitution is the current shift
plus one to three ciphertext letter overrides, not a full alphabet search.
The walk stops when the English quadgram score per letter beats a fixed
threshold. A fixed seed makes the unit test deterministic. The solver is not
given the key. The test then checks the recovered text against the known
plaintext.

Random search solved that known example only: the Caesar fixture in
`engine/data/caesar_certificate.json` (harbor bell plaintext, shift found by
the search, not supplied). It did not solve army message Nr. 86, Kryptos K4,
or an unknown script.
