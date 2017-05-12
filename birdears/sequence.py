import subprocess
import time


class Sequence:
    def __init__(self, elements, duration=2, delay=1.5, pos_delay=1):
        """Sequence of notes or chords.

        Parameters
        ----------
        elements : array_type
            List of elements in this sequence. (notes or chords)
        duration : float
            Default duratin playing time for each element in the sequence.
        delay : float
            Default waiting time to play the next element in the sequence.
        pos_delay : float
            Waiting time after playing the last element in the sequence.
        """

        self.duration = duration
        self.delay = delay
        self.pos_delay = pos_delay

        self.elements = list(elements)

    def append(self, elements):
        self.elements.append(elements)

    def extend(self, elements):
        self.elements.extend(elements)

    def play(self):

        last_idx = len(self.elements) - 1

        for cur_idx,element in enumerate(self.elements):

            # lets leave the last element's delay for pos_delay:
            delay = self.delay if cur_idx != last_idx else 0

            if type(element) == str:
                self._play_note(element,delay=delay)
            elif type(element) == list:
                self._play_chord(element, delay=delay)

        if self.pos_delay:
            self._wait(self.pos_delay)

    def _play_note(self, note, duration=None, delay=None):
        # requires sox to be installed

        duration = self.duration if duration is None else duration
        delay = self.delay if delay is None else delay

        command = (
            "play -qn synth {duration} pluck {note}"
            " fade l 0 {duration} 2 reverb"
        ).format(note=note, duration=duration)

        subprocess.Popen(command.split())

        if delay:
            self._wait(delay)

    def _play_chord(self, chord, duration=None, delay=None):

        duration = self.duration if duration is None else duration
        delay = self.delay if delay is None else delay

        for note in chord:
            self._play_note(note, duration=duration, delay=0)

        if delay:
            self._wait(delay)

    def _wait(self, seconds):
        time.sleep(seconds)
