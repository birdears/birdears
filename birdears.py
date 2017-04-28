#!/usr/bin/env python3

import subprocess
import time
from random import randrange, choice

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

    notes2 = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
    notes3 = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']
    notes4 = ['C', 'C#', 'Db', 'D', 'D#', 'Eb', 'E', 'F',
             'F#', 'Gb', 'G', 'G#', 'Ab', 'A', 'A#', 'Bb', 'B']

             # from birdears import *
             # import iterools as it
             # a = QuestionBase()
             #for i in it.cycle(a.notes):
             #  print(i)
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

    #diatonic_indices = {
    #    'major': [0, 2, 4, 5, 7, 9, 11, -12],
    #    'minor': [0, 2, 3, 5, 7, 8, 10, -12],
    #}

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

        for tone in self.resolution_concrete:
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
            return response

        else:
            response.update({'is_correct': False})
            return response

    def make_diatonic_interval(self,  chromatic_concrete):
        """Chooses a diatonic interval for the question."""

        interval = dict()

        diatonic_mode = self.diatonic_modes[self.mode]

        semitones = choice(diatonic_mode)

        interval_index = diatonic_mode.index(semitones)
        degree = interval_index + 1 # I II III IV VI VII VIII
        #index = randrange(self.scale_size) - 1

        note_and_octave = self.concrete_scale[interval_index]
        note_name = self.scale[interval_index]

        #semitones = diatonic_mode[index]

        #is_chromatic = True if not note_octave in [chromatic_concrete[intv] for intv in diatonic_index] else False
        #FIXME: this is redundant now:
        is_chromatic = True if not note_and_octave in self.concrete_scale else False

        # FIXME: fix this.
        interval_diatonic_index = diatonic_mode.index(semitones)

        interval.update({
            'index': interval_index,
            'note_and_octave': note_and_octave,
            'note_name': note_name,
            'semitones': semitones,
            'is_chromatic': is_chromatic,
            'diatonic_index': interval_index,
        })

        self.interval = interval

        return interval

    def make_chromatic_interval(self,  chromatic_concrete):
        """Chooses a chromatic interval for the question."""

        interval = dict()

        #diatonic_index = self.diatonic_modes[self.mode]
        diatonic_mode = self.diatonic_modes[self.mode]

        #index = randrange(len(self.tone_chroma))
        semitones = choice(self.chromatic_type)
        interval_index = semitones

        # FIXME : these should be passed to function instead
        note_and_octave = self.chroma_concrete[interval_index]
        note_name = self.tone_chroma[interval_index]

        #semitones = chromatic_concrete.index(note_octave)
        #s = semitones

        is_chromatic = True if not note_and_octave in [
            chromatic_concrete[intv] for intv in diatonic_mode] else False

        if is_chromatic:  # TODO: check if augmented forth is really correct in question resolution
            if semitones <= self.max_semitones_resolve_below:
                interval_diatonic_index = diatonic_mode.index(semitones - 1)
            else:
                interval_diatonic_index = diatonic_mode.index(semitones + 1)
        else:
            interval_diatonic_index = diatonic_mode.index(semitones)

        interval.update({
            'index': interval_index,
            'note_and_octave': note_and_octave,
            'note_name': note_name,
            'semitones': semitones,
            'is_chromatic': is_chromatic,
            'diatonic_index': interval_diatonic_index,
        })

        self.interval = interval

        return interval

    def make_resolution(self, scale_type, interval=None):

        resolution_concrete = []
        interval = self.interval
        concrete_scale = self.concrete_scale
        # FIXME: we have this in octave; Resolution: Db3─Db3,

        if scale_type is 'diatonic':
            # if self.ival_semitones <= 6:
            if interval['semitones'] <= self.max_semitones_resolve_below:
                # hotfix
                resolution_concrete = concrete_scale[:interval['index'] + 1]
                resolution_concrete.reverse()
            else:
                resolution_concrete = concrete_scale[interval['index']:]

        elif scale_type is 'chromatic':

            if interval['semitones'] <= self.max_semitones_resolve_below:
                if interval['is_chromatic']:
                    # hotfix #2 FIXME
                    resolution_concrete = concrete_scale[:
                                                         interval['diatonic_index'] + 1]
                    resolution_concrete.append(
                        self.chroma_concrete[interval['index']])
                else:
                    # hotfix FIXME
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

    def append_octave_to_scale(self, scale, starting_octave, descending=None):
        """Inserts scientific octave number to the notes on a the given scale.
        """

        next_octave = 1 if not descending else -1

        scale_with_octave = []
        changing_note = None

        cur_octave = starting_octave

        if not descending:
            for closest in ['C','C#','Db']:
                if closest in scale:
                    changing_note = closest
                    break
        else:
            for closest in ['B','Bb','A#']:
                if closest in scale:
                    changing_note = closest
                    break

        for idx, note in enumerate(scale):
            if idx > 0 and note == changing_note:
                cur_octave += next_octave

            scale_with_octave.append("{}{}".format(note, cur_octave))

        return scale_with_octave


    def get_chromatic_scale(self, tonic, octave=None, descending=None):
        """Returns a chromatic scale from tonic"""

        notes = self.notes

        # lets use last item of tuples, if FMaj or flat keys
        use_flat = -1 if (tonic == 'F' or 'b' in tonic) else 0

        tonic_index = [note[use_flat] for note in notes].index(tonic)
        #last_note_index = tonic_index + 12 # FIXME
        last_note_index = tonic_index + 13 # FIXME

        chromatic = [(notes * 2)[y][use_flat]
                     for y in range(tonic_index, last_note_index)]
                            # FIXME: REMEBER TO CHECK range()

        if descending:
            chromatic.reverse()

        if octave:
            chromatic = self.append_octave_to_scale(chromatic, octave, descending)

        return chromatic

    def get_diatonic_scale(self, tonic, mode, octave=None, descending=None, repeat_tonic=True):
        """Returns a diatonic scale from tonic and mode"""

        diatonic_index = self.diatonic_modes[mode]

        chroma = self.get_chromatic_scale(tonic)
        diatonic = [chroma[step] for step in diatonic_index]

        if descending:
            diatonic.reverse()

        if octave:
            diatonic = self.append_octave_to_scale(diatonic, octave, descending)

        return diatonic

