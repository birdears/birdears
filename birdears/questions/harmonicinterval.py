from ..questionbase import QuestionBase

from ..interval import DiatonicInterval
from ..interval import ChromaticInterval

from .. import DIATONIC_MODES
from .. import MAX_SEMITONES_RESOLVE_BELOW
from .. import INTERVALS

from ..scale import DiatonicScale

from ..sequence import Sequence
from ..resolution import Resolution


class HarmonicIntervalQuestion(QuestionBase):
    """Implements a Harmonic Interval test.
    """

    def __init__(self, mode='major', tonic=None, octave=None, descending=None,
                 chromatic=None, n_octaves=None, *args, **kwargs):
        """Inits the class.

        Args:
            mode (str): A string representing the mode of the question.
                Eg., 'major' or 'minor'
            tonic (str): A string representing the tonic of the question,
                eg.: 'C'; if omitted, it will be selected randomly.
            octave (int): A scienfic octave notation, for example, 4 for 'C4';
                if not present, it will be randomly chosen.
            descending (bool): Is the question direction in descending, ie.,
                intervals have lower pitch than the tonic.
            chromatic (bool): If the question can have (True) or not (False)
                chromatic intervals, ie., intervals not in the diatonic scale
                of tonic/mode.
            n_octaves (int): Maximum number of octaves of the question.
        """

        super(HarmonicIntervalQuestion, self).__init__(mode=mode, tonic=tonic,
                                                       octave=octave,
                                                       descending=descending,
                                                       chromatic=chromatic,
                                                       n_octaves=n_octaves,
                                                       *args, **kwargs)

        self.question_duration = 3
        self.question_delay = 0.5
        self.question_pos_delay = 0

        self.resolution_duration = 2.5
        self.resolution_delay = 0.5
        self.resolution_pos_delay = 1

        tonic = self.tonic

        if not chromatic:
            self.interval = DiatonicInterval(mode=mode, tonic=self.tonic,
                                             octave=self.octave,
                                             n_octaves=n_octaves,
                                             descending=descending)

        else:
            self.interval = ChromaticInterval(mode=mode, tonic=self.tonic,
                                              octave=self.octave,
                                              n_octaves=n_octaves,
                                              descending=descending)

        self.question = self.make_question()

        resolve = Resolution(method='nearest_tonic',
                             duration=self.resolution_duration,
                             delay=self.resolution_delay,
                             pos_delay=self.resolution_pos_delay)

        self.resolution = resolve(chromatic=chromatic, mode=self.mode,
                                  tonic=self.tonic, intervals=self.interval,
                                  descending=descending, harmonic=True,
                                  duration=self.resolution_duration,
                                  delay=self.resolution_delay,
                                  pos_delay=self.resolution_pos_delay)

    def make_question(self):

        tonic = self.concrete_tonic
        interval = self.interval.note_and_octave

        question = Sequence([[tonic, interval]], self.question_duration,
                            self.question_delay, self.question_pos_delay)

        return question

    def make_resolution(self, chromatic, mode, tonic, interval,
                        descending=None):
        pass

    def play_question(self):
        self.question.play()

    def play_resolution(self):
        for sequence in self.resolution:
            sequence.play()

    def check_question(self, user_input_char):
        """Checks whether the given answer is correct."""

        global INTERVALS

        semitones = self.keyboard_index.index(user_input_char[0])

        tonic = self.scales['chromatic_pitch'].scale[0]

        user_interval = INTERVALS[semitones][2]
        correct_interval = INTERVALS[self.interval.semitones][2]

        user_note = self.scales['chromatic_pitch'].scale[semitones]
        correct_note = self.scales['chromatic_pitch']\
            .scale[self.interval.semitones]

        signal = '✓' if semitones == self.interval.semitones else 'x'  # u2713

        extra_response_str = """\
       “{}” ({}─{})
user {} “{}” ({}─{})
{} semitones
""".format(correct_interval, tonic, correct_note,
           signal, user_interval, tonic, user_note, self.interval.semitones)

        response = dict(
            is_correct=False,
            user_interval=user_interval,
            correct_interval=correct_interval,
            user_response_str=user_interval,
            correct_response_str=correct_interval,
            extra_response_str=extra_response_str,
        )

        if semitones == self.interval.semitones:
            response.update({'is_correct': True})

        else:
            response.update({'is_correct': False})

        return response
