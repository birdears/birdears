import os
import sys

from .. import _Getch

from .. import KEYS
from .. import CHROMATIC_SHARP
from .. import CHROMATIC_FLAT

from .. import INTERVALS
from .. import DIATONIC_MODES
from .. import CHROMATIC_TYPE

from ..questionbase import QUESTION_CLASSES

from shutil import get_terminal_size

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

    divider = \
        spacing + (dim + '─' * int(biggest_line_size) + reset) # unicode 0x2500

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

    print(color + center_text(response_text, sep=False, nl=1) + reset)


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

    question_text = """\
     Scale: {scale}
 Intervals: {intervals}
  Keyboard: {keyboard}
""".format(**text_kwargs)

    print(center_text(question_text, nl=2))


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

    def __init__(self, cli_prompt_next=False,
                 cli_no_scroll=False, cli_no_resolution=False,
                 exercise=None, *args, **kwargs):
        """This function implements the birdears loop for command line.

        Args:
            cli_prompt_next (bool): True if --prompt is set.
            cli_no_scroll (bool): True if --no-scroll is set.
            cli_no_resolution (bool): True if --no-resolution is set.
            exercise (str): The question name.
            **kwargs: Keyword arguments passed to the question class.
                Common arguments include:
                - mode (str): The mode of the question (e.g., 'major', 'minor').
                - tonic (str): The tonic of the question (e.g., 'C').
                - octave (int): A scientific octave notation.
                - descending (bool): Is the question direction in descending.
                - chromatic (bool): If the question can have chromatic intervals.
                - n_octaves (int): Maximum number of octaves of the question.
                - valid_intervals (list): A list with valid intervals (int).
                - user_durations (str): A string with default durations.
                - prequestion_method (str): Method of playing a cadence.
                - resolution_method (str): Method of playing the resolution.

                Specific question arguments:
                - n_notes (int): The number of notes (dictation).
                - max_intervals (int): Max number of random intervals (dictation).
                - wait_time (float): Wait time in seconds (instrumental).
                - n_repeats (int): Number of repeats (instrumental).
        """

        if exercise in QUESTION_CLASSES:
            QUESTION_CLASS = QUESTION_CLASSES[exercise]
        else:
            raise Exception("Invalid `exercise` value:", exercise)
        
        self.prompt_next = cli_prompt_next
        self.no_scroll = cli_no_scroll
        self.no_resolution = cli_no_resolution

        self.exercise = exercise

        ####if 'n_notes' in kwargs:
            ####self.dictate_notes = kwargs['n_notes']
        ####else:
            ####self.dictate_notes = 1

        getch = _Getch()

        self.new_question_bit = True

        print('\n')

        while True:
            if self.new_question_bit is True:

                self.new_question_bit = False

                self.input_keys = list()
                self.question = QUESTION_CLASS(**kwargs)

                if   self.exercise == 'melodic':
                    exercise_title  = 'Melodic interval recognition'
                    question_prompt = 'What is the interval?'

                elif self.exercise == 'harmonic':
                    exercise_title  = 'Harmonic interval recognition'
                    question_prompt = 'What is the interval?'

                elif self.exercise == 'dictation':
                    exercise_title  = 'Melodic dictation'
                    question_prompt = 'Now, please type the intervals ' \
                                      'you\'ve heard.'

                elif self.exercise == 'instrumental':
                    exercise_title  = 'Instrumental melodic ' \
                                      'time-based detection'
                    # TODO: question_prompt

                else:               # 'notename':
                    exercise_title  = 'Note name by interval recognition'
                    question_prompt = 'The tonic is {tonic}. ' \
                                      'Press the key representing the ' \
                                      'second note.' \
                                      .format(tonic=self.question.tonic_str)

                if self.no_scroll:
                    # Clear terminal screen (but keep scrollback)
                    # See https://stackoverflow.com/a/2084628
                    os.system('cls' if os.name == 'nt' else 'clear -x')
                    print('\n')

                print(center_text('birdears ─ Functional Ear Training',
                                  sep=False, nl=1))
                print(center_text(exercise_title, nl=0))
                print(center_text('KEY: ' + self.question.tonic_str + ' ' \
                                  + self.question.mode, sep=False, nl=1))

                print_question(self.question)

                if not self.exercise == 'instrumental':
                    self.question.play_question()

                    print(center_text(question_prompt))
                    print(center_text(
                        'key- answer   r- repeat   q- quit', sep=False, nl=1))

            if self.exercise == 'instrumental':
                for r in range(self.question.n_repeats):
                    self.question.play_question()

                # FIXME: Instrumental is broken in CLI, double countdown...
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

        if user_input in self.question.keyboard_index \
            and user_input != ' ':  # spc

            self.input_keys.append(user_input)

            ###if self.exercise == 'dictation':
                ###input_str = make_input_str(self.input_keys,
                ###    self.question.keyboard_index)
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

                if not self.no_resolution:
                    self.question.play_resolution()
                
                if self.prompt_next:
                    print(center_text('Next question', nl=0))
                    print(center_text('any- play   q- quit', sep=False, nl=1))
                    
                    getch2 = _Getch()

                    while True: # wait for input before next question
                        user_input2 = getch2()
                    
                        # q - quit
                        if user_input2 in ('q', 'Q'):
                            sys.exit()
                        # any key - play next question
                        elif user_input2:
                            break
                        # loop, keep waiting
                        else:
                            pass

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

        # q - quit
        elif user_input in ('q', 'Q'):
            sys.exit()

        # r - repeat interval
        elif user_input in ('r', 'R'):
            self.question.play_question()
