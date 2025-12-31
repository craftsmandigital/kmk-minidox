from kmk.keys import KC
from features import *

# -------------------------------------------------------------------------
# KEYMAP GRID
# -------------------------------------------------------------------------
LAYERS = [
    # LAYER 0: BASE
    [
        KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,        KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,
        KC.A,    KC.S,    KC.D,    KC.F,    KC.G,        KC.H,    KC.J,    KC.K,    KC.L,    NO_OE,
        KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,        KC.N,    KC.M,    LEAD,    NO_AA,   NO_AE,
        XXXX,    XXXX,    NAV_HT,  KC.SPC,  SYM_SK,      KC.ENT,  KC.BSPC, NUM_SK,  XXXX,    XXXX,
    ],

    # LAYER 1: SYM
    [
        KC.PLUS, KC.EXLM, KC.SCLN, US_QUOT, KC.ASTR,     KC.COMM, KC.LPRN, KC.RPRN, KC.LCBR, KC.RCBR,
        KC.MINS, KC.QUES, KC.COLN, US_DQUO, KC.SLSH,     KC.DOT,  KC.ESC,  OS_LCTL, OS_LALT, OS_LGUI,
        KC.PERC, US_TILD, KC.PIPE, US_GRV,  KC.EQL,      KC.UNDS, KC.LABK, KC.RABK, KC.LBRC, KC.RBRC,
        XXXX,    XXXX,    US_CIRC, KC.AT,   KC.BSLS,     KC.AMPR, KC.DEL,  KC.DLR,  XXXX,    XXXX,
    ],

    # LAYER 2: NUM
    [
        KC.PLUS, KC.N7,   KC.N8,   KC.N9,   KC.ASTR,     KC.COMM, KC.LPRN, KC.RPRN, KC.LCBR, KC.RCBR,
        KC.MINS, KC.N3,   KC.N2,   KC.N1,   KC.SLSH,     KC.DOT,  OS_LSFT, OS_LCTL, OS_LALT, OS_LGUI,
        KC.PERC, KC.N4,   KC.N5,   KC.N6,   KC.EQL,      KC.UNDS, KC.TAB,  KC.RABK, KC.LBRC, KC.RBRC,
        XXXX,    XXXX,    KC.N0,   KC.SPC,  KC.CW,       KC.CAPS, KC.DEL,  FUN_SK,  XXXX,    XXXX,
    ],

    # LAYER 3: FUN
    [
        XXXX,    KC.F7,   KC.F8,   KC.F9,   XXXX,        XXXX,    XXXX,    XXXX,    XXXX,    XXXX,
        XXXX,    KC.F3,   KC.F2,   KC.F1,   XXXX,        XXXX,    OS_LSFT, OS_LCTL, OS_LALT, OS_LGUI,
        XXXX,    KC.F4,   KC.F5,   KC.F6,   XXXX,        XXXX,    XXXX,    XXXX,    XXXX,    XXXX,
        XXXX,    XXXX,    KC.F10,  KC.F11,  KC.F12,      XXXX,    XXXX,    XXXX,    XXXX,    XXXX,
    ],

    # LAYER 4: NAV
    [
        XXXX,    SelAll,  XXXX,    XXXX,    XXXX,        KC.HOME, KC.PGDN, KC.PGUP, KC.END,  Redo,
        OS_LGUI, OS_LALT, OS_LCTL, OS_LSFT, XXXX,        KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT, Undo,
        XXXX,    XXXX,    Copy,    Paste,   XXXX,        WordL,   KC.TAB,  ALT_TAB, WordR,   XXXX,
        XXXX,    Cut,     TRNS,    TRNS,    XXXX,        TRNS,    TRNS,    XXXX,    XXXX,    XXXX,
    ]
]

