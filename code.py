import board
import digitalio

from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from kmk.scanners import DiodeOrientation
from kmk.modules.split import Split, SplitType, SplitSide
from kmk.modules.layers import Layers

# --- Keyboard Setup ---
keyboard = KMKKeyboard()
keyboard.modules.append(Layers())

# --- Split Configuration (Single Wire PIO) ---
split = Split(
    split_type=SplitType.UART,
    data_pin=board.GP1,   # Connect GP1 to GP1 on both sides
    use_pio=True,         # Uses single-wire communication (Safe for TRRS)
    uart_flip=True        # Standardizes connection logic
)

# --- SIDE DETECTION (The Jumper Logic) ---

# We check Pin GP21.
# If it is connected to GND (False), we are the RIGHT side.
# If it is empty/floating (True), we are the LEFT side.
side_det_pin = digitalio.DigitalInOut(board.GP21)
side_det_pin.direction = digitalio.Direction.INPUT
side_det_pin.pull = digitalio.Pull.UP

if side_det_pin.value == False:
    split.split_side = SplitSide.RIGHT
else:
    split.split_side = SplitSide.LEFT

keyboard.modules.append(split)

# --- Pins & Matrix ---
# Wiring: Pinky=GP2, Ring=GP3, Mid=GP4, Index=GP5, Inner=GP28
col_pins = (board.GP2, board.GP3, board.GP4, board.GP5, board.GP28)
row_pins = (board.GP6, board.GP7, board.GP8, board.GP9)

# --- THE FLIP LOGIC ---
# Since we wired both sides symmetrically (Pin 2 is always Pinky),
# The Right side is technically reading "backwards" compared to the keymap.
# We flip the column order in software ONLY if we are the Right side.
if split.split_side == SplitSide.RIGHT:
    col_pins = tuple(reversed(col_pins))

keyboard.col_pins = col_pins
keyboard.row_pins = row_pins
keyboard.diode_orientation = DiodeOrientation.COL2ROW

# --- Keymap ---
# 36 Keys Total (18 per side)
# The matrix is 4 rows x 5 cols.

# Row 3 (Thumbs) uses the first 3 columns (Cols 0, 1, 2).

# --- Keymap ---
# Layout:
# Left Hand:  Pinky, Ring, Middle, Index, Inner
# Right Hand: Inner, Index, Middle, Ring, Pinky

keyboard.keymap = [
    [
        # Left Hand (Cols 0-4)                     # Right Hand (Cols 0-4)
        KC.Q,  KC.W,  KC.E,    KC.R,    KC.T,      KC.Y,   KC.U,    KC.I,    KC.O,   KC.P,    # Row 0
        KC.A,  KC.S,  KC.D,    KC.F,    KC.G,      KC.H,   KC.J,    KC.K,    KC.L,   KC.SCLN, # Row 1
        KC.Z,  KC.X,  KC.C,    KC.V,    KC.B,      KC.N,   KC.M,    KC.COMM, KC.DOT, KC.SLSH, # Row 2
        
        # Thumbs (Row 3)
        # Note: Pinky & Ring cols are empty (NO) on Dactyl Minidox thumbs
        KC.NO, KC.NO, KC.LCTL, KC.LSFT, KC.SPC,    KC.ENT, KC.BSPC, KC.LALT, KC.NO,  KC.NO,
    ]
]

if __name__ == '__main__':
    keyboard.go()

