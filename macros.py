from kmk.keys import KC
from kmk.modules.macros import Tap

# --- Helpers ---
def dead_fix(code):
    return KC.MACRO(Tap(code), Tap(KC.SPC))

def pair_macro(open_k, close_k):
    return KC.MACRO(Tap(open_k), Tap(close_k), Tap(KC.LEFT))

# --- Dead Key Fixes ---
US_QUOT = dead_fix(KC.QUOTE)
US_DQUO = dead_fix(KC.LSFT(KC.QUOTE))
US_GRV  = dead_fix(KC.GRAVE)
US_TILD = dead_fix(KC.LSFT(KC.GRAVE))
US_CIRC = dead_fix(KC.LSFT(KC.N6))

# --- Text/Symbol Macros ---
MACRO_PAR = pair_macro(KC.LPRN, KC.RPRN)
MACRO_CRL = pair_macro(KC.LCBR, KC.RCBR)
MACRO_SQR = pair_macro(KC.LBRC, KC.RBRC)
MACRO_ANG = pair_macro(KC.LABK, KC.RABK)
MACRO_QUO = pair_macro(KC.QUOT, KC.QUOT)
MACRO_DBL = pair_macro(KC.DQUO, KC.DQUO)
MACRO_GRV = pair_macro(KC.GRV,  KC.GRV)

ACTIVATE_FUN = KC.MACRO(Tap(KC.MO(3))) # Example usage
