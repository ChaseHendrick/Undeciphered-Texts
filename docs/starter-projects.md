# Starter projects: open targets with real data

These are jobs that can be started from public sources. Each one says what **done** looks like. Done is never “a translation of an undeciphered script.” If a project tempts you to publish a reading of Linear A, Indus, rongorongo, Phaistos, Byblos, Cascajal, Voynich, or Rohonc, it has left the rails. See `methods.md`.

Unofficial GitHub dumps are listed only as **derivatives**. The edition is the museum, the print corpus, or the maintained database.

Difficulty is relative: A = a careful student with the linked files can finish a useful artifact; B = needs epigraphic judgment and more reading; C = needs a specialist collaborator or unpublished images.

---

## A. Aegean and Cyprus

### A1. SigLA length and damage audit (Linear A)

**Do.** For every document in SigLA, record sign-count, object type (tablet, roundel, sealing, stone, metal, pottery), and how many signs are marked uncertain. Publish the histogram. Compare the total to the often-quoted 1,427 documents / ~7,400 signs (Petrolito et al. 2015) and explain the gap. Do not “fix” the gap by inventing inscriptions.

**Why.** Almost every computational paper cites a single corpus size. The size is an editorial choice.

**Done.** A table: document id, site, support, token count, uncertain tokens, and a one-paragraph reconciliation with GORILA’s scope.

**Data.** https://sigla.phis.me/ and https://sigla.phis.me/browse.html and https://sigla.phis.me/map.html  
Background counts: https://aclanthology.org/W15-3715.pdf  
Script-type primer (so you do not treat B-values as facts): https://mnamon.sns.it/index.php?id=19&lang=en&page=Scrittura

**Difficulty.** A.

### A2. Where B-values are and are not justified

**Do.** Split Linear A syllabograms into three bins, using only criteria already stated by epigraphers: (i) shapes shared with Linear B that also occur in sign-groups with stable behavior, (ii) shapes shared but values conventional only, (iii) signs with no Linear B match. Mnamon says only about a dozen fall in the strong bin. Test that list against SigLA; do not add new sound values.

**Done.** A cited binning, with each sign’s GORILA/SigLA number and the sentence in the literature that justifies the bin.

**Data.** Mnamon link above; SigLA; Younger’s conventional transcriptions, archived: https://web.archive.org/web/20210415092941/http://www.people.ku.edu/~jyounger/LinearA/ and the Academia mirror https://kansas.academia.edu/JYounger  
**Difficulty.** B.

### A3. Libation-formula concordance, untranslated

**Do.** Collect every stone-vase or libation-table occurrence of the repeated sequence that is conventionally transcribed along the lines of *a-sa-sa-ra-me* / *ja-sa-sa-ra-me*. Align variants. Count what is actually identical.

**Done.** An alignment and a statement of which signs are stable. No English gloss.

**Data.** Same as A2. Secondary discussion of the formula is widespread; the alignment must come from the transcriptions, not from a blog’s translation.  
**Difficulty.** B.

### A4. Linear A ideograms vs Linear B formats

**Do.** Build a commodity table: Linear A ideogram number, proposed referent in the secondary literature (grain, figs, wine, oil, persons, livestock), whether the identification rests on shape, on numerical context, or on both, and a pointer to Palmer 1995 as used by Petrolito et al.

**Done.** A cautious economic index. Words in the Minoan language stay blank on purpose.

**Data.** https://aclanthology.org/W15-3715.pdf ; Corazza’s account of document types: https://cris.unibo.it/retrieve/90a2e16b-e280-42ac-92f1-a9961ef98ca6/d-2-402-corazza-computational-methods.pdf  
**Difficulty.** B.

### A5. Cretan Hieroglyphic sign-list diff

**Do.** Diff CHIC’s 144-sign inventory against the removals and reclassifications in Ferrara, Montecchi, and Valério 2021 (signs they say are Linear A, signs attested once on a lost object, numerals set aside).

**Done.** A spreadsheet: CH number, status (kept / removed / moved), one-line reason, page or section of the paper.

