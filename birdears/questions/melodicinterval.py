from ..questionbase import QuestionBase

from ..interval import Interval
from .. import DIATONIC_MODES

class MelodicIntervalQuestion(QuestionBase):
    "Implements a Melodic Interval test."

    def __init__(self, mode='major', tonic=None, octave=None, descending=None,
                 chromatic=None, n_octaves=None, *args, **kwargs):

        super(MelodicIntervalQuestion, self).\
                __init__(mode=mode, tonic=tonic, octave=octave,
                         descending=descending, chromatic=chromatic,
                         n_octaves=n_octaves, *args, **kwargs)

        self.interval = Interval(mode=mode, tonic=self.tonic,
                                 octave=self.octave, chromatic=chromatic,
                                 n_octaves=n_octaves,
                                 descending=descending).interval_data
        # FIXME
        self.resolution_pitch = \
            self.make_resolution(chromatic=chromatic, mode=self.mode,
                                 tonic=self.tonic, interval=self.interval,
                                 descending=descending)
