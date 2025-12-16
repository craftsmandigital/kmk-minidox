from kmk.keys import KC
from kmk.modules.macros import Tap


# Nordic Keyboard Layout for the us international keyboard Layout

# --- 1. THE HELPER FUNCTION ---
# This function takes any key (like KC.QUOTE) and returns a Macro 
# that taps that key followed immediately by Space.
def dead_fix(key_code):
    return KC.MACRO(Tap(key_code), Tap(KC.SPC))

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

CURLY_DOUBLE = KC.MACRO(
    Tap(KC.LCBR),
    Tap(KC.RCBR),
    #Delay(1000),
    Tap(KC.LEFT),
)

