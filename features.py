import supervisor
from kmk.keys import KC
from kmk.modules import Module
from kmk.modules.macros import Macros, Tap
from kmk.modules.combos import Chord, Sequence

from abbreviations import abbrevs

# -------------------------------------------------------------------------
# 1. CUSTOM MODULE: Sticky Leader (Production Optimized)
# -------------------------------------------------------------------------
class StickyLeader(Module):
    def __init__(self, trigger_key, left_map, right_map, timeout=2000):
        self.trigger = trigger_key
        self.left_map = left_map
        self.right_map = right_map
        self.active = False
        self.pending_mods = [] 
        self.last_time = 0
        self.timeout = timeout

    # --- Boilerplate ---
    def during_bootup(self, keyboard): return
    def before_matrix_scan(self, keyboard): return
    def after_matrix_scan(self, keyboard): return
    def before_hid_send(self, keyboard): return
    def after_hid_send(self, keyboard): return

    # --- Helpers ---
    def get_real_key(self, key):
        return getattr(key, 'tap', key)

    def keys_match(self, k1, k2):
        rk1 = self.get_real_key(k1)
        rk2 = self.get_real_key(k2)
        
        # 1. Scan Code Equality (Best for Split)

        c1 = getattr(rk1, 'code', None)
        c2 = getattr(rk2, 'code', None)
        if c1 is not None and c2 is not None:
            if c1 == c2: return True
            
        # 2. Direct Equality & String Fallback
        if rk1 == rk2: return True
        return str(rk1) == str(rk2)


    def send_atomic(self, keyboard, key):
        """Wraps target key in pending mods and taps as one object."""
        final_key = key
        for mod, _ in self.pending_mods:
            final_key = mod(final_key)
        keyboard.tap_key(final_key)
        self.pending_mods = []

    # --- Core Logic ---
    def process_key(self, keyboard, key, is_pressed, int_coord):
        if not is_pressed: return key
        
        current_time = supervisor.ticks_ms()

        # 1. Handle Timeout
        if self.active and (current_time - self.last_time > self.timeout):
            self.pending_mods = []
            self.active = False

        # 2. Check Trigger
        if self.keys_match(key, self.trigger):
            self.active = True
            self.pending_mods = []
            self.last_time = current_time
            return None 

        # 3. While Active
        if self.active:
            self.last_time = current_time
            
            mod = None
            side = None
            
            # Check Left Map
            for map_key, map_mod in self.left_map.items():
                if self.keys_match(key, map_key):
                    mod = map_mod

                    side = 'L'
                    break
            
            # Check Right Map
            if not mod:
                for map_key, map_mod in self.right_map.items():
                    if self.keys_match(key, map_key):
                        mod = map_mod
                        side = 'R'
                        break

            if mod:
                # Logic: Collision OR Cross-Over -> Type the Key
                has_left = any(s == 'L' for _, s in self.pending_mods)
                has_right = any(s == 'R' for _, s in self.pending_mods)
                
                is_collision = any(m == mod for m, _ in self.pending_mods)
                is_crossover = (side == 'R' and has_left) or (side == 'L' and has_right)

                if is_collision or is_crossover:
                    self.send_atomic(keyboard, key)
                    self.active = False
                    return None 
                else:
                    self.pending_mods.append((mod, side))
                    return None 
            else:
                # Not a modifier key -> Type the sequence
                self.send_atomic(keyboard, key)
                self.active = False

                return None

        return key

# -------------------------------------------------------------------------
# 2. LAYER INDICES
# -------------------------------------------------------------------------
LAYER_BASE = 0
LAYER_SYM  = 1
LAYER_NUM  = 2
LAYER_FUN  = 3
LAYER_NAV  = 4


# -------------------------------------------------------------------------
# 3. HELPER FUNCTIONS
# -------------------------------------------------------------------------
def dead_fix(code):
    return KC.MACRO(Tap(code), Tap(KC.SPC))

def pair_macro(open_k, close_k):
    return KC.MACRO(Tap(open_k), Tap(close_k), Tap(KC.LEFT))

# Helper to convert string "abc" -> (KC.A, KC.B, KC.C)
def get_seq_from_string(trigger):
    seq = []
    for char in trigger:
        if char.isalpha():
            seq.append(getattr(KC, char.upper()))
        elif char.isdigit():
            seq.append(getattr(KC, f"N{char}"))
        elif char == ' ':
            seq.append(KC.SPC)
    return tuple(seq)

# -------------------------------------------------------------------------
# 4. CUSTOM KEYS & ALIASES
# -------------------------------------------------------------------------
# Leader Key for StickyLeader stuff
LEAD_SK = KC.F24

# NEW: Safe Leader for Sticky Layers
# F23 Is a "real" keycode (so Sticky Keys sees it and drops the layer). KC.LEADER is a fake key
LEAD_AB = KC.F23


