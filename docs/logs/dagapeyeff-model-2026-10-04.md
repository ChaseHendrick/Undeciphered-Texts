# The language model does not like the flattering counts

4 October 2026. No letter string is stored.

The most common cell was given the most common English letter, and so on. That string is not a key. It was scored with the solver's quadgram model and its neural trigram. English of this length scores -1.553 per quadgram and -2.495 on the neural model.

The printed cells score -3.6316 and -3.2313. The regrouping 01432, whose chi-square looks close to English, scores -3.6352 and -3.3504. The lower chi-square made the language-model score worse, not better.

Each string was shuffled 200,000 times, 400,000 scores per model across the two strings. On the quadgram model, 177,295 shuffles beat the printed cells and 151,728 beat the regrouping. The best shuffle reached -3.107, still far from -1.553.

The solver refuses the labeling. No string is kept.

The chain ends at `5ff05c351d6dac071d3a572c83bf363be98b2206bd16f4b71783f83f179be40c`.

No letter string is stored.
