"__Main__ docs are here."

import urwid
import click

from . import DIATONIC_MODES

from .interfaces.commandline import CommandLine

from . import CHROMATIC_SHARP
from . import CHROMATIC_FLAT
from . import CHROMATIC_TYPE

from .prequestion import PREQUESTION_METHODS
from .resolution import RESOLUTION_METHODS

from .questions import *

from . import D

CTX_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    max_content_width=80,
)

VALID_MODES = tuple(DIATONIC_MODES) + ('r', 'R')

VALID_PREQUESTION_METHODS = tuple(PREQUESTION_METHODS.keys())
VALID_RESOLUTION_METHODS = tuple(RESOLUTION_METHODS.keys())

INTERFACE = False


def load_interface(*args, **kwargs):

    if INTERFACE == 'urwid':
        from .interfaces.urwid import TextUserInterface
        tui = TextUserInterface(**kwargs)
    else:
        cli = CommandLine(cli_prompt_next, cli_no_scroll, cli_no_resolution,
              *args, **kwargs)


main_epilog = """
You can use 'birdears <command> --help' to show options for a specific command.

Global options can also be set as environment variables (e.g., DEBUG=1).

More info at https://github.com/iacchus/birdears.
"""

tonics = list(set(CHROMATIC_SHARP + CHROMATIC_FLAT))
tonics.sort()

valid_tonics = ", ".join(tonics)
valid_modes = ", ".join(VALID_MODES)
valid_prequestion_methods = ", ".join(VALID_PREQUESTION_METHODS)
valid_resolution_methods = ", ".join(VALID_RESOLUTION_METHODS)

# On the help screen, sort commands by definition order, not alphabetically.
# See https://github.com/pallets/click/issues/513#issuecomment-504158316
class SortCommands(click.Group):
    def list_commands(self, ctx):
        return self.commands.keys()

@click.group(cls=SortCommands,
             options_metavar='[options]',
             subcommand_metavar='<command> [--help]',
             epilog=main_epilog,
             context_settings=CTX_SETTINGS)
@click.option('--debug/--no-debug',
              help='Turn on debugging',
              default=False, envvar='DEBUG')
@click.option('--urwid/--no-urwid',
              help='Use urwid as interface (default)',
              default=True, envvar='URWID')
@click.option('--cli/--no-cli',
              help='Use command line as interface',
              default=False, envvar='CLI')
@click.option('--prompt',
              help='Wait for input before new question (\'cli\' only)',
              default=False, is_flag=True, envvar='PROMPT')
@click.option('--no-scroll',
              help='Clear screen on new question (implies --prompt)',
              default=False, is_flag=True, envvar='NO_SCROLL')
@click.option('--no-resolution',
              help='Do not play resolution after answer (\'cli\' only)',
              default=False, is_flag=True, envvar='NO_RESOLUTION')
def cli(debug, urwid, cli, prompt, no_scroll, no_resolution):
    """birdears ─ Functional Ear Training for Musicians!"""

    global INTERFACE

    if debug:
        from .logger import logger
        from .logger import logging

        global logger

        logger.setLevel(logging.DEBUG)
        logger.debug('debug is on.')

    if cli or not urwid:
        INTERFACE = 'commandline'
    
        global cli_prompt_next
        global cli_no_scroll
        global cli_no_resolution
        
        cli_prompt_next = prompt
        cli_no_scroll = no_scroll
        cli_no_resolution = no_resolution

        if cli_no_scroll:
            cli_prompt_next = True
    else:
        INTERFACE = 'urwid'

#
# EXERCISES' OPTIONS
#

mode_option = \
    click.option('-m', '--mode', type=click.Choice(VALID_MODES),
                 default='major', metavar='<mode>',
                 help="Mode of the question.")
wait_time_option = \
    click.option('-w', '--wait_time', type=click.IntRange(1, 60), default=7,
                 metavar='<seconds>',
                 help='Time in seconds for next question/repeat.')
n_repeats_option = \
    click.option('-u', '--n_repeats', type=click.IntRange(1, 10), default=1,
                metavar='<times>', help='Times to repeat question.')
max_intervals_option = \
    click.option('-i', '--max_intervals', type=click.IntRange(2, 12),
                 default=3, metavar='<n max>',
                 help='Max random intervals for the dictation.')
