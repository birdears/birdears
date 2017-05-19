from .sequence import Sequence

from functools import wraps

PREQUESTION_METHODS = {}
# http://stackoverflow.com/questions/5910703/howto-get-all-methods-of-a-pyt\
# hon-class-with-given-decorator
# http://stackoverflow.com/questions/5707589/calling-functions-by-array-ind\
# ex-in-python/5707605#5707605


def register_prequestion_method(f, *args, **kwargs):
    """Decorator for resolution method functions.

    Functions decorated with this decorator will be registered in the
    `PREQUESTION_METHODS` global.
    """

    @wraps(f)
    def decorator(*args, **kwargs):
        return f(*args, **kwargs)

    PREQUESTION_METHODS.update({f.__name__: f})

    return decorator


class PreQuestion:

    def __init__(self, method, duration, delay, pos_delay):
        """This class implements methods for different types of pre question
        progressions.

        Args:
            method (str): The method used in the pre question.
            duration (float): Default playing time for each element in the
                resolution.
            delay (float): Default waiting time to play the next element
                in the resolution.
            pos_delay (float): Waiting time after playing the last element
                in the resolution.
        """

        self.METHOD = PREQUESTION_METHODS[method]
        self.resolution_duration = duration
        self.resolution_delay = delay
        self.resolution_pos_delay = pos_delay

    def __call__(self, *args, **kwargs):
        """Calls the resolution method and pass arguments to it.
        """
        return self.METHOD(*args, **kwargs)


@register_prequestion_method
def none(*args, **kwargs):
    return Sequence(duration=0, delay=0, pos_delay=0)


@register_prequestion_method
# FIXME: please refactor lol
def tonic_only(tonic, tonic_octave, intervals, harmonic=None, descending=None,
               duration=None, delay=None, pos_delay=None, *args, **kwargs):
    # harmonic? maybe remove this.

    sequence = Sequence()

    sequence_list = []

    if type(intervals) is not list:
        intervals = [intervals]

    tonic_and_octave = "{}{}".format(tonic, tonic_octave)

    for interval in intervals:
        sequence.append(tonic_and_octave)
        # if not harmonic:
        #     sequence.extend([tonic_and_octave])
        # else:
        #     sequence.append([tonic_and_octave])

    print("sequence {}".format(sequence))
    return sequence


@register_prequestion_method
def progression_i_iv_v_i(tonic, mode, duration=None, delay=None,
                         pos_delay=None, *args, **kwargs):

    degrees = [1, 4, 5, 1]

    sequence = Sequence(duration=duration, delay=delay,
                        pos_delay=pos_delay)

    sequence.make_chord_progression(tonic=tonic, mode=mode, degrees=degrees)

    return sequence
