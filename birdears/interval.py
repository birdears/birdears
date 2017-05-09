from random import choice

from . import DIATONIC_MODES

from . import CHROMATIC_TYPE
from . import INTERVALS
from . import MAX_SEMITONES_RESOLVE_BELOW

from .scale import DiatonicScale
from .scale import ChromaticScale


class Interval:

    def __init__(self, mode, tonic, octave, chromatic=None, n_octaves=None,
                 descending=None):
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
            Is the interval dewcending? (default: false)
        """

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

        if not chromatic:
            semitones = choice(step_network)
        else:
            semitones = choice(chromatic_network)

        chromatic_scale = ChromaticScale(tonic=tonic, octave=None,
                                         n_octaves=n_octaves,
                                         descending=descending)

        chromatic_scale_pitch = ChromaticScale(tonic=tonic, octave=octave,
                                               n_octaves=n_octaves,
                                               descending=descending)

        distance = dict({
            'octaves': 0 if (semitones < 12) else int(semitones / 12),
            'semitones': semitones if (semitones < 12) else int(semitones % 12)
        })
        # chromatic_offset = semitones if semitones < 12 else semitones % 12
        chromatic_offset = distance['semitones']

        note_name = "{}".format(chromatic_scale.scale[semitones])
        note_and_octave = "{}".format(chromatic_scale_pitch.scale[semitones])

        is_chromatic = True if chromatic_offset not in diatonic_mode else False

        if is_chromatic:
            # here we are rounding it to the next diatonic degree, to insert
            # it after:
            if chromatic_offset <= MAX_SEMITONES_RESOLVE_BELOW:
                diatonic_index = diatonic_mode.index(chromatic_offset - 1)
            else:
                diatonic_index = diatonic_mode.index(chromatic_offset + 1)
        else:
            diatonic_index = diatonic_mode.index(chromatic_offset)

        if not descending:
            interval_octave = int(octave) + distance['octaves']
        else:
            interval_octave = int(octave) - distance['octaves']

        self.interval_data = dict({
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
