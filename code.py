print("--- STARTING KEYBOARD ---")

# import board
import digitalio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.split import Split, SplitType, SplitSide
from kmk.modules.layers import Layers

# from kmk.modules.macros import Macros, Press, Release, Tap
from kmk.modules.macros import Macros


import hardware  # Pins (Local Library)


# --- INITIAL SETUP ---
keyboard = KMKKeyboard()
keyboard.modules.append(Layers())

# Enable Macros
# macros = Macros()
keyboard.modules.append(Macros())

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
keyboard.keymap = [
    [
        # Left Hand (Cols 1-5)                     # Right Hand (Cols 1-5)
        KC.Q,  KC.W,  KC.E,    KC.R,    KC.T,      KC.Y,   KC.U,    KC.I,    KC.O,   KC.P,    # Row 1
        KC.A,  KC.S,  KC.D,    KC.F,    KC.G,      KC.H,   KC.J,    KC.K,    KC.L,   layout.NO_OE,   # Row 2
        KC.Z,  KC.X,  KC.C,    KC.V,    KC.B,      KC.N,   KC.M,    layout.US_QUOT,  layout.NO_AA,  layout.NO_AE,   # Row 3 
        
        # Left Hands Thumbs (Cols 3-5)             # Right Hands Thumbs (Cols 3-5)
        KC.NO, KC.NO, KC.LCTL, KC.LSFT, KC.SPC,    KC.ENT, KC.BSPC, KC.LALT, KC.NO,  KC.NO,   # Row 4
    ]
]

if __name__ == '__main__':
    keyboard.go()


