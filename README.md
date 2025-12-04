# Dactyl Minidox (KMK Firmware)

A custom, hand-wired 36-key split keyboard running on **[KMK Firmware](https://github.com/KMKfw/kmk_firmware)** and **[Raspberry Pi Pico](https://www.raspberrypi.com/products/raspberry-pi-pico/)** (RP2040).

This repository contains the source code and configuration for a **Dactyl Minidox** build that features **Nordic character support** on a **[US-International](https://en.wikipedia.org/wiki/QWERTY#US-International)** layout, a modular code structure, and a **"Stealth Mode"** boot script.

## 🌟 Features

* **Split Keyboard:** 36 keys (5x3 + 3 thumbs per side).
* **Visual Wiring:** Wiring logic is "Left-to-Right" on both halves (no mirroring required in firmware).
* **Nordic Support:** Type **Æ Ø Å** seamlessly while keeping the coding-friendly **US Layout** (using **[US-International](https://en.wikipedia.org/wiki/QWERTY#US-International)** OS settings).
* **Dead Key Fixes:** Automatic macros to fix annoying dead keys (`' " ^ ~`) common in International layouts.
* **Stealth Drive:** The USB drive is hidden by default to prevent popups.
* **Maintenance Mode:** Unlock the USB drive by holding specific keys during plug-in.
* **Modular Code:** Configuration is split into `hardware.py`, `layout.py`, and `code.py` for easy maintenance.

---

## 🛠️ Hardware & Wiring

For a complete, step-by-step tutorial on hand-wiring this keyboard—including detailed pinout diagrams, matrix logic, and assembly instructions—please consult the full build guide:

👉 **[Read the Dactyl Minidox Build Guide](https://how-to-do-stuff.pages.dev/Keyboard-related/dactyl_minidox_kmk_keyboard_build)**

---

## 📂 File Structure

* [boot.py](./boot.py): Runs at startup. Checks for "Maintenance Keys" to decide if the **[CircuitPython](https://circuitpython.org/)** USB drive should be visible.
* [code.py](./code.py): The main firmware logic. Sets up the keyboard, split communication, and keymap.
* [hardware.py](./hardware.py): Central configuration for Pin definitions. Imported by both `boot.py` and `code.py`.
* [layout.py](./layout.py): Custom key definitions, macros for Nordic characters, and dead key fixes.

---

## 🚀 Installation

1. **Install CircuitPython:** Download and flash the latest **[CircuitPython for Raspberry Pi Pico](https://circuitpython.org/board/raspberry_pi_pico/)** `.uf2` file onto both Picos.
2. **Install KMK:** Download the **[KMK Firmware](https://github.com/KMKfw/kmk_firmware)**, unzip it, and copy the `kmk` folder into the `lib/` folder on both drives.
3. **Deploy Code:** Copy `boot.py`, `code.py`, `hardware.py`, and `layout.py` from this repository to the root directory of **BOTH** drives.

---

## 🔒 Maintenance Mode (Unlocking the Drive)

By default, the `CIRCUITPY` USB drive is **hidden** when you plug in the keyboard to keep your desktop clean. To edit your code:

1. **Unplug** the keyboard.
2. **Hold** the top-corner key:
    * **Left Side:** Hold **Q** (Top-Left).
    * **Right Side:** Hold **P** (Top-Right).
3. **Plug in** the USB cable while holding the key.
4. Release the key after 1 second. The drive will appear.

---

## ⌨️ Layout & Nordic Characters

This keyboard is designed to be used with the **[US-International](https://en.wikipedia.org/wiki/QWERTY#US-International)** input language setting on your computer (Windows/macOS/Linux).

### Custom Macros (`layout.py`)

To solve the "Dead Key" issue on US-International (where you have to type space after a quote), this firmware uses custom macros:

* **`layout.US_QUOT`**: Types `'` + `Space` instantly.
* **`layout.NO_AE`**: Sends `AltGr` + `Z` (Æ).
* **`layout.NO_OE`**: Sends `AltGr` + `L` (Ø).
* **`layout.NO_AA`**: Sends `AltGr` + `W` (Å).

### Modifying the Keymap

Edit **`code.py`** to change your layers. Use the custom keys defined in `layout.py` for special characters.

```python
# Example in code.py
keyboard.keymap = [
    [
        # ...
        layout.NO_AA, layout.NO_AE, layout.NO_OE, ...
    ]
]
