print("--- STARTING KEYBOARD ---")

from hardware import DactylMinidox

# KMK Modules
from kmk.modules.layers import Layers
from kmk.modules.holdtap import HoldTap
from kmk.modules.combos import Combos
from kmk.modules.macros import Macros
from kmk.modules.sticky_keys import StickyKeys
from kmk.modules.sticky_mod import StickyMod
from kmk.modules.capsword import CapsWord

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
caps_word = CapsWord()

# 3. Register Standard Modules
#    Order: Layers -> Combos -> Macros -> StickyKeys
keyboard.modules.append(layers)

keyboard.modules.append(combos)
keyboard.modules.append(macros)
keyboard.modules.append(sticky_keys)
keyboard.modules.append(sticky_mod)

# 4. Import Features
#    (Must be done after Macros/StickyKeys are registered)
from keymap import LAYERS
from features import COMBO_LIST, sticky_leader

# 5. Register Custom & Input Modules (CRITICAL ORDER)
#    StickyLeader must run BEFORE HoldTap to capture keys correctly.
keyboard.modules.append(sticky_leader)
keyboard.modules.append(holdtap) 
keyboard.modules.append(caps_word)


# 6. Apply Configuration
combos.combos = COMBO_LIST
keyboard.keymap = LAYERS

if __name__ == '__main__':
    keyboard.go()
