Voynich MS: the search-free invariant instrument - 23 October 2026

Twentieth execution step for the Voynich case, and family 5's tenth
measurement, declared in `engine/voynich_homophonic.py`'s docstring
before any run beyond the probes it discloses. Every number the band
instruments produced across seven declared changes passed through a
hill-climb whose exploitation of the declared tables is disclosed in
every artifact, and the real's margin survived all seven; this
measurement removes the search entirely - no assignment search, no
candidate evaluation, no restarts, no sweep cap, no convergence
flags, no score table, no split - and prices the manuscript's raw
pair-count structure directly against the simulated encodings' raw
structure, so that no number here can ride any search's exploitation
or its budget's depth.

## Declared design of this run

- For each of the six (file, language) cells the instrument records
  and prices profiles. The real side: the manuscript's kept-adjacent
  mapped pair-count matrix over the 37 symbol alphabet (36 glyphs
  plus the word-boundary mark; unmapped events break adjacency and
  are not counted), one profile per file and shared by both language
  cells of that file.
- The simulated side: every widened band member's selected-draw
  encoding, replayed byte-identically through the declared partition
  and encoder at the frozen kind and position (the selected draw read
  from the frozen restart-budget artifact rather than re-derived,
  because re-derivation is machinery), plus the five plant encodings
  per cell and the five destroyed-adjacency floors per cell replayed
  at their standing kinds.
- The controls: each cell records the truncated standing reference's
  own plaintext stream profile, computed by the same formulas on its
  own 27-type state (729 types), a control whose width differs by
  declaration and that takes no part in any envelope.
- The declared invariant list, fixed in advance, every summary a
  relabeling invariant of a pair-count matrix: the sorted symbol
  marginals as counts and shares, the sorted pair-count multiset as
  counts and shares, the empty type count, the self-pair share, the
  top-k pair concentration at the declared k values 1, 10 and 50, and
  the pair entropy in nats per counted pair; shares and entropy
  rounded to the declared 6 decimals on every side.
- The declared verdict rule, fixed in advance and strict-all: a cell
  is shape-consistent-with-homophonic-encoding only when every
  declared invariant of the real's profile sits inside the closed
  range of its cell's simulated band's profiles (the vectors term by
  term inside the band's per-position envelope, the scalars inside
  [min, max]); any outside invariant makes the cell
  shape-outside-analogues with every outside entry recorded by
  position with its band range so a miss is audited, not summarized.
  No scalar margin is formed. The state note declared beside them:
  the real's profile prices kept-adjacent mapped pairs while an
  encoding's prices every adjacent pair of its full stream; the
  totals differ for that structural reason, every share-valued
  invariant normalises by its own total, the empty count is a raw
  count tied to its own total and recorded in that context, and the
  latin band's members are the roster's own truncated texts whose
  totals range from 45,490 to the full standing lengths - the
  roster's own declared construction disclosed in every prior
  artifact, so the latin envelopes are size-mixed by that standing
  construction.
- A bridge gate declared before the run and enforced in code: the
  six cells' counted pairs, all 45 members' file, ebook and
  plant_length records and the 30 floors' pair totals, re-derived
  fresh, must equal the frozen restart-budget artifact's stored
  values field for field; the plants' totals are verified inside
  every cell instead (each against its standing source's truncated
  length minus one, a length the predecessors never stored frozen);
  any divergence aborts with nothing written. The selected-draw
  indexes are read, not re-derived.
- Corpus discipline: no new corpus files and no new candidates - the
  band population is the frozen widened band's declared roster, the
  plants and the plaintext controls are the standing references'
  frozen files, all stored raw with their markers and processed by
  the standing declared processing. No score table is built or used.

## The measured facts

- The first declared gate anchored the plants' totals against the
  frozen band's first member's stored length and its 15 latin rows
  failed: the standing latin reference's own truncated length was
  never stored frozen, so a gate row cannot anchor to it. The repair
  is declared in the docstring probes (the plant totals moved into
  every cell as the plants_at_source_identity identity with each
  standing source's truncated length recorded as a new declared
  fact; the floors, the streams and the members' identity fields
  kept in the gate) and the repaired gate ran at 171 fields
  compared, no problem.
- Pre-run probes, recorded verbatim before the run: the three real
  profiles - ZL events 218,663, kept 218,537, unmapped 126, pairs
  218,415, empty types 943, self-pair share 0.045162, top shares
  0.066625, 0.355937 and 0.859602 at k 1, 10 and 50, entropy 4.203;
  GC events 186,708, kept 184,939, unmapped 1,769, pairs 183,199,
  empty 645, self 0.009722, top shares 0.078745, 0.352327 and
  0.789781, entropy 4.500206; IT events 220,532, kept 220,532,
  unmapped 0, pairs 220,531, empty 1012, self 0.044039, top shares
  0.067451, 0.356453 and 0.867039, entropy 4.180814 - and the first
  two cells' verdicts printed ahead of the run (ZL english
  shape-outside-analogues with all eight invariant tests outside,
  ZL latin the same), with the recorded plaintext controls (ZL
  english entropy 5.139035, empty 260, self 0.019404, top_1
  0.033115 on 729 types; ZL latin entropy 5.06327, empty 339, self
  0.013775, top_1 0.026671) and the disclosed caution that the
  probes do not decide the artifact.
- The artifact run's headline, all six cells:
  shape-outside-analogues, every one of the eight invariant tests
  outside in every cell. The vector extents: ZL english 37 of 37
  symbol positions and 902 of 1369 pair positions outside, ZL latin
  34 and 838, GC english 34 and 904, GC latin 34 and 854, IT english
  37 and 908, IT latin 36 and 855.