**Data.** https://cris.unibo.it/retrieve/handle/11585/881988/e1dcb33a-1c02-7715-e053-1705fe0a6cc9/Ferrara-Montecchi-Val%c3%a9rio_Kadmos_2021.pdf  
CHIC bibliographic anchor: https://editions.efa.gr/?id=216&r=publication  
Volume introduction: https://cris.unibo.it/retrieve/e402b108-7d20-4ae3-b3e5-79c872eb53e4/Cretan%20Hieroglyphic_CUP.pdf  
**Difficulty.** B. The plates of CHIC are not all online; do not redraw signs from memory.

### A6. Cypro-Minoan: long texts only

**Do.** From published catalogues, list inscriptions with more than 10 signs (the paleographic literature says there are about 21). Record CM 1 / CM 2 / CM 3, site, support, and sign count. Exclude the short bowles and pot-marks from any later statistical experiment, or put them in a separate file.

**Done.** A “long text” subset with Olivier’s HoChyMin numbers where they exist, plus post-2007 additions explicitly marked.

**Data.** Unicode proposal summarizing Olivier’s groups and the CM 2 sign count: https://www.unicode.org/wg2/docs/n5135-cyprominoan.pdf  
Corpus-size reviews: https://bmcr.brynmawr.edu/2013/2013.02.04/ and https://ajaonline.org/book-review/2169/  
Signary dispute: https://www.academia.edu/130061000/Polig_Donnelly_Between_Frustration_and_Progress_An_Integrated_Cypro_Minoan_Signary_and_Its_Paleographic_Diversity  
**Difficulty.** B.

### A7. Valério grid as a ledger, not a reading

**Do.** Extract every phonetic value Miguel Valério has proposed, mark which he called secure vs hypothetical, and note the comparison sign (Linear A or Cypriot syllabary). Do not apply the grid to produce translations.

**Done.** A claim ledger (method rule 6 in `methods.md`).

**Data.** https://cris.unibo.it/handle/11585/743571 and the related script-comparison paper https://cris.unibo.it/handle/11585/722704  
**Difficulty.** B.

### A8. Phaistos sign–object parallels, after 1908

**Do.** A table of the 45 disc signs (use the standard Evans/Godart numbering) against parallels that were excavated **after** the disc was found: the 1955 sealing, the 1965 bowl’s comb-like potmark, impressed fine ware, Arkalochori. Date each parallel.

**Done.** A forgery-relevant catalogue. No phonetic values.

**Data.** https://anetoday.org/phaistos-disk/  
Arkalochori relationship: https://cris.unibo.it/handle/11585/975345  
Sign count and discovery history: https://en.wikipedia.org/wiki/Phaistos_Disc  
**Difficulty.** A/B.

---

## B. Proto-Elamite and Linear Elamite

### B1. Numeral-system tagger

**Do.** Using CDLI transliterations, tag each numeral string as sexagesimal, decimal, bisexagesimal, capacity, or uncertain, following Englund’s criteria. Check that totals, where preserved, match the tag.

**Done.** A file of tablet id, system, and whether the total confirms it. No word readings.

**Data.** Search: https://cdli.earth/search (filter proto-Elamite)  
Englund: https://www.mpiwg-berlin.mpg.de/Preprints/P183.PDF and https://cdli.earth/files-up/publications/englund2004c.pdf  
Sign frequencies: https://cdli.earth/articles/cdlb/2002-1  
A 2025 attempt on the same problem, to be evaluated not copied: https://arxiv.org/html/2502.00090v1  
Handbook: https://www.iranicaonline.org/articles/elam-iii/  
**Difficulty.** B. Transliteration conventions are easy to misread; keep uncertain tags.

### B2. Proto-Elamite complex graphemes

**Do.** Count how often signs are ligatured or sequenced in ways editors treat as one grapheme vs several. Recompute a simple frequency list under both decisions.

**Done.** A demonstration that the “number of signs” is not a stable integer. This stops bad entropy comparisons with Linear B.

