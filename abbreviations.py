from kmk.keys import KC
from kmk.modules.macros import Tap

# 1. Define Lowercase
AE = Tap(KC.RALT(KC.Z))      # æ
OE = Tap(KC.RALT(KC.L))      # ø
AA = Tap(KC.RALT(KC.W))      # å

# Uppercase (Shift + AltGr + Key)
AE_CAP = Tap(KC.LSFT(KC.RALT(KC.Z)))    # Æ
OE_CAP = Tap(KC.LSFT(KC.RALT(KC.L)))    # Ø
AA_CAP = Tap(KC.LSFT(KC.RALT(KC.W)))    # Å

abbrevs = {
    # Simple strings
    "ja": "Jon Arne",
    "firm": "KMK",
    
    # Lowercase example: "Hør og Bør"
    "al": ("Daglig leder\nH", OE, "r og B", OE, "r i Oslo"),
    
    # Uppercase example: "Åsane i Østfold"
    "ex": (AA_CAP, "sane i ", OE_CAP, "stfold"),
    
    # Mixed example: "Vær så god"
    "vg": ("V", AE, "r s", AA, " god"),
}
