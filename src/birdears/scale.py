from . import DIATONIC_FORMS

from .note_and_pitch import Pitch
from .note_and_pitch import Chord
from .note_and_pitch import get_pitch_by_number

from itertools import cycle

# https://docs.python.org/3/reference/datamodel.html#emulating-container-types


class ScaleBase(list):
    def __init__(self):
        pass


class DiatonicScale(ScaleBase):
    """Builds a musical diatonic scale.

    Attributes:
        scale (array_type): The array of notes representing the scale.
    """

    def __init__(self, tonic='C', mode='major', octave=4, n_octaves=1,
                 descending=False, dont_repeat_tonic=False):
        """Returns a diatonic scale from tonic and mode.

        Args:
            tonic (str): The note which the scale will be built upon.
            mode (str): The mode the scale will be built upon.
                ('major' or 'minor')
            octave (int): The scientific octave the scale will be built upon.
            n_octaves (int): The number of octaves the scale will contain.
            descending (bool): Whether the scale is descending.
            dont_repeat_tonic (bool): Whether to skip appending the last
                note (octave) to the scale.
        """

        super(DiatonicScale, self).__init__()

        self.tonic = Pitch(note=tonic, octave=octave)
        self.mode = mode
        self.direction = "Ascending" if not descending else "Descending"
        self.is_descending = descending
        self.n_octaves = n_octaves

        diatonic_mode = DIATONIC_FORMS[mode]

        form_length = len(diatonic_mode)

        direction = +1 if not descending else -1
        repeat_tonic = 0 - dont_repeat_tonic  # 0 (repeat) or -1
        if descending:
            diatonic_mode = diatonic_mode[::-1]

        diatonic_loop = cycle(diatonic_mode)

        scale = list()

        self.append(self.tonic)

        pitch_num = int(self[0])

        accident = ('flat' if (('b' in tonic) or (tonic == 'F'))
                    else 'sharp')

        for i in range((form_length * n_octaves) + repeat_tonic):
            step = next(diatonic_loop)

            pitch_num += step * direction

            pitch = get_pitch_by_number(numeric=pitch_num, accident=accident)
            scale.append(pitch)

        self.extend(scale)

    def __repr__(self):

        repr = "<DiatonicScale {tonic} {mode} {direction} {first}-{to} " \
               "({octaves} octaves)>" \
                   .format(tonic=str(self[0].note),
                           mode=self.mode.capitalize(),
                           direction=self.direction.capitalize(),
                           first=str(self[0]),
                           to=str(self[-1]), octaves=int(len(self)/8))
        return repr

    def __str__(self):
        return str(list(self))


class ChromaticScale(ScaleBase):
    """Builds a musical chromatic scale.

    Attributes:
        scale (array_type): The array of notes representing the scale.
    """

    def __init__(self, tonic='C', octave=4, n_octaves=1, descending=False,
                 dont_repeat_tonic=False):
        """Returns a chromatic scale from tonic.

        Args:
            tonic (str): The note which the scale will be built upon.
            octave (int): The scientific octave the scale will be built upon.
            n_octaves (int): The number of octaves the scale will contain.
            descending (bool): Whether the scale is descending.
            dont_repeat_tonic (bool): Whether to skip appending the last
                note (octave) to the scale.
        """

        super(ChromaticScale, self).__init__()

        # global CHROMATIC_SHARP, CHROMATIC_FLAT

        self.tonic = Pitch(tonic, octave)
        self.direction = "Ascending" if not descending else "Descending"
        self.is_descending = descending
        self.n_octaves = n_octaves

        direction = +1 if not descending else -1

        tonic_pitch_num = int(self.tonic)
        repeat_tonic = not dont_repeat_tonic  # 1 or 0

        accident = 'flat' if (('b' in tonic) or (tonic == 'F')) else 'sharp'

        scale = [get_pitch_by_number(numeric=tonic_pitch_num + (i*direction),
                                     accident=accident)
                 for i in range((12 * n_octaves) + repeat_tonic)]

        self.extend(scale)


def get_triad(tonic, mode, index=0, degree=None):
    """Returns an array with notes from a scale's triad.

    Args:
        tonic (Pitch): The tonic pitch of the scale.
        mode (str): Mode of the scale (eg. 'major' or 'minor')
        index (int): Triad index (eg.: 0 for 1st degree triad.)
        degree (int): Degree of the scale. If provided, overrides the
            `index` argument. (eg.: `1` for the 1st degree triad.)
    Returns:
        An array with three pitches, one for each note of the triad.
    """

    diatonic = DiatonicScale(tonic=tonic.note, mode=mode,
                             octave=tonic.octave, n_octaves=2,
                             descending=False, dont_repeat_tonic=False)

    if degree:
        index = degree - 1

    form = [0, 2, 4]

    triad = [diatonic[index+note] for note in form]

    chord = Chord(triad)

    return chord
