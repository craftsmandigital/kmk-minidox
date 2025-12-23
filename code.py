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

# 2. Initialize Modules
layers = Layers()
holdtap = HoldTap()
combos = Combos()
macros = Macros()
sticky_keys = StickyKeys(release_after=3000)
sticky_mod = StickyMod()

# 3. Register Standard Modules
keyboard.modules.append(layers)
keyboard.modules.append(combos)
keyboard.modules.append(macros)

# 4. Import Features
from keymap import LAYERS
from features import COMBO_LIST, sticky_leader

# 5. CRITICAL ORDER:
# StickyLeader -> StickyKeys -> StickyMod -> HoldTap
keyboard.modules.append(sticky_leader) # Leader generates SK events
keyboard.modules.append(sticky_keys)   # StickyKeys handles SK events
keyboard.modules.append(sticky_mod)
keyboard.modules.append(holdtap)       # HoldTap handles the physical keys

# 6. Apply Configuration
combos.combos = COMBO_LIST
keyboard.keymap = LAYERS

if __name__ == '__main__':
    keyboard.go()
