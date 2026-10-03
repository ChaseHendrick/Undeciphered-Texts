# Where AI and computation have already helped read texts

Honest inventory. “Helped” means a published system improved restoration, transcription, translation, or cryptanalysis of a **known** language or a **known** cipher, or recovered ink from a scan. It does not mean the model discovered a lost language.

Linear A, the Indus script, Rongorongo, the Phaistos Disc, and the Voynich manuscript are **not** on the success list. A 2026 popular article described an amateur Semitic reading of Linear A produced with AI scripts; specialists’ point in that same piece is that a corpus of a few thousand signs and no bilingual will fit many stories. Source: [Phys.org, July 2026](https://phys.org/news/2026-07-code-ai-decipher-ancient-languages.html). Do not repeat that claim as a decipherment. Hauer and Kondrak’s 2016 anagrammed-Hebrew hypothesis for Voynich was not accepted by manuscript specialists; it is a caution, not a result.

## Contrast: Linear B was not an AI result

Michael Ventris, with John Chadwick, showed in 1952-53 that Linear B writes Mycenaean Greek. The work was cryptographic and philological: sign grids, place names, and then language identification. There was no machine learning and no large computer search. It is the calibration case for later papers that **re-predict** Linear B cognates because Greek is already known.

- Chadwick, *The Decipherment of Linear B* (Cambridge).
- Automatic **re-decipherment** experiments below are tests of algorithms on a solved problem. They did not discover that Linear B was Greek.

## 1. Virtual unwrapping and ink detection (Herculaneum)

Known script (Greek). AI finds ink; people read it.

Full writeup: [vesuvius-scrolls.md](vesuvius-scrolls.md).

| Step | What was shown | Source |
|---|---|---|
| Carbon ink is learnable in micro-CT | 3D CNN ink maps on real Herculaneum fragments; no alphabet inside the model | [Parker et al., PLOS One 2019](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0215775) |
| Open aligned dataset | EduceLab-Scrolls: CT of fragments and rolls, labels from spectral photos | [arXiv:2304.02084](https://arxiv.org/abs/2304.02084) |
| First word inside a sealed roll | ΠΟΡΦΥΡΑϹ, Luke Farritor, Oct 2023 | [scrollprize.org/grandprize](https://scrollprize.org/grandprize) |
| 15 partial columns | Nader, Farritor, Schilliger, $700,000, PHerc.Paris 4 | same; code [ScrollPrize/villa ink-detection](https://github.com/ScrollPrize/villa/tree/main/ink-detection) |
| Title of a closed roll | PHerc. 172, Philodemus, *On Vices*, Roth and Nowak, May 2025, $60,000 | [First Title note](https://scrollprize.substack.com/p/60000-first-title-prize-awarded) |
| One damaged roll read continuously | PHerc. 1667 surviving core, ~22 column-bottoms, 2026 preprint | [scrollprize.org/firstscroll](https://scrollprize.org/firstscroll), [arXiv html 2606.29085](https://arxiv.org/html/2606.29085v1) |

Phase-contrast work in 2016 recovered short Greek sequences in PHerc. 375 and 495. That is imaging, not a full read: [Scientific Reports srep27227](https://www.nature.com/articles/srep27227).

What failed: the 2024 prize to read 90% of four scrolls was not won ([archived rules](https://scrollprize.org/2024_prizes)).

## 2. Damaged Greek inscriptions (restoration, not decipherment)

**Ithaca** (Assael, Sommerschield, and colleagues, DeepMind and Oxford), Nature, 9 March 2022.

- Tasks: fill damaged Greek text, attribute a region, and date the inscription.
- Trained on Packard Humanities Institute Greek inscriptions ([inscriptions.packhum.org](https://inscriptions.packhum.org/)), processing code [github.com/sommerschield/iphi](https://github.com/sommerschield/iphi).
- Reported figures: 62% accuracy restoring damaged text alone; historians using Ithaca moved from 25% to 72%; 71% region attribution; dates within 30 years of the ground-truth ranges. Those are the paper’s metrics on held-out Greek, not a promise about a new find with no parallel.
- Used to revisit the dates of some 5th-century BCE Athenian decrees.
- Code and weights: [github.com/google-deepmind/ithaca](https://github.com/google-deepmind/ithaca). Interface: [ithaca.deepmind.com](https://ithaca.deepmind.com/).
- Paper: [Nature s41586-022-04448-z](https://www.nature.com/articles/s41586-022-04448-z). DOI [10.1038/s41586-022-04448-z](https://doi.org/10.1038/s41586-022-04448-z). Lab note: [DeepMind](https://deepmind.google/blog/predicting-the-past-with-ithaca/).

Ithaca does not read an unknown script. The alphabet and language are known; the model proposes letters that fit Greek epigraphic context. Historians still accept or reject each restoration.

**Pythia** is the earlier restoration-only model from the same line of work: Assael, Sommerschield, Prag, EMNLP 2019, [aclanthology.org/D19-1668/](https://aclanthology.org/D19-1668/).

DeepMind has said the same architecture could be retrained on other ancient languages, including Akkadian or Mayan. That is a plan, not a published decipherment of those corpora.

## 3. Cuneiform and Akkadian (known languages)

Cuneiform is deciphered. The bottleneck is specialist labor: sign photos, polyvalent readings, and translation.

### Sign finding

- **Dencker, Klinkisch, Maul, Ommer**, “Deep learning of cuneiform sign detection with weak supervision using transliteration alignment,” PLOS One 2020. DOI [10.1371/journal.pone.0243039](https://doi.org/10.1371/journal.pone.0243039). Detects signs; does not translate.
- **DeepScribe** (University of Chicago / ISAC Persepolis Fortification Archive): localizes and classifies **Elamite** Achaemenid signs. Reported on their test setup: RetinaNet localization mAP 0.78, ResNet top-5 classification 0.89, end-to-end top-5 0.80. Suggestions for scholars, not an automatic edition. Paper: [arXiv:2306.01268](https://arxiv.org/abs/2306.01268).

### Sign to reading

- **Akkademia** transliterates Unicode cuneiform to sign readings (HMM, MEMM, BiLSTM) on RINAP Neo-Assyrian royal inscriptions. The repository reports 89.5% / 94% / 96.7% accuracy for those three models **on the corpora they were trained on**. Other periods are weaker. This is not English translation. Code: [github.com/gaigutherz/Akkademia](https://github.com/gaigutherz/Akkademia) and [github.com/DigitalPasts/Akkademia](https://github.com/DigitalPasts/Akkademia).

### Akkadian to English

- Gutherz, Gordin, Sáenz, Levy, Berant, “Translating Akkadian to English with neural machine translation,” PNAS Nexus 2(5), 2023, pgad096. DOI [10.1093/pnasnexus/pgad096](https://doi.org/10.1093/pnasnexus/pgad096). Open copy: [PMC10153418](https://pmc.ncbi.nlm.nih.gov/articles/PMC10153418/).
- They report BLEU-4 of **36.52** (cuneiform to English) and **37.47** (transliteration to English), above a translation-memory baseline. Best on short and medium sentences. BLEU in the mid-30s is a draft aid, not a publishable translation. The authors describe a human-machine pipeline (the “Babylonian Engine”), not a replacement for an Assyriologist.

Proto-Elamite and Linear Elamite are different problems. Linear Elamite’s 2022 sign readings (Desset and colleagues, *Zeitschrift für Assyriologie*) are philological, not a neural translation. Proto-Elamite remains mostly unread except for numerals. Do not cite Akkademia or DeepScribe as progress on Proto-Elamite.

## 4. Maya glyphs (classification aids; the script is already largely read)

Classic Maya writing was deciphered by epigraphers across the late 20th century (Knorozov’s phonetic insight, then Houston, Stuart, and many others). Neural nets here **sort pictures of known signs**. They do not assign new phonetic values.

Idiap / MAAYA project (Gülcan Can, Jean-Marc Odobez, Daniel Gatica-Perez):

- CNNs on codex glyphs. A sketch-specific network trained from scratch reached about **70.3%** average accuracy on a **150-class** task, which is well above chance and well below a reliable cataloguer. [ACM JOCCH abstract](https://dl.acm.org/doi/10.1145/3230670).
- Crowd segmentation produced a set of over 9,000 glyphs in 291 categories from the three surviving codices. Transfer learning beat hand-built shape descriptors. [Can et al., IEEE TMM 2017 PDF](https://publications.idiap.ch/attachments/papers/2017/Can_IEEETMM_2017.pdf).
- The project’s own limit: too few examples, so a net can memorize the codices and miss real variants. [Gatica-Perez, MAAYA overview PDF](https://publications.idiap.ch/downloads/papers/2017/Gatica-Perez_INAH-REDTDPC_2017.pdf).

Use these tools to retrieve parallels. Do not use them to “read” an undeciphered inscription such as the Cascajal block or a disputed Isthmian text.

## 5. OCR and handwriting recognition of historical documents

The language and script are known. The model transcribes pixels. This is the largest practical win.

| System | Role | URL |
|---|---|---|
| Transkribus | HTR for handwriting and historical type (Fraktur, Kurrent, and many other models). Layout plus text. Not a decipherment engine. | https://www.transkribus.org/ and https://www.transkribus.org/handwriting-ocr |
| Kraken | Open-source layout analysis and recognition, used for print and manuscript OCR | https://github.com/mittagessen/kraken |
| eScriptorium | Web transcription UI commonly paired with Kraken | https://gitlab.com/scripta/escriptorium |
| Tesseract | General OCR; usable on clean historical print, weak on most handwriting | https://github.com/tesseract-ocr/tesseract |

A 2026 HistoCrypt paper trains TrOCR to map **Copiale cipher line images** straight to German plaintext, after pretraining on IAM, CVL, RIMES, and EU27. That is supervised image-to-text on a **cipher that was already solved in 2011**. It does not crack a new manuscript. Code: [github.com/leitro/Decipher-from-Pixels-Copiale](https://github.com/leitro/Decipher-from-Pixels-Copiale).

## 6. Computational cryptanalysis of known cipher types

These systems search keys for ciphers whose family is understood (substitution, homophonic, transposition, Enigma). They are not ancient-script models. Several of the decisive programs are hill climbing or simulated annealing rather than deep nets. They belong in this file because they are the computational half of recent “reads.”

### Copiale, 2011 (statistical NLP, not a modern LLM)

Kevin Knight, Beáta Megyesi, and Christiane Schaefer transcribed a mid-18th-century manuscript (~105 pages, ~75,000 characters, on the order of 90 cipher types) and showed that the Roman letters were spaces/nulls and the abstract symbols carried German. The text is an Oculist lodge ritual. Paper: [ACL Anthology W11-1202](https://aclanthology.org/W11-1202/) (pdf [W11-1202.pdf](https://aclanthology.org/W11-1202.pdf)). Project copies: [Stockholm University project page](https://www.su.se/english/research/research-catalogue/research-projects/d/decipherment-of-historical-manuscripts/the-copiale-cipher). Press writeup with the null-letter story: [Uppsala, 27 Oct 2011](https://www.uu.se/en/news/2011/2011-10-27-language-scholars-solved-18th-century-cipher).

### Automatic attacks on substitution and homophonic ciphers

| Paper | What it actually did | URL |
|---|---|---|
| Ravi and Knight, EMNLP 2008, integer programming for 1:1 substitution with low-order n-grams | Exact search on a classical problem, not a lost script | [aclanthology.org/D08-1085/](https://aclanthology.org/D08-1085/) |
| Ravi and Knight, ACL 2011, Bayesian homophonic decipherment | First published **fully automatic** solve of Zodiac **Z408**, a cipher amateurs had solved in 1969. Did **not** solve Z340 | [aclanthology.org/P11-1025/](https://aclanthology.org/P11-1025/) |
| Nuhn, Schamper, Ney, ACL 2013, beam search for substitution | Better symbol error on substitution benchmarks than the 2011 Bayesian system (they report 2.0% vs 2.2% in one comparison) | [aclanthology.org/P13-1154/](https://aclanthology.org/P13-1154/) |
| Snyder, Barzilay, Knight, ACL 2010 | Statistical cognate model; Ugaritic aligned to Hebrew. Ugaritic was already deciphered in 1929. This is a method test | [aclanthology.org/P10-1107/](https://aclanthology.org/P10-1107/) |
| Berg-Kirkpatrick and Klein, EMNLP 2011 | Coordinate descent over alphabet and lexicon matchings; same family of tests | [aclanthology.org/D11-1029/](https://aclanthology.org/D11-1029/) |
| Luo, Cao, Barzilay, ACL 2019, neural minimum-cost flow | +5.5 points absolute on noisy Ugaritic-Hebrew cognate ID vs prior work; **67.3%** of Linear B-Greek cognates on their names subset. Again a solved language | [aclanthology.org/P19-1303/](https://aclanthology.org/P19-1303/) |
| Knight, Nair, Rathod, Yamada, COLING-ACL 2006 | Unsupervised EM-style analysis for decipherment problems | [aclanthology.org/P06-2065.pdf](https://aclanthology.org/P06-2065.pdf) |

Code that implements the classical search, not those papers line-for-line:

- [github.com/jameslyons/pycipher](https://github.com/jameslyons/pycipher), encrypt/decrypt classical ciphers (Caesar, Vigenère, ADFGVX, Enigma). It does not break them. Docs: [pycipher.readthedocs.io](http://pycipher.readthedocs.io/en/master/).
- [github.com/theikkila/substitution-cipher-SA-solver](https://github.com/theikkila/substitution-cipher-SA-solver), simulated annealing with trigram scores.
- [github.com/perrygeo/simanneal](https://github.com/perrygeo/simanneal), the generic Python annealer people wrap around a substitution fitness function.
- [github.com/Nickory/SABCA---Simulated-Annealing-Based-Cipher-Analysis](https://github.com/Nickory/SABCA---Simulated-Annealing-Based-Cipher-Analysis), monoalphabetic annealing.
- [github.com/doranchak/azdecrypt](https://github.com/doranchak/azdecrypt), Jarl Van Eycke’s hill climber (homophonic, transposition, many hybrids). This is the tool that made the 2020 Z340 search practical.
- [github.com/matthewdgreen/decipher](https://github.com/matthewdgreen/decipher), annealing stack aimed at historical manuscripts, including a Copiale benchmark route.
- [github.com/CrypToolProject/CrypTool-2](https://github.com/CrypToolProject/CrypTool-2) and [CrypToolProject/CTTS](https://github.com/CrypToolProject/CTTS), the academic historical-cipher workbench (Lasry and the CrypTool group). CTTS was used on the Mary Stuart letters.

### Human-plus-solver historical breaks (computation required, neural nets optional)

Documented in [recent-cracks.md](recent-cracks.md). Short list so this file is complete:

- Zodiac Z340, December 2020: Oranchak, Blake, Van Eycke; homophonic substitution **plus** a two-step transposition; AZdecrypt; FBI confirmation. Not a neural net. [Wolfram writeup](https://blog.wolfram.com/2021/03/24/the-solution-of-the-zodiac-killers-340-character-cipher/), paper [arXiv:2403.17350](https://arxiv.org/pdf/2403.17350).
- Mary Stuart letters, Cryptologia 2023: Lasry, Biermann, Tomokiyo. DOI [10.1080/01611194.2022.2160677](https://doi.org/10.1080/01611194.2022.2160677).
- German Army Enigma and the Truppenschlüssel: Ostwald and Weierud, hill climbing. Portal [cryptocellar.org/bgac/](https://cryptocellar.org/bgac/). Truppenschlüssel paper linked there (Cryptologia 47(3), 2023 e-print 2022).
- September 2026: Frode Weierud validated Carter Leffen’s break of the long-standing MVUEH Enigma message (10 July 1941). Weierud writes that GPT-6 Astra, directed by Leffen, built a simulator and bombe and used the crib ROSENOW from a sibling message. One message, known machine, sibling crib, expert validation. It is not a general Enigma breaker and it is not an ancient-script result. [cryptocellar.org/bgac/the-mvueh-break.html](https://www.cryptocellar.org/bgac/the-mvueh-break.html).

## 7. What has not happened

| Claim you will see online | Status |
|---|---|
| AI solved Linear A | No accepted decipherment. Corpus too small, language unknown. |
| AI solved Voynich | No. Statistical structure is published (Bowern and Lindemann, *Annual Review of Linguistics* 2021: [journal page](https://www.annualreviews.org/content/journals/10.1146/annurev-linguistics-011619-030613)). Structure is not a translation. |
| AI solved Indus | Rao et al., *Science* 2009, showed conditional entropy closer to linguistic systems than to some non-linguistic controls ([science.org](https://www.science.org/doi/10.1126/science.1170391), pdf [Rao](https://homes.cs.washington.edu/~rao/ScienceIndus.pdf)). That is evidence about **type of system**, not a reading. |
| AI solved Rongorongo | Computational syllabic tests exist (e.g. [LT4HALA 2026](https://aclanthology.org/2026.lt4hala-1.16.pdf)). No accepted continuous reading. [rongopy](https://github.com/jgregoriods/rongopy) states that its own mapping experiments were not an acceptable decipherment. |
| Neural “decipherment” of Ugaritic or Linear B | Method papers on languages deciphered decades earlier. |
| Kryptos K4 “solved by AI” | In 2025 journalists found plaintext scraps in Sanborn’s Smithsonian papers. Sanborn said that was not a decryption. The method is still unpublished. See [recent-cracks.md](recent-cracks.md). |

## How to read a new paper in this area

1. Is the script already deciphered, or is the cipher type already known?
2. Is there an independent test set the authors did not tune on?
3. Are the metrics restoration accuracy, BLEU, or sign classification, rather than “we found a sentence we like”?
4. Did a domain expert accept the reading against an image or a known parallel?
5. If the only evidence is a generated translation of Linear A, Indus, or Voynich, stop. The missing bilingual is not supplied by a language model.
