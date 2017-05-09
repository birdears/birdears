import itertools

from birdears import KEYS

from birdears.questionbase import QuestionBase

from birdears.interval import Interval

from birdears.scale import Scale

#    def __init__(self, mode='major', tonic=None, octave=None, descending=None,
#                 chromatic=None, n_octaves=None, *args, **kwargs):

def test_questionbase():
    a = QuestionBase()
    assert(a)

def test_questionbase_params():
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

        a = QuestionBase(mode=mode, tonic=tonic, octave=octave,
                                    descending=descending, chromatic=chromatic,
                                    n_octaves=n_octaves)

        assert(a)

#    def __init__(self, mode, tonic, octave, chromatic=None, n_octaves=None,
#                 descending=None):

def test_intervalclass():

    a = Interval(mode='major', tonic='C', octave=4)
    assert(a)

def test_intervalclass_params():
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

        a = Interval(mode=mode, tonic=tonic, octave=octave,
                     chromatic=chromatic, n_octaves=n_octaves,
                     descending=descending,)

        assert(a)

#    def __init__(self, tonic, mode=None, octave=None, n_octaves=None,
#                 chromatic=None, descending=None, dont_repeat_tonic=None):

def test_scaleclass():

    a = Scale(tonic='C', mode='major')
    assert(a)

def test_scaleclass_params():
    global KEYS

    c_modes = ['major','minor']
    c_tonics = KEYS
    c_octaves = [3, 4, 5]
    c_descending = [False, True]
    c_chromatic = [False, True]
    c_n_octaves = [1, 2]
    c_dont_repeat_tonic = [False, True]

    param_combinations = list(itertools.product(c_modes, c_tonics, c_octaves,
                              c_descending, c_chromatic, c_n_octaves,
                              c_dont_repeat_tonic))

    for mode, tonic, octave, descending, chromatic, n_octaves, \
        dont_repeat_tonic in param_combinations:

        a = Scale(tonic=tonic, mode=mode, octave=octave, chromatic=chromatic,
                  n_octaves=n_octaves, descending=descending,
                  dont_repeat_tonic=dont_repeat_tonic)

        assert(a)

def test_sequenceclass():
    pass
