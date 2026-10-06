# Quality record

## Quality standard adoption (2026-10-03)

**Quality standard:** 2026-10-03

- [x] **U1. Complete proofs.** Propositions 1 to 3 are proved in full in Section 3. Proposition 2's lower bound and its attainment are both proved; the exchange step uses the four-case inequality for co-sorted pairs. No theorem is cited without proof. The model is the quadgram model of `engine/language.py` (`DiscountedLanguageModel`, discount 0.75), fit on the stated corpora; no theorem depends on it.
- [ ] **U2. Rigorous computation.** No computation is used as a proof step. Every numerical result is a seeded run of a stated program, frozen once under `engine/data/swarm_cache/` and bound to the manuscript by SHA-256 in `paper/numbers.tex`. Planted-text controls and shuffle controls are the negative controls; their sizes are stated, and several are small (3 to 8 shuffles). Open: the four-square, repeating-shift and Latin searches were not rerun under a second seed for this draft.
- [x] **U3. Every claim labelled.** The manuscript states that Propositions 1 to 3 are proved and everything else is numerical, that no reading is claimed, and which families are excluded by a count, which are closed by a search with shown power, and which remain open (Section 6). Assumptions are stated next to their results: a randomly drawn shift key, held-out prose, the Wikipedia transcription.
- [ ] **U4. Sources read.** The 1939 book and Barker 1978 were not opened. Wikipedia's transcription is the data source. Three Zenodo titles could not be retrieved and are cited by DOI. See `notes/RESEARCH.md`.
- [x] **U5. Prior article review.** `notes/RESEARCH.md` and `docs/logs/dagapeyeff-prior-work-2026-10-05.md` list the sources, dates and reading scope. Novelty statements are bounded to that coverage.
- [ ] **U6. Adversarial second reading.** Partly done: `notes/review-1.md` records an independent in-project reading of the proofs and their application, 8 findings (3 major), all confirmed and fixed; finding 1 reopened keyed four-square and two-square. The numbers, controls and claims readings did not run and remain open.
- [x] **U7. Reproducible.** `README.md` gives the commands. `code/make_numbers.py --check` and `tests/test_dagapeyeff_paper.py` fail when a number in the manuscript no longer matches its frozen file. The PDF was built with TeX Live 2023 (pdfTeX) from the committed source, with no overfull lines, undefined references or warnings; all nine pages were inspected at screen resolution. Byte-identical rebuilds were not checked.
