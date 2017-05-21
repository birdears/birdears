from random import choice

from . import DIATONIC_MODES

from . import CHROMATIC_TYPE
from . import INTERVALS
from . import MAX_SEMITONES_RESOLVE_BELOW
from . import INTERVAL_INDEX

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
            simple_dict.update({key: getattr(self, key)})

        return simple_dict


class DiatonicInterval(IntervalBase):
    """Chooses a diatonic interval for the question.

    Attributes:
        tonic_octave (int): Scientific octave for the tonic. For example, if
            the tonic is a 'C4' then `tonic_octave` is 4.
        interval octave (int): Scientific octave for the interval. For example,
            if the interval is a 'G5' then `tonic_octave` is 5.
        chromatic_offset (int): The offset in semitones inside one octave.
            Relative semitones to tonic.
        note_and_octave (str): Note and octave of the interval, for example, if
            the interval is G5 the note name is 'G5'.
        note_name (str): The note name of the interval, for example, if the
            interval is G5 then the name is 'G'.
        semitones (int): Semitones from tonic to octave. If tonic is C4 and
            interval is G5 the number of semitones is 19.
        is_chromatic (bool): If the current interval is chromatic (True) or if
            it exists in the diatonic scale which key is tonic.
        is_descending (bool): If the interval has a descending direction, ie.,
            has a lower pitch than the tonic.
        diatonic_index (int): If the interval is chromatic, this will be the
            nearest diatonic interval in the direction of the resolution
            (closest tonic.) From II to IV degrees, it is the ditonic interval
            before; from V to VII it is the diatonic interval after.
        distance (dict): A dictionary which the distance from tonic to
            interval, for example, if tonic is C4 and interval is G5::
                {
                    'octaves': 1,
                    'semitones': 7
                }
        data (tuple): A tuple representing the interval data in the form of
            (semitones, short_name, long_name), for example::
                (19, 'P12', 'Perfect Twelfth')

    Todo:
        * Maybe we should refactor some of the attributes with a tuple
            (note, octave)
        * Maybe remove `chromatic_offset` in favor of `distance['semitones']``
    """

    def __init__(self, mode, tonic, octave, n_octaves=None, descending=None,
                 valid_intervals=None):
        """Inits the class and choses a random interval with the given args.

        Args:
            mode (str): Diatonic mode for the interval.
                (eg.: 'major' or 'minor')
            tonic (str): Tonic of the scale. (eg.: 'Bb')
            octave (str): Scientific octave of the scale (eg.: 4)
            n_octaves (int): Maximum number os octaves (eg. 2)
            descending (bool): Is the interval descending? (default: false)
            valid_intervals (int): A list with intervals (int) valid for random
                choice, 1 is 1st, 2 is second etc.
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

        if not valid_intervals:
            semitones = choice(step_network)
        else:
            valid_network = []
            for item in valid_intervals:
                valid_network.extend(INTERVAL_INDEX[item])
            for i in range(1, n_octaves):
                valid_network.extend([semitones + 12*i for semitones in
                                      valid_network[1:]])
            valid_network = [x for x in valid_network if x in step_network]

            semitones = choice(valid_network)

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

        tonic_concrete = "{}{}".format(tonic, octave)

        interval_data = dict(
            tonic_octave=octave,
            tonic_note_and_octave=tonic_concrete,
            interval_octave=interval_octave,
            chromatic_offset=chromatic_offset,
            note_and_octave=note_and_octave,
            note_name=note_name,
            semitones=semitones,
            is_chromatic=False,
            is_descending=False if not descending else True,
            diatonic_index=diatonic_index,
            distance=distance,
            data=INTERVALS[semitones],
        )

        for item, value in interval_data.items():
            setattr(self, item, value)


class ChromaticInterval(IntervalBase):
    """Chooses a diatonic interval for the question.

    Attributes:
        tonic_octave (int): Scientific octave for the tonic. For example, if
            the tonic is a 'C4' then `tonic_octave` is 4.
        interval octave (int): Scientific octave for the interval. For example,
            if the interval is a 'G5' then `tonic_octave` is 5.
        chromatic_offset (int): The offset in semitones inside one octave;
            maybe it will be deprecated in favour of `distance['semitones']`
            which is the same.
        note_and_octave (str): Note and octave of the interval, for example, if
            the interval is G5 the note name is 'G5'.
        note_name (str): The note name of the interval, for example, if the
            interval is G5 then the name is 'G'.
        semitones (int): Semitones from tonic to octave. If tonic is C4 and
            interval is G5 the number of semitones is 19.
        is_chromatic (bool): If the current interval is chromatic (True) or if
            it exists in the diatonic scale which key is tonic.
        is_descending (bool): If the interval has a descending direction, ie.,
            has a lower pitch than the tonic.
        diatonic_index (int): If the interval is chromatic, this will be the
            nearest diatonic interval in the direction of the resolution
            (closest tonic.) From II to IV degrees, it is the ditonic interval
            before; from V to VII it is the diatonic interval after.
        distance (dict): A dictionary which the distance from tonic to
            interval, for example, if tonic is C4 and interval is G5::
                {
                    'octaves': 1,
                    'semitones': 7
                }
        data (tuple): A tuple representing the interval data in the form of
            (semitones, short_name, long_name), for example::
                (19, 'P12', 'Perfect Twelfth')

    Todo:
        * Maybe we should refactor some of the attributes with a tuple
            (note, octave)
        * Maybe remove `chromatic_offset` in favor of `distance['semitones']``
    """

    def __init__(self, mode, tonic, octave, n_octaves=None, descending=None,
                 valid_intervals=None):
        """Inits the class and choses a random interval with the given args.

        Args:
            mode (str): Diatonic mode for the interval.
                (eg.: 'major' or 'minor')
            tonic (str): Tonic of the scale. (eg.: 'Bb')
            octave (str): Scientific octave of the scale (eg.: 4)
            interval (str): Not implemented. The interval.
            chromatic (bool): Can have chromatic notes? (eg.: F# in a key
                of C; default: false)
            n_octaves (int): Maximum number os octaves (eg. 2)
            descending (bool): Is the interval descending? (default: false)
            valid_intervals (int): A list with inervals valid for random
                choice, 1 is 1st, 2 is second etc.
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

        # semitones = choice(chromatic_network)
        if not valid_intervals:
            semitones = choice(chromatic_network)
        else:
            valid_network = []
            for item in valid_intervals:
                valid_network.extend(INTERVAL_INDEX[item])
            for i in range(1, n_octaves):
                valid_network.extend([semitones + 12*i for semitones in
                                      valid_network])

            semitones = choice(valid_network)

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

        tonic_concrete = "{}{}".format(tonic, octave)

        interval_data = dict(
            tonic_octave=octave,
            tonic_note_and_octave=tonic_concrete,
            interval_octave=interval_octave,
            chromatic_offset=chromatic_offset,
            note_and_octave=note_and_octave,
            note_name=note_name,
            semitones=semitones,
            is_chromatic=is_chromatic,
            is_descending=False if not descending else True,
            diatonic_index=diatonic_index,
            distance=distance,
            data=INTERVALS[semitones],
        )

        for item, value in interval_data.items():
            setattr(self, item, value)
