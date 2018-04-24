import itertools

from birdears import KEYS
from birdears.questions.melodicinterval import MelodicIntervalQuestion

# def __init__(self, mode='major', tonic=None, octave=None, descending=None,
#                chromatic=None, n_octaves=None, *args, **kwargs):

def test_melodicintervalclass():
    global KEYS

    mode = ['major', 'minor']
    tonic = KEYS
    octave = [3, 4, 5]
    descending = [False, True]
    chromatic = [False, True]
    n_octaves = [1, 2]

    for i in range(20):
        a = MelodicIntervalQuestion(mode=mode, tonic=tonic, octave=octave,
                                    descending=descending, chromatic=chromatic,
                                    n_octaves=n_octaves)

        # why not guess some interval
        a.check_question('x')

        assert(a)
