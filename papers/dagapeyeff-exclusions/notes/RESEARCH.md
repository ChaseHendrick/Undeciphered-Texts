# Prior-article review

Dated 6 October 2026. The detailed survey, with quotations and per-source reading scope, is `docs/logs/dagapeyeff-prior-work-2026-10-05.md` in this repository (5 October 2026), extended by `docs/logs/dagapeyeff-others-2026-10-04.md`.

## Sources and how they were read

| Source | Read | Used for |
| --- | --- | --- |
| d'Agapeyeff, *Codes and Ciphers*, 1939 | Not inspected | The challenge and the worked exercise are taken from Wikipedia's transcription |
| Wikipedia, "D'Agapeyeff cipher", fetched 2 October 2026 | Full page | Digit block, exercise and its square, the ARYA error, the p. 111 dummy rule |
| Barker, *Cryptologia* 2(2), 1978 | Not opened; bibliographic data checked by search (DOI 10.1080/0161-117891852901) | Citation only |
| Gariazzo, Zenodo 10.5281/zenodo.22057249 (report) and 10.5281/zenodo.21970478 (code) | Project page and report v2 fetched on 5 October; titles confirmed by search on 6 October | Prior searches, shuffled baseline, four-square coverage |
| van Eykelen, MsgTrail parts XIV and XV | Fetched on 5 October; titles confirmed by search on 6 October | No-message construction |
| Marland, dagapeyeffresearch.com | Home page fetched once | Prior configurations |
| Pelling, Cipher Mysteries, 2013 and 2017 | Fetched on 5 October, including comments by Rodrigues and Melichar | Last-column observation; the Kerckhoffs copy; 240-letter remark |
| Snider, dagapeyeff-col14 | README fetched | Quantified last column |
| Uygun, Caillahua Mendoza, Leggett (Zenodo) | Records read on 5 October; titles could not be retrieved on 6 October (zenodo.org blocked here) | Published readings, cited by DOI only |
| Shulman (Ab Struse), *The Cryptogram*, April/May 1952 | Not opened; title from search | Citation; earlier record |
| Schmeh, MysteryTwister challenge PDF | Title from search | Citation |
| Ashley and Antigravity, dagapeyeff-cipher-solver, GitHub, 2026, commit 2009392 | README and PAPER.md read on 6 October 2026 | Its index-of-coincidence argument for a monoalphabetic key is discussed in Section 1 |
| NumberWorld blog, 2013 and 2015; Please Decipher Me blog, 2010 and 2011 | Search summaries | Dictionary-code and ADFGX hypotheses; the 1949 reprint |
| Ney, Essen and Kneser 1994; Kirkpatrick, Gelatt and Vecchi 1983; Lasry, Kopal and Wacker 2014 | Bibliographic data checked by search | Methods credit |

## Queries on 6 October 2026

Web searches for the Zenodo record titles, for Barker's DOI, for the Lasry, Kopal and Wacker article, for Ney, Essen and Kneser, for the MsgTrail and Cipher Mysteries titles, and for public Italian and multilingual corpora. Direct fetches of zenodo.org, crossref.org, msgtrail.com, ciphermysteries.com and ruben-gariazzo.fr were blocked by this environment's network policy, so titles were confirmed through search results.

Second search, 6 October 2026, after the owner asked for more prior work: general searches for D'Agapeyeff analyses, for Shulman's 1952 note, for GitHub projects, for Schmeh's MysteryTwister page, for Bauer's *Unsolved!* (2017), whose coverage of this cipher could not be confirmed and which is not cited, and for the NumberWorld series.

## Novelty bound

Within the sources above, no earlier work shows planted-text recovery for a width-14 columnar key with a letter key at 196 letters, excludes four-square or a repeating coordinate shift by a key-free count, bounds enciphering errors by Proposition 2, or screens languages by it. Gariazzo searched four-square to 20.9 percent coverage after showing 83 percent key recovery; Melichar searched corpora for windows with the cells' coincidence and unused letters, which the corpus count here extends. Absence from this survey does not show that a result is new, and the manuscript says so.
