from birdears import *

def test_questionbase():
    a = QuestionBase()
    assert(a)

def test_questionclass():
    a = Question()
    assert(a)

def test_questionclass_(chromatic=True):
    a = Question()
    assert(a)

def test_questionclass_descending(descending=True):
    a = Question()
    assert(a)

def test_questionclass_chromatic_descending(chromatic=True, descending=True):
    a = Question()
    assert(a)

def test_questionclass_minor_chromatic_descending(mode='minor', chromatic=True, descending=True):
    a = Question()
    assert(a)

def test_questionclass_n_octaves(n_octaves=2):
    a = Question()
    assert(a)

def test_intervalclass():
    a = Interval(mode='major', tonic='C', octave=4)
    assert(a)

def test_scaleclass():
    a = Scale(tonic='C', mode='major')
    assert(a)
