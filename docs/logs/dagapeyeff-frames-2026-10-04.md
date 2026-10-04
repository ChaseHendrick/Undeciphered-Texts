# No language assumed

4 October 2026. 40,000 shuffles. No letter string is stored.

Nothing here is scored as English, French, or any other language. The digits are asked two questions: do even and odd places already use different digits, and does one pair predict the next.

There are 395 digits. The even places use exactly the digits 0, 6, 7, 8, and 9. The odd places use exactly 1, 2, 3, 4, and 5, except one digit. Index 393 is a 0 sitting on an odd place. It is the only digit in the whole string on the wrong side of that split. The four zeros are at indexes 194, 392, 393, and 394. Only 393 is on the wrong side. Dropping the last three digits because they "look like filler" throws away two zeros that sit on the side where 0 already belongs. They are left over because the middle one breaks the pair, not because the split rejects them.

0 of 20,000 shuffles of the same digits are that clean. The split is in the order. It is not an assumption, and it is not forced by how often each digit occurs.

The 196 pairs that stop before that broken pair do not predict their neighbors. Their mutual information is 0.5706. 16,611 of 20,000 shuffles of those pairs are at least as predictable. Order, past the split itself, is not doing extra work. No alphabet of letters was required for that comparison.

No letter string is stored.
