from random import choice

from . import DIATONIC_MODES

from . import CHROMATIC_TYPE
from . import INTERVALS
from . import MAX_SEMITONES_RESOLVE_BELOW
from . import INTERVAL_INDEX

from .scale import ChromaticScale

 
class Interval(dict):
    """Chooses a diatonic interval for the question.

    Attributes:
        tonic_octave (int): Scientific octave for the tonic. For example, if
            the tonic is a 'C4' then `tonic_octave` is 4.
        interval octave (int): Scientific octave for the interval. For example,
            if the interval is a 'G5' then `tonic_octave` is 5.
        chromatic_offset (int): The offset in semitones inside one octave.
            Relative semitones to tonic.
        note_and_octave (str): Note and octave of the interval, for example, if
            the interval is G5 the note name is 'G5'.
        note_name (str): The note name of the interval, for example, if the
            interval is G5 then the name is 'G'.
        semitones (int): Semitones from tonic to octave. If tonic is C4 and
            interval is G5 the number of semitones is 19.
        is_chromatic (bool): If the current interval is chromatic (True) or if
            it exists in the diatonic scale which key is tonic.
        is_descending (bool): If the interval has a descending direction, ie.,
            has a lower pitch than the tonic.
        diatonic_index (int): If the interval is chromatic, this will be the
            nearest diatonic interval in the direction of the resolution
            (closest tonic.) From II to IV degrees, it is the ditonic interval
            before; from V to VII it is the diatonic interval after.
        distance (dict): A dictionary which the distance from tonic to
            interval, for example, if tonic is C4 and interval is G5::
                {
                    'octaves': 1,
                    'semitones': 7
                }
        data (tuple): A tuple representing the interval data in the form of
            (semitones, short_name, long_name), for example::
                (19, 'P12', 'Perfect Twelfth')
    """

    def __init__(self, pitch_a, pitch_b):
        """Measures the musical interval from pitch_a to pitch_b.

        Args:
            pitch_a (str): First `Pitch` object to be measured.
            pitch_b (str): Second `Pitch` object to be measured.
        """

        
        descending = True if int(pitch_b) < int(pitch_a) else False
        
        semitones = int(pitch_b) - int(pitch_a)
        
        self.update({
            'tonic_octave': pitch_a.octave,
            'tonic_note_and_octave': str(pitch_a),
            'interval_octave': pitch_b.octave,
            'chromatic_offset': pitch_b.pitch_class,
            'note_and_octave': str(pitch_b),
            'note_name': str(pitch_b.note),
            'note_octave': pitch_b.octave,
            'semitones': semitones,
            'is_descending': descending,
            'distance': {'octaves': int(semitones/12),
                         'semitones': int(semitones%12)},
            'data': INTERVALS[semitones],
        })