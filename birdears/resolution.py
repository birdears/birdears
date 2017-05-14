from . import MAX_SEMITONES_RESOLVE_BELOW

from .scale import DiatonicScale
from .scale import ChromaticScale

from .sequence import Sequence

class Resolution:

    def __init__(self, method, duration, delay, pos_delay):
        """This class implements methods for different types of question
        resolutions.
        """

        self.METHOD = getattr(self, method)

        self.resolution_duration = duration
        self.resolution_delay = delay
        self.resolution_pos_delay = pos_delay

    def _get_semitones_from_note(self, tonic, note):
        pass

    def resolve(self, *args, **kwargs):
        return self.METHOD(*args, **kwargs)

    def resolve_to_nearest_tonic(self, chromatic, mode, tonic, intervals,
                                 descending=None):

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
            print(resolution_pitch)
            sequence_list.append(Sequence(resolution_pitch,
                              duration=self.resolution_duration,
                              delay=self.resolution_delay,
                              pos_delay=self.resolution_pos_delay))


        # resolution = Sequence(resolution_pitch,
        #                       duration=self.resolution_duration,
        #                       delay=self.resolution_delay,
        #                       pos_delay=self.resolution_pos_delay)

        return sequence_list

    def resolve_to_nearest_tonic_harmonically(self, chromatic, mode, tonic,
                                              intervals, descending=None):

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
            print(resolution_pitch)

            #for item in resolution_pitch:
            harmonic_seq = [[tonic,x] for x in resolution_pitch]

            sequence_list.append(Sequence(harmonic_seq,
                              duration=self.resolution_duration,
                              delay=self.resolution_delay,
                              pos_delay=self.resolution_pos_delay))


        # resolution = Sequence(resolution_pitch,
        #                       duration=self.resolution_duration,
        #                       delay=self.resolution_delay,
        #                       pos_delay=self.resolution_pos_delay)

        return sequence_list
