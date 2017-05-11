from random import choice

from ..questionbase import QuestionBase

# from ..interval import Interval
from ..interval import DiatonicInterval, ChromaticInterval

from .. import DIATONIC_MODES
from .. import MAX_SEMITONES_RESOLVE_BELOW
from .. import INTERVALS

from ..scale import DiatonicScale
from ..scale import ChromaticScale

from ..sequence import Sequence


class MelodicDictationQuestion(QuestionBase):
    """Implements a melodic dictation test.
    """

    def __init__(self, mode='major', max_intervals=3, n_notes=4, tonic=None,
                 octave=None, descending=None, chromatic=None, n_octaves=None,
                 *args, **kwargs):

        super(MelodicDictationQuestion, self).\
                __init__(mode=mode, tonic=tonic, octave=octave,
                         descending=descending, chromatic=chromatic,
                         n_octaves=n_octaves, *args, **kwargs)

        self.question_duration = 2
        self.question_delay = 0.5
        self.question_pos_delay = 0

        self.resolution_duration = 2.5
        self.resolution_delay = 0.5
        self.resolution_pos_delay = 1

        question_intervals = [DiatonicInterval(mode=mode, tonic=self.tonic,
                              octave=self.octave, n_octaves=n_octaves,
                              descending=descending)
                              for _ in range(max_intervals)]

        self.question_phrase_intervals = [choice(question_intervals)
                                          for _ in range(n_notes-1)]

        self.question_phrase = [0]

        self.question_phrase.extend([interval.semitones
                                     for interval
                                     in self.question_phrase_intervals])

        self.question = self.make_question(self.question_phrase)

        self.resolution = Sequence(self.question.elements,
                                   duration=self.resolution_duration,
                                   delay=self.resolution_delay,
                                   pos_delay=self.resolution_pos_delay)

    def make_question(self, phrase_semitones):
        return Sequence([self.scales['chromatic_pitch'].scale[n]
                        for n in phrase_semitones],
                        duration=self.question_duration,
                        delay=self.question_delay,
                        pos_delay=self.question_pos_delay)

    def check_question(self, user_input_keys):
        """Checks whether the given answer is correct."""

        global INTERVALS

        user_input_semitones = [self.keyboard_index.index(s)
                                for s in user_input_keys]

        user_response_str = "-".join([INTERVALS[s][1]
                                     for s in user_input_keys])
        correct_response_str = "-".join([INTERVALS[s][1]
                                        for s in self.question_phrase])

        response = {
            'is_correct': False,
            'user_input': user_input_keys,
            'user_semitones': user_input_semitones,
            'correct_semitones': self.question_phrase,
            'user_response_str': user_response_str,
            'correct_response_str': correct_response_str
        }

        if user_input_semitones == self.question_phrase:
            response.update({'is_correct': True})
        else:
            response.update({'is_correct': False})

        return response
