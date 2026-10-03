# Simplex five-button combination enumerator

This note records a published count of the combinations on a five-button
Simplex lock (the 9600 style in the source). It is checked against the
factory default that the same page names. It is not instructions for a
specific physical lock and not a claim about Nr. 86.

## Source

Patrick Ekman, "Simplex Lock Combinations" (31 July 2024):

https://ekman.cx/articles/simplex_locks/

Fetched 2026-10-02. The page says a first glance, using each of the five
buttons once and never together, is 120 combinations (5 factorial). The
published rules also allow codes that use fewer buttons, and presses of
two or more buttons at the same time, with each button used at most
once. Eighteen patterns are tabulated. Their sizes sum to 1081.

The same page names the factory default `2+4, 3`: buttons 2 and 4
together, then button 3.

## What the certificate stores

The enumerator in `engine/solvers/simplex_lock.py` builds that set of
1081 strings. The certificate at
`engine/data/simplex_lock_certificate.json` stores the method name, the
combination string `2+4, 3`, the candidate count 1081, the source URL,
and the SHA-256 of the string `2+4, 3`.

## What this does not do

The code lists the published button combinations. It does not describe
how to operate a physical lock, and it does not say anything about
army message Nr. 86 or any other undeciphered text.
