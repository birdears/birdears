import unittest
import sys
import os

# Ensure src is in path for imports
sys.path.append(os.path.join(os.getcwd(), 'src'))

from birdears.sequence import Sequence
from birdears.note_and_pitch import Pitch

class TestSequenceChordProgression(unittest.TestCase):
    def test_chord_progression_octave(self):
        seq = Sequence()
        tonic = Pitch('C', 4)
        degrees = [1, 4, 5, 1]

        # Test default octave
        seq.make_chord_progression(tonic, 'major', degrees)
        self.assertEqual(seq[0][0].octave, 4, "Default octave should be 4")

        # Clear sequence
        seq[:] = []

        # Test specific octave
        seq.make_chord_progression(tonic, 'major', degrees, octave=3)
        self.assertEqual(seq[0][0].octave, 3, "Octave should be 3")

        # Clear sequence
        seq[:] = []

        # Test another octave
        seq.make_chord_progression(tonic, 'major', degrees, octave=5)
        self.assertEqual(seq[0][0].octave, 5, "Octave should be 5")

        # Clear sequence
        seq[:] = []

        # Test octave 0
        seq.make_chord_progression(tonic, 'major', degrees, octave=0)
        self.assertEqual(seq[0][0].octave, 0, "Octave should be 0")

if __name__ == '__main__':
    unittest.main()