**Data.** Same CDLI set; clustering discussion: https://aclanthology.org/W19-2516.pdf  
**Difficulty.** B.

### B3. Linear Elamite audit sheet

**Do.** From the 2022 paper, list each published sign value and the inscription plus the Akkadian or Elamite name that is supposed to anchor it. Mark anchors that are royal names vs anchors that are only internal.

**Done.** A one-page-per-value ledger. You are not asked to decide if Desset is right. You are asked to make the claim checkable.

**Data.** https://orbi.uliege.be/bitstream/2268/334018/1/The%20decipherment%20of%20Linear%20Elamite.pdf  
Authors’ summary: https://anetoday.org/desset-irans-linear-elamite-deciphered/  
Critical context: https://www.lrb.co.uk/the-paper/v47/n04/tom-stevenson/beyond-mesopotamia  
Variant database notice (2025): https://orbi.uliege.be/handle/2268/333157  
**Difficulty.** C. Elamite and Akkadian names need a second pair of eyes.

### B4. Keep the two scripts apart

**Do.** A short public note, with a map and a timeline, of every popular source that treats proto-Elamite tablets and Linear Elamite monuments as one script. Include the dates (c. 3100–2900 vs c. 2300–1880) and the object types.

**Done.** A confusion list. Useful, and not a decipherment.

**Difficulty.** A.

---

## C. Indus

### C1. Crosswalk Mahadevan ↔ Wells/ICIT

**Do.** Build a table of sign ids that are the same shape under both lists, ids that one list splits, and ids that only exist in one list. Use only published concordances and the ICIT documentation. Do not invent a third list.

**Done.** The crosswalk, plus a count of inscriptions whose n-gram signature changes if you switch lists.

**Data.** ICIT: https://www.epigraphica.de/indus/menueindus.htm  
Edition history and the 417 vs ~676 contrast: https://www.imsc.res.in/~sitabhra/meetings/bitsscripts24/C_Subramanian_Lecture.pdf  
Structural paper that states it uses Mahadevan’s IDF-80: https://www.nature.com/articles/s41599-019-0274-1  
**Difficulty.** B. ICIT access has at times required contacting the maintainers; if the live database is closed, document that and work from the lecture’s published counts rather than scraping.

### C2. Length histogram and the “writing” debate, without picking a winner

**Do.** From Mahadevan’s published totals (2,906 objects, 13,372 signs), plot approximate lengths. State the mean near 4–5. Then summarize, in their own claims, Farmer/Sproat/Witzel 2004 and Rao et al. *Science* 2009, including Sproat’s later objections. No new entropy “proof.”

**Done.** A briefing a non-specialist can trust.

**Difficulty.** A.

### C3. Terminal-sign and numeral-stroke catalogue

**Do.** List signs that the 2019 *Humanities and Social Sciences Communications* paper treats as terminal or as numeral strokes, with frequencies and sites.

**Done.** A replication of a published structural claim, or a clear statement of where the replication failed.

**Data.** https://www.nature.com/articles/s41599-019-0274-1  
**Difficulty.** B.

### C4. Mesopotamian Indus finds as a separate file

**Do.** Extract the small set of Indus or Indus-like inscriptions found outside South Asia. They are not a bilingual, but they are the only external context. Record object, site, and what is actually identical to a Harappan sign.

**Done.** A short catalogue that says “context” and does not say “translation.”

**Difficulty.** B. Use CISI photographs and museum publications, not a blog’s decipherment.

---

## D. Read scripts, unread stretches of language

### D1. Etruscan formula extractor

**Do.** From texts of at least three letters in a standard edition’s transcription, tag the ownership pattern (the *mi* “I am” inscriptions) and kinship words that handbooks already gloss. Leave unknown ritual words unmarked rather than guessed.

**Done.** A frequency list of **already secure** items, with edition numbers. This is a baseline for later dictionary work, not a reading of the Liber Linteus.

