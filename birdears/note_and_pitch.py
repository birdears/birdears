from . import CHROMATIC_SHARP
from . import CHROMATIC_FLAT

class Note:

    def __init__(self, note='C'):
        if note in CHROMATIC_SHARP or note in CHROMATIC_FLAT:
            self.note = note
        else:
            raise Exception('Invalid note name.')
            
    def __eq__(self, compare):
        # TODO: think a way to compare pitchs vs strings vs notes

        if type(compare) == str and self.note == compare:
            return True
        elif type(compare) == type(self) and self == compare:
            return True
        else:
            return False
        
    def __str__(self):
        return str(self.note)
    
    def __repr__(self):
        return "<Note '{note}'>".format(note=self.note)

# https://en.wikipedia.org/wiki/Scientific_pitch_notation
class Pitch(Note):

    def __init__(self, note='C', octave=4):
        super(Pitch, self).__init__(note=note)

        if octave >= 0 and octave <= 9:
            self.octave = octave
        else:
            raise Exception('Invalid octave number.')
            
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