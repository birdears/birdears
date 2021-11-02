from .. import _Getch

from .. import KEYS
from .. import CHROMATIC_SHARP
from .. import CHROMATIC_FLAT

from .. import INTERVALS
from .. import DIATONIC_MODES
from .. import CHROMATIC_TYPE

from ..questionbase import QUESTION_CLASSES

# from os import popen
from ..click import get_terminal_size

# FIXME: use `click` one instead or it won't be portable
# COLS = int(popen('tput cols', 'r').read())
COLS, LINES = get_terminal_size()


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
        line_length = len(line.expandtabs())
        if line_length > biggest_line_size:
            biggest_line_size = line_length

    columns = COLS
    offset = biggest_line_size / 2
    perfect_center = columns / 2
    padsize = int(perfect_center - offset)
    spacing = ' ' * padsize  # space char
    dim = '\033[2m'
    reset = '\033[0m'

    text = str()
    for line in linelist:
        text += (spacing + line + '\n')

    divider = spacing + (dim + '─' * int(biggest_line_size) + reset)  # unicode 0x2500
    text += divider if sep else ''

    text += nl * '\n'

    return text


def print_response(response):
    """Prints the formatted response.

    Args:
        response (dict): A response returned by question's check_question()
    """

    # TODO: make a class for response
    if response['is_correct']:
        response_text = "Correct!"
        color = '\033[32m' # green
    else:
        response_text = "Wrong"
        color = '\033[31m' # red

    reset = '\033[0m' # reset terminal color

    if 'extra_response_str' in response.keys():
        print(center_text(response['extra_response_str'], nl=0))

    print(color + center_text(response_text, sep=False, nl=0) + reset)

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

    direction = -1 if question.is_descending else +1

    scale = question.scale
    # mode = question.mode

    tonic = scale[0]
    network = [abs(int(tonic) - int(note)) for note in scale]
    # keyboard_map = KEYBOARD_INDICES['chromatic']['ascending']['major']
    keyboard_map = tuple(question.keyboard_index)

    # should we show the octaves here? why not?

    notes = "".join([str(pitch).ljust(4) for pitch in scale][::direction])
    # notes = "".join([str(pitch.note).ljust(4) \
    # for pitch in scale][::direction])
    intervals = "".join([str(INTERVALS[step][1]).ljust(4)
                         for step in network][::direction])
    keys = "".join([str(keyboard_map[step]).ljust(4)
                    for step in network][::direction])

    text_kwargs = {
        'tonic': question.tonic_str,
        'mode': question.mode,
        'chroma': question.is_chromatic,
        'desc': question.is_descending,
        'scale': notes,
        'intervals': intervals,
        'keyboard': keys,
    }

    question_text = """
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


class CommandLine:

    def __init__(self, exercise=None, *args, **kwargs):
        """This function implements the birdears loop for command line.

        Args:
            exercise (str): The question name.
            **kwargs (kwargs): FIXME: The kwargs can contain options for specific
                questions.
        """

        if exercise in QUESTION_CLASSES:
            QUESTION_CLASS = QUESTION_CLASSES[exercise]
        else:
            raise Exception("Invalid `exercise` value:", exercise)
        
        self.exercise = exercise

        ####if 'n_notes' in kwargs:
            ####self.dictate_notes = kwargs['n_notes']
        ####else:
            ####self.dictate_notes = 1

        getch = _Getch()

        self.new_question_bit = True

        while True:
            if self.new_question_bit is True:

                self.new_question_bit = False

                self.input_keys = list()
                self.question = QUESTION_CLASS(**kwargs)

                print_question(self.question)

                if not self.exercise == 'instrumental':
                    self.question.play_question()

            if self.exercise == 'instrumental':
                for r in range(self.question.n_repeats):
                    self.question.play_question()

                for i in range(self.question.wait_time):
                    time_left = str(self.question.wait_time - i).rjust(3)
                    text = '{} seconds remaining...'.format(time_left)
                    print(center_text(text, sep=False), end='')
                    self.question.question._wait(1)

                response = self.question.check_question()
                print_instrumental(response)

                self.new_question_bit = True

                continue

            user_input = getch()
            self.process_key(user_input)

    def process_key(self, user_input):
        
        if user_input in self.question.keyboard_index and user_input != ' ':  # spc

            self.input_keys.append(user_input)

            ###if self.exercise == 'dictation':
                ###input_str = make_input_str(self.input_keys, self.question.keyboard_index)
                ###print(input_str, end='')
            if self.question.n_input_notes > 1:
                input_str = make_input_str(self.input_keys,
                                           self.question.keyboard_index)
                print(input_str, end='')

            # FIXME: use self.question.n_notes instead
            #if len(self.input_keys) == self.dictate_notes:
            if len(self.input_keys) == self.question.n_notes:

                response = self.question.check_question(self.input_keys)
                print_response(response)

                self.question.play_resolution()

                self.new_question_bit = True

        # backspace
        elif user_input == '\x7f':
            # FIXME: use self.question.n_input_notes instead
            #if(len(self.input_keys) > 0) and self.exercise == 'dictation':
            if(len(self.input_keys) > 0) and (self.question.n_input_notes > 1):
                del(self.input_keys[-1])
                input_str = make_input_str(self.input_keys,
                                           self.question.keyboard_index)
                print(input_str, end='')

        # q/Q - quit
        elif user_input in ('q', 'Q'):
            exit(0)

        # r - repeat interval
        elif user_input in ('r', 'R'):
            self.question.play_question()
