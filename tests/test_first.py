from birdears import *

def test_questionbase():
    a = QuestionBase()
    assert(a)

def test_questionclass():
    a = Question()
    assert(a)

def test_intervalclass():
    a = Interval(mode='major', tonic='C', interval=4)
    assert(a)

def test_scaleclass():
    a = Scale(tonic='C')
    assert(a)
