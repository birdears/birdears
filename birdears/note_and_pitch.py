from . import CHROMATIC_SHARP
from . import CHROMATIC_FLAT

from .exception import InvalidNote
from .exception import InvalidOctave
from .exception import InvalidPitch

# pitch_numeric_value = (CHROMATIC_NOTE_INDEX+1) * ((OCTAVE+1) * 12)
# eg.: C4 = (0+1) * ((4+1)*12), 1*5 = 61

class Note:

    def __init__(self, note='C'):
        if note in CHROMATIC_SHARP or note in CHROMATIC_FLAT:
            self.note = note
        else:
            raise InvalidNote
            
    def __eq__(self, compare):
        # TODO: think a way to compare pitchs vs strings vs notes

        if type(compare) == str and self.note == compare:
            return True
        elif type(compare) == Note and self == compare:
            return True
        else:
            return False
        
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
            
    def __eq__(self, compare):
        # TODO: think a way to compare pitchs vs strings vs notes
        #if type(compare) == str and self.note == compare:
        #    return True
        #else:
        #    return False
        pass
        
    def __str__(self):
        return "{note}{octave}".format(note=self.note, octave=self.octave)
    
    def __repr__(self):
        return "<Pitch '{note}{octave}'>".format(note=self.note,
               octave=self.octave)
        
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
    
    