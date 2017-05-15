from . import DIATONIC_MODES
from . import notes2
from . import notes3

from collections import deque


class ScaleBase:
    def __init__(self):
        pass

    def get_triad(self, degree):
        pass

    def _append_octave_to_scale(self, scale, starting_octave, descending=None):
        """Inserts scientific octave number to the notes on a the given scale.
        """

        next_octave = 1 if not descending else -1

        scale_with_octave = []
        changing_note = None

        current_octave = starting_octave

        if not descending:
            for closest in ['C', 'C#', 'Db']:
                if closest in scale:
                    changing_note = closest
                    break
        else:
            for closest in ['B', 'Bb', 'A#']:
                if closest in scale:
                    changing_note = closest
                    break

        for idx, note in enumerate(scale):
            if idx > 0 and note == changing_note:
                current_octave += next_octave

            scale_with_octave.append("{}{}".format(note, current_octave))

        return scale_with_octave

    def _get_chromatic_idx(self, note):
        """Gets the chromatic index, ie., the distance in semitones of a given
        note from C.
        """

        global notes2, notes3

        # use_flat = -1 if (note == 'F' or 'b' in note) else 0

        # FIXME
        if note in notes2:
            note_index = notes2.index(note)
        # elif note in notes3:
        else:
            note_index = notes3.index(note)

        return note_index


class DiatonicScale(ScaleBase):
    """Builds a musical diatonic scale.

    Attributes:
        scale (array_type): The array of notes representing the scale.
    """

    def __init__(self, tonic, mode=None, octave=None, n_octaves=None,
                 descending=None, dont_repeat_tonic=None):
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

        global DIATONIC_MODES

        self.tonic = tonic
        self.mode = mode
        self.octave = octave

        diatonic_mode = DIATONIC_MODES[mode]

        chromatic = ChromaticScale(tonic).scale

        diatonic = [chromatic[semitones] for semitones in diatonic_mode[:-1]]

        if n_octaves:
            diatonic = diatonic * n_octaves

        # FIXME: check if this works on descending
        if not dont_repeat_tonic:
            diatonic.append(chromatic[diatonic_mode[-1]])

        if descending:
            diatonic.reverse()

        if octave:
            diatonic = self._append_octave_to_scale(scale=diatonic,
                                                    starting_octave=octave,
                                                    descending=descending)

        self.scale = diatonic

    def get_triad(self, index=0, degree=None):

        global DIATONIC_MODES

        tonic = self.tonic
        mode = self.mode
        octave = self.octave

        diatonic_mode = DIATONIC_MODES[mode]

        chromatic = ChromaticScale(tonic).scale

        diatonic = [chromatic[semitones] for semitones in diatonic_mode[:-1]]

        #if n_octaves:
        #diatonic = diatonic * n_octaves
        diatonic = diatonic * 2

        # FIXME: check if this works on descending
        diatonic.append(chromatic[diatonic_mode[-1]])

        #if descending:
        #    diatonic.reverse()

        #if octave:
        octave = self.octave or 4
        diatonic = self._append_octave_to_scale(scale=diatonic,
                                                starting_octave=octave,
                                                descending=False)

        self.scale = diatonic
        if degree:
            index = degree - 1

        form = [0, 2, 4]

        triad = [diatonic[index+note] for note in form]

        return triad


class ChromaticScale(ScaleBase):
    def __init__(self, tonic, octave=None, n_octaves=None, descending=None,
                 dont_repeat_tonic=None):
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

        global notes3, notes2

        self.tonic = tonic
        self.octave = octave

        tonic_index = self._get_chromatic_idx(tonic)

        if tonic == 'F' or 'b' in tonic:
            notes = deque(notes3)
        else:
            notes = deque(notes2)

        notes.rotate(-(tonic_index))

        if n_octaves:
            chromatic = notes * n_octaves
        else:
            chromatic = notes

        # FIXME: check if this works on descending
        if not dont_repeat_tonic:
            chromatic.append(chromatic[0])

        if descending:
            chromatic.reverse()

        if octave:
            chromatic = self._append_octave_to_scale(scale=chromatic,
                                                     starting_octave=octave,
                                                     descending=descending)

        self.scale = chromatic

    def get_triad(self, mode, index=0, degree=None):

        global DIATONIC_MODES

        tonic = self.tonic
        octave = self.octave

        diatonic_mode = DIATONIC_MODES[mode]

        chromatic = ChromaticScale(tonic).scale

        diatonic = [chromatic[semitones] for semitones in diatonic_mode[:-1]]

        #if n_octaves:
        #diatonic = diatonic * n_octaves
        diatonic = diatonic * 2

        # FIXME: check if this works on descending
        diatonic.append(chromatic[diatonic_mode[-1]])

        #if descending:
        #    diatonic.reverse()

        #if octave:
        octave = self.octave or 4
        diatonic = self._append_octave_to_scale(scale=diatonic,
                                                starting_octave=octave,
                                                descending=False)

        self.scale = diatonic
        if degree:
            index = degree - 1

        form = [0, 2, 4]

        triad = [diatonic[index+note] for note in form]

        return triad
