import itertools

from birdears import KEYS

from birdears.questionbase import QuestionBase

from birdears.interval import DiatonicInterval
from birdears.interval import ChromaticInterval

from birdears.scale import ScaleBase
from birdears.scale import DiatonicScale
from birdears.scale import ChromaticScale

from birdears.sequence import Sequence

#    def __init__(self, mode='major', tonic=None, octave=None, descending=None,
#                 chromatic=None, n_octaves=None, *args, **kwargs):


#    def __init__(self, mode, tonic, octave, chromatic=None, n_octaves=None,
#                 descending=None):

def test_questionbase_placeholders():
    a = QuestionBase()

    a.make_question()
    a.make_resolution()
    a.check_question()

    assert(a)

def test_scalebase_placeholders():
    a = ScaleBase()

    #a.get_triad(degree='something something')

    assert(a)

def test_sequenceclass_notes():

    sequence = Sequence(['C4','D4','E4'])
    sequence.play()

    assert(sequence)

def test_sequenceclass_chords():

    sequence = Sequence([['C4', 'E4', 'G4'], ['G4', 'B4', 'D5'],
                        ['C4','E4','G4']])
    sequence.play()

    assert(sequence)

def test_sequenceclass_append():

    sequence = Sequence(['C3'])
    sequence.append(['C4', 'D4', 'E4'])

    assert(sequence.elements)

def test_sequenceclass_extend():
    sequence = Sequence(['C3'])
    sequence.extend(['C4', 'D4', 'E4'])

    assert(sequence.elements)

def test_diatonicintervalclass():

    a = DiatonicInterval(mode='major', tonic='C', octave=4)
    assert(a)

def test_chromaticintervalclass():

    a = ChromaticInterval(mode='major', tonic='C', octave=4)
    assert(a)

def test_diatonicintervalclass_returnsimple():

    a = DiatonicInterval(mode='major', tonic='C', octave=4)
    b = a.return_simple(['tonic_octave'])

    assert(type(b) == dict)

def test_chromaticintervalclass_returnsimple():

    a = ChromaticInterval(mode='major', tonic='C', octave=4)
    b = a.return_simple(['tonic_octave'])

    assert(type(b) == dict)

def test_diatonicintervalclass_params():
    global KEYS

    c_modes = ['major','minor']
    c_tonics = KEYS
    c_octaves = [3, 4, 5]
    c_descending = [False, True]
    c_n_octaves = [1, 2]

    param_combinations = list(itertools.product(c_modes, c_tonics, c_octaves,
                              c_descending, c_n_octaves))

    for mode, tonic, octave, descending, n_octaves \
        in param_combinations:

        a = DiatonicInterval(mode=mode, tonic=tonic, octave=octave,
                             n_octaves=n_octaves, descending=descending)

        assert(a)

def test_chromaticintervalclass_params():
    global KEYS

    c_modes = ['major','minor']
    c_tonics = KEYS
    c_octaves = [3, 4, 5]
    c_descending = [False, True]
    c_n_octaves = [1, 2]

    param_combinations = list(itertools.product(c_modes, c_tonics, c_octaves,
                              c_descending, c_n_octaves))

    for mode, tonic, octave, descending, n_octaves \
        in param_combinations:

        a = ChromaticInterval(mode=mode, tonic=tonic, octave=octave,
                              n_octaves=n_octaves, descending=descending)

        assert(a)

#    def __init__(self, tonic, mode=None, octave=None, n_octaves=None,
#                 chromatic=None, descending=None, dont_repeat_tonic=None):

def test_diatonicscaleclass():

    a = DiatonicScale(tonic='C', mode='major')
    assert(a)

def test_chromaticscaleclass():

    a = ChromaticScale(tonic='C')
    assert(a)

def test_diatonicscaleclass_params():
    global KEYS

    c_modes = ['major','minor']
    c_tonics = KEYS
    c_octaves = [3, 4, 5]
    c_descending = [False, True]
    c_n_octaves = [1, 2]
    c_dont_repeat_tonic = [False, True]

    param_combinations = list(itertools.product(c_modes, c_tonics, c_octaves,
                              c_descending, c_n_octaves, c_dont_repeat_tonic))

    for mode, tonic, octave, descending, n_octaves,  dont_repeat_tonic \
        in param_combinations:

        a = DiatonicScale(tonic=tonic, mode=mode, octave=octave,
                          n_octaves=n_octaves, descending=descending,
                          dont_repeat_tonic=dont_repeat_tonic)

        assert(a)

def test_chromaticscaleclass_params():
    global KEYS

    c_tonics = KEYS
    c_octaves = [3, 4, 5]
    c_descending = [False, True]
    c_n_octaves = [1, 2]
    c_dont_repeat_tonic = [False, True]

    param_combinations = list(itertools.product(c_tonics, c_octaves,
                              c_descending, c_n_octaves, c_dont_repeat_tonic))

    for tonic, octave, descending, n_octaves, dont_repeat_tonic \
        in param_combinations:

        a = ChromaticScale(tonic=tonic, octave=octave, n_octaves=n_octaves,
                           descending=descending,
                           dont_repeat_tonic=dont_repeat_tonic)

        assert(a)

def test_sequenceclass():
    pass
