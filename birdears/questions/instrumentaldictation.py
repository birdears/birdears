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

from ..__main__ import COLS
from ..__main__ import center_text


class InstrumentalDictationQuestion(QuestionBase):
    """Implements an instrumental dictation test.
    """

    def __init__(self, mode='major', wait_time=11, n_repeats=1,
                 max_intervals=3, n_notes=4, tonic=None, octave=None,
                 descending=None, chromatic=None, n_octaves=None,
                 *args, **kwargs):

        super(InstrumentalDictationQuestion, self).\
                __init__(mode=mode, tonic=tonic, octave=octave,
                         descending=descending, chromatic=chromatic,
                         n_octaves=n_octaves, *args, **kwargs)

        self.wait_time = wait_time
        self.n_repeats = n_repeats

        self.question_duration = 0.5
        self.question_delay = 0.5
        self.question_pos_delay = 0

        # self.resolution_duration = 2.5
        # self.resolution_delay = 0.5
        # self.resolution_pos_delay = 1

        # FIXME: for chromatics
        if not chromatic:
            INTERVAL_CLASS = DiatonicInterval
        else:
            INTERVAL_CLASS = ChromaticInterval

        question_intervals = [INTERVAL_CLASS(mode=mode, tonic=self.tonic,
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

        # self.resolution = Sequence(self.question.elements,
        #                           duration=self.resolution_duration,
        #                           delay=self.resolution_delay,
        #                           pos_delay=self.resolution_pos_delay)

    def make_question(self, phrase_semitones):
        return Sequence([self.scales['chromatic_pitch'].scale[n]
                        for n in phrase_semitones],
                        duration=self.question_duration,
                        delay=self.question_delay,
                        pos_delay=self.question_pos_delay)

    def play_question(self):

        for r in range(self.n_repeats):
            self.question.play()

            for i in range(self.wait_time):
                time_left = str(self.wait_time - i).rjust(3)
                text = '{} seconds remaining...'.format(time_left)
                print(center_text(text, sep=False), end='')
                self.question._wait(1)

    def play_resolution(self):
        pass

    def check_question(self, user_input_keys):

        """Checks whether the given answer is correct."""

        # global INTERVALS
        #
        # user_input_semitones = [self.keyboard_index.index(s)
        #                         for s in user_input_keys]
        #
        # user_response_str = "-".join([INTERVALS[s][1]
        #                              for s in user_input_semitones])
        # correct_response_str = "-".join([INTERVALS[s][1]
        #                                 for s in self.question_phrase])
        #
        # response = {
        #     'is_correct': False,
        #     'user_input': user_input_keys,
        #     'user_semitones': user_input_semitones,
        #     'correct_semitones': self.question_phrase,
        #     'user_response_str': user_response_str,
        #     'correct_response_str': correct_response_str
        # }
        #
        # if user_input_semitones == self.question_phrase:
        #     response.update({'is_correct': True})
        # else:
        #     response.update({'is_correct': False})
        #
        # return response

        pass
