"__Main__ docs are here."

import urwid

from . import click

from . import DIATONIC_MODES

from .interfaces.commandline import CommandLine

from . import CHROMATIC_SHARP
from . import CHROMATIC_FLAT
from . import CHROMATIC_TYPE

from .prequestion import PREQUESTION_METHODS
from .resolution import RESOLUTION_METHODS

from .questions import *

CTX_SETTINGS = dict(
    help_option_names=['-h', '--help'],
    max_content_width=80,
)

VALID_MODES = tuple(DIATONIC_MODES.keys())
VALID_PREQUESTION_METHODS = tuple(PREQUESTION_METHODS.keys())
VALID_RESOLUTION_METHODS = tuple(RESOLUTION_METHODS.keys())

INTERFACE = False

def load_interface(*args, **kwargs):
    
    if INTERFACE == 'urwid':
       # from .interfaces.urwid import urwid

        from .interfaces.urwid import TextUserInterface
        palette = [
            ('default', 'default', 'default'),
            ('highlight', 'black', 'light gray')
            ]
        
        wrapper = []
        tui = TextUserInterface(loop_wrapper=wrapper, *args, **kwargs)
        
        #loop = urwid.MainLoop(tui, palette)
        #loop.run()
        #global loop
        loop = urwid.MainLoop(tui, palette)
        wrapper.append(loop)
        loop.run()
        
    else:
        CommandLine(*args, **kwargs)

main_epilog = """
You can use 'birdears <command> --help' to show options for a specific command.

More info at https://github.com/iacchus/birdears
"""

tonics = list(set(CHROMATIC_SHARP + CHROMATIC_FLAT))
tonics.sort()

valid_tonics = ", ".join(tonics)
valid_modes = ", ".join(VALID_MODES)
valid_prequestion_methods = ", ".join(VALID_PREQUESTION_METHODS)
valid_resolution_methods = ", ".join(VALID_RESOLUTION_METHODS)


@click.group(options_metavar='', subcommand_metavar='<command> [options]',
             epilog=main_epilog,
             context_settings=CTX_SETTINGS)
@click.option('--debug/--no-debug',
              help='Turns on debugging; instead you can set DEBUG=1.',
              default=False, envvar='DEBUG')
@click.option('--urwid/--no-urwid',
              help='Uses urwid as interface.',
              default=False, envvar='URWID')
def cli(debug, urwid):
    """birdears ─ Functional Ear Training for Musicians!"""

    global INTERFACE
    
    if debug:
        from .logger import logger
        from .logger import logging

        global logger

        logger.setLevel(logging.DEBUG)
        logger.debug('debug is on.')

    if urwid:
        INTERFACE = 'urwid'
    else:
        INTERFACE = 'commandline'

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
@click.option('-m', '--mode', type=click.Choice(VALID_MODES),
              default='major', metavar='<mode>', help="Mode of the question.")
@click.option('-t', '--tonic', type=str, default='C', metavar='<tonic>',
              help='Tonic of the question.')
# @click.option('-o', '--octave', type=click.IntRange(3, 6), default=None,
@click.option('-o', '--octave', type=str, default='4',
              metavar='<octave>',
              help="Octave of the question.")
@click.option('-d', '--descending', is_flag=True,
              help='Whether the question interval is descending.')
@click.option('-c', '--chromatic', is_flag=True,
              help='If chosen, question has chromatic notes.')
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=1,
              metavar='<n max>', help='Maximum number of octaves.')
@click.option('-v', '--valid_intervals', type=str, default=CHROMATIC_TYPE,
              metavar='<1,2,..>', help='A comma-separated list without spaces\
              of valid scale degrees to be chosen for the question.')
@click.option('-q', '--user_durations', type=str, default=None,
              metavar='<1,0.5,n..>', help='A comma-separated list without\
              spaces with PRECISELY 9 floating values. Or \'n\' for default\
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
@click.option('-m', '--mode', metavar='<mode>', type=click.Choice(VALID_MODES),
              default='major', help="Mode of the question.")
@click.option('-t', '--tonic', type=str, default='C', metavar='<note>',
              help='Tonic of the question.')
# @click.option('-o', '--octave', type=click.IntRange(3, 6), default=None,
@click.option('-o', '--octave', type=str, default='4',
              metavar='<octave>',
              help="Octave of the question.")
@click.option('-d', '--descending', is_flag=True,
              help='Whether the question interval is descending.')
@click.option('-c', '--chromatic', is_flag=True,
              help='If chosen, question has chromatic notes.')
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=1,
              metavar='<n max>', help='Maximum number of octaves.')
