"__Main__ docs are here."

from . import click

from . import _Getch

from . import INTERVALS
from . import DIATONIC_MODES

from .interfaces.commandline import CommandLine

from .prequestion import PREQUESTION_METHODS
from .resolution import RESOLUTION_METHODS

CTX_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    # max_content_width=click.get_terminal_size()[0],
    max_content_width=80,
)

VALID_MODES = tuple(DIATONIC_MODES.keys())
VALID_PREQUESTION_METHODS = tuple(PREQUESTION_METHODS.keys())
VALID_RESOLUTION_METHODS = tuple(RESOLUTION_METHODS.keys())

main_epilog = """
You can use 'birdears <command> --help' to show options for a specific command.

More info at https://github.com/iacchus/birdears
"""

valid_modes = ", ".join(VALID_MODES)
valid_prequestion_methods = ", ".join(VALID_PREQUESTION_METHODS)
valid_resolution_methods = ", ".join(VALID_RESOLUTION_METHODS)


@click.group(options_metavar='', subcommand_metavar='<command> [options]',
             epilog=main_epilog,
             context_settings=CTX_SETTINGS)
@click.option('--debug/--no-debug',
              help='Turns on debugging; instead you can set DEBUG=1.',
              default=False, envvar='DEBUG')
def cli(debug):
    """birdears ─ Functional Ear Training for Musicians!"""

    if debug:
        from .logger import logger
        from .logger import logging

        global logger

        logger.setLevel(logging.DEBUG)
        logger.debug('debug is on.')

#
# melodic interval
#

melodic_epilog = """
In this exercise birdears will play two notes, the tonic and the interval
melodically, ie., one after the other and you should reply which is the correct
distance between the two.

Valid values are as follows:

-m <mode> is one of: {valid_modes}

-p <prequestion_method> is one of: {valid_prequestion_methods}

-r <resolution_method> is one of: {valid_resolution_methods}
""".format(
    valid_modes=valid_modes,
    valid_resolution_methods=valid_resolution_methods,
    valid_prequestion_methods=valid_prequestion_methods,
)


@cli.command(options_metavar='[options]', epilog=melodic_epilog)
@click.option('-m', '--mode', type=click.Choice(VALID_MODES),
              default='major', metavar='<mode>', help="Mode of the question.")
@click.option('-t', '--tonic', type=str, default=None, metavar='<note>',
              help='Tonic of the question.')
@click.option('-o', '--octave', type=click.IntRange(2, 5), default=None,
              metavar='<octave>',
              help="Octave of the question.")
@click.option('-d', '--descending', is_flag=True,
              help='Whether the question interval is descending.')
@click.option('-c', '--chromatic', is_flag=True,
              help='If chosen, question has chromatic notes.')
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=1,
              metavar='<n max>', help='Maximum number of octaves.')
@click.option('-v', '--valid_intervals', type=str, default=None,
              metavar='<1,2,..>', help='A comma-separated list without spaces\
              of valid scale degrees to be chosen for the question.')
@click.option('-q', '--user_durations', type=str, default=None,
              metavar='<1,0.5,n..>', help='A comma-separated list without\
              spaces with PRECISLY 9 floating values. Or \'n\' for default\
              duration.')
@click.option('-p', '--prequestion_method', type=str, default='tonic_only',
              metavar='<prequestion_method>',
              help='The name of a pre-question method.')
@click.option('-r', '--resolution_method', type=str, default='nearest_tonic',
              metavar='<resolution_method>',
              help='The name of a resolution method.')
def melodic(*args, **kwargs):
    """Melodic interval recognition
    """

    kwargs.update({'exercise': 'melodic'})
    CommandLine(**kwargs)

#
# harmonic interval
#

harmonic_epilog = """
In this exercise birdears will play two notes, the tonic and the interval
harmonically, ie., both on the same time and you should reply which is the
correct distance between the two.

Valid values are as follows:

-m <mode> is one of: {valid_modes}

-p <prequestion_method> is one of: {valid_prequestion_methods}

-r <resolution_method> is one of: {valid_resolution_methods}
""".format(
    valid_modes=valid_modes,
    valid_resolution_methods=valid_resolution_methods,
    valid_prequestion_methods=valid_prequestion_methods,
)


