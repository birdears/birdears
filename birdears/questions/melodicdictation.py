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


class MelodicDictationQuestion(QuestionBase):
    """Implements a melodic dictation test.
    """

    def __init__(self, mode='major', max_intervals=3, n_notes=4, tonic=None,
                 octave=None, descending=None, chromatic=None,
                 n_octaves=None, valid_intervals=None, user_durations=None,
                 prequestion_method='progression_i_iv_v_i',
                 resolution_method='repeat_only', *args, **kwargs):
        """Inits the class.

        Args:
            mode (str): A string representing the mode of the question.
                Eg., 'major' or 'minor'.
            max_intervals (int): The maximum number of random intervals
                the question will have.
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
        """

        self.default_durations = {
            'preq': {'duration': 2, 'delay': 0.5, 'pos_delay': 1},
            'quest': {'duration': 2, 'delay': 0.8, 'pos_delay': 0},
            'resol': {'duration': 2.5, 'delay': 0.5, 'pos_delay': 1}
        }

        super(MelodicDictationQuestion, self).\
            __init__(mode=mode, tonic=tonic, octave=octave,
                     descending=descending, chromatic=chromatic,
                     n_octaves=n_octaves, valid_intervals=valid_intervals,
                     user_durations=user_durations,
                     prequestion_method=prequestion_method,
                     resolution_method=resolution_method, *args, **kwargs)

        self.is_harmonic = False

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

        self.pre_question =\
            self.make_pre_question(method=prequestion_method)
        # self.pre_question = self.make_pre_question(method='none')
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
        self.pre_question.play()
        self.question.play()

    def play_resolution(self):

        thread = self.resolution.play()
        thread.join()

    def check_question(self, user_input_keys):
        """Checks whether the given answer is correct."""

        global INTERVALS

        STR_OFFSET = 5

        user_input_semitones = [self.keyboard_index.index(s)
                                for s in user_input_keys]

        user_response_str = "".join([INTERVALS[s][1].center(STR_OFFSET)
                                     for s in user_input_semitones])
        correct_response_str = "".join([INTERVALS[s][1].center(STR_OFFSET)
                                        for s in self.question_phrase])

        correct_semitones = list()
        correct_wrong_str = str()

        for i, s in enumerate(self.question_phrase):
            if self.question_phrase[i] == user_input_semitones[i]:
                correct_semitones.append(True)
                correct_wrong_str += "✓".center(STR_OFFSET)  # u2713
            else:
                correct_semitones.append(False)
                correct_wrong_str += "x".center(STR_OFFSET)

        extra_response_str = """\
{}
{}
""".format(correct_wrong_str, correct_response_str)

        response = dict(
            is_correct=False,
            user_input=user_input_keys,
            user_semitones=user_input_semitones,
            question_semitones=self.question_phrase,
            correct_semitones=correct_semitones,
            user_response_str=user_response_str,
            correct_response_str=correct_response_str,
            extra_response_str=extra_response_str,
        )

        if user_input_semitones == self.question_phrase:
            response.update({'is_correct': True})
        else:
            response.update({'is_correct': False})

        return response
