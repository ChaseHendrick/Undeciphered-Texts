# External tools, repos, and papers (pointers only)

We **do not vendor** these codebases. Use them directly; cite authors. This repo’s `engine/` is a small classical practice toolkit.

## Production historical-cryptology stacks

| Resource | Why it matters | URL |
|----------|----------------|-----|
| **DECRYPT / DECODE** | Digitized cipher corpus, HistCorp LMs, transcription pipeline | https://de-crypt.org/ · https://de-crypt.org/decrypt-web/ |
| **CrypTool 2** | Full GUI cryptanalysis for classical & historical ciphers; used inside DECRYPT | https://github.com/CrypToolProject/CrypTool-2 |
| **CTTS** (CrypTool Transcriber & Solver) | Transcription + key recovery workflow (Lasry / CrypTool team) | https://github.com/CrypToolProject/CTTS |
| **CrypTool-Online** | Browser solvers for simpler classical ciphers | Linked from https://de-crypt.org/ |

## Classical / homophonic solvers (community)

| Resource | Notes | URL |
|----------|-------|-----|
| **AZdecrypt** | Strong hill-climber; used in Zodiac Z340 break | Search “AZdecrypt” (Van Eycke); Oranchak writeup: https://blog.wolfram.com/2021/03/24/the-solution-of-the-zodiac-killers-340-character-cipher/ |
| **Crypto Cellar (Weierud)** | Enigma / German Army message breaks & challenges | https://cryptocellar.org/bgac/ |
| **Practical Cryptography** | Teaching attacks, pigeon-cipher notes | http://practicalcryptography.com/ |

## NLP / unsupervised decipherment literature

| Work | Topic | URL |
|------|-------|-----|
| Knight, Nair, Rathod, Yamada (2006) | Unsupervised decipherment / EM | https://aclanthology.org/P06-2065.pdf |
| Knight, Megyesi, Schaefer (2011) | Copiale Cipher | https://www.su.se/english/research/research-catalogue/research-projects/d/decipherment-of-historical-manuscripts/the-copiale-cipher |
| Ravi & Knight (and follow-ons) | Combinatorial / Bayesian decipherment | ACL Anthology search “decipherment” |
| Berg-Kirkpatrick & Klein | Feature-rich decipherment models | ACL Anthology |
| HistoCrypt proceedings | Venue for historical cryptology | e.g. https://ecp.ep.liu.se/ (HistoCrypt series) |
| Megyesi et al. (2020) | DECRYPT project overview (Cryptologia) | https://doi.org/10.1080/01611194.2020.1716410 |

## Image→plaintext research (Copiale case studies)

Pointers only, different problem than classical substitution annealing:

- https://github.com/leitro/Decipher-from-Pixels-Copiale (HistoCrypt 2026)
- https://github.com/marinocom/Direct-Image-Decryption-Copiale

## Ancient-script data (not cipher solvers)

| Resource | Script | URL |
|----------|--------|-----|
| SigLA | Linear A | https://phis.me/sigla/ |
| kohaumotu | Rongorongo | http://kohaumotu.org/rongorongo_org/corpus/digit.html |
| Beinecke digital library | Voynich MS 408 | https://beinecke.library.yale.edu/beinecke/collections/beinecke-cipher-voynich-manuscript |
| Indus corpora / stats papers | Indus | e.g. https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0009506 |

## How to use these with this repo

1. Learn classical attacks with `python -m engine.cli demo`.
2. Graduate to **CrypTool 2 / CTTS / DECODE** for real manuscripts.
3. Use Crypto Cellar for Enigma-specific search.
4. Keep ancient-script work in corpus/statistics land unless you have specialist training.


## Additions from the 2023-2026 audit

### Herculaneum

- https://scrollprize.org/
- https://scrollprize.org/data
- https://scrollprize.org/grandprize
- https://scrollprize.org/firstscroll
- https://github.com/ScrollPrize/villa
- https://arxiv.org/abs/2304.02084
- https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0215775

### Known-language ML

- https://www.nature.com/articles/s41586-022-04448-z
- https://github.com/google-deepmind/ithaca
- https://github.com/sommerschield/iphi
- https://doi.org/10.1093/pnasnexus/pgad096
- https://github.com/gaigutherz/Akkademia
- https://arxiv.org/abs/2306.01268
- https://doi.org/10.1371/journal.pone.0243039
- https://aclanthology.org/P19-1303/
- https://aclanthology.org/P11-1025/
- https://aclanthology.org/D08-1085/
- https://aclanthology.org/P13-1154/
- https://aclanthology.org/P10-1107/
- https://aclanthology.org/D11-1029/
- https://aclanthology.org/W11-1202/

### Solvers and OCR

