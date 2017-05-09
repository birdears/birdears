import subprocess
import time

from random import randrange
from random import choice

from . import KEYBOARD_INDICES
from . import KEYS
from . import MAX_SEMITONES_RESOLVE_BELOW
from . import INTERVALS

from .scale import DiatonicScale
from .scale import ChromaticScale

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

        # if descending:
        #    self.keyboard_index = self.keyboard_index[::-1].swapcase()

        # FIXME
        # self.tonic = tonic if tonic else choice(KEYS)
        self.tonic = tonic or choice(KEYS)
        tonic = self.tonic

        diatonic_scale = DiatonicScale(tonic=tonic, mode=mode, octave=None,
                                       descending=descending,
                                       n_octaves=n_octaves)

        chromatic_scale = ChromaticScale(tonic=tonic, octave=None,
                                         descending=descending,
                                         n_octaves=n_octaves)

        diatonic_scale_pitch = DiatonicScale(tonic=tonic, mode=mode,
                                     octave=self.octave, descending=descending,
                                     n_octaves=n_octaves)

        chromatic_scale_pitch = ChromaticScale(tonic=tonic, octave=self.octave,
                                      descending=descending,
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

        # diatonic_mode = DIATONIC_MODES[mode]

        scale_pitch = DiatonicScale(tonic=tonic, mode=mode,
                            octave=interval['interval_octave'],
                            descending=descending)
        self.res_scale = scale_pitch

        if not chromatic:

            if interval['chromatic_offset'] <= MAX_SEMITONES_RESOLVE_BELOW:
                resolution_pitch =\
                    scale_pitch.scale[:interval['diatonic_index'] + 1]
                resolution_pitch.reverse()
            else:
                resolution_pitch =\
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
            resolution_pitch.append("{}{}".format(tonic,
                                                  interval['tonic_octave']))

        return resolution_pitch
