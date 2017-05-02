#!/usr/bin/env python3

"""
BirdEars provides facilities to development of musical ear training
exercises.
"""

import subprocess
import time
from random import randrange, choice
from collections import deque
from math import floor

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


class Scale:
    """Builds a musical scale.

    Attributes
    ----------
    scale : array_type
        the array of notes representing the scale.
    """

    def __init__(self, tonic, mode=None, octave=None, n_octaves=None,
                 chromatic=None, descending=None, dont_repeat_tonic=None):
        if not chromatic:
            scale = self.get_diatonic(tonic=tonic, mode=mode, octave=octave,
                                      n_octaves=n_octaves,
                                      descending=descending,
                                      dont_repeat_tonic=dont_repeat_tonic)
        else:
            scale = self.get_chromatic(tonic=tonic, octave=octave,
                                       n_octaves=n_octaves,
                                       descending=descending,
                                       dont_repeat_tonic=dont_repeat_tonic)

        self.scale = scale
        self.chromatic = chromatic

    def get_chromatic(self, tonic, octave=None, n_octaves=None,
                      descending=None, dont_repeat_tonic=None):
        """Returns a chromatic scale from tonic.

        Parameters
        ----------
        tonic : str
            The note which the scale will be built upon.
        octave : int
            The scientific octave the scale will be built upon.
        n_octaves : int
            The number of octaves the scale will contain.
        descending : bool
            Whether the scale is descending.
        dont_repeat_tonic : bool
            Whethe to skip appending the last note (octave) to the scale.
        """

        global notes3, notes2

        tonic_index = self._get_chromatic_idx(tonic)

        if tonic == 'F' or 'b' in tonic:
            notes = deque(notes3)
        else:
            notes = deque(notes2)

        notes.rotate(-(tonic_index))

        if n_octaves:
            chromatic = notes * n_octaves
        else:
            chromatic = notes

        # FIXME: check if this works on descending
        if not dont_repeat_tonic:
            chromatic.append(chromatic[0])

        if descending:
            chromatic.reverse()

        if octave:
            chromatic = self._append_octave_to_scale(scale=chromatic,
                                                     starting_octave=octave,
                                                     descending=descending)

        return chromatic

    def get_diatonic(self, tonic, mode, octave=None, n_octaves=None,
                     descending=None, dont_repeat_tonic=None):
        """Returns a diatonic scale from tonic and mode.

        Parameters
        ----------
        tonic : str
            The note which the scale will be built upon.
        mode : str
            The mode the scale will be built upon. ('major' or 'minor')
        octave : int
            The scientific octave the scale will be built upon.
        n_octaves : int
            The number of octaves the scale will contain.
        descending : bool
            Whether the scale is descending.
        dont_repeat_tonic : bool
            Whether to skip appending the last note (octave) to the scale.
        """

        global DIATONIC_MODES

        diatonic_mode = DIATONIC_MODES[mode]

        chromatic = self.get_chromatic(tonic)

        diatonic = [chromatic[semitones] for semitones in diatonic_mode[:-1]]

        if n_octaves:
            diatonic = diatonic * n_octaves

        # FIXME: check if this works on descending
        if not dont_repeat_tonic:
            diatonic.append(chromatic[diatonic_mode[-1]])

        if descending:
            diatonic.reverse()

        if octave:
            diatonic = self._append_octave_to_scale(scale=diatonic,
                                                    starting_octave=octave,
                                                    descending=descending)

        return diatonic

    def _append_octave_to_scale(self, scale, starting_octave, descending=None):
        """Inserts scientific octave number to the notes on a the given scale.
        """

        next_octave = 1 if not descending else -1

        scale_with_octave = []
        changing_note = None

        current_octave = starting_octave

        if not descending:
            for closest in ['C', 'C#', 'Db']:
                if closest in scale:
                    changing_note = closest
                    break
        else:
            for closest in ['B', 'Bb', 'A#']:
                if closest in scale:
                    changing_note = closest
                    break

        for idx, note in enumerate(scale):
            if idx > 0 and note == changing_note:
                current_octave += next_octave

            scale_with_octave.append("{}{}".format(note, current_octave))

        return scale_with_octave

    def _get_chromatic_idx(self, note):
        """Gets the chromatic index, ie., the distance in semitones of a given
        note from C.
        """

        global notes2, notes3

        #use_flat = -1 if (note == 'F' or 'b' in note) else 0

        # FIXME
        if note in notes2:
            note_index = notes2.index(note)
        elif note in notes3:
            note_index = notes3.index(note)
        else:
            note_index = False

        return note_index


