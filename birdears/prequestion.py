"""This module implements pre-questions' progressions.

Pre questions are chord progressions or notes played before the question is
played, so to affirmate the sound of the question's key.

For example a common cadence is chords I-IV-V-I from the diatonic scale, which
in a key of `C` is `CM-FM-GM-CM` and in a key of `A` is `AM-DM-EM-AM`.

Pre-question methods should be decorated with `register_prequestion_method`
decorator, so that they will be registered as a valid pre-question method.
"""

from .sequence import Sequence

from functools import wraps

PREQUESTION_METHODS = {}
# http://stackoverflow.com/questions/5910703/howto-get-all-methods-of-a-pyt\
# hon-class-with-given-decorator
# http://stackoverflow.com/questions/5707589/calling-functions-by-array-ind\
# ex-in-python/5707605#5707605


def register_prequestion_method(f, *args, **kwargs):
    """Decorator for prequestion method functions.

    Functions decorated with this decorator will be registered in the
    `PREQUESTION_METHODS` global.
    """

    @wraps(f)
    def decorator(*args, **kwargs):
        return f(*args, **kwargs)

    PREQUESTION_METHODS.update({f.__name__: f})

    return decorator


class PreQuestion:

    def __init__(self, method, question):
        """This class implements methods for different types of pre-question
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
        self.question = question

    def __call__(self, *args, **kwargs):
        """Calls the resolution method and pass arguments to it.
        """
        return self.METHOD(question=self.question, *args, **kwargs)


@register_prequestion_method
def none(question, *args, **kwargs):
    return Sequence(duration=0, delay=0, pos_delay=0)


@register_prequestion_method
def tonic_only(question, *args, **kwargs):

    intervals = question.interval if not hasattr(question, 'intervals') else\
                question.intervals
    tonic = question.tonic
    tonic_octave = question.octave

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

    return sequence


@register_prequestion_method
def progression_i_iv_v_i(question, *args, **kwargs):

    tonic = question.tonic
    mode = question.mode
    duration = question.durations['preq']['duration']
    delay = question.durations['preq']['delay']
    pos_delay = question.durations['preq']['pos_delay']

    degrees = [1, 4, 5, 1]

    sequence = Sequence(duration=duration, delay=delay,
                        pos_delay=pos_delay)

    sequence.make_chord_progression(tonic=tonic, mode=mode, degrees=degrees)

    return sequence