@cli.command(options_metavar='[options]', epilog=harmonic_epilog)
@click.option('-m', '--mode', metavar='<mode>', type=click.Choice(VALID_MODES),
              default='major', help="Mode of the question.")
@click.option('-t', '--tonic', type=str, default=None, metavar='<note>',
              help='Tonic of the question.')
@click.option('-o', '--octave', type=click.IntRange(2, 5), default=None,
              metavar='<octave>',
              help="Octave of the question.")
@click.option('-d', '--descending', is_flag=True,
              help='Whether the question interval is descending.')
@click.option('-c', '--chromatic', is_flag=True,
              help='If chosen, question has chromatic notes.')
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=None,
              metavar='<n max>', help='Maximum number of octaves.')
@click.option('-v', '--valid_intervals', type=str, default=None,
              metavar='<1,2,..>', help='A comma-separated list without spaces\
              of valid scale degrees to be chosen for the question.')
@click.option('-q', '--user_durations', type=str, default=None,
              metavar='<1,0.5,n..>', help='A comma-separated list without\
              spaces with PRECISLY 9 floating values. Or \'n\' for default\
              duration.')
@click.option('-p', '--prequestion_method', type=str, default='tonic_only',
              metavar='<prequestion_method>',
              help='The name of a pre-question method.')
@click.option('-r', '--resolution_method', type=str, default='nearest_tonic',
              metavar='<resolution_method>',
              help='The name of a resolution method.')
def harmonic(*args, **kwargs):
    """Harmonic interval recognition
    """

    kwargs.update({'exercise': 'harmonic'})
    CommandLine(**kwargs)

#
# dictation
#

dictation_epilog = """
In this exercise birdears will choose some random intervals and create a
melodic dictation with them. You should reply the correct intervals of the
melodic dictation.


Valid values are as follows:

-m <mode> is one of: {valid_modes}

-p <prequestion_method> is one of: {valid_prequestion_methods}

-r <resolution_method> is one of: {valid_resolution_methods}
""".format(
    valid_modes=valid_modes,
    valid_resolution_methods=valid_resolution_methods,
    valid_prequestion_methods=valid_prequestion_methods,
)


@cli.command(options_metavar='[options]', epilog=dictation_epilog)
@click.option('-m', '--mode', metavar='<mode>', type=click.Choice(VALID_MODES),
              default='major', help="Mode of the question.")
@click.option('-i', '--max_intervals', type=click.IntRange(2, 12), default=3,
              metavar='<n max>',
              help='Max random intervals for the dictation.')
@click.option('-x', '--n_notes', type=click.IntRange(3, 10), default=4,
              metavar='<n notes>',
              help='Number of notes for the dictation.')
@click.option('-t', '--tonic', type=str, default=None, metavar='<note>',
              help='Tonic of the question.')
@click.option('-o', '--octave', type=click.IntRange(2, 5), default=None,
              metavar='<octave>',
              help="Octave of the question.")
@click.option('-d', '--descending', is_flag=True,
              help='Wether the question interval is descending.')
@click.option('-c', '--chromatic', is_flag=True,
              help='If chosen, question has chromatic notes.')
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=None,
              metavar='<n max>', help='Maximum number of octaves.')
@click.option('-v', '--valid_intervals', type=str, default=None,
              metavar='<1,2,..>', help='A comma-separated list without spaces\
              of valid scale degrees to be chosen for the question.')
@click.option('-q', '--user_durations', type=str, default=None,
              metavar='<1,0.5,n..>', help='A comma-separated list without\
              spaces with PRECISLY 9 floating values. Or \'n\' for default\
              duration.')
@click.option('-p', '--prequestion_method', type=str,
              default='progression_i_iv_v_i', metavar='<prequestion_method>',
              help='The name of a pre-question method.')
@click.option('-r', '--resolution_method', type=str, default='repeat_only',
              metavar='<resolution_method>',
              help='The name of a resolution method.')
def dictation(*args, **kwargs):
    """Melodic dictation
    """

    kwargs.update({'exercise': 'dictation'})
    CommandLine(**kwargs)


