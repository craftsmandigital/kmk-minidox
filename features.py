from kmk.keys import KC
from kmk.modules.macros import Macros, Tap
from kmk.modules.combos import Chord, Sequence

# -------------------------------------------------------------------------
# 1. LAYER INDICES
# -------------------------------------------------------------------------
LAYER_BASE = 0
LAYER_SYM  = 1
LAYER_NUM  = 2
LAYER_FUN  = 3
LAYER_NAV  = 4


# -------------------------------------------------------------------------
# 2. HELPER FUNCTIONS
# -------------------------------------------------------------------------
def dead_fix(code):

    """Fixes dead keys by tapping the key followed by Space."""
    return KC.MACRO(Tap(code), Tap(KC.SPC))

def pair_macro(open_k, close_k):
    """Types a pair of brackets and moves cursor left."""
    return KC.MACRO(Tap(open_k), Tap(close_k), Tap(KC.LEFT))

# -------------------------------------------------------------------------
# 3. CUSTOM KEYS & ALIASES
# -------------------------------------------------------------------------
# Leader Key
LEAD = KC.F24

# Nordic Characters (US-Int AltGr codes)
NO_AE = KC.RALT(KC.Z)
NO_OE = KC.RALT(KC.L)
NO_AA = KC.RALT(KC.W)

# Dead Key Fixes
US_QUOT = dead_fix(KC.QUOTE)
US_DQUO = dead_fix(KC.LSFT(KC.QUOTE))
US_GRV  = dead_fix(KC.GRAVE)
US_TILD = dead_fix(KC.LSFT(KC.GRAVE))
US_CIRC = dead_fix(KC.LSFT(KC.N6))

# Sticky / One-Shot Logic
SYM_SK  = KC.SK(KC.MO(LAYER_SYM))
NUM_SK  = KC.SK(KC.MO(LAYER_NUM))
FUN_SK  = KC.SK(KC.MO(LAYER_FUN))
NAV_HT  = KC.HT(KC.TG(LAYER_NAV), KC.MO(LAYER_NAV)) # Tap to Toggle, Hold for Momentary


# Sticky Modifiers
OS_LCTL = KC.SK(KC.LCTL)
OS_LSFT = KC.SK(KC.LSFT)
OS_LALT = KC.SK(KC.LALT)
OS_LGUI = KC.SK(KC.LGUI)

# Nav Shortcuts

SelAll  = KC.LCTL(KC.A)
Paste   = KC.LCTL(KC.V)
Copy    = KC.LCTL(KC.C)
Cut     = KC.LCTL(KC.X)
Undo    = KC.LCTL(KC.Z)
Redo    = KC.LCTL(KC.Y)
ALT_TAB = KC.SM(KC.TAB, KC.LALT)

# Visual Aliases
TRNS = KC.TRNS
XXXX = KC.NO

# -------------------------------------------------------------------------
# 4. MACROS
# -------------------------------------------------------------------------
MACRO_PAR = pair_macro(KC.LPRN, KC.RPRN) # ()
MACRO_CRL = pair_macro(KC.LCBR, KC.RCBR) # {}
MACRO_SQR = pair_macro(KC.LBRC, KC.RBRC) # []
MACRO_ANG = pair_macro(KC.LABK, KC.RABK) # <>
MACRO_QUO = pair_macro(KC.QUOT, KC.QUOT) # ''
MACRO_DBL = pair_macro(KC.DQUO, KC.DQUO) # ""
MACRO_GRV = pair_macro(KC.GRV,  KC.GRV)  # ``

# Macro to safely activate Sticky Layer from Combo
ACTIVATE_FUN = KC.MACRO(Tap(FUN_SK))

# -------------------------------------------------------------------------
# 5. COMBOS
# -------------------------------------------------------------------------
COMBO_LIST = [
    # Leader Sequences (Right Hand)
    Sequence((LEAD, KC.F), KC.SK(KC.RSFT), timeout=1000),
    Sequence((LEAD, KC.D), KC.SK(KC.RCTL), timeout=1000),
    Sequence((LEAD, KC.S), KC.SK(KC.LALT), timeout=1000), # Fixed RALT->LALT
    Sequence((LEAD, KC.A), KC.SK(KC.RGUI), timeout=1000),
   
    # Leader Sequences (Left Hand)
    Sequence((LEAD, KC.J), KC.SK(KC.LSFT), timeout=1000),
    Sequence((LEAD, KC.K), KC.SK(KC.LCTL), timeout=1000),
    Sequence((LEAD, KC.L), KC.SK(KC.LALT), timeout=1000),
    Sequence((LEAD, NO_OE), KC.SK(KC.LGUI), timeout=1000),
    
    # Layer Triggers
    Chord((KC.BSPC, NUM_SK), ACTIVATE_FUN), # Backspace + Num -> Fun Layer

    # Brackets & Quotes
    Chord((KC.MINS, KC.QUES), MACRO_PAR),
    Chord((KC.LCBR, KC.RCBR), MACRO_CRL),

    Chord((KC.LPRN, KC.RPRN), MACRO_PAR),
    Chord((KC.LABK, KC.RABK), MACRO_ANG),
    Chord((KC.LBRC, KC.RBRC), MACRO_SQR),
    Chord((US_QUOT, KC.SCLN), MACRO_QUO), 
    Chord((US_DQUO, KC.COLN), MACRO_DBL),
    Chord((US_GRV,  US_TILD), MACRO_GRV),
]