n_notes_option = \
    click.option('-x', '--n_notes', type=click.IntRange(1, 20), default=4,
                 metavar='<n notes>',
                 help='Number of notes for the dictation.')
tonic_option = \
    click.option('-t', '--tonic', type=str, default='C', metavar='<tonic>',
                 help='Tonic of the question.')
octave_option = \
    click.option('-o', '--octave', type=str, default='4', metavar='<octave>',
                 help="Octave of the question.")
descending_option = \
    click.option('-d', '--descending', is_flag=True,
                 help='Whether the question interval is descending.')
chromatic_option = \
    click.option('-c', '--chromatic', is_flag=True,
                 help='If chosen, question has chromatic notes.')
n_octaves_option = \
    click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=1,
                 metavar='<n max>', help='Maximum number of octaves.')
valid_intervals_option = \
    click.option('-v', '--valid_intervals', type=str,
                 default=str(",").join([str(item) for item in CHROMATIC_TYPE]),
                 metavar='<1,2,..>',
                 help='A comma-separated list without spaces of valid scale '
                      'degrees to be chosen for the question.')
user_durations_option = \
    click.option('-q', '--user_durations', type=str, default=None,
                 metavar='<1,0.5,n..>',
                 help='A comma-separated list without spaces with PRECISLY 9'
                      ' floating values. Or \'n\' for default duration.')
prequestion_method_option = \
    click.option('-p', '--prequestion_method', type=str, default='tonic_only',
                 metavar='<prequestion_method>',
                 help='The name of a pre-question method.')
resolution_method_option = \
    click.option('-r', '--resolution_method', type=str,
                 default='nearest_tonic', metavar='<resolution_method>',
                 help='The name of a resolution method.')
repeat_only_resolution_method_option = \
    click.option('-r', '--resolution_method', type=str,
                 default='repeat_only', metavar='<resolution_method>',
                 help='The name of a resolution method.')
keyboard_width_option = \
    click.option('-k', '--keyboard_width', type=click.IntRange(10, 100),
                 default=60, metavar='<width>',
                 help='The width of the keyboard in percentage.')


#
# melodic interval
#

melodic_epilog = """
In this exercise birdears will play two notes, the tonic and the interval
melodically, ie., one after the other and you should reply which is the correct
distance between the two.

Valid values are as follows:

-m <mode> is one of: {valid_modes}

-t <tonic> is one of: {valid_tonics}

-p <prequestion_method> is one of: {valid_prequestion_methods}

-r <resolution_method> is one of: {valid_resolution_methods}
""".format(
    valid_modes=valid_modes,
    valid_tonics=valid_tonics,
    valid_resolution_methods=valid_resolution_methods,
    valid_prequestion_methods=valid_prequestion_methods,
)

@cli.command(options_metavar='[options]', epilog=melodic_epilog)
@mode_option
@tonic_option
@octave_option
@descending_option
@chromatic_option
@n_octaves_option
@valid_intervals_option
@user_durations_option
@prequestion_method_option
@resolution_method_option
@keyboard_width_option
def melodic(*args, **kwargs):
    """Melodic interval recognition
    """

    kwargs.update({'exercise': 'melodic'})
    load_interface(*args, **kwargs)


#
# harmonic interval
#

harmonic_epilog = """
In this exercise birdears will play two notes, the tonic and the interval
harmonically, ie., both on the same time and you should reply which is the
correct distance between the two.

Valid values are as follows:

-m <mode> is one of: {valid_modes}

-t <tonic> is one of: {valid_tonics}

-p <prequestion_method> is one of: {valid_prequestion_methods}

-r <resolution_method> is one of: {valid_resolution_methods}
""".format(
    valid_modes=valid_modes,
    valid_tonics=valid_tonics,
    valid_resolution_methods=valid_resolution_methods,
    valid_prequestion_methods=valid_prequestion_methods,
)

@cli.command(options_metavar='[options]', epilog=harmonic_epilog)
@mode_option
@tonic_option
@octave_option
@descending_option
@chromatic_option
@n_octaves_option
@valid_intervals_option
@user_durations_option
@prequestion_method_option
@resolution_method_option
@keyboard_width_option
def harmonic(*args, **kwargs):
    """Harmonic interval recognition
    """

    kwargs.update({'exercise': 'harmonic'})
    load_interface(*args, **kwargs)