#
# instrumental dictation
#

instrumental_epilog = """
In this exercise birdears will choose some random intervals and create a
melodic dictation with them. You should play the correct melody in you musical
instrument.

Valid values are as follows:

-m <mode> is one of: {valid_modes}

-p <prequestion_method> is one of: {valid_prequestion_methods}

-r <resolution_method> is one of: {valid_resolution_methods}
""".format(
    valid_modes=valid_modes,
    valid_resolution_methods=valid_resolution_methods,
    valid_prequestion_methods=valid_prequestion_methods,
)


@cli.command(options_metavar='[options]', epilog=instrumental_epilog)
@click.option('-m', '--mode', metavar='<mode>', type=click.Choice(VALID_MODES),
              default='major', help="Mode of the question.")
@click.option('-w', '--wait_time', type=click.IntRange(1, 60), default=7,
              metavar='<seconds>',
              help='Time in seconds for next question/repeat.')
@click.option('-u', '--n_repeats', type=click.IntRange(1, 10), default=1,
              metavar='<times>', help='Times to repeat question.')
@click.option('-i', '--max_intervals', type=click.IntRange(2, 12), default=3,
              metavar='<n max>',
              help='Max random intervals for the dictation.')
@click.option('-x', '--n_notes', type=click.IntRange(3, 10), default=4,
              metavar='<n notes>',
              help='Number of notes for the dictation.')
@click.option('-t', '--tonic', type=str, default=None, metavar='<note>',
              help='Tonic of the question.')
@click.option('-o', '--octave', type=click.IntRange(2, 5), default=None,
              metavar='<octave>', help="Octave of the question.")
@click.option('-d', '--descending', is_flag=True,
              help='Wether the question interval is descending.')
@click.option('-c', '--chromatic', is_flag=True,
              help='If chosen, question has chromatic notes.')
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=None,
              metavar='<n max>', help='Maximum number of octaves.')
@click.option('-v', '--valid_intervals', type=str, default=None,
              metavar='<1,2,..>', help='A comma-separated list without spaces\
              of valid scale degrees to be chosen for the question.')
@click.option('-q', '--user_durations', type=str, default=None,
              metavar='<1,0.5,n..>', help='A comma-separated list without\
              spaces with PRECISLY 9 floating values. Or \'n\' for default\
              duration.')
@click.option('-p', '--prequestion_method', type=str,
              default='progression_i_iv_v_i', metavar='<prequestion_method>',
              help='The name of a pre-question method.')
@click.option('-r', '--resolution_method', type=str, default='nearest_tonic',
              metavar='<resolution_method>',
              help='The name of a resolution method.')
def instrumental(*args, **kwargs):
    """Instrumental melodic time-based dictation
    """

    kwargs.update({'exercise': 'instrumental'})
    CommandLine(**kwargs)

#
# birdear's "load"
#

load_epilog = """
Loads exercise from file.
"""


@cli.command(options_metavar='', epilog=load_epilog)
@click.argument('filename', type=click.File(), metavar='<filename>')
def load(filename, *args, **kwargs):
    """Loads exercise from .toml config file <filename>.
    """

    from .toml import toml

    toml_file_str = filename.read()
    config_dict = toml.loads(toml_file_str)

    CommandLine(**config_dict)

urwid_epilog = """
This uses urwid to load birdears TUI.
"""


@cli.command(options_metavar='', epilog=urwid_epilog)
def urwid(*args, **kwargs):
    """Starts birdears text user interface (using urwid).
    """

    try:
        import urwid
    except ImportError:
        print("You need to install 'urwid' python library to use the tui.")
        exit(1)

    pass


kivy_epilog = """
This uses kivy to load birdears GUI.
"""


@cli.command(options_metavar='', epilog=kivy_epilog)
def kivy(*args, **kwargs):
    """Starts birdears graphical user interface (using kivy).
    """

    try:
        import kivy
    except ImportError:
        print("You need to install 'kivy' python library to use the gui.")
        exit(1)

    from .interfaces.gui.app import BirdearsApp

    BirdearsApp().run()


if __name__ == "__main__":

    cli()
