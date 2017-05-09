from birdears import KEYS

from birdears.questionbase import QuestionBase

from birdears.interval import Interval

from birdears.scale import Scale


def test_questionbase():
    a = QuestionBase()
    assert(a)


def test_intervalclass():

    a = Interval(mode='major', tonic='C', octave=4)
    assert(a)


def test_scaleclass():

    a = Scale(tonic='C', mode='major')
    assert(a)