#
# melodic dictation
#

dictation_epilog = """
In this exercise birdears will choose some random intervals and create a
melodic dictation with them. You should reply the correct intervals of the
melodic dictation.

Valid values are as follows:

-m <mode> is one of: {valid_modes}

-t <tonic> is one of: {valid_tonics}

-p <prequestion_method> is one of: {valid_prequestion_methods}

-r <resolution_method> is one of: {valid_resolution_methods}
""".format(
    valid_modes=valid_modes,
    valid_tonics=valid_tonics,
    valid_resolution_methods=valid_resolution_methods,
    valid_prequestion_methods=valid_prequestion_methods,
)

@cli.command(options_metavar='[options]', epilog=dictation_epilog)
@mode_option
@max_intervals_option
@n_notes_option
@tonic_option
@octave_option
@descending_option
@chromatic_option
@n_octaves_option
@valid_intervals_option
@user_durations_option
@prequestion_method_option
#@resolution_method_option
@repeat_only_resolution_method_option
@keyboard_width_option
def dictation(*args, **kwargs):
    """Melodic dictation
    """

    kwargs.update({'exercise': 'dictation'})
    load_interface(*args, **kwargs)


#
# instrumental dictation
#

instrumental_epilog = """
In this exercise birdears will choose some random intervals and create a
melodic dictation with them. You should play the correct melody on your musical
instrument.

Valid values are as follows:

-m <mode> is one of: {valid_modes}

-t <tonic> is one of: {valid_tonics}

-p <prequestion_method> is one of: {valid_prequestion_methods}

-r <resolution_method> is one of: {valid_resolution_methods}
""".format(
    valid_modes=valid_modes,
    valid_tonics=valid_tonics,
    valid_resolution_methods=valid_resolution_methods,
    valid_prequestion_methods=valid_prequestion_methods,
)

@cli.command(options_metavar='[options]', epilog=instrumental_epilog)
@mode_option
@wait_time_option
@n_repeats_option
@max_intervals_option
@n_notes_option
@tonic_option
@octave_option
@descending_option
@chromatic_option
@n_octaves_option
@valid_intervals_option
@user_durations_option
@prequestion_method_option
#@resolution_method_option
@repeat_only_resolution_method_option
@keyboard_width_option
def instrumental(*args, **kwargs):
    """Instrumental melodic dictation (time-based)
    """

    kwargs.update({'exercise': 'instrumental'})
    load_interface(*args, **kwargs)


#
# notename
#

notename_epilog = """
In this exercise birdears will play two notes, the tonic and the interval
melodically, ie., one after the other and you should reply which is the correct
name of the second note.

Valid values are as follows:

-m <mode> is one of: {valid_modes}

-t <tonic> is one of: {valid_tonics}

-p <prequestion_method> is one of: {valid_prequestion_methods}

-r <resolution_method> is one of: {valid_resolution_methods}
""".format(
    valid_modes=valid_modes,
    valid_tonics=valid_tonics,
    valid_resolution_methods=valid_resolution_methods,
    valid_prequestion_methods=valid_prequestion_methods,
)

@cli.command(options_metavar='[options]', epilog=notename_epilog)
@mode_option
@tonic_option
@octave_option
@descending_option
@chromatic_option
@n_octaves_option
@valid_intervals_option
@user_durations_option
@prequestion_method_option
@resolution_method_option
@keyboard_width_option
def notename(*args, **kwargs):
    """Note name by interval recognition
    """

    kwargs.update({'exercise': 'notename'})
    load_interface(*args, **kwargs)


#
# load preset config
#

@cli.command(options_metavar='')
@click.argument('filename', type=click.File(), metavar='<filename>')
def load(filename, *args, **kwargs):
    """Load exercise preset from .toml config file <filename>.
    """

    try:
        import toml
    except ImportError:
        from .toml import toml

    toml_file_str = filename.read()
    config_dict = toml.loads(toml_file_str)

    load_interface(*args, **kwargs, **config_dict)


if __name__ == "__main__":

    cli()
