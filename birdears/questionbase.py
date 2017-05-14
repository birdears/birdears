import subprocess
import time

from random import randrange
from random import choice

from . import KEYBOARD_INDICES
from . import KEYS

from .scale import DiatonicScale
from .scale import ChromaticScale


class QuestionBase:
    """
    Base Class to be subclassed for Question classes.

    This class implements attributes and routines to be used in Question
    subclasses.
    """

    # question_duration = 2
    # question_delay = 1.5
    # question_pos_delay = 0
    #
    # resolution_duration = 2.5
    # resolution_delay = 0.5
    # resolution_pos_delay = 1

    def __init__(self, mode='major', tonic=None, octave=None, descending=None,
                 chromatic=None, n_octaves=None, *args, **kwargs):

        global KEYBOARD_INDICES, KEYS

        self.mode = mode

        self.is_descending = descending
        self.is_chromatic = chromatic

        # self.octave = octave if octave else randrange(3, 5)
        self.octave = octave or randrange(2, 7)
        self.n_octaves = n_octaves or 1

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

    def play_question(self):
        """This method should be overwritten by the question subclasses.
        """

        pass

    def check_question(self):
        """This method should be overwritten by the question subclasses.
        """

        pass
