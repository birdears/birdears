from ..questionbase import QuestionBase

from ..interval import DiatonicInterval
from ..interval import ChromaticInterval

from .. import DIATONIC_MODES
from .. import MAX_SEMITONES_RESOLVE_BELOW
from .. import INTERVALS

from ..scale import DiatonicScale

from ..sequence import Sequence
from ..resolution import Resolution
from ..prequestion import PreQuestion


class HarmonicIntervalQuestion(QuestionBase):
    """Implements a Harmonic Interval test.
    """

    def __init__(self, mode='major', tonic=None, octave=None, descending=None,
                 chromatic=None, n_octaves=None, valid_intervals=None,
                 user_durations=None, prequestion_method='none',
                 resolution_method='nearest_tonic', *args, **kwargs):
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
            valid_intervals (list): A list with intervals (int) valid for
                random choice, 1 is 1st, 2 is second etc. Eg. [1, 4, 5] to
                allow only tonics, fourths and fifths.
            user_durations (str): A string with 9 comma-separated `int` or
                `float`s to set the default duration for the notes played. The
                values are respectively for: pre-question duration (1st),
                pre-question delay (2nd), and pre-question pos-delay (3rd);
                question duration (4th), question delay (5th), and question
                pos-delay (6th); resolution duration (7th), resolution
                delay (8th), and resolution pos-delay (9th).
                duration is the duration in of the note in seconds; delay is
                the time to wait before playing the next note, and pos_delay is
                the time to wait after all the notes of the respective sequence
                have been played. If any of the user durations is `n`, the
                default duration for the type of question will be used instead.
                Example::
                    "2,0.5,1,2,n,0,2.5,n,1"
            prequestion_method (str): Method of playing a cadence or the
                exercise tonic before the question so to affirm the question
                musical tonic key to the ear. Valid ones are registered in the
                `birdears.prequestion.PREQUESION_METHODS` global dict.
            resolution_method (str): Method of playing the resolution of an
                exercise. Valid ones are registered in the
                `birdears.resolution.RESOLUTION_METHODS` global dict.
        """

        default_durations = {
            'preq': {'duration': 3, 'delay': 0.5, 'pos_delay': 1},
            'quest': {'duration': 3, 'delay': 0.5, 'pos_delay': 0},
            'resol': {'duration': 2.5, 'delay': 0.5, 'pos_delay': 1}
        }

        super(HarmonicIntervalQuestion,
              self).__init__(mode=mode, tonic=tonic, octave=octave,
                             descending=descending, chromatic=chromatic,
                             n_octaves=n_octaves,
                             valid_intervals=valid_intervals,
                             user_durations=user_durations,
                             prequestion_method=prequestion_method,
                             resolution_method=resolution_method,
                             default_durations=default_durations,
                             *args, **kwargs)

        self.is_harmonic = True

        # tonic = self.tonic

        if not chromatic:
            self.interval = \
                DiatonicInterval(mode=mode, tonic=self.tonic,
                                 octave=self.octave,
                                 n_octaves=n_octaves,
                                 descending=descending,
                                 valid_intervals=self.valid_intervals)

        else:
            self.interval = \
                ChromaticInterval(mode=mode, tonic=self.tonic,
                                  octave=self.octave,
                                  n_octaves=n_octaves,
                                  descending=descending,
                                  valid_intervals=self.valid_intervals)

        self.pre_question = self.make_pre_question(method=prequestion_method)
        self.question = self.make_question()
        self.resolution = self.make_resolution(method=resolution_method)

    def make_pre_question(self, method):
        prequestion = PreQuestion(method=method, question=self)

        return prequestion()

    def make_question(self):

        tonic = self.concrete_tonic
        interval = self.interval.note_and_octave
        durations = self.durations

        question = Sequence([[tonic, interval]], **self.durations['quest'])

        return question

    def make_resolution(self, method):

        resolve = Resolution(method=method, question=self)
        resolution = resolve()

        return resolution

    def play_question(self):
        self.pre_question.play()
        self.question.play()

    def play_resolution(self):
        thread = self.resolution.play()
        thread.join()

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
