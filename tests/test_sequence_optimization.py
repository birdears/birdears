
import unittest
from unittest.mock import patch, MagicMock
from birdears.sequence import Sequence
from birdears.note_and_pitch import Pitch, Chord
import sys
import os

# Ensure src is in path for imports
sys.path.append(os.path.join(os.getcwd(), 'src'))

class TestSequenceOptimization(unittest.TestCase):
    @patch('birdears.sequence.subprocess.Popen')
    def test_play_chord_command_construction(self, mock_popen):
        # Setup
        c4 = Pitch('C', 4)
        e4 = Pitch('E', 4)
        g4 = Pitch('G', 4)
        chord = Chord([c4, e4, g4])
        # Force duration/delay to avoid defaults if needed
        chord.duration = 1.0

        sequence = Sequence()
        # We access the private method directly to test it without threading complexity
        sequence._play_chord(chord)

        # Verify
        self.assertTrue(mock_popen.called)
        # Get the arguments passed to Popen. It's called with a list.
        # call_args[0] is the tuple of positional args. call_args[0][0] is the first arg (the command list).
        command_list = mock_popen.call_args[0][0]

        # We expect to see 'pluck', 'C4', 'pluck', 'E4', 'pluck', 'G4' in that order in the list.
        expected_sequence = ['pluck', 'C4', 'pluck', 'E4', 'pluck', 'G4']

        def is_subsequence(sub, main):
            it = iter(main)
            return all(any(x == y for x in it) for y in sub)

        self.assertTrue(is_subsequence(expected_sequence, command_list),
                        f"Expected sequence {expected_sequence} not found in command list: {command_list}")

if __name__ == '__main__':
    unittest.main()
