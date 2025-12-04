print("--- STARTING KEYBOARD ---")

# import board
import digitalio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.split import Split, SplitType, SplitSide
from kmk.modules.layers import Layers
from kmk.modules.sticky_keys import StickyKeys

# from kmk.modules.macros import Macros, Press, Release, Tap
from kmk.modules.macros import Macros


# 1. Import our new, custom OSL module
#from osl import OSL
import hardware  # Pins (Local Library)


# --- INITIAL SETUP ---
keyboard = KMKKeyboard()
keyboard.modules.append(Layers())
keyboard.modules.append(StickyKeys())
# Enable Macros
# macros = Macros()
keyboard.modules.append(Macros())
#keyboard.modules.append(OSL())  # This enables our custom KC.OSL

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

import layout    # Custom Keys (Nordic + Dead Fixes)  (Local Library)

# --- 4. KEYMAP ---

# --- 4. KEYMAP ---
_BASE = 0
_SYM  = 1

keyboard.keymap = [
    # -------------------------------------------------------------------------
    # LAYER 0: BASE
    # -------------------------------------------------------------------------
    [
        # Left Hand (Cols 1-5)                     # Right Hand (Cols 1-5)
        KC.Q,  KC.W,  KC.E,    KC.R,    KC.T,      KC.Y,   KC.U,    KC.I,    KC.O,   KC.P,    # Row 1
        KC.A,  KC.S,  KC.D,    KC.F,    KC.G,      KC.H,   KC.J,    KC.K,    KC.L,   layout.NO_OE,   # Row 2
        KC.Z,  KC.X,  KC.C,    KC.V,    KC.B,      KC.N,   KC.M,    layout.US_QUOT,  layout.NO_AA,  layout.NO_AE,   # Row 3 
        
        # Left Hands Thumbs (Cols 3-5)             # Right Hands Thumbs (Cols 3-5)
        # Note: Left Inner (SPC) is now LT(_SYM, KC.SPC)
        KC.NO, KC.NO, KC.LCTL, KC.SPC, KC.SK(KC.MO(_SYM)),    KC.ENT, KC.BSPC, KC.LALT, KC.NO,  KC.NO,   # Row 4
    ],

    # -------------------------------------------------------------------------
    # LAYER 1: SYM (Miryoku Style)
    # -------------------------------------------------------------------------
    [
        # Left Hand (Cols 1-5)                     # Right Hand (Cols 1-5)

        # +        !        ;        '        *        ,        .        CW       Caps     NO
        KC.PLUS, KC.EXLM, KC.SCLN, layout.US_QUOT, KC.ASTR,   KC.COMM, KC.DOT,  KC.CW,   KC.CAPS, KC.NO,   # Row 1

        
        # -        ?        :        "        /        {        (        [        $        _
        KC.MINS, KC.QUES, KC.COLN, layout.US_DQUO, KC.SLSH,   KC.LCBR, KC.LPRN, KC.LBRC, KC.DLR,  KC.UNDS, # Row 2
        
        # %        ~        ^        `        =        }        )        ]        &        #
        KC.PERC, layout.US_TILD, layout.US_CIRC, layout.US_GRV, KC.EQL,    KC.RCBR, KC.RPRN, KC.RBRC, KC.AMPR, KC.HASH, # Row 3 
        
        # Left Hands Thumbs (Cols 3-5)             # Right Hands Thumbs (Cols 3-5)

        # |        \        TRNS (Hold)            >        @        NO
        KC.NO, KC.NO, KC.PIPE, KC.BSLS, KC.TRNS,             KC.RABT, KC.AT,   KC.NO,   KC.NO,  KC.NO,   # Row 4
    ]
]




if __name__ == '__main__':
    keyboard.go()




