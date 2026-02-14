from birdears.interfaces import commandline
from birdears import get_keyboard_index

from birdears.questions.melodicinterval import MelodicIntervalQuestion
from birdears.questions.instrumentaldictation \
    import InstrumentalDictationQuestion


def test_centertext():
    commandline.center_text('test')


def test_printquestion():

    a = MelodicIntervalQuestion()
    a.keyboard_index = get_keyboard_index(a.mode, a.is_descending)
    resp = a.check_question('x')
    commandline.print_question(a)
    assert(a)

    a = MelodicIntervalQuestion(chromatic=True)
    a.keyboard_index = get_keyboard_index(a.mode, a.is_descending)
    resp = a.check_question('x')
    commandline.print_question(a)
    assert(a)

    a = MelodicIntervalQuestion(descending=True)
    a.keyboard_index = get_keyboard_index(a.mode, a.is_descending)
    resp = a.check_question('x')
    commandline.print_question(a)
    assert(a)

    a = MelodicIntervalQuestion(n_octaves=2)
    a.keyboard_index = get_keyboard_index(a.mode, a.is_descending)
    resp = a.check_question('x')
    commandline.print_question(a)
    assert(a)


def test_printresponse():

    a = MelodicIntervalQuestion()
    a.keyboard_index = get_keyboard_index(a.mode, a.is_descending)
    resp = a.check_question('x')
    commandline.print_response(resp)
    assert(a)

    a = MelodicIntervalQuestion(chromatic=True)
    a.keyboard_index = get_keyboard_index(a.mode, a.is_descending)
    resp = a.check_question('x')
    commandline.print_response(resp)
    assert(a)

    a = MelodicIntervalQuestion(descending=True)
    a.keyboard_index = get_keyboard_index(a.mode, a.is_descending)
    resp = a.check_question('x')
    commandline.print_response(resp)
    assert(a)

    a = MelodicIntervalQuestion(n_octaves=2)
    a.keyboard_index = get_keyboard_index(a.mode, a.is_descending)
    resp = a.check_question('x')
    commandline.print_response(resp)
    assert(a)


def test_instrumental_print():

    a = InstrumentalDictationQuestion()
    resp = a.check_question()
    commandline.print_instrumental(resp)
