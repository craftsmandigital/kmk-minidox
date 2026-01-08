# LayerColorRGB Module Documentation

## Overview
**LayerColorRGB** is a custom, high-performance module designed for the Dactyl Minidox. Unlike standard RGB animations that cycle through rainbows, this module provides **functional status lighting**. It talks directly to the hardware to ensure instant response times and stability.

## Features
1.  **Layer Indication**: Instantly changes color when you switch layers (NAV, NUM, SYM).
2.  **Smart Caps Indication**:
    *   If you are on the **Base Layer**, the LEDs turn **White** when Caps Lock or Caps Word is active.
    *   If you are on a **Function Layer** (like NAV), the Layer Color takes priority so you always know where you are.
3.  **Power Saving**: Automatically turns LEDs off (Black) on the Base layer when not in use.
4.  **Split Support**: Works on both halves of a split keyboard (requires file synchronization).

---

## Prerequisites
Before using this module, ensure your `CIRCUITPY/lib` folder contains:
*   `neopixel.mpy` (Required for direct hardware control)


---

## Installation & Setup

### 1. `code.py` Configuration
This module requires access to the `CapsWord` module and the `LockStatus` extension to function correctly.

```python
# 1. Initialize Dependencies
caps_word = CapsWord()
lock_status = LockStatus()

# 2. Register Dependencies
keyboard.modules.append(caps_word)
keyboard.extensions.append(lock_status)

# 3. Configure RGB
from extensions import LayerColorRGB

rgb = LayerColorRGB(
    pixel_pin=keyboard.rgb_pixel_pin,  # Defined in hardware.py
    num_pixels=keyboard.num_pixels,    # Defined in hardware.py
    caps_word_mod=caps_word,           # To detect Caps Word state
    lock_status_ext=lock_status        # To detect Standard Caps Lock state
)

# 4. Register as a Module
keyboard.modules.append(rgb)
```

### 2. `hardware.py` Configuration
Ensure your pin definitions match your soldering.

```python
self.rgb_pixel_pin = board.GP16  # The pin connected to LED Data (Green wire)
self.num_pixels = 8              # Number of LEDs per side
```

---

## Customization

You can change colors and brightness directly in **`extensions.py`**. Look for the `LayerColorRGB` class definition at the bottom of the file.

### Changing Colors
Colors are defined as `(Red, Green, Blue)` tuples, ranging from 0 to 255.

```python
class LayerColorRGB(Module):
    # --- Configuration ---
    COL_NAV   = (255, 0, 0)     # Red
    COL_NUM   = (0, 0, 255)     # Blue
    COL_SYM   = (0, 255, 0)     # Green
    COL_CAPS  = (255, 255, 255) # White
    COL_OFF   = (0, 0, 0)       # Black (Off)
```

### Changing Brightness
**Warning:** SK6812/WS2812 LEDs draw significant power.
*   **0.1 (10%)**: Recommended for USB power.
*   **0.2 (20%)**: Very bright.
*   **> 0.5**: Risk of overheating or USB disconnect.

```python
    # Brightness (0.0 to 1.0)
    BRIGHTNESS = 0.1
```

---


## Logic Hierarchy

The module decides which color to show based on this strict priority list:

1.  **Function Layers** (Highest Priority)

    *   If Layer 4 (NAV) is active -> **Red**
    *   If Layer 2 (NUM) is active -> **Blue**
    *   If Layer 1 (SYM) is active -> **Green**
    *   *Note: This ensures you never get lost in a layer, even if Caps Lock is on.*

2.  **Base Layer** (Layer 0)
    *   If **Caps Lock** OR **Caps Word** is Active -> **White**
    *   Otherwise -> **Black (Off)**

---

## Troubleshooting

### 1. LEDs are completely dark
*   **Check Wiring:** Is the LED strip direction correct? (Arrows must point away from the controller).
*   **Check Pin:** Does `hardware.py` match the physical pin?
*   **Check Libs:** Is `neopixel.mpy` in the `lib` folder?

### 2. Caps Word doesn't turn lights White
*   Ensure you are on the **Base Layer**. (Layer colors override Caps colors).
*   Ensure `caps_word` was passed correctly in `code.py`.

### 3. Right side LEDs are off or stuck on Red
*   **Sync Files:** The Right Side (Slave) **must** have the exact same `extensions.py`, `code.py`, and `lib/neopixel.mpy` as the Left Side.
*   **Check Cable:** Ensure the TRRS cable is fully inserted.
