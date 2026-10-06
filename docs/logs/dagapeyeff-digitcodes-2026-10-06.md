# Digit ciphers other than Polybius pairs, 6 October 2026

Not a reading. No letter string is stored.

Without the final 000 the challenge's 392 digits alternate perfectly between two classes: every even place holds one of 6, 7, 8, 9, 0 and every odd place one of 1, 2, 3, 4, 5 ([frames](dagapeyeff-frames-2026-10-04.md)). No key can change that, so `engine.dagapeyeff_digitcodes` uses it against digit ciphers whose codes are not all pairs from two fixed classes. The statistic is the best share of the first 392 digits that alternate between any two classes of five digits; the cells score 1.

For 300 planted held-out English texts per system, each under a random key:

| System | Best share | Reaching 1 |
| --- | --- | --- |
| Straddling checkerboard (eight one-digit letters, two prefix digits) | 0.6505 | 0 |
| Nihilist substitution, keyed square with coordinates 1 to 5, keyword of period 2 to 14, sums 22 to 110 | 0.8469 | 0 |
| The same with coordinates 0 to 4 | 0.7628 | 0 |

A straddling checkerboard mixes one- and two-digit codes, so the classes slip out of step. Nihilist sums of coordinates 1 to 5 never end in 1 and can run to three digits. Neither gives the cells. The Polybius-plus-repeating-digit-key family that keeps the alternation was searched on 2 October ([first inspection](dagapeyeff-2026-10-02.md)) and allows only keys such as 50, 4050 and 5050.

Not a reading. No letter string is stored.
