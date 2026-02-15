from random import choice

from birdears import KEYS
from birdears import get_keyboard_index
from birdears.questions.melodicdictation import MelodicDictationQuestion


def test_melodicintervalclass():

    mode = choice(['major', 'minor'])
    max_intervals = choice([2, 3, 4])
    n_notes = choice([2, 3, 4])
    tonic = choice(KEYS)
    octave = choice([3, 4, 5])
    descending = choice([False, True])
    chromatic = choice([False, True])
    n_octaves = choice([1, 2])

    for i in range(20):
        a = MelodicDictationQuestion(mode=mode, max_intervals=max_intervals,
                                     n_notes=n_notes, tonic=tonic,
                                     octave=octave, descending=descending,
                                     chromatic=chromatic, n_octaves=n_octaves,
                                     prequestion_method='none')

        a.keyboard_index = get_keyboard_index(a.mode, a.is_descending)

# why not guess some interval
        a.check_question(['z', 'x', 'x', 'Z'])

        assert(a)
