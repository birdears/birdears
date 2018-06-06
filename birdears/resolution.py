from . import MAX_SEMITONES_RESOLVE_BELOW

from .interval import Interval

from .scale import DiatonicScale

from .sequence import Sequence

from .note_and_pitch import get_pitch_by_number
from .note_and_pitch import Chord

from functools import wraps

RESOLUTION_METHODS = {}
# http://stackoverflow.com/questions/5910703/howto-get-all-methods-of-a-pyt\
# hon-class-with-given-decorator
# http://stackoverflow.com/questions/5707589/calling-functions-by-array-ind\
# ex-in-python/5707605#5707605


def register_resolution_method(f, *args, **kwargs):
    """Decorator for resolution method functions.

    Functions decorated with this decorator will be registered in the
    `RESOLUTION_METHODS` global dict.
    """

    @wraps(f)
    def decorator(*args, **kwargs):
        return f(*args, **kwargs)

    RESOLUTION_METHODS.update({f.__name__: f})

    return decorator


class Resolution:
    """This class implements methods for different types of question
    resolutions.

    A resolution is an answer to a question. It aims to create a mnemonic on
    how the inverval resvolver to the tonic.
    """

    def __init__(self, method, question):
        """Inits the resolution class.

        Args:
            method (str): The method used in the resolution.
            question (obj): Question object from which to generate the
            resolution sequence.
        """

        self.METHOD = RESOLUTION_METHODS[method]
        self.question = question

    def __call__(self, *args, **kwargs):
        """Calls the resolution method and pass arguments to it.

        Returns a `birdears.Sequence` object with the resolution generated by
        the.method.
        """
        return self.METHOD(question=self.question, *args, **kwargs)


@register_resolution_method
def nearest_tonic(question):
    """Resolution method that resolve the intervals to their nearest tonics.

    Args:
        question (obj): Question object from which to generate the
            resolution sequence. (this is provided by the `Prequestion` class
            when it is `__call__`ed)
    """

    tonic_pitch = question.tonic_pitch

    # if hasattr(question, 'random_pitch'):
    #    random_pitch = tuple(question.random_pitch)
    # else:
    #    random_pitch = tuple(question.random_pitches)
    #
    # TODO:
    if hasattr(question, 'random_pitches'):
        raise Exception('NEAREST_TONIC FOR MULTIPLE PITCHES IS STILL TO BE'
                        'IMPLEMENTED')
    random_pitch = question.random_pitch

    duration = question.durations['resol']['duration']
    delay = question.durations['resol']['delay']
    pos_delay = question.durations['resol']['pos_delay']

    # this function will receive: tonic, scale and random_pitch (which may be
    # chromatic, ie., not in `scale`)

    # negative is descending
    semitones = (int(random_pitch) - int(tonic_pitch)) % 12

    scale_random_pitch = question.diatonic_scale

    direction = -1 if (semitones <= MAX_SEMITONES_RESOLVE_BELOW) else +1
    # invert `direction` signal if descending:
    pitch_direction = (direction * -1) if question.is_descending else direction

    resolution = []

    if random_pitch not in scale_random_pitch:  # random_pitch is chromatic
        resolution.append(random_pitch)
        # if this note is chromatic then the
        # next ones above or below are in the diatonic for sure, so we
        # add one semitone and we will have the next diatonic degree:
        nearest_diatonic_pitch = \
            get_pitch_by_number(int(random_pitch) + direction)
            # get_pitch_by_number(int(random_pitch) + pitch_direction)

    else:
        nearest_diatonic_pitch = random_pitch  # random_pitch is diatonic

    resolve_mask = 0 if semitones <= MAX_SEMITONES_RESOLVE_BELOW else 12

    nearest_tonic_pitch = get_pitch_by_number(int(random_pitch) +
                                              (resolve_mask-semitones))

    nearest_tonic_index = scale_random_pitch.index(nearest_tonic_pitch)

    nearest_diatonic_pitch_index = \
        scale_random_pitch.index(nearest_diatonic_pitch)

    random_pitch_index = nearest_diatonic_pitch_index

    ohslice = slice(min(nearest_tonic_index, random_pitch_index),
                    max(nearest_tonic_index, nearest_diatonic_pitch_index)+1)

    resolution = scale_random_pitch[ohslice][::pitch_direction]

    # is it chromatic?
    if random_pitch not in scale_random_pitch:
        resolution.insert(0, random_pitch)

    if len(resolution) == 1:
        resolution.append(tonic_pitch)

    if question.is_harmonic:
        resolution_harmonic = []

        for item in resolution:
            resolution_harmonic.append(Chord([tonic_pitch, item]))

        resolution = resolution_harmonic

    print(resolution)

    # resolution
    return Sequence(elements=resolution, duration=duration, delay=delay,
                    pos_delay=pos_delay)


@register_resolution_method
# FIXME : it should both play preq and question
def repeat_only(question):
    """Resolution method that only repeats the sequence elements with given
    durations.

    Args:
        question (obj): Question object from which to generate the
            resolution sequence. (this is provided by the `Prequestion` class
            when it is `__call__`ed)
    """
    elements = tuple(question.question)

    duration = question.durations['resol']['duration']
    delay = question.durations['resol']['delay']
    pos_delay = question.durations['resol']['pos_delay']

    sequence_list = Sequence(elements, duration=duration, delay=delay,
                             pos_delay=pos_delay)

    return sequence_list
