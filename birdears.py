#!/usr/bin/env python3

import subprocess
import time
from random import randrange

#from pprint import pprint


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

    intervals = [
        [0, 'P1', 'Perfect Unison'],
        [1, 'm2', 'Minor Second'],
        [2, 'M2', 'Major Second'],
        [3, 'm3', 'Minor Third'],
        [4, 'M3', 'Major Third'],
        [5, 'P4', 'Perfect Fourth'],
        [6, 'A4', 'Augmented Fourth'],
        [7, 'P5', 'Perfect Fifth'],
        [8, 'm6', 'Minor Sixth'],
        [9, 'M6', 'Major Sixth'],
        [10, 'm7', 'Minor Seventh'],
        [11, 'M7', 'Major Seventh'],
        [12, 'P8', 'Perfect Octave']
    ]

    diatonic_indices = {
        'major': [0, 2, 4, 5, 7, 9, 11, -12],
        'minor': [0, 2, 3, 5, 7, 8, 10, -12],
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
    max_semitones_index_resolve_below_inclusive = 5

    def __init__(self):

        self.question_duration = 2
        self.question_delay = 1.5
        self.question_pos_delay = 0

        self.resolution_duration = 2.5
        self.resolution_delay = 0.5
        self.resolution_pos_delay = 1

    def wait(self, seconds):
        time.sleep(seconds)

    def play_note(self, note='C', duration=4, delay=0):
        # requires sox to be installed
        command = (
            "play -qn synth {duration} pluck {note}"
            " fade l 0 {duration} 2 reverb"
        ).format(note=note, duration=duration)

        subprocess.Popen(command.split())

        if delay:
            self.wait(delay)

    def play_question(self):

        tonic = self.concrete_tonic
        interval = self.interval['note_octave']

        play_note = self.play_note

        play_note(note=tonic, duration=self.question_duration,
                  delay=self.question_delay)
        play_note(note=interval, duration=self.question_duration, delay=0)

        if self.question_pos_delay:
            self.wait(self.resolution_pos_delay)

    def play_resolution(self):

        play_note = self.play_note

        for tone in self.resolution_concrete:
            play_note(note=tone, duration=self.resolution_duration,
                      delay=self.resolution_delay)

        if self.resolution_pos_delay:
            self.wait(self.resolution_pos_delay)

    def check_question(self, user_input_char):

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
            return response

        else:
            response.update({'is_correct': False})
            return response

    def make_diatonic_interval(self,  chromatic_concrete):
        """Chooses a diatonic interval for the question."""

        interval = dict()

        diatonic_index = self.diatonic_indices[self.kind]

        index = randrange(self.scale_size)

        note_octave = self.concrete_scale[index]
        note_name = self.scale[index]

        semitones = diatonic_index[index]

        #is_chromatic = True if not note_octave in [chromatic_concrete[intv] for intv in diatonic_index] else False
        is_chromatic = True if not note_octave in self.concrete_scale else False

        interval_diatonic_index = diatonic_index.index(semitones)

        interval.update({
            'index': index,
            'note_octave': note_octave,
            'note_name': note_name,
            'semitones': semitones,
            'is_chromatic': is_chromatic,
            'diatonic_index': interval_diatonic_index,
        })

        self.interval = interval

        return interval

    def make_chromatic_interval(self,  chromatic_concrete):
        """Chooses a chromatic interval for the question."""

        interval = dict()

        diatonic_index = self.diatonic_indices[self.kind]

        index = randrange(len(self.tone_chroma))

        note_octave = self.chroma_concrete[index]
        note_name = self.tone_chroma[index]

        semitones = chromatic_concrete.index(note_octave)

        s = semitones

        is_chromatic = True if not note_octave in [
            chromatic_concrete[intv] for intv in diatonic_index] else False

        if is_chromatic:  # TODO: check if augmented forth is really correct in question resolution
            if s <= 5:
                interval_diatonic_index = diatonic_index.index(s - 1)
            else:
                interval_diatonic_index = diatonic_index.index(s + 1)
        else:
            interval_diatonic_index = diatonic_index.index(s)

        interval.update({
            'index': index,
            'note_octave': note_octave,
            'note_name': note_name,
            'semitones': semitones,
            'is_chromatic': is_chromatic,
            'diatonic_index': interval_diatonic_index,
        })

        self.interval = interval

        return interval

    def make_resolution(self, mode,  interval=None):

        resolution_concrete = []
        interval = self.interval
        concrete_scale = self.concrete_scale

        if mode is 'diatonic':
            # if self.ival_semitones <= 6:
            if interval['semitones'] <= 5:
                # hotfix
                resolution_concrete = concrete_scale[:interval['index'] + 1]
                resolution_concrete.reverse()
            else:
                resolution_concrete = concrete_scale[interval['index']:]

        elif mode is 'chromatic':

            if interval['semitones'] <= 5:
                if interval['is_chromatic']:
                    # hotfix #2
                    resolution_concrete = concrete_scale[:
                                                         interval['diatonic_index'] + 1]
                    resolution_concrete.append(
                        self.chroma_concrete[interval['index']])
                else:
                    # hotfix
                    resolution_concrete = concrete_scale[:
                                                         interval['diatonic_index'] + 1]

                resolution_concrete.reverse()

            else:
                if interval['is_chromatic']:
                    resolution_concrete.append(
                        self.chroma_concrete[interval['index']])
                resolution_concrete.extend(
                    self.concrete_scale[interval['diatonic_index']:])

        if len(resolution_concrete) == 1:
            repeat_unison = resolution_concrete[0]
            resolution_concrete.append(repeat_unison)

        self.resolution_concrete = resolution_concrete
        return self.resolution_concrete

    def get_chromatic_scale(self, tonic='C', octave=None, descending=None):
        """Returns a chromatic scale from tonic"""

        notes = self.notes

        #use_flat = True if (tonic == 'F' or 'b' in tonic) else False
        use_flat = -1 if (tonic == 'F' or 'b' in tonic) else 0

        #tonic_index = [note[0] if not use_flat else note[-1] for note in notes].index(tonic)
        tonic_index = [note[use_flat] for note in notes].index(tonic)
        # last_note_index = tonic_index + 12 # FIXME!
        last_note_index = tonic_index + 12

        #chromatic = [note[0] if not use_flat else note[-1] for note in (notes*2)[tonic_index:last_note_index]]
        chromatic = [(notes * 2)[y][use_flat]
                     for y in range(tonic_index, last_note_index)]

        if octave:
            cur_octave = octave
            for idx, note in enumerate(chromatic):
                if idx > 0 and chromatic[idx] == 'C':
                    cur_octave += 1

                chromatic[idx] = "{}{}".format(note, cur_octave)

        if descending:
            chromatic.reverse()

        return chromatic

    def get_diatonic_scale(self, tonic='C', mode='major', octave=None, descending=None):
        """Returns a diatonic scale from tonic and mode"""

        diatonic_index = self.diatonic_indices[mode]

        chroma = self.get_chromatic_scale(tonic)
        diatonic = [chroma[step] for step in diatonic_index]

        if octave:
            cur_octave = octave
            for idx, note in enumerate(diatonic):
                if idx > 0 and 'C' in diatonic[idx]:
                    cur_octave += 1

                diatonic[idx] = "{}{}".format(note, cur_octave)

        if descending:
            diatonic.reverse()

        return diatonic


class Question(QuestionBase):

    def __init__(self, kind='major', mode='diatonic', octave=[2, 6]):

        super(Question, self).__init__()  # runs base class init

        self.kind = kind
        self.mode = mode

        if type(octave) == int:
            self.octave = octave
        elif type(octave) == list and len(octave) == 2:
            self.octave = randrange(octave[0], octave[1])

        self.keyboard_index = self.keyboard_indices[self.mode][self.kind]

        sort_tonic = self.notes[randrange(len(self.notes))]

        if type(sort_tonic) == tuple:
            self.tonic = tonic = sort_tonic[randrange(2)]
        else:
            self.tonic = tonic = sort_tonic

        if mode == 'diatonic':
            self.scale = self.get_diatonic_scale(
                tonic=tonic, mode=kind, octave=None, descending=None)
        elif mode == 'chromatic':
            self.scale = self.get_chromatic_scale(
                tonic=tonic, octave=None, descending=None)

        self.tone_chroma = self.get_chromatic_scale(
            tonic=tonic, octave=None, descending=None)

        self.scale_size = len(self.scale)

        self.concrete_scale = self.get_diatonic_scale(
            tonic=tonic, mode=kind, octave=self.octave, descending=None)
        self.chroma_concrete = self.get_chromatic_scale(
            tonic=tonic, octave=self.octave, descending=None)
        self.concrete_tonic = self.concrete_scale[0]

        if mode == 'chromatic':
            self.make_chromatic_interval(
                chromatic_concrete=self.chroma_concrete)
        elif mode == 'diatonic':
            self.make_diatonic_interval(
                chromatic_concrete=self.chroma_concrete)

        self.make_resolution(mode=mode)

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
        question.tonic,
        question.interval['note_name'],
        "─".join(question.intervals[question.interval['semitones']][1:]),
        question.interval['semitones'],
        question.interval['is_chromatic'],
        "─".join(question.scale),
        "{}-{}".format(question.octave, question.octave + 1),
        "─".join(question.resolution_concrete),
        "─".join(question.tone_chroma),
        "─".join(question.concrete_scale),
        "─".join(question.chroma_concrete)
    ))


if __name__ == "__main__":
    getch = _Getch()

    new_question_bit = True

    while True:
        if new_question_bit is True:

            new_question_bit = False
            #question = Question(kind='major', mode='chromatic')
            question = Question(kind='major', mode='diatonic')

            # debug
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
