from random import choice

from . import DIATONIC_MODES

from . import CHROMATIC_TYPE
from . import INTERVALS
from . import MAX_SEMITONES_RESOLVE_BELOW

#from .scale import DiatonicScale
from .scale import ChromaticScale

class IntervalBase:

    def __init__(self):
        """Base class for interval classes.
        """

        pass

    def return_simple(self, keys):
        """This method returns a dict with only the values passed to `keys`.
        """

        simple_dict = dict()

        for key in keys:
            simple_dict.update({ key : getattr(self, key) })

        return simple_dict


class DiatonicInterval(IntervalBase):

    def __init__(self, mode, tonic, octave, n_octaves=None, descending=None):
        """Chooses a diatonic interval for the question.

        Parameters
        ----------
        mode : str
            Diatonic mode for the interval. (eg.: 'major' or 'minor')
        tonic : str
            Tonic of the scale. (eg.: 'Bb')
        octave : str
            Scientific octave of the scale (eg.: 4)
        interval : str
            Not implemented. The interval.
        n_octaves : int
            Maximum number os octaves (eg. 2)
        descending : bool
            Is the interval descending? (default: false)
        """

        super(DiatonicInterval, self).__init__()

        global DIATONIC_MODES, CHROMATIC_TYPE, MAX_SEMITONES_RESOLVE_BELOW
        global INTERVALS

        diatonic_mode = list(DIATONIC_MODES[mode])
        chromatic_network = list(CHROMATIC_TYPE)

        if descending:
            # TODO: use list( map(lambda x: 12-x, diatonic_mode) ) here
            diatonic_mode = [12 - x for x in diatonic_mode]
            diatonic_mode.reverse()

        step_network = diatonic_mode

        # FIXME: please refactore this with method signature n_octaves=1:
        if n_octaves:
            for i in range(1, n_octaves):
                step_network.extend([semitones + 12 * i for semitones in
                                     diatonic_mode[1:]])
                chromatic_network.extend([semitones + 12 * i for semitones in
                                          CHROMATIC_TYPE[1:]])

        semitones = choice(step_network)

        chromatic_scale = ChromaticScale(tonic=tonic, octave=None,
                                         n_octaves=n_octaves,
                                         descending=descending)

        chromatic_scale_pitch = ChromaticScale(tonic=tonic, octave=octave,
                                               n_octaves=n_octaves,
                                               descending=descending)

        octaves, chromatic_offset = divmod(semitones, 12)
        distance = dict(octaves=octaves, semitones=chromatic_offset)

        note_name = "{}".format(chromatic_scale.scale[semitones])
        note_and_octave = "{}".format(chromatic_scale_pitch.scale[semitones])

        diatonic_index = diatonic_mode.index(chromatic_offset)

        if not descending:
            interval_octave = int(octave) + distance['octaves']
        else:
            interval_octave = int(octave) - distance['octaves']

        # these will be written to self
        interval_data = dict({
            'tonic_octave': octave,
            'interval_octave': interval_octave,
            'chromatic_offset': chromatic_offset,
            'note_and_octave': note_and_octave,
            'note_name': note_name,
            'semitones': semitones,
            'is_chromatic': False,
            'is_descending': False if not descending else True,
            'diatonic_index': diatonic_index,
            'distance': distance,
            'data': INTERVALS[semitones],
        })

        for item, value in interval_data.items():
            setattr(self, item, value)


class ChromaticInterval(IntervalBase):

    def __init__(self, mode, tonic, octave, n_octaves=None, descending=None):
        """Chooses a chromatic interval for the question.

        Parameters
        ----------
        mode : str
            Diatonic mode for the interval. (eg.: 'major' or 'minor')
        tonic : str
            Tonic of the scale. (eg.: 'Bb')
        octave : str
            Scientific octave of the scale (eg.: 4)
        interval : str
            Not implemented. The interval.
        chromatic: bool
            Can have chromatic notes? (eg.: F# in a key of C; default: false)
        n_octaves : int
            Maximum number os octaves (eg. 2)
        descending : bool
            Is the interval descending? (default: false)
        """

        super(ChromaticInterval, self).__init__()

        global DIATONIC_MODES, CHROMATIC_TYPE, MAX_SEMITONES_RESOLVE_BELOW
        global INTERVALS

        diatonic_mode = list(DIATONIC_MODES[mode])
        chromatic_network = list(CHROMATIC_TYPE)

        if descending:
            # TODO: use list( map(lambda x: 12-x, diatonic_mode) ) here
            diatonic_mode = [12 - x for x in diatonic_mode]
            diatonic_mode.reverse()

        step_network = diatonic_mode

        # FIXME: please refactore this with method signature n_octaves=1:
        if n_octaves:
            for i in range(1, n_octaves):
                step_network.extend([semitones + 12 * i for semitones in
                                     diatonic_mode[1:]])
                chromatic_network.extend([semitones + 12 * i for semitones in
                                          CHROMATIC_TYPE[1:]])

        semitones = choice(chromatic_network)

        chromatic_scale = ChromaticScale(tonic=tonic, octave=None,
                                         n_octaves=n_octaves,
                                         descending=descending)

        chromatic_scale_pitch = ChromaticScale(tonic=tonic, octave=octave,
                                               n_octaves=n_octaves,
                                               descending=descending)

        octaves, chromatic_offset = divmod(semitones, 12)
        distance = dict(octaves=octaves, semitones=chromatic_offset)

        note_name = "{}".format(chromatic_scale.scale[semitones])
        note_and_octave = "{}".format(chromatic_scale_pitch.scale[semitones])

        is_chromatic = True if chromatic_offset not in diatonic_mode else False

        if is_chromatic and chromatic_offset <= MAX_SEMITONES_RESOLVE_BELOW:
            diatonic_index = diatonic_mode.index(chromatic_offset - 1)
        elif is_chromatic and chromatic_offset > MAX_SEMITONES_RESOLVE_BELOW:
            diatonic_index = diatonic_mode.index(chromatic_offset + 1)
        else:
            diatonic_index = diatonic_mode.index(chromatic_offset)

        if not descending:
            interval_octave = int(octave) + distance['octaves']
        else:
            interval_octave = int(octave) - distance['octaves']

        # these will be written to self
        interval_data = dict({
            'tonic_octave': octave,
            'interval_octave': interval_octave,
            'chromatic_offset': chromatic_offset,
            'note_and_octave': note_and_octave,
            'note_name': note_name,
            'semitones': semitones,
            'is_chromatic': is_chromatic,
            'is_descending': False if not descending else True,
            'diatonic_index': diatonic_index,
            'distance': distance,
            'data': INTERVALS[semitones],
        })

        for item, value in interval_data.items():
            setattr(self, item, value)
