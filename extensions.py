import supervisor
from kmk.keys import KC
from kmk.modules import Module
from kmk.modules.combos import Sequence
# from kmk.extensions.rgb import RGB
import neopixel
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
    def __init__(self, pixel_pin, num_pixels, caps_word_mod=None, lock_status_ext=None):
        self.strip = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.1, auto_write=False)
        self.caps_word_mod = caps_word_mod
        self.lock_status_ext = lock_status_ext 
        self.last_color = None 

    def during_bootup(self, keyboard):
        # Flash RED on boot
        self.strip.fill((255, 0, 0))
        self.strip.show()

    def before_matrix_scan(self, keyboard):
        return

    def after_matrix_scan(self, keyboard):
        target_color = (0, 0, 0) # Default

        # -----------------------------------------------------------------
        # 1. Check Layers (Highest Priority)
        # -----------------------------------------------------------------
        top_layer = 0
        if keyboard.active_layers:
            top_layer = max(keyboard.active_layers)
        
        if top_layer == 4:     # NAV
            target_color = (255, 0, 0)   # Red
        elif top_layer == 2:   # NUM
            target_color = (0, 0, 255)   # Blue
        elif top_layer == 1:   # SYM
            target_color = (0, 255, 0)   # Green
            
        else: 
            # -------------------------------------------------------------
            # 2. Base Layer Logic (Layer 0)
            # -------------------------------------------------------------
            is_caps_on = False

            # A. Check Standard Caps Lock
            if self.lock_status_ext and self.lock_status_ext.get_caps_lock():
                is_caps_on = True
                
            # B. Check Caps Word
            if not is_caps_on and self.caps_word_mod:
                # FIX: Check '_cw_active' based on your debug output
                if getattr(self.caps_word_mod, '_cw_active', False):
                    is_caps_on = True
                # Fallback checks for other versions
                elif getattr(self.caps_word_mod, '_active', False):
                    is_caps_on = True
                elif getattr(self.caps_word_mod, 'active', False):
                    is_caps_on = True

            if is_caps_on:
                target_color = (255, 255, 255) # White
            else:
                target_color = (0, 0, 0)       # Off

        # -----------------------------------------------------------------
        # 3. Update LEDs
        # -----------------------------------------------------------------
        if target_color != self.last_color:
            # Debug print
            print(f"RGB UPDATE: Layer={top_layer}, Color={target_color}")
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
