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

DURATION = 0
DELAY = 1
POS_DELAY = 2


class InstrumentalDictationQuestion(QuestionBase):
    """Implements an instrumental dictation test.
    """

    def __init__(self, mode='major', wait_time=11, n_repeats=1,
                 max_intervals=3, n_notes=4, tonic=None, octave=None,
                 descending=None, chromatic=None, n_octaves=None,
                 valid_intervals=None, *args, **kwargs):
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
        """

        super(InstrumentalDictationQuestion, self).\
            __init__(mode=mode, tonic=tonic, octave=octave,
                     descending=descending, chromatic=chromatic,
                     n_octaves=n_octaves, valid_intervals=valid_intervals,
                     *args, **kwargs)

        durations = dict(
            preq=(2, 0.5, 1),
            quest=(2, 0.5, 0),
            resol=(2.5, 0.5, 1)
        )

        self.durations = durations

        self.wait_time = wait_time
        self.n_repeats = n_repeats

        # self.prequestion_duration = 2
        # self.prequestion_delay = 0.5
        # self.prequestion_pos_delay = 0
        #
        # self.question_duration = 0.5
        # self.question_delay = 0.5
        # self.question_pos_delay = 0
        #
        # self.resolution_duration = 2.5
        # self.resolution_delay = 0.5
        # self.resolution_pos_delay = 1

        # FIXME: for chromatics
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
            self.make_pre_question(method='progression_i_iv_v_i')
        self.question = self.make_question(self.question_phrase)
        self.resolution = self.make_resolution()

    def make_pre_question(self, method):
        prequestion = PreQuestion(method=method,
                                  duration=self.durations['preq'][DURATION],
                                  delay=self.durations['preq'][DELAY],
                                  pos_delay=self.durations['preq'][POS_DELAY])

        return prequestion(**dict(tonic=self.tonic, tonic_octave=self.octave,
                           mode=self.mode,
                           intervals=self.question_phrase_intervals))

    def make_question(self, phrase_semitones):
        return Sequence([self.scales['chromatic_pitch'].scale[n]
                        for n in phrase_semitones],
                        duration=self.durations['quest'][DURATION],
                        delay=self.durations['quest'][DELAY],
                        pos_delay=self.durations['quest'][POS_DELAY])

    def make_resolution(self):
        # the idea here is execute resolve() to each interval of the dictation

        resolve = Resolution(method='repeat_only',
                             duration=self.durations['resol'][DURATION],
                             delay=self.durations['resol'][DELAY],
                             pos_delay=self.durations['resol'][POS_DELAY])

        resolution = resolve(elements=self.question.elements)

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

    # TODO: implement his later
    # def play_resolution(self):
    #
    #    for sequence in self.resolution:
    #        sequence.play()

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
