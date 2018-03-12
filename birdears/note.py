from .. import CHROMATIC_SHARP
from .. import CHROMATIC_FLAT

class Note:

    def __init__(self, note):
        if note in CHROMATIC_SHARP or note in CHROMATIC_FLAT:
            self.note = note
