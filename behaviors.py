from kmk.keys import KC
from kmk.modules.macros import Tap
from extensions import StickyLeader

# --- Layer Indices ---
LAYER_BASE = 0
LAYER_SYM  = 1
LAYER_NUM  = 2
LAYER_FUN  = 3
LAYER_NAV  = 4


# --- Custom Keys ---
LEAD = KC.F24


# Nordic Characters
NO_AE = KC.RALT(KC.Z)
NO_OE = KC.RALT(KC.L)
NO_AA = KC.RALT(KC.W)

# Sticky / Hold-Tap
# SYM_SK  = KC.SK(KC.MO(LAYER_SYM))
# NUM_SK  = KC.SK(KC.MO(LAYER_NUM))
# Tap = LEAD, Hold = Momentary Layer NUM
# NUM_LEAD_LT = KC.LT(LAYER_NUM, LEAD)
# NUM_LEAD_LT  = KC.SK(KC.MO(LAYER_NUM))
# NUM_LEAD_LT = KC.HT(LEAD, KC.MO(LAYER_NUM), prefer_hold=True) 
# NUM_LEAD_LT = KC.HT(KC.SK(LAYER_SYM), KC.MO(LAYER_NUM)) 
# NUM_LEAD_LT = KC.HT(KC.SK(LAYER_SYM), KC.MO(LAYER_NUM)) 
# Alternative (only if OSL doesn't work)
SYM_NUM_HT = KC.HT(KC.SK(KC.MO(LAYER_SYM)), KC.MO(LAYER_NUM))
FUN_SK  = KC.SK(KC.MO(LAYER_FUN))
NAV_HT  = KC.HT(KC.TG(LAYER_NAV), KC.MO(LAYER_NAV)) 

# Sticky Mods
OS_LCTL = KC.SK(KC.LCTL)
OS_LSFT = KC.SK(KC.LSFT)
OS_LALT = KC.SK(KC.LALT)
OS_LGUI = KC.SK(KC.LGUI)

# Nav Shortcuts
SelAll  = KC.LCTL(KC.A)
Paste   = KC.LCTL(KC.V)
PasteU  = KC.LSFT(Paste)
PasteM  = KC.LCTL(KC.G) # this is chortcut to my clipboard manager
Copy    = KC.LCTL(KC.C)
Cut     = KC.LCTL(KC.X)
Undo    = KC.LCTL(KC.Z)
Redo    = KC.LCTL(KC.Y)
ALT_TAB = KC.SM(KC.TAB, KC.LALT)
WordR   = KC.LCTL(KC.RIGHT)
WordL   = KC.LCTL(KC.LEFT)
RClick  = KC.LSFT(KC.F10)


# Aliases
TRNS = KC.TRNS
XXXX = KC.NO

# --- Sticky Leader Configuration ---
MAP_L = {
    KC.F: KC.LSFT,
    KC.D: KC.LCTL,
    KC.S: KC.LALT,
    KC.A: KC.LGUI,
}

MAP_R = {
    KC.J: KC.LSFT,
    KC.K: KC.LCTL,
    KC.L: KC.LALT,
    NO_OE: KC.LGUI, 
}

# Initialize the module instance
sticky_leader_mod = StickyLeader(trigger_key=LEAD, left_map=MAP_L, right_map=MAP_R)
