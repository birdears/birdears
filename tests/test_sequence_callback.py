import unittest
from unittest.mock import MagicMock, patch
from birdears.sequence import Sequence
from birdears.note_and_pitch import Pitch, Chord
import time

class TestSequenceCallback(unittest.TestCase):
    def test_async_play_callback_receives_dict(self):
        # Create a sequence with two elements
        elements = [Pitch('C', 4), Pitch('E', 4)]
        seq = Sequence(elements, duration=0.5, delay=0.1)

        # Mock callback
        callback = MagicMock()

        # Mock _play_note so we don't actually play sound or subprocess
        with patch.object(Sequence, '_play_note', return_value=None):
            # Play sequence
            # We need to wait for the thread to finish
            thread = seq.play(callback=callback)
            thread.join()

        # Verify callback was called twice
        self.assertEqual(callback.call_count, 2)

        # Verify first call arguments
        # args[0] is the first positional argument passed to callback
        call_args_list = callback.call_args_list

        # First call
        first_call_args = call_args_list[0][0][0]
        self.assertIsInstance(first_call_args, dict, "Callback should receive a dictionary")
        self.assertEqual(first_call_args['element'], elements[0])
        self.assertEqual(first_call_args['index'], 0)
        self.assertEqual(first_call_args['duration'], 0.5)
        self.assertEqual(first_call_args['delay'], 0.1)
        self.assertFalse(first_call_args['is_last'])

        # Second call
        second_call_args = call_args_list[1][0][0]
        self.assertIsInstance(second_call_args, dict, "Callback should receive a dictionary")
        self.assertEqual(second_call_args['element'], elements[1])
        self.assertEqual(second_call_args['index'], 1)
        self.assertEqual(second_call_args['duration'], 0.5)
        self.assertEqual(second_call_args['delay'], 0.1)
        self.assertTrue(second_call_args['is_last'])

if __name__ == '__main__':
    unittest.main()
