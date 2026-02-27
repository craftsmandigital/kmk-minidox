from kmk.keys import KC
from kmk.modules.macros import Tap

# Import the LEAD key so you don't have to define it twice.
# This works because behaviors.py does NOT import this file.
from behaviors import LEAD

TASK_TRIGGER = 28 # Å
# --- Sequence Leader Configuration ---
# Format: { LEADER_KEY: [ ((COORD_1, COORD_2), OUTPUT), ... ] }
LEADER_SEQUENCES = {
    LEAD: [
       
        # Leader -> Pos q  Closing window
        ((0,), KC.LALT(KC.F4)),         
        # Leader -> Pos 4 (T)  To copy screen content with power tools 
        ((4,), KC.LWIN(KC.LSFT(KC.T))),
       
        # hitting an app on the windows taskbar
        ((TASK_TRIGGER, 1), KC.LWIN(KC.N7)),
        ((TASK_TRIGGER, 2), KC.LWIN(KC.N8)),
        ((TASK_TRIGGER, 3), KC.LWIN(KC.N9)),
        ((TASK_TRIGGER, 11), KC.LWIN(KC.N3)),
        ((TASK_TRIGGER, 12), KC.LWIN(KC.N2)),
        ((TASK_TRIGGER, 13), KC.LWIN(KC.N1)),
        ((TASK_TRIGGER, 21), KC.LWIN(KC.N4)),
        ((TASK_TRIGGER, 22), KC.LWIN(KC.N5)),
        ((TASK_TRIGGER, 23), KC.LWIN(KC.N6)),
    ]
}


