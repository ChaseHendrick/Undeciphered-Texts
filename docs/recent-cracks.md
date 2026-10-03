# Recent and famous cracks, methods that worked

Only cases with public documentation. **No new breaks claimed by this repo.**

## Copiale Cipher (2011)
- **What:** 18th-century German secret-society manuscript (~75k characters), abstract symbols + Roman/Greek letters.
- **Who:** Kevin Knight (USC) with Beáta Megyesi & Christiane Schaefer (Uppsala).
- **Method:** Machine-readable transcription; cluster similar shapes; treat abstract symbols as the real cipher (Roman letters were nulls/red herrings); recover German plaintext (“Ceremonies of Initiation”…).
- **Lesson:** Transcription quality + correct null hypothesis beats guessing.
- **Sources:** https://www.eurekalert.org/news-releases/845343 · https://phys.org/news/2011-10-scientist-mysterious-copiale-cipher.html

## Zodiac Z340 (2020)
- **What:** 340-character cipher mailed by the Zodiac Killer; unsolved ~51 years.
- **Who:** David Oranchak, Sam Blake, Jarl Van Eycke; FBI CRRU confirmed.
- **Method:** Combined **homophonic substitution + transposition**; candidate transposition search + AZdecrypt; cribs (“HOPE YOU ARE”, etc.).
- **Lesson:** Hybrid cipher types need hybrid attacks; community tooling matters.
- **Source:** https://blog.wolfram.com/2021/03/24/the-solution-of-the-zodiac-killers-340-character-cipher/

## Zodiac Z408 (1969), contrast
- Solved quickly by the Hardens as homophonic substitution, shows Z340’s transposition layer was the extra trap.

## German WWII Enigma, hobby / distributed era
- **M4 project (2006):** Stefan Krah + distributed home PCs broke U-boat Enigma traffic that wartime and early hobby efforts had left.  
  Sources: BBC / Times reporting on amateur grids (historical).
- **Crypto Cellar BGAC:** Ongoing break of German Army Enigma messages from archival forms; honours roll of amateur breakers.  
  https://cryptocellar.org/bgac/ · https://cryptocellar.org/bgac/honours-roll.html
- **MVUEH (Sept 2026):** Carter Leffen + GPT-6 Astra; crib from related SIPVX plaintext (ROSENOW); Enigma simulator/bombe search; **validated by Frode Weierud**. Transcription errors and rare left-wheel turnover had blocked earlier attempts.  
  https://www.cryptocellar.org/bgac/the-mvueh-break.html
- **Related 2026 work:** Additional July 1941 messages (e.g. reports around AWTZK/ZNLZT, FMNGI) discussed on Crypto Cellar, always prefer Weierud’s pages over social media alone.

## Mary Queen of Scots letters (2023)
- Lasry, Biermann, Tomokiyo recovered and deciphered lost letters using homophonic/nomenclator cryptanalysis (DECRYPT-adjacent community).  
  Popular coverage: https://edition.cnn.com/2023/02/07/world/mary-queen-of-scots-lost-letters-scn/index.html  
  Research: Cryptologia DOI https://doi.org/10.1080/01611194.2022.2160677

## Kryptos (CIA sculpture)
- **K1-K3:** Solved (Sanborn sculpture; public plaintexts known).
- **K4:** Still unsolved as of public consensus; Sanborn has released cribs (e.g. EASTNORTHEAST, BERLINCLOCK). Treat new “K4 solutions” as unverified unless Sanborn/community consensus agrees.
- **Lesson:** Partial cribs ≠ full break.

## Beale ciphers
- **B2** (Declaration of Independence book cipher) long solved; automatic homophonic-style attacks have recovered B2 in NLP papers.
- **B1 / B3:** Still generally considered unsolved; may be flawed/hoax components. Controversy persists.

## Dorabella Cipher
- Elgar’s 1897 letter to Dora Penny; many proposed solutions, **no consensus**. Short ciphertext → underdetermined.

## Somerton Man (“Tamam Shud”)
- Cipherette/code page remains unsettled as cryptanalysis; identity research (DNA) is a separate track from cipher solution.

## WWII carrier-pigeon message (Bletchingley)
- GCHQ: likely codebook and/or one-time pad; **not decryptable without keying material**. Public “solutions” not accepted.  
  https://www.bbc.co.uk/news/uk-20456782 · GCHQ PDF summary · practicalcryptography.com analysis

## Smithfield / newspaper cryptograms
- Newspaper aristocrats/cryptograms are usually short monoalphabetic or simple puzzles, good **training**, rarely “lost history.” Prefer DECODE for archival substance.

