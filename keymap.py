from kmk.keys import KC
from behaviors import *
from macros import *

# -------------------------------------------------------------------------
# KEYMAP GRID
# -------------------------------------------------------------------------
LAYERS = [
    # LAYER 0: BASE
        [
            # 0        1        2        3        4            5        6        7        8        9
        KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,        KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,

        # 10       11       12       13       14           15       16       17       18       19
        KC.A,    KC.S,    KC.D,    KC.F,    KC.G,        KC.H,    KC.J,    KC.K,    KC.L,    NO_OE,

        # 20       21       22       23       24           25       26       27       28       29
        KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,        KC.N,    KC.M,    LEAD,    NO_AA,   NO_AE,

        # 30       31       32       33       34           35       36       37       38       39
        XXXX,    XXXX,    NAV_HT,  KC.SPC,  SYM_SK,      KC.ENT,  KC.BSPC, NUM_SK,  XXXX,    XXXX,
    ],
    # LAYER 1: SYM
    [
        # Left Hand                                      # Right Hand
        # +        !        ;        '        *            #        (        )        {        }
        KC.PLUS, KC.EXLM, KC.SCLN, US_QUOT, KC.ASTR,     KC.HASH, KC.LPRN, KC.RPRN, KC.LCBR, KC.RCBR,

        # -        ?        :        "        /            ,        .        Ctrl     Alt      GUI
        KC.MINS, KC.QUES, KC.COLN, US_DQUO, KC.SLSH,     KC.COMM, KC.DOT,  OS_LCTL, OS_LALT, OS_LGUI,

        # %        ~        |        `        =            _        <        >        [        ]
        KC.PERC, US_TILD, KC.PIPE, US_GRV,  KC.EQL,      KC.UNDS, KC.LABK, KC.RABK, KC.LBRC, KC.RBRC,

        # (None)   (None)   ^        @        \            &        Del      $        (None)   (None)
        XXXX,    XXXX,    US_CIRC, KC.AT,   KC.BSLS,     KC.AMPR, KC.DEL,  KC.DLR,  XXXX,    XXXX,
    ],
    # LAYER 2: NUM
    [
        KC.PLUS, KC.N7,   KC.N8,   KC.N9,   KC.ASTR,     KC.HASH, KC.LPRN, KC.RPRN, KC.LCBR, KC.RCBR,
        KC.MINS, KC.N3,   KC.N2,   KC.N1,   KC.SLSH,     KC.COMM, KC.ESC,  OS_LCTL, OS_LALT, OS_LGUI,
        KC.PERC, KC.N4,   KC.N5,   KC.N6,   KC.EQL,      KC.UNDS, KC.TAB,  KC.RABK, KC.LBRC, KC.RBRC,
        XXXX,    XXXX,    KC.N0,   KC.SPC,  KC.CW,       KC.CAPS, KC.BSPC, FUN_SK,  XXXX,    XXXX,
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
        OS_LGUI, OS_LALT, OS_LCTL, OS_LSFT, PasteM,      KC.LEFT, KC.DOWN, KC.UP,   KC.RGHT, Undo,
        XXXX,    Cut,     Copy,    PasteU,  Paste,       WordL,   KC.TAB,  ALT_TAB, WordR,   RClick,
        XXXX,    XXXX,    TRNS,    TRNS,    XXXX,        TRNS,    TRNS,    XXXX,    XXXX,    XXXX,
    ]
]