**Data.** Concordance project description: https://www.degruyterbrill.com/document/doi/10.1515/etst-2023-0007/html  
Pyrgi as the bilingual that is **not** a full key: https://www.museoetru.it/masterpieces/lamine-doro-da-pyrgi  
Liber Linteus scale: https://bmcr.brynmawr.edu/2011/2011.01.36/  
CIE scale: https://bmcr.brynmawr.edu/2007/2007.07.04/  
**Difficulty.** B. *Etruskische Texte* (Meiser 2014) is a book, not an open dump. Do not pirate it; use what is actually licensed and open.

### D2. Pyrgi, side by side, differences marked

**Do.** Align the Phoenician plaque with the two Etruscan plaques at the level of phrases the museum and the standard discussions already identify (deity, dedication, Thefarie Velianas). Mark clauses that do **not** match.

**Done.** A one-page demonstration of why Pyrgi is not the Rosetta Stone.

**Data.** Museum page above; Szemerényi’s linguistic comments: http://smea.isma.cnr.it/wp-content/uploads/2015/05/Szemer%C3%A9nyi_Linguistic-comments.pdf  
**Difficulty.** B.

### D3. Hesperia length-and-script census

**Do.** Export or count northeastern vs southeastern vs southwestern inscriptions, and the proportion under 5 signs. Cite Gómez-Moreno’s semi-syllabary as settled for the northeast and unsettled for the southwest.

**Done.** A census with a date-of-export stamp, because Hesperia grows.

**Data.** http://hesperia.ucm.es/ and http://hesperia.ucm.es/bancodatos.php  
Script history: https://www.unicode.org/L2/L2015/15120-northeastern-iberian.pdf  
Language status: https://ifc.dpz.es/recursos/publicaciones/38/77/17moncunillvelaza.pdf  
Southwest: https://dialnet.unirioja.es/descarga/articulo/3339686.pdf  
**Difficulty.** A.

### D4. Iberian recurring suffixes, no Basque

**Do.** On long northeastern texts only, list recurring final sign-sequences that epigraphers already segment as morphological. Do not assign them to Basque etyma.

**Done.** A segmentation baseline with citations to Moncunill and Velaza or Untermann’s MLH, not a family claim.

**Difficulty.** C.

### D5. Southwestern sign confidence table

**Do.** Two columns: values generally used by the mid-2010s, and values still marked hypothetical. Each row cites the discussion that put it in that column.

**Done.** A script-status table. The stelae stay untranslated.

**Difficulty.** B.

### D6. Meroitic secure lexicon, evidence required

**Do.** For each handbook gloss (*qore*, *kdi*, *mk*, *ato*, plural and case suffixes, and only a few more), record the REM example that carries it and whether the gloss comes from Egyptian transcription, formulaic contrast, or Rilly’s comparative argument.

**Done.** A tiny dictionary that a skeptic can audit. Omit any word you cannot source.

**Data.** REM volumes on Persée: https://www.persee.fr/collection/rem  
Rilly’s survey: https://escholarship.org/uc/item/3128r3sw  
2024 lecture notice (scope of what he still calls unfinished): https://voices.uchicago.edu/lvc/2024/03/05/claude-rilly-cnrs-ephe-paris-sorbonne-meroitic-phonology-syntax-and-linguistic-family/  
**Difficulty.** B/C.

### D7. Meroitic family-argument synopsis

**Do.** Two columns, Rilly (East Sudanic: SOV, postpositions, genitive order) vs Rowan (Afroasiatic-like phonotactics). No winner unless you have a new argument; the project is to stop papers from citing only one side.

**Data.** UCLA article above; Rowan’s working paper is the 2006 SOAS piece “Meroitic – An Afroasiatic Language?” (cited throughout the specialist literature; check eprints.soas.ac.uk).  
**Difficulty.** A.

### D8. Funerary-formula slots

**Do.** From REM curses and offering formulae, mark the slots that vary (personal name, parent, title) vs the slots that do not. This is the frame in which new glosses would have to sit.

**Done.** A template with blanks. The blanks stay blank unless D6 already filled them.

