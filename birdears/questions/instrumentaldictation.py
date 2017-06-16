from random import choice

from ..questionbase import QuestionBase

from ..interval import DiatonicInterval
from ..interval import ChromaticInterval

from .. import DIATONIC_MODES
from .. import MAX_SEMITONES_RESOLVE_BELOW
from .. import INTERVALS

from ..scale import DiatonicScale
from ..scale import ChromaticScale

from ..sequence import Sequence
from ..resolution import Resolution
from ..prequestion import PreQuestion

from ..interfaces.commandline import COLS
from ..interfaces.commandline import center_text


class InstrumentalDictationQuestion(QuestionBase):
    """Implements an instrumental dictation test.
    """

    def __init__(self, mode='major', wait_time=11, n_repeats=1,
                 max_intervals=3, n_notes=4, tonic=None, octave=None,
                 descending=None, chromatic=None, n_octaves=None,
                 valid_intervals=None, user_durations=None,
                 prequestion_method='progression_i_iv_v_i',
                 resolution_method='repeat_only', *args, **kwargs):
        """Inits the class.

        Args:
            mode (str): A string representing the mode of the question.
                Eg., 'major' or 'minor'.
            wait_time (float): Wait time in seconds for the next question or
                repeat.
            n_repeats (int): Number of times the same dictation will be
                repeated before the end of the exercise.
            max_intervals (int): The maximum number of random intervals the
                question will have.
            n_notes (int): The number of notes the melodic dictation will have.
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
            'preq': {'duration': 2, 'delay': 0.5, 'pos_delay': 1},
            'quest': {'duration': 2, 'delay': 0.5, 'pos_delay': 0},
            'resol': {'duration': 2.5, 'delay': 0.5, 'pos_delay': 1}
        }

        super(InstrumentalDictationQuestion, self).\
            __init__(mode=mode, tonic=tonic, octave=octave,
                     descending=descending, chromatic=chromatic,
                     n_octaves=n_octaves, valid_intervals=valid_intervals,
                     user_durations=user_durations,
                     prequestion_method=prequestion_method,
                     resolution_method=resolution_method,
                     default_durations=default_durations, *args, **kwargs)

        self.is_harmonic = False

        self.wait_time = wait_time
        self.n_repeats = n_repeats

        if not chromatic:
            INTERVAL_CLASS = DiatonicInterval
        else:
            INTERVAL_CLASS = ChromaticInterval

        question_intervals = [INTERVAL_CLASS(mode=mode, tonic=self.tonic,
                              octave=self.octave, n_octaves=self.n_octaves,
                              descending=descending,
                              valid_intervals=self.valid_intervals)
                              for _ in range(max_intervals)]

        self.question_phrase_intervals = [choice(question_intervals)
                                          for _ in range(n_notes-1)]

        self.question_phrase = [0]

        self.question_phrase.extend([interval.semitones
                                     for interval
                                     in self.question_phrase_intervals])

        # self.pre_question = self.make_pre_question(method='none')
        self.pre_question =\
            self.make_pre_question(method=prequestion_method)
        self.question = self.make_question(self.question_phrase)
        self.resolution = self.make_resolution(method=resolution_method)

    def make_pre_question(self, method):
        prequestion = PreQuestion(method=method, question=self)

        return prequestion()

    def make_question(self, phrase_semitones):
        return Sequence([self.scales['chromatic_pitch'].scale[n]
                        for n in phrase_semitones], **self.durations['quest'])

    def make_resolution(self, method):

        resolve = Resolution(method=method, question=self)

        resolution = resolve()

        return resolution

    def play_question(self):

        for r in range(self.n_repeats):
            self.pre_question.play()
            self.question.play()

            for i in range(self.wait_time):
                time_left = str(self.wait_time - i).rjust(3)
                text = '{} seconds remaining...'.format(time_left)
                print(center_text(text, sep=False), end='')
                self.question._wait(1)

    def check_question(self):
        """Checks whether the given answer is correct.

        This currently doesn't applies to instrumental dictation questions.
        """

        global INTERVALS

        intervals_str = "".join([INTERVALS[s][1].center(7)
                                for s in self.question_phrase])
        notes_str = "".join([self.scales['chromatic_pitch'].scale[s].center(7)
                            for s in self.question_phrase])

        correct_response_str = """\
The intervals and notes of this question:

{intervals}
{notes}
""".format(**dict(intervals=intervals_str, notes=notes_str))
        response = {
            'correct_semitones': self.question_phrase,
            'correct_response_str': correct_response_str
        }

        return response
