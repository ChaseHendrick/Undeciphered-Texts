# Headless Truppenschlüssel, 4 October 2026

Not solved. No square was chosen for an unsolved message.

The Enigma machine from the previous note does not open these. They are the pencil cipher: two 5×5 squares, J left out. `engine/headless_truppenschluessel.py` is that machine with the same rule as the headless Enigma. A dash occupies one slot and stays a hole. J is treated the same way, instead of being quietly turned into I and sliding every later pair. An odd leftover letter is a hole. The machine will not pad with X.

A planted pair of squares, built from the keywords `FELD` and `POST`, seals `ABCDEF` and feeds it back to the same six letters. The intact pairs are re-sealed and match. A dash or a J in the third slot spoils only that pair, and the re-seal of the other two pairs still matches. The pairs on either side still come back as `AB` and `EF`.

The six residue messages already in the repo, IASRZ 129 and 130, DSZPZ, DEZPS, SSKFV, and HOHOX, have no printed squares. The machine records them as blocked and does not open them.

M-209 was not given a second headless wrapper. `engine/solvers/m209.py` is already a known-key machine, and none of the open army messages in this set are M-209. The Ultimate Enigma messages were not given a custom-wiring machine. No alternative wiring is printed, and inventing one would be the same mistake as inventing a missing daily key.

`solved` stays false and `claimed_plaintext` stays null.
