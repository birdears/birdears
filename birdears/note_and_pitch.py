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

# FIXME: maybe move this somewhere else
def get_pitch_by_number(numeric, accident='sharp'):
    octave, pitch_class  = divmod(numeric, 12)
    
    note = CHROMATIC_SHARP[pitch_class] if accident == 'sharp' \
            else CHROMATIC_FLAT[pitch_class]
    
    pitch = Pitch(note=note, octave=octave)
    
    return pitch

class Note:

    def __init__(self, note='C'):
        if note in CHROMATIC_SHARP or note in CHROMATIC_FLAT:
            self.note = note
        else:
            raise InvalidNote

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
    
    def __init__(self, note='C', octave=4):
        super(Pitch, self).__init__(note=note)

        if octave >= 0 and octave <= 9:
            self.octave = octave
        else:
            raise InvalidOctave
        
    @property
    def pitch_number(self):
        value = self.pitch_class + (self.octave * 12)
        return value
    
    # FIXME: maybe move this somewhere else
    def get_pitch_by_number(self, numeric, accident='sharp'):
        octave, pitch_class  = divmod(numeric, 12)
        
        note = CHROMATIC_SHARP[pitch_class] if accident == 'sharp' \
                else CHROMATIC_FLAT[pitch_class]
        
        pitch = Pitch(note=note, octave=octave)
        
        return pitch
    
    def distance(self, other):
        if type(other) == Pitch:
            return self.pitch_number - int(other)
            
    def __eq__(self, compare):
        
        if type(compare) == int:
            result = self.pitch_number == compare
            
        elif type(compare) == Pitch:
            result = self.pitch_number == int(compare)
            
        elif type(compare) == Note:
            result = self.pitch_class == int(compare)        
        
        else:
            raise Exception('Invalid operand for addition.')
        
        return result
        
    def __str__(self):
        return "{note}{octave}".format(note=self.note, octave=self.octave)
    
    def __int__(self):
        return self.pitch_number
    
    def __repr__(self):
        return "<Pitch '{note}{octave}' ({numeric})>" \
            .format(note=self.note, octave=self.octave,
                    numeric=self.pitch_number)
            
    def __add__(self, other):
        if type(other) == int:
            pitch_number = self.pitch_number + other
            pitch = Pitch().get_pitch_by_number(pitch_number)
        else:
            raise Exception('Invalid operand for addition.')
        return pitch

    def __iadd__(self, other):
        if type(other) == int:
            pitch_number = self.pitch_number + other
            pitch = Pitch().get_pitch_by_number(pitch_number)
        else:
            raise Exception('Invalid operand for addition.')
            
        return pitch
            
    def __sub__(self, other):
        if type(other) == int:
            pitch_number = self.pitch_number - other
            pitch = Pitch().get_pitch_by_number(pitch_number)
        
        #elif type(other) == Pitch:
        #    pitch_number = self.pitch_number - int(other)
        #    pitch = Pitch().get_pitch_by_number(pitch_number)
        
        else:
            raise Exception('Invalid operand for subtraction.')
        
        return pitch
    
    def __isub__(self, other):
        if type(other) == int:
            pitch_number = self.pitch_number - other
            pitch = Pitch().get_pitch_by_number(pitch_number)
        else:
            raise Exception('Invalid operand for subtraction.')
            
        return pitch
        
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
    
    