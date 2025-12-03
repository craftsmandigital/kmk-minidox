import board

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



# --- KMK GROUPS ---
# We group the individual variables above into tuples.
# This allows KMK and boot.py to iterate over them easily.

COL_PINS = (
    PINKY_COL_PIN, 
    RING_FINGER_COL_PIN, 
    MIDDLE_FINGER_COL_PIN, 
    INDEX_FINGER_COL_PIN, 
    INDEX_INNER_COL_PIN
)

ROW_PINS = (
    TOP_ROW_PIN, 
    HOME_ROW_PIN, 
    BOTTOM_ROW_PIN, 
    THUMB_ROW_PIN
)
