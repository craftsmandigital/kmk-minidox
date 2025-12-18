print("--- STARTING KEYBOARD ---")

from hardware import DactylMinidox

# KMK Modules
from kmk.modules.layers import Layers
from kmk.modules.holdtap import HoldTap
from kmk.modules.combos import Combos
from kmk.modules.macros import Macros
from kmk.modules.sticky_keys import StickyKeys
from kmk.modules.sticky_mod import StickyMod

# 1. Initialize Hardware
keyboard = DactylMinidox()
keyboard.debug_enabled = False

# 2. Install Modules (Order is critical!)
# We MUST do this BEFORE importing keymap/features so KC.MACRO exists!
keyboard.modules.append(Layers())

# Combos must be before HoldTap/Macros
combos = Combos()
keyboard.modules.append(combos)

keyboard.modules.append(HoldTap())
keyboard.modules.append(Macros())     # <--- This injects KC.MACRO
keyboard.modules.append(StickyMod())
keyboard.modules.append(StickyKeys(release_after=3000))

# 3. Import Keymap & Features (NOW it is safe)
from keymap import LAYERS
from features import COMBO_LIST

# 4. Apply Configuration
combos.combos = COMBO_LIST
keyboard.keymap = LAYERS

# 5. Run
if __name__ == '__main__':
    keyboard.go()

