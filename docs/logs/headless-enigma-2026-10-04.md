# Headless army Enigma, 4 October 2026

Not solved. No daily key was invented.

`engine/headless_enigma.py` is the repo's three-rotor Enigma I with the clerk's procedure and nothing else. You set the day's rotors, rings, and plugboard. You give it the Grundstellung and the enciphered message setting. It returns the three-letter start, then the body. A dash steps the wheels once and stays a hole. The machine does not score the letters and does not fill a hole.

The Wikipedia check still types `AAAAA` and gets `BDZGO`. A hole in the middle of a four-letter message still lets the last two letters come out in the right place, so the wheels did step.

The 5 July control runs before any open message. Ground `AIK` and second group `SUD` give start `WER`. The first 20 body letters are `BETRIEBSSPRUQXKUPPLU`. That is the known Betriebsspruch prefix, garble included. Its mean Grimm score is -3.3563.

The open messages tried on the published keys for 1 July and 5 through 9 July:

| Message | What was fed | Result |
| --- | --- | --- |
| KLJBO, Nr. 87, 3 July | Ground `RGN`, second `KUI`, 50 slots with 4 holes | Six starts. Not scored. A hole is not a German letter. |
| LXACA, Nr. 100, 5 July | Ground `OGD`, second `PKN`, 20 letters | 5 July start is `LXI`, the same window as the earlier neighborhood. None of the six scores beat the control. |
| JBIYH, Nr. 242, 20 July | Ground `BSB`, second `NTK`, 55 letters | Six starts. None beat the control. |

Zero of the 18 rows beat the control. The 3 July key and the 20 July key are not on the key page, and this pass does not search stand-ins for them. June messages EHSTQ, AFKZT, and RXPSB are not in this run: the June message page returned 404, and their groups were not copied from memory. BYQMZ, FKQLZ, and XFEDT are the Ultimate challenge, whose wiring the publisher questions. This machine is ordinary Enigma I with reflector B, so it was not aimed at them.

`solved` stays false and `claimed_plaintext` stays null.
