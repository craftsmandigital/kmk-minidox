from kmk.keys import KC
from kmk.modules.macros import Tap

# Import the LEAD key so you don't have to define it twice.
# This works because behaviors.py does NOT import this file.
from behaviors import LEAD


# --- Sequence Leader Configuration ---
# Format: { LEADER_KEY: [ ((COORD_1, COORD_2), OUTPUT), ... ] }
LEADER_SEQUENCES = {
    LEAD: [
        # Leader -> Pos 26 (M) -> Pos 12 (D)
        ((26, 12), KC.MACRO("idibidi", Tap(KC.ENT), "dabada", Tap(KC.ENT))),
        
        # Leader -> Pos 0 (Q) -> Pos 1 (W)
        ((0, 1), KC.MACRO("Hello")),
        
        # Leader -> Pos 7 (I)
        ((7,), KC.MACRO("Nock Nock")),
    ]
}