**Difficulty.** C.

---

## E. East Asia

### E1. Khitan large-script coverage map

**Do.** Using Kane’s published counts as summarized in Unicode N5319, list how many large-script characters had proposed readings versus how many are only attested. Contrast with the small script’s much higher coverage. Update only where you have a post-2009 paper in hand; do not guess that “more has been done.”

**Done.** A coverage map with dates on every number.

**Data.** https://www.unicode.org/wg2/docs/n5319-KhitanLargeScriptEncoding.pdf  
Small-script phonetic revisions (2017): https://akjournals.com/view/journals/062/70/2/article-p109.xml  
**Difficulty.** B.

### E2. Epitaph parallels

**Do.** For one published Khitan epitaph that has a Chinese parallel, list the proper names and titles that are already equated in the literature. Stop there.

**Done.** A model of what a bilingual actually buys, for comparison with Pyrgi and with Indus (which has none).

**Difficulty.** C. Requires the inscription publication, not a Wikipedia list.

---

## F. Americas

### F1. Isthmian claim ledger

**Do.** A document with four sections only: (1) Justeson and Kaufman 1993, language claimed, what they treated as the key; (2) the later La Mojarra column, what was predicted; (3) Houston and Coe’s mask, what they say fails; (4) later alternative claims, one paragraph each, marked unaccepted. No new translation.

**Data.** https://www.science.org/doi/10.1126/science.259.5102.1703  
https://www.baltimoresun.com/2004/02/09/a-translation-unmasked/  
A later alternative, to be logged not endorsed: https://bonndoc.ulb.uni-bonn.de/xmlui/bitstream/handle/20.500.11811/1429/2020_Vonk_Yet_another_decipherment_of_the_Isthmian_Writing2_System.pdf  
**Difficulty.** B.

### F2. Cascajal sign images vs Olmec iconography

**Do.** Number the 62 signs as in the 2006 report. Note which signs Mora-Marín and others have compared to Olmec motifs. Record proposed reading orders as rival hypotheses.

**Done.** A sign sheet. No sentence in a language.

**Data.** https://www.science.org/doi/10.1126/science.1131492  
Reading-order discussion: https://davidmm.web.unc.edu/wp-content/uploads/sites/400/2025/09/Mora-Marin-2020-Cascajal-Block-Print-Edition.pdf  
Archaeometry: https://www.cambridge.org/core/journals/ancient-mesoamerica/article/digital-imaging-and-archaeometric-analysis-of-the-cascajal-block-establishing-context-and-authenticity-for-the-earliest-known-olmec-text/42B1EB580DAA062892886EA04F115046  
**Difficulty.** B.

### F3. Zapotec calendar layer

**Do.** From Urcid and the Monte Albán lunar-count paper, list day signs and numeral uses that are **not** disputed, separate from narrative glyphs that are.

**Data.** https://www.famsi.org/zapotecwriting/zapotec_text.pdf  
https://www.cambridge.org/core/journals/latin-american-antiquity/article/lunar-day-count-at-monte-alban-and-the-chronology-of-early-and-middle-preclassic-zapotec-hieroglyphic-texts-ca-496221-bce/DB892A3F96BB78AA2356046A35B7B547  
Urcid 2001 is the monograph (library, not a free dump).  
**Difficulty.** C.

---

## G. Rongorongo

### G1. Barthel vs Fischer conflict list on H, P, and Q

**Do.** These three texts largely repeat each other. Align a public transcription of one repeated line under both drawing traditions. Mark every glyph where the two records differ.

**Done.** A conflict list. This is the single most useful rongorongo data-cleaning job, and it is not a decipherment.

**Data.** Concordance mirror: https://www.kohaumotu.org/rongorongo_org/concord/index.html  
Site home: https://kohaumotu.org/  
Corpus description and the reason both transcriptions exist: https://en.wikipedia.org/wiki/Rongorongo  
**Difficulty.** B.

### G2. Authenticity filter

