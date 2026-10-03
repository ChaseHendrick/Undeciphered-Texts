# Homophonic substitution, fixed temperature (Kopal 2019)

`engine/solvers/homophonic_fixed_temperature.py` is a small version of the homophonic substitution attack in Nils Kopal, "Cryptanalysis of Homophonic Substitution Ciphers Using Simulated Annealing with Fixed Temperature", HistoCrypt 2019, pages 107-116.

Paper URL (fetched 2026-10-02):

https://ep.liu.se/ecp/158/012/ecp19158012.pdf

Year: 2019.

## What was implemented

Section 5.2 maps each ciphertext homophone to a plaintext letter. The key is longer than the observed homophones (length about 1.3 times that count) and the extra slots start as random English letters, with E more likely than X. Search swaps two key entries. Fitness is a sum of natural-log n-gram scores. The paper sums log pentagrams scaled by a user-chosen factor (500000 in their tests). This version sums the repository quadgram log-likelihood and leaves that sum unscaled.

Section 5.3 keeps the temperature fixed. A better score is always kept. A worse score is kept only when `exp(-(current - new) / temperature)` is above 0.0085 and a uniform draw falls under that probability. The paper's reported temperature is 15000 on the scaled pentagram sum. Temperature is a user setting. Here it is 2.0 on the unscaled quadgram sum, which is the same rule on this short fixture.

If 500 proposals do not beat the best key, the last three key letters are replaced. The paper uses a stall of 100 tries on a full sweep of pairs. This small version draws random pairs, so the stall count is 500 proposals.

A final hill climb sets each homophone to the one plaintext letter that most raises the quadgram sum, and repeats while any such edit still helps.

## Fixture

The ciphertext is constructed. It is not a text printed in the paper. The sentence is about a baker on Pine Street. The letter E has two homophones. Every other letter that occurs has one. Homophones are taken in turn so the ciphertext does not depend on a draw. `tests/test_homophonic_fixed_temperature.py` recovers that plaintext with seed 3 and 20000 proposals.

## Verification certificate

`engine/data/homophonic_fixed_temperature_certificate.json` stores the cipher name, plaintext, ciphertext, source URL, year, and the SHA-256 of the plaintext. The certificate test recomputes the hash and checks that the search returns the same letters.

## What it does not do

This does not solve army message Nr. 86. It does not solve Kryptos K4. It does not read an unknown script. It is not a claim about the Zodiac messages, Linear A, the Indus script, the Voynich manuscript, or rongorongo.