@click.option('-v', '--valid_intervals', type=str, default=CHROMATIC_TYPE,
              metavar='<1,2,..>', help='A comma-separated list without spaces\
              of valid scale degrees to be chosen for the question.')
@click.option('-q', '--user_durations', type=str, default=None,
              metavar='<1,0.5,n..>', help='A comma-separated list without\
              spaces with PRECISELY 9 floating values. Or \'n\' for default\
              duration.')
@click.option('-p', '--prequestion_method', type=str, default='none',
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
@click.option('-m', '--mode', metavar='<mode>', type=click.Choice(VALID_MODES),
              default='major', help="Mode of the question.")
@click.option('-i', '--max_intervals', type=click.IntRange(2, 12), default=3,
              metavar='<n max>',
              help='Max random intervals for the dictation.')
@click.option('-x', '--n_notes', type=click.IntRange(1, 20), default=4,
              metavar='<n notes>',
              help='Number of notes for the dictation.')
@click.option('-t', '--tonic', type=str, default='C', metavar='<note>',
              help='Tonic of the question.')
#@click.option('-o', '--octave', type=click.IntRange(3, 6), default=4,
@click.option('-o', '--octave', type=str, default='4',
              metavar='<octave>',
              help="Octave of the question.")
@click.option('-d', '--descending', is_flag=True,
              help='Wether the question interval is descending.')
@click.option('-c', '--chromatic', is_flag=True,
              help='If chosen, question has chromatic notes.')
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=1,
              metavar='<n max>', help='Maximum number of octaves.')
@click.option('-v', '--valid_intervals', type=str, default=CHROMATIC_TYPE,
              metavar='<1,2,..>', help='A comma-separated list without spaces\
              of valid scale degrees to be chosen for the question.')
@click.option('-q', '--user_durations', type=str, default=None,
              metavar='<1,0.5,n..>', help='A comma-separated list without\
              spaces with PRECISELY 9 floating values. Or \'n\' for default\
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
@click.option('-x', '--n_notes', type=click.IntRange(1, 20), default=4,
              metavar='<n notes>',
              help='Number of notes for the dictation.')
@click.option('-t', '--tonic', type=str, default='C', metavar='<note>',
              help='Tonic of the question.')
#@click.option('-o', '--octave', type=click.IntRange(3, 6), default=4,
@click.option('-o', '--octave', type=str, default='4',
              metavar='<octave>', help="Octave of the question.")
@click.option('-d', '--descending', is_flag=True,
              help='Wether the question interval is descending.')
@click.option('-c', '--chromatic', is_flag=True,
              help='If chosen, question has chromatic notes.')
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=1,
              metavar='<n max>', help='Maximum number of octaves.')
@click.option('-v', '--valid_intervals', type=str, default=CHROMATIC_TYPE,
              metavar='<1,2,..>', help='A comma-separated list without spaces\
              of valid scale degrees to be chosen for the question.')
@click.option('-q', '--user_durations', type=str, default=None,
              metavar='<1,0.5,n..>', help='A comma-separated list without\
              spaces with PRECISELY 9 floating values. Or \'n\' for default\
              duration.')
@click.option('-p', '--prequestion_method', type=str,
              default='progression_i_iv_v_i', metavar='<prequestion_method>',
              help='The name of a pre-question method.')
@click.option('-r', '--resolution_method', type=str, default='repeat_only',
              metavar='<resolution_method>',
              help='The name of a resolution method.')
def instrumental(*args, **kwargs):
    """Instrumental melodic time-based dictation
    """

    kwargs.update({'exercise': 'instrumental'})
    CommandLine(**kwargs)


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
@click.option('-m', '--mode', type=click.Choice(VALID_MODES),
              default='major', metavar='<mode>', help="Mode of the question.")
@click.option('-t', '--tonic', type=str, default='C', metavar='<tonic>',
              help='Tonic of the question.')
#@click.option('-o', '--octave', type=click.IntRange(3, 6), default=4,
@click.option('-o', '--octave', type=str, default='4',
              metavar='<octave>',
              help="Octave of the question.")
@click.option('-d', '--descending', is_flag=True,
              help='Whether the question interval is descending.')
@click.option('-c', '--chromatic', is_flag=True,
              help='If chosen, question has chromatic notes.')
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=1,
              metavar='<n max>', help='Maximum number of octaves.')
@click.option('-v', '--valid_intervals', type=str, default=CHROMATIC_TYPE,
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
@click.pass_context
def notename(ctx, *args, **kwargs):
    """Note name by intervaç recognition
    """

    #print(ctx.obj)
    kwargs.update({'exercise': 'notename'})
    # CommandLine(**kwargs)
    load_interface(*args, **kwargs)
    

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


if __name__ == "__main__":

    cli()