class Interval:

    def __init__(self, mode, tonic, octave, chromatic=None, n_octaves=None,
                 descending=None):
        """Chooses a chromatic interval for the question.

        Parameters
        ----------
        mode : str
        tonic : str
        octave : str
        interval : str
        chromatic: bool
        n_octaves : int
        descending : bool
        """

        global DIATONIC_MODES, CHROMATIC_TYPE, MAX_SEMITONES_RESOLVE_BELOW
        global INTERVALS

        diatonic_mode = list(DIATONIC_MODES[mode])
        chromatic_network = list(CHROMATIC_TYPE)

        if descending:
            diatonic_mode = [12 - x for x in diatonic_mode]
            print(diatonic_mode)
            diatonic_mode.reverse()
            print(diatonic_mode)

            #chromatic_

        step_network = diatonic_mode

        # FIXME: please refactore this with method signature n_octaves=1:
        if n_octaves:
            for i in range(1, n_octaves):
                step_network.extend([semitones + 12 * i for semitones in
                                     diatonic_mode[1:]])
                chromatic_network.extend([semitones + 12 * i for semitones in
                                          CHROMATIC_TYPE[1:]])
        #else:
        #    n_octaves = 1

        if not chromatic:
            semitones = choice(step_network)
        else:
            semitones = choice(chromatic_network)

        chromatic_scale = Scale(tonic=tonic, octave=None, chromatic=True,
                                n_octaves=n_octaves, descending=descending)

        chromatic_scale_pitch = Scale(tonic=tonic, octave=octave,
                                      chromatic=True, n_octaves=n_octaves,
                                      descending=descending)


        distance = dict({
            'octaves': 0 if (semitones < 12) else int(semitones / 12),
            'semitones': semitones if (semitones < 12) else int(semitones % 12)
        })
        # chromatic_offset = semitones if semitones < 12 else semitones % 12
        chromatic_offset = distance['semitones']

        note_name = "{}".format(chromatic_scale.scale[semitones])
        note_and_octave = "{}".format(chromatic_scale_pitch.scale[semitones])


        is_chromatic = True if chromatic_offset not in diatonic_mode else False

        if is_chromatic:
            # here we are rounding it to the next diatonic degree, to insert
            # it after:
            if chromatic_offset <= MAX_SEMITONES_RESOLVE_BELOW:
                diatonic_index = diatonic_mode.index(chromatic_offset - 1)
            else:
                diatonic_index = diatonic_mode.index(chromatic_offset + 1)
        else:
            diatonic_index = diatonic_mode.index(chromatic_offset)

        if not descending:
            interval_octave = int(octave) + distance['octaves']
        else:
            interval_octave = int(octave) - distance['octaves']

        self.interval_data = dict({
            'tonic_octave': octave,
            'interval_octave': interval_octave,
            'chromatic_offset': chromatic_offset,
            'note_and_octave': note_and_octave,
            'note_name': note_name,
            'semitones': semitones,
            'is_chromatic': is_chromatic,
            'is_descending': False if not descending else True,
            'diatonic_index': diatonic_index,
            'distance': distance,
            'data': INTERVALS[semitones],
        })


class Cadence:
    def __init__(self):
        pass


