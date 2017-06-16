from ..logger import logger
from ..logger import log_event

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


class MelodicIntervalQuestion(QuestionBase):
    """Implements a Melodic Interval test.
    """

    @log_event
    def __init__(self, mode='major', tonic=None, octave=None, descending=None,
                 chromatic=None, n_octaves=None, valid_intervals=None,
                 user_durations=None, prequestion_method='tonic_only',
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
        """

        self.default_durations = {
            'preq': {'duration': 2, 'delay': 0.5, 'pos_delay': 1},
            'quest': {'duration': 2, 'delay': 0.5, 'pos_delay': 0},
            'resol': {'duration': 2.5, 'delay': 0.5, 'pos_delay': 1}
        }

        super(MelodicIntervalQuestion, self).\
            __init__(mode=mode, tonic=tonic, octave=octave,
                     descending=descending, chromatic=chromatic,
                     n_octaves=n_octaves, valid_intervals=valid_intervals,
                     user_durations=user_durations,
                     prequestion_method=prequestion_method,
                     resolution_method=resolution_method, *args, **kwargs)

        self.is_harmonic = False

        if not chromatic:
            self.interval = \
                DiatonicInterval(mode=mode, tonic=self.tonic,
                                 octave=self.octave,
                                 n_octaves=self.n_octaves,
                                 descending=descending,
                                 valid_intervals=self.valid_intervals)
        else:
            self.interval = \
                ChromaticInterval(mode=mode, tonic=self.tonic,
                                  octave=self.octave,
                                  n_octaves=self.n_octaves,
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

        question = Sequence([interval], **self.durations['quest'])

        return question

    def make_resolution(self, method):

        resolve = Resolution(method=method, question=self)
        resolution = resolve()

        return resolution

    def play_question(self):
        # Other threads can call a thread’s join() method. This blocks the
        # calling thread until the thread whose join() method is called is
        # terminated.
        # https://docs.python.org/3/library/threading.html#thread-objects

        self.pre_question.play()
        self.question.play()

    def play_resolution(self):

        thread = self.resolution.play()
        thread.join()

    def check_question(self, user_input_char):
        """Checks whether the given answer is correct.
        """

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
