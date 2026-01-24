from kmk.keys import KC
from kmk.modules.macros import Tap, Delay
from extensions import StickyLeader
from macros import * # Import macros to use them as triggers/outputs
from kmk.modules.capsword import CapsWord

from extensions import MagicKey, Seq
caps_word = CapsWord()
caps_word.keys_ignored.append(KC.DOT)

# --- Layer Indices ---
LAYER_BASE = 0
LAYER_SYM  = 1
LAYER_NUM  = 2
LAYER_FUN  = 3
LAYER_NAV  = 4


# --- Custom Keys ---
LEAD = KC.F24
MAGIC = KC.F23


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
ALT_TAB_X = KC.SM(KC.TAB, KC.LALT)
ALT_TAB = KC.LALT(KC.TAB)
WordR   = KC.LCTL(KC.RIGHT)
WordL   = KC.LCTL(KC.LEFT)
RClick  = KC.LSFT(KC.F10)


# Aliases
TRNS = KC.TRNS
XXXX = KC.NO




# -------------------------------------------------------------------------
# --- Sticky Leader Configuration ---
# -------------------------------------------------------------------------
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


# -------------------------------------------------------------------------
# --- MagicKey Configuration ---
# -------------------------------------------------------------------------
MAGIC_DEFAULT = KC.SPC

# Define Triggers
# Format: { TRIGGER_EVENT : NEW_MAGIC_OUTPUT }
MAGIC_TRIGGERS = {
    # Scenario 1: Auto-Capitalization
    # Context: After typing a period
    # Action: Space, then One-Shot Shift for the next letter
    KC.DOT: KC.MACRO(Tap(KC.SPC), Tap(KC.SK(KC.LSFT))),
    # KC.DOT: KC.SK(KC.LSFT),
    KC.ENT: KC.SK(KC.LSFT),

    # Holding CAPS WORD on, even if space is pressed in a smart way
    KC.CW: KC.MACRO(Tap(KC.SPC), Delay(100), KC.CW),


    # Scenario 3: Combo Spacing
    # Context: After triggering any bracket/quote pair
    # Action: Move Right (outside the pair), then add a Space
    # Result: "(bla bla bla|)" -> "(bla bla bla) |"
    (MACRO_PAR, MACRO_CRL, MACRO_SQR, MACRO_ANG, MACRO_QUO, MACRO_DBL, MACRO_GRV): KC.MACRO(Tap(KC.RIGHT), Tap(KC.SPC)), 
    # Scenario 4: Reset
    # If I press Space, Magic Key resets to Backspace (example)
    # KC.SPC: KC.BSPC,

    # Home -> Magic Key selects to end of line
    KC.HOME: KC.LSFT(KC.END),


    # 3. Trigger: You type "def" (Python)
    #    Magic Key becomes: "return" (The logical end of a function)
    Seq(KC.D, KC.E, KC.F): KC.MACRO(
        Tap(KC.ENT), "return "
    ),

    # -------------------------------------------------------------------------
    # WORKFLOW A: The "Clipboard Loop"
    # Story: Copy -> Switch App -> Paste -> Done
    # -------------------------------------------------------------------------
    
    # 1. Trigger: You press Copy (Ctrl+C)
    #    Magic Key becomes: Alt+Tab (Switch Window)
    (Copy, Paste): ALT_TAB,

    # 2. Trigger: You press Alt+Tab (Switching apps)
    #    Magic Key becomes: Paste (Ctrl+V)
    ALT_TAB: Paste,

    # 3. Trigger: You press Paste (Ctrl+V)
    #    Magic Key becomes: Enter (To submit the form/command)
    # Paste: KC.ENT,


}

# Initialize the module
magic_key_mod = MagicKey(
    magic_key=MAGIC, 

    triggers=MAGIC_TRIGGERS, 
    default_behavior=MAGIC_DEFAULT
)