class QuestionBase:
    """
    Base Class to be subclassed for Question classes.

    This class implements attributes and routines to be used in Question
    subclasses.
    """

    def __init__(self, mode='major', tonic=None, octave=None, descending=None,
                 chromatic=None, n_octaves=None, *args, **kwargs):

        global KEYBOARD_INDICES, KEYS

        self.question_duration = 2
        self.question_delay = 1.5
        self.question_pos_delay = 0

        self.resolution_duration = 2.5
        self.resolution_delay = 0.5
        self.resolution_pos_delay = 1

        self.mode = mode

        # self.octave = octave if octave else randrange(3, 5)
        self.octave = octave or randrange(3, 5)

        # FIXME: maybe this should go to __main__
        self.keyboard_index = KEYBOARD_INDICES['chromatic'][self.mode]

        #if descending:
        #    self.keyboard_index = self.keyboard_index[::-1].swapcase()

        # FIXME
        # self.tonic = tonic if tonic else choice(KEYS)
        self.tonic = tonic or choice(KEYS)
        tonic = self.tonic

        diatonic_scale = Scale(tonic=tonic, mode=mode, octave=None,
                         descending=descending, n_octaves=n_octaves)
        chromatic_scale = Scale(tonic=tonic, octave=None, chromatic=True,
                          descending=descending, n_octaves=n_octaves)

        diatonic_scale_pitch = Scale(tonic=tonic, mode=mode, octave=self.octave,
                               descending=descending, n_octaves=n_octaves)
        chromatic_scale_pitch = Scale(tonic=tonic, octave=self.octave,
                                chromatic=True, descending=descending,
                                n_octaves=n_octaves)

        scales = dict({
            'diatonic': diatonic_scale,
            'chromatic': chromatic_scale,
            'diatonic_pitch': diatonic_scale_pitch,
            'chromatic_pitch': chromatic_scale_pitch,
        })
        self.scales = scales

        self.concrete_tonic = scales['diatonic_pitch'].scale[0]
        self.scale_size = len(scales['diatonic'].scale)


    def _wait(self, seconds):
        time.sleep(seconds)

    def _play_note(self, note, duration, delay):
        # requires sox to be installed

        command = (
            "play -qn synth {duration} pluck {note}"
            " fade l 0 {duration} 2 reverb"
        ).format(note=note, duration=duration)

        subprocess.Popen(command.split())

        if delay:
            self._wait(delay)

    def _play_chord(self, chord, duration, delay):

        for note in chord:
            self._play_note(note, duration=duration, delay=0)

        if delay:
            self._wait(delay)

    def play_question(self):

        tonic = self.concrete_tonic
        interval = self.interval['note_and_octave']

        play_note = self._play_note

        play_note(note=tonic, duration=self.question_duration,
                  delay=self.question_delay)
        play_note(note=interval, duration=self.question_duration, delay=0)

        if self.question_pos_delay:
            self._wait(self.resolution_pos_delay)

    def play_resolution(self):

        play_note = self._play_note

        for tone in self.resolution_pitch:
            play_note(note=tone, duration=self.resolution_duration,
                      delay=self.resolution_delay)

        if self.resolution_pos_delay:
            self._wait(self.resolution_pos_delay)

    def check_question(self, user_input_char):
        """Checks whether the given answer is correct."""

        global INTERVALS

        semitones = self.keyboard_index.index(user_input_char)

        user_interval = INTERVALS[semitones][2]
        correct_interval = INTERVALS[self.interval['semitones']][2]

        response = {
            'is_correct': False,
            'user_interval': user_interval,
            'correct_interval': correct_interval,
        }

        if semitones == self.interval['semitones']:
            response.update({'is_correct': True})

        else:
            response.update({'is_correct': False})

        return response

    def make_resolution(self, chromatic, mode, tonic, interval,
                        descending=None):

        global DIATONIC_MODES, MAX_SEMITONES_RESOLVE_BELOW

        resolution_pitch = []

        #diatonic_mode = DIATONIC_MODES[mode]

        scale_pitch = Scale(tonic=tonic, mode=mode,
                            octave=interval['interval_octave'],
                            descending=descending)
        self.res_scale = scale_pitch

        print(scale_pitch.scale)
        print(interval)

        if not chromatic:

            if interval['chromatic_offset'] <= MAX_SEMITONES_RESOLVE_BELOW:
                resolution_pitch = \
                    scale_pitch.scale[:interval['diatonic_index'] + 1]
                resolution_pitch.reverse()
            else:
                resolution_pitch = \
                    scale_pitch.scale[interval['diatonic_index']:]

        else:

            if interval['chromatic_offset'] <= MAX_SEMITONES_RESOLVE_BELOW:
                if interval['is_chromatic']:
                    resolution_pitch.extend(
                        scale_pitch.scale[: interval['diatonic_index'] + 1])
                    resolution_pitch.append(interval['note_and_octave'])
                else:
                    resolution_pitch.extend(
                        scale_pitch.scale[: interval['diatonic_index'] + 1])
                resolution_pitch.reverse()

            else:
                if interval['is_chromatic']:
                    resolution_pitch.append(interval['note_and_octave'])

                resolution_pitch.extend(
                    scale_pitch.scale[interval['diatonic_index']:])

        # unisson and octave
        if interval['semitones'] == 0:
            resolution_pitch.append(scale_pitch.scale[0])
        elif interval['semitones'] % 12 == 0:
            # FIXME: multipe octaves
            resolution_pitch.append("{}{}".format(tonic, interval['tonic_octave']))

        return resolution_pitch


