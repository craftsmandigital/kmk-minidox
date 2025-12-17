print("--- STARTING KEYBOARD ---")

# import board
import digitalio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.split import Split, SplitType, SplitSide
from kmk.modules.layers import Layers
from kmk.modules.sticky_keys import StickyKeys
from kmk.modules.combos import Combos, Chord, Sequence
# from kmk.modules.macros import Macros, Press, Release, Tap
from kmk.modules.macros import Macros


# 1. Import our new, custom OSL module
#from osl import OSL
import hardware  # Pins (Local Library)


# --- INITIAL SETUP ---
keyboard = KMKKeyboard()
keyboard.debug_enabled = True  # <--- ADD THIS LINE

# 1. Layers (Always first)
keyboard.modules.append(Layers())

# 2. HoldTap (If you use it)
# keyboard.modules.append(HoldTap())

# 3. Combos (MUST be before Macros!)
# This ensures Combos only looks at your fingers, not at what Macros type.
combos = Combos()
keyboard.modules.append(combos)

# 4 Macros
# macros = Macros()
keyboard.modules.append(Macros())
#keyboard.modules.append(OSL())  # This enables our custom KC.OSL

# 5. Sticky Keys (Last)?dfs?"s?+?a?a-?-??--??--?-??--?-?-?-?-?-?-??-s-?--?-??--??-
keyboard.modules.append(StickyKeys())


import layout    # Custom Keys (Nordic + Dead Fixes)  (Local Library)
# 1. Define a placeholder key for "Leader"
# We use F24 because it rarely does anything on a PC.
LEAD = KC.F24

# 2. Define the Sequences
# Sequence((FirstKey, SecondKey), Action, timeout=ms)
combos.combos = [
    Sequence((LEAD, KC.F), KC.SK(KC.RSFT), timeout=1000),
    Sequence((LEAD, KC.D), KC.SK(KC.RCTL), timeout=1000),
    Sequence((LEAD, KC.S), KC.SK(KC.RALT), timeout=1000),
    Sequence((LEAD, KC.A), KC.SK(KC.RGUI), timeout=1000),
   
    Sequence((LEAD, KC.J), KC.SK(KC.LSFT), timeout=1000),
    Sequence((LEAD, KC.K), KC.SK(KC.LCTL), timeout=1000),
    Sequence((LEAD, KC.L), KC.SK(KC.LALT), timeout=1000),
    Sequence((LEAD, layout.NO_OE), KC.SK(KC.LGUI), timeout=1000),
    
    Chord((KC.MINS, KC.QUES), layout.CURLY_DOUBLE),
]
# combos.combos = [
#     # Leader -> J (28) -> Sticky Ctrl
#     Sequence((37, 28), KC.SK(KC.LCTL), timeout=1000),
#
#     # Leader -> K (27) -> Sticky Shift
#     Sequence((37, 27), KC.SK(KC.LSFT), timeout=1000),
#
#     # Leader -> L (26) -> Sticky Alt
#     Sequence((37, 26), KC.SK(KC.LALT), timeout=1000),
#
#     # Leader -> ; (25) -> Sticky GUI (Pinky neighbor)
#     Sequence((37, 25), KC.SK(KC.LGUI), timeout=1000),
# ]


# --- 1. JUMPER DETECTION ---
jumper = digitalio.DigitalInOut(hardware.SIDE_DETECTION_PIN)
jumper.direction = digitalio.Direction.INPUT
jumper.pull = digitalio.Pull.UP


is_right = False
if not jumper.value:
    is_right = True

# --- 2. SPLIT CONFIGURATION ---

split = Split(
    split_type=SplitType.UART,
    data_pin=hardware.SPLIT_UART_PIN,
    use_pio=True,
    uart_flip=True
)

if is_right:
    split.split_side = SplitSide.RIGHT
else:
    split.split_side = SplitSide.LEFT

keyboard.modules.append(split)

