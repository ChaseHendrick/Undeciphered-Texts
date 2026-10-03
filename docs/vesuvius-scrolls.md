# Vesuvius Challenge and the Herculaneum papyri

Charred book-rolls from the Villa of the Papyri at Herculaneum, buried in the 79 CE eruption of Vesuvius. This is **not** an undeciphered script. The language is ancient Greek (mostly Philodemus and other Epicurean prose). The problem is physical: the rolls are carbonized, too brittle to unroll, and the carbon ink has almost the same density as the carbonized papyrus, so a plain CT scan does not show letters the way metal-ink manuscripts do.

Nothing below is a claim that AI “translated” or “deciphered” a lost language. AI and geometry recover **images of ink**. Papyrologists read the Greek.

## What was charred

- The library was excavated from the Villa of the Papyri (Herculaneum). Hundreds of rolls and fragments are in Naples (Biblioteca Nazionale, the PHerc. series) and a smaller set at the Institut de France in Paris (PHerc.Paris).
- 18th- and 19th-century mechanical unrolling, and later attempts (including work on PHerc. 1667 in 1969 and the 1980s), destroyed outer layers of many rolls. What remains of some “scrolls” is a compact inner core.
- PHerc. 1667, called Scroll 4 in the challenge, survives as about 8 cm of an original height of roughly 19-24 cm. The 2026 read is of that **surviving** core, not of a complete ancient book. Source: [Vesuvius Challenge, first full scroll](https://scrollprize.org/firstscroll).
- The 2023 grand-prize text is from **PHerc.Paris 4**, one of the Institut de France rolls, still rolled. Source: [UK Research on the grand prize](https://research.uky.edu/news/grand-prize-discovery-made-2000-year-old-herculaneum-scrolls) and [the prize announcement](https://scrollprize.org/grandprize).

## What the pipeline actually does

Three separate jobs are easy to conflate.

1. **Scan.** Micro-CT, and for the hardest rolls phase-contrast micro-CT (ESRF BM18 and earlier synchrotron work). The volume is a 3D image of the carbonized mass, not a photograph of writing.
2. **Virtual unwrapping / segmentation.** Find each papyrus sheet inside the spiral, even where it is crushed, and flatten that surface to 2D. Brent Seales (University of Kentucky, EduceLab) and colleagues built this geometric pipeline over many years. Software in the contest includes Volume Cartographer and Julian Schilliger’s ThaumatoAnakalyptor. A 2016 En-Gedi Hebrew scroll (not Herculaneum) was an earlier proof that virtual unwrapping can recover a real text when ink contrasts with the substrate.
3. **Ink detection.** Carbon ink in Herculaneum often does **not** show up as a simple density difference. A supervised model, trained where infrared or spectral photos of **opened fragments** can be aligned to CT, learns a texture that predicts “ink” vs “not ink.” The 2019 PLOS One paper from Seales’s group is the methods foundation: a 3D convolutional network used as a texturing step after the surface is isolated. It outputs an ink-prediction image. It does not know the Greek alphabet. Sources: [Parker et al., PLOS One 2019](https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0215775); [EduceLab-Scrolls, arXiv:2304.02084](https://arxiv.org/abs/2304.02084).

The EduceLab-Scrolls paper states the limit directly: the model operates on pixels, labeling them ink or not, and has no knowledge of character alphabets, OCR, paleography, or language. Seales later described the contest models the same way: they do not decide that a shape is eta rather than theta, which is exactly what limits hallucination of letters. Interview summary: [Gizmodo, 2023](https://gizmodo.com/ai-herculaneum-scrolls-computer-vision-transformers-2000481322).

Human papyrologists then transcribe the images. Disagreement between readers is normal and is part of the review, not a failure of the scan.

### Earlier synchrotron readings, and why they are not the same result

A 2016 Scientific Reports paper (Mocella, Bukreeva, and colleagues) reported virtual unrolling and short Greek letter sequences inside Naples rolls PHerc. 375 and PHerc. 495 using phase-contrast tomography, arguing that ordered papyrus fibers could be distinguished from amorphous carbon ink. Source: [Scientific Reports, srep27227](https://www.nature.com/articles/srep27227). That was a real imaging result on a small amount of text. It did not produce a continuously read book, and it is a different pipeline from the Seales / Vesuvius Challenge segmentation-plus-learned-ink stack. Do not cite it as “the scrolls have been read since 2016.”

## 2023: first letters, then the grand prize

The contest opened in 2023 (Nat Friedman, Daniel Gross, and Seales’s group; prize pool built from many donors, with a public $700,000 grand prize for reading four passages).

- **October 2023, First Letters.** Luke Farritor was the first to recover a whole word from inside a still-rolled Herculaneum scroll: ΠΟΡΦΥΡΑϹ, “purple.” He won the $40,000 first-place First Letters prize. Youssef Nader placed second ($10,000) using domain adaptation so fragment-trained ink models would fire on segmented scroll surfaces. Casey Handmer won a separate “first ink” recognition. Segmentation tooling prizes went to Julian Schilliger for work on Volume Cartographer. Sources: [grand-prize writeup](https://scrollprize.org/grandprize), [winners index](https://scrollprize.org/winners).
- **Grand prize, announced for the 31 December 2023 deadline.** Youssef Nader, Luke Farritor, and Julian Schilliger split the **$700,000** prize. The reviewed submission showed **15 partial columns** in PHerc.Paris 4, enough to pass the four-passage bar. Nader led the ink-detection models (community writeups describe TimeSformer-class and 3D CNN models plus pseudo-labeling). Schilliger’s ThaumatoAnakalyptor segmented in 3D, including crushed regions. Farritor hunted ink “crackle” and trained on the shapes he found. Sources: [scrollprize.org/grandprize](https://scrollprize.org/grandprize), [UK Research](https://research.uky.edu/news/grand-prize-discovery-made-2000-year-old-herculaneum-scrolls), [Nader’s technical note](https://youssefnader.com/2024/02/06/the-ink-detection-journey-of-the-vesuvius-challenge/).

The winners index heading “$850,000 Grand Prize 2023” is a different tally line from the $700,000 team award in the announcement. Use the announcement figure for what the three people received, and the winners page for the full prize list: [scrollprize.org/winners](https://scrollprize.org/winners).

Winning code (ink detection and the segmentation tool) is public:

- https://github.com/ScrollPrize/villa/tree/main/ink-detection
- ThaumatoAnakalyptor is linked from that tree and from Nader’s writeup (Julian Schilliger).

This was **not** 100% of any scroll. Nader’s own note says some well-segmented regions still showed no ink, and that loss could be damage or a weak signal. Columns were partial.

## 2024: the “read 90% of four scrolls” prize was not won

The 2024 grand prize ($200,000 to read 90% of each of four already-scanned scrolls) was **not claimed**. First-letters prizes for scrolls 2, 3, and 4 and the title prize for scroll 1 were also still open when that cycle closed. Two teams (Hendrik Schilling and Sean Johnson; Paul Henderson) received $30,000 each toward automated segmentation; they were faster than 2023 but did not match the required text recovery. The winners page lists a $60,000 “First Automated Segmentation” line for December 2024; prefer the winners page plus the archived prize rules if you need the exact split. Sources: [archived 2024 prizes](https://scrollprize.org/2024_prizes), [winners](https://scrollprize.org/winners), contemporary summary [i-programmer, 2 Feb 2025](https://www.i-programmer.info/news/204-challenges/17797-vesuvius.html).

## 2025: a title inside a closed roll

In May 2025 Marcel Roth and Micha Nowak won the **$60,000 First Title** prize. Independently, Sean Johnson on the challenge team produced a segmentation of the same region. The title is on **PHerc. 172**: Philodemus, *On Vices* (papyrologist Michael McOsker: likely book 1, and not the same text as the known *On Flattery*). PHerc. 172 is unusually “ink-visible” compared with other scanned rolls. That title was, at the time of the announcement, the only recovered title among the challenge scrolls. Source: [Vesuvius Challenge Substack, First Title](https://scrollprize.substack.com/p/60000-first-title-prize-awarded).

## 2026: one surviving roll read end to end

The challenge’s June 2026 report says **PHerc. 1667 (Scroll 4)** is the first Herculaneum papyrus digitally unrolled and read continuously, end to end, under an explicit coverage bar and papyrological review. What was read is the **lower parts of about twenty-two columns** of the surviving inner core, not a restored full-height book. A preprint, “Complete virtual unwrapping and reading of a rolled Herculaneum papyrus,” is linked from the announcement and from arXiv (html: [arxiv.org/html/2606.29085v1](https://arxiv.org/html/2606.29085v1)).

The same preprint reports:

- **PHerc. Paris 4:** an optimized scan in which ink deposits are directly visible in the volume, so 3D ink segmentation can be checked against the learned surface-ink maps. That is an imaging control, not a new literary edition by itself.
- **PHerc. 139:** title and author evidence read as Philodemus, *On Gods*, book 8.

The preprint repeats the constraint: surface ink models are visibility amplifiers for experts. They are not trained on character identities, words, transcriptions, OCR targets, or lexical labels.

Most of the library is still unread. Hundreds of Naples rolls have never been scanned at this resolution. Even among scanned challenge scrolls, large regions fail because the sheet is crushed, the surface segmentation drifts, or the ink signal is absent. A title is not a book.

## What AI did not do

- It did not decipher an unknown script. The writing is Greek.
- It did not decide readings, supplements, or philosophical meaning.
- It did not invent text in regions with no ink signal. Empty predictions are a known failure mode; pseudo-labeling can also paint false ink if you do not review it.
- It did not replace autopsy or the existing editions of rolls that were physically opened. Those editions remain the comparison set.
- It did not, as of the 2024 close, deliver 90% of four scrolls. Later success on PHerc. 1667 is one damaged core plus titles on other rolls.

## Data, code, and whether a newcomer can contribute

Yes, with a narrow kind of contribution. You do not need to be a Greek papyrologist to work on segmentation, ink models, or evaluation harnesses. You do need to read the review rules: a picture of letters counts only if papyrologists can read it, and methods have to be open-sourced to win.

| Resource | URL | What it is |
|---|---|---|
| Challenge home and how to start | https://scrollprize.org/ | Current prizes, community entry |
| Data | https://scrollprize.org/data | CT volumes, surfaces, transcriptions; the 2026 announcement says CC licensing, with an ESRF archive copy |
| Winners and what is already claimed | https://scrollprize.org/winners | Do not re-solve a closed prize |
| 2023 ink-detection winner | https://github.com/ScrollPrize/villa/tree/main/ink-detection | Grand-prize models |
| EduceLab-Scrolls paper and dataset description | https://arxiv.org/abs/2304.02084 | Fragments plus rolls, aligned labels |
| Ink-detection methods paper | https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0215775 | Why carbon ink is detectable at all |
| Nader’s lab notes | https://youssefnader.com/2024/02/06/the-ink-detection-journey-of-the-vesuvius-challenge/ | What failed in 2023 |

Practical constraints:

- Volumes are huge. A laptop can explore released segment images; training on raw CT wants a GPU and disk, not a notebook alone.
- Useful newcomer work is reproducible: a segmentation that agrees with a published surface, an ink model that does not light up blank papyrus, a documented failure on a hard region.
- Do not publish a “new Greek text” from a raw heatmap. Transcription is a separate scholarly step. The contest’s own bar is that a papyrologist can read the image.

## How this differs from Linear A or the Voynich manuscript

Herculaneum has a known language, a known alphabet, and a physical measurement (CT) that contains the letters. Undeciphered scripts lack the language anchor. Virtual unwrapping does not transfer to Linear A tablets or to Voynich, which are already visible and still unread. See [ai-already-helped.md](ai-already-helped.md).
