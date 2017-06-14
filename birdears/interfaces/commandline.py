from .. import click

from .. import _Getch

from .. import INTERVALS
from .. import DIATONIC_MODES
from .. import CHROMATIC_TYPE

from .. import DEBUG

from os import popen
COLS = int(popen('tput cols', 'r').read())


def center_text(text, sep=True, nl=0):
    """This function returns input text centered according to terminal columns.

    Args:
        text (str): The string to be centered, it can have multiple lines.
        sep (bool): Add line separator after centered text (True) or
            not (False).
        nl (int): How many new lines to add after text.
    """

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
    padsize = int(perfect_center - offset)
    spacing = ' ' * padsize  # space char

    text = str()
    for line in linelist:
        text += (spacing + line + '\n')

    divider = spacing + ('─' * int(biggest_line_size))  # unicode 0x2500
    text += divider if sep else ''

    text += nl * '\n'

    return text


def print_response(response):
    """Prints the formatted response.

    Args:
        response (dict): A response returned by question's check_question()
    """

    text_kwargs = dict(
        user_resp=response['user_response_str'],
        correct_resp=response['correct_response_str']
    )

    # TODO: make a class for response
    if response['is_correct']:
        response_text = "Correct!"
    else:
        response_text = "Wrong.."

    if 'extra_response_str' in response.keys():
        print(center_text(response['extra_response_str']))

    print(center_text(response_text, nl=2))


def print_instrumental(response):
    """Prints the formatted response for 'instrumental' exercise.

    Args:
        response (dict): A response returned by question's check_question()
    """

    text_kwargs = dict(
        correct_resp=response['correct_response_str']
    )

    response_text = """
{correct_resp}
""".format(**text_kwargs)

    print(center_text(response_text, nl=2))


def print_question(question):
    """Prints the question to the user.

    Args:
        question (obj): A Question class with the question to be printed.
    """

    keyboard = question.keyboard_index

    if not question.is_chromatic:
        scale = list(question.scales['diatonic'].scale)

        mode = list(DIATONIC_MODES[question.mode])
        scale_index = list(mode)
    else:
        scale = list(question.scales['chromatic'].scale)

        mode = list(CHROMATIC_TYPE)
        scale_index = list(mode)

    for o in range(1, question.n_octaves):
        scale_index.extend([x + (12*o) for x in mode[1:]])

    # FIXME: bug with descending n_octaves=2
    if question.is_descending:
        highest = max(scale_index)
        scale_index = [highest - x for x in scale_index]
        scale = reversed(scale)

    intervals = [INTERVALS[i][1] for i in scale_index]
    keys = [keyboard[i] for i in scale_index]

    scale_str = " ".join(map(lambda x: x.ljust(3), scale))
    intervals_str = " ".join(map(lambda x: x.ljust(3), intervals))
    keys_str = " ".join(map(lambda x: x.ljust(3), keys))

    text_kwargs = dict(
        tonic=question.tonic,
        mode=question.mode,
        chroma=question.is_chromatic,
        desc=question.is_descending,
        scale=scale_str,
        intervals=intervals_str,
        keyboard=keys_str,
    )

    question_text = """\

KEY: {tonic} {mode}
(chromatic: {chroma}; descending: {desc})

Intervals {intervals}
Scale     {scale}
Keyboard  {keyboard}

""".format(**text_kwargs)

    print(center_text(question_text, nl=1))


def make_input_str(user_input, keyboard_index):
    """Makes a string representing intervals entered by the user.

    This function is to be used by questions which takes more than one interval
    input as MelodicDictation, and formats the intervals already entered.

    Args:
        user_input (array_type): The list of keyboard keys entered by user.
        keyboard_index (array_type): The keyboard mapping used by question.
    """

    input_str = str()

    user_input_semitones = [keyboard_index.index(s)
                            for s in user_input]

    user_str = "".join([INTERVALS[s][1].center(5)
                       for s in user_input_semitones]).center(COLS)

    input_str = ("\r{}".format(user_str))

    return input_str


def CommandLine(exercise, **kwargs):
    """This function implements the birdears loop for command line.

    Args:
        exercise (str): The question name.
        **kwargs (kwargs): FIXME: The kwargs can contain options for specific
            questions.
    """

    if exercise == 'dictation':
        from ..questions.melodicdictation import MelodicDictationQuestion
        dictate_notes = kwargs['n_notes']
        MYCLASS = MelodicDictationQuestion

    elif exercise == 'instrumental':
        from ..questions.instrumentaldictation \
            import InstrumentalDictationQuestion

        dictate_notes = kwargs['n_notes']
        MYCLASS = InstrumentalDictationQuestion

    elif exercise == 'melodic':
        from ..questions.melodicinterval import MelodicIntervalQuestion
        MYCLASS = MelodicIntervalQuestion
        dictate_notes = 1

    elif exercise == 'harmonic':
        from ..questions.harmonicinterval import HarmonicIntervalQuestion
        MYCLASS = HarmonicIntervalQuestion
        dictate_notes = 1

    getch = _Getch()

    new_question_bit = True

    while True:
        if new_question_bit is True:

            new_question_bit = False

            input_keys = []
            question = MYCLASS(**kwargs)

            print_question(question)
            question.play_question()

        if exercise == 'instrumental':
            response = question.check_question()
            print_instrumental(response)

            new_question_bit = True

            continue

        user_input = getch()

        if user_input in question.keyboard_index and user_input != ' ':  # spc

            input_keys.append(user_input)

            if exercise == 'dictation':
                input_str = make_input_str(input_keys, question.keyboard_index)
                print(input_str, end='')

            if len(input_keys) == dictate_notes:

                response = question.check_question(input_keys)
                print_response(response)

                question.play_resolution()

                new_question_bit = True

        # backspace
        elif user_input == '\x7f':
            if(len(input_keys) > 0) and exercise == 'dictation':
                del(input_keys[-1])
                input_str = make_input_str(input_keys, question.keyboard_index)
                print(input_str, end='')

        # q/Q - quit
        elif user_input in ('q', 'Q'):
            exit(0)

        # r - repeat interval
        elif user_input in ('r', 'R'):
            question.play_question()
