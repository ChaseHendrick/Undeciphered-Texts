# What to research next

Date: 2 October 2026 (ET). Ranked by what a careful newcomer can check against a public source, not by fame. Nothing here is a decipherment. Pair with [closest.md](closest.md) and the refusal list at the bottom.

## Queue

### 1. Live Truppenschlüssel residue, counted, not attacked in this repo

**Why.** Ostwald and Weierud, *Cryptologia* (published online 2022; author PDF [cryptocellar.org/pubs/mcts.pdf](https://cryptocellar.org/pubs/mcts.pdf)), recovered 94 of 136 German Army Truppenschlüssel messages from the 1941 collection. Seven of those 94 used a plaintext-ciphertext compromise. They left **42** unsolved on purpose: lengths 14 to 152 letters, mean 77. Causes they name: bad plaintext, garbles, enciphering errors, short messages. The cipher is a double Playfair (two 5×5 squares). J is not in the ciphertext alphabet; plaintext J is written II. An erroneous received J is usually P or Y, sometimes W.

The public “failed” page was updated **27 July 2026** and still mixes later breaks into the old list: several June and July items are marked “Broken on 22.01.2022” or “26.01.2022” in the body. A count that ignores those dates will overstate the residue. Entries with no break date on that page, read 2 October 2026, are the live problem. Designators and the length printed on the form: YSGSS (short header), FCVHR 64, HKMZI 140, FBOIQ 46, TKYKJ (garbled J), KVLIG 98, SGOXX 88, UBYVQ 126, HFEYY 148 (a dashed gap), LICUD 74 (erroneous J), DSZPZ 62 and DEZPS 60 (both timed 1735 on 4 July, similar groups), SSKFV 60 and HOHOX 50 (both end in the same five letters), IABZV 48, EHNPZ 87, IASRZ 90 and IASRZ 52 (same indicator), XWFEC 98, AFUVO **14**, DOLHA 70, CPUDN 32, NEUEM 74, LSSLG 68, CFQIB 56, VHRNE 136, ZUBZE 62, MZXNX 88, AAXYN 72, AOXST **152**. That is 30 lines. The paper’s 42 included the ones later marked broken. Long failures (HKMZI 140, HFEYY 148, VHRNE 136, AOXST 152) show that length is not the only cause.

**Do.** A table: designator, date, stated length, whether a J is marked, whether a sibling on the same minute exists, whether the page has a “Broken on” date. Stop there.

**Do not.** Publish a plaintext. Hill-climbing the 14-letter AFUVO message cannot be unique. Dunin and others’ later Playfair work is a *suggested* next attack in the paper, not a result.

**Data.** [g-army-ts-messages.html](https://cryptocellar.org/bgac/g-army-ts-messages.html) · [1941 message list](https://cryptocellar.org/bgac/1941-msg-list.html) · [mcts.pdf](https://cryptocellar.org/pubs/mcts.pdf). Enigma is a different column: the FMNGI note says that of nearly 1,000 Enigma and TS messages, seven Enigma messages plus the WEUWY puzzle remained when that page was written ([the-fmngi-break.html](https://cryptocellar.org/bgac/the-fmngi-break.html)).

### 2. DECODE metadata audit

**Why.** The corpus is the right place for a newcomer who wants a real ciphertext in a known language. Sizes, so the audit has a baseline:

| Date | What was public | Source |
|---|---|---|
| 2016 | Development release, a few hundred manuscripts | Héder and Megyesi, HistoCrypt 2022 |
| 2019 | First full release, nearly 1,000 records | Megyesi, Blomqvist, Pettersson, HistoCrypt 2019 |
| 4 April 2022 | **2,939** records: 1,272 ciphertexts (44%), 1,667 keys (56%); 18,788 images, 128 GB | [HistoCrypt 2022 paper](https://ecp.ep.liu.se/index.php/histocrypt/article/view/397) |
| 2024 project summary | “over 8,000” encrypted sources | [Megyesi, SLTC 2024 abstract](https://sltc2024.github.io/abstracts/megyesi.pdf) |
| DECODE2LOD write-up | Knowledge graph from **9,390** records (25,970 nodes, 115,303 edges); the live collection called nearly 10,000 | Cited from that paper’s own description; confirm the PDF before you quote the graph as current |

Keys outnumber ciphertexts in the 2022 cut because early-modern keys survived more often than the letters. A key without its ciphertext, and a ciphertext with no transcription, are different jobs.

**Do.** Export the public table from [decrypt-web/RecordsList](https://www.de-crypt.org/decrypt-web/RecordsList) (CSV is a documented feature of the 2022 interface). Count ciphertext vs key vs “decrypted” vs not. Record the fetch date in the CSV header. HistCorp n-gram models are the language side (Pettersson and Megyesi 2018); the 2024 abstract says they were wired into CrypTool.

**Do not.** Treat a decrypted Vatican nomenclator as training for Linear A.

### 3. Kryptos K4: archive versus cryptanalysis

**Why.** Headlines in September 2025 said the sculpture was solved. The people who found the papers say it was not a decryption.

Facts with dates:

- The CIA sculpture (1990) has four ciphertexts, 869 characters in the usual public count. K4 is 97 letters beginning OBKR. K1-K3 were read inside CIA by David Stein in 1998 and published by Jim Gillogly in 1999 ([FAQ](https://elonka.com/kryptos/faq.html)). In 2006 K2’s public ending was corrected to “X LAYER TWO” after a missing ciphertext S ([Dunin](https://www.elonka.com/kryptos/CorrectedK2Announcement.html)).
- Sanborn had released cribs (BERLIN, CLOCK, EASTNORTHEAST / BERLINCLOCK). Cribs are not the method.
- September 2025: Jarett Kobek and Richard Byrne, tipped by an auction listing, photographed Sanborn’s papers at the Smithsonian Archives of American Art. They found scrambled plaintext scraps from 1990 CIA-review copies, not the coding charts. Kobek: there is no way this is a cryptographic solve. Sanborn, quoted by RR Auction and in an open letter reproduced at [numberworld, November 2025](https://www.numberworld.blog/2025/11/jim-sanborn-open-letter.html): “K4 has not been solved or decrypted. The scrambled plain text was found, but without the coding method or key.” The plaintext was still unpublished in that letter. The Smithsonian sealed the files for 50 years. *Scientific American* states the distinction the same way ([found after 35 years](https://www.scientificamerican.com/article/a-solution-to-the-cias-kryptos-code-is-found-after-35-years/), [how it gave up its secret](https://www.scientificamerican.com/article/how-the-cias-kryptos-sculpture-gave-up-its-final-secret/)).
- The auction closed 20 November 2025. A notebook on that page records a winning bid of $770,000; RR Auction’s own post says the archive sold for $962,500. Those can be bid versus total with premium. Do not collapse them into one number without saying which. The lot is the method and an alternate paragraph Sanborn calls K5. The buyer is not a published decryption.
- The system was designed with Ed Scheidt. Method still unpublished.

**Do.** A one-page chronology with those URLs, labeled “plaintext recovered from an archive” versus “cipher solved.”

**Do not.** Reconstruct the plaintext from sealed scans, or claim an AI solve. See [recent-cracks.md](recent-cracks.md).

### 4. PHerc. 1667: what “complete” excludes

**Why.** The June 2026 Vesuvius Challenge announcement is easy to over-read. The preprint defines the words.

**Do.** A coverage sheet, every number from [arXiv:2606.29085](https://arxiv.org/html/2606.29085v1) and [scrollprize.org/firstscroll](https://scrollprize.org/firstscroll): 22 columns, ~860 cm² writing surface, 31 wraps, 1231 cm² papyrus, 33 cm² of columns 1-3 untranscribed, 8 cm of 19-24 cm height, diameter 4.9→2 cm, weight 14 g→~6 g, title not recovered, Stoic *hypothesis* from Aristocreon in column 22 (2nd century BC, not a signed author). Then a second table of rolls that are **not** read: Paris 4 (3D ink confirms the 2023 region only), PHerc. 139 (title Philodemus, *On Gods*, book 8; body not a book), PHerc. 172 (title plus a partial unwrap, [~70% note](https://scrollprize.substack.com/p/70-of-pherc-172-is-now-digitally)), unscanned Naples rolls. Square brackets are not recovered letters.

**Do not.** Run Tesseract on a CT slice and publish Greek. [image-reading.md](image-reading.md).

### 5. Meroitic glosses with a REM number

**Why.** Script since Griffith 1909-1911. Rilly’s lexicon volume presents on the order of **800** entries including debated and rejected ones; a “hell” appendix exists so that Zyhlarz’s glosses are not reused by accident. The UCLA Encyclopedia (2016) still calls the translatable basic vocabulary scanty and lists a short secure set (*qore*, *kdi*, *ato*, *abr*, kinship, a handful of verbs) plus later proposals (*ar*, *dime*, *yer*, *wle*, and others). Funerary texts are about a third of the corpus and are where formulae A-X are actually parsed (Rilly and de Voogt 2012: more than 1,100 texts in REM at that date; the field’s “about 2,000” includes later finds). Verbal morphology is the weak side. Northern East Sudanic (Rilly) versus Afroasiatic phonotactics (Rowan 2006; Lipiński) is unsettled. [UCLA](https://escholarship.org/uc/item/3128r3sw).

The 2025 paper “Towards Ancient Meroitic Decipherment” ([ACL ALP](https://aclanthology.org/2025.alp-1.11.pdf)) is a machine-translation experiment. It says the authors started from 871 examples and, by swapping names, built 1,868 “unique word forms.” Those forms are synthetic. The title is not a result.

**Do.** One gloss, one REM line, the formula slot, the rival gloss that lost.

**Do not.** Cite the 2025 paper as a translation.

### 6. Etruscan: types versus tokens

**Why.** The alphabet is done. Wallace, *Zikh Rasna* (2008): over 10,000 inscriptions, most of them names; Liber Linteus about 1,300 word-forms; Tabula Capuana about 300 words in 60 lines. BMCR on Belfiore (2011): about 1,300 lexemes reduce to about **500** distinct words or roots, and the reviewer does not treat that as 500 known meanings. A popular “about 300 words” figure is a handbook estimate, not Meiser’s *Etruskische Texte* (2014). Van der Meer’s word-by-word Liber Linteus commentary is a commentary. Pyrgi is not a Rosetta Stone. Tyrsenian (Rix: Raetic, Lemnian) is the working comparison. An Anatolian/Indo-European “basic lexicon” argument that assigns IE etymologies to glosses other people proposed is not the consensus, and it is not a new reading.

**Do.** From a named edition, mark each Liber Linteus type as glossed, grammatical, or unknown. Count them.

**Do not.** Force the linen book into Latin.

### 7. Iberian morphology without Basque

**Why.** Northeastern script since Gómez-Moreno (coin names, the Alcoy Greco-Iberian lead, the Turma Salluitana name list). Untermann’s *Monumenta Linguarum Hispanicarum* compiled on the order of a thousand Iberian word-forms (Almagro, interviewed in *El País*, 31 Dec 2022: [english.elpais.com](https://english.elpais.com/culture/2022-12-31/the-incredible-art-of-translating-pre-roman-languages-without-a-rosetta-stone.html)). Almagro’s “we understand 60% of the Iberian words” is explicitly **60% of the words in the texts we have**, not 60% of the language, and it is not the same claim as Moncunill and Velaza’s handbook statement that affiliation is unknown and Basque is not demonstrated ([PDF](https://ifc.dpz.es/recursos/publicaciones/38/77/17moncunillvelaza.pdf)). The Ullastret lead (MLH C.2.3, Hesperia GI.15.04) is 173 characters, 31 word-divisions, fourth century BC. Mnamon still marks the meaning unknown ([SNS example](https://mnamon.sns.it/index.php?id=13&lang=en&page=Esempi)). A numeral reading of *borste abaŕkeborste* is a hypothesis.

**Do.** Segment one long lead in Hesperia, every cut tied to a parallel suffix, no Basque column.

**Do not.** Publish a Basque glossary.

### 8. Independent check of Linear Elamite 2022

Already the conditional rank in [closest.md](closest.md). The next act is a held-out inscription, not another press summary. Proto-Elamite values are not Linear Elamite values.

## Do not bother

These waste the time the queue above would have used. Each has a reason, not a vibe.

| Temptation | Why it fails | Where this is already said |
|---|---|---|
| Dictionary search of Linear A against Hurrian, Luwian, Greek, Semitic | Texts are too short; B-values are conventional; no held-out ideogram test | [starter-projects.md](starter-projects.md), [closest.md](closest.md) |
| A full reading of the Phaistos Disc, Cascajal, Dispilio, or Tărtăria | One text, or no sentences | closest ranks 17-18; Vinča note |
| Indus “alphabet” aimed at the 2025 Tamil Nadu prize | Mean text length has not changed. A prize is not a bilingual | [landscape.md](landscape.md) §4 |
| Basque = Iberian | Tried for decades, not demonstrated | Moncunill and Velaza |
| “AI solved K4” or republishing the Smithsonian scraps | Archive find, method unpublished, files sealed 50 years | this file §3 |
| Re-solving Zodiac Z340, or “solving” Z13 and Z32 | Z340 is done (arXiv:2403.17350). Z13 and Z32 are underdetermined | [recent-cracks.md](recent-cracks.md) |
| Tesseract or a vision model on a Herculaneum heatmap | Ink models are not character models; brackets are not letters | [image-reading.md](image-reading.md) |
| The 2025 Meroitic ACL paper as a translation | Name-swapped synthetic forms | this file §5 |
| Truppenschlüssel under ~20 letters, especially AFUVO at 14 | Not a unique plaintext | Ostwald and Weierud |
| Bletchingley pigeon, Dorabella, Beale B1/B3 as lost history | Codebook missing, or the text is too short, or the hoax question is open | recent-cracks |
| Copying Blackletter into this repo | Private Canvas desk. Screen-reading policy only | [image-reading.md](image-reading.md) |
| Another unsupervised “what language is Voynich” from entropy | Structure is published; a language name is not | Bowern and Lindemann 2021, cited in closest |

If a new tablet, a long bilingual, or a second Cascajal block is published, reopen the row. Until then the row stands.