- https://github.com/jameslyons/pycipher
- https://github.com/perrygeo/simanneal
- https://github.com/theikkila/substitution-cipher-SA-solver
- https://github.com/doranchak/azdecrypt
- https://github.com/matthewdgreen/decipher
- https://github.com/mittagessen/kraken
- https://gitlab.com/scripta/escriptorium
- https://www.transkribus.org/
- https://github.com/leitro/Decipher-from-Pixels-Copiale

### Agent harnessing (tools for how this repo itself is run)

Pointer found via a public X post by Shubham Saboo, 18 October 2026; the
project page and paper are the source of record. This repo has **not** used it.

| Resource | Why it is adjacent here | URL |
|----------|------------------------|-----|
| **Harness²** (Google Research) | Recursive harnessing: a Propose–Probe–Compose loop refines the system around a fixed-weight model — prompts, guardrails, memory, tool guidance, subagents, skills, scripts, plugins — for tasks unseen during harness design; supports OpenCode and Codex executors, which is how this repo's K4 runs are driven. Source-not-used experiment status: their paper reports gains of up to 11.5 points on WorkBuddy-Bench, 4.5 on JobBench, and 11.8 points on LAB's partial pass with one recursion step (arXiv:2610.14224, Apache-2.0). | https://github.com/google-research/harness2 · https://arxiv.org/abs/2610.14224 |

If a future K4 session adopts it, the rules do not change: planted controls,
shown power, dated logs in `docs/k4-focus/`, and nothing is a plaintext until
it survives the usual verification.

### Constraint, SAT, and model counting (the current K4 method spine)

The 2026 K4 exclusions are exact SAT over one-hot encodings. These are the
reference tools of that layer, none vendored; the engine already installs
PySat, which itself bundles CaDiCaL, Glucose and MiniSat.

| Resource | Why it matters here | URL |
|----------|--------------------|-----|
| **PySat** | The SAT framework the K4 modules are actually written on | https://github.com/pysathq/pysat |
| **Kissat (Biere)** | Flagship-class SAT solver; a faster drop-in alternative to CaDiCaL for the wide CNF heads | https://github.com/arminbiere/kissat |
| **Z3** | SMT: native all-different, arithmetic and bit-vector models for structured cipher constraints | https://github.com/Z3Prover/z3 |
| **Google OR-Tools (CP-SAT)** | Constraint programming with all-different and counting constraints; useful for the sizing steps the ledger asks for before language searches | https://github.com/google/or-tools |
| **ApproxMC (Meel group)** | Approximate model counter: counts the satisfying set without enumerating it — the missing piece between "SAT" and "excluded-by-count" for families whose survivors are too many to list, e.g. the surviving letter-chain shapes | https://github.com/meelgroup/approxmc |

### Cipher web toolboxes (cross-checks, not search targets)

| Resource | Why it matters here | URL |
|----------|--------------------|-----|
| **dCode.fr** | Solver and identifier zoo for hundreds of classical cipher types | https://www.dcode.fr/ |
| **Guballa solvers** | Community-standard online substitution and Vigenère hill-climbers, useful as an independent second opinion on our engine's results | https://www.guballa.de/substitution-solver |
| **Zodiac ciphers site (Oranchak)** | The webtoy workbench and the full Z340 solution archive, including the hill-climb methodology notes | https://zodiackillerciphers.com/ |
| **MysteryTwister C3 (MTC3)** | Challenge archive with known plaintexts — a calibration set for new solvers before their results are trusted on K4 | https://www.mysterytwisterc3.org/ |
| **Crypto Museum** | Hardware and archive references for rotor machines and landmark cipher devices | https://www.cryptomuseum.com/ |

### Running-key and language corpora (the open running-key family is corpus-starved)

| Resource | Why it matters here | URL |
|----------|--------------------|-----|
| **Chronicling America (Library of Congress)** | OCR'd US newspapers from 1756 to 1963 with a search API — a plausible source class for a K4-era running key | https://chroniclingamerica.loc.gov/ |
| **Papers Past (National Library NZ)** | OCR'd newspapers 1839-2014, freely searchable at scale | https://paperspast.natlib.govt.nz/ |
| **Project Gutenberg** | Mass public-domain prose for language models beyond the repo's 1.9M-letter training file | https://www.gutenberg.org/ |
| **Norvig n-gram tables** | Word and letter count tables for building stronger scoring models | https://norvig.com/ngrams/ |
| **Google Books Ngram Viewer** | Very large historical English frequency data, with a downloadable dataset | https://books.google.com/ngrams |

Narrative with the numbers and the negative results: [ai-already-helped.md](ai-already-helped.md), [vesuvius-scrolls.md](vesuvius-scrolls.md).
