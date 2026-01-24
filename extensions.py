import supervisor
from kmk.keys import KC
from kmk.modules import Module
from kmk.modules.combos import Sequence
# from kmk.extensions.rgb import RGB
import neopixel





# -------------------------------------------------------------------------
# Custom Module: MagicKey
# -------------------------------------------------------------------------

# Helper Class for Sequences (Keep this if you use Seq)
class Seq:

    def __init__(self, *keys):
        self.keys = keys
    def __hash__(self):
        return hash(self.keys)
    def __eq__(self, other):
        return isinstance(other, Seq) and self.keys == other.keys

class MagicKey(Module):

    def __init__(self, magic_key, triggers, default_behavior, max_history=10):
        self.magic_key = magic_key
        self.triggers = triggers
        self.current_behavior = default_behavior
        self.buffer = [] 
        self.max_history = max_history

    def during_bootup(self, keyboard): return
    def before_matrix_scan(self, keyboard): return
    def after_matrix_scan(self, keyboard): return
    def before_hid_send(self, keyboard): return
    def after_hid_send(self, keyboard): return

    def keys_match(self, k1, k2):
        if k1 == k2: return True
        c1 = getattr(k1, 'code', None)
        c2 = getattr(k2, 'code', None)
        if c1 is not None and c2 is not None and c1 == c2: return True
        return str(k1) == str(k2)

    def buffer_matches_sequence(self, seq_keys):
        if len(self.buffer) < len(seq_keys): return False
        snippet = self.buffer[-len(seq_keys):]
        for i, k in enumerate(seq_keys):
            if not self.keys_match(snippet[i], k): return False
        return True

    def find_trigger_result(self, key_to_check):
        # Helper to find if a key matches any trigger
        for trigger, result in self.triggers.items():
            if isinstance(trigger, Seq):

                # Sequences are handled in the buffer logic, not here
                continue 
            elif isinstance(trigger, (tuple, list)):
                if any(self.keys_match(key_to_check, t) for t in trigger):
                    return result
            elif self.keys_match(key_to_check, trigger):
                return result
        return None

    def process_key(self, keyboard, key, is_pressed, int_coord):
        # 1. Handle the Magic Key itself
        if self.keys_match(key, self.magic_key):
            if is_pressed:
                # Get the behavior we are about to send
                to_send = self.current_behavior
                
                # --- NEW: SELF-ADVANCING LOGIC ---
                # Check if the output we are sending is ITSELF a trigger for the next state
                next_state = self.find_trigger_result(to_send)
                if next_state:
                    self.current_behavior = next_state
                
                return to_send
            return None # Handle release if needed, or just None

        # 2. Listen for External Triggers (Only on Press)
        if is_pressed:
            self.buffer.append(key)
            if len(self.buffer) > self.max_history:
                self.buffer.pop(0)


            # Check Sequences first
            match_found = False
            for trigger, result in self.triggers.items():
                if isinstance(trigger, Seq):
                    if self.buffer_matches_sequence(trigger.keys):
                        self.current_behavior = result
                        match_found = True
                        break
            
            # If no sequence matched, check standard keys
            if not match_found:
                res = self.find_trigger_result(key)
                if res:
                    self.current_behavior = res

        return key






#
# class MagicKey(Module):
#     def __init__(self, magic_key, triggers, default_behavior):
#         self.magic_key = magic_key
#
#         self.triggers = triggers
#         self.current_behavior = default_behavior
#
#     def during_bootup(self, keyboard): return
#     def before_matrix_scan(self, keyboard): return
#     def after_matrix_scan(self, keyboard): return
#     def before_hid_send(self, keyboard): return
#     def after_hid_send(self, keyboard): return
#
#     def keys_match(self, k1, k2):
#         if k1 == k2: return True
#         c1 = getattr(k1, 'code', None)
#         c2 = getattr(k2, 'code', None)
#         if c1 is not None and c2 is not None and c1 == c2: return True
#         return str(k1) == str(k2)
#
#     def process_key(self, keyboard, key, is_pressed, int_coord):
#
#         # 1. Handle the Magic Key itself
#         if self.keys_match(key, self.magic_key):
#             return self.current_behavior
#
#         # 2. Listen for Triggers (Only on Press)
#         if is_pressed:
#             for trigger, result in self.triggers.items():
#                 # --- NEW: Support for multiple keys (Tuples) ---
#                 if isinstance(trigger, (tuple, list)):
#                     # Check if the pressed key matches ANY key in the tuple
#                     if any(self.keys_match(key, t) for t in trigger):
#                         self.current_behavior = result
#                         break
#                 # --- OLD: Support for single keys ---
#                 elif self.keys_match(key, trigger):
#                     self.current_behavior = result
#                     break
#
#         return key



















