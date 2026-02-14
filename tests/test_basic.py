import itertools

from birdears import KEYS

from birdears.questionbase import QuestionBase

# from birdears.interval import DiatonicInterval
# from birdears.interval import ChromaticInterval
from birdears.interval import Interval

from birdears.scale import ScaleBase
from birdears.scale import DiatonicScale
from birdears.scale import ChromaticScale
from birdears.scale import get_triad

from birdears.sequence import Sequence

from birdears.note_and_pitch import Pitch
from birdears.note_and_pitch import Chord

#    def __init__(self, mode='major', tonic=None, octave=None, descending=None,
#                 chromatic=None, n_octaves=None, *args, **kwargs):


#    def __init__(self, mode, tonic, octave, chromatic=None, n_octaves=None,
#                 descending=None):

def test_questionbase_placeholders():
    a = QuestionBase()

    a.make_question()
    a.make_resolution()
    a.play_question()
    a.check_question()

    assert(a)


def test_questionbase_toniclist():
    a = QuestionBase(tonic=['G', 'D', 'A'])

    assert(a)


def test_questionbase_octavelist():
    a = QuestionBase(octave=[2, 3, 5])

    assert(a)


def test_questionbase_octavetuple():
    a = QuestionBase(octave=(2, 5))

    assert(a)


def test_diatonicscale_placeholders():
    a = DiatonicScale()

    assert(a)


def test_chromaticscale_placeholders():
    a = ChromaticScale()

    assert(a)


def test_sequenceclass_notes():

    c4 = Pitch('C', 4)
    d4 = Pitch('D', 4)
    e4 = Pitch('E', 4)

    # sequence = Sequence(['C4', 'D4', 'E4'])

    sequence = Sequence([c4, d4, e4])
    sequence.play()

    assert(sequence)


def test_sequenceclass_chords():

    c4 = Pitch('C', 4)
    e4 = Pitch('E', 4)
    g4 = Pitch('G', 4)
    b4 = Pitch('B', 4)
    d5 = Pitch('D', 5)

    sequence = Sequence([Chord([c4, e4, g4]), Chord([b4, b4, d5]),
                        Chord([c4, e4, g4])])

    sequence.play()

    assert(sequence)


def test_sequenceclass_append():

    sequence = Sequence([Pitch('C', 3)])
    sequence.append(Chord([Pitch('C', 4), Pitch('D', 4), Pitch('E', 4)]))

    assert(sequence)


def test_sequenceclass_extend():
    sequence = Sequence([Pitch('C', 3)])
    sequence.extend(Chord([Pitch('C', 4), Pitch('D', 4), Pitch('E', 4)]))

    assert(sequence)


def test_sequenceclass_makeprogression():
    pitch = Pitch(note='A', octave=4)

    sequence = Sequence()
    sequence.make_chord_progression(tonic_pitch=pitch, mode='minor',
                                    degrees=[1, 4, 5, 1])

    assert(sequence)


def test_intervalclass():

    a5 = Pitch('A', 5)
    c3 = Pitch('C', 3)

    a = Interval(a5, c3)

    assert(a)


# def test_intervalclass_params():
#    global KEYS
#
#    c_modes = ['major','minor']
#    c_tonics = KEYS
#    c_octaves = [3, 4, 5]
#    c_descending = [False, True]
#    c_n_octaves = [1, 2]
#
#    param_combinations = list(itertools.product(c_modes, c_tonics, c_octaves,
#                              c_descending, c_n_octaves))
#
#    for mode, tonic, octave, descending, n_octaves \
#        in param_combinations:
#
#        a = Interval(mode=mode, tonic=tonic, octave=octave,
#                     n_octaves=n_octaves, descending=descending)
#
#        assert(a)


def test_diatonicscaleclass():

    a = DiatonicScale(tonic='C', mode='major')
    assert(a)


def test_diatonicscale_gettriad():

    a = DiatonicScale(tonic='C', mode='major')
    b = get_triad(tonic=a.tonic, mode=a.mode, degree=7)
    assert(b)


def test_chromaticscaleclass():

    a = ChromaticScale(tonic='C')
    assert(a)


def test_chromaticscale_gettriad():

    a = ChromaticScale(tonic='C')
    b = get_triad(tonic=a.tonic, mode='major', degree=7)
    assert(b)


def test_diatonicscaleclass_params():
    global KEYS

    c_modes = ['major', 'minor']
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
