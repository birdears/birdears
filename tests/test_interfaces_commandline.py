from birdears.interfaces import commandline

from birdears.questions.melodicinterval import MelodicIntervalQuestion
from birdears.questions.instrumentaldictation \
    import InstrumentalDictationQuestion


def test_centertext():
    commandline.center_text('test')


def test_printquestion():

    a = MelodicIntervalQuestion()
    resp = a.check_question('x')
    commandline.print_question(a)
    assert(a)

    a = MelodicIntervalQuestion(chromatic=True)
    resp = a.check_question('x')
    commandline.print_question(a)
    assert(a)

    a = MelodicIntervalQuestion(descending=True)
    resp = a.check_question('x')
    commandline.print_question(a)
    assert(a)

    a = MelodicIntervalQuestion(n_octaves=2)
    resp = a.check_question('x')
    commandline.print_question(a)
    assert(a)


def test_printresponse():

    a = MelodicIntervalQuestion()
    resp = a.check_question('x')
    commandline.print_response(resp)
    assert(a)

    a = MelodicIntervalQuestion(chromatic=True)
    resp = a.check_question('x')
    commandline.print_response(resp)
    assert(a)

    a = MelodicIntervalQuestion(descending=True)
    resp = a.check_question('x')
    commandline.print_response(resp)
    assert(a)

    a = MelodicIntervalQuestion(n_octaves=2)
    resp = a.check_question('x')
    commandline.print_response(resp)
    assert(a)


def test_instrumental_print():

    a = InstrumentalDictationQuestion()
    resp = a.check_question()
    commandline.print_instrumental(resp)
