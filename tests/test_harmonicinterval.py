import itertools

from birdears import KEYS

from birdears.questions.harmonicinterval import HarmonicIntervalQuestion

# def __init__(self, mode='major', tonic=None, octave=None, descending=None,
 #                chromatic=None, n_octaves=None, *args, **kwargs):

def test_harmonicintervalclass():
    global KEYS

    c_modes = ['major','minor']
    c_tonics = KEYS
    c_octaves = [3, 4, 5]
    c_descending = [False, True]
    c_chromatic = [False, True]
    c_n_octaves = [1, 2]

    param_combinations = list(itertools.product(c_modes, c_tonics, c_octaves,
                              c_descending, c_chromatic, c_n_octaves))

    for mode, tonic, octave, descending, chromatic, n_octaves \
        in param_combinations:

        a = HarmonicIntervalQuestion(mode=mode, tonic=tonic, octave=octave,
                                    descending=descending, chromatic=chromatic,
                                    n_octaves=n_octaves)


        # why not guess some interval
        a.check_question('x')

        assert(a)
