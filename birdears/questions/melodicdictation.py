from random import choice
from random import sample

from .. import CHROMATIC_TYPE

from ..questionbase import QuestionBase
from ..questionbase import get_valid_pitches

from ..scale import DiatonicScale
from ..scale import ChromaticScale

from ..interval import Interval
from ..note_and_pitch import get_pitch_by_number

from ..sequence import Sequence
from ..resolution import Resolution
from ..prequestion import PreQuestion


class MelodicDictationQuestion(QuestionBase):
    """Implements a melodic dictation test.
    """

    def __init__(self, mode='major', max_intervals=3, n_notes=4, tonic='C',
                 octave=4, descending=False, chromatic=False, n_octaves=1,
                 valid_intervals=CHROMATIC_TYPE, user_durations=None,
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
            'quest': {'duration': 2, 'delay': 0.8, 'pos_delay': 0},
            'resol': {'duration': 2.5, 'delay': 0.5, 'pos_delay': 1}
        }

        super(MelodicDictationQuestion, self).\
            __init__(mode=mode, tonic=tonic, octave=octave,
                     descending=descending, chromatic=chromatic,
                     n_octaves=n_octaves, valid_intervals=valid_intervals,
                     user_durations=user_durations,
                     prequestion_method=prequestion_method,
                     resolution_method=resolution_method,
                     default_durations=default_durations, *args, **kwargs)

        self.is_harmonic = False

        if not chromatic:
            self.scale = DiatonicScale(tonic=self.tonic_str, mode=mode,
                                       octave=octave, n_octaves=n_octaves,
                                       descending=descending)
        else:
            self.scale = ChromaticScale(tonic=self.tonic_str, octave=octave,
                                        n_octaves=n_octaves,
                                        descending=descending)

        self.valid_pitches = get_valid_pitches(self.scale, valid_intervals)

        random_choose_from_pitches = sample(self.valid_pitches, max_intervals)

        # self.random_pitches = choices(population=random_choose_from_pitches,
        #                              k=n_notes)
        self.random_pitches = [choice(random_choose_from_pitches) for note
                               in range(n_notes)]

        self.pre_question = \
            self.make_pre_question(method=prequestion_method)

        self.question = self.make_question()
        self.resolution = self.make_resolution(method=resolution_method)

    def make_pre_question(self, method):
        prequestion = PreQuestion(method=method, question=self)

        return prequestion()

    def make_question(self):
        return Sequence(self.random_pitches, **self.durations['quest'])

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

        # global INTERVALS

        string_offset = 5

        tonic_pitch_number = self.tonic_pitch.pitch_number

        user_semitones = [self.keyboard_index.index(s)
                          for s in user_input_keys]

        user_pitches = [get_pitch_by_number(tonic_pitch_number + semitones)
                        for semitones in user_semitones]

        correct_intervals = [Interval(self.tonic_pitch, pitch)
                             for pitch in self.random_pitches]

        user_intervals = [Interval(self.tonic_pitch, pitch)
                          for pitch in user_pitches]

        user_response_str = "".join([interval['data'][1].center(string_offset)
                                     for interval in user_intervals])

        correct_response_str = "".join([interval['data'][1]
                                       .center(string_offset)
                                       for interval in correct_intervals])

        correct_semitones = list()
        correct_wrong_str = str()

        for position, correct_pitch in enumerate(self.random_pitches):
            if correct_pitch == user_pitches[position]:
                correct_semitones.append(True)
                correct_wrong_str += "✓".center(string_offset)  # u2713
            else:
                correct_semitones.append(False)
                correct_wrong_str += "x".center(string_offset)

        extra_response_str = """\
{}
{}
""".format(correct_wrong_str, correct_response_str)

        is_correct = user_pitches == self.random_pitches

        response = {
            'is_correct': is_correct,
            'user_input': user_input_keys,
            'user_semitones': user_semitones,
            'question_semitones': self.random_pitches,
            'correct_semitones': correct_semitones,
            'user_response_str': user_response_str,
            'correct_response_str': correct_response_str,
            'extra_response_str': extra_response_str
        }

        return response
