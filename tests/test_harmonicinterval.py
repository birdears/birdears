from random import choice

from birdears import KEYS

from birdears.questions.harmonicinterval import HarmonicIntervalQuestion


def test_harmonicintervalclass():

    mode = choice(['major', 'minor'])
    tonic = choice(KEYS)
    octave = choice([3, 4, 5])
    descending = choice([False, True])
    chromatic = choice([False, True])
    n_octaves = choice([1, 2])

    for i in range(20):

        a = HarmonicIntervalQuestion(mode=mode, tonic=tonic, octave=octave,
                                     descending=descending,
                                     chromatic=chromatic, n_octaves=n_octaves)

        # why not guess some interval
        a.check_question('x')

        assert(a)
        