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

Narrative with the numbers and the negative results: [ai-already-helped.md](ai-already-helped.md), [vesuvius-scrolls.md](vesuvius-scrolls.md).
