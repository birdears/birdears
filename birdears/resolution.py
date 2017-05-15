from . import MAX_SEMITONES_RESOLVE_BELOW

from .scale import DiatonicScale
from .scale import ChromaticScale

from .sequence import Sequence

class Resolution:

    def __init__(self, method, duration, delay, pos_delay):
        """This class implements methods for different types of question
        resolutions.

        Args:
            method (str): The method used in the resolution.
            duration (float): Default playing time for each element in the
                resolution.
            delay (float): Default waiting time to play the next element
                in the resolution.
            pos_delay (float): Waiting time after playing the last element
                in the resolution.

        Todo:
            * Maybe refactor the resolve `method`s with a prefix.
        """

        self.METHOD = getattr(self, method)

        self.resolution_duration = duration
        self.resolution_delay = delay
        self.resolution_pos_delay = pos_delay

    def resolve(self, *args, **kwargs):
        """Calls the resolution method and pass arguments to it.
        """
        return self.METHOD(*args, **kwargs)

    def resolve_to_nearest_tonic(self, chromatic, mode, tonic, intervals,
                                 descending=None):
        """Resolve the intervals to their nearest tonics.

        Args:
            chromatic (bool): x
            mode (str): x
            tonic (str): x
            intervals (str or array_type): x
            descending (bool): x

        Todo:
            * chromatic doesn't seem to be used.
        """

        global DIATONIC_MODES, MAX_SEMITONES_RESOLVE_BELOW

        sequence_list = []

        if type(intervals) is not list:
            intervals = [intervals]

        # diatonic_mode = DIATONIC_MODES[mode]

        for interval in intervals:
            resolution_pitch = []
            scale_pitch = DiatonicScale(tonic=tonic, mode=mode,
                                        octave=interval.interval_octave,
                                        descending=descending)
            self.res_scale = scale_pitch

            if interval.chromatic_offset <= MAX_SEMITONES_RESOLVE_BELOW:
                begin_to_diatonic = slice(None, interval.diatonic_index + 1)
                resolution_pitch.extend(scale_pitch.scale[begin_to_diatonic])
                if interval.is_chromatic:
                    resolution_pitch.append(interval.note_and_octave)
                resolution_pitch.reverse()
            else:
                diatonic_to_end = slice(interval.diatonic_index, None)
                if interval.is_chromatic:
                    resolution_pitch.append(interval.note_and_octave)
                resolution_pitch.extend(scale_pitch.scale[diatonic_to_end])

            # unisson and octave
            if interval.semitones == 0:
                resolution_pitch.append(scale_pitch.scale[0])

            elif interval.semitones % 12 == 0:
                # FIXME: multipe octaves
                resolution_pitch.append("{}{}".format(tonic,
                                        interval.tonic_octave))

            sequence_list.append(Sequence(resolution_pitch,
                              duration=self.resolution_duration,
                              delay=self.resolution_delay,
                              pos_delay=self.resolution_pos_delay))


        return sequence_list

    def resolve_to_nearest_tonic_harmonically(self, chromatic, mode, tonic,
                                              intervals, descending=None):
        """Resolve the intervals to their nearest tonics harmonically.

        Args:
            chromatic (bool): x
            mode (str): x
            tonic (str): x
            intervals (str or array_type): x
            descending (bool): x

        Todo:
            * chromatic doesn't seem to be used.
        """

        global DIATONIC_MODES, MAX_SEMITONES_RESOLVE_BELOW

        sequence_list = []

        if type(intervals) is not list:
            intervals = [intervals]

        # diatonic_mode = DIATONIC_MODES[mode]

        for interval in intervals:
            resolution_pitch = []
            scale_pitch = DiatonicScale(tonic=tonic, mode=mode,
                                        octave=interval.interval_octave,
                                        descending=descending)
            self.res_scale = scale_pitch

            if interval.chromatic_offset <= MAX_SEMITONES_RESOLVE_BELOW:
                begin_to_diatonic = slice(None, interval.diatonic_index + 1)
                resolution_pitch.extend(scale_pitch.scale[begin_to_diatonic])
                if interval.is_chromatic:
                    resolution_pitch.append(interval.note_and_octave)
                resolution_pitch.reverse()
            else:
                diatonic_to_end = slice(interval.diatonic_index, None)
                if interval.is_chromatic:
                    resolution_pitch.append(interval.note_and_octave)
                resolution_pitch.extend(scale_pitch.scale[diatonic_to_end])

            # unisson and octave
            if interval.semitones == 0:
                resolution_pitch.append(scale_pitch.scale[0])

            elif interval.semitones % 12 == 0:
                # FIXME: multipe octaves
                resolution_pitch.append("{}{}".format(tonic,
                                        interval.tonic_octave))

            #for item in resolution_pitch:
            harmonic_seq = [[tonic,x] for x in resolution_pitch]

            sequence_list.append(Sequence(harmonic_seq,
                              duration=self.resolution_duration,
                              delay=self.resolution_delay,
                              pos_delay=self.resolution_pos_delay))

        return sequence_list
