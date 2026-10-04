# What others found, and what the digits do with it

Checked 4 October 2026. None of this is a reading of the challenge.

## Sources

- Wikipedia, D'Agapeyeff cipher. Prints the digit block and says the pair index of coincidence is 1.812, while the letter frequencies are too flat for English. Also prints the book's solved Polybius exercise.
- Robert Matthews, archived note (as of 2013). 395 digits, drop the last three, 196 pairs, first digit from 67890 and second from 12345. He cites The Cryptogram (1952 and 1959) and Cryptologia (1978). He reads the flatness as possible suppression of E, not as a solution.
- Nick Pelling, Cipher Mysteries, 27 January 2014. The rare symbols sit in the rightmost column of the 14 by 14 grid. He names 04 and the three 92s as padding and suggests a diagonal flip. That is a location claim, not a plaintext.
- Nick Pelling, Cipher Mysteries, 5 March 2017. The book's double-transposition section follows Kerckhoffs but swaps encryption and decryption. This is a fact about the book's method chapter. It is not, by itself, a fact about the challenge digits.
- Tim Marland, dagapeyeffresearch.com, findings page, 2026. Polybius domain, 14 by 14, missing pairs 61, 73 and 95, pair 81 twenty times, pair IoC about 0.065 in one paragraph and 0.0697 in another, 280 configurations with no coherent plaintext, an ADFGX period-7 spike he later calls an overfitting artefact (28 of 196 positions), Esperanto no better than English, bigram note that may argue against a transposition. He also reports George Lasry as having ruled out simple substitution plus transposition, and Gavin Taylor on the printed keyword SCHUVALOF for SCHUVALOV. Those two are his citations. They were not re-opened here.
- Erik van Eykelen, MsgTrail, 14 March 2026 and later addenda. Same column, and a period-7 story that is the same residue as "column 14" once you are already on a width of 14. Esperanto words are his solver's output. He still calls the cipher unsolved.
- Billy Snider, comment on Pelling's 2014 post, 1 October 2026. Rare-pair concentration, stated as about 9e-10 from 10,000 permutations, and four semantic readings of the column (date, coordinate, checksum, position) that failed. A draw of 10,000 cannot resolve a probability near 1e-9. The exact count is below.
- Unadopted solution posts seen the same day: a September 2026 forum pipeline with a long letter string, and a December 2025 Zenodo paper claiming a British air-defense message. Transposition does not change letter counts. A one-for-one reading of these 18 symbols still has chi-square 34.23, and 0 of 2,000 English strings of that length were that flat. Those posts are not used.

## What the digits say back

The legal square has 25 cells. Eighteen appear. The seven absences are 61, 73, 95, 01, 02, 03 and 05. Marland's three missing pairs are real, and so is the rest of the 0-row: 04 is the only pair in that row, and it appears once.

The pair index of coincidence is 0.069702, which is 1.8122 on the scale Wikipedia prints. That number is unchanged by relabeling the pairs and unchanged by any transposition. Repeating it across 280 alphabets is one measurement, not 280. It says the counts are uneven. It does not say they match English. The English-shaped score on the same counts remains 34.23.

Every symbol that appears once (04, 71, 94) sits in column 14. Exact probability if those three cells were placed at random: 2.946e-4. Every symbol that appears at most twice does too (add 93). Exact probability for those five cells: 8.744e-7. Pelling's own pair, 04 and 92, is four cells, all in that column, probability 1.679e-5. This is the part of the outside work that holds.

It is not a padding column. Eight of its fourteen cells are ordinary frequent pairs (62, 64, 74, 83, 84, 85, and two more of the common ones in that list). Deleting column 14 leaves 182 cells with score 45.57, the worst of the fourteen columns. The friendliest column to delete scores 26.23. Against 200 English strings of length 182, 0 were that flat. Stripping the famous column does not uncover English counts.

No letter string is stored.