# --- 3. PINS & MATRIX (The Fix) ---
# We use the SAME pin order for both sides.
# Because you wired the Right side mirrored (GP2=Inner), 
# we do NOT need to reverse the list in software.

# Order: GP2 -> GP3 -> GP4 -> GP5 -> GP28
keyboard.col_pins = hardware.COL_PINS
keyboard.row_pins = hardware.ROW_PINS

keyboard.diode_orientation = DiodeOrientation.COL2ROW


# -------------------------------------------------------------------------
# LAYERS & MODIFIERS
# -------------------------------------------------------------------------
LAYER_BASE = 0
LAYER_SYM  = 1
LAYER_NUM  = 2
LAYER_FUN  = 3
LAYER_NAV  = 4

SYM_SK_MO = KC.SK(KC.MO(LAYER_SYM))
NUM_SK_MO = KC.SK(KC.MO(LAYER_NUM))

OS_LCTL = KC.SK(KC.LCTL)
OS_LSFT = KC.SK(KC.LSFT)
OS_LALT = KC.SK(KC.LALT)
OS_LGUI = KC.SK(KC.LGUI)

ALT_TAB = KC.LALT(KC.TAB)

🪟 = KC.TRNS
⛔ = KC.NO

keyboard.keymap = [

    # -------------------------------------------------------------------------
    # LAYER 0: BASE
    # -------------------------------------------------------------------------
    [
        KC.Q,  KC.W,  KC.E,    KC.R,    KC.T,      KC.Y,   KC.U,    KC.I,    KC.O,   KC.P,
        KC.A,  KC.S,  KC.D,    KC.F,    KC.G,      KC.H,   KC.J,    KC.K,    KC.L,   layout.NO_OE,
        KC.Z,  KC.X,  KC.C,    KC.V,    KC.B,      KC.N,   KC.M,    layout.US_QUOT, layout.NO_AA,  layout.NO_AE,
        ⛔,      ⛔,  LEAD,   KC.SPC, SYM_SK_MO,   KC.ENT, KC.BSPC, NUM_SK_MO,   ⛔,      ⛔,
    ],
    # -------------------------------------------------------------------------
    # LAYER 1: SYM
    # -------------------------------------------------------------------------
    [
        KC.PLUS, KC.EXLM, KC.SCLN, layout.US_QUOT, KC.ASTR,      KC.COMM, KC.LPRN, KC.RPRN, KC.LCBR, KC.RCBR,
        KC.MINS, KC.QUES, KC.COLN, layout.US_DQUO, KC.SLSH,      KC.DOT,  OS_LCTL, OS_LSFT, OS_LALT, OS_LGUI,
        KC.PERC, layout.US_TILD, KC.PIPE, layout.US_GRV,  KC.EQL,       KC.UNDS, KC.LABK, KC.RABK, KC.LBRC, KC.RBRC,
        ⛔,      ⛔,      layout.US_CIRC, KC.AT,  KC.BSLS,      KC.AMPR, KC.DEL,  KC.DLR,  ⛔,      ⛔,
    ],
    # -------------------------------------------------------------------------
    # LAYER 2: NUM
    # -------------------------------------------------------------------------
    [
        KC.PLUS, KC.N7,   KC.N8,   KC.N9,   KC.ASTR,      KC.COMM, KC.LPRN, KC.RPRN, KC.LCBR, KC.RCBR,
        KC.MINS, KC.N3,   KC.N2,   KC.N1,   KC.SLSH,      KC.DOT,  OS_LCTL, OS_LSFT, OS_LALT, OS_LGUI,
        KC.PERC, KC.N4,   KC.N5,   KC.N6,   KC.EQL,       KC.UNDS, KC.LABK, KC.RABK, KC.LBRC, KC.RBRC,
        ⛔,      ⛔,     KC.N0,   KC.SPC,  KC.CW,        KC.CAPS, KC.DEL,  KC.DLR,   ⛔,      ⛔,
    ],
]




if __name__ == '__main__':
    keyboard.go()





