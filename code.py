print("--- STARTING KEYBOARD ---")

import board
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

# 2. Initialize Modules (This injects keys like KC.MO and KC.SK into KC)
layers = Layers()

holdtap = HoldTap()
combos_mod = Combos()
macros = Macros()
sticky_keys = StickyKeys(release_after=3000)
sticky_mod = StickyMod()
caps_word = CapsWord()

# 3. Register Modules
#    Order matters: Layers -> Combos -> Macros -> StickyKeys
keyboard.modules.append(layers)
keyboard.modules.append(combos_mod)
keyboard.modules.append(macros)
keyboard.modules.append(sticky_keys)
keyboard.modules.append(sticky_mod)

# -------------------------------------------------------------------------
# 4. Import Custom Features (NOW it is safe to import these)
# -------------------------------------------------------------------------
# These files use KC.MO, KC.SK, etc., so they must be imported 
# AFTER the modules above are initialized.
import behaviors
import combos
import sequences
import keymap
from extensions import apply_leader_sequences

# 5. Register Custom Modules
#    StickyLeader must run BEFORE HoldTap
keyboard.modules.append(behaviors.sticky_leader_mod)
keyboard.modules.append(holdtap) 
keyboard.modules.append(caps_word)

# 6. Apply Configuration
combos_mod.combos = combos.COMBO_LIST
keyboard.keymap = keymap.LAYERS

# 7. Generate Leader Sequences
apply_leader_sequences(keyboard, sequences.LEADER_SEQUENCES, combos_mod)

if __name__ == '__main__':
    keyboard.go()
