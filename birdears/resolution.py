from . import MAX_SEMITONES_RESOLVE_BELOW

from .scale import DiatonicScale
from .scale import ChromaticScale

from .sequence import Sequence

from functools import wraps

RESOLUTION_METHODS = {}
# http://stackoverflow.com/questions/5910703/howto-get-all-methods-of-a-pyt\
# hon-class-with-given-decorator
# http://stackoverflow.com/questions/5707589/calling-functions-by-array-ind\
# ex-in-python/5707605#5707605


def register_resolution_method(f, *args, **kwargs):
    """Decorator for resolution method functions.

    Functions decorated with this decorator will be registered in the
    `RESOLUTION_METHODS` global.
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

    def __init__(self, method, duration, delay, pos_delay):
        """Inits the resolution class.

        Args:
            method (str): The method used in the resolution.
            duration (float): Default playing time for each element in the
                resolution.
            delay (float): Default waiting time to play the next element
                in the resolution.
            pos_delay (float): Waiting time after playing the last element
                in the resolution.
        """

        self.METHOD = RESOLUTION_METHODS[method]
        self.duration = duration
        self.delay = delay
        self.pos_delay = pos_delay

    def __call__(self, *args, **kwargs):
        """Calls the resolution method and pass arguments to it.
        """
        return self.METHOD(duration=self.duration, delay=self.delay,
                           pos_delay=self.pos_delay, *args, **kwargs)


@register_resolution_method
def nearest_tonic(mode, tonic, intervals, duration, delay, pos_delay,
                  harmonic=None, descending=None):
    """Resolution method that resolve the intervals to their nearest tonics.

    Args:
        mode (str): Mode of the scale.
        tonic (str): Tonic of the scale. (eg., 'C')
        intervals (str or array_type): Interval or list of intervals to resolve
            to the nearest tonic.
        descending (bool): Are the intervals descending (True) or
            ascending (False).
        duration (float): Duration of the elements of the resolution Sequence.
        delay (float): Delay before the next of the elements of the
            resolution Sequence.
        pos_delay (int): Delay after the Sequence.
    """

    global DIATONIC_MODES, MAX_SEMITONES_RESOLVE_BELOW

    sequence_list = []

    if type(intervals) is not list:
        intervals = [intervals]

    # last_el_idx = len(intervals) - 1
    # for cur_el_idx, interval in enumerate(intervals):
    for interval in intervals:
        resolution_pitch = []
        scale_pitch = DiatonicScale(tonic=tonic, mode=mode,
                                    octave=interval.interval_octave,
                                    descending=descending)

        if interval.chromatic_offset <= MAX_SEMITONES_RESOLVE_BELOW:
            begin_to_diatonic = slice(None, interval.diatonic_index + 1)
            resolution_pitch.extend(scale_pitch.scale[begin_to_diatonic])
            if interval.is_chromatic:
                resolution_pitch.append(interval.note_and_octave)
            resolution_pitch.reverse()
        else:
            diatonic_to_end = slice(interval.diatonic_index, None)
            if interval.is_chromatic:
                resolution_pitch.append(interval.note_and_octave)
            resolution_pitch.extend(scale_pitch.scale[diatonic_to_end])

        # unisson and octave
        if interval.semitones == 0:
            resolution_pitch.append(scale_pitch.scale[0])

        elif interval.semitones % 12 == 0:
            # FIXME: multipe octaves
            resolution_pitch.append("{}{}".format(tonic,
                                    interval.tonic_octave))

        if harmonic:
            seq = [[interval.tonic_note_and_octave, x]
                   for x in resolution_pitch]
        else:
            seq = resolution_pitch

        seq_list = list()
        last_el_idx = len(seq) - 1
        for cur_el_idx, cur_el in enumerate(seq):
            cur_delay = delay if last_el_idx != cur_el_idx else pos_delay
            cur_tuple = (cur_el, duration, cur_delay)
            seq_list.append(cur_tuple)

        cur_delay = delay if last_el_idx != cur_el_idx else pos_delay
        cur_tuple = (cur_el, duration, cur_delay)

        sequence_list.extend(seq_list)

        # sequence_list.append(Sequence(seq, duration=duration, delay=delay,
        #                     pos_delay=pos_delay))

    return Sequence(elements=sequence_list, delay=delay, pos_delay=pos_delay)


@register_resolution_method
def repeat_only(elements, duration, delay, pos_delay):
    """Resolution method that only repeats the sequence elements with given
    durations.

    Args:
        elements (array_type): A list with notes.
        duration (float): Duration of the elements of the resolution Sequence.
        delay (float): Delay before the next of the elements of the
            resolution Sequence.
        pos_delay (int): Delay after the Sequence.
    """

    sequence_list = Sequence(elements, duration=duration, delay=delay,
                             pos_delay=pos_delay)

    return sequence_list