# Nordic Characters
NO_AE = KC.RALT(KC.Z)
NO_OE = KC.RALT(KC.L)
NO_AA = KC.RALT(KC.W)

# Dead Key Fixes
US_QUOT = dead_fix(KC.QUOTE)
US_DQUO = dead_fix(KC.LSFT(KC.QUOTE))

US_GRV  = dead_fix(KC.GRAVE)
US_TILD = dead_fix(KC.LSFT(KC.GRAVE))

US_CIRC = dead_fix(KC.LSFT(KC.N6))

# Sticky / One-Shot Logic
SYM_SK  = KC.SK(KC.MO(LAYER_SYM))
NUM_SK  = KC.SK(KC.MO(LAYER_NUM))
FUN_SK  = KC.SK(KC.MO(LAYER_FUN))
NAV_HT  = KC.HT(KC.TG(LAYER_NAV), KC.MO(LAYER_NAV)) 

# Sticky Modifiers
OS_LCTL = KC.SK(KC.LCTL)
OS_LSFT = KC.SK(KC.LSFT)
OS_LALT = KC.SK(KC.LALT)
OS_LGUI = KC.SK(KC.LGUI)

# Nav Shortcuts
SelAll  = KC.LCTL(KC.A)
Paste   = KC.LCTL(KC.V)
Copy    = KC.LCTL(KC.C)
Cut     = KC.LCTL(KC.X)
Undo    = KC.LCTL(KC.Z)
Redo    = KC.LCTL(KC.Y)
ALT_TAB = KC.SM(KC.TAB, KC.LALT)
WordR   = KC.LCTL(KC.RIGHT)
WordL   = KC.LCTL(KC.LEFT)

# Visual Aliases
TRNS = KC.TRNS
XXXX = KC.NO

# -------------------------------------------------------------------------
# 5. CONFIGURE STICKY LEADER
# -------------------------------------------------------------------------
MAP_L = {
    KC.F: KC.LSFT,
    KC.D: KC.LCTL,
    KC.S: KC.LALT,
    KC.A: KC.LGUI,
}

MAP_R = {
    KC.J: KC.LSFT,
    KC.K: KC.LCTL,
    KC.L: KC.LALT,
    NO_OE: KC.LGUI, 
}

sticky_leader = StickyLeader(trigger_key=LEAD_SK, left_map=MAP_L, right_map=MAP_R)

# -------------------------------------------------------------------------
# 6. MACROS
# -------------------------------------------------------------------------
MACRO_PAR = pair_macro(KC.LPRN, KC.RPRN)
MACRO_CRL = pair_macro(KC.LCBR, KC.RCBR)
MACRO_SQR = pair_macro(KC.LBRC, KC.RBRC)
MACRO_ANG = pair_macro(KC.LABK, KC.RABK)
MACRO_QUO = pair_macro(KC.QUOT, KC.QUOT)
MACRO_DBL = pair_macro(KC.DQUO, KC.DQUO)
MACRO_GRV = pair_macro(KC.GRV,  KC.GRV)

ACTIVATE_FUN = KC.MACRO(Tap(FUN_SK))

# -------------------------------------------------------------------------
# 7. COMBOS
# -------------------------------------------------------------------------
COMBO_LIST = [
    Chord((KC.MINS, KC.QUES), MACRO_PAR),
    Chord((KC.LCBR, KC.RCBR), MACRO_CRL),
    Chord((KC.LPRN, KC.RPRN), MACRO_PAR),
    Chord((KC.LABK, KC.RABK), MACRO_ANG),
    Chord((KC.LBRC, KC.RBRC), MACRO_SQR),
    Chord((US_QUOT, KC.SCLN), MACRO_QUO), 
    Chord((US_DQUO, KC.COLN), MACRO_DBL),
    Chord((US_GRV,  US_TILD), MACRO_GRV),
]

# Dynamically add Abbreviations to COMBO_LIST
for trigger, content in abbrevs.items():
    # 1. Convert trigger text to KeyCodes (e.g. "al" -> KC.A, KC.L)
    trigger_seq = get_seq_from_string(trigger)
    
    # 2. Prepend the Leader Key (F23)
    full_sequence = (LEAD_AB,) + trigger_seq
    
    # 3. Create Sequence
    # Check if content is a List/Tuple (Complex) or String (Simple)
    if isinstance(content, (list, tuple)):
        # Unpack the list into the Macro: KC.MACRO("H", OE, "r")
        COMBO_LIST.append(
            Sequence(full_sequence, KC.MACRO(*content), timeout=2000)
        )
    else:
        # Standard string: KC.MACRO("Jon Arne")
        COMBO_LIST.append(
            Sequence(full_sequence, KC.MACRO(content), timeout=2000)
        )
