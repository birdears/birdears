import subprocess
import time

from random import randrange
from random import choice

from . import KEYBOARD_INDICES
from . import CIRCLE_OF_FIFTHS
from . import DIATONIC_MODES
from . import CHROMATIC_TYPE
from . import INTERVAL_INDEX

from .scale import DiatonicScale
from .scale import ChromaticScale

QUESTION_CLASSES = {}


def register_question_class(f, *args, **kwargs):
    """Decorator for question classes.

    Classes decorated with this decorator will be registered in the
    `QUESTION_CLASSES` global.
    """

    @wraps(f)
    def decorator(*args, **kwargs):
        return f(*args, **kwargs)

    QUESTION_CLASSES.update({f.__name__: f})

    return decorator


class QuestionBase:
    """
    Base Class to be subclassed for Question classes.

    This class implements attributes and routines to be used in Question
    subclasses.
    """

    default_durations = None

    def __init__(self, mode='major', tonic=None, octave=None, descending=None,
                 chromatic=None, n_octaves=None, valid_intervals=None,
                 user_durations=None, prequestion_method=None,
                 resolution_method=None, *args, **kwargs):
        """Inits the class.

        Args:
            mode (str): A string represnting the mode of the question.
                Eg., 'major' or 'minor'
            tonic (str): A string representing the tonic of the
                question, eg.: 'C'; if omitted, it will be selected
                randomly.
            octave (int): A scienfic octave notation, for example,
                4 for 'C4'; if not present, it will be randomly chosen.
            descending (bool): Is the question direction in descending,
                ie., intervals have lower pitch than the tonic.
            chromatic (bool): If the question can have (True) or not
                (False) chromatic intervals, ie., intervals not in the
                diatonic scale of tonic/mode.
            n_octaves (int): Maximum numbr of octaves of the question.
            valid_intervals (list): A list with intervals (int) valid for
                random choice, 1 is 1st, 2 is second etc. Eg. [1, 4, 5] to
                allow only tonics, fourths and fifths.
        """

        global KEYBOARD_INDICES, CIRCLE_OF_FIFTHS

        self.mode = mode

        self.is_descending = descending
        self.is_chromatic = chromatic

        # self.octave = octave if octave else randrange(3, 5)
        if not octave:
            octave = randrange(3, 5)
        elif type(octave) == list:
            octave = choice(octave)
        elif type(octave) == tuple and len(octave) == 2:
            octave = randrange(*octave)

        self.octave = octave

        if not n_octaves:
            self.n_octaves = 1
        else:
            self.n_octaves = n_octaves

        # this should go to questionbase
        if type(valid_intervals) == str:
            valid_intervals = valid_intervals.split(',')
            valid_intervals = [int(x, 10) for x in valid_intervals]

        self.valid_intervals = valid_intervals

        direction = 'ascending' if not self.is_descending else 'descending'
        # FIXME: maybe this should go to __main__
        self.keyboard_index = \
            KEYBOARD_INDICES['chromatic'][direction][self.mode]

        if not tonic:
            tonic = choice(CIRCLE_OF_FIFTHS[randrange(2)])
        elif type(tonic) == list:
            tonic = choice(tonic)

        self.tonic = tonic

        diatonic_scale = DiatonicScale(tonic=tonic, mode=mode, octave=None,
                                       descending=descending,
                                       n_octaves=n_octaves)

        chromatic_scale = ChromaticScale(tonic=tonic, octave=None,
                                         descending=descending,
                                         n_octaves=n_octaves)

        diatonic_scale_pitch = DiatonicScale(tonic=tonic, mode=mode,
                                             octave=self.octave,
                                             descending=descending,
                                             n_octaves=n_octaves)

        chromatic_scale_pitch = ChromaticScale(tonic=tonic, octave=self.octave,
                                               descending=descending,
                                               n_octaves=n_octaves)

        scales = dict({
            'diatonic': diatonic_scale,
            'chromatic': chromatic_scale,
            'diatonic_pitch': diatonic_scale_pitch,
            'chromatic_pitch': chromatic_scale_pitch,
        })
        self.scales = scales

        self.concrete_tonic = scales['diatonic_pitch'].scale[0]
        self.scale_size = len(scales['diatonic'].scale)

        self.durations = self.default_durations
        if user_durations:
            ud_index = {
                0: ('preq', 'duration'),
                1: ('preq', 'delay'),
                2: ('preq', 'pos_delay'),
                3: ('quest', 'duration'),
                4: ('quest', 'delay'),
                5: ('quest', 'pos_delay'),
                6: ('resol', 'duration'),
                7: ('resol', 'delay'),
                8: ('resol', 'pos_delay'),
            }
            ud = user_durations.split(',')
            if len(ud) == len(ud_index):
                for idx, v in ud_index.items():
                    cur_duration = ud[idx].strip()
                    if cur_duration != 'n':
                        self.durations[v[0]][v[1]] = float(cur_duration)

        self.prequestion_method = prequestion_method
        self.resolution_method = resolution_method

    def get_valid_semitones(self):
        """Returns a list with valid semitones for question.
        """

        global DIATONIC_MODES, CHROMATIC_TYPE, MAX_SEMITONES_RESOLVE_BELOW
        global INTERVALS

        diatonic_mode = list(DIATONIC_MODES[self.mode])
        chromatic_network = list(CHROMATIC_TYPE)

        step_network = diatonic_mode

        # FIXME: please refactore this with method signature n_octaves=1:
        if self.n_octaves:
            for i in range(1, self.n_octaves):
                step_network.extend([semitones + 12 * i for semitones in
                                     diatonic_mode[1:]])
                chromatic_network.extend([semitones + 12 * i for semitones in
                                          CHROMATIC_TYPE[1:]])

        if not self.is_chromatic:
            if not self.valid_intervals:
                # semitones = choice(step_network)
                valid_network = step_network
            else:
                valid_network = []
                for item in self.valid_intervals:
                    valid_network.extend(INTERVAL_INDEX[item])
                for i in range(1, self.n_octaves):
                    valid_network.extend([semitones + 12*i for semitones in
                                          valid_network[1:]])
                valid_network = [x for x in valid_network if x in step_network]

                # semitones = choice(valid_network)
        else:
            if not self.valid_intervals:
                # semitones = choice(chromatic_network)
                valid_network = chromatic_network
            else:
                valid_network = []
                for item in self.valid_intervals:
                    valid_network.extend(INTERVAL_INDEX[item])
                for i in range(1, self.n_octaves):
                    valid_network.extend([semitones + 12*i for semitones in
                                          valid_network])

                # semitones = choice(valid_network)

        return valid_network

    def make_question(self):
        """This method should be overwritten by the question subclasses.
        """

        pass

    def make_resolution(self):
        """This method should be overwritten by the question subclasses.
        """

        pass

    def play_question(self):
        """This method should be overwritten by the question subclasses.
        """

        pass

    def check_question(self):
        """This method should be overwritten by the question subclasses.
        """

        pass
