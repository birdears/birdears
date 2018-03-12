from . import CHROMATIC_SHARP
from . import CHROMATIC_FLAT

class Note:

    def __init__(self, note):
        if note in CHROMATIC_SHARP or note in CHROMATIC_FLAT:
            self.note = note
            
    def __eq__(self, compare):
        if type(compare) == str and self.note == compare:
            return True
        else:
            return False
        
    def __str__(self):
        return str(self.note)

class Pitch(Note):

    def __init__(self, note, octave):
        super(Pitch, self).__init__(note=note)
        # self.note = note
        # TODO: validate octave
        self.octave = octave
