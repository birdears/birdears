from ..questionbase import QuestionBase

# from ..interval import Interval
from ..interval import DiatonicInterval, ChromaticInterval

from .. import DIATONIC_MODES
from .. import MAX_SEMITONES_RESOLVE_BELOW
from .. import INTERVALS

from ..scale import DiatonicScale
from ..scale import ChromaticScale

from ..sequence import Sequence


class HarmonicIntervalQuestion(QuestionBase):
    """Implements a Harmonic Interval test.
    """

    def __init__(self, mode='major', tonic=None, octave=None, descending=None,
                 chromatic=None, n_octaves=None, *args, **kwargs):

        super(HarmonicIntervalQuestion, self).\
                __init__(mode=mode, tonic=tonic, octave=octave,
                         descending=descending, chromatic=chromatic,
                         n_octaves=n_octaves, *args, **kwargs)

        tonic = self.tonic

        if not chromatic:
            self.interval = DiatonicInterval(mode=mode, tonic=self.tonic,
                                             octave=self.octave,
                                             n_octaves=n_octaves,
                                             descending=descending)\
                                                .interval_data
        else:
            self.interval = ChromaticInterval(mode=mode, tonic=self.tonic,
                                              octave=self.octave,
                                              n_octaves=n_octaves,
                                              descending=descending)\
                                                .interval_data

        self.question = self.make_question()

        # FIXME
        self.resolution = \
            self.make_resolution(chromatic=chromatic, mode=self.mode,
                                 tonic=self.tonic, interval=self.interval,
                                 descending=descending)

    def make_question(self):

        tonic = self.concrete_tonic
        interval = self.interval['note_and_octave']

        question = Sequence([[tonic, interval]], self.question_duration,
                            self.question_delay, self.question_pos_delay)

        return question

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

        if interval['chromatic_offset'] <= MAX_SEMITONES_RESOLVE_BELOW:
            begin_to_diatonic = slice(None, interval['diatonic_index'] + 1)
            resolution_pitch = scale_pitch.scale[begin_to_diatonic]
            if interval['is_chromatic']:
                resolution_pitch.append(interval['note_and_octave'])
            resolution_pitch.reverse()
        else:
            diatonic_to_end = slice(interval['diatonic_index'], None)
            if interval['is_chromatic']:
                resolution_pitch.append(interval['note_and_octave'])
            resolution_pitch.extend(scale_pitch.scale[diatonic_to_end])

        # unisson and octave
        if interval['semitones'] == 0:
            resolution_pitch.append(scale_pitch.scale[0])

        elif interval['semitones'] % 12 == 0:
            # FIXME: multipe octaves
            resolution_pitch.append("{}{}".format(tonic,
                                                  interval['tonic_octave']))

        resolution = Sequence([[tonic, item] for item in resolution_pitch],
                              duration=self.resolution_duration,
                              delay=self.resolution_delay,
                              pos_delay=self.resolution_pos_delay)

        return resolution
