#!/usr/bin/env python3

"""
BirdEars provides facilities to development of musical ear training
exercises.
"""

import subprocess
import time
from random import randrange, choice
from collections import deque
# from math import floor

DEBUG = True

# FIXME
notes2 = ('C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B')
notes3 = ('C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B')

KEYS = ('C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F', 'F#', 'Gb', 'G', 'G#',
        'Ab', 'A', 'A#', 'Bb', 'B')

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
    'minor': (0, 2, 3, 5, 7, 8, 10, 12),
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

# FIXME: these should be inverted/reverted for descending scales:
KEYBOARD_INDICES = {
    'diatonic': {
        'minor': 'z xc v bn m Z XC V BN M',
        'major': 'z x cv b n mZ X CV B NM'
    },
    'chromatic': {
        'minor': "zsxcfvgbnjmkZSXCFVGBNJMK",
        'major': "zsxdcvgbhnjmZSXDCVGBHNJM",
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

# this is for debugging


def print_stuff(question):
    padd = "─" * 30  # vim: insert mode, ^vu2500
    print("""
{}

Tonic: {} | Note(Int): {} |  Interval: {} | Semitones(Int): {} |
Is Note Chromatic: {} |
Scale: {}, Octave: {}
Resolution: {},
Chromatic: {}
Concrete Scale: {} | Chroma Concrete: {}
{}
""".format(
        padd,
        question.concrete_tonic,
        question.interval['note_and_octave'],
        "─".join(INTERVALS[question.interval['semitones']][1:]),
        question.interval['semitones'],
        question.interval['is_chromatic'],
        "─".join(question.scales['diatonic'].scale),
        "{}-{}".format(question.octave, question.octave + 1),
        "─".join(question.resolution_pitch),
        "─".join(question.scales['chromatic'].scale),
        "─".join(question.scales['diatonic_pitch'].scale),
        "─".join(question.scales['chromatic_pitch'].scale),
        padd,
    ))

def print_stuff_dictation(question):
    padd = "─" * 30  # vim: insert mode, ^vu2500
    print("""
{}

Tonic: {} | Note(Int): {} |  Interval: {} | Semitones(Int): {} |
Scale: {}, Octave: {}
Chromatic: {}
Concrete Scale: {} | Chroma Concrete: {}
{}
""".format(
        padd,
        question.concrete_tonic,
        "─".join(map(str, question.question_phrase)),
        "─".join([INTERVALS[n][1] for n in question.question_phrase]),
        "─".join([str(n) for n in question.question_phrase]),
        "─".join(question.scales['diatonic'].scale),
        "{}-{}".format(question.octave, question.octave + 1),
        "─".join(question.scales['chromatic'].scale),
        "─".join(question.scales['diatonic_pitch'].scale),
        "─".join(question.scales['chromatic_pitch'].scale),
        padd,
    ))

dictate_notes = 4


def main():
    from .questions.melodicdictation import MelodicDictationQuestion
    getch = _Getch()

    new_question_bit = True

    while True:
        if new_question_bit is True:

            new_question_bit = False

            input_keys = []
            # question = MelodicDictateQuestion(mode='major',descending=True)
            question = MelodicDictationQuestion(mode='major')
            # question = HarmonicIntervalQuestion(mode='major')
            # question = HarmonicIntervalQuestion(mode='major')

            # debug
            if DEBUG:
                print_stuff_dictation(question)

            question.play_question()

        user_input = getch()

        # any response input interval from valid keys
        if user_input in question.keyboard_index and user_input != ' ':  # spc

            input_keys.append(user_input)
            print(user_input, end='')

            if len(input_keys) == dictate_notes:
                # response = question.check_question(user_input)
                response = question.check_question(input_keys)

                if response['is_correct']:
                    # print("Correct!.. it is “{}”".\
                    # format( response['user_interval']))
                    print("Correct! It was semitones {}".
                          format("-".join(map(str, question.question_phrase))))
                else:
                    print("It is incorrect...")
                    print("You replied semitones {} but the correct is "
                          "semitones {}".format(response['user_semitones'],
                                                question.question_phrase))

                question.play_resolution()

                new_question_bit = True
            # else:
            #    input_keys.append(user_input)
            #    print(user_input,)

        # q - quit
        elif user_input == 'q':
            exit(0)

        # r - repeat interval
        elif user_input == 'r':
            question.play_question()

# wait_keys = 1
# def main():
#     from .harmonicintervalquestion import HarmonicIntervalQuestion
#     from .melodicintervalquestion import MelodicIntervalQuestion
#     getch = _Getch()
#
#     new_question_bit = True
#
#     while True:
#         if new_question_bit is True:
#
#             new_question_bit = False
#
#             input_keys = []
#             #question = HarmonicIntervalQuestion(mode='major')
#             question = MelodicIntervalQuestion(mode='major',descending=True)
#
#             # debug
#             if DEBUG:
#                 print_stuff(question)
#
#             question.play_question()
#
#         user_input = getch()
#
#         if user_input in question.keyboard_index:
#             response = question.check_question(user_input)
#
#             if response['is_correct']:
#                 print("Correct!.. it is “{}”".\
#                 format( response['user_interval']))
#             else:
#                 print("It is incorrect... correct is {}.. you said {}".format(question.interval['data'],response['user_interval']))
#
#             question.play_resolution()
#
#             new_question_bit = True
#
#         # q - quit
#         elif user_input == 'q':
#             exit(0)
#
#         # r - repeat interval
#         elif user_input == 'r':
#             question.play_question()
