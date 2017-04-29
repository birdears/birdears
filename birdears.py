#!/usr/bin/env python3

import subprocess
import time
from random import randrange, choice
from collections import deque

#from pprint import pprint

DEBUG = True

class QuestionBase:
    """
    Base Class to be subclassed for Question classes.

    This class implements attributes and routines to be used in Question
    subclasses.

    Attributes
    ----------

    notes : list
            list of notes and enharmonics to be used by the class

    """

    # maybe we'd better use circle of fifths here
    notes = ['C', ('C#', 'Db'), 'D', ('D#', 'Eb'), 'E', 'F',
             ('F#', 'Gb'), 'G', ('G#', 'Ab'), 'A', ('A#', 'Bb'), 'B']

    notes2 = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    notes3 = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

    notes4 = ['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F',
              'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B']

    # from birdears import *
    # import iterools as it
    # a = QuestionBase()
    # for i in it.cycle(a.notes):
    #  print(i)
    intervals = [
        (0, 'P1', 'Perfect Unison'), # tonic
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
        (12, 'P8', 'Perfect Octave'), # 1st octave
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
        (24, 'P15', 'Perfect Double-octave'), #2nd octave
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
        (36, 'P22', 'Perfect Triple-octave'),   # 3rd octave; the
        (37, 'A22', 'Minor 23'), # pattern ends here-lets compute hence forth
        (38, 'M23', 'Major 23'),
        (39, 'm24', 'Minor 24'),
        (40, 'M24', 'Major 24'),
        (41, 'P25', 'Perfect 25'),
        (42, 'A25', 'Augmented 25'),
        (43, 'P26', 'Perfect 26'),
        (44, 'm27', 'Minor 27'),
        (45, 'M27', 'Major 27'),
        (46, 'm28', 'Minor 28'),
        (47, 'M28', 'Major 28'),
        (48, 'P29', 'Perfect 29'),  # 4th octave
        (49, 'A29', 'Minor 30'),
        (50, 'M30', 'Major 30'),
        (51, 'm31', 'Minor 31'),
        (52, 'M31', 'Major 31'),
        (53, 'P32', 'Perfect 32'),
        (54, 'A32', 'Augmented 32'),
        (55, 'P33', 'Perfect 33'),
        (56, 'm34', 'Minor 34'),
        (57, 'M34', 'Major 34'),
        (58, 'm35', 'Minor 35'),
        (59, 'M35', 'Major 35'),
        (60, 'P36', 'Perfect 36')
    ]

    chromatic_type = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    diatonic_modes = {
        'major': [0, 2, 4, 5, 7, 9, 11, 12],
        'minor': [0, 2, 3, 5, 7, 8, 10, 12],
    }

    keyboard_indices = {
        'diatonic': {
            'minor': 'z xc v bn m Z XC V BN M',
            'major': 'z x cv b n mZ X CV B NM'
        },
        'chromatic': {
            'minor': "zsxcfvgbnjmkZSXCFVGBNJMK",
            'major': "zsxdcvgbhnjmZSXDCVGBHNJM",
        }
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

    # how many steps to resolve on tonic,
    # after which resolves on tonic octave
    # (begins on 0 as it is an index)
    # 5 is tritone; then
    # [0 1 2 3 4 5] resolves below (tonic)
    # and [6 7 8 9 10 11] resolves above (octave)
    max_semitones_resolve_below = 5

    def __init__(self, *args, **kwargs):

        self.question_duration = 2
        self.question_delay = 1.5
        self.question_pos_delay = 0

        self.resolution_duration = 2.5
        self.resolution_delay = 0.5
        self.resolution_pos_delay = 1

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

        semitones = self.keyboard_index.index(user_input_char)

        user_interval = self.intervals[semitones][2]
        correct_interval = self.intervals[self.interval['semitones']][2]

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

    def make_diatonic_interval(self, mode, scale, scale_pitch, chromatic, chromatic_pitch, octave, n_octaves=None):
        """Chooses a diatonic interval for the question."""

        interval = dict()

        diatonic_mode = list(self.diatonic_modes[mode])

        step_network = diatonic_mode

        if n_octaves:
            for i in range(1, n_octaves):
                step_network.extend([semitones + 12 * i for semitones in diatonic_mode[1:]])
        else: n_octaves =1

        semitones = choice(step_network)
        interval_index = step_network.index(semitones)

        note_and_octave = chromatic_pitch[semitones]
        note_name = chromatic[semitones]

        #interval.update({
        #    'index': interval_index,
        #    'tonic_octave': octave,
        #    'note_and_octave': note_and_octave,
        #    'note_name': note_name,
        #    'semitones': semitones,
        #    'is_chromatic': False,
        #    'diatonic_index': interval_index,
        #})
        chromatic_offset = semitones if semitones < 12 else semitones % 12

        interval_octave = octave + int(semitones / 12)
        interval.update({
            'index': interval_index,
            'tonic_octave': octave,
            'interval_octave': interval_octave,
            'note_and_octave': note_and_octave,
            'chromatic_offset':chromatic_offset,
            'note_name': note_name,
            'semitones': semitones,
            'is_chromatic': False,
            'diatonic_index': interval_index,
        })
        return interval

    def make_chromatic_interval(self, mode, chromatic, chromatic_pitch, octave, n_octaves=None):
        """Chooses a chromatic interval for the question."""

        interval = dict()

        diatonic_mode = list(self.diatonic_modes[mode])
        chromatic_type = list(self.chromatic_type)

        step_network = diatonic_mode
        chromatic_network = chromatic_type

        if n_octaves:
            for i in range(1, n_octaves):
                step_network.extend([semitones + 12 * i for semitones in diatonic_mode[1:]])
                chromatic_network.extend([semitones + 12 * i for semitones in chromatic_type[1:]])
        else: n_octaves = 1

        semitones = choice(chromatic_network)
        interval_index = chromatic_network.index(semitones)

        interval_index = semitones

        note_and_octave = chromatic_pitch[interval_index]
        note_name = chromatic[interval_index]

        is_chromatic = True if not semitones in diatonic_mode else False

        chromatic_offset = semitones if semitones < 12 else semitones % 12
        if is_chromatic:
            # here we are rounding it to the next ditonic degree:
            if chromatic_offset <= self.max_semitones_resolve_below:
                interval_diatonic_index = diatonic_mode.index(chromatic_offset - 1)
            else:
                interval_diatonic_index = diatonic_mode.index(chromatic_offset + 1)
        else:
            interval_diatonic_index = diatonic_mode.index(chromatic_offset)

        interval_octave = octave + int(semitones / 12)
        interval.update({
            'index': interval_index,
            'tonic_octave': octave,
            'interval_octave': interval_octave,
            'note_and_octave': note_and_octave,
            'chromatic_offset':chromatic_offset,
            'note_name': note_name,
            'semitones': semitones,
            'is_chromatic': is_chromatic,
            'diatonic_index': interval_diatonic_index,
        })

        return interval

    def make_resolution(self, scale_type, mode, tonic, interval, descending=None):

        resolution_pitch = []

        diatonic_mode = list(self.diatonic_modes[mode])

        scale_pitch = self.get_diatonic_scale(tonic,mode,interval['interval_octave'])
        self.res_scale = scale_pitch

        if scale_type is 'diatonic':

            local_idx = scale_pitch.index(interval['note_and_octave'])

            if interval['chromatic_offset'] <= self.max_semitones_resolve_below:
                resolution_pitch = scale_pitch[:local_idx + 1]
                resolution_pitch.reverse()
            else:
                resolution_pitch = scale_pitch[local_idx:]

        elif scale_type is 'chromatic':

            if interval['chromatic_offset'] <= self.max_semitones_resolve_below:
                if interval['is_chromatic']:
                    resolution_pitch.extend(scale_pitch[: interval['diatonic_index']+1])
                    resolution_pitch.append(interval['note_and_octave'])
                else:
                    resolution_pitch.extend(scale_pitch[: interval['diatonic_index']+1])
                resolution_pitch.reverse()

            else:
                if interval['is_chromatic']:
                    resolution_pitch.append(interval['note_and_octave'])

                resolution_pitch.extend(scale_pitch[interval['diatonic_index']:])

        # unisson and octave
        #if interval['semitones'] == 0:
        if interval['chromatic_offset'] == 0:
            resolution_pitch.append(scale_pitch[0])
            #maybe we should use original tonic here, then maybe reverse()
        elif interval['chromatic_offset'] % 12 == 0:
            resolution_pitch.append(scale_pitch[-1]) #FIXME: multipe octaves

        return resolution_pitch

    def append_octave_to_scale(self, scale, starting_octave, descending=None):
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
        use_flat = -1 if (note == 'F' or 'b' in note) else 0

        # FIXME
        if note in self.notes2:
            note_index = self.notes2.index(note)
        elif note in self.notes3:
            note_index = self.notes3.index(note)
        else:
            note_index = False

        return note_index

    def get_chromatic_scale(self, tonic, octave=None, n_octaves=None, descending=None, dont_repeat_tonic=None):
        """Returns a chromatic scale from tonic."""

        tonic_index = self._get_chromatic_idx(tonic)

        if tonic == 'F' or 'b' in tonic:
            notes = deque(self.notes3)
        else:
            notes = deque(self.notes2)

        notes.rotate(-(tonic_index))

        if n_octaves:
            chromatic = list(notes * n_octaves)
        else:
            chromatic = list(notes)

        if not dont_repeat_tonic:
            chromatic.append(chromatic[0])

        if descending:
            chromatic.reverse()

        if octave:
            chromatic = self.append_octave_to_scale(
                chromatic, octave, descending)

        return chromatic

    def get_diatonic_scale(self, tonic, mode, octave=None, n_octaves=None, descending=None, dont_repeat_tonic=None):
        """Returns a diatonic scale from tonic and mode"""

        diatonic_mode = list(self.diatonic_modes[mode])

        chromatic = self.get_chromatic_scale(tonic)

        diatonic = [chromatic[semitones] for semitones in diatonic_mode[:-1]]

        if n_octaves:
            diatonic = diatonic * n_octaves

        if not dont_repeat_tonic:
            diatonic.append(chromatic[diatonic_mode[-1]])

        if descending:
            diatonic.reverse()

        if octave:
            diatonic = self.append_octave_to_scale(
                diatonic, octave, descending)

        return diatonic


class Question(QuestionBase):

    def __init__(self, mode='major', scale_type='diatonic', octave=[2, 6], descending=None, n_octaves=None, *args, **kwargs):

        super(Question, self).__init__(*args, **kwargs)  # runs base class init

        self.mode = mode
        # FIXME: scale_type should be changed to something like interval_type
        self.scale_type = scale_type

        if type(octave) == int:
            self.octave = octave
        elif type(octave) == list and len(octave) == 2:
            self.octave = randrange(octave[0], octave[1])

        # FIXME: maybe this should go to __main__
        self.keyboard_index = self.keyboard_indices[self.scale_type][self.mode]

        tonic = choice(self.notes4)

        self.scale = self.get_diatonic_scale(tonic=tonic, mode=mode, octave=None, descending=descending, n_octaves=n_octaves)
        self.chromatic = self.get_chromatic_scale(tonic=tonic, octave=None, descending=descending, n_octaves=n_octaves)

        self.scale_pitch = self.get_diatonic_scale(tonic=tonic, mode=mode, octave=self.octave, descending=descending, n_octaves=n_octaves)
        self.chromatic_pitch = self.get_chromatic_scale(tonic=tonic, octave=self.octave, descending=descending, n_octaves=n_octaves)

        self.concrete_tonic = self.scale_pitch[0]
        self.scale_size = len(self.scale)

        if scale_type == 'chromatic':
            self.interval = self.make_chromatic_interval(self.mode, self.chromatic, self.chromatic_pitch, self.octave, n_octaves=n_octaves)
        #elif scale_type == 'diatonic':
        else:
            self.interval = self.make_diatonic_interval(self.mode, self.scale,
                                                        self.scale_pitch,
                                                        self.chromatic,
                                                        self.chromatic_pitch,
                                                        self.octave,
                                                        n_octaves=n_octaves)

        #FIXME
        self.resolution_pitch = self.make_resolution(self.scale_type, self.mode, self.scale[0], self.interval)

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
    padd = "─" * 30;  # vim: insert mode, ^vu2500
    print("""
{}

Tonic: {} | Note(Int): {} |  Interval: {} | Semitones(Int): {} |
Is Note Chromatic: {} |
Scale: {}, Octave: {}
Resolution: {},
Chromatic: {}
Concrete Scale: {} | Chroma Concrete: {}

""".format(
        padd,
        question.concrete_tonic,
        question.interval['note_and_octave'],
        "─".join(question.intervals[question.interval['semitones']][1:]),
        question.interval['semitones'],
        question.interval['is_chromatic'],
        "─".join(question.scale),
        "{}-{}".format(question.octave, question.octave + 1),
        "─".join(question.resolution_pitch),
        "─".join(question.chromatic),
        "─".join(question.scale_pitch),
        "─".join(question.chromatic_pitch)
    ))


if __name__ == "__main__":
    getch = _Getch()

    new_question_bit = True

    while True:
        if new_question_bit is True:

            new_question_bit = False
            #question = Question(mode='major', scale_type='chromatic', descending=True)
            #question = Question(mode='major', scale_type='diatonic', descending=True)
            #question = Question(mode='major', scale_type='diatonic', octave=[3,5], n_octaves=2)
            #question = Question(mode='major', scale_type='chromatic', octave=[3,5], n_octaves=2)
            question = Question(mode='major', scale_type='diatonic', octave=[3,5], n_octaves=2)

            # debug
            if DEBUG:
                print_stuff(question)

            question.play_question()

        user_input = getch()

        # any response input interval from valid keys
        if user_input in question.keyboard_index and user_input != ' ':  # space char

            response = question.check_question(user_input)

            if response['is_correct']:
                print("Correct!.. it is “{}”".format(
                    response['user_interval']))
            else:
                print("Incorrect.. the correct is “{}” ! You aswered “{}”..".format(
                    response['correct_interval'], response['user_interval']))

            question.play_resolution()

            new_question_bit = True

        # q - quit
        elif user_input == 'q':
            exit(0)

        # r - repeat interval
        elif user_input == 'r':
            question.play_question()
