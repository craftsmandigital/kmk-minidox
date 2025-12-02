print("--- STARTING KEYBOARD ---")

import board
import digitalio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.split import Split, SplitType, SplitSide
from kmk.modules.layers import Layers

keyboard = KMKKeyboard()
keyboard.modules.append(Layers())

# --- 1. JUMPER DETECTION ---
jumper = digitalio.DigitalInOut(board.GP21)
jumper.direction = digitalio.Direction.INPUT

jumper.pull = digitalio.Pull.UP

is_right = False
if jumper.value == False:
    is_right = True

# --- 2. SPLIT CONFIGURATION ---
split = Split(
    split_type=SplitType.UART,
    data_pin=board.GP1,
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
col_pins = (board.GP2, board.GP3, board.GP4, board.GP5, board.GP28)

keyboard.col_pins = col_pins
keyboard.row_pins = (board.GP6, board.GP7, board.GP8, board.GP9)
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# --- 4. KEYMAP ---
keyboard.keymap = [
    [
        # Left Hand (Cols 0-4)                     # Right Hand (Cols 0-4)
        KC.Q,  KC.W,  KC.E,    KC.R,    KC.T,      KC.Y,   KC.U,    KC.I,    KC.O,   KC.P,    # Row 0
        KC.A,  KC.S,  KC.D,    KC.F,    KC.G,      KC.H,   KC.J,    KC.K,    KC.L,   KC.SCLN, # Row 1
        KC.Z,  KC.X,  KC.C,    KC.V,    KC.B,      KC.N,   KC.M,    KC.COMM, KC.DOT, KC.SLSH, # Row 2
        
        # Thumbs (Row 3)
        KC.NO, KC.NO, KC.LCTL, KC.LSFT, KC.SPC,    KC.ENT, KC.BSPC, KC.LALT, KC.NO,  KC.NO,
    ]
]

if __name__ == '__main__':
    keyboard.go()