**Do.** From the standard corpus table, flag texts cut with steel, of poor provenance, or considered imitations (the literature names K, V, Y, and others as problematic). Produce a “core corpus” file and a “do not train on this” file.

**Done.** The filter, with the reason for each exclusion.

**Difficulty.** A, if you stick to published judgments and do not re-authenticate from photos you do not have.

### G3. Mamari lunar sequence, structure only

**Do.** Isolate the stretch on tablet C that Guy and others identify as a lunar month. Describe its structure (repeated glyph, inserted glyphs, length). Do not extend the reading to the rest of the tablet.

**Data.** Same as G1. A 2026 computational test of syllabic ideas, not a reading: https://aclanthology.org/2026.lt4hala-1.16.pdf  
**Difficulty.** B.

### G4. Wood-date vs inscription-date table

**Do.** One row per dated object: species if known (Orliac), radiocarbon result, and the explicit caveat that the inscription can be later. Include the 2024 Rome results.

**Data.** https://www.nature.com/articles/s41598-024-53063-7  
**Difficulty.** A.

---

## H. Manuscripts

### H1. Voynich transcription diff

**Do.** Diff two IVTFF files (for example Zandbergen–Landini vs Takahashi) by folio. Report where the *words* change, not a language.

**Done.** A disagreement map of Currier A vs B pages and of the herbal labels.

**Data.** Format and file list: https://voynich.nu/extra/sp_transcr.html  
ZL file: https://voynich.nu/data/ZL3a-n.txt  
Word counts: https://www.voynich.nu/a4_word.html  
Vellum date: https://voynich.nu/origin.html  
Beinecke images: search the library catalogue for MS 408 (the images, not a third-party redraw, are the ground truth).  
**Difficulty.** A.

### H2. Voynich control texts

**Do.** Reproduce one published statistic (word-length distribution or a simple entropy) on EVA text **and** on a control of similar length generated by a simple stochastic process or by shuffled words. If both pass, say so.

**Why.** This is the antidote to “we proved it is a language.”

**Data.** Bowern and Lindemann (language-like structure): https://alumniacademy.yale.edu/sites/default/files/2021-07/The%20Linguistics%20of%20the%20Voynich%20Manuscript.pdf  
A gibberish-comparison paper: https://ceur-ws.org/Vol-3313/paper4.pdf  
A natural-language claim to test against, not to adopt: https://www.tandfonline.com/doi/full/10.1080/01611194.2024.2414128  
**Difficulty.** A/B.

### H3. Plant-label uncertainty

**Do.** For the herbal folios, list labels whose plant drawing has **no** agreed botanical identification in the literature you actually read. The point is the size of the unanchored set.

**Done.** A negative catalogue. Do not name the plants yourself from a field guide and then “read” the label.

**Difficulty.** B.

### H4. Rohonc prediction test

**Do.** If you use the Király–Tokai proposal, freeze the mapping on the pages they used to define it, then apply it to pages you held out. Score exact string matches only. Láng 2010 is the problem statement, not a solution.

**Data.** https://www.tandfonline.com/doi/full/10.1080/01611191003605587  
The codex images, if used, must come from the holding library’s terms, not from a random PDF.

**Done.** Either a passed prediction or a documented failure. Both are results. A new biblical story is not.

**Difficulty.** C.

---

## I. Fragment, Neolithic, and “stop” projects

### I1. Singapore Stone stroke inventory

**Do.** From museum photography, count visible lines and legible character-spaces on the surviving fragment. Compare with Kawi descriptions in the 2023 papers without filling gaps.

**Data.** https://www.roots.gov.sg/Collection-Landing/listing/1148198  
https://www.mdpi.com/2409-9252/3/3/19  
https://www.mdpi.com/2409-9252/3/3/18  
**Done.** A physical description. Missing lines stay missing.  
**Difficulty.** A/B.

### I2. Dispilio: one-page evidence limit

**Do.** Summarize Facorellis et al. 2014: what was dated, the radiocarbon result, and the conditional sentence about writing. List what would be required to call the marks a script (a second text, a repeated ordered inventory, a context of accounts or names) and note that none of it exists.