## Pattern across successes
1. Accurate transcription of originals.  
2. Right cipher model (including nulls/transposition).  
3. Language model / cribs / sibling messages.  
4. External validation by domain experts.  
5. Enough ciphertext (or a key leak).


## Cracks and non-cracks added after the first pass

### Silk dress cryptogram (solved 2023, not a murder cipher)

Sara Rivers-Cofield found two sheets of apparent ciphertext in a silk dress. Wayne S. Chan showed they are U.S. Army Signal Service **weather telegrams** for 27 May 1888, using the 1887 weather code. Cryptologia 48(5): 387-426. DOI [10.1080/01611194.2023.2223562](https://doi.org/10.1080/01611194.2023.2223562). NOAA summary: [noaa.gov heritage story](https://www.noaa.gov/heritage/stories/cryptogram-in-silk-dress-tells-weather-story). Klaus Schmeh’s 2017 “top 50” still lists this as unsolved; that page is a snapshot, not a live status: [Cipherbrain top 50](https://scienceblogs.de/klausis-krypto-kolumne/the-top-50-unsolved-encrypted-messages/).

### Kryptos K4 (2025): plaintext found, method not

See the update in [closest.md](closest.md). Do not describe the Smithsonian find as an amateur cryptanalytic solve. K2’s public ending was corrected in 2006 to “X LAYER TWO” after a missing ciphertext S: [Elonka Dunin](https://www.elonka.com/kryptos/CorrectedK2Announcement.html). Gillogly’s public K1-K3 solution was 1999; David Stein at CIA had them in 1998 ([FAQ](https://elonka.com/kryptos/faq.html)).

### Papal ciphers and Mary Stuart’s circle of methods

Lasry, Megyesi, and Kopal, “Deciphering papal ciphers from the 16th to the 18th Century,” Cryptologia 45(6): 479-540 (2021). Hundreds of Vatican ciphertexts, keys recovered with DECRYPT/CrypTool-style search. Mary Stuart’s 57 letters (1578-1584) are the better-known amateur-team paper: Lasry, Biermann, Tomokiyo, Cryptologia 47(2), 2023, DOI [10.1080/01611194.2022.2160677](https://doi.org/10.1080/01611194.2022.2160677). Biermann had earlier solved three of Giovan Battista Bellaso’s 1555 challenges (Cryptologia 2018, DOI [10.1080/01611194.2017.1422050](https://doi.org/10.1080/01611194.2017.1422050)).

### German Army manual ciphers and ADFGVX

- Truppenschlüssel: Ostwald and Weierud, Cryptologia 47(3), author’s copy linked from [cryptocellar.org/bgac/](https://cryptocellar.org/bgac/) and [cryptocellar.org/pubs/mcts.pdf](https://cryptocellar.org/pubs/mcts.pdf). Hill climbing on authentic 1941 German Army hand ciphers; a residue was left unsolved on purpose because the messages are short or corrupt.
- ADFGVX (WWI German field cipher): George Lasry and coauthors published large ciphertext-only recoveries of Eastern Front traffic. A handful of badly garbled 1918 messages are still cited as open. Schmeh’s 2017 list item “about 20 unsolved” is out of date. Do not claim every ADFGVX intercept in the archives is solved.
- Enigma: the M4 distributed project (Stefan Krah) broke naval messages in 2006, including a Scharnhorst message, documented on the Crypto Cellar portal. The September 2026 MVUEH validation is one Army message, not a new machine.

### Linear Elamite (humanists, 2022)

Not an amateur cipher solve and not an AI solve. Cited in [closest.md](closest.md). Proto-Elamite was **not** solved by that paper.

### Zodiac paper trail

The long technical account is Oranchak, Blake, and Van Eycke, arXiv:2403.17350 (2024): [pdf](https://arxiv.org/pdf/2403.17350). Z13 and Z32 remain unsolved because they are underdetermined. The FBI confirmed Z340 in December 2020 after receiving the solution on 5 December (press the following week).

### Still unsolved, so they are not in the “cracks” column

Dorabella, Beale B1/B3, D’Agapeyeff (1939; the author later said he forgot it, and the cipher may be garbled), the WWII Bletchingley pigeon message ([GCHQ](https://www.gchq.gov.uk/information/pigeon-takes-secret-message-grave): no credible public solution without the codebook), Ricky McCormick’s notes (FBI appeal, 2011, still unsolved), Somerton Man’s letters.
