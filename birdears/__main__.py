"__Main__ docs are here."

from . import click

from . import _Getch

from . import INTERVALS
from . import DIATONIC_MODES

from . import DEBUG


from os import popen
COLS = int(popen('tput cols', 'r').read())

def center_text(text, sep=True, nl=0):
    linelist = list(text.splitlines())

    # gets the biggest line
    biggest_line_size = 0
    for line in linelist:
        line_lenght = len(line.expandtabs())
        if line_lenght > biggest_line_size:
            biggest_line_size = line_lenght

    columns = COLS
    offset = biggest_line_size / 2
    perfect_center = columns / 2
    padsize =  int(perfect_center - offset)
    spacing = ' ' * padsize # space char

    text = str()
    for line in linelist:
        text += (spacing + line + '\n')

    divider = spacing + ('─' * int(biggest_line_size)) # unicode 0x2500
    text += divider

    text += nl * '\n'

    return text


# this is for debugging
def print_stuff(question):
    padd = "─" * 30  # vim: insert mode, ^vu2500
    print("""
{}

Tonic: {} | Note(Int): {} |  Interval: {} | Semitones(Int): {} |
Is Note Chromatic: {} |
Scale: {}, Octave: {}
Resolution: ,
Chromatic: {}
Concrete Scale: {} | Chroma Concrete: {}
{}
""".format(
        padd,
        question.concrete_tonic,
        question.interval.note_and_octave,
        "─".join(INTERVALS[question.interval.semitones][1:]),
        question.interval.semitones,
        question.interval.is_chromatic,
        "─".join(question.scales['diatonic'].scale),
        "{}-{}".format(question.octave, question.octave + 1),
        "─".join(question.scales['chromatic'].scale),
        "─".join(question.scales['diatonic_pitch'].scale),
        "─".join(question.scales['chromatic_pitch'].scale),
        padd,
    ))


def print_stuff_dictation(question):
    padd = "─" * 30  # vim: insert mode, ^vu2500
    print("""
{}

Tonic: {} | Note(Int): {} |  Interval: {} | Semitones(Int): {} |
Scale: {}, Octave: {}
Chromatic: {}
Concrete Scale: {} | Chroma Concrete: {}
{}
""".format(
        padd,
        question.concrete_tonic,
        "─".join(map(str, question.question_phrase)),
        "─".join([INTERVALS[n][1] for n in question.question_phrase]),
        "─".join([str(n) for n in question.question_phrase]),
        "─".join(question.scales['diatonic'].scale),
        "{}-{}".format(question.octave, question.octave + 1),
        "─".join(question.scales['chromatic'].scale),
        "─".join(question.scales['diatonic_pitch'].scale),
        "─".join(question.scales['chromatic_pitch'].scale),
        padd,
    ))


@click.group()
def cli():
    pass


@cli.command()
@click.option('-m', '--mode', type=click.Choice(['major', 'minor']), default='major')
@click.option('-t', '--tonic', type=str, default=None)
@click.option('-o', '--octave', type=click.IntRange(2, 5), default=None)
@click.option('-d', '--descending', is_flag=True)
@click.option('-c', '--chromatic', is_flag=True)
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=None)
def melodic(*args, **kwargs):
    kwargs.update({'exercise': 'melodic'})
    ear(**kwargs)


@cli.command()
@click.option('-m', '--mode', type=click.Choice(['major', 'minor']), default='major')
@click.option('-t', '--tonic', type=str, default=None)
@click.option('-o', '--octave', type=click.IntRange(2, 5), default=None)
@click.option('-d', '--descending', is_flag=True)
@click.option('-c', '--chromatic', is_flag=True)
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=None)
def harmonic(*args, **kwargs):
    kwargs.update({'exercise': 'harmonic'})
    ear(**kwargs)


@cli.command()
@click.option('-m', '--mode', type=click.Choice(['major', 'minor']), default='major')
@click.option('-i', '--max_intervals', type=click.IntRange(2, 12), default=3)
@click.option('-x', '--n_notes', type=click.IntRange(3, 10), default=4)
@click.option('-t', '--tonic', type=str, default=None)
@click.option('-o', '--octave', type=click.IntRange(2, 5), default=None)
@click.option('-d', '--descending', is_flag=True)
@click.option('-c', '--chromatic', is_flag=True)
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=None)
def dictation(*args, **kwargs):
    kwargs.update({'exercise': 'dictation'})
    ear(**kwargs)

def print_response(response):

    text_kwargs = dict(
        user_resp = response['user_response_str'],
        correct_resp = response['correct_response_str']
    )

    # TODO: make a class for response
    if response['is_correct']:
        response_text = "Correct! It is {correct_resp}".format(**text_kwargs)

    else:
        response_text = "It is incorrect...You replied {user_resp} but the"\
                        " correct is {correct_resp}".format(**text_kwargs)

    print(center_text(response_text,nl=2))

def print_question(question):

    keyboard = question.keyboard_index

    scale = list(question.scales['diatonic'].scale)

    diatonic_index = list(DIATONIC_MODES[question.mode])

    if question.is_descending:
        diatonic_index = [12 - x for x in diatonic_index]
        #diatonic_index.reverse()
        scale.reverse()

    intervals = [INTERVALS[i][1] for i in diatonic_index]
    keys = [keyboard[i] for i in diatonic_index]

    scale_str = " ".join(map(lambda x: x.ljust(3), scale))
    intervals_str = " ".join(map(lambda x: x.ljust(3), intervals))
    keys_str = " ".join(map(lambda x: x.ljust(3), keys))

    text_kwargs = dict(
        tonic = question.tonic,
        mode = question.mode,
        chroma = question.is_chromatic,
        desc = question.is_descending,
        scale = scale_str,
        intervals = intervals_str,
        keyboard = keys_str,

    )

    question_text = """\

KEY: {tonic} {mode}
(chromatic: {chroma}; descending: {desc})

Intervals {intervals}
Scale     {scale}
Keyboard  {keyboard}

""".format(**text_kwargs)

    print(center_text(question_text,nl=1))
    #print(question_text)

def ear(exercise, **kwargs):

    if exercise == 'dictation':
        from .questions.melodicdictation import MelodicDictationQuestion
        #dictate_notes = 4
        dictate_notes = kwargs['n_notes']
        MYCLASS = MelodicDictationQuestion
        MYPRINT = print_stuff_dictation

    elif exercise == 'melodic':
        from .questions.melodicinterval import MelodicIntervalQuestion
        MYCLASS = MelodicIntervalQuestion
        dictate_notes = 1
        MYPRINT = print_stuff

    elif exercise == 'harmonic':
        from .questions.harmonicinterval import HarmonicIntervalQuestion
        MYCLASS = HarmonicIntervalQuestion
        dictate_notes = 1
        MYPRINT = print_stuff

    getch = _Getch()

    new_question_bit = True

    while True:
        if new_question_bit is True:

            new_question_bit = False

            input_keys = []
            question = MYCLASS(**kwargs)

            # debug
            if DEBUG:
                MYPRINT(question)

            print_question(question)
            question.question.play()

        user_input = getch()

        #print(user_input, end='')
        if user_input in question.keyboard_index and user_input != ' ':  # spc

            input_keys.append(user_input)

            if len(input_keys) == dictate_notes:

                response = question.check_question(input_keys)
                print_response(response)

                question.resolution.play()

                new_question_bit = True

        # q - quit
        elif user_input == 'q':
            exit(0)

        # r - repeat interval
        elif user_input == 'r':
            question.question.play()


if __name__ == "__main__":

    cli()
