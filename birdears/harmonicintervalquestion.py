from .questionbase import QuestionBase

from .interval import Interval
from . import DIATONIC_MODES

class HarmonicIntervalQuestion(QuestionBase):
    "Implements a Harmonic Interval test."

    def __init__(self, mode='major', tonic=None, octave=None, descending=None,
                 chromatic=None, n_octaves=None, *args, **kwargs):

        super(HarmonicIntervalQuestion, self).\
                __init__(mode=mode, tonic=tonic, octave=octave,
                         descending=descending, chromatic=chromatic,
                         n_octaves=n_octaves, *args, **kwargs)

        tonic = self.tonic
        self.interval = Interval(mode=mode, tonic=self.tonic,
                                 octave=self.octave, chromatic=chromatic,
                                 n_octaves=n_octaves,
                                 descending=descending).interval_data

        # FIXME
        self.resolution_pitch = \
            self.make_resolution(chromatic=chromatic, mode=self.mode,
                                 tonic=self.tonic, interval=self.interval,
                                 descending=descending)

    def play_question(self):

        tonic = self.concrete_tonic
        interval = self.interval['note_and_octave']

        #question_chords = [(tonic, tonic), (tonic, interval)]
        question_chords = [(tonic, interval)]

        for item in question_chords:
            self._play_chord(chord=item, duration=self.question_duration,
                             delay=self.question_delay)

        if self.question_pos_delay:
            self._wait(self.resolution_pos_delay)

    def play_resolution(self):

        tonic = self.concrete_tonic

        for tone in self.resolution_pitch:
            self._play_chord(chord=[tonic, tone],
                             duration=self.resolution_duration,
                             delay=self.resolution_delay)

        if self.resolution_pos_delay:
            self._wait(self.resolution_pos_delay)
