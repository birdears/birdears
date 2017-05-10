import subprocess
import time

from random import randrange
from random import choice

from . import KEYBOARD_INDICES
from . import KEYS
# from . import MAX_SEMITONES_RESOLVE_BELOW
# from . import INTERVALS

from .scale import DiatonicScale
from .scale import ChromaticScale

# from .sequence import Sequence


class QuestionBase:
    """
    Base Class to be subclassed for Question classes.

    This class implements attributes and routines to be used in Question
    subclasses.
    """

    def __init__(self, mode='major', tonic=None, octave=None, descending=None,
                 chromatic=None, n_octaves=None, *args, **kwargs):

        global KEYBOARD_INDICES, KEYS

        self.question_duration = 2
        self.question_delay = 1.5
        self.question_pos_delay = 0

        self.resolution_duration = 2.5
        self.resolution_delay = 0.5
        self.resolution_pos_delay = 1

        self.mode = mode

        # self.octave = octave if octave else randrange(3, 5)
        self.octave = octave or randrange(3, 5)

        # FIXME: maybe this should go to __main__
        self.keyboard_index = KEYBOARD_INDICES['chromatic'][self.mode]

        # if descending:
        #    self.keyboard_index = self.keyboard_index[::-1].swapcase()

        # FIXME
        # self.tonic = tonic if tonic else choice(KEYS)
        self.tonic = tonic or choice(KEYS)
        tonic = self.tonic

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

    def make_question(self):
        """This method should be overwritten by the question subclasses.
        """

        pass

    def make_resolution(self):
        """This method should be overwritten by the question subclasses.
        """

        pass

    def check_question(self):
        """This method should be overwritten by the question subclasses.
        """

        pass
