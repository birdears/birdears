from .note import Note

class Pitch(Note):

    def __init__(self, note, pitch):
        self.note = note
        self.pitch = pitch
