import itertools

from birdears import KEYS
from birdears.questions.melodicdictation import MelodicDictationQuestion

# def __init__(self, mode='major', max_intervals=3, n_notes=4, tonic=None,
#                 octave=None, descending=None, chromatic=None, n_octaves=None,
#                 *args, **kwargs):

def test_melodicintervalclass():
    global KEYS

    c_modes = ['major','minor']
    c_max_intervals = [2, 3, 4]
    c_n_notes = [2, 3, 4]
    c_tonics = KEYS
    c_octaves = [3, 4, 5]
    c_descending = [False, True]
    c_chromatic = [False, True]
    c_n_octaves = [1, 2]

    param_combinations = list(itertools.product(c_modes, c_max_intervals,
                                                c_n_notes, c_tonics, c_octaves,
                                                c_descending, c_chromatic,
                                                c_n_octaves))

    for mode, max_intervals, n_notes, tonic, octave, descending, chromatic, \
        n_octaves in param_combinations:

        a = MelodicDictationQuestion(mode=mode, max_intervals=max_intervals,
                                     n_notes=n_notes, tonic=tonic,
                                     octave=octave, descending=descending,
                                     chromatic=chromatic, n_octaves=n_octaves)

        assert(a)
