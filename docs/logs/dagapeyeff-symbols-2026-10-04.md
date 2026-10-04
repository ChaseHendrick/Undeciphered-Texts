# One cell repeating is not the column

4 October 2026. 195,000 scores. No letter string is stored.

The rare cells share a column. The next question is whether that is just one cell repeating, or several different cells meeting.

Cell 82 is the best candidate for a repeat. It sits in one column six times, in a pair and then a triple at the bottom of that column:

```
85 82 82 81 82 63 81 91 91 64 84 82 82 82
```

Six is the most any single cell manages in any column. The search is allowed to pick the luckiest cell. 738 of 20,000 random grids still do as well or better. The same search across widths 2 through 28, allowed to pick the luckiest width too, is closest at width 14, and 187 of 5,000 random grids still match that width. One cell does not own a column.

The downward stutter is ordinary as well. The longest run of the same cell down a column is 3. 10,855 of 20,000 random grids have a run at least that long.

The rare cells are a different pattern. Five of them, from four different cells, sit in one column, and 0 of 20,000 random grids match that. Their rows are 2, 6, 7, 8, and 9, which includes four rows in a row. Given that they already share a column, 100 of the 2,002 ways to place five rows are at least that bunched. The bunch is not a second fact. The meeting of different rare cells is the fact. A single cell repeating is not.

No letter string is stored.
