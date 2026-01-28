from birdears.interfaces.commandline import CommandLine

from birdears.questions.melodicinterval import MelodicIntervalQuestion
from birdears.questions.instrumentaldictation \
    import InstrumentalDictationQuestion


def test_centertext():
    cli = CommandLine(exercise='melodic')
    cli.center_text('test')


def test_printquestion():
    cli = CommandLine(exercise='melodic')
    a = MelodicIntervalQuestion()
    resp = a.check_question('x')
    cli.print_question(a)
    assert(a)

    a = MelodicIntervalQuestion(chromatic=True)
    resp = a.check_question('x')
    cli.print_question(a)
    assert(a)

    a = MelodicIntervalQuestion(descending=True)
    resp = a.check_question('x')
    cli.print_question(a)
    assert(a)

    a = MelodicIntervalQuestion(n_octaves=2)
    resp = a.check_question('x')
    cli.print_question(a)
    assert(a)


def test_printresponse():
    cli = CommandLine(exercise='melodic')
    a = MelodicIntervalQuestion()
    resp = a.check_question('x')
    cli.print_response(resp)
    assert(a)

    a = MelodicIntervalQuestion(chromatic=True)
    resp = a.check_question('x')
    cli.print_response(resp)
    assert(a)

    a = MelodicIntervalQuestion(descending=True)
    resp = a.check_question('x')
    cli.print_response(resp)
    assert(a)

    a = MelodicIntervalQuestion(n_octaves=2)
    resp = a.check_question('x')
    cli.print_response(resp)
    assert(a)


def test_instrumental_print():
    cli = CommandLine(exercise='melodic')
    a = InstrumentalDictationQuestion()
    resp = a.check_question()
    cli.print_instrumental(resp)
