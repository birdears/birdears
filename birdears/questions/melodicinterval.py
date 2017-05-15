from ..questionbase import QuestionBase

from ..interval import DiatonicInterval
from ..interval import ChromaticInterval

from .. import DIATONIC_MODES
from .. import MAX_SEMITONES_RESOLVE_BELOW
from .. import INTERVALS

from ..scale import DiatonicScale

from ..sequence import Sequence
from ..resolution import Resolution


class MelodicIntervalQuestion(QuestionBase):
    """Implements a Melodic Interval test.
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

        super(MelodicIntervalQuestion, self).\
             __init__(mode=mode, tonic=tonic, octave=octave,
                      descending=descending, chromatic=chromatic,
                      n_octaves=n_octaves, *args, **kwargs)

        self.question_duration = 2
        self.question_delay = 0.5
        self.question_pos_delay = 0

        self.resolution_duration = 2.5
        self.resolution_delay = 0.5
        self.resolution_pos_delay = 1

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

        # self.pre_question = self.make_pre_question()
        self.question = self.make_question()

        resolve = Resolution(method='resolve_to_nearest_tonic',
                             duration=self.resolution_duration,
                             delay=self.resolution_delay,
                             pos_delay=self.resolution_pos_delay)

        self.resolution =  resolve.resolve(chromatic=chromatic, mode=self.mode,
                                   tonic=self.tonic, intervals=self.interval,
                                   descending=descending)

    # def make_pre_question(self):
    #     self.pre_question = Sequence([], duration=self.question_duration,
    #                         delay=self.question_delay,
    #                         pos_delay=1)
    #     self.pre_question.make_chord_progression(self.tonic, self.mode,
    #                                              [1, 4, 5, 1])
    #
    #     return self.pre_question

    def make_question(self):

        tonic = self.concrete_tonic
        interval = self.interval.note_and_octave

        question = Sequence([tonic, interval], duration=self.question_duration,
                            delay=self.question_delay,
                            pos_delay=self.question_pos_delay)

        return question

    def make_resolution(self, chromatic, mode, tonic, interval,
                        descending=None):

        # global DIATONIC_MODES, MAX_SEMITONES_RESOLVE_BELOW
        #
        # resolution_pitch = []
        #
        # # diatonic_mode = DIATONIC_MODES[mode]
        #
        # scale_pitch = DiatonicScale(tonic=tonic, mode=mode,
        #                             octave=interval.interval_octave,
        #                             descending=descending)
        # self.res_scale = scale_pitch
        #
        # if interval.chromatic_offset <= MAX_SEMITONES_RESOLVE_BELOW:
        #     begin_to_diatonic = slice(None, interval.diatonic_index + 1)
        #     resolution_pitch = scale_pitch.scale[begin_to_diatonic]
        #     if interval.is_chromatic:
        #         resolution_pitch.append(interval.note_and_octave)
        #     resolution_pitch.reverse()
        # else:
        #     diatonic_to_end = slice(interval.diatonic_index, None)
        #     if interval.is_chromatic:
        #         resolution_pitch.append(interval.note_and_octave)
        #     resolution_pitch.extend(scale_pitch.scale[diatonic_to_end])
        #
        # # unisson and octave
        # if interval.semitones == 0:
        #     resolution_pitch.append(scale_pitch.scale[0])
        #
        # elif interval.semitones % 12 == 0:
        #     # FIXME: multipe octaves
        #     resolution_pitch.append("{}{}".format(tonic,
        #                             interval.tonic_octave))
        #
        # resolution = Sequence(resolution_pitch,
        #                       duration=self.resolution_duration,
        #                       delay=self.resolution_delay,
        #                       pos_delay=self.resolution_pos_delay)
        #
        # return resolution
        pass

    def play_question(self):
        # self.pre_question.play()
        self.question.play()

    def play_resolution(self):
        for sequence in self.resolution:
            sequence.play()

    def check_question(self, user_input_char):
        """Checks whether the given answer is correct."""

        global INTERVALS

        semitones = self.keyboard_index.index(user_input_char[0])

        user_interval = INTERVALS[semitones][2]
        correct_interval = INTERVALS[self.interval.semitones][2]

        response = dict(
            is_correct = False,
            user_interval = user_interval,
            correct_interval = correct_interval,
            user_response_str = user_interval,
            correct_response_str = correct_interval,
        )

        if semitones == self.interval.semitones:
            response.update({'is_correct': True})

        else:
            response.update({'is_correct': False})

        return response
