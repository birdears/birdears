from birdears import *


def test_questionbase():
    a = QuestionBase()
    assert(a)


def test_questionclass():
    global KEYS

    for tonic in KEYS:
        a = Question()
        assert(a)


def test_questionclass_chromatic():
    global KEYS

    for tonic in KEYS:
        a = Question(tonic=tonic, chromatic=True)
        assert(a)


def test_questionclass_descending():
    global KEYS

    for tonic in KEYS:
        a = Question(tonic=tonic, descending=True)
        assert(a)


def test_questionclass_chromatic_descending():
    global KEYS

    for tonic in KEYS:
        a = Question(tonic=tonic, chromatic=True, descending=True)
        assert(a)


def test_questionclass_minor_chromatic_descending():
    global KEYS

    for tonic in KEYS:
        a = Question(tonic=tonic, mode='minor', chromatic=True,
                     descending=True)
        assert(a)


def test_questionclass_n_octaves():
    global KEYS

    for tonic in KEYS:
        a = Question(tonic=tonic, n_octaves=2)
        assert(a)


def test_intervalclass():

    a = Interval(mode='major', tonic='C', octave=4)
    assert(a)


def test_scaleclass():

    a = Scale(tonic='C', mode='major')
    assert(a)
