import itertools
from random import choice

from birdears import KEYS
from birdears.questions.instrumentaldictation \
    import InstrumentalDictationQuestion

def test_instrumentaldictationclass():
    global KEYS

    mode = choice(['major', 'minor'])
    max_intervals = choice([2, 3, 4])
    wait_time = choice([0, 1])
    n_repeats = choice([0, 1])
    n_notes = choice([2, 3, 4])
    tonic = choice(KEYS)
    octave = choice([3, 4, 5])
    descending = choice([False, True])
    chromatic = choice([False, True])
    n_octaves = choice([1, 2])

    for i in range(20):

        a = InstrumentalDictationQuestion(mode=mode, wait_time=wait_time,
                                          n_repeats=n_repeats,
                                          max_intervals=max_intervals,
                                          n_notes=n_notes, tonic=tonic,
                                          octave=octave, descending=descending,
                                          chromatic=chromatic,
                                          n_octaves=n_octaves)

        assert(a)
