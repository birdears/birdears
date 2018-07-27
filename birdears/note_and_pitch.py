from . import CHROMATIC_SHARP
from . import CHROMATIC_FLAT

from .exception import InvalidNote
from .exception import InvalidOctave
from .exception import InvalidPitch

# pitch_numeric_value = (PITCH_CLASS) + (OCTAVE * 12)
# eg.: C4 == (0) + (4*12), == 60


def get_pitch_class(note):
    if note in CHROMATIC_SHARP:
        pitch_class = CHROMATIC_SHARP.index(note)
    elif note in CHROMATIC_FLAT:
        pitch_class = CHROMATIC_FLAT.index(note)
    else:
        raise InvalidNote

    return pitch_class


def get_pitch_number(note, octave):
    pitch_number = get_pitch_class(note) + (octave * 12)
    return pitch_number


def get_pitch_by_number(numeric, accident='sharp'):

    octave, pitch_class = divmod(numeric, 12)

    if accident == 'sharp':
        note = CHROMATIC_SHARP[pitch_class]
    elif accident == 'flat':
        note = CHROMATIC_FLAT[pitch_class]
    else:
        raise Exception('accident should be \'sharp\' or \'flat\'')

    pitch = Pitch(note=note, octave=octave, accident=accident)

    return pitch


def get_abs_chromatic_offset(pitch1, pitch2):
    if not all(isinstance(element, Pitch) for element in [pitch1, pitch2]):
        raise InvalidPitch

    offset = abs(int(pitch1) - int(pitch2)) % 12

    return offset


class Note:

    def __init__(self, note='C', accident='sharp'):

        if note in CHROMATIC_SHARP or note in CHROMATIC_FLAT:
            self.note = note
        else:
            raise InvalidNote()

        if accident in ('sharp', 'flat'):
            self.accident = accident
        else:
            raise Exception('\'accident\' should be \'sharp\' or \'flat\'')

    # https://en.wikipedia.org/wiki/Pitch_class
    @property
    def pitch_class(self):
        if self.note in CHROMATIC_SHARP:
            value = CHROMATIC_SHARP.index(self.note)
        else:
            value = CHROMATIC_FLAT.index(self.note)

        return value

    def __eq__(self, compare):
        # TODO: think a way to compare pitchs vs strings vs notes

        # FIXME: we should use isinstance() here
        if type(compare) == str and str(self) == compare:
            return True

        elif type(compare) == Note and int(self) == int(compare):
            return True

        elif type(compare) == Pitch and int(self) == int(compare):
            return True


        return False

    def __int__(self):
        return self.pitch_class

    def __str__(self):
        return str(self.note)

    def __repr__(self):
        return "<Note '{note}'>".format(note=self.note)


# https://en.wikipedia.org/wiki/Scientific_pitch_notation
class Pitch(Note):

    duration = None
    delay = None

    def __init__(self, note='C', octave=4, accident='sharp'):
        super(Pitch, self).__init__(note=note, accident=accident)

        if octave >= 0 and octave <= 9:
            self.octave = octave
        else:
            raise InvalidOctave

    @property
    def pitch_number(self):
        value = self.pitch_class + (self.octave * 12)
        return value

    def distance(self, other):
        if isinstance(other, (Pitch, int)):
            return self.pitch_number - int(other)

    def __eq__(self, compare):

        if isinstance(compare, (Note, Pitch, int)):
            return self.pitch_number == int(compare)
        else:
            raise Exception('Invalid operand for comparison.')

    def __gt__(self, other):
        return self.pitch_number > int(other)

    def __ge__(self, other):
        return self.pitch_number >= int(other)

    def __lt__(self, other):
        return self.pitch_number < int(other)

    def __le__(self, other):
        return self.pitch_number <= int(other)

    def __str__(self):
        return "{note}{octave}".format(note=self.note, octave=self.octave)

    def __int__(self):
        return self.pitch_number

    def __repr__(self):
        return "<Pitch '{note}{octave}' ({numeric})>" \
            .format(note=self.note, octave=self.octave,
                    numeric=self.pitch_number)

    def __add__(self, other):

        if isinstance(other, int):
            result = self.pitch_number + int(other)

        return get_pitch_by_number(result, accident=self.accident)

    def __iadd__(self, other):

        if isinstance(other, int):
            result = self.pitch_number + int(other)

        return get_pitch_by_number(result, accident=self.accident)

        # if isinstance(other, int):
        #    pitch_number = self.pitch_number + other
        #    pitch = Pitch().get_pitch_by_number(pitch_number)
        #else:
        #    raise Exception('Invalid operand for addition.')

        #return pitch

    def __sub__(self, other):

        if isinstance(other, int):
            result = self.pitch_number - int(other)

            return get_pitch_by_number(result, accident=self.accident)

    def __isub__(self, other):

        if isinstance(other, int):
            result = self.pitch_number - int(other)

            return get_pitch_by_number(result, accident=self.accident)


class Chord(list):

    duration = None
    delay = None

    def __init__(self, iterable):
        if not all(isinstance(element, Pitch) for element in iterable):
            raise InvalidPitch
        # else:
        super(Chord, self).__init__(iterable)

    def append(self, obj):
        if not isinstance(obj, Pitch):
            raise InvalidPitch
        # else:
        super(Chord, self).append(obj)

    def extend(self, iterable):
        if not all(isinstance(element, Pitch) for element in iterable):
            raise InvalidPitch
        # else:
        super(Chord, self).extend(iterable)
