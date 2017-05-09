from random import choice

from ..questionbase import QuestionBase

from ..interval import Interval
#from .. import DIATONIC_MODES

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

        question_intervals = [Interval(mode=mode, tonic=self.tonic,
                              octave=self.octave, chromatic=chromatic,
                              n_octaves=n_octaves, descending=descending)
                              for _ in range(max_intervals)]

        self.question_phrase_intervals = [choice(question_intervals)
                                          for _ in range(n_notes-1)]

        #question_phrase = Sequence()
        self.question_phrase = list([0])

        self.question_phrase.extend([interval.interval_data['semitones']
                                     for interval
                                     in self.question_phrase_intervals])

    def play_question(self, melodic_phrase=None):

        tonic = self.concrete_tonic

        for item in self.question_phrase:
            self._play_note(note=self.scales['chromatic_pitch'].scale[item],
                            duration=self.question_duration,
                            delay=self.question_delay)

        if self.question_pos_delay:
            self._wait(self.resolution_pos_delay)

    def play_resolution(self):

        tonic = self.concrete_tonic

        for tone in [self.scales['chromatic_pitch'].scale[note]
                     for note in self.question_phrase]:
            self._play_note(tone,
                            duration=self.resolution_duration,
                            delay=self.resolution_delay)

        if self.resolution_pos_delay:
            self._wait(self.resolution_pos_delay)

    def check_question(self, user_input_keys):
        """Checks whether the given answer is correct."""

        global INTERVALS

        user_input_semitones = [self.keyboard_index.index(s)
                                for s in user_input_keys]

        response = {
            'is_correct': False,
            'user_input': user_input_keys,
            'user_semitones': user_input_semitones,
            'correct_semitones': self.question_phrase,
        }

        if user_input_semitones == self.question_phrase:
            response.update({'is_correct': True})
        else:
            response.update({'is_correct': False})

        return response
