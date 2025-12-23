import supervisor  # <--- REQUIRED for time tracking
from kmk.keys import KC
from kmk.modules import Module
from kmk.modules.macros import Macros, Tap
from kmk.modules.combos import Chord, Sequence



# -------------------------------------------------------------------------
# 1. CUSTOM MODULE: Sticky Leader (Sided / Bilateral)
# -------------------------------------------------------------------------
class StickyLeader(Module):
    def __init__(self, trigger_key, left_map, right_map, timeout=2000):
        self.trigger = trigger_key
        self.left_map = left_map
        self.right_map = right_map
        self.active = False
        # pending_mods stores tuples: (KC.MOD, 'L' or 'R')
        self.pending_mods = [] 
        self.last_time = 0
        self.timeout = timeout

    # --- Boilerplate ---
    def during_bootup(self, keyboard): return
    def before_matrix_scan(self, keyboard): return
    def after_matrix_scan(self, keyboard): return
    def before_hid_send(self, keyboard): return
    def after_hid_send(self, keyboard): return
    # -------------------

    def get_real_key(self, key):
        if hasattr(key, 'tap'): return key.tap
        return key

    def keys_match(self, k1, k2):
        rk1 = self.get_real_key(k1)
        rk2 = self.get_real_key(k2)
        if hasattr(rk1, 'code') and hasattr(rk2, 'code'):
            if rk1.code == rk2.code: return True
        if str(rk1) == str(rk2): return True
        if rk1 == rk2: return True
        return False

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if not is_pressed: return key
        
        try:
            import supervisor
            current_time = supervisor.ticks_ms()
        except ImportError:
            current_time = keyboard.time.monotonic_ms()

        # 1. Handle Timeout
        if self.active and (current_time - self.last_time > self.timeout):
            print("Leader: Timeout")
            self.pending_mods = []

            self.active = False

        # 2. CHECK TRIGGER
        if self.keys_match(key, self.trigger):
            self.active = True
            self.pending_mods = []
            self.last_time = current_time
            print(">>> LEADER ACTIVE! <<<") 
            return None 

        # 3. While Active
        if self.active:
            self.last_time = current_time
            
            # IDENTIFY KEY SIDE & MODIFIER
            mod = None
            side = None
            
            # Check Left Map
            for map_key, map_mod in self.left_map.items():
                if self.keys_match(key, map_key):
                    mod = map_mod
                    side = 'L'
                    break
            
            # Check Right Map (if not found in Left)
            if not mod:
                for map_key, map_mod in self.right_map.items():
                    if self.keys_match(key, map_key):
                        mod = map_mod
                        side = 'R'
                        break

            # LOGIC: Handle the Key
            if mod:

                # 1. Check for Collision (Same Mod exists) -> Type Key
                # 2. Check for Cross-Over (Left Mod exists, Key is Right) -> Type Key
                
                has_left = any(s == 'L' for m, s in self.pending_mods)
                has_right = any(s == 'R' for m, s in self.pending_mods)
                
                is_collision = any(m == mod for m, s in self.pending_mods)
                is_crossover = (side == 'R' and has_left) or (side == 'L' and has_right)


                if is_collision or is_crossover:
                    print(f"Leader: Type Key (Collision={is_collision}, Cross={is_crossover})")
                    self.send_atomic(keyboard, key)
                    self.active = False
                    return None 
                else:
                    self.pending_mods.append((mod, side))
                    print(f"Leader: Queued {mod} ({side})")
                    return None 
            else:
                # Not a home row mod key -> Type it
                print(f"Leader: Sequence End -> {key}")
                self.send_atomic(keyboard, key)
                self.active = False
                return None


        return key

    def send_atomic(self, keyboard, key):
        final_key = key
        # Unwrap the tuples to get just the modifiers
        mods_only = [m for m, s in self.pending_mods]
        
        for mod in reversed(mods_only):
            final_key = mod(final_key)
            
        keyboard.tap_key(final_key)
        self.pending_mods = []


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
    """Fixes dead keys by tapping the key followed by Space."""
    return KC.MACRO(Tap(code), Tap(KC.SPC))

def pair_macro(open_k, close_k):
    """Types a pair of brackets and moves cursor left."""
    return KC.MACRO(Tap(open_k), Tap(close_k), Tap(KC.LEFT))

# -------------------------------------------------------------------------
# 4. CUSTOM KEYS & ALIASES
# -------------------------------------------------------------------------
# Leader Key
LEAD = KC.F24

# Nordic Characters (US-Int AltGr codes)
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

# Left Hand Map
MAP_L = {
    KC.F: KC.LSFT,
    KC.D: KC.LCTL,
    KC.S: KC.LALT,
    KC.A: KC.LGUI,
}

# Right Hand Map
MAP_R = {
    KC.J: KC.LSFT,
    KC.K: KC.LCTL,
    KC.L: KC.LALT,
    NO_OE: KC.LGUI, 
}

# Initialize with BOTH maps
sticky_leader = StickyLeader(trigger_key=LEAD, left_map=MAP_L, right_map=MAP_R)

# -------------------------------------------------------------------------
# 6. MACROS
# -------------------------------------------------------------------------
MACRO_PAR = pair_macro(KC.LPRN, KC.RPRN) # ()
MACRO_CRL = pair_macro(KC.LCBR, KC.RCBR) # {}
MACRO_SQR = pair_macro(KC.LBRC, KC.RBRC) # []
MACRO_ANG = pair_macro(KC.LABK, KC.RABK) # <>
MACRO_QUO = pair_macro(KC.QUOT, KC.QUOT) # ''
MACRO_DBL = pair_macro(KC.DQUO, KC.DQUO) # ""
MACRO_GRV = pair_macro(KC.GRV,  KC.GRV)  # ``

ACTIVATE_FUN = KC.MACRO(Tap(FUN_SK))

# -------------------------------------------------------------------------
# 7. COMBOS
# -------------------------------------------------------------------------
COMBO_LIST = [
    # Layer Triggers
    Chord((KC.BSPC, NUM_SK), ACTIVATE_FUN), 

    # Brackets & Quotes
    Chord((KC.MINS, KC.QUES), MACRO_PAR),
    Chord((KC.LCBR, KC.RCBR), MACRO_CRL),

    Chord((KC.LPRN, KC.RPRN), MACRO_PAR),
    Chord((KC.LABK, KC.RABK), MACRO_ANG),
    Chord((KC.LBRC, KC.RBRC), MACRO_SQR),
    Chord((US_QUOT, KC.SCLN), MACRO_QUO), 
    Chord((US_DQUO, KC.COLN), MACRO_DBL),
    Chord((US_GRV,  US_TILD), MACRO_GRV),
]
