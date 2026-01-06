from kmk.keys import KC
from kmk.modules.combos import Chord
from macros import *

# Define Chords
COMBO_LIST = [
    Chord((KC.MINS, KC.QUES), MACRO_PAR),
    Chord((KC.LCBR, KC.RCBR), MACRO_CRL),
    Chord((KC.LPRN, KC.RPRN), MACRO_PAR),
    Chord((KC.LABK, KC.RABK), MACRO_ANG),
    Chord((KC.LBRC, KC.RBRC), MACRO_SQR),
    Chord((US_QUOT, KC.SCLN), MACRO_QUO), 
    Chord((US_DQUO, KC.COLN), MACRO_DBL),
    Chord((US_GRV,  US_TILD), MACRO_GRV),
]