# -------------------------------------------------------------------------
# Custom Module: Sticky Leader
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

    def during_bootup(self, keyboard): return
    def before_matrix_scan(self, keyboard): return
    def after_matrix_scan(self, keyboard): return
    def before_hid_send(self, keyboard): return
    def after_hid_send(self, keyboard): return

    def get_real_key(self, key):
        return getattr(key, 'tap', key)

    def keys_match(self, k1, k2):
        rk1 = self.get_real_key(k1)
        rk2 = self.get_real_key(k2)
        c1 = getattr(rk1, 'code', None)
        c2 = getattr(rk2, 'code', None)
        if c1 is not None and c2 is not None:
            if c1 == c2: return True
        if rk1 == rk2: return True
        return str(rk1) == str(rk2)

    def send_atomic(self, keyboard, key):
        final_key = key
        for mod, _ in self.pending_mods:
            final_key = mod(final_key)
        keyboard.tap_key(final_key)
        self.pending_mods = []

    def process_key(self, keyboard, key, is_pressed, int_coord):
        if not is_pressed: return key
        current_time = supervisor.ticks_ms()

        # Timeout
        if self.active and (current_time - self.last_time > self.timeout):
            self.pending_mods = []
            self.active = False

        # Trigger
        if self.keys_match(key, self.trigger):
            self.active = True
            self.pending_mods = []
            self.last_time = current_time
            return None 

        # Active Logic
        if self.active:
            self.last_time = current_time
            mod = None
            side = None
            
            # Check Maps
            for map_key, map_mod in self.left_map.items():
                if self.keys_match(key, map_key):
                    mod = map_mod
                    side = 'L'
                    break
            if not mod:
                for map_key, map_mod in self.right_map.items():
                    if self.keys_match(key, map_key):
                        mod = map_mod
                        side = 'R'
                        break

            if mod:
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
                self.send_atomic(keyboard, key)
                self.active = False
                return None

        return key


# -------------------------------------------------------------------------
# Custom Module: LayerColorRGB Extension
# Direct Control RGB Module
# read RGB_HELP.md for dock
# -------------------------------------------------------------------------

class LayerColorRGB(Module):
    # --- Configuration ---
    # Define colors here (R, G, B) for easy editing
    COL_NAV   = (255, 0, 0)     # Red
    COL_NUM   = (0, 0, 255)     # Blue
    COL_SYM   = (0, 255, 0)     # Green
    COL_CAPS  = (255, 255, 255) # White

    COL_OFF   = (0, 0, 0)       # Black (Off)
    
    # Brightness (0.0 to 1.0). Keep low (0.1 - 0.2) for USB power safety.
    BRIGHTNESS = 0.022

    def __init__(self, pixel_pin, num_pixels, caps_word_mod=None, lock_status_ext=None):
        self.strip = neopixel.NeoPixel(
            pixel_pin, 
            num_pixels, 
            brightness=self.BRIGHTNESS, 
            auto_write=False
        )
        self.caps_word_mod = caps_word_mod
        self.lock_status_ext = lock_status_ext 
        self.last_color = None 

    def during_bootup(self, keyboard):
        # Quick Red Flash to confirm power/boot
        self.strip.fill(self.COL_NAV)
        self.strip.show()

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        target_color = self.COL_OFF

        # 1. Determine Highest Active Layer
        # Use max() to ensure we get the highest layer index regardless of list order
        top_layer = max(keyboard.active_layers) if keyboard.active_layers else 0
        
        # 2. Assign Color based on Layer
        if top_layer == 4:     # NAV
            target_color = self.COL_NAV
        elif top_layer == 2:   # NUM
            target_color = self.COL_NUM
        elif top_layer == 1:   # SYM
            target_color = self.COL_SYM
        else: 
            # 3. Base Layer Logic (Layer 0)
            # Only check Caps Lock/Word if we are on the Base Layer
            is_caps_on = False

            # Check Standard Caps Lock
            if self.lock_status_ext and self.lock_status_ext.get_caps_lock():
                is_caps_on = True
            # Check Caps Word (using known internal attribute)
            elif self.caps_word_mod and getattr(self.caps_word_mod, '_cw_active', False):
                is_caps_on = True

            if is_caps_on:
                target_color = self.COL_CAPS

        # 4. Update Hardware (Only if color changed)
        if target_color != self.last_color:
            self.strip.fill(target_color)
            self.strip.show()
            self.last_color = target_color

    def before_hid_send(self, keyboard): return
    def after_hid_send(self, keyboard): return

# -------------------------------------------------------------------------
# Sequence Generator Logic
# -------------------------------------------------------------------------
def apply_leader_sequences(keyboard, config, combos_module):
    def get_effective_key(layer_idx, coord):
        for idx in range(layer_idx, -1, -1):
            try:
                key = keyboard.keymap[idx][coord]
                if key != KC.TRNS: return key
            except IndexError: continue
        return None

    for leader_key, seq_list in config.items():
        for coords, output_key in seq_list:
            generated_sequences = set()
            for layer_idx, _ in enumerate(keyboard.keymap):
                current_seq = []
                valid_layer = True
                for coord in coords:
                    eff_key = get_effective_key(layer_idx, coord)
                    if eff_key is None or eff_key == KC.NO:
                        valid_layer = False
                        break
                    current_seq.append(eff_key)


                if valid_layer:
                    full_seq_tuple = (leader_key,) + tuple(current_seq)
                    generated_sequences.add(full_seq_tuple)

            for seq_tuple in generated_sequences:
                combos_module.combos.append(
                    Sequence(seq_tuple, output_key, timeout=2000)
                )
