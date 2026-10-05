# The slow searches are now read, not rerun

5 October 2026. Not a reading. No letter string is stored.

A fresh process spent about 14 seconds rebuilding the hash chain. Almost all of that was seven searches that had only been remembered inside one process: the delay, the book key, the solver swarm, the group routes, the autokey, the angles, and the digit routes. The group-end shuffle in the checks was the next cost, about a quarter of a second, and it always came out the same.

Those eight results now sit in `engine/data/swarm_cache`, the same store as the other frozen scores. The scores themselves did not change. A later process reads them. The hash chain is also kept for the rest of that process, so a second call does not hash the whole chain again.

Measured on this machine: the first chain dropped from 13.9 seconds to 0.58 seconds. The second call dropped from 0.87 seconds to nothing measurable. 45 frozen files claim no reading.

No letter string is stored.