**Data.** https://www.cambridge.org/core/journals/radiocarbon/article/abs/radiocarbon-dating-of-the-neolithic-lakeside-settlement-of-dispilio-kastoria-northern-greece/759AA29502776E142883F1971293BEB1  
**Difficulty.** A.

### I3. Vinča / Tărtăria claim vs corpus

**Do.** Contrast “oldest writing” headlines with the actual evidence: many short signs on pottery, three disputed tablets, no sentences, context problems. Cite the *Documenta Praehistorica* critique.

**Data.** https://journals.uni-lj.si/DocumentaPraehistorica/article/download/32.19/1882/3526  
https://en.wikipedia.org/wiki/T%C4%83rt%C4%83ria_tablets  
**Done.** A bibliography annotated “not a corpus.”  
**Difficulty.** A.

### I4. Byblos inscription inventory

**Do.** A list of the securely identified texts (about 14), support (stone or metal), and published source (Dunand 1945 and later), plus Sass’s dating argument in one paragraph.

**Data.** https://scholarlypublications.universiteitleiden.nl/access/item%3A3732020/view  
https://www.academia.edu/38559714/  
**Difficulty.** B.

---

## J. Meta-projects (high value, low glamour)

### J1. Claim ledger for the whole field

**Do.** One row per announced decipherment you can tie to a publication: script, year, proposed language, whether a held-out prediction was attempted, whether specialists adopted it. Start with Linear B (adopted), Meroitic script (adopted), NE Iberian (adopted), Maya (adopted), Isthmian (not adopted), Linear Elamite 2022 (not yet consensus), Fischer rongorongo (rejected), every Voynich “solution” you can document (rejected or ignored).

**Done.** A living CSV in this directory or beside it. This is the single best guardrail for future work.

**Difficulty.** B, and it should stay open.

### J2. “Solved neighbor” one-pagers

**Do.** For Linear B, the Cypriot syllabary, Ugaritic, Egyptian, Maya, and Carian, write half a page on the **external check** that made the reading stick. Use the Cambridge Linear B pages as the model of how specific to be.

**Data.** https://www.classics.cam.ac.uk/system/files/documents/process.pdf  
https://www.cam.ac.uk/research/news/cracking-the-code-the-decipherment-of-linear-b-60-years-on  
**Difficulty.** A.

### J3. Data-provenance sheet

**Do.** For any CSV you download, record URL, date fetched, upstream edition, and known normalizations. In particular, mark derivative GitHub corpora of Linear A or Indus as **not editions**. Prefer:

| Corpus | Prefer | Avoid treating as the edition |
|---|---|---|
| Linear A | SigLA; GORILA (print); Younger archive clearly labeled as B-values | Random JSON “complete translations” |
| Proto-Elamite | CDLI | Any list that mixes in Linear Elamite |
| Indus | Mahadevan / CISI / ICIT, named | An unlabeled Hugging Face mix of sign lists |
| Iberian | Hesperia | A wordlist already glossed into Basque |
| Meroitic | REM | A blog transliteration with no REM number |
| Rongorongo | Kohaumotu, with Barthel/Fischer flag | A single “cleaned” glyph string |
| Voynich | voynich.nu IVTFF + Beinecke images | A transcription that already inserts Latin words |

**Difficulty.** A, and mandatory before any other computational project.

---

## What not to start

- A program that searches Linear A strings against dictionaries of Hurrian, Luwian, Greek, and Semitic and prints the best gloss.
- A complete reading of the Phaistos Disc, the Cascajal Block, the Dispilio plank, or the Tărtăria tablets.
- Filling the Singapore Stone’s missing lines with a language model.
- An Indus decipherment aimed at the 2025 prize. The text lengths have not changed.
- Training a model on all 26 rongorongo objects, including the ones specialists already set aside as doubtful.

If new tablets, a bilingual, or a second Cascajal block appear, the ranking in `closest.md` changes and these prohibitions can be reopened. Until then they stand.
