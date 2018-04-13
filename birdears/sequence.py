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
                (notes or chords)
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

        # for el in elements:
        #    if type(el) != Pitch and type(el) != list:
        #        raise InvalidSequenceElement

        # self.extend(list(elements))
        
        self.index = 0
        self.last_idx = len(self) - 1

    @log_event
    def play(self, callback=None, end_callback=None):
        global SEQUENCE_THREAD
        # callback = print

        if hasattr(SEQUENCE_THREAD, 'is_alive') and SEQUENCE_THREAD.is_alive():
            try:
                SEQUENCE_THREAD.join()
            except KeyboardInterrupt:
                print('Ctrl+C')
                exit(0)

        SEQUENCE_THREAD = Thread(target=self.async_play,
                                 kwargs={
                                    'callback': callback,
                                    'end_callback': end_callback
                                 })

        SEQUENCE_THREAD.start()

        return SEQUENCE_THREAD

    @log_event
    def async_play(self, callback, end_callback):
        """Plays the Sequence elements of notes and/or chords and wait for
        `Sequence.pos_delay` seconds.
        """

        # last_idx = len(self.elements) - 1
        last_idx = len(self) - 1

        for cur_idx, element in enumerate(self):

            is_last = False if cur_idx != last_idx else True

            # lets leave the last element's delay for pos_delay:
            delay = self.delay if not is_last else 0

            if type(element) == tuple:
                el, duration, delay = element
            else:
                el = element

            current_data = dict(
                index=cur_idx,
                element=el,
                delay=delay,
                is_last=is_last,
            )

            if callback:
                callback(current_data)

            if type(el) == Pitch:
                self._play_note(el, delay=delay)
            # FIXME: remove 'str' as an allowed type:
            #elif type(el) == str:
            #    self._play_note(el, delay=delay)
            elif type(el) == list:
                self._play_chord(el, delay=delay)
            else:
                raise Exception

        if self.pos_delay:
            self._wait(self.pos_delay)

        if end_callback:
            end_callback()

    def play_element(self, index):
        """Plays element `Sequence[index].`
        """

        element = self[index]

        delay = self.delay

        if type(element) == tuple:
            el, duration, delay = element
        else:
            el = element
            
        if type(el) == Pitch:
            self._play_note(el, delay=delay)
        elif type(el) == list:
            self._play_chord(el, delay=delay)
        else:
            raise InvalidSequenceElement

        #  if self.pos_delay:
        #     self._wait(self.pos_delay)

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
            self.append(triad)

    def _async_play_note(self, note, duration=None, delay=None):
        """Plays a note.

        Args:
            note (str): The note and octave to be played. Eg.: 'C4'
            duration (float): Duration of the note in seconds.
            delay (float): Delay after the note in seconds.
        """

        # requires sox to be installed

        duration = self.duration if duration is None else duration
        delay = self.delay if delay is None else delay

        command = (
            "play -V1 -qn synth {duration} pluck {note}"
            " fade l 0 {duration} 2 reverb"
        ).format(note=note, duration=duration)

        subprocess.Popen(command.split())

        if delay:
            self._wait(delay)

    def _async_play_chord(self, chord, duration=None, delay=None):
        """Plays a chord.

        Args:
            chord (array_type): An array of pitches (notes and octaves)
                to be played, representing a chord. Eg.: ['C4', 'Eb4', 'G5']
            duration (float): Duration of the chord in seconds.
            delay (float): Delay after the chord in seconds.
        """

        duration = self.duration if duration is None else duration
        delay = self.delay if delay is None else delay

        chord_plucks = str()
        for note in chord:
            chord_plucks += " pluck {note} ".format(note=str(note))

        command = (
            "play -V1 -qn synth {duration} {chord_plucks}"
            " fade l 0 {duration} 2 reverb"
        ).format(duration=duration, chord_plucks=chord_plucks)
        # command = (
        #    "play -V1 -qn synth {duration} {chord}"
        #    " fade l 0 {duration} 2 reverb"
        #).format(note=note, duration=duration, chord=chord_plucks)

        subprocess.Popen(command.split())

        if delay:
            self._wait(delay)

    def _async_wait(self, seconds):
        """Waits, ie., stops execution for some time.

        Args:
            seconds (float): Seconds to wait.
        """

        time.sleep(seconds)

    def _play_note(self, note, duration=None, delay=None):
        """Plays a note.

        Args:
            note (str): The note and octave to be played. Eg.: 'C4'
            duration (float): Duration of the note in seconds.
            delay (float): Delay after the note in seconds.
        """

        # requires sox to be installed

        duration = self.duration if duration is None else duration
        delay = self.delay if delay is None else delay

        # double_duration = str(int(duration)*2)
        
        # from sox manual: fade [type] fade-in-length [stop-position(=) [fade-out-length]]
        # TODO: this is experimental
        command = (
            "play -V1 -qn synth {duration} pluck {note}"
            " fade l 0 {duration} {duration} reverb"
        ).format(note=str(note), duration=duration)
        # command = (
        #    "play -V1 -qn synth {duration} pluck {note}"
        #    " fade l 0 {duration} 2 reverb"
        # ).format(note=note, duration=duration)

        subprocess.Popen(command.split())

        if delay:
            self._wait(delay)

    def _play_chord(self, chord, duration=None, delay=None):
        """Plays a chord.

        Args:
            chord (array_type): An array of pitches (notes and octaves)
                to be played, representing a chord. Eg.: ['C4', 'Eb4', 'G5']
            duration (float): Duration of the chord in seconds.
            delay (float): Delay after the chord in seconds.
        """

        duration = self.duration if duration is None else duration
        delay = self.delay if delay is None else delay

        chord_plucks = str()
        for note in chord:
            chord_plucks += " pluck {} ".format(note)

        double_duration = str(int(duration)*2)

        # from sox manual: fade [type] fade-in-length [stop-position(=) [fade-out-length]]
        # TODO: this is experimental
        command = (
            "play -V1 -qn synth {duration} {chord}"
            " fade l 0 {duration} {duration} reverb"
        ).format(chord=chord_plucks, duration=duration)
        #command = (
        #    "play -V1 -qn synth {duration} {chord}"
        #    " fade l 0 {duration} 2 reverb"
        #).format(note=note, duration=duration, chord=chord_plucks)

        subprocess.Popen(command.split())

        if delay:
            self._wait(delay)

    def _wait(self, seconds):
        """Waits, ie., stops execution for some time.

        Args:
            seconds (float): Seconds to wait.
        """

        time.sleep(seconds)