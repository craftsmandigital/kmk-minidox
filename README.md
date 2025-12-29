# ⌨️ Dactyl Minidox - KMK Firmware

![KMK Firmware](https://img.shields.io/github/v/release/KMKfw/kmk_firmware?label=KMK%20Firmware&logo=python)
![CircuitPython](https://img.shields.io/badge/CircuitPython-${CIRCUITPY_VERSION}-blue)
![Platform](https://img.shields.io/badge/Platform-RP2040-Pico-X2-Blue%20Micro-success)

> A hand-wired, split ergonomic keyboard powered by Raspberry Pi Pico (RP2040) and [KMK Firmware](https://github.com/KMKfw/kmk_firmware).

This repository contains the source code and configuration for a **Dactyl Minidox** build. It features a modular codebase, a custom Norwegian/US-International hybrid layout, Vim-style navigation, and a "Stealth Mode" that hides the USB drive by default.

## 📖 Build Guide

For a complete, step-by-step tutorial on hand-wiring this keyboard—including detailed pinout diagrams, matrix logic, and assembly instructions—please consult the full build guide:

👉 **[Read the Dactyl Minidox Build Guide](https://how-to-do-stuff.pages.dev/Keyboard-related/dactyl_minidox_kmk_keyboard_build)**

---

## ⚠️ Important: OS Layout

To use the Norwegian characters (`Æ`, `Ø`, `Å`) and the dead-key fixes provided in this firmware, you **must** set your computer's input language to **US-International**.

* **Windows/Linux/macOS**: Set keyboard layout to **US-International**.
* The firmware handles the translation of macros (e.g., `AltGr` + `L`) to produce the correct characters on screen.

---

## 📂 Project Structure

The code is organized into logical modules for easy maintenance. Click the files below to view them:

| File | Description |
| :--- | :--- |
| **[`code.py`](./code.py)** | **The Entry Point.** Initializes hardware, loads modules in the correct order, and runs the keyboard. |
| **[`hardware.py`](./hardware.py)** | **Physical Config.** Defines the `DactylMinidox` class, GPIO pinouts, diode orientation, and split logic. |
| **[`features.py`](./features.py)** | **The Logic.** Contains Macros, Combos, Custom Keys, Helper functions, and Layer definitions. |
| **[`keymap.py`](./keymap.py)** | **The Visuals.** Contains the raw keymap grid and layer layout. |
| **[`boot.py`](./boot.py)** | **Startup Script.** Handles "Stealth Mode" (hides the USB drive unless a key is held). |

---

## ✨ Features

* **Split Architecture**: Two RP2040s communicating via UART (TRRS).
* **"Split Flip" Wiring**: Identical pinout definition for both sides (Right side columns wired in reverse).
* **Norwegian Support**: Type **Æ Ø Å** seamlessly on a US layout.
* **Dead Key Fixes**: Automatic macros to fix annoying dead keys (`' " ^ ~`).
* **Stealth Drive**: The USB drive is hidden by default to prevent popups.
* **Advanced Input**:
  * **Combos**: Auto-closing brackets `()`, `{}`, `[]`, `<>` and quotes.
  * **Leader Key**: Sequences for Sticky Modifiers.
  * **One-Shot Layers**: Sticky keys for seamless layer switching.
  * **Vim Navigation**: HJKL-style movement on the Nav layer.

---

## 🔌 Hardware & Wiring

### Pinout Configuration

Both halves use the same GPIO pins.

| Matrix Position | RP2040 Pin | Note |
| :--- | :--- | :--- |
| **Row 0** (Top) | `GP6` | |
| **Row 1** | `GP7` | |
| **Row 2** | `GP8` | |
| **Row 3** (Thumbs) | `GP9` | |
| **Col 0** (Pinky) | `GP2` | |
| **Col 1** | `GP3` | |
| **Col 2** | `GP4` | |
| **Col 3** | `GP5` | |
| **Col 4** (Inner) | `GP28` | |
| **UART (Data)** | `GP1` | Connects TRRS Tip/Ring |
| **Side Detect** | `GP21` | **Jumper to GND** = Right Side |

### ⚠️ The "Split Flip" Wiring

To allow identical firmware on both sides, the **Right Half** columns must be physically wired in reverse order compared to the Left Half.

* **Left Side**: Col 0 (Pinky) $\rightarrow$ GP2 ... Col 4 (Inner) $\rightarrow$ GP28
* **Right Side**: Col 0 (Pinky) $\rightarrow$ GP28 ... Col 4 (Inner) $\rightarrow$ GP2

---

## 🗺️ Layout & Layers

### Layer 0: BASE

Standard QWERTY.

* **Thumbs**: `Space`, `Enter`, `Backspace`, and Sticky Layer keys (`SYM`, `NUM`).
* **Leader Key**: Located on the inner column (Right hand).

### Layer 1: SYM (Symbols)

Activated via One-Shot (Sticky) key.

* Contains all programming symbols (`!`, `@`, `#`, `{`, `}`, etc.).
* Includes One-Shot Modifiers on the home row.

### Layer 2: NUM (Numbers)

Activated via One-Shot (Sticky) key.

* **Left Hand**: Numpad (`789`, `456`, `123`, `0`).
* **Right Hand**: Navigation symbols and modifiers.

### Layer 3: FUN (Function)

Activated via Combo (`Backspace` + `NUM` key).

* F1 - F12 keys.

### Layer 4: NAV (Navigation)

Activated by **Tapping** the Toggle key, or **Holding** for momentary access.

* **Left Hand**: Clipboard tools (`Select All`, `Copy`, `Cut`, `Paste`).
* **Right Hand**: Arrow keys, `Home`, `End`, `PgUp`, `PgDn`.
* **Special**: Sticky `Alt+Tab` for window switching.

---

## 🚀 Advanced Usage

### ⚡ Combos (Brackets)

Pressing two keys simultaneously triggers macros that type the brackets and move the cursor inside them.

| Chord | Result |
| :--- | :--- |
| `(` + `)` | `(|)` |
| `{` + `}` | `{|}` |
| `[` + `]` | `[|]` |
| `<` + `>` | `<|>` |
| `'` + `;` | `'|'` |
| `"` + `:` | `"|"` |

### 👑 Leader Key Sequences

Tap the **Leader Key** (`F24`), then tap a letter to activate a Sticky Modifier.

* `Lead` + `F` $\rightarrow$ Sticky **Right Shift**
* `Lead` + `D` $\rightarrow$ Sticky **Right Ctrl**
* `Lead` + `S` $\rightarrow$ Sticky **Left Alt**
* `Lead` + `A` $\rightarrow$ Sticky **Right GUI**
* *(Mirrored on the Left hand with J, K, L, ;)*

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

## 🛠️ Installation

1. **Install CircuitPython**: Flash the latest **[CircuitPython for Raspberry Pi Pico](https://circuitpython.org/board/raspberry_pi_pico/)** `.uf2` file onto both Picos.
2. **Install KMK**: Download the **[KMK Firmware](https://github.com/KMKfw/kmk_firmware)**, unzip it, and copy the `kmk` folder into the `lib/` folder on both drives.

3. **Deploy Code**: Copy `boot.py`, `code.py`, `hardware.py`, `features.py`, and `keymap.py` to the root directory of **BOTH** drives.
