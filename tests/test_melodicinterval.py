from random import choice

from birdears import CHROMATIC_SHARP
from birdears import CHROMATIC_FLAT

from birdears.questions.melodicinterval import MelodicIntervalQuestion

# def __init__(self, mode='major', tonic=None, octave=None, descending=None,
#                chromatic=None, n_octaves=None, *args, **kwargs):

def test_melodicintervalclass():

    keys = list(CHROMATIC_SHARP)
    keys.extend(CHROMATIC_FLAT)

    mode = choice(['major', 'minor'])
    tonic = choice(keys)
    octave = choice([3, 4, 5])
    descending = choice([False, True])
    chromatic = choice([False, True])
    n_octaves = choice([1, 2])

    for i in range(20):
        a = MelodicIntervalQuestion(mode=mode, tonic=tonic, octave=octave,
                                    descending=descending, chromatic=chromatic,
                                    n_octaves=n_octaves)

        # why not guess some interval
        a.check_question('x')

        assert(a)
