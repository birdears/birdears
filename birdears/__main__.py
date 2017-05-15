"__Main__ docs are here."

from . import click

from . import _Getch

from . import INTERVALS
from . import DIATONIC_MODES

from . import DEBUG

from .interfaces.commandline import CommandLine


@click.group()
def cli():
    """birdears ─ Functional Ear Training for Musicians!"""
    
    pass


@cli.command()
@click.option('-m', '--mode', type=click.Choice(['major', 'minor']), default='major')
@click.option('-t', '--tonic', type=str, default=None)
@click.option('-o', '--octave', type=click.IntRange(2, 5), default=None)
@click.option('-d', '--descending', is_flag=True)
@click.option('-c', '--chromatic', is_flag=True)
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=None)
def melodic(*args, **kwargs):
    """Melodic interval recognition.
    """

    kwargs.update({'exercise': 'melodic'})
    CommandLine(**kwargs)


@cli.command()
@click.option('-m', '--mode', type=click.Choice(['major', 'minor']), default='major')
@click.option('-t', '--tonic', type=str, default=None)
@click.option('-o', '--octave', type=click.IntRange(2, 5), default=None)
@click.option('-d', '--descending', is_flag=True)
@click.option('-c', '--chromatic', is_flag=True)
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=None)
def harmonic(*args, **kwargs):
    """Harmonic interval recognition.
    """

    kwargs.update({'exercise': 'harmonic'})
    CommandLine(**kwargs)


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
    """Melodic dictation.
    """

    kwargs.update({'exercise': 'dictation'})
    CommandLine(**kwargs)


@cli.command()
@click.option('-m', '--mode', type=click.Choice(['major', 'minor']), default='major')
@click.option('-w', '--wait_time', type=click.IntRange(1, 60), default=7)
@click.option('-u', '--n_repeats', type=click.IntRange(1, 10), default=1)
@click.option('-i', '--max_intervals', type=click.IntRange(2, 12), default=3)
@click.option('-x', '--n_notes', type=click.IntRange(3, 10), default=4)
@click.option('-t', '--tonic', type=str, default=None)
@click.option('-o', '--octave', type=click.IntRange(2, 5), default=None)
@click.option('-d', '--descending', is_flag=True)
@click.option('-c', '--chromatic', is_flag=True)
@click.option('-n', '--n_octaves', type=click.IntRange(1, 2), default=None)
def instrumental(*args, **kwargs):
    """Instrumental melodic time-based dictation.
    """

    kwargs.update({'exercise': 'instrumental'})
    CommandLine(**kwargs)


if __name__ == "__main__":

    cli()
