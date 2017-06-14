"""
BirdEars provides facilities to musical ear training exercises.
"""

from .logger import logger
logger.info('Starting app...')
logger.debug('Starting appzz...')

DEBUG = False

CHROMATIC_SHARP = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#',
                   'B')
CHROMATIC_FLAT = ('C', 'Db', 'D', 'Eb', 'Fb', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb',
                  'Cb')

KEYS = ('C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#',
        'Ab', 'A', 'A#', 'Bb', 'B')

CIRCLE_OF_FIFTHS = [
        ('C', 'G', 'D', 'A', 'E', 'B', 'Gb', 'Db', 'Ab', 'Eb', 'Bb', 'F'),
        ('C', 'F', 'Bb', 'Eb', 'Ab', 'C#', 'F#', 'Cb', 'E', 'A', 'D', 'G')
    ]

INTERVALS = (
    (0, 'P1', 'Perfect Unison'),
    (1, 'm2', 'Minor Second'),
    (2, 'M2', 'Major Second'),
    (3, 'm3', 'Minor Third'),
    (4, 'M3', 'Major Third'),
    (5, 'P4', 'Perfect Fourth'),
    (6, 'A4', 'Augmented Fourth'),
    (7, 'P5', 'Perfect Fifth'),
    (8, 'm6', 'Minor Sixth'),
    (9, 'M6', 'Major Sixth'),
    (10, 'm7', 'Minor Seventh'),
    (11, 'M7', 'Major Seventh'),
    (12, 'P8', 'Perfect Octave'),
    (13, 'A8', 'Minor Ninth'),
    (14, 'M9', 'Major Ninth'),
    (15, 'm10', 'Minor Tenth'),
    (16, 'M10', 'Major Tenth'),
    (17, 'P11', 'Perfect Eleventh'),
    (18, 'A11', 'Augmented Eleventh'),
    (19, 'P12', 'Perfect Twelfth'),
    (20, 'm13', 'Minor Thirteenth'),
    (21, 'M13', 'Major Thirteenth'),
    (22, 'm14', 'Minor Fourteenth'),
    (23, 'M14', 'Major Fourteenth'),
    (24, 'P15', 'Perfect Double-octave'),
    (25, 'A15', 'Minor Sixteenth'),
    (26, 'M16', 'Major Sixteenth'),
    (27, 'm17', 'Minor Seventeenth'),
    (28, 'M17', 'Major Seventeenth'),
    (29, 'P18', 'Perfect Eighteenth'),
    (30, 'A18', 'Augmented Eighteenth'),
    (31, 'P19', 'Perfect Nineteenth'),
    (32, 'm20', 'Minor Twentieth'),
    (33, 'M20', 'Major Twentieth'),
    (34, 'm21', 'Minor Twenty-first'),
    (35, 'M21', 'Major Twenty-first'),
    (36, 'P22', 'Perfect Triple-octave')
)

CHROMATIC_TYPE = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12)
DIATONIC_MODES = {
    'major': (0, 2, 4, 5, 7, 9, 11, 12),
    'dorian': (0, 2, 3, 5, 7, 9, 10, 12),
    'phrygian': (0, 1, 3, 5, 7, 8, 10, 12),
    'lydian': (0, 2, 4, 6, 7, 9, 11, 12),
    'mixolydian': (0, 2, 4, 5, 7, 9, 10, 12),
    'minor': (0, 2, 3, 5, 7, 8, 10, 12),
    'locrian': (0, 1, 3, 5, 6, 8, 10, 12),
}

INTERVAL_INDEX = {
    1: [0],
    2: [1, 2],
    3: [3, 4],
    4: [5, 6],
    5: [6, 7],
    6: [8, 9],
    7: [10, 11],
    8: [12]
}
# MAJOR keyboard keys (with chromatics)
# keyindex for major and chromatic major context
#  s d   g h j        IIb  IIIb       Vb VIb  VIIb
# z x c v b n m  <-  I   II   III  IV   V   VI   VII
#
#  -- SHIFT meaning an octave higher

# MINOR keyboard keys (with chromatics)
# keyindex for minor and chromatic minor context
#
#  s   f g   j k   eg.:      a#   c# d#    f# g#
# z x c v b n m    -------  a  b c  d  e  f  g


# it is better if this is made progamatically
# note that all diatonic are in keys zxcvvbnm, and uppercase
KEYBOARD_INDICES = {
    'diatonic': {
        'ascending': {
            'minor': 'z xc v bn m Z XC V BN M,',
            'major': 'z x cv b n mZ X CV B NM,'
        },
        # FIXME
        'descending': {
            'minor': 'z xc v bn m Z XC V BN M,',
            'major': 'z x cv b n mZ X CV B NM,'
        },
    },
    'chromatic': {
        'ascending': {
            'major':      "zsxdcvgbhnjm,SXDCVGBHNJMZ",
            'dorian':     "zsxcfvgbhnmk,SXCFVGBHNMKZ",
            'phrygian':   "zxdcfvgbnjmk,XDCFVGBNJMKZ",
            'lydian':     "zsxdcfvbhnjm,SXDCFVBHNJMZ",
            'myxolidian': "zsxdcvgbhnmk,SXDCVGBHNMNZ",
            'minor':      "zsxcfvgbnjmk,SXCFVGBNJMKZ",
            'locrian':    "zxdcfvbhnjmk,XDCFVBHNJMKZ",
        },
        'descending': {
            'major':      ",mjnhbgvcdxszMJNHBGVCDXSZ",
            'dorian':     ",kmnhbgvfcxszKMNHBGVFCXSZ",
            'dorian':     ",kmnhbgvfcxszKMNHBGVFCXSZ",
            'phrygian':   ",kmjnbgvfcdxzKMJNBGVFCDXZ",
            'lydian':     ",mjnhbvfcdxszMJNHBVFCDXSZ",
            'mixolydian': ",kmnhbgvcdxszKMNHBGVCDXSZ",
            'minor':      ",kmjnbgvfcxszKMJNBGVFCXSZ",
            'locrian':    ",kmjnhbvfcdxzKMJNHBVFCDXZ",
        }
    }
}

# how many steps to resolve on tonic,
# after which resolves on tonic octave
# (begins on 0 as it is an index)
# 5 is tritone; then
# [0 1 2 3 4 5] resolves below (tonic)
# and [6 7 8 9 10 11] resolves above (octave)

MAX_SEMITONES_RESOLVE_BELOW = 5


# http://code.activestate.com/recipes/134892/
class _Getch:
    """Gets a single character from standard input.  Does not echo to the
screen."""

    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()


class _GetchUnix:
    def __init__(self):
        import tty
        import sys

    def __call__(self):
        import sys
        import tty
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
