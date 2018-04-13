from .logger import log_event

from threading import Thread
import subprocess
import time

from .scale import ChromaticScale
from .note_and_pitch import Pitch
from .note_and_pitch import Chord

from .exception import InvalidSequenceElement

SEQUENCE_THREAD = None


class Sequence(list):
    """Register a Sequence of notes and/or chords.

    Attributes:
        elements (array_type): List of notes (strings) ou chords (list of
            strings) in this Sequence.
    """

    @log_event
    def __init__(self, elements=[], duration=2, delay=1.5, pos_delay=1):
        """Inits the Sequence with an array and sets the default times for
            playing / pausing the elements.

        Args:
            elements (array_type): List of elements in this sequence.
                (Pitch'es and/or Chord's)
            duration (float): Default playing time for each element in the
                sequence.
            delay (float): Default waiting time to play the next element
                in the sequence.
            pos_delay (float): Waiting time after playing the last element
                in the sequence.
        """

        if not all(isinstance(element, (Pitch, Chord))
                   for element in elements):
            raise InvalidSequenceElement

        super(Sequence, self).__init__(elements)

        self.duration = duration
        self.delay = delay
        self.pos_delay = pos_delay
        
    @log_event
    def play(self):
        global SEQUENCE_THREAD

        if hasattr(SEQUENCE_THREAD, 'is_alive') and SEQUENCE_THREAD.is_alive():
            try:
                SEQUENCE_THREAD.join()
            except KeyboardInterrupt:
                print('Ctrl+C')
                exit(0)

        # TODO: later we should passa callback and end_callback here so the
        # thread can talk to user interfaces, cli/tui/gui etc
        SEQUENCE_THREAD = Thread(target=self.async_play)
        SEQUENCE_THREAD.start()

        # FIXME: is this really needed? it is a global
        return SEQUENCE_THREAD

    @log_event
    def async_play(self):
        """Plays the Sequence elements of notes and/or chords and wait for
        `Sequence.pos_delay` seconds.
        """

        for element in self:

            # is the current element to be played the last of the sequence?
            # because if it is the last, we will supress it's  playing delay
            # and will use the Sequence.pos_delay
            is_last = element is self[-1]

            if type(element) == Pitch:
                self._play_note(element, last_element=is_last)
            elif type(element) == Chord:
                self._play_chord(element, last_element=is_last)
            else:
                raise InvalidSequenceElement
                
            # TODO we should later get the element information and pass via a
            # dict to Sequence._async_play()'s callback so it can inform the
            # user interfaces on the status of the element current being played
            
        if self.pos_delay:
            self._wait(self.pos_delay)


    # FIXME: implement octave here:
    def make_chord_progression(self, tonic, mode, degrees):
        """Appends triad chord(s) to the Sequence.

        Args:
            tonic (str): Tonic note of the scale.
            mode (str): Mode of the scale from which build the triads upon.
            degrees (array_type): List with integers represending the degrees
                of each triad.
        """

        scale = ChromaticScale(tonic=tonic)

        for degree in degrees:
            triad = scale.get_triad(mode=mode, degree=degree)
            chord = Chord(triad)
            self.append(chord)

    def _play_note(self, pitch, last_element=False):
        """Plays a note.

        Args:
            note (Pitch): The note and octave to be played. Eg.: 'C4'
            duration (float): Duration of the note in seconds.
            delay (float): Delay after the note in seconds.
        """

        # requires sox to be installed

        duration = pitch.duration or self.duration
        delay = pitch.delay or self.delay

        # from sox manual: fade [type] fade-in-length [stop-position(=)
        # [fade-out-length]]
        
        # FIXME: this is experimental, revert to the old code if it is the case
        command = (
            "play -V1 -qn synth {duration} pluck {note}"
            " fade l 0 {duration} {duration} reverb"
        ).format(note=str(pitch), duration=duration)

        subprocess.Popen(command.split())

        if not last_element:
            self._wait(delay)

    def _play_chord(self, chord, last_element=False):
        """Plays a chord.

        Args:
            chord (Chord): An array of pitches (notes and octaves)
                to be played, representing a chord. Eg.: ['C4', 'Eb4', 'G5']
            duration (float): Duration of the chord in seconds.
            delay (float): Delay after the chord in seconds.
        """

        duration = chord.duration or self.duration
        delay = chord.delay or self.delay
        
        chord_plucks = str()
        for note in chord:
            chord_plucks += " pluck {} ".format(note)
        
        # FIXME: this is experimental, revert to the old code if it is the case
        command = (
            "play -V1 -qn synth {duration} {chord}"
            " fade l 0 {duration} {duration} reverb"
        ).format(chord=chord_plucks, duration=duration)

        subprocess.Popen(command.split())

        if not last_element:
            self._wait(delay)

    def _wait(self, seconds):
        """Waits, ie., stops execution for some time.

        Args:
            seconds (float): Seconds to wait.
        """

        time.sleep(seconds)
        