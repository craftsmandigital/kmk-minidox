print("--- STARTING KEYBOARD ---")

import board
import digitalio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.split import Split, SplitType, SplitSide
from kmk.modules.layers import Layers

# from kmk.modules.macros import Macros, Press, Release, Tap
from kmk.modules.macros import Macros, Tap



# --- 0. PIN DEFINITIONS ---
# All GPIO pins are defined here as constants for readability and easy maintenance.
# If you change the wiring, you only need to update the values in this section.

# General Pins
SIDE_DETECTION_PIN = board.GP21  # Jumper to GND on the right side to identify it.
SPLIT_UART_PIN = board.GP1       # Pin used for UART communication between halves.

# Column Pins (based on finger hints, from outside to inside)
PINKY_COL_PIN         = board.GP2   # Col 1
RING_FINGER_COL_PIN   = board.GP3   # Col 2
MIDDLE_FINGER_COL_PIN = board.GP4   # Col 3
INDEX_FINGER_COL_PIN  = board.GP5   # Col 4
INDEX_INNER_COL_PIN   = board.GP28  # Col 5

# Row Pins (from top to bottom)
TOP_ROW_PIN    = board.GP6   # Row 1
HOME_ROW_PIN   = board.GP7   # Row 2
BOTTOM_ROW_PIN = board.GP8   # Row 3
THUMB_ROW_PIN  = board.GP9   # Row 4



# --- INITIAL SETUP ---
keyboard = KMKKeyboard()
keyboard.modules.append(Layers())

# Enable Macros
# macros = Macros()
keyboard.modules.append(Macros())




# Nordic Keyboard Layout for the us international keyboard Layout

# --- 1. THE HELPER FUNCTION ---
# This function takes any key (like KC.QUOTE) and returns a Macro 
# that taps that key followed immediately by Space.
def dead_fix(key_code):
    return KC.MACRO(Tap(key_code), Tap(KC.SPC))

# --- 2. GENERATE THE KEYS ---
# Now we just call the function for the keys we need.

# Fix all symbols that are dead keys in the us international layout
US_QUOT = dead_fix(KC.QUOTE)             # '
US_DQUO = dead_fix(KC.LSFT(KC.QUOTE))    # "
US_GRV  = dead_fix(KC.GRAVE)             # `
US_TILD = dead_fix(KC.LSFT(KC.GRAVE))    # ~
US_CIRC = dead_fix(KC.LSFT(KC.N6))       # ^

# Define Nordic letters (Standard US-Int shortcuts)
NO_AE = KC.RALT(KC.Z) # Æ
NO_OE = KC.RALT(KC.L) # Ø
NO_AA = KC.RALT(KC.W) # Å








# --- 1. JUMPER DETECTION ---
jumper = digitalio.DigitalInOut(SIDE_DETECTION_PIN)
jumper.direction = digitalio.Direction.INPUT
jumper.pull = digitalio.Pull.UP


is_right = False
if not jumper.value:
    is_right = True

# --- 2. SPLIT CONFIGURATION ---
split = Split(
    split_type=SplitType.UART,
    data_pin=SPLIT_UART_PIN,
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
col_pins = (
    PINKY_COL_PIN,
    RING_FINGER_COL_PIN,
    MIDDLE_FINGER_COL_PIN,
    INDEX_FINGER_COL_PIN,
    INDEX_INNER_COL_PIN,
)
row_pins = (
    TOP_ROW_PIN,
    HOME_ROW_PIN,
    BOTTOM_ROW_PIN,
    THUMB_ROW_PIN,
)

keyboard.col_pins = col_pins
keyboard.row_pins = row_pins

keyboard.diode_orientation = DiodeOrientation.COL2ROW

# --- 4. KEYMAP ---
keyboard.keymap = [
    [
        # Left Hand (Cols 1-5)                     # Right Hand (Cols 1-5)
        KC.Q,  KC.W,  KC.E,    KC.R,    KC.T,      KC.Y,   KC.U,    KC.I,    KC.O,   KC.P,    # Row 1
        KC.A,  KC.S,  KC.D,    KC.F,    KC.G,      KC.H,   KC.J,    KC.K,    KC.L,   NO_OE,   # Row 2
        KC.Z,  KC.X,  KC.C,    KC.V,    KC.B,      KC.N,   KC.M,    US_DQUO, NO_AA,  NO_AE,   # Row 3 
        
        # Left Hands Thumbs (Cols 3-5)             # Right Hands Thumbs (Cols 3-5)
        KC.NO, KC.NO, KC.LCTL, KC.LSFT, KC.SPC,    KC.ENT, KC.BSPC, KC.LALT, KC.NO,  KC.NO,   # Row 4
    ]
]

if __name__ == '__main__':
    keyboard.go()

