import board
import digitalio
from kmk.kmk_keyboard import KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.modules.split import Split, SplitType, SplitSide

class DactylMinidox(KMKKeyboard):
    def __init__(self):
        super().__init__()

        # ---------------------------------------------------------------------
        # 1. MATRIX CONFIGURATION
        # ---------------------------------------------------------------------
        # Columns: GP2 -> GP3 -> GP4 -> GP5 -> GP28
        self.col_pins = (board.GP2, board.GP3, board.GP4, board.GP5, board.GP28)
        # Rows: GP6 -> GP7 -> GP8 -> GP9
        self.row_pins = (board.GP6, board.GP7, board.GP8, board.GP9)
        self.diode_orientation = DiodeOrientation.COL2ROW


        # --- RGB CONFIGURATION (NEW) ---
        # CHANGE THIS PIN to match your soldering!
        self.rgb_pixel_pin = board.GP16 
        # Total LEDs (Left + Right if chained, or just one side count if mirrored)
        self.num_pixels = 6         

        # ---------------------------------------------------------------------
        # 2. SPLIT CONFIGURATION
        # ---------------------------------------------------------------------
        self.split = Split(
            split_type=SplitType.UART,
            data_pin=board.GP1,
            use_pio=True,
            uart_flip=True
        )

        # ---------------------------------------------------------------------
        # 3. SIDE DETECTION
        # ---------------------------------------------------------------------
        # Jumper on GP21 to GND = Right Side
        jumper = digitalio.DigitalInOut(board.GP21)
        jumper.direction = digitalio.Direction.INPUT
        jumper.pull = digitalio.Pull.UP

        self.split.split_side = SplitSide.RIGHT if not jumper.value else SplitSide.LEFT
        self.modules.append(self.split)

