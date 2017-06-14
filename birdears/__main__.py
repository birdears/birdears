"__Main__ docs are here."

from . import click

from . import _Getch

from . import INTERVALS
from . import DIATONIC_MODES

from .interfaces.commandline import CommandLine

CTX_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    # max_content_width=click.get_terminal_size()[0],
    max_content_width=80,
)

VALID_MODES = tuple(DIATONIC_MODES.keys())

main_epilog = """
You can use 'birdears <command> --help' to show options for a specific command.

More info at https://github.com/iacchus/birdears
"""


valid_modes = ", ".join(VALID_MODES)


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

melodic_epilog = """
In this exercise birdears will play two notes, the tonic and the interval
melodically, ie., one after the other and you should reply which is the correct
distance between the two.

<mode> is one of these: {valid_modes}
""".format(
    valid_modes=valid_modes,
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
def melodic(*args, **kwargs):
    """Melodic interval recognition
    """

    kwargs.update({'exercise': 'melodic'})
    CommandLine(**kwargs)

harmonic_epilog = """
In this exercise birdears will play two notes, the tonic and the interval
harmonically, ie., both on the same time and you should reply which is the
correct distance between the two.

<mode> is one of these: {valid_modes}
""".format(
    valid_modes=valid_modes,
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
def harmonic(*args, **kwargs):
    """Harmonic interval recognition
    """

    kwargs.update({'exercise': 'harmonic'})
    CommandLine(**kwargs)


dictation_epilog = """
In this exercise birdears will choose some random intervals and create a
melodic dictation with them. You should reply the correct intervals of the
melodic dictation.

<mode> is one of these: {valid_modes}
""".format(
    valid_modes=valid_modes,
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
def dictation(*args, **kwargs):
    """Melodic dictation
    """

    kwargs.update({'exercise': 'dictation'})
    CommandLine(**kwargs)


instrumental_epilog = """
In this exercise birdears will choose some random intervals and create a
melodic dictation with them. You should play the correct melody in you musical
instrument.

<mode> is one of these: {valid_modes}
""".format(
    valid_modes=valid_modes,
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
def instrumental(*args, **kwargs):
    """Instrumental melodic time-based dictation
    """

    kwargs.update({'exercise': 'instrumental'})
    CommandLine(**kwargs)

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
