
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

        #self.resolution_duration = 2.5
        #self.resolution_delay = 0.5
        #self.resolution_pos_delay = 1

        self.elements = list(elements)

    def append(self, elements):
        self.elements.append(elements)

    def extend(self, elements):
        self.elements.extend(elements)

    def play(self):

        for element in self.elements:
            if type(element) == str:
                self._play_note(element)
            elif type(element) == list:
                self._play_chord(element)


        #tonic = self.concrete_tonic
        #interval = self.interval['note_and_octave']
		#
        #play_note = self._play_note
		#
        #play_note(note=tonic, duration=self.question_duration,
        #          delay=self.question_delay)
        #play_note(note=interval, duration=self.question_duration, delay=0)

        if self.pos_delay:
            self._wait(self.pos_delay)

    def _play_note(self, note, duration, delay):
        # requires sox to be installed

        command = (
            "play -qn synth {duration} pluck {note}"
            " fade l 0 {duration} 2 reverb"
        ).format(note=note, duration=duration)

        subprocess.Popen(command.split())

        if delay:
            self._wait(delay)

    def _play_chord(self, chord, duration, delay):

        for note in chord:
            self._play_note(note, duration=duration, delay=0)

        if delay:
            self._wait(delay)
