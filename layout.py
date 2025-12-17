from kmk.keys import KC
from kmk.modules.macros import Tap


# Nordic Keyboard Layout for the us international keyboard Layout

# --- 1. THE HELPER FUNCTION ---
# This function takes any key (like KC.QUOTE) and returns a Macro 
# that taps that key followed immediately by Space.
def dead_fix(key_code):
    return KC.MACRO(Tap(key_code), Tap(KC.SPC))


def pairs_and_left(key_code1, key_code2):
    return KC.MACRO(Tap(key_code1), Tap(key_code2), Tap(KC.LEFT))


# --- 2. GENERATE THE KEYS ---
# Now we just call the function for the keys we need.

# Fix all symbolvs that are dead keys in the us international layout
US_QUOT = dead_fix(KC.QUOTE)             # '
US_DQUO = dead_fix(KC.LSFT(KC.QUOTE))    # "
US_GRV  = dead_fix(KC.GRAVE)             # `
US_TILD = dead_fix(KC.LSFT(KC.GRAVE))    # ~
US_CIRC = dead_fix(KC.LSFT(KC.N6))       # ^

# Define Nordic letters (Standard US-Int shortcuts)
NO_AE = KC.RALT(KC.Z) # Æ
NO_OE = KC.RALT(KC.L) # Ø
NO_AA = KC.RALT(KC.W) # Å


MACRO_PAR = pairs_and_left(KC.LPRN, KC.RPRN)
MACRO_CRL = pairs_and_left(KC.LCBR, KC.RCBR)
MACRO_SQR = pairs_and_left(KC.LBRC, KC.RBRC)
MACRO_ANG = pairs_and_left(KC.LABK, KC.RABK)
MACRO_QUO = pairs_and_left(KC.QUOT, KC.QUOT)
MACRO_DBL = pairs_and_left(KC.DQUO, KC.DQUO)
MACRO_GRV = pairs_and_left(KC.GRV,  KC.GRV)