class MelodicIntervalQuestion(QuestionBase):
    "Implements a Melodic Interval test."

    def __init__(self, mode='major', tonic=None, octave=None, descending=None,
                 chromatic=None, n_octaves=None, *args, **kwargs):

        super(MelodicIntervalQuestion, self).\
                __init__(mode=mode, tonic=tonic, octave=octave,
                         descending=descending, chromatic=chromatic,
                         n_octaves=n_octaves, *args, **kwargs)

        self.interval = Interval(mode=mode, tonic=self.tonic, octave=self.octave,
                                 chromatic=chromatic, n_octaves=n_octaves,
                                 descending=descending).interval_data
        # FIXME
        self.resolution_pitch = \
            self.make_resolution(chromatic=chromatic, mode=self.mode,
                                 tonic=self.tonic, interval=self.interval,
                                 descending=descending)

class HarmonicIntervalQuestion(QuestionBase):
    "Implements a Harmonic Interval test."

    def __init__(self, mode='major', tonic=None, octave=None, descending=None,
                 chromatic=None, n_octaves=None, *args, **kwargs):

        super(HarmonicIntervalQuestion, self).\
                __init__(mode=mode, tonic=tonic, octave=octave,
                         descending=descending, chromatic=chromatic,
                         n_octaves=n_octaves, *args, **kwargs)

        tonic = self.tonic
        self.interval = Interval(mode=mode, tonic=self.tonic, octave=self.octave,
                                 chromatic=chromatic, n_octaves=n_octaves,
                                 descending=descending).interval_data
        # FIXME
        self.resolution_pitch = \
            self.make_resolution(chromatic=chromatic, mode=self.mode,
                                 tonic=self.tonic, interval=self.interval,
                                 descending=descending)

    def play_question(self):

        tonic = self.concrete_tonic
        interval = self.interval['note_and_octave']

        question_chords = [(tonic, tonic), (tonic, interval)]

        for item in question_chords:
            self._play_chord(chord=item, duration=self.question_duration,
                             delay=self.question_delay)

        if self.question_pos_delay:
            self._wait(self.resolution_pos_delay)

    def play_resolution(self):

        tonic = self.concrete_tonic

        for tone in self.resolution_pitch:
            self._play_chord(chord=[tonic, tone],
                             duration=self.resolution_duration,
                             delay=self.resolution_delay)

        if self.resolution_pos_delay:
            self._wait(self.resolution_pos_delay)


class MelodicDictateQuestion(QuestionBase):
    """Implements a melodic dictate test.
    """

    def __init__(self, mode='major', max_intervals=3, n_notes=4, tonic=None,
                 octave=None, descending=None, chromatic=None, n_octaves=None,
                 *args, **kwargs):

        super(MelodicDictateQuestion, self).\
                __init__(mode=mode, tonic=tonic, octave=octave,
                         descending=descending, chromatic=chromatic,
                         n_octaves=n_octaves, *args, **kwargs)

        question_intervals = [Interval(mode=mode, tonic=self.tonic,
                              octave=self.octave, chromatic=chromatic,
                              n_octaves=n_octaves,
                              descending=descending).interval_data for n in range(max_intervals)]
        self.question_phrase_intervals = [choice(question_intervals) for n in range(n_notes-1)]

        self.question_phrase= list([0])

        self.question_phrase.extend([ ival['semitones'] for ival in self.question_phrase_intervals ])

    def play_question(self, melodic_phrase=None):

        tonic = self.concrete_tonic

        for item in self.question_phrase:
            self._play_note(note=self.scales['chromatic_pitch'].scale[item], duration=self.question_duration,
                             delay=self.question_delay)

        if self.question_pos_delay:
            self._wait(self.resolution_pos_delay)

    def play_resolution(self):

        tonic = self.concrete_tonic

        for tone in [self.scales['chromatic_pitch'].scale[note] for note in self.question_phrase]:
            self._play_note(tone,
                             duration=self.resolution_duration,
                             delay=self.resolution_delay)

        if self.resolution_pos_delay:
            self._wait(self.resolution_pos_delay)

    def check_question(self, user_input_keys):
        """Checks whether the given answer is correct."""

        global INTERVALS

        response = {
            'is_correct': False,
            'user_input': user_input_keys,
            #'correct_interval': correct_interval,
        }

        if [self.keyboard_index.index(s) for s in user_input_keys] == self.question_phrase:
            response.update({'is_correct': True})
        else:
            response.update({'is_correct': False})

        return response

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