- The scalar directions, recorded rather than summarized: the real's
  pair entropy sits below its band's minimum in every cell (4.203
  against [5.7732, 5.904914] ZL english, 4.500206 against
  [5.778682, 5.922013] GC english, 4.180814 against
  [5.772971, 5.905219] IT english; latin bands [5.923406, 6.050813],
  [5.923931, 6.050891], [5.923107, 6.050902]); its top-k shares sit
  above their bands' maxima in every cell (top_50 0.859602 against
  [0.414205, 0.443301] ZL english, 0.789781 against
  [0.413675, 0.443213] GC english, 0.867039 against
  [0.414368, 0.443484] IT english); its empty type count sits above
  (943 against [325, 447] ZL, 645 against [319, 454] GC, 1012
  against [327, 446] IT english); and its self-pair share's
  direction splits: above the band in the ZL and IT cells (0.045162
  against [0.012192, 0.01645] ZL english, 0.044039 against
  [0.012221, 0.016664] IT english) while below in the GC cells
  (0.009722 against [0.012367, 0.016764] GC english and
  [0.009893, 0.016417] GC latin).
- The band's own facts: the english cells' seven members all measure
  218,662, 186,707 and 220,531 profile totals (ZL, GC, IT - the
  roster's full-length encodings); the latin cells' eight members'
  totals are the roster's own truncated lengths, 45,490 to
  218,662, 186,707 and 220,531 per cell, recorded member by member;
  the members' entropies run 5.7732 to 5.904914 (ZL english),
  5.778682 to 5.922013 (GC english), 5.772971 to 5.905219 (IT
  english) and 5.923107 to 6.050902 across the latin cells; every
  member's file, ebook, plant_length and selected_draw_index replay
  the frozen restart-budget artifact exactly.
- The plants and floors: all 30 plants carry the
  plants_at_source_identity identity true (each plant's total
  exactly its standing source's truncated length minus one, the
  standing latin sources long enough for all three files at 218,663,
  186,708 and 220,532); all 30 floors price every cell's counted
  pairs exactly (the total is shuffle-invariant) and sit outside the
  real's profile in the recorded direction - entropy above the
  real's (5.371898 to 5.519104 against the real's 4.180814 to
  4.500206), top-pair share below, empty types below, self-pair
  share above in every cell.
- The plaintext controls, recorded not tested, standing beside the
  verdict on their 729-type states: entropies 5.139035, 5.139139 and
  5.139068 (ZL, GC, IT english) and 5.06327, 5.063406 and 5.062979
  (latin), self shares 0.013631 to 0.019439, top_1 shares 0.026544 to
  0.033115. The structural gradient they disclose: the members'
  encodings raise entropy well above their own plaintext sources
  (5.772971 to 6.050902), while the real sits below everything
  measured here (4.180814 to 4.500206).

## The exclusion format's outcome, stated exactly

The declared exclusion keys to the 36-slot class under the inherited
add-one form and this artifact re-scopes nothing: a search-free
verdict is structure evidence and the band instruments' verdicts
stand untouched by this artifact's numbers, declared in the artifact
and in the docstring before the run. So this measurement adds no
exclusion and no identification: the family stays open at priority 1.

## The disclosure the verdicts ride on

This is the family's first search-free instrument, and its answer's
direction cuts the other way from the band instruments': where the
band instruments record the real's held-out score above every
member's under disclosed machinery exploitation, this instrument
records that the real's raw pair profile sits outside the simulated
encodings' range on every declared invariant in all six cells. The
two answers coexist by declaration and are recorded side by side;
neither re-scopes the other. The structural reading, recorded as
structure and not as language: under the declared partition and
encoder, the manuscript's raw pair-count profile is far more
concentrated (its top-50 share carries 0.79 to 0.87 of all counted
pairs against every simulated encoding's 0.34 to 0.44, and its most
frequent pair alone carries 0.066625 to 0.078745 against every
simulated encoding's 0.021142 to 0.034072), emptier (645 to 1012
unused pair types against the bands' 241 to 510 empties), and less
entropic (4.18 to 4.50 nats against every simulated encoding's
5.77 to 6.05) than any homophonic encoding of the sampled prose the
declared machinery can produce; the step from plaintext prose to its
own homophonic encodings raises entropy by 0.634 to 0.988 nats,
while the real stands 1.28 to 1.72 nats below every encoding of its
own cell and 0.56 to 0.96 nats below the plaintext controls
themselves.
The size caveats stay attached: the real's matrix prices
kept-adjacent pairs and the encodings' price full streams, the
totals differ for that reason, the shares normalise by their own
totals, and the latin envelopes are size-mixed by the roster's
standing construction disclosed since family 4. The floors' role is
answered: the same totals shuffled give flatter pools (less peaked,
more entropy, fewer empties than the real in every cell), so the
destroyed control sits outside the real and outside the bands too.
This measurement adds no identification, no closure and no exclusion;
no mapping is published, no assignment is stored,
plaintext_recovered_percent stays 0, and nothing here is a reading.

## Next

Family 5 stays open at priority 1. The measured next question this
artifact hands to the ledger: the outsides sit at both ends of the
profiles and the boundary mark is each profile's most frequent
symbol, so the next instrument isolates the boundary mark's role -
the declared boundary-mark re-instrument: the same search-free
invariants and the same strict-all rule, with the word-boundary
mark's symbol excluded from every profile's state space on both
sides (the real's kept-adjacent pair matrix and every simulated
encoding recomputed over the 36 glyph symbols alone, 1296 types,
including the boundary-carried pairs removed from both sides the
same way), testing whether the outsides ride the boundary mark's own
concentration or the interior pair structure; the corpus-breadth
angle in the same search-free form stays the later candidate;
declared on its own branch in its own docstring before any run, the
family stays open unless the declared exclusion format fires, and
family 4's exclusion stands untouched by this artifact.
