# Truppenschlüssel residue, counted 4 October 2026

This is the table requested by [next.md](next.md) item 1. It counts the public failure page. It does not attack a message and it does not publish plaintext.

Source page: [German Army TS Messages](https://cryptocellar.org/bgac/g-army-ts-messages.html), updated on 27 July 2026, read on 4 October 2026. The page meta description says the collection contains 41 ciphertext messages. The cipher is the double Playfair described by Ostwald and Weierud, [Modern Cryptanalysis of the Truppenschlüssel](https://cryptocellar.org/pubs/mcts.pdf). J is not in the ciphertext alphabet. A received J is an error, most often P or Y, sometimes W or O.

Counting rule: a row is live residue only when that entry has no "Broken on" line. Form length is the integer printed as "- N -" on the preamble. Reception time is the Uhr field. Form time is the leading time on the preamble. The ledger stores neither ciphertext nor plaintext. The checker is `engine.truppenschluessel_residue`.

## Count

| Set | Count |
| --- | --- |
| Listed on the page | 41 |
| Marked Broken on 22.01.2022 | 10 |
| Marked Broken on 26.01.2022 | 1 |
| No break date, live residue | 30 |

The June heading says eight messages. One has no break date (YSGSS) and seven are marked broken. That matches the heading. The paper's older residue of 42 included messages this page now marks broken. A count that ignores the break dates will overstate the live set.

## Live residue

| Date | Nr | Indicator | Direction | Reception | Form time | Form length | J note | Relation or transcription note |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1941-06-28 | 56 | YSGSS | incoming | 2251 | 2215 | 90 | no | Short header. Form length does not match the visible letters. A group contains a dash. |
| 1941-07-03 | 84 | FCVHR | incoming | 1003 | 0957 | 64 | no | |
| 1941-07-03 | 85 | HKMZI | incoming | 1140 | 1125 | 140 | no | Facsimile linked. |
| 1941-07-03 | 86 | FBOIQ | incoming | 1435 | 1425 | 46 | no | Not Funkspruch Nr. 86. |
| 1941-07-04 | 88 | TKYKJ | incoming | 0300 | 0130 | none | erroneous J in the first group | Preamble is "0130 - mtc 2 km 40 -". Dashes inside groups. |
| 1941-07-04 | 90 | KVLIG | incoming | 0850 | 0835 | 98 | no | Dash inside a group. |
| 1941-07-04 | 91 | SGOXX | incoming | 1010 | 0910 | 88 | no | Same reception minute as UBYVQ. |
| 1941-07-04 | 92 | UBYVQ | incoming | 1010 | 0835 | 126 | no | Same reception minute as SGOXX. Form times differ. |
| 1941-07-04 | 94 | HFEYY | incoming | 2110 | 1930 | 148 | no | Five-dash gap in the ciphertext line. |
| 1941-07-04 | 95 | LICUD | incoming | 2017 | 1650 | 74 | erroneous J in the eighth group | Facsimile linked. |
| 1941-07-04 | 96 | DSZPZ | incoming | 2024 | 1735 | 62 | no | Same form time as DEZPS. Reception times differ. |
| 1941-07-04 | 97 | DEZPS | incoming | 2028 | 1735 | 60 | no | Same form time as DSZPZ. Dash inside a group. |
| 1941-07-06 | 109 | SSKFV | incoming | 2242 | 2232 | 60 | no | Same final five-letter group, TIYIZ, as HOHOX. |
| 1941-07-06 | 110 | HOHOX | incoming | 2350 | 2248 | 50 | no | Same final group as SSKFV. Visible uppercase run is longer than 50. |
| 1941-07-08 | 121 | IABZV | incoming | 0735 | 0712 | 48 | no | |
| 1941-07-08 | 123 | EHNPZ | incoming | 1458 | 1450 | 87 | no | |
| 1941-07-08 | 129 | IASRZ | incoming | 2039 | 2025 | 90 | no | Same indicator as Nr. 130. |
| 1941-07-08 | 130 | IASRZ | incoming | 2334 | 2330 | 52 | no | Same indicator as Nr. 129. |
| 1941-07-12 | 193 | XWFEC | incoming | 1140 | 1130 | 98 | no | |
| 1941-07-13 | 26 | AFUVO | outgoing | 2132 | 2030 | 14 | no | Too short for a unique plaintext. |
| 1941-07-23 | 252 | DOLHA | incoming | 1945 | 1923 | 70 | no | |
| 1941-07-25 | 263 | CPUDN | incoming | 0050 | 0035 | 32 | no | |
| 1941-07-25 | 264 | NEUEM | incoming | 1233 | 1229 | 74 | no | |
| 1941-07-26 | 268 | LSSLG | incoming | 1033 | 2330 | 68 | no | Reception time and form time are printed on different clocks. |
| 1941-07-29 | 281 | CFQIB | incoming | 0945 | 0930 | 56 | no | Visible uppercase run is 46 letters. |
| 1941-07-31 | 284 | VHRNE | incoming | 0645 | 0630 | 136 | no | Visible uppercase run is 140 letters. Facsimile linked. |
| 1941-08-10 | 8 | ZUBZE | outgoing | 1142 | 1125 | 62 | no | Facsimile linked. |
| 1941-08-17 | 21 | MZXNX | outgoing | none | none | 88 | no | No Uhr field in the extracted header. |
| 1941-09-05 | 31 | AAXYN | outgoing | 1113 | 1055 | 72 | no | Facsimile linked. |
| 1941-09-23 | 91 | AOXST | outgoing | 1533 | 1420 | 152 | no | Visible uppercase run is 168 letters. Facsimile linked. |

## Already marked broken

These stay on the failure page, but they are not live residue. Ten are marked "Broken on 22.01.2022": SGNGI 62, CEFDC 63, DSGPZ 64, VGNZE 66, MXWQP 68, CEIXC 69, DUESE 70, JBTVE 245, BNZIM 246, BOFXE 248. One is marked "Broken on 26.01.2022": TUNYA 21 of 20 August 1941. CEIXC has a page note that a whole group is missing after the indicator. DUESE has a page note of two erroneous J letters in the last group. JBTVE has J in the indicator.

## What this does not do

No key was searched. No plaintext is claimed. AFUVO at 14 letters cannot be a unique double-Playfair reading. A shared indicator, a shared minute, or a shared final group is a lead for a later sourced attack, not a result. Existing two-square checks remain the published Fig. 6 pair and the synthetic keyword search. They are not a reading of this residue.