# def print_stuff(question):
#     padd = "─" * 30  # vim: insert mode, ^vu2500
#     print("""
# {}
#
# Tonic: {} | Note(Int): {} |  Interval: {} | Semitones(Int): {} |
# Is Note Chromatic: {} |
# Scale: {}, Octave: {}
# Resolution: {},
# Chromatic: {}
# Concrete Scale: {} | Chroma Concrete: {}
# {}
# """.format(
#         padd,
#         question.concrete_tonic,
#         question.interval['note_and_octave'],
#         "─".join(INTERVALS[question.interval['semitones']][1:]),
#         question.interval['semitones'],
#         question.interval['is_chromatic'],
#         "─".join(question.scales['diatonic'].scale),
#         "{}-{}".format(question.octave, question.octave + 1),
#         "─".join(question.resolution_pitch),
#         "─".join(question.scales['chromatic'].scale),
#         "─".join(question.scales['diatonic_pitch'].scale),
#         "─".join(question.scales['chromatic_pitch'].scale),
#         padd,
#     ))

def print_stuff(question):
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
        "─".join(str(question.question_phrase)),
        "─".join([ "/".join(INTERVALS[n][1:]) for n in question.question_phrase]),
        "─".join([str(n) for n in question.question_phrase]),
        #question.interval['is_chromatic'],
        "─".join(question.scales['diatonic'].scale),
        "{}-{}".format(question.octave, question.octave + 1),
        #"─".join(question.resolution_pitch),
        "─".join(question.scales['chromatic'].scale),
        "─".join(question.scales['diatonic_pitch'].scale),
        "─".join(question.scales['chromatic_pitch'].scale),
        padd,
    ))
dictate_notes = 4

def main():
    getch = _Getch()

    new_question_bit = True

    while True:
        if new_question_bit is True:

            new_question_bit = False

            input_keys = []
            #question = MelodicDictateQuestion(mode='major',descending=True)
            question = MelodicDictateQuestion(mode='major')
            #question = HarmonicIntervalQuestion(mode='major')
            #question = HarmonicIntervalQuestion(mode='major')

            # debug
            if DEBUG:
                print_stuff(question)

            question.play_question()

        user_input = getch()

        # any response input interval from valid keys
        if user_input in question.keyboard_index and user_input != ' ':  # spc

            input_keys.append(user_input)
            print(user_input,)

            if len(input_keys) == dictate_notes:
                #response = question.check_question(user_input)
                response = question.check_question(input_keys)

                if response['is_correct']:
                    #print("Correct!.. it is “{}”".format( response['user_interval']))
                    print("Correct! It was semitones {}".format("-".join(str(question.question_phrase))))
                else:
                    print("It is incorrect...")
                    print("You replied semitones {} but the correct is semitones {}".format("-".join(str(input_keys)), "-".join(str(question.question_phrase))))
                #else:
                #    print("Incorrect.. the correct is “{}” ! You aswered “{}”..".
                #          format(response['correct_interval'],
                #                 response['user_interval']))

                question.play_resolution()

                new_question_bit = True
            #else:
            #    input_keys.append(user_input)
            #    print(user_input,)

        # q - quit
        elif user_input == 'q':
            exit(0)

        # r - repeat interval
        elif user_input == 'r':
            question.play_question()

if __name__ == "__main__":
    main()
