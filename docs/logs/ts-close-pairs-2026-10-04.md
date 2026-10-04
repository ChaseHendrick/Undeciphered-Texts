# Truppenschlüssel pairs, 4 October 2026

Not solved. No plaintext claimed. No square was searched.

The letters are the groups printed on the [failure page](https://cryptocellar.org/bgac/g-army-ts-messages.html), updated 27 July 2026. The metadata ledger still stores none of them. This note is only the three pairs that share a designator, a clock time, or an ending.

## IASRZ, 8 July, Nr. 129 and Nr. 130

Same station, 4fc. Both printed strings start `IASRZEDSTB`, 10 letters. The form lengths are 90 and 52, and those counts include the designator. After the designator the bodies are 85 and 47 letters, both odd. The two-square solver refuses an odd length, and these bodies were not padded. The shared body prefix that remains is `EDSTB`.

## DSZPZ and DEZPS, 4 July, both headed 1735

Nr. 96 has 62 letters. Nr. 97 prints `RQMX-`, so one slot is unknown and the known letters are 59 against a form length of 60. The dash was not filled in. Comparing the known bodies with no gaps gives 11 matches in 53 positions. A random J-free string of that length, 20 draws, seed 20261004, aligns to at most 15 letters. The real alignment keeps 33. That is above the control. It is not an identity, so this is not a clean retransmission and it is not a key.

## SSKFV and HOHOX, 6 July, Nr. 109 and Nr. 110

Same station, f8y, form times 2232 and 2248. The printed strings end in `LMOTIYIZ`, 8 letters, which is longer than the shared final group `TIYIZ`. SSKFV has 60 letters, matching its form length. HOHOX prints 55 letters against a form length of 50. The extra letters are left as printed. No group was dropped to force the form length.

## What this does not do

Identical ciphertext under one key would be identical plaintext, but no key was tried. A later reading of one message in a pair would bear on the other only at the letters that actually agree. `solved` stays false and `claimed_plaintext` stays null.
