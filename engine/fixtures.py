"""Known plaintexts used by the demo and the recovery tests.

The prose is original and is not copied from the language-model sample, so a
successful solve is not a lookup of a stored sentence.
"""

from __future__ import annotations

CAESAR_PLAIN = (
    "The harbor bell rang twice before dawn, and the small boats left the quay "
    "with nets folded on the deck. A thin mist hid the far shore, but the crew "
    "knew the channel by the sound of water against stone."
)

VIGENERE_PLAIN = (
    "A printer on Oak Street kept the presses running after dark whenever a ship "
    "brought fresh paper. He mixed the ink himself and checked each sheet against "
    "the copy the editor had marked. Customers wanted notices of auctions, lists of "
    "timber prices, and the names of passengers who had booked a cabin. The apprentice "
    "learned to lock the type tightly so the lines would not dance. When the last form "
    "was washed the room smelled of oil and wet rag paper, and the printer walked home "
    "along the canal with ink still on his cuffs."
)

SUBSTITUTION_PLAIN = (
    "Geologists followed the creek upstream until the gravel turned from gray river "
    "stone to a band of red shale. They measured the dip of each layer and wrote the "
    "numbers in a field book before the rain could smear them. One outcrop showed "
    "ripples that had hardened when the water was shallow and warm. Another held "
    "broken shells the size of a thumbnail. The party ate lunch on a flat boulder and "
    "argued, without any heat, about whether the ridge had been a beach or a delta. "
    "By late afternoon they had samples enough to justify the long walk back to the wagon. "
    "A quick extra box of quartz fixed the last gap in the section."
)

CAESAR_SHIFT = 11
VIGENERE_KEY = "HARBOR"
SUBSTITUTION_KEY = "QWERTYUIOPASDFGHJKLZXCVBNM"
DEMO_SEED = 20261002