class Question(QuestionBase):

    def __init__(self, mode='major', scale_type='diatonic', octave=[2, 6], *args, **kwargs):

        super(Question, self).__init__(*args, **kwargs)  # runs base class init

        self.mode = mode
        self.scale_type = scale_type

        if type(octave) == int:
            self.octave = octave
        elif type(octave) == list and len(octave) == 2:
            self.octave = randrange(octave[0], octave[1])

        self.keyboard_index = self.keyboard_indices[self.scale_type][self.mode]

        #sort_tonic = self.notes[randrange(len(self.notes))]
        #if not tonic:
        tonic = choice(self.notes4)

        #if type(sort_tonic) == tuple:
        #    self.tonic = tonic = sort_tonic[randrange(2)]
        #else:
        #    self.tonic = tonic = sort_tonic

        if scale_type == 'diatonic':
            self.scale = self.get_diatonic_scale(
                tonic=tonic, mode=mode, octave=None, descending=None)
        elif scale_type == 'chromatic':
            self.scale = self.get_chromatic_scale(
                tonic=tonic, octave=None, descending=None)

        self.tone_chroma = self.get_chromatic_scale(
            tonic=tonic, octave=None, descending=None)

        self.scale_size = len(self.scale)

        self.concrete_scale = self.get_diatonic_scale(
            tonic=tonic, mode=mode, octave=self.octave, descending=None)
        self.chroma_concrete = self.get_chromatic_scale(
            tonic=tonic, octave=self.octave, descending=None)
        self.concrete_tonic = self.concrete_scale[0]

        if scale_type == 'chromatic':
            self.make_chromatic_interval(
                chromatic_concrete=self.chroma_concrete)
        elif scale_type == 'diatonic':
            self.make_diatonic_interval(
                chromatic_concrete=self.chroma_concrete)

        self.make_resolution(scale_type=scale_type)

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
            question = Question(mode='major', scale_type='chromatic')
            #question = Question(mode='major', scale_type='diatonic')

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
